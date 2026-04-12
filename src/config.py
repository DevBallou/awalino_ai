from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    app_env: str = os.getenv("APP_ENV", "test").lower()
    llm_provider: str = os.getenv("LLM_PROVIDER", "auto").lower()

    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1")

    temperature: float = float(os.getenv("TEMPERATURE", "0.2"))

    use_postgres_memory: bool = os.getenv("USE_POSTGRES_MEMORY", "true").lower() == "true"
    postgres: str = os.getenv(
        "POSTGRES_NEON",
        "POSTGRES_DSN",
     #    "postgresql://postgres:postgres@localhost:5432/awalino_agent",
    )

    ddgs_max_results: int = int(os.getenv("DDGS_MAX_RESULTS", "5"))


DEFAULT_SYSTEM_PROMPT = (
    "You are a general-purpose assistant. Use tools when needed, be precise, "
    "and cite useful facts from attached documents or images when available."
)
