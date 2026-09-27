from functools import lru_cache

from langchain_core.language_models import BaseChatModel
from langchain_groq import ChatGroq

from app.core.config import settings


@lru_cache
def get_llm() -> BaseChatModel:
    provider = settings.llm_provider.lower()

    if provider == "groq":
        return ChatGroq(
            model=settings.llm_model,
            api_key=settings.groq_api_key, # type: ignore
            temperature=0.2,
        )

    raise ValueError(
        f"Unsupported LLM provider: {settings.llm_provider}"
    )