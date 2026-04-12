# Awalino AI

## 📌 Description du projet

Awalino AI est un projet collaboratif visant à développer une application intelligente pour l’apprentissage du Tashelhit et de la Darija.  
L’objectif est de proposer une plateforme moderne, accessible et évolutive, basée sur l’intelligence artificielle, afin de faciliter l’apprentissage des langues locales marocaines et de promouvoir l’inclusion numérique.

Ce dépôt sert de base au développement, au versioning et à la collaboration selon un workflow Git/DevOps structuré.

---

## 👥 Membres de l’équipe

- Hicham
- Oussama

---

## 🔁 Schéma du Workflow Git

            feature/ma-fonctionnalite
                     |
                     v
                   develop
                     |
                     v
                    main

Flux de travail :

1. Créer une branche depuis `develop` :
   feature/ma-fonctionnalite

2. Développer et faire des commits sur la branche feature

3. Ouvrir une Pull Request :
   feature/\* → develop

4. Après validation et tests :
   develop → main (Release)

Règles :

- `main` : branche stable (production)
- `develop` : branche d’intégration
- `feature/*` : nouvelles fonctionnalités
- Aucun push direct sur `main` (ni sur `develop` si protégé)
- Tout passe par Pull Request + review

## Architecture

- `main.py`: interactive CLI
- `src/graph_agent.py`: graph definition, tool routing, memory saver
- `src/llm_factory.py`: provider and model selection
- `src/tools.py`: DDGS tool
- `src/file_context.py`: document/image ingestion
- `src/config.py`: environment configuration

## Quickstart

1. Install dependencies:

```bash
uv venv && uv sync or pip install -e .
```

2. Configure environment:

```bash
cp .env.example .env
```

Then edit `.env`.

3. Run:

```bash
python main.py
```

Or:

```bash
awalino-agent
```

## Environment Variables

Core:

- `APP_ENV=test|prod`
- `LLM_PROVIDER=auto|openai|groq|ollama|llama`
- `TEMPERATURE=0.2`

Providers:

- `OPENAI_API_KEY`
- `GROQ_API_KEY`
- `OPENAI_MODEL`
- `GROQ_MODEL`
- `OLLAMA_MODEL`

Search:

- `DDGS_MAX_RESULTS=5`

PostgreSQL memory:

- `USE_POSTGRES_MEMORY=true`
- `POSTGRES_DSN=postgresql://postgres:postgres@localhost:5432/awalino_agent`

## Test vs Production Behavior

When `LLM_PROVIDER=auto`:

- `APP_ENV=prod`: tries OpenAI, then Groq, then Ollama
- `APP_ENV=test`: tries Groq, then OpenAI, then Ollama

You can always force a provider using `LLM_PROVIDER`.

## Using Docs and Images

Inside CLI:

- Attach files: `/files C:/path/doc1.pdf,C:/path/image1.png`
- Clear file context: `/clearfiles`
- Exit: `/exit`

Supported file types:

- Docs: `.txt`, `.md`, `.py`, `.json`, `.csv`, `.yaml`, `.yml`, `.pdf`
- Images: `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`, `.bmp`

Note: image handling currently extracts metadata for context. If you want full vision analysis, we can add provider-specific multimodal message payloads next.

## PostgreSQL + Metabase

If Metabase is connected to the same PostgreSQL instance, you can inspect agent checkpoint tables and thread history directly in dashboards.

## Suggested Next Enhancements

- Add a retrieval index (pgvector) for long document memory
- Add provider-specific vision input formatting
- Add FastAPI endpoint for API-based agent serving
