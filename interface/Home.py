import streamlit as st

st.set_page_config(
    page_title="AI Trend Radar",
    page_icon="🪐",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 3em;
        font-weight: 700;
        background: linear-gradient(90deg, #667EEA 0%, #764BA2 50%, #F093FB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #aaa;
        font-size: 1.2em;
        margin-bottom: 40px;
    }
    .nav-box {
        background-color: #1a1c24;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #333;
        transition: all 0.3s;
    }
    .nav-box:hover {
        border-color: #667EEA;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🪐 AI Trend Radar</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your unified dashboard for AI intelligence.</p>', unsafe_allow_html=True)

st.markdown("---")

# Navigation Cards
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="nav-box">
        <h3>📜 Research</h3>
        <p style="color:#aaa;">Top ArXiv papers filtered by influential authors, organizations, and code signals.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="nav-box">
        <h3>🛠️ Products</h3>
        <p style="color:#aaa;">New AI tools and products. Product Hunt, There's An AI For That.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="nav-box">
        <h3>🎧 Podcasts</h3>
        <p style="color:#aaa;">Interviews with AI leaders. Lex Fridman, Dwarkesh, Latent Space.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="nav-box">
        <h3>📣 News</h3>
        <p style="color:#aaa;">Official blogs, newsletters, and media coverage. All in one feed.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="nav-box">
        <h3>💬 Discourse</h3>
        <p style="color:#aaa;">Community discussions. Reddit, Hacker News, Alignment Forum.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center; color:#666;'>Use the sidebar to navigate between modules. Each module has its own fetch button.</p>", unsafe_allow_html=True)
