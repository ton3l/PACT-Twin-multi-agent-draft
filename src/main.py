from typing import cast
from langchain.messages import AnyMessage
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode
from models.llama3_1_8b import model
from states.messages_state import MessagesState
from agents.calculator import def_calculator_agent
from nodes.loop_node import loop_node
from langchain.messages import HumanMessage
from tools.arithmetics import ARITHMETIC_TOOLS


def main():
    graph = StateGraph(MessagesState)

    graph.add_node("agent", def_calculator_agent(model(), ARITHMETIC_TOOLS))
    graph.add_node("tool_node", ToolNode(ARITHMETIC_TOOLS))

    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", loop_node, ["tool_node", END])
    graph.add_edge("tool_node", "agent")

    agent = graph.compile()

    # with open("graph.png", "wb") as f:
    # f.write(agent.get_graph(xray=True).draw_mermaid_png())
    # print("Grafo salvo em graph.png")

    # Invoke
    messages: list[AnyMessage] = [
        HumanMessage(content=input("Pergunte ao agente calculador: "))
    ]
    input_state: MessagesState = {"messages": messages, "llm_calls": 0}
    result = cast(MessagesState, agent.invoke(input_state))
    for m in result["messages"]:
        m.pretty_print()


if __name__ == "__main__":
    main()
