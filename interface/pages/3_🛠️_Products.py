import streamlit as st
import sys
import time
import feedparser
from pathlib import Path
from typing import List, Dict, Any

sys.path.append(str(Path(__file__).parent.parent.parent))
from core.utils.config_loader import ConfigLoader
from interface.ui_utils import apply_styles, load_data, save_data, last_updated_component

st.set_page_config(page_title="Product Radar", page_icon="🛠️", layout="wide")
apply_styles()

st.title("🛠️ AI Product Radar")
st.markdown("New AI tools, models, and products. Sources: **Product Hunt**, **There's An AI For That**.")

def fetch_products(config: ConfigLoader, max_per_source: int = 10) -> List[Dict[str, Any]]:
    cfg = config.load()
    products = []
    for feed in cfg.product_sources:
        try:
            parsed = feedparser.parse(feed.url)
            for entry in parsed.entries[:max_per_source]:
                products.append({
                    "source": feed.name,
                    "title": entry.title,
                    "url": entry.link,
                    "published": entry.get('published', 'N/A'),
                    "summary": (entry.get('summary', '') or entry.get('description', ''))[:200] + "..."
                })
        except Exception as e:
            st.warning(f"Could not fetch {feed.name}")
    return products

# Sidebar
with st.sidebar:
    st.header("Actions")
    if st.button("🚀 Scan New Products", type="primary"):
        with st.spinner("Scanning Product Hunt & TAAFT..."):
            try:
                config = ConfigLoader()
                products = fetch_products(config)
                save_data("products.json", products)
                st.success(f"Found {len(products)} new products!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

last_updated_component("products.json")

# Display
data = load_data("products.json")

if not data:
    st.info("No products yet. Click 'Scan New Products'.")
else:
    cols = st.columns(2)
    for i, p in enumerate(data):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1c24 0%, #2d2f3a 100%); padding: 15px; border-radius: 10px; margin-bottom:12px; border: 1px solid #444;">
                <div style="font-size:0.75em; color:#aaa;">{p['source']} • {p['published'][:10]}</div>
                <h4 style="margin:8px 0;"><a href="{p['url']}" target="_blank" style="color:#fff; text-decoration:none;">🆕 {p['title']}</a></h4>
                <p style="color:#bbb; font-size:0.85em;">{p['summary']}</p>
                <a href="{p['url']}" target="_blank" style="color:#FF6B6B; font-weight:bold; font-size:0.9em;">Try it →</a>
            </div>
            """, unsafe_allow_html=True)
