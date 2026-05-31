# 🪐 AI Radar

> **您的 AI 情报统一仪表盘 | Your Unified Dashboard for AI Intelligence**  
> 全面的 AI 趋势追踪器，自动聚合、分析和提炼来自研究论文、行业新闻、简报、社区讨论和播客的信息。  
> A comprehensive AI trend tracker that automatically aggregates, analyzes, and digests information from research papers, industry news, newsletters, community discussions, and podcasts.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)]()

---

## 🌍 项目价值 | Why This Project Matters

AI research and product development move too quickly for developers to follow manually across papers, company blogs, newsletters, forums, product launches, and long-form interviews. AI Radar turns these noisy information streams into a structured intelligence workflow: it collects signals, ranks what matters, generates daily digests, and produces deeper paper reviews for technical decision-making.

This project is useful for AI builders, researchers, students, and independent developers who need a reproducible way to stay current without spending hours scanning disconnected sources. It also serves as an open-source reference implementation for building domain-specific intelligence dashboards with retrieval, ranking, summarization, and LLM-powered analysis.

AI 研究与产品演进速度很快，开发者很难同时跟踪论文、公司博客、简报、社区讨论、新产品发布和播客访谈。AI Radar 将这些分散的信息流整理成结构化情报工作流：自动采集信号、排序重点、生成日报，并为重要论文提供更深入的技术解读。

---

## ✨ 核心功能 | Features

### 📜 研究情报 | Research Intelligence
- **ArXiv 论文追踪**：自动抓取并评分，基于作者权威度、GitHub Stars 和机构关键词  
  **ArXiv Paper Tracking**: Automatically fetch and score papers by author authority, GitHub stars, and organization keywords
- **双模式深度解读 | Dual-Mode Analysis**：
  - **📋 评审报告 | Referee Report**：NeurIPS 风格的结构化评审（贡献、方法论、局限性、可复现性）  
    NeurIPS-style structured review (contribution, methodology, limitations, reproducibility)
  - **📚 技术解读 | Technical Deep Dive**：学习导向的分析，聚焦"我能学到什么"和"值不值得复现"  
    Learning-oriented analysis focused on "what can I learn" and "should I reproduce"
- **雷达频道**：按领域筛选论文（Agents、RAG、Vision、Reasoning、Safety & Alignment）  
  **Radar Channels**: Filter papers by domain (Agents, RAG, Vision, Reasoning, Safety & Alignment)

