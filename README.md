# 🚀 CodeSprint

[![ETIC](https://img.shields.io/badge/ETIC-Backend2-blue)](https://github.com/seu-usuario/codesprint)
[![Status](https://img.shields.io/badge/Status-completo-green)](https://github.com/seu-usuario/codesprint)

## 📋 Sumário
- [Sobre o Projeto](#-sobre-o-projeto)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Diagnóstico e Debug](#-diagnóstico-e-debug)
- [Tecnologias](#-tecnologias)
- [Workflow da Aplicação](#-workflow-da-aplicação)
- [Logging e Monitoramento](#-logging-e-monitoramento)
- [Testes de Conexão](#-testes-de-conexão)
- [Comandos Makefile](#-comandos-makefile)

## 🎯 Sobre o Projeto

O CodeSprint é uma plataforma inovadora que automatiza o processo de criação de projetos de software. Utilizando Inteligência Artificial avançada, o sistema permite que desenvolvedores especifiquem suas necessidades através de uma interface intuitiva e recebam um projeto base completo, pronto para desenvolvimento.

### 🌟 Principais Características
- Geração automática de código base
- Interface web responsiva e intuitiva
- Integração com agentes de IA para análise e desenvolvimento
- Ambiente Docker completo e isolado
- Sistema robusto de diagnóstico e monitoramento

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
# Iniciar todos os serviços
make up

# Verificar status
make status
```

3. **Verifique a Instalação**
```bash
# Executar testes de conexão
make test-connection
```

## 🎮 Como Usar

1. **Acesse a Interface**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Documentação API: http://localhost:8000/docs

2. **Crie um Novo Projeto**
   - Preencha o formulário com as especificações do projeto
   - Selecione as tecnologias desejadas
   - Defina os requisitos funcionais

3. **Acompanhe o Progresso**
   - Monitore o status da geração
   - Visualize os logs em tempo real
   - Receba notificações de conclusão

## 🔍 Diagnóstico e Debug

### Interface de Diagnóstico
- Acesse: http://localhost:3000/diagnostico
- Verifique o status de todos os serviços
- Monitore as conexões entre componentes
- Visualize logs em tempo real

### Comandos de Diagnóstico
```bash
# Verificar status dos serviços
make status

# Ver logs detalhados
make logs

# Testar conexões
make test-connection
```

## 🛠️ Tecnologias

### Frontend
- **React/Next.js**: Framework para interface do usuário
- **TypeScript**: Tipagem estática
- **TailwindCSS**: Estilização moderna
- **Axios**: Comunicação com API

### Backend
- **Python/FastAPI**: API REST de alta performance
- **Pydantic**: Validação de dados
- **Poetry**: Gerenciamento de dependências
- **Pytest**: Testes automatizados

### IA e Processamento
- **CrewAI**: Orquestração de agentes de IA
- **Ollama**: Execução de modelos de linguagem
- **LangChain**: Framework para aplicações de IA

### Infraestrutura
- **Docker**: Containerização
- **Redis**: Cache e filas
- **PostgreSQL**: Banco de dados principal
- **Nginx**: Proxy reverso

## 🔄 Workflow da Aplicação

### 1. Interação do Usuário
```
Frontend (React) → Formulário de Especificação → Validação Local
```

### 2. Processamento Backend
```
Frontend → Backend (FastAPI)
↓
Validação de Dados (Pydantic)
↓
Processamento Assíncrono
↓
Comunicação com CrewAI
```

### 3. Integração com IA
```
Backend → CrewAI
↓
Orquestração de Agentes
↓
Comunicação com Ollama
↓
Processamento de Modelos
↓
Geração de Código
```

### 4. Retorno e Feedback
```
CrewAI → Backend → Frontend
↓
Atualização em Tempo Real
↓
Notificação de Conclusão
```

## 📊 Logging e Monitoramento

### Níveis de Log
- **DEBUG**: Detalhes de execução
- **INFO**: Operações normais
- **WARNING**: Situações não críticas
- **ERROR**: Falhas e exceções

### Comandos de Logging
```bash
# Ver todos os logs
make logs

# Ver logs específicos
make logs SERVICE=backend
make logs SERVICE=frontend
make logs SERVICE=crewai

# Limpar logs
make clean-logs
```

## 🧪 Testes de Conexão

### Verificação de Serviços
```bash
# Testar todas as conexões
make test-connection

# Testar serviço específico
make test-connection SERVICE=backend
make test-connection SERVICE=crewai
make test-connection SERVICE=ollama
```

## 📝 Comandos Makefile

### Gerenciamento de Serviços
```bash
# Iniciar serviços
make up              # Inicia todos os serviços
make up SERVICE=xxx  # Inicia serviço específico

# Parar serviços
make down            # Para todos os serviços
make down SERVICE=xxx # Para serviço específico

# Reiniciar serviços
make restart         # Reinicia todos os serviços
make restart SERVICE=xxx # Reinicia serviço específico
```

### Manutenção
```bash
# Limpar ambiente
make clean           # Remove contêineres e volumes
make clean-logs      # Limpa logs
make clean-cache     # Limpa cache

# Verificar status
make status          # Status de todos os serviços
make status SERVICE=xxx # Status de serviço específico
```

### Desenvolvimento
```bash
# Testes
make test            # Executa todos os testes
make test-unit       # Executa testes unitários
make test-integration # Executa testes de integração

# Logs
make logs            # Ver todos os logs
make logs SERVICE=xxx # Ver logs específicos
```

### Diagnóstico
```bash
# Testes de conexão
make test-connection # Testa todas as conexões
make test-connection SERVICE=xxx # Testa conexão específica

# Monitoramento
make monitor         # Inicia monitoramento em tempo real
make stats           # Mostra estatísticas dos serviços
```