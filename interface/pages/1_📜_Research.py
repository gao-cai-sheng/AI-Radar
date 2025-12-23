import streamlit as st
import sys
import time
import json
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from core.miners.arxiv_miner import ArxivMiner
from core.writers.insight_engine import InsightEngine
from core.utils.config_loader import ConfigLoader
from interface.ui_utils import apply_styles, load_data, save_data, last_updated_component

st.set_page_config(page_title="Research Radar", page_icon="📜", layout="wide")
apply_styles()

st.title("📜 Research Radar")
st.markdown("Top papers with **Deep Dive** analysis options.")

# --- Referee Report Display (Checklist Format) ---
deep_dive_data = load_data("deep_dive_current.json")
if deep_dive_data and not deep_dive_data.get("error"):
    d = deep_dive_data
    meta = d.get('meta', {})
    
    with st.expander("📋 Structured Referee Report", expanded=True):
        # Header
        st.markdown(f"## {meta.get('title_cn', 'N/A')}")
        st.markdown(f"**{meta.get('one_liner', '')}**")
        
        tags = meta.get('tags', {})
        tag_str = f"`{tags.get('contribution_type', '')}` · `{tags.get('task_type', '')}` · {'🤖 LLM' if tags.get('is_llm') else ''} {'🛡️ Safety' if tags.get('is_safety_related') else ''}"
        st.markdown(tag_str)
        
        st.markdown("---")
        
        # --- Contribution ---
        st.markdown("### 💡 贡献定位 (Contribution)")
        contrib = d.get('contribution', {})
        
        prob = contrib.get('problem_clear', {})
        st.checkbox("问题定义清晰", value=prob.get('answer', False), disabled=True)
        st.caption(prob.get('note', ''))
        
        repkg = contrib.get('is_repackaged', {})
        st.checkbox("是「重新包装旧问题」", value=repkg.get('answer', False), disabled=True)
        st.caption(repkg.get('note', ''))
        
        comp = contrib.get('comparison', {})
        st.markdown(f"**相关工作**: {', '.join(comp.get('related_works', []))}")
        st.markdown(f"**真实差异**: {comp.get('real_difference', '')}")
        st.metric("创新度", f"{comp.get('novelty_score', 'N/A')}/5")
        
        st.markdown("---")
        
        # --- Methodology ---
        st.markdown("### 🔧 方法论 (Methodology)")
        meth = d.get('methodology', {})
        
        st.markdown(f"**技术路线**: `{meth.get('pipeline', '')}`")
        
        st.markdown("**核心模块**:")
        for mod in meth.get('core_modules', []):
            st.markdown(f"- **{mod.get('name', '')}**: {mod.get('mechanism', '')}")
        
        assump = meth.get('assumptions', {})
        st.markdown(f"**关键假设**: {assump.get('key_assumptions', '')}")
        st.markdown(f"✅ 适用: {assump.get('applicable_scenarios', '')}")
        st.markdown(f"❌ 不适用: {assump.get('not_applicable', '')}")
        
        cpx = meth.get('complexity', {})
        st.markdown(f"**复杂度**: {cpx.get('time', '')} | **扩展性**: {cpx.get('scalability', '')}")
        
        theory = meth.get('theory_support', {})
        st.checkbox("有理论支撑", value=theory.get('has_theory', False), disabled=True)
        st.caption(theory.get('note', ''))
        
        st.markdown("---")
        
        # --- Limitations ---
        st.markdown("### ⚠️ 风险边界 (Limitations)")
        lim = d.get('limitations', {})
        
        st.markdown("**作者自述局限**:")
        for issue in lim.get('author_stated', []):
            st.markdown(f"- `{issue.get('category', '')}` {issue.get('issue', '')}")
        
        hidden = lim.get('hidden_issues', {})
        st.markdown(f"**隐形坑**: {hidden.get('fragile_assumptions', '')}")
        st.markdown(f"**Hack 风险**: {hidden.get('potential_hacks', '')}")
        
        harm = lim.get('harm_risk', {})
        st.warning(f"**部署风险**: {harm.get('deployment_risk', '')} | **潜在受害者**: {harm.get('who_might_be_harmed', '')}")
        
        st.markdown("**反例场景**:")
        for anti in lim.get('anti_use_cases', []):
            st.markdown(f"- 🚫 {anti}")
        
        st.markdown("---")
        
        # --- Reproducibility ---
        st.markdown("### 🔁 复现透明度 (Reproducibility)")
        rep = d.get('reproducibility', {})
        
        col1, col2 = st.columns(2)
        with col1:
            code = rep.get('code', {})
            st.markdown(f"**代码**: {code.get('status', '')}")
            st.checkbox("版本依赖写明", value=code.get('version_deps', False), disabled=True)
            
            data = rep.get('data', {})
            st.markdown(f"**数据**: {data.get('status', '')}")
            st.checkbox("数据统计提供", value=data.get('stats_provided', False), disabled=True)
        
        with col2:
            exp = rep.get('experiment', {})
            st.checkbox("Seed 提供", value=exp.get('seed_provided', False), disabled=True)
            st.checkbox("方差报告", value=exp.get('variance_reported', False), disabled=True)
            st.checkbox("完整 Ablation", value=exp.get('ablation_complete', False), disabled=True)
            st.markdown(f"Baseline 调参: {exp.get('baseline_tuned', 'N/A')}")
        
        cost = rep.get('cost_estimate', {})
        st.info(f"**复现成本**: {cost.get('gpu_hours', '')} | {cost.get('memory_requirement', '')} | 人力: {cost.get('human_level', '')}")
        
        st.markdown("---")
        
        # --- Verdict ---
        st.markdown("### 📊 最终评价 (Verdict)")
        verd = d.get('verdict', {})
        scores = verd.get('scores', {})
        
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("创新", f"{scores.get('novelty', 'N/A')}/5")
        c2.metric("工程价值", f"{scores.get('engineering_value', 'N/A')}/5")
        c3.metric("科学严谨", f"{scores.get('scientific_rigor', 'N/A')}/5")
        c4.metric("可复现", f"{scores.get('reproducibility', 'N/A')}/5")
        c5.metric("加权总分", scores.get('weighted_total', 'N/A'))
        
        recs = verd.get('recommendations', {})
        st.markdown(f"{'✅' if recs.get('worth_reproducing') else '❌'} 值得复现 | {'✅' if recs.get('worth_industry_trial') else '❌'} 值得工业试点 | {'✅' if recs.get('worth_survey_inclusion') else '❌'} 值得写入综述")
        
        st.markdown(f"**适合人群**: {verd.get('target_audience', '')}")
        
        st.success(f"💎 **Key Takeaway**: {verd.get('key_takeaway', '')}")
        st.info(f"🎯 **实践教训**: {verd.get('practical_lesson', '')}")
        
        if st.button("❌ 关闭 Report"):
            save_data("deep_dive_current.json", {})
            st.rerun()