### 📣 新闻聚合 | News Aggregation
- **统一信息流**：整合官方博客（OpenAI、Google AI、Anthropic）和 AI 简报（Ben's Bites、TLDR AI、The Batch）  
  **Unified Feed**: Merge official blogs (OpenAI, Google AI, Anthropic) with newsletters (Ben's Bites, TLDR AI, The Batch)
- **AI 日报**：一键生成每日简报，由 OpenAI-compatible LLM 层驱动
  **AI Digest**: One-click daily briefing powered by an OpenAI-compatible LLM layer

### 💬 社区脉搏 | Community Pulse
- 追踪来自 **r/LocalLlama**、**r/MachineLearning**、**r/Singularity** 和 **Hacker News** 的社区讨论  
  Track grassroots sentiment from **r/LocalLlama**, **r/MachineLearning**, **r/Singularity**, and **Hacker News**
- 按来源类型筛选（Reddit / HN / 论坛）  
  Filter by source type (Reddit / HN / Forums)

### 🛠️ 产品发现 | Product Discovery
- 实时追踪 **Product Hunt** 和 **There's An AI For That** 的新工具发布  
  Real-time tracking from **Product Hunt** and **There's An AI For That**
- 第一时间发现最新 AI 产品  
  Discover new AI tools as they launch

### 🎧 AI 播客 | AI Podcasts
- 监控 **Lex Fridman**、**Dwarkesh Patel**、**Latent Space**、**No Priors** 的访谈节目  
  Monitor interviews from **Lex Fridman**, **Dwarkesh Patel**, **Latent Space**, **No Priors**
- 自动检测您关注的 VIP 嘉宾出场  
  Auto-detect VIP guests from your influencer watchlist

---

## 🚀 快速开始 | Quick Start

### 前置要求 | Prerequisites
- Python 3.9+
- LLM API Key（OpenAI API 或兼容服务，用于 AI 分析 | OpenAI API or compatible provider for AI-powered analysis）
- GitHub Token（可选，提升速率限制 | optional, for better rate limits）

### 安装 | Installation

```bash
# 克隆仓库 | Clone the repository
git clone https://github.com/gao-cai-sheng/AI-Radar.git
cd AI-Radar

# 创建虚拟环境 | Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖 | Install dependencies
pip install -r requirements.txt

# 设置环境变量 | Set up environment variables
cp .env.example .env
# 编辑 .env 并添加您的 LLM_API_KEY / OPENAI_API_KEY / DEEPSEEK_API_KEY
# Edit .env and add your LLM_API_KEY / OPENAI_API_KEY / DEEPSEEK_API_KEY
```

### 运行应用 | Run the Application

```bash
streamlit run interface/Home.py
```

在浏览器中打开 **http://localhost:8501**  
Open your browser at **http://localhost:8501**

---

## 📁 项目结构 | Project Structure

```
AI-Radar/
├── config/                 # 配置文件 | Configuration files
│   ├── influencers.yaml   # 追踪的作者、机构、RSS 源
│   └── channels.yaml      # 主题频道（Agents、RAG 等）
├── core/
│   ├── miners/            # 数据抓取器 | Data fetchers
│   ├── writers/           # AI 分析引擎 | AI analysis engines
│   └── utils/             # 工具函数 | Utilities
├── interface/
│   ├── Home.py            # 主入口 | Main entry point
│   └── pages/             # 多页面应用 | Multi-page app
├── data/                  # 缓存数据（已忽略）| Cached data (gitignored)
└── requirements.txt
```

---

## 🎯 使用指南 | Usage Guide

### 1. 研究论文 | Research Papers
1. 进入 **📜 Research** 页面
2. 点击 **"Scan ArXiv Now"** 抓取最新论文
3. 按 **Radar Channels** 筛选（如 "Safety & Alignment"）
4. 对任意论文，选择：
   - **📋 评审报告**：获取 NeurIPS 风格的结构化评审
   - **📚 技术解读**：获取学习导向的技术分析

### 2. 新闻摘要 | News Digest
1. 进入 **📣 News** 页面
2. 点击 **"Fetch All News"**
3. 点击 **"生成今日 Digest"** 获取 AI 生成的每日简报

### 3. 社区监控 | Community Monitoring
1. 进入 **💬 Discourse** 页面
2. 点击 **"Scan Communities"**
3. 按来源类型筛选（Reddit / HN / Forums）

---

## ⚙️ 配置 | Configuration

### LLM Provider

AI Radar uses the OpenAI Python SDK and supports OpenAI-compatible providers through environment variables. For OpenAI API usage, set:

```env
LLM_API_KEY=your_openai_api_key
LLM_MODEL=gpt-4o-mini
```

For DeepSeek or another OpenAI-compatible provider, also set `LLM_BASE_URL`:

```env
LLM_API_KEY=your_provider_api_key
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat
```

The legacy `DEEPSEEK_API_KEY` variable is still supported for existing users.

### 添加关注的影响者 | Adding Influencers
编辑 `config/influencers.yaml`:

```yaml
authors:
  - name: "Your Favorite Researcher"
    weight: 90

organizations:
  - name: "Your Lab/Company"
    weight: 85
```

### 自定义频道 | Customizing Channels
编辑 `config/channels.yaml`:

```yaml
- name: "Your Custom Channel"
  description: "..."
  keywords:
    - "keyword1"
    - "keyword2"
```

---

## 📊 分析模式 | Analysis Modes

### 评审报告（评估模式）| Referee Report (Evaluation Mode)
- **目的 | Purpose**: "这篇论文值得发表吗？" | "Is this paper worth publishing?"
- **输出 | Output**: 结构化清单与评分 | Structured checklist with scores
- **适用于 | Best for**: 文献综述、快速筛选 | Literature review, quick screening

### 技术解读（实现模式）| Technical Learning (Implementation Mode)
- **目的 | Purpose**: "我能学到什么？值得复现吗？" | "What can I learn? Should I reproduce this?"
- **输出 | Output**: 详细 Markdown 与实践建议 | Detailed Markdown with practical insights
- **适用于 | Best for**: 深度阅读、工程采用 | Deep reading, engineering adoption

---

## 🤝 贡献 | Contributing

欢迎贡献！请随时提交 Pull Request。  
Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📝 许可证 | License

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE)。<br>
This project is licensed under the MIT License. See [LICENSE](LICENSE).

---

## 🙏 致谢 | Acknowledgments

- 使用 OpenAI-compatible SDK 构建，可接入 OpenAI API 或兼容服务 | Built on an OpenAI-compatible SDK for OpenAI API or compatible providers
- 使用 [Streamlit](https://streamlit.io/) 构建 | Built with Streamlit
- 灵感来源于对更好的 AI 信息整理的需求 | Inspired by the need for better AI information curation

---

**⭐ 如果觉得这个项目有用，请给个 Star！| If you find this project useful, consider giving it a star!**
