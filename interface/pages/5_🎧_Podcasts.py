import streamlit as st
import sys
import time
import feedparser
from pathlib import Path
from typing import List, Dict, Any

sys.path.append(str(Path(__file__).parent.parent.parent))
from core.utils.config_loader import ConfigLoader
from interface.ui_utils import apply_styles, load_data, save_data, last_updated_component

st.set_page_config(page_title="Podcasts", page_icon="🎧", layout="wide")
apply_styles()

st.title("🎧 AI Podcasts & Interviews")
st.markdown("Deep dives with **Industry Leaders** and **Researchers**. Lex Fridman, Dwarkesh, Latent Space, and more.")

def fetch_podcasts(config: ConfigLoader, max_per_source: int = 5) -> List[Dict[str, Any]]:
    cfg = config.load()
    watchlist = set(a.name.lower() for a in cfg.authors)
    episodes = []
    
    for feed in cfg.podcast_sources:
        try:
            parsed = feedparser.parse(feed.url)
            for entry in parsed.entries[:max_per_source]:
                title = entry.title
                summary = entry.get('summary', '') or entry.get('description', '')
                full_text = (title + " " + summary).lower()
                
                # Check for guest matches
                detected_guests = [n.title() for n in watchlist if n in full_text]
                
                episodes.append({
                    "source": feed.name,
                    "title": title,
                    "url": entry.link,
                    "published": entry.get('published', 'N/A'),
                    "summary": summary[:200] + "...",
                    "guests": detected_guests,
                    "has_vip": len(detected_guests) > 0
                })
        except Exception as e:
            pass
    
    # Sort: VIP guests first
    episodes.sort(key=lambda x: x['has_vip'], reverse=True)
    return episodes

# Sidebar
with st.sidebar:
    st.header("Actions")
    if st.button("🎙️ Find Interviews", type="primary"):
        with st.spinner("Scanning podcasts for AI leaders..."):
            try:
                config = ConfigLoader()
                episodes = fetch_podcasts(config)
                save_data("podcasts.json", episodes)
                st.success(f"Found {len(episodes)} episodes!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.markdown("---")
    st.checkbox("Show only VIP guests", key="vip_only", value=False)

last_updated_component("podcasts.json")

# Display
data = load_data("podcasts.json")

if not data:
    st.info("No podcasts yet. Click 'Find Interviews'.")
else:
    if st.session_state.get("vip_only", False):
        data = [d for d in data if d['has_vip']]
    
    for ep in data:
        guest_tags = "".join([f'<span style="background:#7248b9;color:white;padding:2px 6px;border-radius:4px;font-size:0.75em;margin-right:4px;">⭐ {g}</span>' for g in ep['guests']])
        border = "#7248b9" if ep['has_vip'] else "#444"
        
        st.markdown(f"""
        <div style="background-color: #1a1c24; padding: 15px; border-radius: 10px; margin-bottom:12px; border-left: 5px solid {border};">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="color:#aaa; font-size:0.8em;">{ep['source']} • {ep['published'][:16]}</span>
                <div>{guest_tags}</div>
            </div>
            <h3 style="margin:10px 0;"><a href="{ep['url']}" target="_blank" style="color:#fff; text-decoration:none;">{ep['title']}</a></h3>
            <p style="color:#ccc; font-size:0.9em;">{ep['summary']}</p>
            <a href="{ep['url']}" target="_blank" style="color:#7248b9; font-weight:bold;">▶ Play Episode</a>
        </div>
        """, unsafe_allow_html=True)
