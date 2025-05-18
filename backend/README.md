# Backend do CodeSprint

## Visão Geral
O backend do CodeSprint é responsável por gerenciar a comunicação entre o frontend e os serviços de IA, processando requisições e coordenando o fluxo de trabalho dos agentes.

## Funcionamento Técnico

### Processamento de Requisições
1. **Recebimento**
   - Endpoints REST assíncronos via FastAPI
   - Validação automática de payloads com Pydantic
   - Rate limiting e autenticação integrados

2. **Fluxo de Processamento**
   ```
   Requisição HTTP → FastAPI → Validação → Serviço CrewAI → Resposta
   ```

3. **Integração com CrewAI**
   - Gerenciamento de sessões de agentes
   - Coordenação de tarefas entre agentes
   - Processamento assíncrono de respostas

### Endpoints Principais

#### Health Check
- `GET /health`
  - Status básico do serviço
  - Verificação de conexões
  - Métricas de performance

- `GET /health/detailed`
  - Status detalhado dos componentes
  - Conexões com serviços externos
  - Métricas de uso de recursos

#### Logging e Monitoramento
- Logs estruturados em JSON
- Níveis de log configuráveis:
  - DEBUG: Detalhes de execução
  - INFO: Operações normais
  - WARNING: Situações não críticas
  - ERROR: Falhas e exceções

### Configuração do Ambiente

```bash
# Variáveis de Ambiente Necessárias
CREWAI_API_URL=http://crewai:8004
OLLAMA_API_URL=http://ollama:11434
REDIS_URL=redis://redis:6379
LOG_LEVEL=INFO
```

### Execução Local

```bash
# Instalação
poetry install

# Execução
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testes
```bash
# Execução dos testes
./run_tests.sh

# Testes específicos
poetry run pytest app/tests/ -v
```

## Documentação da API
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
