from langchain.messages import SystemMessage
from agents.states.messages_state import MessagesState
from agents.models.llama3_1_8b import model
from agents.tools.arithmetics import multiply, add, subtract

def calculator_agent(state: MessagesState):
    """LLM doing a calculator role"""

    agent = model.bind_tools([multiply, add, subtract])

    return {
       "messages": [
            agent.invoke(
                [
                    SystemMessage(
                        content="You are a helpful assistant tasked with performing arithmetic on a set of inputs. If you do not have a tool to perform the required operation inform the user"
                    )
                ]
                + state["messages"],
            )
        ], 
        "llm_calls": state.get('llm_calls', 0) + 1
    }