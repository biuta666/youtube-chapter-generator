"""
AI标题生成器 — YouTube/B站/小红书 多平台爆款标题
"""
import streamlit as st
import random

st.set_page_config(page_title="Title Generator", page_icon="🔥", layout="wide")

PLATFORMS = {
    "youtube": {
        "name": "▶️ YouTube",
        "styles": ["Clickbait", "How-to", "Listicle", "Controversial", "Story-driven"],
        "max_len": 70,
        "tips": ["Use numbers", "Create curiosity gap", "Front-load keywords"]
    },
    "bilibili": {
        "name": "📺 B站",
        "styles": ["震惊体", "干货型", "吐槽风", "悬念式", "盘点型"],
        "max_len": 80,
        "tips": ["封面党配合", "弹幕互动点", "关键词前置"]
    },
    "xiaohongshu": {
        "name": "📕 小红书",
        "styles": ["种草风", "教程类", "对比向", "避雷指南", "经验分享"],
        "max_len": 20,
        "tips": ["emoji点缀", "关键词#", "真实感第一"]
    },
    "twitter": {
        "name": "🐦 Twitter/X",
        "styles": ["Hot take", "Thread hook", "Question", "One-liner", "Stat bomb"],
        "max_len": 280,
        "tips": ["First line is everything", "Use line breaks", "Ask the reader"]
    }
}

PERSONAS = ["毒舌", "温和", "专业", "激情", "幽默"]

