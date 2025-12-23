import feedparser
import logging
import time
from typing import List, Dict, Any
from core.utils.config_loader import ConfigLoader

logger = logging.getLogger(__name__)

class RedditMiner:
    def __init__(self, config_loader: ConfigLoader):
        self.config = config_loader.load()
        # Feedparser usually handles UAs well, but we can set it if needed globally
        # or just rely on standard fetching.
        
    def fetch_community_pulse(self, max_items: int = 15) -> List[Dict[str, Any]]:
        posts = []
        
        if not hasattr(self.config, 'social_sources'):
            logger.warning("No social_sources found in config.")
            return []

        for source in self.config.social_sources:
            try:
                # Universal RSS Fetching (Works for Reddit .rss and HN rss)
                posts.extend(self._fetch_rss(source))
            except Exception as e:
                logger.error(f"Error fetching {source.name}: {e}")
                
        return posts[:max_items * len(self.config.social_sources)] 

    def _fetch_rss(self, source) -> List[Dict[str, Any]]:
        items = []
        try:
           # feedparser handles HTTP requests internally
           logger.info(f"Fetching RSS: {source.name}...")
           feed = feedparser.parse(source.url)
           
           if feed.bozo and feed.bozo_exception:
               logger.warning(f"Feed error for {source.name}: {feed.bozo_exception}")

           # Get a few top items
           limit = 8
           for entry in feed.entries[:limit]:
               # Extract basic info
               content = entry.get('summary', '') or entry.get('description', '')
               
               # Clean up Reddit HTML content a bit if possible (optional)
               # But for raw feed, raw text is okay.
               
               items.append({
                   "source": source.name,
                   "title": entry.title,
                   "url": entry.link,
                   "score": "🔥 Hot", # RSS doesn't give score, assumes 'Hot' feed
                   "comments": "💬 Topic",
                   "author": entry.get('author', 'Unknown'),
                   "created_utc": time.time(), 
                   "selftext": content[:300] + "..."
               })
        except Exception as e:
             logger.error(f"RSS error for {source.name}: {e}")
        return items

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    miner = RedditMiner(ConfigLoader())
    pulse = miner.fetch_community_pulse()
    for p in pulse:
        print(f"[{p['source']}] {p['title']}\nLink: {p['url']}\n")
