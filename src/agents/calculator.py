from langchain.messages import SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool

from prompts.calculator_prompts import CALCULATOR_SYSTEM_PROMPT
from states.messages_state import MessagesState


def def_calculator_agent(llm: BaseChatModel, tools: list[BaseTool]):
    """Calculator Agent Factory"""

    agent = llm.bind_tools(tools)

    def calculator_agent(state: MessagesState):
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
