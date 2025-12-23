import re
import requests
import os
import logging
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)

class CodeSignals:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"

    def extract_links(self, text: str) -> Dict[str, str]:
        """
        Extracts first GitHub and HuggingFace links found in text.
        Returns: {'github': '...', 'hf': '...'}
        """
        links = {}
        
        # Regex for GitHub
        github_match = re.search(r'(https?://github\.com/[\w-]+/[\w.-]+)', text)
        if github_match:
            links['github'] = github_match.group(1)

        # Regex for HuggingFace (models or papers or spaces, usually models)
        # Matches huggingface.co/Org/Model
        hf_match = re.search(r'(https?://huggingface\.co/[\w-]+/[\w.-]+)', text)
        if hf_match:
            links['hf'] = hf_match.group(1)
            
        return links

    def get_github_stars(self, url: str) -> int:
        """
        Fetches numbers of stars for a GitHub repo.
        """
        try:
            # Extract owner/repo from URL
            # https://github.com/owner/repo
            parts = url.rstrip('/').split('/')
            if len(parts) < 2: 
                return 0
            owner, repo = parts[-2], parts[-1]
            
            api_url = f"https://api.github.com/repos/{owner}/{repo}"
            resp = requests.get(api_url, headers=self.headers, timeout=5)
            
            if resp.status_code == 200:
                data = resp.json()
                return data.get('stargazers_count', 0)
            elif resp.status_code == 403:
                logger.warning("GitHub API Rate Limit Exceeded")
            elif resp.status_code == 404:
                # Repo might be private or deleted
                pass
        except Exception as e:
            logger.warning(f"Failed to fetch GitHub stars: {e}")
            
        return 0

    def get_hf_likes(self, url: str) -> int:
        """
        Fetches numbers of likes for a Hugging Face model/dataset.
        """
        try:
            # https://huggingface.co/DeepSeek-AI/DeepSeek-V3
            # API: https://huggingface.co/api/models/DeepSeek-AI/DeepSeek-V3
            
            # Need to determine if it is model, dataset or space. 
            # Simplified: Assume model first.
            
            clean_url = url.replace("https://huggingface.co/", "")
            parts = clean_url.split('/')
            if len(parts) < 2:
                return 0
            
            # Try model endpoint
            object_id = "/".join(parts[-2:]) # Org/Name
            api_url = f"https://huggingface.co/api/models/{object_id}"
            
            resp = requests.get(api_url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                return data.get('likes', 0)
            
            # TODO: try /datasets/ or /spaces/ if needed, but models are primary target
            
        except Exception as e:
            logger.warning(f"Failed to fetch HF likes: {e}")
            
        return 0
