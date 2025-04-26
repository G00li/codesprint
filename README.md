# CodeSprint

Uma plataforma de desenvolvimento de projetos guiada por IA, que ajuda desenvolvedores a iniciar novos projetos rapidamente.

## Arquitetura do Sistema

O CodeSprint é composto por quatro componentes principais:

1. **Frontend** - Uma aplicação Next.js com Tailwind CSS que fornece uma interface responsiva para usuários.
2. **Backend** - Um servidor FastAPI que gerencia a comunicação entre o frontend e o serviço CrewAI.
3. **CrewAI** - Um serviço especializado que utiliza modelos de IA para gerar projetos com base nas entradas do usuário.
4. **Redis** - Um banco de dados em memória usado para cache e gerenciamento de estado.

Além disso, o sistema utiliza o **Ollama** para executar modelos de linguagem de grande porte localmente.

## Pré-requisitos

- Docker e Docker Compose
- Node.js 18+ (para desenvolvimento local do frontend)
- Python 3.10+ (para desenvolvimento local do backend e CrewAI)

## Inicializando o Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/codesprint.git
   cd codesprint
   ```

2. Inicie os serviços com Docker Compose:
   ```bash
   docker-compose up
   ```

3. Acesse o frontend em [http://localhost:3000](http://localhost:3000)

## Configuração de Desenvolvimento

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

### CrewAI

```bash
cd crewai
poetry install
poetry run uvicorn app.main:app --reload --port 8004
```

## Estrutura do Projeto

```
codesprint/
├── frontend/            # Aplicação Next.js com Tailwind
├── backend/             # API FastAPI 
├── crewai/              # Serviço de IA para geração de projetos
├── docker-compose.yaml  # Configuração dos serviços
└── README.md
```

## Funcionalidades

- Geração de projetos personalizados baseados em:
  - Áreas de interesse
  - Stack tecnológico
  - Descrição do projeto
- Integração opcional com serviços externos (EXA.ai)
- Interface responsiva para todos os dispositivos

## Licença

Este projeto está licenciado sob os termos da [MIT License](LICENSE).
