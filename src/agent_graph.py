import asyncio
from typing import cast

from langchain.messages import AnyMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode

from agents.calculator import def_calculator_agent
from graph_state import GraphState
from llms.gpt_oss_120b import gpt_oss_120b
from nodes.loop_node import loop_node
from tools.arithmetics import ARITHMETIC_TOOLS


class Agent:
    _agent: CompiledStateGraph
    _state: GraphState

    def __init__(self) -> None:
        graph = StateGraph(GraphState)

        graph.add_node("agent", def_calculator_agent(gpt_oss_120b(), ARITHMETIC_TOOLS))
        graph.add_node("tool_node", ToolNode(ARITHMETIC_TOOLS))

        graph.add_edge(START, "agent")
        graph.add_conditional_edges("agent", loop_node, ["tool_node", END])
        graph.add_edge("tool_node", "agent")

        self._agent = graph.compile()

        messages: list[AnyMessage] = []
        self._state = {"messages": messages, "llm_calls": 0}

    async def chat(self, input: str):
        self._state["messages"].append(HumanMessage(content=input))
        self._state = cast(GraphState, await self._agent.ainvoke(self._state))
        return cast(str, self._state["messages"][-1].content)


async def _main():
    # Generate graph image
    # with open("graph.png", "wb") as f:
    # f.write(agent.get_graph(xray=True).draw_mermaid_png())
    # print("Grafo salvo em graph.png")

    from dotenv import load_dotenv

    load_dotenv()

    agent = Agent()
    last_msg_printed = 0
    while True:
        print("\n")
        await agent.chat(
            input("""
================
PACT-Twin-Agent-Example# """)
        )
        for i in range(last_msg_printed, len(agent._state["messages"])):
            m = agent._state["messages"][i]
            m.pretty_print()
        last_msg_printed = len(agent._state["messages"])


if __name__ == "__main__":
    asyncio.run(_main())
