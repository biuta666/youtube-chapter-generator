"""
AI邮件润色器 — 3种风格一键切换
基于 persona_manager 人设系统
"""
import streamlit as st

st.set_page_config(page_title="Email Polisher", page_icon="✉️", layout="wide")

STYLES = {
    "business": {
        "name": "💼 正式商务",
        "prompt": "Rewrite this email in professional business tone. Use formal language, clear structure, polite opening/closing. Keep the original meaning.",
        "color": "#667eea"
    },
    "friendly": {
        "name": "😊 亲切友好",
        "prompt": "Rewrite this email in warm friendly tone. Use casual but respectful language, add a personal touch, make it feel genuine. Keep the original meaning.",
        "color": "#48bb78"
    },
    "direct": {
        "name": "⚡ 简洁直接",
        "prompt": "Rewrite this email to be ultra-concise. Remove all fluff, get straight to the point. Maximum 5 sentences. Keep the original meaning.",
        "color": "#ed8936"
    },
    "persuasive": {
        "name": "🎯 说服力",
        "prompt": "Rewrite this email to be persuasive and compelling. Use power words, create urgency, include a clear call to action. Keep the original meaning.",
        "color": "#9f7aea"
    }
}

LANGUAGES = ["English", "中文", "日本語", "한국어"]

# CSS
st.markdown("""
<style>
.header { font-size:2rem; font-weight:800; background:linear-gradient(135deg,#667eea,#48bb78); 
          -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:0.3rem; }
.version-card {
    background:white; border-radius:12px; padding:20px; margin:8px 0;
    border-left:4px solid #667eea; box-shadow:0 2px 8px rgba(0,0,0,0.08);
    transition:all 0.2s;
}
.version-card:hover { transform:translateY(-2px); box-shadow:0 4px 16px rgba(0,0,0,0.12); }
.version-label { font-size:0.85rem; color:#888; margin-bottom:4px; }
.version-text { font-size:1rem; color:#333; white-space:pre-wrap; line-height:1.6; }
.char-count { font-size:0.8rem; color:#999; float:right; }
.copy-btn { float:right; margin-top:-28px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="header">✉️ AI Email Polisher</p>', unsafe_allow_html=True)
st.caption("Paste a draft → get 3 polished versions. Copy the best one.")

# Input
col1, col2 = st.columns([3, 1])
with col1:
    draft = st.text_area("", placeholder="Paste your email draft here...", height=200, label_visibility="collapsed")
with col2:
    active_styles = st.multiselect("Style", list(STYLES.keys()), default=["business","friendly","direct"],
                                    format_func=lambda x: STYLES[x]["name"])
    lang = st.selectbox("Language", LANGUAGES, index=0)

# Generate
if st.button("✨ Polish Email", use_container_width=True) and draft.strip():
    original_chars = len(draft)
    
    st.markdown("---")
    st.markdown(f"### Results ({original_chars} chars)")
    
    for i, style_key in enumerate(active_styles):
        style = STYLES[style_key]
        
        # Simulate LLM polish (in production: call LLM API with style["prompt"])
        # For demo: apply basic transformations based on style
        result = polish_email(draft, style_key, lang)
        
        with st.container():
            st.markdown(f"""
            <div class="version-card" style="border-left-color:{style['color']}">
                <div class="version-label">{style['name']} · {len(result)} chars</div>
                <div class="version-text">{result}</div>
            </div>
            """, unsafe_allow_html=True)
            col_a, col_b = st.columns([0.9, 0.1])
            with col_b:
                if st.button("📋", key=f"copy_{style_key}", help="Copy"):
                    st.toast(f"Copied {style['name']}!")

st.caption("Tip: Results are simulated in demo mode. Connect LLM API for real polish.")


def polish_email(text, style, lang):
    """Apply style transformations to email text"""
    if style == "direct":
        # Keep first and last 2 sentences, plus key middle
        sents = [s.strip() for s in text.replace('\n','. ').split('.') if s.strip()]
        if len(sents) <= 5:
            return text
        result = '. '.join(sents[:2]) + '. ' + '. '.join(sents[-2:])
        return result[:500] + ('.' if not result.endswith('.') else '')
    
    elif style == "business":
        lines = text.strip().split('\n')
        # Add formal greeting if missing
        has_greeting = any(w.lower() in lines[0].lower() for w in ['dear','hi','hello','尊敬的','您好'])
        has_closing = any(w.lower() in (lines[-1] if lines else '').lower() 
                         for w in ['regards','sincerely','best','谢谢','此致'])
        
        result_lines = []
        if not has_greeting:
            result_lines.append("Dear [Name],\n")
        result_lines.extend(lines)
        if not has_closing:
            result_lines.append("\nBest regards,\n[Your Name]")
        
        result = '\n'.join(result_lines)
        # Remove exclamation marks for formal tone
        result = result.replace('!', '.').replace('!!', '.')
        return result
    
    elif style == "friendly":
        # Add friendly touches
        lines = text.strip().split('\n')
        has_greeting = any(w.lower() in lines[0].lower() for w in ['dear','hi','hello','hey'])
        
        result_lines = []
        if not has_greeting:
            result_lines.append("Hi there! 👋\n")
        result_lines.extend(lines)
        # Add friendly closing if not present
        last = lines[-1].strip() if lines else ""
        if not any(w.lower() in last.lower() for w in ['thanks','cheers','best','talk']):
            result_lines.append("\nThanks so much! 😊")
        
        return '\n'.join(result_lines)
    
    elif style == "persuasive":
        result = text
        # Add persuasive elements
        if "?" not in result:
            result = result.rstrip('.') + " — would you be interested in discussing further?"
        # Add urgency
        if "limited" not in result.lower() and "deadline" not in result.lower():
            result += "\n\nI'd love to get your thoughts before [date] if possible."
        return result
    
    return text
