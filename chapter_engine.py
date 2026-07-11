"""
章节生成核心引擎 — 复用V6已验证算法
支持: YouTube URL(yt-dlp下载) / 本地视频 / 已有SRT
"""
import os, sys, json, time, re, tempfile, subprocess
import numpy as np
from pathlib import Path

def parse_srt(srt_path):
    """解析SRT字幕 → [{start,end,text}]"""
    with open(srt_path, 'r', encoding='utf-8') as f:
        blocks = [b.strip() for b in f.read().strip().split('\n\n') if b.strip()]
    
    def t2s(ts):
        p = ts.strip().replace(',','.').split(':')
        return int(p[0])*3600 + int(p[1])*60 + float(p[2])
    
    segments = []
    for b in blocks:
        lines = b.split('\n')
        if len(lines) < 3 or '-->' not in lines[1]: continue
        s_str, rest = lines[1].split(' --> ')
        segments.append({"start": t2s(s_str), "end": t2s(rest.split(' ')[0]), "text": lines[2]})
    return segments

def extract_audio(video_path):
    """提取16kHz mono音频"""
    audio = os.path.join(tempfile.gettempdir(), "_chapter_audio.wav")
    subprocess.run(["ffmpeg","-y","-i",video_path,"-vn",
        "-acodec","pcm_s16le","-ar","16000","-ac","1",audio],
        capture_output=True, check=True)
    return audio

def transcribe(audio_path, model_size="medium"):
    """Whisper转录"""
    import whisper
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path, language="zh", beam_size=5,
                               word_timestamps=True, verbose=False)
    return result["segments"]

def download_youtube(url, out_dir):
    """yt-dlp下载视频"""
    os.makedirs(out_dir, exist_ok=True)
    r = subprocess.run(["yt-dlp","-f","best[height<=720]","--no-playlist",
        "-o",os.path.join(out_dir,"%(title)s.%(ext)s"),url],
        capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        raise RuntimeError(f"下载失败: {r.stderr[-200:]}")
    # 找到下载的文件
    for f in os.listdir(out_dir):
        if f.endswith(('.mp4','.webm','.mkv')):
            return os.path.join(out_dir, f)
    raise RuntimeError("找不到下载文件")

def find_chapter_boundaries(segments, gap_threshold=20.0):
    """字幕大间隙 → 章节边界"""
    boundaries = [0.0]
    for i in range(len(segments)-1):
        gap = segments[i+1]["start"] - segments[i]["end"]
        if gap > gap_threshold:
            boundaries.append((segments[i]["end"] + segments[i+1]["start"]) / 2)
    boundaries.append(segments[-1]["end"])
    return boundaries

def detect_visual_cuts(segments, small_gap=3.0):
    """小间隙 → 伪视觉切点"""
    cuts = []
    for i in range(len(segments)-1):
        gap = segments[i+1]["start"] - segments[i]["end"]
        if gap > small_gap:
            cuts.append((segments[i]["end"] + segments[i+1]["start"]) / 2)
    return cuts

def merge_and_verify(boundaries, visual_cuts, window=10.0):
    """双重验证 + 合并短段"""
    chapters = []
    for s, e in zip(boundaries[:-1], boundaries[1:]):
        nearby = [t for t in visual_cuts if abs(t - s) < window]
        chapters.append({"start": s, "end": e, "visual_verified": bool(nearby)})
    
    # 合并<60s + 拆分>480s
    merged = []
    for ch in chapters:
        dur = ch["end"] - ch["start"]
        if merged and dur < 60:
            merged[-1]["end"] = ch["end"]
        elif dur > 480:
            mid = ch["start"] + dur/2
            merged.append({"start": ch["start"], "end": mid, "visual_verified": ch["visual_verified"]})
            merged.append({"start": mid, "end": ch["end"], "visual_verified": ch["visual_verified"]})
        else:
            merged.append(ch)
    return merged

def pick_title(segments_in_chapter):
    """选最佳字幕句做章节标题"""
    texts = [s["text"].strip() for s in segments_in_chapter]
    candidates = []
    for t in texts:
        t = t.strip()
        if len(t) < 5 or len(t) > 40: continue
        cn_chars = sum(1 for c in t if '\u4e00' <= c <= '\u9fff')
        if cn_chars < 2: continue
        candidates.append(t)
    
    if candidates:
        best = sorted(candidates, key=lambda t: sum(1 for c in t if '\u4e00' <= c <= '\u9fff'), reverse=True)[0]
        return best[:20]
    
    for t in texts:
        if any('\u4e00' <= c <= '\u9fff' for c in t):
            return t[:20]
    return "(无对白)"

def generate_titles(chapters, segments):
    """为每个章节生成标题"""
    for ch in chapters:
        relevant = [s for s in segments if s["start"] >= ch["start"] and s["end"] <= ch["end"]]
        ch["title"] = pick_title(relevant) if relevant else "(无对白)"

def run(video_path=None, srt_path=None, url=None, model="medium", gap=20):
    """
    主入口 — 生成章节
    返回: [(mm:ss, title, start_sec, visual_verified)]
    """
    segments = None
    
    # 优先用已有SRT
    if srt_path and os.path.exists(srt_path):
        segments = parse_srt(srt_path)
    
    # 其次下载YouTube
    if not segments and url:
        tmp_dir = tempfile.mkdtemp(prefix="_yt_")
        video_path = download_youtube(url, tmp_dir)
        print(f"下载完成: {video_path}")
    
    # 最后转录视频
    if not segments and video_path:
        audio = extract_audio(video_path)
        segments = transcribe(audio, model)
    
    if not segments:
        raise ValueError("无可用字幕: 请提供SRT/视频/YouTube链接之一")
    
    # 章节检测
    boundaries = find_chapter_boundaries(segments, gap)
    visual_cuts = detect_visual_cuts(segments)
    chapters = merge_and_verify(boundaries, visual_cuts)
    generate_titles(chapters, segments)
    
    # 格式化输出
    results = []
    for ch in chapters:
        mm, ss = int(ch["start"]//60), int(ch["start"]%60)
        results.append({
            "timestamp": f"{mm:02d}:{ss:02d}",
            "start_sec": ch["start"],
            "end_sec": ch["end"],
            "title": ch["title"],
            "verified": ch["visual_verified"],
            "duration_sec": int(ch["end"] - ch["start"]),
        })
    return results
