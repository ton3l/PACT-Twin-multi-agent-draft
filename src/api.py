from typing import cast

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect

from agent_graph import Agent

load_dotenv()


app = FastAPI()

# 1. Rota fantasma apenas para gerar a documentação no Swagger
@app.post("/ws/agent/", tags=["WebSockets"])
async def docs_websocket_agente(payload):
    """
    **ATENÇÃO: Não chame esta rota HTTP.**

    Conecte via: `ws://localhost:8000/ws/agent`

    Esta rota existe apenas para documentar a estrutura dos JSONs
    enviados pelo cliente e retornados pelo servidor durante a conexão.
    """


@app.websocket("/ws/agent")
async def agent_chat(websocket: WebSocket, agent=Depends(Agent)):
    await websocket.accept()
    agent = cast(Agent, agent)

    try:
        while True:
            # 2. Fica aguardando mensagens do cliente
            mensagem = await websocket.receive_text()

            # 3. Processa e responde
            await websocket.send_text(await agent.chat(mensagem))

    except WebSocketDisconnect:
        # 4. Lida com a desconexão de forma graciosa
        print("Cliente desconectado")