# --- Sidebar Controls ---
with st.sidebar:
    st.header("Actions")
    if st.button("🔄 Scan ArXiv Now", type="primary"):
        with st.spinner("Fetching ArXiv..."):
            try:
                config = ConfigLoader()
                miner = ArxivMiner(config)
                papers = miner.fetch_latest_papers(max_results=80)
                top_papers = [p for p in papers if p['hype_score'] >= 20]
                for p in top_papers:
                    if hasattr(p.get('published'), 'isoformat'):
                        p['published'] = p['published'].isoformat()
                save_data("papers_latest.json", top_papers)
                st.success(f"Found {len(top_papers)} papers!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")
    st.header("📡 Radar Channels")
    config_loader = ConfigLoader()
    channels = config_loader.load_channels()
    channel_names = ["All Channels"] + [c.name for c in channels]
    selected_channel = st.radio("Focus Area:", channel_names)

last_updated_component("papers_latest.json")

# --- Load cached analyses ---
all_analyses = load_data("paper_analyses.json") or {}

# --- Display Papers ---
data = load_data("papers_latest.json")

if not data:
    st.info("No data. Click 'Scan ArXiv Now'.")
else:
    filtered_data = data if selected_channel == "All Channels" else [p for p in data if selected_channel in p.get('channels', [])]

    if not filtered_data:
        st.info(f"No papers in '{selected_channel}'.")
    
    for i, p in enumerate(filtered_data[:20]):
        score = p['hype_score']
        color = "#FF4444" if score >= 80 else "#FF8800" if score >= 50 else "#4488FF"
        paper_id = p['url'].split('/')[-1]  # Use ArXiv ID as key
        
        with st.container():
            st.markdown(f"""
            <div style="border-left: 4px solid {color}; padding: 10px 15px; margin-bottom:4px; background-color: #262730; border-radius: 5px;">
                <h4><span style="color:{color}">[{score}]</span> <a href="{p['url']}" target="_blank" style="color:white;">{p['title']}</a></h4>
                <p style="color:#888; font-size:0.8em;">{' • '.join(p.get('signals', []))}</p>
                <p style="color:#aaa; font-size:0.85em;">{p['abstract'][:200]}...</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons row
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("📋 评审报告", key=f"ref_{i}"):
                    with st.spinner("生成评审..."):
                        try:
                            engine = InsightEngine()
                            analysis = engine.deep_dive(p)
                            all_analyses[paper_id] = {"type": "referee", "data": analysis}
                            save_data("paper_analyses.json", all_analyses)
                            st.rerun()
                        except Exception as e:
                            st.error(f"{e}")
            
            with col2:
                if st.button("📚 技术解读", key=f"learn_{i}"):
                    with st.spinner("生成解读..."):
                        try:
                            engine = InsightEngine()
                            result = engine.technical_learning(p)
                            all_analyses[paper_id] = {"type": "learning", "data": result}
                            save_data("paper_analyses.json", all_analyses)
                            st.rerun()
                        except Exception as e:
                            st.error(f"{e}")
            
            with col3:
                # Show "View Result" only if this paper has been analyzed
                if paper_id in all_analyses:
                    analysis_info = all_analyses[paper_id]
                    label = "📋 查看报告" if analysis_info["type"] == "referee" else "📚 查看解读"
                    if st.button(label, key=f"view_{i}"):
                        st.session_state[f"show_{paper_id}"] = not st.session_state.get(f"show_{paper_id}", False)
                        st.rerun()
            
            # Display analysis inline if toggled on
            if paper_id in all_analyses and st.session_state.get(f"show_{paper_id}", False):
                analysis_info = all_analyses[paper_id]
                
                if analysis_info["type"] == "learning":
                    # Markdown display for technical learning
                    with st.expander("📚 技术学习型解读", expanded=True):
                        st.markdown(analysis_info["data"])
                        if st.button("❌ 收起", key=f"close_{i}"):
                            st.session_state[f"show_{paper_id}"] = False
                            st.rerun()
                else:
                    # Simplified referee display (inline)
                    d = analysis_info["data"]
                    with st.expander("📋 Referee Report", expanded=True):
                        meta = d.get('meta', {})
                        st.markdown(f"**{meta.get('one_liner', '')}**")
                        
                        verd = d.get('verdict', {})
                        scores = verd.get('scores', {})
                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("创新", f"{scores.get('novelty', '?')}/5")
                        c2.metric("工程", f"{scores.get('engineering_value', '?')}/5")
                        c3.metric("严谨", f"{scores.get('scientific_rigor', '?')}/5")
                        c4.metric("复现", f"{scores.get('reproducibility', '?')}/5")
                        
                        st.success(f"💎 {verd.get('key_takeaway', '')}")
                        
                        if st.button("📖 查看完整报告", key=f"full_{i}"):
                            save_data("deep_dive_current.json", d)
                            st.rerun()
                        
                        if st.button("❌ 收起", key=f"closex_{i}"):
                            st.session_state[f"show_{paper_id}"] = False
                            st.rerun()
