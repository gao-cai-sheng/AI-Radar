import yaml
from pathlib import Path
from typing import List, Dict, Optional, Any
from pydantic import BaseModel

class AuthorConfig(BaseModel):
    name: str
    weight: int

class OrgConfig(BaseModel):
    name: str
    weight: int

class FeedConfig(BaseModel):
    name: str
    url: str
    type: Optional[str] = None # e.g. "official", "media", "reddit", "forum"

class ChannelConfig(BaseModel):
    name: str
    description: str
    keywords: List[str]

class InfluencerConfig(BaseModel):
    authors: List[AuthorConfig] = []
    organizations: List[OrgConfig] = []
    news_feeds: List[FeedConfig] = []
    product_sources: List[FeedConfig] = []
    discourse_sources: List[FeedConfig] = []
    podcast_sources: List[FeedConfig] = []

class ConfigLoader:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self._config: Optional[InfluencerConfig] = None
        self._channels: List[ChannelConfig] = []

    def load(self) -> InfluencerConfig:
        influencer_path = self.config_dir / "influencers.yaml"
        if influencer_path.exists():
            with open(influencer_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            self._config = InfluencerConfig(**data)
        else:
             self._config = InfluencerConfig()
        return self._config

    def load_channels(self) -> List[ChannelConfig]:
        channel_path = self.config_dir / "channels.yaml"
        if channel_path.exists():
            with open(channel_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if data and 'channels' in data:
                    self._channels = [ChannelConfig(**c) for c in data['channels']]
        return self._channels

    @property
    def author_names(self) -> List[str]:
        if not self._config:
            self.load()
        return [a.name for a in self._config.authors]
    
    @property
    def org_names(self) -> List[str]:
        if not self._config:
            self.load()
        return [o.name for o in self._config.organizations]
