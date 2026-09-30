from langchain.messages import SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool

from graph_state import GraphState
from prompts.calculator_prompts import CALCULATOR_SYSTEM_PROMPT


def def_calculator_agent(llm: BaseChatModel, tools: list[BaseTool]):
    """Calculator Agent Factory"""

    agent = llm.bind_tools(tools)

    def calculator_agent(state: GraphState):
        """LLM doing a calculator role"""

        return {
            "messages": [
                agent.invoke(
                    [SystemMessage(content=CALCULATOR_SYSTEM_PROMPT)]
                    + state["messages"],
                )
            ],
            "llm_calls": state.get("llm_calls", 0) + 1,
        }

    return calculator_agent
