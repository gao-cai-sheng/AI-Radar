# Project v3: AI-Trend-Radar (代号: 破迷雾)

## 0. 核心痛点与愿景

**痛点 (Pain Points)**:
1.  **速度过快 (Velocity)**: 每天 100+ 篇 ArXiv 论文，追得心累。
2.  **噪音过大 (Noise)**: Twitter/自媒体过度解读，标题党横行。
3.  **认知滞后 (Lag)**: 等到读懂论文，技术可能已经迭代了。
4.  **真假难辨 (Validity)**: 是真的 SOTA (State of the Art) 还只是炒作？

**愿景 (Vision)**:
不做一个简单的“新闻聚合器”，而是做一个 **“信息精炼厂” (Information Refinery)**。
它应该像一个经验丰富的 CTO，每天早上告诉你：“昨天出了 500 篇论文，但这 3 篇通过了我的代码验证和背景调查，值得你花 10 分钟细看。”

---

## 1. 竞品调研与差距分析 (Market Analysis)

在 GitHub 上搜索了类似方案，发现主要分为三类：

| 类别 | 代表项目 | 优点 | 缺点/不足 |
| :--- | :--- | :--- | :--- |
| **订阅推送类** | `AutoLLM/ArxivDigest`, `newsletter-agent` | 自动化，推送到邮箱 | **缺乏深度**。只是简单的“标题+摘要”，没有甄别价值。 |
| **深度研究类** | `Litmaps`, `Inciteful` | 引用关系分析强大 | **太重了**。适合写论文做背景调查，不适合通过“每日快讯”获取新知。 |
| **趋势榜单类** | `Trending-AI-Paper-Repos` | 直观看到热门 | **滞后性**。等上了榜单通常已经火了几天了，且缺乏“为什么火”的解释。 |

**我们的机会点**:
大多数工具只解决了 **"Access" (获取)** 的问题，没有解决 **"Insight" (洞察)** 的问题。我们需要一个 **Smart-Miner for AI**，核心不仅仅是 Mine (挖掘)，而是 **Judge (评判)**。

---

## 2. 拟定架构设计 (Proposed Architecture)

参照旧项目 `Lit-Miner`，我们设计 v3 的 Pipeline：

### 2.1 源头与获取 (Sources) - "捕鱼"
不同于 PubMed 单一源，AI 需要多维度信号：
*   **学术源**: ArXiv (API) -> 关注 CS.CL, CS.CV, CS.LG 等板块。
*   **代码源**: GitHub Trending / HuggingFace Papers (Daily) -> 验证是否有代码实现。
*   **社交源**: (可选) 关键 KOL 的关注列表 -> 验证传播热度。

### 2.2 信号过滤器 (The Smart Filter) - "筛鱼"
这是核心算法，替代旧版 Lit-Miner 的“影响因子筛选”：
*   **Hype Score (热度分)**: GitHub Stars 增长率、HuggingFace Likes、Twitter 提及数。
*   **Credibility Score (靠谱分)**:
    *   作者机构背景 (Google/DeepMind/Stanford 加分)。
    *   是否有 Code/Demo (有则大幅加分)。
    *   引用的基准测试是否权威。

### 2.3 AI 洞察引擎 (The Insight Engine) - "烹饪"
使用 LLM (DeepSeek/GPT-4) 扮演不同角色进行深加工：
*   **角色 A (摘要员)**: 用人话解释这篇论文解决了什么问题。
*   **角色 B (质检员)**: **Critical Thinking**。找出论文的弱点（例如：只在特定数据集有效？显存需求过大？）。
*   **角色 C (猎头)**: 判断这个技术是否可以立即应用到工程中。

### 2.4 展示层 (Presentation) - "上菜"
*   **形式**: 每日/每周 简报 (Markdown/Web UI)。
*   **特色**:
    *   **"TL;DR"**: 一句话总结。
    *   **"Show me the code"**: 直接链接到可用代码。
    *   **"Hype vs Reality"**: AI 评出的推荐指数。

---

## 3. 下一步规划 (Roadmap)

### Phase 1: MVP (最小可行性产品)
*   **目标**: 跑通 "ArXiv -> 筛选 -> AI总结" 流程。
*   **数据源**: 仅 ArXiv + HuggingFace Daily Papers。
*   **输出**: 生成一个 Markdown 日报。

### Phase 2: 增强筛选
*   **目标**: 引入 GitHub API，计算“代码含金量”。
*   **功能**: 自动检测 Repo 是否由于只有 README 而没有代码（"Paperware" 检测）。

### Phase 3: 交互式 UI
*   **目标**: 重建 Streamlit/Web 界面，允许用户订阅特定领域的 "Radar"。

---

## 4. 技术栈迁移决策
*   **LLM**: 继续使用 DeepSeek (性价比高，适合长文本分析)。
*   **DB**: 依然使用 ChromaDB 或 SQLite 存储已读论文，避免重复分析。
*   **Framework**: 建议尝试 **FastAPI + Vue/React** 或继续 **Streamlit** (为了快速开发推荐继续 Streamlit)。
