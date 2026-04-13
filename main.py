from __future__ import annotations

from dotenv import load_dotenv

from src.config import Settings
from src.file_context import build_file_context
from src.graph_agent import build_agent, invoke_agent


def _parse_files(raw: str) -> list[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def main():
    load_dotenv(override=True)

    settings = Settings()
    agent = build_agent(settings)

    print("Awalino Agent is running.")
    print("Commands: /files <path1,path2>, /clearfiles, /exit")

    thread_id = input("Thread id [default]: ").strip() or "default"
    active_files: list[str] = []

    while True:
        user_text = input("You: ").strip()
        if not user_text:
            continue

        if user_text.lower() in {"/exit", "/quit"}:
            print("Bye.")
            break

        if user_text.startswith("/files "):
            active_files = _parse_files(user_text.replace("/files ", "", 1))
            print(f"Attached {len(active_files)} file(s).")
            continue

        if user_text == "/clearfiles":
            active_files = []
            print("File context cleared.")
            continue

        file_context = build_file_context(active_files) if active_files else ""
        answer = invoke_agent(
            agent=agent,
            user_text=user_text,
            thread_id=thread_id,
            file_context=file_context,
        )
        print(f"Agent: {answer}")


if __name__ == "__main__":
    main()
