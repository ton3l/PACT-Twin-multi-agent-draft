# PACT-Twin Multi-Agent

## Pré-requisitos
Antes de partir para a execução do projeto verifique se o Pixi está instalado no seu sistema:
```bash
  pixi --version
  ```
Acesse https://pixi.sh/ para realizar a instalação caso necessário.

## 🛠 Pixi: Gerenciamento de Projeto

O projeto utiliza o [Pixi](https://pixi.sh/) como gerenciador de pacotes e ambientes, garantindo reprodutibilidade total.

### Execução do Projeto
1. **Instalação de dependências**
Configure o ambiente e instale as dependências:
```bash
  pixi install
  ```
2. **Modo de Desenvolvimento (FastAPI Dev)**
Inicie o servidor em modo de desenvolvimento:
  ```bash
  pixi run fastapi-dev
  ```

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

---

## 🚀 FastAPI: Interface da API

A API é construída com FastAPI e oferece uma interface automática para documentação e testes.

### Documentação Interativa
Após iniciar o servidor (geralmente em `http://127.0.0.1:8000`), você pode acessar:

- **Swagger UI (`/docs`):** Permite visualizar todos os endpoints, modelos de dados e testar as requisições diretamente pelo navegador.
- **Redoc (`/redoc`):** Uma documentação alternativa e mais limpa.

### Testando o Relatório
No `/docs`, localize o endpoint `POST /report`, clique em "Try it out", insira o JSON no corpo da requisição e veja o agente gerar o relatório em tempo real.

---

## 🤖 Agno & Ollama

O projeto utiliza o framework **Agno** para criar agentes especializados.

### Agente de Relatórios (`ReporterAgent`)
Localizado em `agents/reporter.py`, este agente:
- Utiliza o modelo **llama3.1:8b** via Ollama.
- Está configurado com uma `system_message` que o instrui a converter JSON em relatórios Markdown detalhados.

### Requisito: Ollama
Para que os agentes funcionem, você deve ter o **Ollama** instalado e o modelo baixado:
1. Certifique-se que o serviço do Ollama está rodando.
2. Baixe o modelo necessário:
   ```bash
   ollama pull llama3.1:8b
   ```

---

## 📁 Estrutura do Projeto
- `main.py`: Ponto de entrada que instancia a aplicação FastAPI.
- `agents/`: Contém as definições dos agentes.
- `pixi.toml`: Configurações de ambiente e tarefas.

_Descrição gerada com assitência de IA_