# 🪐 AI Radar

> **Your Unified Dashboard for AI Intelligence**  
> A comprehensive AI trend tracker that automatically aggregates, analyzes, and digests information from research papers, industry news, newsletters, community discussions, and podcasts.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)]()
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)]()

---

## ✨ 核心功能

### 📜 研究情报
- **ArXiv 论文追踪**：自动抓取并评分，基于作者权威度、GitHub Stars 和机构关键词
- **双模式深度解读**：
  - **📋 评审报告**：NeurIPS 风格的结构化评审（贡献、方法论、局限性、可复现性）
  - **📚 技术解读**：学习导向的分析，聚焦"我能学到什么"和"值不值得复现"
- **雷达频道**：按领域筛选论文（Agents、RAG、Vision、Reasoning、Safety & Alignment）

### 📣 新闻聚合
- **统一信息流**：整合官方博客（OpenAI、Google AI、Anthropic）和 AI 简报（Ben's Bites、TLDR AI、The Batch）
- **AI 日报**：一键生成每日简报，由 DeepSeek LLM 驱动

### 💬 社区脉搏
- 追踪来自 **r/LocalLlama**、**r/MachineLearning**、**r/Singularity** 和 **Hacker News** 的社区讨论
- 按来源类型筛选（Reddit / HN / 论坛）

### 🛠️ 产品发现
- 实时追踪 **Product Hunt** 和 **There's An AI For That** 的新工具发布
- 第一时间发现最新 AI 产品

### 🎧 AI 播客
- 监控 **Lex Fridman**、**Dwarkesh Patel**、**Latent Space**、**No Priors** 的访谈节目
- 自动检测您关注的 VIP 嘉宾出场

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
