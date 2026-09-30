# AGENTS.md — PACT-Twin Multi-Agent

## Project Overview

PACT-Twin Multi-Agent is a **LangGraph-based multi-agent system** built as an academic project at UFCG (Universidade Federal de Campina Grande). It implements a graph-driven agent architecture where LLM-powered agents coordinate through LangGraph's `StateGraph`, using tool-calling to perform tasks. The current prototype is a calculator agent served over a **FastAPI WebSocket API** (`ws://localhost:8000/ws/agent`), backed by the Groq-hosted `gpt-oss-120b` model.

## Tech Stack

| Layer            | Technology                          | Notes                                        |
|------------------|-------------------------------------|----------------------------------------------|
| Language         | Python ≥ 3.14                       | Type hints used throughout                   |
| Agent Framework  | LangGraph ≥ 1.2.4                   | `StateGraph` for graph-based orchestration   |
| LLM Abstraction  | LangChain ≥ 1.3.9                   | Messages, tools, and system prompts          |
| LLM Provider     | LangChain-Groq ≥ 1.1.3              | Cloud inference via Groq (`GROQ_API_KEY`)    |
| LLM Model        | `gpt-oss-120b` (via `ChatGroq`)     | Temperature 0, deterministic outputs         |
| Local Alternative| LangChain-Ollama ≥ 1.1.0            | `llama3.1:8b` via `ChatOllama` (see `src/llms/`) |
| Web API          | FastAPI ≥ 0.141 + fastapi-cli       | WebSocket endpoint, `Depends` DI             |
| Env vars         | python-dotenv ≥ 1.2                 | `.env` loaded by `load_dotenv()`             |
| Package Manager  | Pixi (conda-forge + PyPI)           | `pixi.toml` at project root                  |
| Platforms        | `linux-64`, `win-64`                |                                              |

## Architecture

The system follows a **graph-based agent loop** pattern:

```
START → agent (LLM) → loop_node (conditional) → tool_node → agent → … → END
```

- **Agent Node** (`src/agents/calculator.py`): Factory function that injects the LLM and bound tools, returning the pure node function.
- **Tool Node** (`langgraph.prebuilt.ToolNode`): Native LangGraph node that executes tool calls from the last LLM message.
- **Loop Node** (`src/nodes/loop_node.py`): Conditional router — if the last message contains tool calls, routes back to `tool_node`; otherwise ends the graph.

### API Layer

