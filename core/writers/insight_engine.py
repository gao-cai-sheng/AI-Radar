from openai import OpenAI
import os
import json
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class InsightEngine:
    """
    升维引擎 v2: Structured Referee Report (NeurIPS-style Checklist)
    """
    
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.base_url = "https://api.deepseek.com"
        
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in .env")

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def analyze_paper(self, paper: Dict[str, Any]) -> Dict[str, Any]:
        """Quick scan (unchanged)."""
        prompt = f"""
        You are a Senior AI Researcher. Briefly analyze this paper.
        Title: {paper['title']}
        Authors: {', '.join(paper['authors'][:5])}
        Abstract: {paper['abstract'][:500]}
        
        Output (JSON):
        {{
            "tldr": "一句话中文总结",
            "innovation_score": "1-10",
            "reality_check": "简短点评 (中文)",
            "verdict": "MUST READ / OPTIONAL / SKIP"
        }}
        """
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.3, max_tokens=300
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e), "verdict": "ERROR"}

    def deep_dive(self, paper: Dict[str, Any]) -> Dict[str, Any]:
        """
        升维分析 v2: Structured Referee Report
        Aligned with NeurIPS ML Reproducibility Checklist
        """
        github_info = f"GitHub: {paper.get('links', {}).get('github', '无')}"
        
        prompt = f"""
你是一位资深 ML Reviewer，请按照 **NeurIPS 审稿 Checklist** 风格对这篇论文进行结构化评审。

论文信息:
- 标题: {paper['title']}
- 作者: {', '.join(paper['authors'][:8])}
- 摘要: {paper['abstract']}
- {github_info}

请严格按以下 JSON 结构输出评审报告:

{{
    "meta": {{
        "title_cn": "中文标题",
        "one_liner": "一句话摘要 (中文, 20字以内)",
        "tags": {{
            "task_type": "分类/生成/推理/对齐/其他",
            "is_llm": true/false,
            "is_safety_related": true/false,
            "contribution_type": "方法/理论/系统/数据集/调研"
        }}
    }},
    
    "contribution": {{
        "problem_clear": {{
            "answer": true/false,
            "note": "问题定义是否清晰？1句说明"
        }},
        "is_repackaged": {{
            "answer": true/false,
            "note": "是否只是「重新包装旧问题」？"
        }},
        "comparison": {{
            "related_works": ["相关工作1", "相关工作2"],
            "real_difference": "与相关工作的真实差异是什么？换了什么假设？提升了什么？",
            "novelty_score": 1-5
        }}
    }},
    
    "methodology": {{
        "pipeline": "输入→关键模块→输出 (一句话技术路线)",
        "core_modules": [
            {{"name": "模块1", "mechanism": "靠什么起作用？"}},
            {{"name": "模块2", "mechanism": ""}}
        ],
        "assumptions": {{
            "key_assumptions": "关键假设 (如需要 IID、高质量标注等)",
            "applicable_scenarios": "适用场景",
            "not_applicable": "不适用场景"
        }},
        "complexity": {{
            "time": "时间复杂度粗评",
            "scalability": "能否扩展到大规模？"
        }},
        "theory_support": {{
            "has_theory": true/false,
            "note": "有无理论支撑或 toy example？"
        }}
    }},
    
    "limitations": {{
        "author_stated": [
            {{"issue": "局限1", "category": "数据/方法/计算/伦理/泛化"}}
        ],
        "hidden_issues": {{
            "fragile_assumptions": "依赖哪些脆弱假设？",
            "potential_hacks": "是否容易 cherry-pick / 数据泄漏 / prompt hack？"
        }},
        "harm_risk": {{
            "deployment_risk": "部署风险是什么？",
            "who_might_be_harmed": "对谁可能有害？"
        }},
        "anti_use_cases": ["反例场景1: 不要在__时使用"]
    }},
    
    "reproducibility": {{
        "code": {{
            "status": "开源/局部开源/未开源",
            "version_deps": true/false,
            "note": ""
        }},
        "data": {{
            "status": "公开/受限/不开源",
            "stats_provided": true/false
        }},
        "experiment": {{
            "seed_provided": true/false,
            "variance_reported": true/false,
            "ablation_complete": true/false,
            "baseline_tuned": "是/否/不确定"
        }},
        "cost_estimate": {{
            "gpu_hours": "估算 GPU 小时",
            "memory_requirement": "显存需求",
            "human_level": "本科生/研究生/熟练工程师/研究团队"
        }}
    }},
    
    "verdict": {{
        "scores": {{
            "novelty": 1-5,
            "engineering_value": 1-5,
            "scientific_rigor": 1-5,
            "reproducibility": 1-5,
            "weighted_total": "加权总分 (自定义权重)"
        }},
        "recommendations": {{
            "worth_reproducing": true/false,
            "worth_industry_trial": true/false,
            "worth_survey_inclusion": true/false
        }},
        "target_audience": "适合人群 (例: 大模型安全研究者 / 推荐系统团队 / 博士新生)",
        "key_takeaway": "这篇工作最值得被记住的一点",
        "practical_lesson": "如果只带走一个实践教训，会是什么？"
    }}
}}
"""

        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一位严谨的 ML Reviewer，按 NeurIPS checklist 标准输出结构化评审。"},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=2000
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}

    def technical_learning(self, paper: Dict[str, Any]) -> str:
        """
        技术学习型解读: 专注于 "我能学到什么" 和 "值不值得复现"
        返回 Markdown 格式的详细分析
        """
        github_info = f"GitHub: {paper.get('links', {}).get('github', '无')}"
        
        system_prompt = """你是一名在机器学习与大模型方向有多年经验的研究员和代码实现者。
我会提供一篇论文（标题、摘要）。
你的任务不是写新闻式综述，而是帮我**从技术细节出发搞懂这篇 paper，并评估是否值得我亲自复现或在工程中采用**。

回答必须结构化，严格使用以下模块和问题，并尽量引用论文中的具体细节（公式、实验设定、超参、图表编号等），不要给空泛的评价。
如果某个问题论文中没有给出信息，请明确标「论文未说明」，不要编造。
语言：中文为主，必要时保留英文术语与公式符号，方便与原文对应。"""

        user_prompt = f"""
请对以下论文进行技术学习型解读：

**标题**: {paper['title']}
**作者**: {', '.join(paper['authors'][:8])}
**摘要**: {paper['abstract']}
**{github_info}**

请按以下结构输出 Markdown 格式的分析：

## 1. 贡献定位 (Contribution)
- 用 1–2 句话给出这篇论文的「最小问题描述」和自我定位
- 用要点列出论文声称的主要贡献，并标明贡献类型：方法 / 理论 / 系统 / 数据集 / 调研
- 和最相关的 2–3 篇工作做简要对比，指出**实质差异**

## 2. 方法细节 (Method & Assumptions)
- 画出技术路线：`输入 → 模块1 → 模块2 → … → 输出`
- 说明每个关键模块各自解决什么子问题，用了哪些具体技术点
- 列出关键假设（数据分布、模型结构、训练资源等）+ 适用场景
- 如果有理论分析，概括核心结论

## 3. 实验与局限 (Experiments & Limitations)
- 总结主要实验设置：数据集、模型规模、训练细节、关键 baseline
- 模型在哪些指标上获得明显收益，哪些场景表现一般
- 作者承认的局限 + 你补充的潜在问题

## 4. 可复现性与成本 (Reproducibility)
- 代码和数据状态
- 复现所需关键细节：显存、训练时间
- 估算：GPU 小时 + 复现难度（本科高年级/研究生/资深工程师）

## 5. 学习价值与实践建议 (For Me) ⭐
- **技术学习点** (2–3 个)：最值得学的技巧/策略/分析方法
- **工程实践建议**：适合什么场景试验 + 落地需注意的细节
- **综合判断**：「建议亲自复现 / 建议只读懂思路不必复现 / 建议当作背景阅读」+ 理由
"""

        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.4,
                max_tokens=2500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"**Error**: {str(e)}"


if __name__ == "__main__":
    engine = InsightEngine()
    test_paper = {
        "title": "DeepSeek-V3 Technical Report",
        "authors": ["DeepSeek-AI"],
        "abstract": "We present DeepSeek-V3, a strong Mixture-of-Experts...",
        "links": {"github": "https://github.com/deepseek-ai/DeepSeek-V3"}
    }
    result = engine.deep_dive(test_paper)
    print(json.dumps(result, ensure_ascii=False, indent=2))

