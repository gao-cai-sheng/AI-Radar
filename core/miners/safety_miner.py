import feedparser
import logging
from typing import List, Dict, Any
from core.utils.config_loader import ConfigLoader

logger = logging.getLogger(__name__)

class SafetyMiner:
    def __init__(self, config_loader: ConfigLoader):
        self.config = config_loader.load()
        # Keywords to filter generic feeds (like OpenAI Blog) for Safety content
        self.safety_keywords = [
            "safety", "alignment", "risk", "red team", "preparedness", 
            "superalignment", "policy", "societal", "governance", "audit"
        ]
        
    def fetch_safety_reports(self, max_items: int = 10) -> List[Dict[str, Any]]:
        reports = []
        
        if not hasattr(self.config, 'safety_sources'):
            logger.warning("No safety_sources found in config.")
            return []

        for source in self.config.safety_sources:
            try:
                # logger.info(f"Scanning Safety Source: {source.name}...")
                feed = feedparser.parse(source.url)
                
                for entry in feed.entries[:max_items]:
                    title = entry.title
                    summary = entry.get('summary', '') or entry.get('description', '')
                    full_text = (title + " " + summary).lower()
                    
                    # Filtering Logic
                    # If it's a dedicated source (Alignment Forum), keep everything.
                    # If it's a general source (OpenAI Blog), only keep Safety-related items.
                    is_dedicated = "Alignment" in source.name or "Future of Life" in source.name
                    
                    if not is_dedicated:
                        # Check keywords
                        if not any(k in full_text for k in self.safety_keywords):
                            continue

                    reports.append({
                        "source": source.name,
                        "title": title,
                        "url": entry.link,
                        "published": entry.get('published', 'N/A'),
                        "summary": summary[:300] + "..."
                    })
            except Exception as e:
                logger.error(f"Error checking {source.name}: {e}")
                
        return reports

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    miner = SafetyMiner(ConfigLoader())
    reports = miner.fetch_safety_reports()
    for r in reports:
        print(f"🛡️ [{r['source']}] {r['title']}\n   {r['url']}\n")
