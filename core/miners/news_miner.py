import feedparser
import logging
from typing import List, Dict, Any
from core.utils.config_loader import ConfigLoader

logger = logging.getLogger(__name__)

class NewsMiner:
    def __init__(self, config_loader: ConfigLoader):
        self.config = config_loader.load()
        
        # Categorized Feeds
        self.feeds = {
            "official": {
                "OpenAI Blog": "https://openai.com/blog/rss.xml",
                "Hugging Face Blog": "https://huggingface.co/blog/feed.xml",
                "Google AI Blog": "http://googleaiblog.blogspot.com/atom.xml",
                "DeepMind": "https://deepmind.google/blog/rss.xml",
                "Microsoft Research": "https://www.microsoft.com/en-us/research/feed/",
                "AWS Machine Learning": "https://aws.amazon.com/blogs/machine-learning/feed/"
            },
            "media": {
                "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
                "The Verge AI": "https://www.theverge.com/rss/artificial-intelligence/index.xml",
                "Wired AI": "https://www.wired.com/feed/category/ai/latest/rss",
                "MIT Tech Review": "https://www.technologyreview.com/feed/",
                "Simon Willison": "https://simonwillison.net/atom/everything/", # Engineering/Security
                "Last Week in AI": "https://lastweekin.ai/feed", # Newsletter
            },
            "tools": {} # Dynamic from yaml
        }

        # Load tools from config
        if hasattr(self.config, 'tools'):
            for t in self.config.tools:
                self.feeds['tools'][t.name] = t.url

        # Load media from config (Merging with defaults)
        if hasattr(self.config, 'media_sources'):
            for m in self.config.media_sources:
                 # Support both Dict and Object access depending on how pydantic parsed it
                 name = m.get('name') if isinstance(m, dict) else m.name
                 url = m.get('url') if isinstance(m, dict) else m.url
                 self.feeds['media'][name] = url


        
    def fetch_by_category(self, category: str, max_items: int = 5) -> List[Dict[str, Any]]:
        """
        Fetch news for a specific category ('official' or 'media')
        """
        if category not in self.feeds:
            return []
            
        news_items = []
        target_feeds = self.feeds[category]
        
        logger.info(f"Fetching RSS feeds for category: {category}...")
        
        for source_name, url in target_feeds.items():
            try:
                # Set specific timeout to avoid hanging
                feed = feedparser.parse(url)
                if not feed.entries:
                    continue
                
                # Get latest 1-2 items per feed
                limit = 2 if category == 'official' else 1
                for entry in feed.entries[:limit]:
                    item = {
                        "source": source_name,
                        "title": entry.title,
                        "url": entry.link,
                        "published": entry.get('published', 'N/A'),
                        "summary": entry.get('summary', '')[:200] + "..."
                    }
                    news_items.append(item)
            except Exception as e:
                logger.error(f"Error fetching {source_name}: {e}")
                
        # Sort by somewhat recent if possible, otherwise just return list
        # We could parse dates but for MVP just shuffling/listing is fine.
        return news_items[:max_items]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    miner = NewsMiner(ConfigLoader())
    news = miner.fetch_latest_news()
    for n in news:
        print(f"[{n['source']}] {n['title']}\nLink: {n['url']}\n")
