from agno.agent import Agent
from agno.models.ollama import Ollama


class ReporterAgent(Agent):
    def __init__(self):
        super().__init__(
            model=Ollama(id="llama3.1:8b"),
            system_message="Você fala português. Você é um relator, seu trabalho é pegar os dados que forem enviados para você no formato de JSON e gerar um relatório completo deles em markdown. Você deve fazer considerações construtivas sobre os dados e informar sobre a qualidade deles.",
            markdown=True,
        )
