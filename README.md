# 🪐 AI Radar

> **Your Unified Dashboard for AI Intelligence**  
> A comprehensive AI trend tracker that automatically aggregates, analyzes, and digests information from research papers, industry news, newsletters, community discussions, and podcasts.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)]()
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)]()

---

## ✨ Features

### 📜 Research Intelligence
- **ArXiv Paper Tracking**: Automatically fetch and score papers by author authority, GitHub stars, and organization keywords
- **Dual-Mode Analysis**:
  - **📋 Referee Report**: NeurIPS-style structured review (contribution, methodology, limitations, reproducibility)
  - **📚 Technical Deep Dive**: Learning-oriented analysis focused on "what can I learn" and "should I reproduce"
- **Radar Channels**: Filter papers by domain (Agents, RAG, Vision, Reasoning, Safety & Alignment)

### 📣 News Aggregation
- **Unified Feed**: Merge official blogs (OpenAI, Google AI, Anthropic) with newsletters (Ben's Bites, TLDR AI, The Batch)
- **AI Digest**: One-click daily briefing powered by DeepSeek LLM

### 💬 Community Pulse
- Track grassroots sentiment from **r/LocalLlama**, **r/MachineLearning**, **r/Singularity**, and **Hacker News**
- Filter by source type (Reddit / HN / Forums)

### 🛠️ Product Discovery
- Real-time tracking from **Product Hunt** and **There's An AI For That**
- Discover new AI tools as they launch

### 🎧 AI Podcasts
- Monitor interviews from **Lex Fridman**, **Dwarkesh Patel**, **Latent Space**, **No Priors**
- Auto-detect VIP guests from your influencer watchlist

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- DeepSeek API Key (for AI-powered analysis)
- GitHub Token (optional, for better rate limits)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/AI-Radar.git
cd AI-Radar

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your DEEPSEEK_API_KEY
```

### Run the Application

```bash
streamlit run interface/Home.py
```

Open your browser at **http://localhost:8501**

---

## 📁 Project Structure

```
AI-Radar/
├── config/                 # Configuration files
│   ├── influencers.yaml   # Tracked authors, orgs, RSS feeds
│   └── channels.yaml      # Topic channels (Agents, RAG, etc.)
├── core/
│   ├── miners/            # Data fetchers
│   │   ├── arxiv_miner.py
│   │   ├── news_miner.py
│   │   ├── reddit_miner.py
│   │   └── ...
│   ├── writers/           # AI analysis engines
│   │   ├── insight_engine.py  # Paper analysis
│   │   └── digest_engine.py   # News summarization
│   └── utils/             # Utilities
├── interface/
│   ├── Home.py            # Main entry point
│   └── pages/             # Multi-page app
│       ├── 1_📜_Research.py
│       ├── 2_📣_News.py
│       ├── 3_🛠️_Products.py
│       ├── 4_💬_Discourse.py
│       └── 5_🎧_Podcasts.py
├── data/                  # Cached data (gitignored)
├── docs/                  # Documentation
└── requirements.txt
```

---

## 🎯 Usage Guide

### 1. Research Papers
1. Navigate to **📜 Research**
2. Click **"Scan ArXiv Now"** to fetch latest papers
3. Filter by **Radar Channels** (e.g., "Safety & Alignment")
4. For any paper, choose:
   - **📋 评审报告**: Get a structured NeurIPS-style review
   - **📚 技术解读**: Get a learning-focused technical breakdown

### 2. News Digest
1. Navigate to **📣 News**
2. Click **"Fetch All News"**
3. Click **"生成今日 Digest"** to get an AI-generated daily briefing

### 3. Community Monitoring
1. Navigate to **💬 Discourse**
2. Click **"Scan Communities"**
3. Filter by source type (Reddit / HN / Forums)

---

## ⚙️ Configuration

### Adding Influencers
Edit `config/influencers.yaml`:

```yaml
authors:
  - name: "Your Favorite Researcher"
    weight: 90

organizations:
  - name: "Your Lab/Company"
    weight: 85
```

### Customizing Channels
Edit `config/channels.yaml`:

```yaml
- name: "Your Custom Channel"
  description: "..."
  keywords:
    - "keyword1"
    - "keyword2"
```

---

## 📊 Analysis Modes

### Referee Report (Evaluation Mode)
- **Purpose**: "Is this paper worth publishing?"
- **Output**: Structured checklist with scores
- **Best for**: Literature review, quick screening

### Technical Learning (Implementation Mode)
- **Purpose**: "What can I learn? Should I reproduce this?"
- **Output**: Detailed Markdown with practical insights
- **Best for**: Deep reading, engineering adoption

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests (if available)
pytest
```

---

## 📝 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- Powered by [DeepSeek](https://www.deepseek.com/) for AI analysis
- Built with [Streamlit](https://streamlit.io/)
- Inspired by the need for better AI information curation

---

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**⭐ If you find this project useful, consider giving it a star!**