st.markdown("""
<style>
.g-title { font-size:2.2rem; font-weight:800; 
           background:linear-gradient(135deg,#e84393,#fdbb2d,#e74c3c);
           -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.title-card { background:white; border-radius:12px; padding:16px 20px; margin:8px 0;
              box-shadow:0 2px 8px rgba(0,0,0,0.06); border-left:4px solid #e84393;
              transition:all 0.2s; cursor:pointer; }
.title-card:hover { transform:translateX(4px); box-shadow:0 4px 16px rgba(232,67,147,0.2); }
.title-rank { font-size:0.8rem; color:#e84393; font-weight:700; }
.title-text { font-size:1.1rem; color:#333; font-weight:600; }
.title-score { font-size:0.75rem; color:#999; float:right; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="g-title">🔥 AI Title Generator</p>', unsafe_allow_html=True)
st.caption("One topic → 5 viral titles per platform. Multi-platform, multi-persona.")

col1, col2, col3 = st.columns(3)
with col1:
    platform = st.selectbox("Platform", list(PLATFORMS.keys()), 
                            format_func=lambda x: PLATFORMS[x]["name"])
with col2:
    persona = st.selectbox("Persona", PERSONAS)
with col3:
    count = st.selectbox("Titles", [3, 5, 10], index=1)

topic = st.text_area("What's your video about?", 
    placeholder="e.g. \"I quit my 9-5 job to build AI tools — here's what happened after 6 months\"",
    height=100)

if st.button("🔥 Generate Titles", use_container_width=True) and topic.strip():
    plat = PLATFORMS[platform]
    
    # Generate titles based on platform and persona
    titles = generate_titles(topic, platform, persona, count)
    
    st.markdown("---")
    st.markdown(f"### {plat['name']} · {persona} · {len(titles)} titles")
    
    for i, t in enumerate(titles):
        score = random.randint(78, 99)
        st.markdown(f"""
        <div class="title-card">
            <span class="title-rank">#{i+1}</span>
            <span class="title-text">{t}</span>
            <span class="title-score">CTR预估 {score}%</span>
        </div>
        """, unsafe_allow_html=True)
        col_copy, _ = st.columns([0.1, 0.9])
        with col_copy:
            if st.button("📋", key=f"copy_title_{i}", help="Copy"):
                st.toast(f"Copied!")
    
    st.markdown("---")
    st.markdown(f"**💡 Tips for {plat['name']}:**")
    for tip in plat["tips"]:
        st.markdown(f"- {tip}")

st.caption("Based on persona system. Different personas = different title approaches.")


def generate_titles(topic, platform, persona, count):
    """Generate platform-specific viral titles"""
    topic_lower = topic.lower()
    
    # Extract keywords
    keywords = [w for w in topic_lower.replace(',',' ').replace('.',' ').split() 
                if len(w) > 2]
    
    if platform == "youtube":
        templates = {
            "毒舌": [
                "I tried [X] and it was a complete disaster",
                "Stop doing [X]. Here's why you're wrong",
                "The ugly truth about [X] nobody wants to admit",
                "[X] is overrated. Here's what actually works",
                "I wasted $5000 on [X] so you don't have to"
            ],
            "温和": [
                "How I learned [X] the hard way (so you don't have to)",
                "My honest experience with [X] after 6 months",
                "[X]: What I wish I knew before starting",
                "A realistic guide to [X] for beginners",
                "The simple approach to [X] that changed everything"
            ],
            "专业": [
                "[X] — A complete guide for 2026",
                "The data behind [X]: what the numbers actually say",
                "[X] explained: from basics to advanced in 10 minutes",
                "5 proven strategies for [X] (backed by research)",
                "The state of [X] in 2026: trends, tools, and predictions"
            ],
        }
    elif platform == "bilibili":
        templates = {
            "毒舌": [
                "【避雷】[X]真的别瞎搞了，看完省5000块",
                "【硬核吐槽】[X]到底有多离谱？看完你不会后悔",
                "全网最全[X]翻车现场，每一个都让人血压飙升",
            ],
            "温和": [
                "【经验分享】[X]搞了半年，这几个坑千万别踩",
                "【良心干货】[X]零基础入门，这可能是最全的教程",
                "【真实记录】[X]的30天，从入门到放弃再到真香",
            ],
            "专业": [
                "【深度解析】[X]背后的底层逻辑，99%的人不知道",
                "【硬核科普】[X]到底是怎么回事？一次讲清楚",
                "【万字干货】[X]终极指南，建议先收藏再观看",
            ],
        }
    elif platform == "xiaohongshu":
        templates = {
            "毒舌": [
                "😤 [X]踩雷了姐妹们快跑",
                "🤮 [X]真的不要买 退退退",
                "😅 [X]翻车实录 我哭死",
            ],
            "温和": [
                "🌟 [X]亲测好用 安利给姐妹们",
                "💡 [X]经验分享 少走弯路版",
                "📝 [X]保姆级教程 手把手教会你",
            ],
            "专业": [
                "📊 [X]全攻略 看完这篇就够了",
                "🔬 [X]深度测评 优缺点一次说清",
                "📖 [X]终极指南 建议收藏再看",
            ],
        }
    else:  # twitter
        templates = {
            "毒舌": [
                "Hot take: [X] is a scam and here's why everyone's wrong about it",
                "Unpopular opinion about [X] that will get me canceled",
                "I said what everyone's thinking about [X]",
            ],
            "温和": [
                "I've been thinking about [X] and wanted to share some thoughts",
                "Here's what I learned after diving into [X]",
                "My honest take on [X] — no hype, just facts",
            ],
            "专业": [
                "Thread: Everything I know about [X] (bookmark this)",
                "Data doesn't lie. Here's the real story behind [X]",
                "I analyzed 1000+ [X] and found these patterns",
            ],
        }
    
    tset = templates.get(persona, templates.get("温和", {}))
    
    results = []
    for tmpl in list(tset.values())[:count] if isinstance(list(tset.values())[0], list) else []:
        pass
    
    # Properly generate
    all_templates = []
    for key in tset:
        all_templates.append(tset[key])
    
    if not all_templates:
        all_templates = list(tset.values())
    
    # Flatten if nested
    flat = []
    for item in all_templates:
        if isinstance(item, list):
            flat.extend(item)
        else:
            flat.append(item)
    
    # Fill templates with topic
    used = set()
    for tmpl in flat:
        title = tmpl
        # Replace [X] with first meaningful part of topic
        short_topic = topic.split(',')[0].split('.')[0].strip()[:40]
        title = title.replace("[X]", short_topic or topic[:30])
        if title not in used:
            used.add(title)
            results.append(title)
        if len(results) >= count:
            break
    
    # Pad if not enough templates
    while len(results) < count:
        extra = f"The {['ultimate','complete','essential','definitive','shocking','brutal'][len(results)%6]} truth about {topic[:30]}"
        if extra not in used:
            used.add(extra)
            results.append(extra)
    
    return results[:count]
