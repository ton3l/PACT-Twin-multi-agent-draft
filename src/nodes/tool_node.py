from langchain.messages import ToolMessage
from agents.tools.arithmetics import ARITHMETIC_TOOLS
from agents.states.messages_state import MessagesState
from langchain_core.messages import AIMessage

def tool_node(state: MessagesState):
    """Performs the tool call"""

    last_message  = state["messages"][-1]
    if not isinstance(last_message, AIMessage):
        raise Exception("Messages that aren't comming from AI can not perform tool calls")

    result = []
    for tool_call in last_message.tool_calls:
        tool = ARITHMETIC_TOOLS[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}