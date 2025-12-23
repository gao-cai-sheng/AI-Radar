import arxiv
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging
from core.utils.config_loader import ConfigLoader
from core.utils.code_signals import CodeSignals

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArxivMiner:
    def __init__(self, config_loader: ConfigLoader):
        self.config_loader = config_loader
        self.influencers = self.config_loader.load()
        self.client = arxiv.Client()
        self.code_signals = CodeSignals()

    def fetch_latest_papers(self, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch papers from CS.CL, CS.CV, CS.LG from the last 7 days.
        """
        # Construct query for "Artificial Intelligence" related categories
        # cat:cs.CL OR cat:cs.AI OR cat:cs.CV OR cat:cs.LG
        search_query = 'cat:cs.CL OR cat:cs.AI OR cat:cs.CV OR cat:cs.LG'
        
        search = arxiv.Search(
            query=search_query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )

        papers = []
        author_watchlist = set(a.lower() for a in self.config_loader.author_names)
        org_watchlist = set(k.lower() for k in self.config_loader.org_names)

        logger.info(f"Fetching max {max_results} papers from ArXiv...")
        
        for result in self.client.results(search):
            paper_data = self._process_paper(result, author_watchlist, org_watchlist)
            papers.append(paper_data)

        # Sort by 'hype_score' descending
        papers.sort(key=lambda x: x['hype_score'], reverse=True)
        return papers

    def _process_paper(self, result: arxiv.Result, author_watchlist: set, org_watchlist: set) -> Dict[str, Any]:
        """
        Convert arxiv result to dictionary and calculate Hype Score.
        """
        authors = [a.name for a in result.authors]
        title = result.title
        abstract = result.summary
        full_text = (title + " " + abstract).lower()
        
        # --- SCORING LOGIC ---
        hype_score = 0
        signals = []

        # 1. Check Authors
        for author in authors:
            if author.lower() in author_watchlist:
                hype_score += 100 # MASSIVE BOOST
                signals.append(f"Star Author: {author}")
        
        # 2. Check Org Keywords
        for org in org_watchlist:
            if org in full_text:
                hype_score += 50
                signals.append(f"Org Mention: {org}")

        # 3. Check Code Signals (GitHub & HuggingFace)
        links = self.code_signals.extract_links(abstract)  # Note: ArXiv API abstracts often contain links
        
        if 'github' in links:
            stars = self.code_signals.get_github_stars(links['github'])
            if stars > 0:
                # Score formula: 1 point per 10 stars, max 50 points cap for pure stars (to balance author weight)
                star_points = min(int(stars / 10), 100)
                hype_score += star_points
                signals.append(f"GitHub: {stars} stars (+{star_points})")
            else:
                # Even if 0 stars, having code is good
                hype_score += 10 
                signals.append("Code Available")

        if 'hf' in links:
            likes = self.code_signals.get_hf_likes(links['hf'])
            if likes > 0:
                # HF likes are valuable. 1 point per 5 likes.
                like_points = min(int(likes / 5), 100)
                hype_score += like_points
                signals.append(f"HF Likes: {likes} (+{like_points})")

        # 4. Check Radar Channels
        active_channels = []
        channels = self.config_loader.load_channels()
        for ch in channels:
            for kw in ch.keywords:
                if kw.lower() in full_text:
                    active_channels.append(ch.name)
                    break # Matched this channel, move to next channel
        
        if active_channels:
             signals.append(f"Channels: {', '.join(active_channels)}")

        paper_data = {
            "title": title,
            "authors": authors,
            "published": result.published,
            "url": result.entry_id,
            "abstract": abstract,
            "hype_score": hype_score,
            "signals": signals,
            "links": links,
            "channels": active_channels
        }
        
        return paper_data

if __name__ == "__main__":
    # Test Run
    loader = ConfigLoader()
    miner = ArxivMiner(loader)
    
    # Lazy load InsightEngine to avoid errors if API key is missing during simple tests
    try:
        from core.writers.insight_engine import InsightEngine
        insight = InsightEngine()
        print("Insight Engine: ONLINE")
    except Exception as e:
        insight = None
        print(f"Insight Engine: OFFLINE ({e})")

    print("Miner initialized. Watched authors:", loader.author_names)
    print("Fetching papers...")
    
    results = miner.fetch_latest_papers(max_results=50)
    
    print(f"\nFetched {len(results)} papers.")
    print("\n--- TOP HYPE PAPERS & INSIGHTS ---")
    
    for p in results[:5]:
        score = p['hype_score']
        if score > 0:
            print(f"🔥 [Score: {score}] {p['title']}")
            print(f"Type: {p['signals']}")
            print(f"Link: {p['url']}")
            
            # TRIGGER ANALYST if score is high enough (e.g. > 40)
            if insight and score >= 40:
                print("   > Refining info with AI...")
                analysis = insight.analyze_paper(p)
                print(f"   > Analysis: {analysis}")
            print("-" * 50)

