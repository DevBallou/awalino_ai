from __future__ import annotations

from duckduckgo_search import DDGS

try:
    from langchain.tools import tool
except Exception:
    from langchain_core.tools import tool


def _format_results(results: list[dict]) -> str:
    if not results:
        return "No relevant web results found."

    lines: list[str] = []
    for idx, item in enumerate(results, start=1):
        title = item.get("title", "(no title)")
        href = item.get("href", "")
        body = item.get("body", "")
        lines.append(f"{idx}. {title}\nURL: {href}\nSnippet: {body}")
    return "\n\n".join(lines)


@tool
def ddgs_search(query: str, max_results: int = 5) -> str:
    """Search the public web via DuckDuckGo and return concise ranked results."""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
    return _format_results(results)


def get_tools(default_max_results: int):
    # Keep tools list explicit so you can add more tools safely later.
    search_tool = ddgs_search

    # Wrap a configured closure so max_results defaults from environment.
    @tool("ddgs_search_configured")
    def ddgs_search_configured(query: str) -> str:
        """Search the web using environment-configured max results."""
        return ddgs_search.invoke({"query": query, "max_results": default_max_results})

    return [search_tool, ddgs_search_configured]
