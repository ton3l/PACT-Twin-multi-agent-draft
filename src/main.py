from typing import cast
from langchain.messages import AnyMessage
from langgraph.graph import END, StateGraph, START
from agents.states.messages_state import MessagesState
from agents.calculator import calculator_agent
from nodes.loop_node import loop_node
from nodes.tool_node import tool_node
from langchain.messages import HumanMessage

graph = StateGraph(MessagesState)

graph.add_node("agent", calculator_agent)
graph.add_node("tool_node", tool_node)

graph.add_edge(START, "agent")
graph.add_conditional_edges(
   "agent",
   loop_node,
   ["tool_node", END]
)
graph.add_edge("tool_node", "agent")

agent = graph.compile()

with open("graph.png", "wb") as f:
    f.write(agent.get_graph(xray=True).draw_mermaid_png())
print("Grafo salvo em graph.png")

# Invoke
messages: list[AnyMessage] = [HumanMessage(content="divide 10 and 4.")]
input_state: MessagesState = {"messages": messages, "llm_calls": 0}
result = cast(MessagesState, agent.invoke(input_state))
for m in result["messages"]:
    m.pretty_print()
