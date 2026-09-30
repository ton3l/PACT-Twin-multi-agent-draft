from langchain_core.messages import AIMessage
from langgraph.graph import END

from graph_state import GraphState


def loop_node(state: GraphState) -> str:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call."""

    last_message = state["messages"][-1]

    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tool_node"

    return END
