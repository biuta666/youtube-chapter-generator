"""
AI语音克隆 — MOSS-TTS-Nano 全本地零API
chars×3.0公式, min=15帧, 零截断
"""
import streamlit as st
import subprocess, os, tempfile, time

st.set_page_config(page_title="Voice Clone", page_icon="🎤", layout="wide")

PERSONAS = {
    "professional": {"name": "🎙️ 专业主播", "desc": "沉稳大气, 适合新闻/解说", "ref": "G:\\克隆音频\\kelong.mp4"},
    "warm": {"name": "🌸 温暖亲切", "desc": "柔和自然, 适合生活/教程", "ref": "G:\\克隆音频\\kelong.mp4"},
    "sharp": {"name": "⚡ 利落干练", "desc": "语速稍快, 适合财经/快讯", "ref": "G:\\克隆音频\\kelong.mp4"},
    "custom": {"name": "🎛️ 自定义音色", "desc": "上传你自己的参考音频", "ref": None},
}

st.markdown("""
<style>
.big-title { font-size:2.2rem; font-weight:800;
             background:linear-gradient(135deg,#667eea,#48bb78,#1abc9c);
             -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.audio-player { margin:16px 0; padding:12px; background:#f8f9fa; border-radius:12px; }
.stat-row { display:flex; gap:20px; margin:12px 0; }
.stat-box { flex:1; text-align:center; padding:12px; background:#f0f4ff; border-radius:10px; }
.stat-num { font-size:1.4rem; font-weight:800; color:#667eea; }
.stat-label { font-size:0.8rem; color:#888; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">🎤 AI Voice Clone</p>', unsafe_allow_html=True)
st.caption("MOSS-TTS-Nano · Full local · Zero API · No limits")

# Layout
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("### 1. Voice Style")
    persona_key = st.radio("Preset", list(PERSONAS.keys()), 
                            format_func=lambda x: PERSONAS[x]["name"])
    persona = PERSONAS[persona_key]
    
    ref_audio = None
    if persona_key == "custom":
        ref_file = st.file_uploader("Upload reference audio (MP4/mp3/wav, 10-30s clear speech)", 
                                     type=["mp4","mp3","wav","m4a"])
        if ref_file:
            ref_audio = os.path.join(tempfile.gettempdir(), "_voice_ref" + os.path.splitext(ref_file.name)[1])
            with open(ref_audio, "wb") as f:
                f.write(ref_file.read())
            st.audio(ref_audio)
        else:
            st.warning("请上传参考音频")
    else:
        if os.path.exists(persona["ref"]):
            st.success(f"✅ {persona['name']} 已就绪")
            st.caption(persona["desc"])
        else:
            st.warning(f"参考音频未找到: {persona['ref']}")

with col_right:
    st.markdown("### 2. Text to Speak")
    text = st.text_area("Enter your script", height=150,
                         placeholder="大家好，欢迎收看今天的节目...")
    
    chars = len(text.replace(" ","").replace("\n",""))
    st.caption(f"{chars} characters · ~{chars*0.24:.0f}s estimated duration")

# Generate
if st.button("🎤 Generate Speech", use_container_width=True, disabled=(not text.strip())):
    if persona_key != "custom":
        ref_audio = persona["ref"]
    
    if not ref_audio or not os.path.exists(ref_audio):
        st.error("参考音频未就绪")
        st.stop()
    
    chars_count = len(text.replace(" ","").replace("\n",""))
    frames = max(15, int(chars_count * 3.0))  # 修正公式
    
    output = os.path.join(tempfile.gettempdir(), "_voice_out.wav")
    
    with st.spinner(f"Cloning voice... {chars_count} chars → {frames} frames"):
        t0 = time.time()
        
        cmd = [
            "moss-tts-nano", "generate",
            "--backend", "onnx",
            "--device", "cpu",
            "--text", text,
            "--output", output,
            "--mode", "voice_clone",
            "--prompt-speech", ref_audio,
            "--max-new-frames", str(frames),
            "--cpu-threads", "8"
        ]
        
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, 
                             encoding='utf-8', errors='replace', timeout=300)
            elapsed = time.time() - t0
            
            if r.returncode == 0 and os.path.exists(output):
                import soundfile as sf
                dur = len(sf.read(output)[0]) / 48000 if os.path.getsize(output) > 100 else 0
                size_kb = os.path.getsize(output) / 1024
                
                st.success(f"✅ Done! {elapsed:.0f}s")
                
                # Stats
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f'<div class="stat-box"><div class="stat-num">{dur:.1f}s</div><div class="stat-label">Duration</div></div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div class="stat-box"><div class="stat-num">{size_kb:.0f}KB</div><div class="stat-label">File Size</div></div>', unsafe_allow_html=True)
                with c3:
                    speed = chars_count / dur if dur > 0 else 0
                    st.markdown(f'<div class="stat-box"><div class="stat-num">{speed:.1f}</div><div class="stat-label">Chars/sec</div></div>', unsafe_allow_html=True)
                
                # Player
                st.markdown('<div class="audio-player">', unsafe_allow_html=True)
                st.audio(output)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Download
                with open(output, "rb") as f:
                    st.download_button("📥 Download WAV", f.read(), 
                                      file_name="cloned_speech.wav", mime="audio/wav")
            else:
                st.error(f"Generation failed: {r.stderr[-200:] if r.stderr else 'Unknown error'}")
        
        except subprocess.TimeoutExpired:
            st.error("Generation timed out (5 min). Try shorter text.")
        except Exception as e:
            st.error(f"Error: {e}")

# Tips
with st.expander("💡 Tips for best quality"):
    st.markdown("""
    **Reference audio:**
    - 10-30 seconds of clear speech
    - No background music/noise
    - 16kHz mono is ideal
    
    **Text formula:**
    - `max_new_frames = chars × 3.0` (min 15)
    - ~240ms per character
    - Best for texts 50-300 chars
    
    **Persona tips:**
    - Short texts (<20 chars): add padding words for natural flow
    - Long texts (>300 chars): split into segments for best quality
    - Punctuation matters: proper commas and periods create natural pauses
    """)

st.caption("MOSS-TTS-Nano · 0.1B params · ONNX CPU · 48kHz output")
