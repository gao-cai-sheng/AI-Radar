import os
import json
import logging
from typing import List, Dict, Any, Optional
from openai import OpenAI
from datetime import datetime

logger = logging.getLogger(__name__)

class DigestEngine:
    """
    Generates AI-powered digests/summaries for news feeds.
    降维引擎: 把 N 条新闻压缩成核心要点。
    """
    
    def __init__(self):
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if not api_key:
            raise ValueError("Missing DEEPSEEK_API_KEY environment variable")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        self.model = "deepseek-chat"
    
    def generate_news_digest(self, news_items: List[Dict[str, Any]], max_items: int = 15) -> str:
        """
        Takes a list of news items and generates a concise Chinese digest.
        """
        if not news_items:
            return "暂无新闻数据，请先抓取 News Feed。"
        
        # Prepare context for LLM
        news_text = ""
        for i, item in enumerate(news_items[:max_items]):
            news_text += f"{i+1}. [{item.get('source', 'Unknown')}] {item.get('title', 'No Title')}\n"
            news_text += f"   {item.get('summary', '')[:150]}\n\n"
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        prompt = f"""
你是一位专业的 AI 行业分析师。请根据以下 {len(news_items[:max_items])} 条新闻标题和摘要，生成一份精炼的 "今日 AI 速览"。

要求:
1. 用中文输出
2. 分为 "🔥 核心动态" (3-5 条最重要的) 和 "📌 其他值得关注" (简短一句话列表)
3. 每条要点要归纳，不要照抄标题
4. 如果有多条新闻讲同一件事，合并为一条
5. 风格简洁、信息密度高

新闻数据:
{news_text}

请输出今日 AI 速览 ({today}):
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a concise AI industry analyst."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.5
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Digest generation failed: {e}")
            return f"Digest 生成失败: {e}"

    def generate_podcast_digest(self, episodes: List[Dict[str, Any]], max_items: int = 5) -> str:
        """
        Summarizes podcast episodes into key takeaways.
        """
        if not episodes:
            return "暂无播客数据。"
        
        ep_text = ""
        for i, ep in enumerate(episodes[:max_items]):
            ep_text += f"{i+1}. [{ep.get('source', '')}] {ep.get('title', '')}\n"
            ep_text += f"   嘉宾: {', '.join(ep.get('guests', ['Unknown']))}\n"
            ep_text += f"   摘要: {ep.get('summary', '')[:100]}\n\n"
        
        prompt = f"""
作为 AI 领域的观察者，请根据以下播客摘要，提炼出 "本周对话精华"。

要求:
1. 用中文输出
2. 每个播客提炼 1-2 个核心观点或"金句"
3. 如果能看出行业趋势，请在最后总结

播客数据:
{ep_text}

请输出本周对话精华:
"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a podcast summarizer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.5
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Podcast digest failed: {e}")
            return f"Podcast Digest 生成失败: {e}"


if __name__ == "__main__":
    # Test
    engine = DigestEngine()
    test_news = [
        {"source": "OpenAI", "title": "GPT-5 Announced", "summary": "OpenAI unveils next gen model..."},
        {"source": "Google AI", "title": "Gemini 2.0 Flash", "summary": "Google releases faster model..."},
    ]
    print(engine.generate_news_digest(test_news))
