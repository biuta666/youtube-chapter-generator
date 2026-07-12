"""
SBTI — Silly Big Test I 搞笑人格测试
中国梗出海: MBTI恶搞版, Reddit/TikTok病毒传播
"""
import streamlit as st
import random, time

st.set_page_config(page_title="SBTI Test", page_icon="🧠", layout="centered")

PERSONALITIES = {
    "DEAD": {
        "full": "Dead Inside Every Afternoon Definitely",
        "emoji": "💀",
        "desc": "You peaked at 10am. After lunch you're a zombie. Your superpower: staring at spreadsheets without processing a single cell.",
        "color": "#6c757d",
        "vibe": "Monday energy, 7 days a week"
    },
    "MALO": {
        "full": "Maximum Awkward Loud Overthinker",
        "emoji": "🤡",
        "desc": "You say 'you too' when the waiter says 'enjoy your meal'. You rehearse phone calls. Your brain runs 47 scenarios before sending a text.",
        "color": "#e74c3c",
        "vibe": "Anxiety's favorite child"
    },
    "SHIT": {
        "full": "Somehow Handling It Together",
        "emoji": "🦝",
        "desc": "You have no idea what you're doing but somehow things work out. Pure chaos energy with suspiciously good luck.",
        "color": "#7d6b5d",
        "vibe": "Trash panda philosophy"
    },
    "GOAT": {
        "full": "Grinding Obsessively At Terminal",
        "emoji": "🐐",
        "desc": "You shipped 3 features while reading this. Sleep is optional. Coffee is a food group. Your GitHub contribution graph is solid green.",
        "color": "#27ae60",
        "vibe": "Built different, literally"
    },
    "NOOB": {
        "full": "Naturally Oblivious Optimistic Being",
        "emoji": "🐣",
        "desc": "You just learned what Ctrl+C does yesterday and already deployed to production. Ignorance is bliss and also terrifying.",
        "color": "#f39c12",
        "vibe": "Confidently incorrect"
    },
    "RAGE": {
        "full": "Reacts Aggressively Generally Everywhere",
        "emoji": "😤",
        "desc": "Minor inconvenience? Full meltdown. Someone merged without review? Nuclear launch detected. You're 3 pixels away from quitting everything.",
        "color": "#e67e22",
        "vibe": "Perpetual fight mode"
    },
    "CHAD": {
        "full": "Confidently Happy Always Delusional",
        "emoji": "🗿",
        "desc": "You think you're the main character. Maybe you are. Reality hasn't caught up yet and honestly it might never.",
        "color": "#2980b9",
        "vibe": "Giga chad energy"
    },
    "SIMP": {
        "full": "Sweet Innocent Mild Pushover",
        "emoji": "🥺",
        "desc": "You say 'sorry' to inanimate objects. You let people cut in line. Your browser has 47 tabs you'll 'read later'.",
        "color": "#9b59b6",
        "vibe": "Too pure for this world"
    },
    "YOLO": {
        "full": "Yearning Openly Living Optimistically",
        "emoji": "🚀",
        "desc": "You quit jobs on impulse. You book flights without checking the date. Your retirement plan is 'figure it out later'. Respect.",
        "color": "#1abc9c",
        "vibe": "Main character syndrome, season finale"
    },
    "MEOW": {
        "full": "Minimal Effort Often Wins",
        "emoji": "🐱",
        "desc": "You do the absolute minimum and somehow outperform everyone. You've turned laziness into an art form. Efficiency through apathy.",
        "color": "#e84393",
        "vibe": "Cats did it first"
    },
}

QUESTIONS = [
    {
        "q": "It's Monday morning. What do you do?",
        "options": [
            ("😴 Hit snooze 7 times", "DEAD"),
            ("💻 Open laptop at 6am already coding", "GOAT"),
            ("🤔 Google 'how to quit job' again", "RAGE"),
            ("🐱 Stay in bed, work from phone", "MEOW"),
        ]
    },
    {
        "q": "Someone says your code has a bug.",
        "options": [
            ("😤 It's not a bug, it's a feature", "RAGE"),
            ("🥺 I'm sorry I'll fix it right now", "SIMP"),
            ("🤷 It works on my machine", "SHIT"),
            ("🗿 Bug? Where? I see perfection", "CHAD"),
        ]
    },
    {
        "q": "You have 3 deadlines today.",
        "options": [
            ("💀 Stare at wall for 2 hours first", "DEAD"),
            ("📝 Already submitted all 3 yesterday", "GOAT"),
            ("🍿 Procrastinate then panic-finish in 30min", "YOLO"),
            ("😰 Rehearse 47 apology emails", "MALO"),
        ]
    },
    {
        "q": "How do you handle a crush?",
        "options": [
            ("😳 Never tell them, pine silently for years", "MALO"),
            ("🥰 Tell them immediately, what's the worst that could happen", "CHAD"),
            ("📱 Analyze every text for hidden meanings", "MALO"),
            ("🐣 Wait... people date?", "NOOB"),
        ]
    },
    {
        "q": "It's 3am. You are...",
        "options": [
            ("💻 Still coding", "GOAT"),
            ("😴 What's 3am? I sleep at 9pm", "DEAD"),
            ("🧠 Overthinking every life choice since 2008", "MALO"),
            ("🎮 Gaming. Tomorrow's problem.", "SHIT"),
        ]
    },
    {
        "q": "The waiter says 'enjoy your meal'.",
        "options": [
            ("😊 'Thanks, you too!' — wait...", "MALO"),
            ("🤐 Silent nod", "DEAD"),
            ("🗿 'I always do'", "CHAD"),
            ("😨 Panic and leave", "SIMP"),
        ]
    },
    {
        "q": "Your life motto is:",
        "options": [
            ("💀 'It is what it is'", "DEAD"),
            ("🐐 'Sleep is for the weak'", "GOAT"),
            ("🦝 'We ball' (barely)", "SHIT"),
            ("🚀 'YOLO, deal with consequences later'", "YOLO"),
        ]
    },
]

