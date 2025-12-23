import feedparser
import logging
from typing import List, Dict, Any
from core.utils.config_loader import ConfigLoader

logger = logging.getLogger(__name__)

class InterviewMiner:
    def __init__(self, config_loader: ConfigLoader):
        logging.basicConfig(level=logging.INFO)
        self.config_loader = config_loader
        self.config = self.config_loader.load()
        
    def fetch_interviews(self, max_items_per_feed: int = 20) -> List[Dict[str, Any]]:
        """
        Fetches interviews and filters them by Author Names.
        """
        matches = []
        
        # 1. Build Watchlist
        # We look for names like "Sam Altman", "Ilya", "Kaiming He"
        watchlist = set(a.name.lower() for a in self.config.authors)
        # Also include Org names? Maybe less relevant for interviews, but "DeepMind CEO" is good.
        # Let's stick to Authors for "Big Talk" focus.
        
        logger.info(f"Scanning for interviews with: {list(watchlist)[:5]}...")
        
        if not hasattr(self.config, 'interview_sources'):
            logger.warning("No interview_sources found in config.")
            return []

        # 2. Scan Feeds
        for source in self.config.interview_sources:
            try:
                # logger.info(f"Checking {source.name}...")
                feed = feedparser.parse(source.url)
                
                if not feed.entries:
                    continue
                
                for entry in feed.entries[:max_items_per_feed]:
                    title = entry.title
                    summary = entry.get('summary', '') or entry.get('description', '')
                    full_text = (title + " " + summary).lower()
                    
                    # 3. Match Logic
                    detected_names = []
                    for name in watchlist:
                        # Simple substring match. 
                        # "Sam Altman" in "Sam Altman Interview" -> Match
                        # "Ilya" in "Ilya Sutskever" -> Match
                        # Split name to handle partials? No, full name is safer to avoid false positives.
                        # But user config has full names.
                        if name in full_text:
                            detected_names.append(name)
                            
                    if detected_names:
                        # Found a match!
                        matches.append({
                            "source": source.name,
                            "title": title,
                            "url": entry.link,
                            "published": entry.get('published', 'N/A'),
                            "guests": detected_names,
                            "summary": summary[:300] + "..."
                        })
            except Exception as e:
                logger.error(f"Error checking {source.name}: {e}")
                
        return matches

if __name__ == "__main__":
    miner = InterviewMiner(ConfigLoader())
    interviews = miner.fetch_interviews(max_items_per_feed=50) # Scan deeper history
    for i in interviews:
        print(f"🎙️ [{i['source']}] {i['title']}")
        print(f"   Guests: {i['guests']}")
        print(f"   Link: {i['url']}\n")
