"""
Creator Toolkit — YouTube章节生成器 Web版
Streamlit前端, 部署到HuggingFace Spaces
"""
import streamlit as st
import os, sys, json, tempfile, time

# 导入引擎
sys.path.insert(0, os.path.dirname(__file__))
from chapter_engine import run as gen_chapters

st.set_page_config(
    page_title="YouTube Chapter Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====== CSS ======
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #888;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .chapter-row {
        display: flex;
        align-items: center;
        padding: 8px 12px;
        border-radius: 8px;
        margin: 4px 0;
        background: #f8f9fa;
        transition: all 0.2s;
    }
    .chapter-row:hover {
        background: #e9ecef;
        transform: translateX(4px);
    }
    .chapter-time {
        font-family: 'Courier New', monospace;
        font-weight: 700;
        font-size: 1.1rem;
        color: #667eea;
        min-width: 70px;
    }
    .chapter-star {
        color: #ffd700;
        font-size: 1.2rem;
        margin-right: 8px;
    }
    .chapter-title {
        flex: 1;
        font-size: 1rem;
        color: #333;
    }
    .chapter-dur {
        font-size: 0.8rem;
        color: #999;
        margin-left: 12px;
    }
    .copy-box {
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 16px;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        white-space: pre-wrap;
        max-height: 400px;
        overflow-y: auto;
    }
    .stat-card {
        text-align: center;
        padding: 16px;
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 12px;
        border: 1px solid #dee2e6;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 800;
        color: #667eea;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #888;
    }
    .verified-badge {
        background: #d4edda;
        color: #155724;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 40px;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 12px;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(102,126,234,0.4);
    }
</style>
""", unsafe_allow_html=True)

# ====== Header ======
st.markdown('<p class="main-header">🎬 YouTube Chapter Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-powered chapter detection with visual+audio dual verification. Free, offline, zero API.</p>', unsafe_allow_html=True)

# ====== Input ======
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    method = st.radio("输入方式", ["📤 上传视频", "🔗 YouTube链接", "📄 已有SRT字幕"],
                      horizontal=True, label_visibility="collapsed")
with col2:
    model = st.selectbox("Whisper模型", ["small", "medium", "large-v3"], index=1,
                         help="medium=推荐, small=更快, large=最准")
with col3:
    gap = st.slider("章节间隔(秒)", 10, 60, 20,
                    help="20秒=标准, 更小=更多章节")

video_file = None
youtube_url = ""
srt_file = None

if "📤" in method:
    video_file = st.file_uploader("选择视频文件", type=["mp4","mkv","webm","mov","avi"])
elif "🔗" in method:
    youtube_url = st.text_input("粘贴YouTube链接", placeholder="https://www.youtube.com/watch?v=...")
else:
    srt_file = st.file_uploader("上传SRT字幕", type=["srt","vtt"])

# ====== Generate Button ======
if st.button("⚡ 生成章节", use_container_width=True):
    video_path = None
    srt_path = None
    
    # 准备文件
    if srt_file:
        srt_path = os.path.join(tempfile.gettempdir(), "_upload.srt")
        with open(srt_path, "wb") as f:
            f.write(srt_file.read())
    
    if video_file:
        video_path = os.path.join(tempfile.gettempdir(), "_upload_video"+os.path.splitext(video_file.name)[1])
        with open(video_path, "wb") as f:
            f.write(video_file.read())
    
    if not video_path and not youtube_url and not srt_path:
        st.error("请先选择输入方式")
        st.stop()
    
    # 生成
    with st.spinner("AI分析中... 音频转录 + 章节边界检测 + 标题生成"):
        try:
            t0 = time.time()
            chapters = gen_chapters(
                video_path=video_path,
                url=youtube_url if youtube_url else None,
                srt_path=srt_path,
                model=model,
                gap=gap
            )
            elapsed = time.time() - t0
            
            st.session_state.chapters = chapters
            st.session_state.elapsed = elapsed
            
        except Exception as e:
            st.error(f"生成失败: {e}")
            st.stop()
    
    st.success(f"✅ 完成! 耗时 {elapsed:.0f}秒")

# ====== Results ======
if "chapters" in st.session_state and st.session_state.chapters:
    chapters = st.session_state.chapters
    elapsed = st.session_state.elapsed
    
    # Stats
    verified = sum(1 for c in chapters if c["verified"])
    total_dur = sum(c["duration_sec"] for c in chapters)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{len(chapters)}</div><div class="stat-label">章节数</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{verified}</div><div class="stat-label">⭐ 视觉验证</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{total_dur//60}:{total_dur%60:02d}</div><div class="stat-label">总时长</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{elapsed:.0f}s</div><div class="stat-label">处理耗时</div></div>', unsafe_allow_html=True)
    
    # Chapters preview
    st.markdown("---")
    st.markdown("### 📋 章节预览 (可编辑)")
    
    edited = []
    for i, ch in enumerate(chapters):
        cols = st.columns([1, 8, 2, 1])
        with cols[0]:
            if ch["verified"]:
                st.markdown(f"⭐")
        with cols[1]:
            new_title = st.text_input(f"title_{i}", ch["title"], 
                                       label_visibility="collapsed",
                                       key=f"edit_{i}")
        with cols[2]:
            st.markdown(f'<code style="background:#f0f0f0;padding:4px 8px;border-radius:4px;">{ch["timestamp"]}</code>', unsafe_allow_html=True)
        with cols[3]:
            st.markdown(f'<span style="color:#999;font-size:0.8rem;">{ch["duration_sec"]//60}:{ch["duration_sec"]%60:02d}</span>', unsafe_allow_html=True)
        edited.append(new_title)
    
    # Generate YouTube format
    youtube_lines = ["00:00 开场"]
    for i, ch in enumerate(chapters):
        star = "⭐ " if ch["verified"] else ""
        youtube_lines.append(f"{star}{ch['timestamp']} {edited[i]}")
    youtube_text = "\n".join(youtube_lines)
    
    # Copy box
    st.markdown("---")
    st.markdown("### 📋 YouTube格式 (直接粘贴到视频描述栏)")
    st.code(youtube_text, language="markdown")
    
    # Download buttons
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.download_button("📥 下载 chapters.txt", youtube_text, 
                          file_name="chapters.txt", mime="text/plain")
    with col_b:
        st.download_button("📥 下载 chapters.json", 
                          json.dumps(chapters, ensure_ascii=False, indent=2),
                          file_name="chapters.json", mime="application/json")
    with col_c:
        if st.button("📋 复制到剪贴板"):
            st.toast("已复制! 可粘贴到YouTube描述栏", icon="✅")
            st.markdown(f"""<script>navigator.clipboard.writeText(`{youtube_text}`);</script>""", unsafe_allow_html=True)

# ====== Footer ======
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#999;font-size:0.8rem;">
    Built with ❤️ | 全本地零API | <a href="https://github.com">GitHub</a> | 
    <a href="#">Pro版去水印</a> $4.99/月
</div>
""", unsafe_allow_html=True)
