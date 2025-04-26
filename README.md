# 🚀 CodeSprint

Uma plataforma de desenvolvimento de projetos guiada por IA que ajuda desenvolvedores a iniciar novos projetos rapidamente.

![CodeSprint Banner](https://via.placeholder.com/1200x300?text=CodeSprint)

## 📋 Índice
- [Sobre o Projeto](#-sobre-o-projeto)
- [Arquitetura](#-arquitetura-do-sistema)
- [Funcionalidades](#-funcionalidades)
- [Requisitos](#-requisitos)
- [Instalação e Uso](#-instalação-e-uso)
- [Comandos Make](#-comandos-make)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Desenvolvimento](#-desenvolvimento)
- [Licença](#-licença)

## 🔍 Sobre o Projeto

O **CodeSprint** é uma plataforma inovadora que utiliza Inteligência Artificial para acelerar o desenvolvimento de novos projetos. Com uma interface intuitiva e responsiva, desenvolvedores podem especificar suas necessidades e obter um projeto base completo em questão de minutos.

## 🏗️ Arquitetura do Sistema

O CodeSprint é composto por quatro componentes principais:

1. **🖥️ Frontend** - Aplicação Next.js com Tailwind CSS que fornece uma interface responsiva para usuários.
2. **⚙️ Backend** - Servidor FastAPI que gerencia a comunicação entre o frontend e o serviço CrewAI.
3. **🧠 CrewAI** - Serviço especializado que utiliza modelos de IA para gerar projetos com base nas entradas do usuário.
4. **💾 Redis** - Banco de dados em memória usado para cache e gerenciamento de estado.

Além disso, o sistema utiliza o **🤖 Ollama** para executar modelos de linguagem de grande porte localmente.

## 🌟 Funcionalidades

- ✨ **Geração de Projetos Personalizados** baseados em:
  - 📚 Áreas de interesse
  - 🛠️ Stack tecnológico
  - 📝 Descrição do projeto
- 🔄 **Integração** com serviços externos (EXA.ai)
- 📱 **Interface Responsiva** para todos os dispositivos
- 🧩 **Fluxo Intuitivo** de criação de projetos

## 📋 Requisitos

- 🐳 Docker e Docker Compose
- 📦 Node.js 18+ (para desenvolvimento local do frontend)
- 🐍 Python 3.10+ (para desenvolvimento local do backend e CrewAI)
- 📄 Make (para utilizar os comandos do Makefile)

## 🚀 Instalação e Uso

### Passo 1: Clone o Repositório
```bash
git clone https://github.com/G00li/codesprint
cd codesprint
```

### Passo 2: Inicialize os Serviços
Você pode iniciar todos os serviços de uma só vez utilizando o comando Make:
```bash
make up
```

Ou utilizando Docker Compose diretamente:
```bash
docker-compose up -d
```

### Passo 3: Acesse a Aplicação
Após a inicialização, acesse o frontend em [http://localhost:3000](http://localhost:3000)

## 🛠️ Comandos Make

O projeto inclui um Makefile para facilitar operações comuns:

| Comando | Descrição |
|---------|-----------|
| `make help` | Exibe ajuda sobre os comandos disponíveis |
| `make up` | Inicia todos os containers do projeto |
| `make down` | Para todos os containers |
| `make restart` | Reinicia todos os containers |
| `make clean` | Remove todos os containers e volumes |
| `make up_crewai` | Inicia apenas o container CrewAI |
| `make down_crewai` | Para o container CrewAI |
| `make env_backend` | Ativa o ambiente Poetry do backend |
| `make env_crewai` | Ativa o ambiente Poetry do CrewAI |
| `make env_desactivate` | Desativa o ambiente Poetry atual |

## 📁 Estrutura do Projeto

```
codesprint/
├── 🖥️ frontend/            # Aplicação Next.js com Tailwind
│   ├── src/                # Código fonte do frontend
│   ├── public/             # Arquivos estáticos
│   └── Dockerfile          # Configuração do container
├── ⚙️ backend/             # API FastAPI
│   ├── app/                # Código fonte do backend
│   └── Dockerfile          # Configuração do container
├── 🧠 crewai/              # Serviço de IA para geração de projetos
│   ├── app/                # Código fonte do serviço CrewAI
│   └── Dockerfile          # Configuração do container
├── 📄 docker-compose.yaml  # Configuração dos serviços Docker
├── 📄 makefile             # Scripts e comandos úteis
└── 📄 README.md            # Documentação do projeto
```

## 💻 Desenvolvimento

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

## 🔄 Fluxo de Funcionamento

1. O usuário acessa a interface do frontend e especifica os detalhes do projeto desejado
2. O backend recebe essas informações e as envia para o serviço CrewAI
3. O CrewAI utiliza modelos de IA (via Ollama) para gerar o esqueleto do projeto
4. O resultado é retornado ao usuário através do frontend
5. O usuário pode baixar o projeto gerado ou solicitar ajustes

## 📄 Licença

Este projeto está licenciado sob os termos da [MIT License](LICENSE).

---

Desenvolvido com ❤️ pelo time CodeSprint
