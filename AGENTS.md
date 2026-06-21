# AGENTS.md — PACT-Twin Multi-Agent

## Project Overview

PACT-Twin Multi-Agent is a **LangGraph-based multi-agent system** built as an academic project at UFCG (Universidade Federal de Campina Grande). It implements a graph-driven agent architecture where LLM-powered agents coordinate through LangGraph's `StateGraph`, using tool-calling to perform tasks. The current prototype features a calculator agent that can perform arithmetic operations via Ollama-hosted local LLMs.

## Tech Stack

| Layer            | Technology                          | Notes                                        |
|------------------|-------------------------------------|----------------------------------------------|
| Language         | Python ≥ 3.14                       | Type hints used throughout                   |
| Agent Framework  | LangGraph ≥ 1.2.4                   | `StateGraph` for graph-based orchestration   |
| LLM Abstraction  | LangChain ≥ 1.3.9                   | Messages, tools, and system prompts          |
| LLM Provider     | LangChain-Ollama ≥ 1.1.0           | Local inference via Ollama                   |
| LLM Model        | `llama3.1:8b` (via `ChatOllama`)    | Temperature 0, deterministic outputs         |
| Package Manager  | Pixi (conda-forge + PyPI)           | `pixi.toml` at project root                  |
| Platforms        | `linux-64`, `win-64`                |                                              |

## Architecture

The system follows a **graph-based agent loop** pattern:

```
START → agent (LLM) → loop_node (conditional) → tool_node → agent → … → END
```

- **Agent Node** (`src/agents/calculator.py`): Invokes the LLM with a system prompt and bound tools. Returns the LLM response and increments `llm_calls`.
- **Tool Node** (`src/nodes/tool_node.py`): Iterates over tool calls from the last LLM message, invokes each tool, and appends `ToolMessage` results.
- **Loop Node** (`src/nodes/loop_node.py`): Conditional router — if the last message contains tool calls, routes back to `tool_node`; otherwise ends the graph.

### State

Defined in `src/agents/states/messages_state.py` as a `TypedDict`:
- `messages`: `list[AnyMessage]` — accumulated via `operator.add` (append-only reducer).
- `llm_calls`: `int` — counts how many times the LLM has been invoked.

## Directory Structure

```
├── AGENTS.md                        # This file — project rules for AI agents
├── README.md                        # Project readme (Portuguese)
├── pixi.toml                        # Pixi workspace config, deps, and tasks
├── pixi.lock                        # Lockfile (auto-generated, do not edit)
├── .gitignore
├── .vscode/
│   └── settings.json                # Editor settings (Pylance, IntelliSense)
└── src/
    ├── main.py                      # Entrypoint — builds and runs the StateGraph
    ├── agents/
    │   ├── calculator.py            # Calculator agent definition
    │   ├── models/
    │   │   └── llama3_1_8b.py       # ChatOllama model instance
    │   ├── states/
    │   │   └── messages_state.py    # MessagesState TypedDict (graph state schema)
    │   └── tools/
    │       └── arithmetics.py       # @tool functions: multiply, add, subtract
    └── nodes/
        ├── loop_node.py             # Conditional edge — continue or end the loop
        └── tool_node.py             # Executes tool calls from the last LLM message
```

## Conventions & Rules

### Code Style
- **Language**: Python code, comments, and docstrings should be written in **English**.
- **Documentation**: README and user-facing docs are in **Portuguese (pt-BR)**.
- **Type hints**: Always use type hints for function arguments and return types.
- **Docstrings**: Every public function and class must have a docstring.
- **Imports**: Use relative imports within `src/` subpackages (e.g., `from models.llama3_1_8b import model`).

### Project Structure
- **Agents** go in `src/agents/`. Each agent is a function that takes state and returns a state update dict.
- **Tools** go in `src/agents/tools/`. Each tool is decorated with `@tool` from `langchain.tools` and must have a docstring with `Args:` section for LLM schema generation.
- **Models** go in `src/agents/models/`. Each file exports a configured LLM instance.
- **States** go in `src/agents/states/`. State schemas are `TypedDict` subclasses.
- **Nodes** go in `src/nodes/`. Graph nodes that are not agents (e.g., tool execution, conditional routing).

### Development Workflow
- **Install dependencies**: `pixi install`
- **Run the project**: `pixi start` (or `pixi run python src/main.py`)
- **Run a single script**: `pixi run python <path>`
- **Add a conda package**: `pixi add <package>`
- **Add a PyPI package**: `pixi add --pypi <package>`
- **Ollama prerequisite**: The local Ollama server must be running with the `llama3.1:8b` model pulled before starting the app.

### Things to Avoid
- Do not edit `pixi.lock` manually — it is auto-generated.
- Do not commit `.pixi/` contents (except `.pixi/config.toml`), `__pycache__/`, or `.env*` files.
- Do not hardcode API keys or secrets in source files; use environment variables.
