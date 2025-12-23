import streamlit as st
import json
import os
from pathlib import Path
from datetime import datetime

# Common visual styles
def apply_styles():
    st.markdown("""
    <style>
        .card {
            background-color: #262730;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            border-left: 5px solid #FF4B4B;
        }
        .news-card {
            background-color: #1E1E1E;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 8px;
            border-left: 3px solid #00BFFF;
        }
        .tool-card {
            background-color: #1E1E1E;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 8px;
            border-left: 3px solid #FFD700;
        }
        a { text-decoration: none; color: #4FC3F7; }
        a:hover { text-decoration: underline; }
        h3 { margin-top: 0; }
        .stButton>button {
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)

def load_data(filename):
    path = Path(f"outputs/{filename}")
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_data(filename, data):
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    with open(output_dir / filename, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def last_updated_component(filename):
    path = Path(f"outputs/{filename}")
    if path.exists():
        # Get modification time
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        st.caption(f"Last updated: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        st.caption("No data cached.")
