# AI Trend Radar (v3) - Strategic Enhancements
> "Not just an aggregator, but a programmable Radar."

## 1. Custom Radar Channels (用户自定义领域雷达)
目前的问题：我们只有一个笼统的 "Top Hype Papers"，包含所有 AI 领域，信息密度不均。
**解决方案**：引入 **"Radar Channels" (雷达频道)** 概念。
允许用户在配置文件中定义自己关注的 "Verticals" (垂直领域)。

### Configuration (`config/channels.yaml`):
```yaml
channels:
  - name: "Agentic Flux"
    description: "Autonomous agents and multi-agent systems"
    keywords: ["autonomous agent", "multi-agent", "agentic workflow"]
    
  - name: "RAG & Context"
    description: "Retrieval Augmented Generation optimization"
    keywords: ["RAG", "long context", "kv cache", "retrieval"]

  - name: "Embodied AI"
    description: "Robotics and physical world interactions"
    keywords: ["robotics", "manipulation", "ego-centric"]
```

**功能实现**:
1.  **Tagging Engine**: 抓取论文后，不再只是打分，而是根据关键词自动打上 `#Agent`, `#RAG` 标签。
2.  **Channel View**: UI 上增加 "Channel" 过滤器，只看特定领域的进展。

---

## 2. SOTA Watch (Benchmark 哨兵)
目前的问题：我们知道论文很火，但不知道它到底“强”在哪里。
**解决方案**：**Benchmark Extraction**。
利用 Regex 或 LLM 从 Abstract 中提取核心指标。

**功能实现**:
*   自动扫描 `GSM8K`, `MMLU`, `HumanEval`, `MATH` 等关键词。
*   如果发现 `GSM8K > 85%` 这样的字眼，在 UI 上高亮显示 **"🔥 New SOTA Potential"**。
*   把单纯的 "热度" (Hype) 转化为 "硬实力" (Performance) 监控。

---

## 3. Product/Model Radar (Hugging Face Daily)
目前的问题：Code Miner 只看了 Stars，但没有区分 "Release" (发布) 和 "Update" (更新)。
**解决方案**：**"New Weights Drop" (重磅模型发布监控)**。
*   专门监控 Hugging Face 的 `Trending` 榜单中 `Created Date` < 7 days 的项目。
*   过滤掉 Dataset，只看 Model。
*   **目标**: 第一时间发现 "Llama 4", "Mistral Next" 这种级别的发布。

---

## 4. Signal-to-Noise Ratio (反向过滤)
目前的问题：噪音还是可能很大。
**解决方案**：**Negative Filters (屏蔽词)**。
允许用户定义 `ignore_keywords`，例如屏蔽掉大量灌水的 "Survey papers" (综述) 或者特定不想看的领域。

```yaml
ignore:
  - "Survey"
  - "Review of"
  - "blockchain" # 如果用户不关心
```