- **`src/api.py`**: FastAPI app. The WebSocket route (`/ws/agent`) uses `Depends(Agent)`, so **one `Agent` instance is created per connection** — each connection owns its own conversation session. Outgoing messages go through `websocket.send_text(...)`.
- **`src/agent_graph.py` — class `Agent`**: imperative facade that compiles the graph, holds the per-session `_state`, and exposes `chat(input) -> str`. It is the **only place** where state is mutated (append user message, then replace `_state` with the graph's returned state).

### State

Defined in `src/states/messages_state.py` as a `TypedDict`:
- `messages`: `list[AnyMessage]` — accumulated via `operator.add` (append-only reducer).
- `llm_calls`: `int` — counts how many times the LLM has been invoked.

### Prompts

System prompts live in `src/prompts/` as module-level constants (e.g., `CALCULATOR_SYSTEM_PROMPT` in `calculator_prompts.py`), kept out of node logic. The calculator agent **always responds in Brazilian Portuguese (pt-BR)**, regardless of the input language.

## Directory Structure

```
├── AGENTS.md                        # This file — project rules for AI agents
├── README.md                        # Project readme (Portuguese)
├── pixi.toml                        # Pixi workspace config, deps, and tasks
├── pixi.lock                        # Lockfile (auto-generated, do not edit)
├── .env                             # Local secrets (GROQ_API_KEY) — never commit
├── .gitignore
├── .vscode/
│   └── settings.json                # Editor settings (Pylance, IntelliSense)
└── src/
    ├── api.py                       # Entrypoint — FastAPI app + WebSocket route
    ├── agent_graph.py               # Agent facade — builds/compiles the StateGraph, holds session state
    ├── agents/
    │   └── calculator.py            # Calculator agent node (Factory)
    ├── llms/
    │   ├── gpt_oss_120b.py          # ChatGroq factory (primary)
    │   └── llama3_1_8b.py           # ChatOllama factory (local alternative)
    ├── prompts/
    │   └── calculator_prompts.py    # CALCULATOR_SYSTEM_PROMPT constant
    ├── states/
    │   └── messages_state.py        # MessagesState TypedDict (graph state schema)
    ├── tools/
    │   └── arithmetics.py           # @tool functions: multiply, add, subtract
    └── nodes/
        └── loop_node.py             # Conditional edge — continue or end the loop
```

## Conventions & Rules

### Code Style
- **Language**: Python code, comments, and docstrings should be written in **English**.
- **Documentation**: README and user-facing docs are in **Portuguese (pt-BR)**.
- **Type hints**: Always use type hints for function arguments and return types.
- **Docstrings**: Every public function and class must have a docstring.
- **Imports**: Absolute imports rooted at `src/` (e.g., `from agents.calculator import def_calculator_agent`), enabled by `PYTHONPATH=src`.

### Project Structure & Multi-Paradigm Pattern
The project uses a **hybrid paradigm** — a functional core wrapped in a thin imperative shell — together with Dependency Injection, as standard in LangGraph:

**Functional core** (pure data and functions, no hidden state):
- **Agents** (`src/agents/`): Defined as Factory functions that receive dependencies (LLMs, tools) and return the pure node function (e.g., `def_calculator_agent(llm, tools)`).
- **Tools** (`src/tools/`): Each tool is decorated with `@tool` from `langchain.tools`. They are exported as explicit immutable global lists (e.g., `ARITHMETIC_TOOLS = [multiply, add, subtract]`) using `UPPER_SNAKE_CASE`.
- **LLMs** (`src/llms/`): Exported as factory getter functions (e.g., `def gpt_oss_120b() -> BaseChatModel`) to avoid side effects on import.
- **Prompts** (`src/prompts/`): System prompts are immutable module-level constants.
- **States** (`src/states/`): State schemas are `TypedDict` subclasses to maintain functional purity (dumb data containers).
- **Nodes** (`src/nodes/`): Custom graph nodes. Tool execution relies on the native `ToolNode` from `langgraph.prebuilt`.

**Imperative shell** (the single class with state):
- **`Agent`** (`src/agent_graph.py`): The only class in the project. It wraps the compiled graph plus the session `_state` behind an async `chat()` method and is the sole owner of mutation. Do not mutate graph state outside this class.

**Dependency Injection** works at two layers: constructor-level (LLMs and tools injected into agent factories) and framework-level (`Depends(Agent)` in FastAPI, giving one instance per WebSocket connection).

### Development Workflow
- **Install dependencies**: `pixi install`
- **Run the API server**: `pixi start` (runs `fastapi dev src/api.py`)
- **Run a single script**: `pixi run python <path>`
- **Add a conda package**: `pixi add <package>`
- **Add a PyPI package**: `pixi add --pypi <package>`
- **Secrets**: `GROQ_API_KEY` must be set in `.env` (loaded via `load_dotenv()`). The Groq model fails without it; switching to `llama3_1_8b` instead requires a local Ollama server with `llama3.1:8b` pulled.

### Things to Avoid
- Do not edit `pixi.lock` manually — it is auto-generated.
- Do not commit `.pixi/` contents (except `.pixi/config.toml`), `__pycache__/`, or `.env*` files.
- Do not hardcode API keys or secrets in source files; use environment variables.
- Do not bypass `Agent.chat()` to write to graph state — it is the single mutation point.
