# Guia de Solução de Problemas - Comunicação Backend → CrewAI

Este guia ajudará a diagnosticar e resolver problemas de comunicação entre o serviço Backend e o serviço CrewAI no projeto CodeSprint.

## Problema Comum

Se você estiver vendo o erro:

```json
{ 
  "error": "Erro ao comunicar com o CrewAi", 
  "details": "500 Server Error: Internal Server Error for url: http://crewai:8004/gerar-projeto" 
}
```

Isso significa que o Backend consegue fazer uma conexão TCP com o CrewAI, mas está recebendo um erro HTTP 500 (erro interno do servidor) ao tentar utilizar o endpoint `/gerar-projeto`.

## Ferramentas de Diagnóstico

Fornecemos várias ferramentas para diagnóstico:

1. **Script de Teste Integrado**: Execute `./test_connection.sh` na raiz do projeto para realizar um diagnóstico completo.

2. **Endpoint de Diagnóstico de Rede**: Acesse `http://localhost:8000/diagnose-network` para obter um relatório detalhado sobre a conectividade entre os serviços.

3. **Teste de Conexão CrewAI**: Acesse `http://localhost:8000/diagnose-crewai` para um teste específico da conexão Backend → CrewAI.

4. **Script Python para Testes**: Execute `python backend/app/test_crewai_connection.py` para testes detalhados.

## Possíveis Causas e Soluções

### 1. Serviços não estão rodando

**Sintoma**: Erros de conexão recusada.

**Verificação**:
```bash
docker-compose ps
```

**Solução**: Inicie os serviços que não estão rodando:
```bash
docker-compose up -d
```

### 2. Problemas de Rede entre Contêineres

**Sintoma**: Erro "Connection refused" ou timeouts.

**Verificação**:
```bash
docker-compose exec backend ping crewai
docker-compose exec backend curl -v http://crewai:8004/health
```

**Solução**: Verifique se os serviços estão na mesma rede no `docker-compose.yml` e se as configurações de rede estão corretas.

### 3. Erro Interno no CrewAI (500)

**Sintoma**: Resposta HTTP 500 do CrewAI.

**Verificação**:
```bash
docker-compose logs crewai
```

**Solução**: 
- Verifique os logs do CrewAI para detalhes do erro
- Problemas comuns incluem:
  - Falha na comunicação com Ollama
  - Erros na formatação do payload
  - Problemas no processamento da requisição

### 4. Problemas com o Ollama (LLM)

**Sintoma**: CrewAI retorna erro relacionado ao LLM.

**Verificação**:
```bash
docker-compose logs ollama
docker-compose exec crewai curl -v http://ollama:11434/api/version
```

**Solução**:
- Verifique se o Ollama está rodando
- Verifique se o modelo necessário foi baixado:
```bash
docker-compose exec ollama ollama list
```
- Se necessário, puxe o modelo:
```bash
docker-compose exec ollama ollama pull llama3
```

### 5. Problemas de Timeout

**Sintoma**: Requests demoram muito e eventualmente falham com timeout.

**Solução**:
- Aumente os timeouts nas configurações:
  - Edite `backend/app/services/crewai.py` e aumente o valor de timeout
  - Considere ajustar configurações de timeout no Docker ou nos proxies, se aplicável

### 6. Variáveis de Ambiente Incorretas

**Sintoma**: Backend não consegue conectar ao endereço correto do CrewAI.

**Verificação**:
```bash
docker-compose exec backend env | grep CREW
```

**Solução**: Verifique se as variáveis de ambiente no arquivo `.env` e no `docker-compose.yml` estão configuradas corretamente:

```
CREWAI_HOST=crewai
CREWAI_PORT=8004
CREWAI_BASE_URL=http://crewai:8004
```

### 7. Problemas na Inicialização do Ollama

**Sintoma**: Container do Ollama fica preso em estado "waiting" ou "health: starting".

**Verificação**:
```bash
docker-compose ps
docker-compose logs ollama
```

**Solução**:
- Use o script de inicialização sequencial:
```bash
./start_services.sh
```
- Este script inicia o Ollama primeiro, verifica se está pronto, baixa o modelo necessário e só então inicia os outros serviços
- Se persistir o problema, tente usar um modelo menor (como llama3:8b em vez de llama3:latest)
- Verifique se há espaço suficiente em disco para o modelo (cerca de 5GB para llama3:8b)

## Reiniciando com Configurações Limpas

Se você continuar tendo problemas, pode ser útil reiniciar todo o ambiente:

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Logs Detalhados

Para visualizar logs mais detalhados em tempo real:

```bash
docker-compose logs -f crewai
docker-compose logs -f backend
docker-compose logs -f ollama
```

## Verificações de Saúde

Para verificar se cada serviço está saudável individualmente:

```bash
curl http://localhost:8000/health  # Backend
curl http://localhost:8004/health  # CrewAI
curl http://localhost:11434/api/version  # Ollama
```

## Contato para Suporte

Se após seguir estas etapas você ainda estiver enfrentando problemas, entre em contato com a equipe de desenvolvimento. 