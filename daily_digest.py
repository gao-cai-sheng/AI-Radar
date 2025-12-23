import os
import json
from datetime import datetime
from core.miners.arxiv_miner import ArxivMiner
from core.miners.news_miner import NewsMiner
from core.writers.insight_engine import InsightEngine
from core.utils.config_loader import ConfigLoader

def generate_daily_digest():
    print("🚀 Starting Daily AI Trend Radar...")
    
    # 1. Setup
    config = ConfigLoader()
    arxiv = ArxivMiner(config)
    news = NewsMiner(config)
    
    try:
        insight = InsightEngine()
        print("✅ AI Analyst Online")
    except:
        insight = None
        print("⚠️ AI Analyst Offline (Using passive mode)")

    # 2. Fetch Content
    # A. Papers
    papers = arxiv.fetch_latest_papers(max_results=50)
    top_papers = [p for p in papers if p['hype_score'] >= 40][:5] 
    
    # Analyze Top Papers
    analyzed_papers = []
    for p in top_papers:
        # Fix: Convert datetime to string for JSON serialization
        if hasattr(p.get('published'), 'isoformat'):
            p['published'] = p['published'].isoformat()
            
        if insight:
             print(f"Analyzing: {p['title']}...")
             analysis = insight.analyze_paper(p)

             if isinstance(analysis, str):
                 p['ai_analysis'] = {'verdict': 'N/A', 'tldr': analysis}
             else:
                 p['ai_analysis'] = analysis
        analyzed_papers.append(p)
    
    # B. Official Blogs
    official_news = news.fetch_by_category("official", max_items=10)

    # C. Media & Newsletters
    media_news = news.fetch_by_category("media", max_items=10)

    # D. Tools & Vibe Coding (NEW)
    tool_news = news.fetch_by_category("tools", max_items=10)

    # 3. Create Structured Data
    digest_data = {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "hype_papers": analyzed_papers,
        "official_news": official_news,
        "media_news": media_news,
        "tool_news": tool_news
    }

    # 4. Save
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save JSON (Source of Truth for App)
    json_filename = f"{output_dir}/digest_{datetime.now().strftime('%Y%m%d')}.json"
    with open(json_filename, "w", encoding='utf-8') as f:
        json.dump(digest_data, f, ensure_ascii=False, indent=2)

    # Save Markdown (Backup / Human Readability)
    md_filename = f"{output_dir}/briefing_{datetime.now().strftime('%Y%m%d')}.md"
    _save_markdown(digest_data, md_filename)
        
    print(f"✅ Briefing generated: {json_filename} & {md_filename}")
    return json_filename

def _save_markdown(data, filename):
    md = f"# 📡 Daily AI Trend Radar ({data['date']})\n\n"
    
    md += "## 🏆 Top Hype Papers\n"
    for p in data['hype_papers']:
        md += f"### [{p['hype_score']}] {p['title']}\n"
        md += f"**Signals**: `{', '.join(p['signals'])}`\n"
        md += f"**Link**: {p['url']}\n"
        if 'ai_analysis' in p:
             a = p['ai_analysis']
             md += f"> **Verdict**: {a.get('verdict')}\n> {a.get('tldr')}\n"
        md += "\n"

    md += "## 📰 Industry Beat\n"
    for n in data['official_news']:
        md += f"- [{n['source']}] [{n['title']}]({n['url']})\n"

    md += "## 🗞️ AI Newsletter\n"
    for n in data['media_news']:
        md += f"- [{n['source']}] [{n['title']}]({n['url']})\n"

    md += "## 🛠️ AI Dev Tools\n"
    for n in data.get('tool_news', []):
        md += f"- [{n['source']}] [{n['title']}]({n['url']})\n"

        
    with open(filename, "w", encoding='utf-8') as f:
        f.write(md)

if __name__ == "__main__":
    generate_daily_digest()
