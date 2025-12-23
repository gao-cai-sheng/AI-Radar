# 快速上手指南 | Quick Start Guide

**用途 | Purpose**: 帮助新对话快速了解项目当前状态 | Help new conversations quickly understand the project status  
**最后更新 | Last Updated**: 2025-12-23  
**当前版本 | Current Version**: v1.0

---

## 🚀 30秒快速了解 | 30-Second Overview

**项目 | Project**: AI Radar - AI 情报统一仪表盘  
**状态 | Status**: ✅ 生产就绪，已部署到 GitHub | Production ready, deployed to GitHub  
**核心功能 | Core Features**: 论文追踪 + 新闻聚合 + 社区监控 + 产品发现 + 播客追踪

---

## 📋 必读文件（按优先级）| Essential Files (By Priority)

### 1️⃣ 项目概览 | Project Overview
- **README.md** - 项目介绍、功能特性、快速开始 | Project intro, features, quick start

### 2️⃣ 设计文档 | Design Documents
- **docs/PAPER_REVIEW_MODES.md** - 双模式论文解读系统设计 | Dual-mode paper review system design
  - Referee Report（评审模式）
  - Technical Learning（学习模式）

### 3️⃣ 配置文件 | Configuration Files
- **config/influencers.yaml** - 追踪的作者、机构、RSS 源 | Tracked authors, orgs, RSS feeds
- **config/channels.yaml** - 主题频道配置 | Topic channel configuration

---

## 🗂️ 关键文件位置 | Key File Locations

### 公开文件（GitHub上）| Public Files (On GitHub)
```
/Users/gao/Desktop/Lit-Miner/v3_next_gen/
├── README.md                    # 项目主文档
├── requirements.txt             # Python 依赖
├── config/
│   ├── influencers.yaml        # 影响者配置
│   └── channels.yaml           # 频道配置
├── core/
│   ├── miners/                 # 数据抓取器
│   │   ├── arxiv_miner.py     # ArXiv 论文
│   │   ├── news_miner.py      # 新闻源
│   │   ├── reddit_miner.py    # Reddit/HN
│   │   └── interview_miner.py # 播客
│   ├── writers/                # AI 分析引擎
│   │   ├── insight_engine.py  # 论文解读
│   │   └── digest_engine.py   # 新闻摘要
│   └── utils/
│       ├── config_loader.py   # 配置加载器
│       └── code_signals.py    # GitHub/HF 检测
├── interface/
│   ├── Home.py                 # 主页
│   ├── ui_utils.py            # UI 工具
│   └── pages/
│       ├── 1_📜_Research.py   # 研究论文
│       ├── 2_📣_News.py       # 新闻聚合
│       ├── 3_🛠️_Products.py  # 产品发现
│       ├── 4_💬_Discourse.py # 社区讨论
│       └── 5_🎧_Podcasts.py  # 播客追踪
└── docs/
    └── PAPER_REVIEW_MODES.md  # 设计文档
```

### 私有文件（本地，不在GitHub）| Private Files (Local, Not on GitHub)
```
/Users/gao/Desktop/Lit-Miner/v3_next_gen/
├── .env                        # API 密钥
└── data/                       # 缓存数据
    ├── papers_latest.json
    ├── news_feed.json
    ├── paper_analyses.json
    └── ...
```

---

## 🎯 当前版本功能 | Current Version Features

### v1.0 (最新 | Latest)
✅ ArXiv 论文追踪（作者权威 + GitHub Stars + 机构关键词）  
✅ 双模式论文解读（Referee Report + Technical Learning）  
✅ 雷达频道筛选（Agents, RAG, Vision, Reasoning, Safety & Alignment）  
✅ 新闻聚合（官方博客 + 简报 + 媒体）  
✅ AI 日报生成（DeepSeek LLM）  
✅ 社区脉搏监控（Reddit + HN + 论坛）  
✅ 产品发现（Product Hunt + TAAFT）  
✅ 播客追踪（VIP 嘉宾检测）

---

## 🔧 快速命令 | Quick Commands

### 启动应用 | Start Application
```bash
cd /Users/gao/Desktop/Lit-Miner/v3_next_gen
source .venv/bin/activate
streamlit run interface/Home.py
# 访问 | Visit: http://localhost:8501
```

### 验证配置 | Verify Configuration
```bash
cd /Users/gao/Desktop/Lit-Miner/v3_next_gen
python -c "from core.utils.config_loader import ConfigLoader; c=ConfigLoader(); print(f'✅ {len(c.load().authors)} authors, {len(c.load_channels())} channels')"
# 应显示 | Should show: ✅ XX authors, 6 channels
```

### 查看 Git 状态 | Check Git Status
```bash
cd /Users/gao/Desktop/Lit-Miner/v3_next_gen
git status
git log --oneline -5
```

