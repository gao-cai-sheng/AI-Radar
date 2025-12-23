import streamlit as st
import sys
import time
import feedparser
from pathlib import Path
from typing import List, Dict, Any

sys.path.append(str(Path(__file__).parent.parent.parent))
from core.utils.config_loader import ConfigLoader
from interface.ui_utils import apply_styles, load_data, save_data, last_updated_component

st.set_page_config(page_title="Community Discourse", page_icon="💬", layout="wide")
apply_styles()

st.title("💬 Community Discourse")
st.markdown("Grassroots discussions from **Reddit**, **Hacker News**, and **Alignment Forums**.")

def fetch_discourse(config: ConfigLoader, max_per_source: int = 8) -> List[Dict[str, Any]]:
    cfg = config.load()
    posts = []
    for feed in cfg.discourse_sources:
        try:
            parsed = feedparser.parse(feed.url)
            for entry in parsed.entries[:max_per_source]:
                posts.append({
                    "source": feed.name,
                    "type": feed.type or "unknown",
                    "title": entry.title,
                    "url": entry.link,
                    "published": entry.get('published', 'N/A'),
                    "summary": (entry.get('summary', '') or entry.get('description', ''))[:250] + "..."
                })
        except Exception as e:
            pass # Silent fail for individual feeds
    return posts

# Sidebar
with st.sidebar:
    st.header("Actions")
    if st.button("🔥 Scan Communities", type="primary"):
        with st.spinner("Browsing Reddit, HN, Forums..."):
            try:
                config = ConfigLoader()
                posts = fetch_discourse(config)
                save_data("discourse.json", posts)
                st.success(f"Found {len(posts)} discussions!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.markdown("---")
    st.header("Filter by Type")
    filter_type = st.radio("Source Type:", ["All", "reddit", "hn", "forum"])

last_updated_component("discourse.json")

# Display
data = load_data("discourse.json")

if not data:
    st.info("No discussions yet. Click 'Scan Communities'.")
else:
    filtered = data if filter_type == "All" else [d for d in data if d.get('type') == filter_type]
    
    type_colors = {"reddit": "#FF4500", "hn": "#FF6600", "forum": "#4CAF50"}
    type_icons = {"reddit": "🔴", "hn": "🟠", "forum": "🟢"}
    
    col1, col2 = st.columns(2)
    for i, p in enumerate(filtered):
        c = type_colors.get(p['type'], '#888')
        icon = type_icons.get(p['type'], '💬')
        
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div style="background-color: #1a1a1b; padding: 12px; border-radius: 5px; margin-bottom:10px; border-left: 4px solid {c};">
                <div style="font-size:0.75em; color:#818384;">{icon} {p['source']}</div>
                <h4 style="margin:5px 0;"><a href="{p['url']}" target="_blank" style="color:#D7DADC; text-decoration:none;">{p['title']}</a></h4>
                <a href="{p['url']}" target="_blank" style="color:{c}; font-size:0.85em;">Join Discussion →</a>
            </div>
            """, unsafe_allow_html=True)
