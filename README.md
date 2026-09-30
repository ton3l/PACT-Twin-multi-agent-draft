# PACT-Twin Multi-Agent

Assistente calculadora construído com **LangGraph** e exposto via **WebSocket (FastAPI)**. O agente executa operações aritméticas por meio de tools (`add`, `subtract`, `multiply`) e responde sempre em pt-BR.

## Pré-requisitos
Antes de partir para a execução do projeto verifique se o Pixi está instalado no seu sistema:
```bash
  pixi --version
  ```
Acesse https://pixi.sh/ para realizar a instalação caso necessário.

## 🔑 Variáveis de Ambiente

O modelo em produção (`gpt-oss-120b`) é hospedado no **Groq**. Crie um arquivo `.env` na raiz do projeto com sua chave:

```bash
GROQ_API_KEY=sua-chave-aqui
```

> O `.env` é ignorado pelo Git — nunca commit chaves. Para usar o modelo local alternativo (`llama3.1:8b` via Ollama), altere a fábrica de LLM em `src/agent_graph.py` e garanta que o servidor Ollama esteja rodando com o modelo baixado.

## 🛠 Pixi: Gerenciamento de Projeto

O projeto utiliza o [Pixi](https://pixi.sh/) como gerenciador de pacotes e ambientes, garantindo reprodutibilidade total.

### Execução do Projeto
1. **Instalação de dependências**
Configure o ambiente e instale as dependências:
```bash
  pixi install
  ```
2. **Iniciar o servidor de API**
```bash
  pixi start
  ```
O servidor sobe em modo de desenvolvimento (`fastapi dev src/api.py`) em `http://localhost:8000`.

### Conectando ao Agente

O agente é consumido por WebSocket:

```
ws://localhost:8000/ws/agent
```

Envie uma mensagem de texto (ex.: `quanto é 12 + 7 * 3?`) e o servidor responderá com o resultado. A documentação interativa fica em `http://localhost:8000/docs`.

### Adicionando Dependências
- **Pacotes Conda (Padrão):**
  ```bash
  pixi add <nome-do-pacote>
  ```
- **Pacotes PyPI (Python):**
  ```bash
  pixi add --pypi <nome-do-pacote>
  ```

### Executando Arquivos Individuais
Para rodar qualquer script Python dentro do ambiente do projeto:
```bash
pixi run python caminho/do/arquivo.py
```

## 📁 Estrutura do Projeto
- `src/api.py`: Ponto de entrada — aplicação FastAPI e rota WebSocket (`/ws/agent`).
- `src/agent_graph.py`: Classe `Agent` — monta/compila o `StateGraph`, guarda o estado da sessão e expõe `chat()`.
- `src/agents/`: Definição dos agentes (fábricas de nós).
- `src/llms/`: Fábricas de modelos — `gpt_oss_120b` (Groq, padrão) e `llama3_1_8b` (Ollama, alternativa local).
- `src/prompts/`: System prompts como constantes de módulo.
- `src/nodes/`: Nós customizados do grafo (ex.: `loop_node`).
- `src/tools/`: Tools com `@tool` (`add`, `subtract`, `multiply`).
- `src/states/`: Schema de estado do grafo (`MessagesState`).
- `pixi.toml`: Configurações de ambiente e tarefas.

## Arquitetura

```
START → agent (LLM) → loop_node (condicional) → tool_node → agent → … → END
```

Cada conexão WebSocket recebe uma instância própria de `Agent` (via `Depends`), ou seja, cada conexão é uma sessão de conversa independente.

_Descrição gerada com assitência de IA_