---

## 📊 项目统计 | Project Statistics

- **代码行数 | Lines of Code**: ~3,000 行
- **配置数据 | Configuration Data**: 
  - 30+ 追踪作者 | Tracked authors
  - 20+ 追踪机构 | Tracked organizations
  - 30+ RSS 源 | RSS feeds
  - 6 个雷达频道 | Radar channels
- **GitHub**: https://github.com/gao-cai-sheng/AI-Radar
- **Commits**: 3+

---

## 🚨 重要提醒 | Important Reminders

### 私有文件 | Private Files
**这些文件不在 GitHub 上，需要本地维护 | These files are not on GitHub, require local maintenance**：
1. `.env` - API 密钥（DEEPSEEK_API_KEY, GITHUB_TOKEN）
2. `data/` - 所有缓存数据

### 环境变量 | Environment Variables
必需 | Required:
- `DEEPSEEK_API_KEY` - 用于 AI 分析和摘要生成

可选 | Optional:
- `GITHUB_TOKEN` - 提升 GitHub API 速率限制

---

## 📝 使用流程 | Usage Workflow

### 1. 研究论文 | Research Papers
```
进入 Research 页面 → Scan ArXiv Now → 选择 Channel → 点击论文 → 选择解读模式
```

### 2. 新闻摘要 | News Digest
```
进入 News 页面 → Fetch All News → 生成今日 Digest
```

### 3. 社区监控 | Community Monitoring
```
进入 Discourse 页面 → Scan Communities → 按来源筛选
```

### 4. 产品发现 | Product Discovery
```
进入 Products 页面 → Scan Products → 查看最新工具
```

### 5. 播客追踪 | Podcast Tracking
```
进入 Podcasts 页面 → Fetch Episodes → 查看 VIP 嘉宾
```

---

## 🎨 双模式论文解读 | Dual-Mode Paper Analysis

### 📋 Referee Report（评审模式）
- **目的 | Purpose**: "这篇论文值得发表吗？"
- **输出 | Output**: NeurIPS 风格结构化评审
- **包含 | Includes**: 
  - 贡献定位（问题清晰度、创新度）
  - 方法论（技术路线、假设、复杂度）
  - 风险边界（局限性、部署风险）
  - 复现透明度（代码/数据/实验）
  - 最终评价（5 维评分）

### 📚 Technical Learning（学习模式）
- **目的 | Purpose**: "我能学到什么？值得复现吗？"
- **输出 | Output**: 详细 Markdown 技术解读
- **包含 | Includes**:
  - 贡献定位
  - 方法细节（技术路线、关键假设）
  - 实验与局限
  - 可复现性与成本
  - **学习价值与实践建议** ⭐

---

## 🤖 给新 AI 助手的建议 | Tips for New AI Assistants

### 首次对话时应该 | On First Conversation:
1. **阅读本文件** - 了解项目全貌 | Read this file - understand the project
2. **查看 README.md** - 了解功能特性 | Check README.md - understand features
3. **检查 Git 状态** - 确认最新提交 | Check Git status - confirm latest commit
4. **验证配置** - 运行验证命令 | Verify configuration - run verification commands
5. **询问用户** - 确认当前需求 | Ask user - confirm current needs

### 常见场景 | Common Scenarios
- **添加新源 | Add New Source**: 编辑 `config/influencers.yaml`
- **添加频道 | Add Channel**: 编辑 `config/channels.yaml`
- **调试问题 | Debug Issues**: 检查 `data/` 目录下的 JSON 文件
- **扩展功能 | Extend Features**: 参考 `docs/PAPER_REVIEW_MODES.md`

### 关键命令 | Key Commands
```bash
# 查看项目状态 | Check project status
cd /Users/gao/Desktop/Lit-Miner/v3_next_gen
git status
ls -lh data/

# 验证系统 | Verify system
python -c "from core.utils.config_loader import ConfigLoader; print('✅ Config OK')"

# 启动应用 | Start application
streamlit run interface/Home.py
```

---

## 📚 文档索引 | Documentation Index

| 文档 | 用途 | 位置 |
|------|------|------|
| README.md | 项目介绍 | 公开 |
| QUICKSTART.md | 快速上手 | 公开 |
| PAPER_REVIEW_MODES.md | 解读模式设计 | 公开 |
| influencers.yaml | 影响者配置 | 公开 |
| channels.yaml | 频道配置 | 公开 |

---

**最后更新 | Last Updated**: 2025-12-23  
**文档位置 | Document Location**: `/Users/gao/Desktop/Lit-Miner/v3_next_gen/QUICKSTART.md`  
**状态 | Status**: ✅ 生产就绪 | Production Ready
