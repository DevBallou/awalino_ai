from __future__ import annotations

from typing import Annotated, TypedDict

try:
    from langchain.messages import AIMessage, HumanMessage, SystemMessage
except Exception:
    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

try:
    from langgraph.checkpoint.memory import MemorySaver
except Exception:
    from langgraph.checkpoint.memory import InMemorySaver as MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from .config import DEFAULT_SYSTEM_PROMPT, Settings
from .llm_factory import build_chat_model
from .tools import get_tools


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    file_context: str


def _build_checkpointer(settings: Settings):
    if not settings.use_postgres_memory:
        return MemorySaver()

    try:
        from langgraph.checkpoint.postgres import PostgresSaver

        checkpointer = PostgresSaver.from_conn_string(settings.postgres)

        # Some versions return a context manager from from_conn_string.
        if hasattr(checkpointer, "__enter__"):
            checkpointer = checkpointer.__enter__()

        if hasattr(checkpointer, "setup"):
            checkpointer.setup()

        return checkpointer
    except Exception as exc:
        print(f"[WARN] Postgres checkpointer unavailable, using in-memory saver: {exc}")
        return MemorySaver()


def build_agent(settings: Settings):
    llm = build_chat_model(settings)
    tools = get_tools(settings.ddgs_max_results)
    llm_with_tools = llm.bind_tools(tools)

    def call_model(state: AgentState):
        file_context = (state.get("file_context") or "").strip()
        messages = list(state["messages"])

        if file_context:
            context_msg = SystemMessage(
                content=(
                    "Attached file context is provided below. Use it when relevant and "
                    "state clearly when context is incomplete.\n\n"
                    f"{file_context}"
                )
            )
            messages = [context_msg, *messages]

        response = llm_with_tools.invoke([
            SystemMessage(content=DEFAULT_SYSTEM_PROMPT),
            *messages,
        ])
        return {"messages": [response]}

    def should_continue(state: AgentState):
        last = state["messages"][-1]
        if isinstance(last, AIMessage) and last.tool_calls:
            return "tools"
        return END

    graph = StateGraph(AgentState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", ToolNode(tools))

    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")

    return graph.compile(checkpointer=_build_checkpointer(settings))


def invoke_agent(agent, user_text: str, thread_id: str, file_context: str = "") -> str:
    result = agent.invoke(
        {
            "messages": [HumanMessage(content=user_text)],
            "file_context": file_context,
        },
        config={"configurable": {"thread_id": thread_id}},
    )

    last = result["messages"][-1]
    return last.content if hasattr(last, "content") else str(last)
