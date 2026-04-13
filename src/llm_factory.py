from __future__ import annotations

import os
from typing import Any

from .config import Settings


def _has_env(name: str) -> bool:
    value = os.getenv(name, "")
    return bool(value.strip())


def _resolve_provider(settings: Settings) -> str:
    if settings.llm_provider != "auto":
        return settings.llm_provider

    # In prod, prefer OpenAI first, then Groq, then local Ollama.
    if settings.app_env == "prod":
        if _has_env("OPENAI_API_KEY"):
            return "openai"
        if _has_env("GROQ_API_KEY"):
            return "groq"
        return "ollama"

    # In test, prefer Groq for fast/cheap experimentation when available.
    if _has_env("GROQ_API_KEY"):
        return "groq"
    if _has_env("OPENAI_API_KEY"):
        return "openai"
    return "ollama"


def build_chat_model(settings: Settings) -> Any:
    provider = _resolve_provider(settings)

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=settings.openai_model,
            temperature=settings.temperature,
        )

    if provider == "groq":
        from langchain_groq import ChatGroq

        return ChatGroq(
            model=settings.groq_model,
            temperature=settings.temperature,
        )

    if provider in {"ollama", "llama"}:
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=settings.ollama_model,
            temperature=settings.temperature,
        )

    raise ValueError(
        "Unsupported LLM provider. Use one of: auto, openai, groq, ollama, llama."
    )
