from langchain_core.language_models.chat_models import BaseChatModel
from langchain_ollama import ChatOllama


def model() -> BaseChatModel:
    return ChatOllama(
        model="llama3.1:8b",
        temperature=0,
        # other params...
    )
