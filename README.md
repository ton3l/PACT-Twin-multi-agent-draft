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
- `src/main.py`: Ponto de entrada que instancia a aplicação FastAPI.
- `src/agents/`: Contém as definições dos agentes.
- `pixi.toml`: Configurações de ambiente e tarefas.

_Descrição gerada com assitência de IA_