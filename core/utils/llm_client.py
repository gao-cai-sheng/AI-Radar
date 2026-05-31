import os
from dataclasses import dataclass
from typing import Any, Optional, Tuple


@dataclass(frozen=True)
class LLMConfig:
    api_key: str
    model: str
    base_url: Optional[str]


def load_llm_config() -> LLMConfig:
    """Load an OpenAI-compatible LLM configuration from environment variables."""
    llm_api_key = os.getenv("LLM_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    api_key = llm_api_key or openai_api_key or deepseek_api_key

    if not api_key:
        raise ValueError(
            "Missing LLM API key. Set LLM_API_KEY, OPENAI_API_KEY, or DEEPSEEK_API_KEY."
        )

    base_url = os.getenv("LLM_BASE_URL")
    using_deepseek_fallback = bool(deepseek_api_key and not llm_api_key and not openai_api_key)

    if not base_url and using_deepseek_fallback:
        base_url = "https://api.deepseek.com"

    default_model = "deepseek-chat" if using_deepseek_fallback else "gpt-4o-mini"
    model = os.getenv("LLM_MODEL", default_model)

    return LLMConfig(api_key=api_key, model=model, base_url=base_url)


def create_llm_client() -> Tuple[Any, str]:
    from openai import OpenAI

    config = load_llm_config()
    kwargs = {"api_key": config.api_key}

    if config.base_url:
        kwargs["base_url"] = config.base_url

    return OpenAI(**kwargs), config.model
