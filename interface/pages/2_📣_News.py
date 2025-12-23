import streamlit as st
import sys
import time
import feedparser
from pathlib import Path
from typing import List, Dict, Any

sys.path.append(str(Path(__file__).parent.parent.parent))
from core.utils.config_loader import ConfigLoader
from core.writers.digest_engine import DigestEngine
from interface.ui_utils import apply_styles, load_data, save_data, last_updated_component

st.set_page_config(page_title="News Feed", page_icon="📣", layout="wide")
apply_styles()

st.title("📣 AI News Feed")
st.markdown("All news in one place: **Official Blogs**, **Media**, and **Newsletters**.")

# --- Digest Display (Top of Page) ---
digest_data = load_data("news_digest.json")
if digest_data and digest_data.get("content"):
    with st.container():
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%); padding: 20px; border-radius: 12px; margin-bottom: 20px;">
            <h3 style="color: white; margin-bottom: 15px;">📋 今日 AI 速览</h3>
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; color: white; white-space: pre-wrap;">
{digest_data['content']}
            </div>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.8em; margin-top: 10px;">Generated: {digest_data.get('generated_at', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)

def fetch_all_news(config: ConfigLoader, max_per_source: int = 5) -> List[Dict[str, Any]]:
    cfg = config.load()
    all_news = []
    for feed in cfg.news_feeds:
        try:
            parsed = feedparser.parse(feed.url)
            for entry in parsed.entries[:max_per_source]:
                all_news.append({
                    "source": feed.name,
                    "type": feed.type or "unknown",
                    "title": entry.title,
                    "url": entry.link,
                    "published": entry.get('published', 'N/A'),
                    "summary": (entry.get('summary', '') or entry.get('description', ''))[:250] + "..."
                })
        except Exception as e:
            st.warning(f"Could not fetch {feed.name}")
    return all_news

# Sidebar
with st.sidebar:
    st.header("Actions")
    if st.button("📡 Fetch All News", type="primary"):
        with st.spinner("Scanning Official + Media + Newsletters..."):
            try:
                config = ConfigLoader()
                news = fetch_all_news(config, max_per_source=8)
                save_data("news_feed.json", news)
                st.success(f"Found {len(news)} articles!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.markdown("---")
    
    # Digest Button
    if st.button("📝 生成今日 Digest", type="secondary"):
        with st.spinner("AI 正在归纳要点..."):
            try:
                news_data = load_data("news_feed.json")
                if not news_data:
                    st.error("请先抓取 News Feed。")
                else:
                    engine = DigestEngine()
                    digest_content = engine.generate_news_digest(news_data)
                    from datetime import datetime
                    save_data("news_digest.json", {
                        "content": digest_content,
                        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.success("Digest 生成完毕！")
                    time.sleep(1)
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.markdown("---")
    st.header("Filter by Type")
    filter_type = st.radio("Source Type:", ["All", "official", "media"])

last_updated_component("news_feed.json")

# Display
data = load_data("news_feed.json")

if not data:
    st.info("No news yet. Click 'Fetch All News'.")
else:
    filtered = data if filter_type == "All" else [d for d in data if d.get('type') == filter_type]
    
    for n in filtered:
        type_color = "#4CAF50" if n['type'] == 'official' else "#2196F3"
        type_label = "🏢 Official" if n['type'] == 'official' else "📰 Media"
        
        st.markdown(f"""
        <div style="border-left: 4px solid {type_color}; padding: 10px 15px; margin-bottom:12px; background-color: #262730; border-radius: 5px;">
            <div style="font-size:0.8em; color:#aaa;">{type_label} • {n['source']} • {n['published'][:16]}</div>
            <h4 style="margin:5px 0;"><a href="{n['url']}" target="_blank" style="color:white; text-decoration:none;">{n['title']}</a></h4>
            <p style="color:#ccc; font-size:0.9em;">{n['summary']}</p>
        </div>
        """, unsafe_allow_html=True)

