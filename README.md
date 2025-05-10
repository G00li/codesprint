# 🚀 CodeSprint

[![ETIC](https://img.shields.io/badge/ETIC-Backend2-blue)](https://github.com/seu-usuario/codesprint)
[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)](https://github.com/seu-usuario/codesprint)

## 📋 Sumário
- [Sobre o Projeto](#-sobre-o-projeto)
- [Tecnologias e Ferramentas](#-tecnologias-e-ferramentas)
- [Instalação](#-instalação)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura do Sistema](#-arquitetura-do-sistema)
- [Diagnóstico e Troubleshooting](#-diagnóstico-e-troubleshooting)
- [Monitoramento](#-monitoramento)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

## 🎯 Sobre o Projeto

Bem-vindo ao **CodeSprint**! 🎉

O CodeSprint é uma plataforma que utiliza Inteligência Artificial para auxiliar no desenvolvimento de novos projetos. Com uma interface intuitiva e responsiva, desenvolvedores podem especificar suas necessidades e obter um projeto base completo em questão de minutos.

### 🌟 Destaques
- Desenvolvimento assistido por IA
- Interface web responsiva
- Geração de código base
- Ambiente Docker completo
- Ferramentas de diagnóstico integradas

## 🛠️ Tecnologias e Ferramentas

### Frontend
- **React/Next.js** - Framework para interface do usuário
- **TypeScript** - Tipagem estática
- **TailwindCSS** - Estilização moderna

### Backend
- **Python/FastAPI** - API REST de alta performance
- **SQLAlchemy** - ORM para banco de dados
- **Pydantic** - Validação de dados

### IA e Processamento
- **CrewAI** - Orquestração de agentes de IA
- **Ollama** - Execução de modelos de linguagem

### Infraestrutura
- **Docker** - Containerização
- **Redis** - Cache e filas
- **PostgreSQL** - Banco de dados principal

## 💻 Instalação

### Pré-requisitos
- Docker e Docker Compose
- 8GB+ de RAM
- 20GB+ de espaço em disco
- Conexão estável com internet

### Passo a Passo

1. **Clone o Repositório**
```bash
git clone https://github.com/seu-usuario/codesprint.git
cd codesprint
```

2. **Inicie os Serviços**
```bash
# Método 1: Script de inicialização
./start_services.sh

# Método 2: Usando Makefile
make up
```

3. **Verifique a Instalação**
```bash
./check_services.sh
```

4. **Acesse a Aplicação**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentação API: http://localhost:8000/docs

### Comandos Makefile Disponíveis

O projeto inclui um Makefile com vários comandos úteis para gerenciar o ambiente:

```bash
# Iniciar todos os serviços
make up

# Parar todos os serviços
make down

# Reiniciar todos os serviços
make restart

# Limpar ambiente (remove contêineres e volumes)
make clean

# Verificar status dos serviços
make status

# Ver logs de todos os serviços
make logs

# Ver logs de um serviço específico
make logs SERVICE=backend

# Executar testes
make test

# Construir imagens Docker
make build
```

## ✨ Funcionalidades

### 1. Desenvolvimento Assistido por IA
- Geração de código base para novos projetos
- Sugestões de implementação via IA
- Documentação automática do código gerado

### 2. Interface Web
- Dashboard intuitivo
- Formulários para especificação de projetos
- Visualização do progresso de geração
- Ferramentas de diagnóstico integradas

### 3. Diagnóstico e Monitoramento
- Interface de diagnóstico web
- Scripts de verificação de serviços
- Endpoints de health check
- Logs detalhados por serviço

## 🏗️ Arquitetura do Sistema

O CodeSprint utiliza uma arquitetura distribuída com os seguintes serviços:

- **Frontend** (porta 3000)
- **Backend** (porta 8000)
- **CrewAI** (porta 8004)
- **Ollama** (porta 11434)
- **Redis** (porta 6379)

## 🔍 Diagnóstico e Troubleshooting

### Ferramentas de Diagnóstico
- Interface web de diagnóstico (http://localhost:3000/diagnostico)
- Scripts de verificação automática
- Endpoints de health check
- Logs detalhados por serviço

### Comandos Úteis
```bash
# Verificar status dos serviços
docker-compose ps

# Ver logs específicos
docker-compose logs [serviço]

# Diagnóstico de rede
docker-compose exec backend python -m app.services.network_diagnostics
```

## 📊 Monitoramento

### Recursos do Sistema
```bash
# Monitoramento em tempo real
docker stats

# Verificar modelos disponíveis
docker exec -it codesprint-ollama-1 ollama list
```

## 📄 Licença

Desenvolvido com ❤️ pelo time CodeSprint, ou seja, Leandro Oliveira