st.markdown("""
<style>
.big-title { font-size:3rem; font-weight:900; text-align:center; 
             background:linear-gradient(135deg,#667eea,#e84393,#fdbb2d);
             -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.subtitle { text-align:center; color:#888; font-size:1rem; margin-bottom:2rem; }
.result-card {
    text-align:center; padding:30px; border-radius:20px; margin:20px 0;
    box-shadow:0 8px 32px rgba(0,0,0,0.12);
    animation:fadeIn 0.6s ease;
}
.result-emoji { font-size:5rem; }
.result-type { font-size:2.5rem; font-weight:900; letter-spacing:4px; margin:10px 0; }
.result-full { font-size:1.2rem; color:#666; font-style:italic; margin-bottom:16px; }
.result-desc { font-size:1.1rem; line-height:1.7; max-width:500px; margin:0 auto; }
.result-vibe { margin-top:12px; font-size:0.9rem; padding:6px 16px; border-radius:20px; display:inline-block; }
.share-box { background:#1e1e1e; color:#0f0; padding:16px; border-radius:12px; 
             font-family:monospace; font-size:0.85rem; margin-top:16px; text-align:left; }
@keyframes fadeIn { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
.question-card { background:white; border-radius:12px; padding:24px; margin:16px 0;
                 box-shadow:0 2px 12px rgba(0,0,0,0.06); }
.stButton>button { width:100%; padding:16px; font-size:1.2rem; font-weight:700;
                   background:linear-gradient(135deg,#667eea,#e84393); color:white; border:none; border-radius:12px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">🧠 SBTI</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Silly Big Test I — the personality test that judges you, MBTI style, but worse</p>', unsafe_allow_html=True)

if "stage" not in st.session_state:
    st.session_state.stage = "start"
    st.session_state.answers = []

# START
if st.session_state.stage == "start":
    st.markdown("### " + "\n")
    name = st.text_input("Your name (optional)", placeholder="Anonymous chaos agent")
    
    if st.button("🔮 Reveal My True Self", use_container_width=True):
        st.session_state.name = name or "Anonymous"
        st.session_state.stage = "quiz"
        st.session_state.q_index = 0
        st.session_state.answers = []
        st.rerun()

# QUIZ
elif st.session_state.stage == "quiz":
    qi = st.session_state.q_index
    q = QUESTIONS[qi]
    
    progress = (qi+1) / len(QUESTIONS)
    st.progress(progress, f"Question {qi+1}/{len(QUESTIONS)}")
    
    st.markdown(f'<div class="question-card"><h3>{q["q"]}</h3></div>', unsafe_allow_html=True)
    
    for emoji_text, trait in q["options"]:
        if st.button(emoji_text, key=f"q{qi}_{trait}", use_container_width=True):
            st.session_state.answers.append(trait)
            if qi + 1 < len(QUESTIONS):
                st.session_state.q_index += 1
            else:
                st.session_state.stage = "result"
            st.rerun()

# RESULT
elif st.session_state.stage == "result":
    from collections import Counter
    tally = Counter(st.session_state.answers)
    top_trait = tally.most_common(1)[0][0]
    p = PERSONALITIES[top_trait]
    
    # Fun: sometimes random
    if random.random() < 0.15:
        top_trait = random.choice(list(PERSONALITIES.keys()))
        p = PERSONALITIES[top_trait]
    
    st.markdown(f"""
    <div class="result-card" style="border:3px solid {p['color']}">
        <div class="result-emoji">{p['emoji']}</div>
        <div class="result-type" style="color:{p['color']}">{top_trait}</div>
        <div class="result-full">{p['full']}</div>
        <div class="result-desc">{p['desc']}</div>
        <div class="result-vibe" style="background:{p['color']}20;color:{p['color']}">
            {p['vibe']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📋 Share your SBTI result")
    share_text = f"""🧠 My SBTI: {top_trait} ({p['full']})
{p['emoji']} "{p['vibe']}"
{p['desc'][:100]}...
        
Find yours: sbti.ai"""
    st.code(share_text, language=None)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.stage = "start"
            st.rerun()
    with col2:
        if st.button("📋 Copy Result", use_container_width=True):
            st.toast("Copied!")

# Footer
st.markdown("---")
st.markdown("SBTI = Silly Big Test I • Based on actual Chinese internet meme culture • MBTI's chaotic cousin")
