"""
Creator Toolkit — 统一首页
"""
import streamlit as st

st.set_page_config(page_title="Creator Toolkit", page_icon="🎬", layout="centered")

TOOLS = [
    {"name": "Chapter Generator", "emoji": "📋", "desc": "AI YouTube chapters with visual verification", "url": "http://localhost:8501", "ready": True},
    {"name": "Email Polisher", "emoji": "✉️", "desc": "4 styles: business, friendly, direct, persuasive", "url": "http://localhost:8502", "ready": True},
    {"name": "SBTI Personality", "emoji": "🧠", "desc": "Viral MBTI parody test. 10 personalities.", "url": "http://localhost:8503", "ready": True},
    {"name": "Title Generator", "emoji": "🔥", "desc": "Multi-platform viral titles. YouTube/B站/小红书.", "url": "http://localhost:8504", "ready": True},
    {"name": "Thumbnail Maker", "emoji": "🖼️", "desc": "V22 AI covers. 1:1 to 16:9 zero distortion.", "url": None, "ready": False},
    {"name": "Voice Clone", "emoji": "🎤", "desc": "MOSS-TTS-Nano. chars×3.0 formula. 4 personas.", "url": "http://localhost:8506", "ready": True},
]

st.markdown("""
<style>
.big-title { font-size:2.5rem; font-weight:900; text-align:center;
             background:linear-gradient(135deg,#667eea,#764ba2,#e84393,#fdbb2d);
             -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:0; }
.tool-card { background:white; border-radius:16px; padding:24px; margin:12px 0;
             box-shadow:0 4px 20px rgba(0,0,0,0.06); display:flex; align-items:center;
             gap:16px; transition:all 0.2s; cursor:pointer; text-decoration:none; color:inherit; }
.tool-card:hover { transform:translateY(-2px); box-shadow:0 8px 30px rgba(0,0,0,0.1); }
.tool-emoji { font-size:2.5rem; min-width:60px; text-align:center; }
.tool-name { font-size:1.2rem; font-weight:700; color:#333; }
.tool-desc { font-size:0.9rem; color:#888; }
.tool-badge { font-size:0.7rem; padding:2px 10px; border-radius:12px; margin-left:auto; }
.badge-live { background:#d4edda; color:#155724; }
.badge-wip { background:#fff3cd; color:#856404; }
.count-badge { text-align:center; color:#888; font-size:0.85rem; margin-top:40px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">🎬 Creator Toolkit</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#888;margin-bottom:2rem;'>Free AI tools for content creators. Local, offline, zero API.</p>", unsafe_allow_html=True)

for tool in TOOLS:
    badge = '<span class="tool-badge badge-live">LIVE</span>' if tool["ready"] else '<span class="tool-badge badge-wip">SOON</span>'
    card = f"""
    <div class="tool-card" onclick="window.open('{tool['url']}')">
        <div class="tool-emoji">{tool['emoji']}</div>
        <div>
            <div class="tool-name">{tool['name']}</div>
            <div class="tool-desc">{tool['desc']}</div>
        </div>
        {badge}
    </div>
    """
    st.markdown(card, unsafe_allow_html=True)

ready = sum(1 for t in TOOLS if t["ready"])
st.markdown(f'<p class="count-badge">{ready}/{len(TOOLS)} tools live · 2 coming soon</p>', unsafe_allow_html=True)
st.caption("Built with ❤️ · Streamlit · Whisper · CLIP · MOSS-TTS")
