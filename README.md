# CodeSprint - Plataforma de Desenvolvimento de Projetos

## 🔍 Sobre o Projeto

O **CodeSprint** é uma plataforma inovadora que utiliza Inteligência Artificial para acelerar o desenvolvimento de novos projetos. Com uma interface intuitiva e responsiva, desenvolvedores podem especificar suas necessidades e obter um projeto base completo em questão de minutos.

## Ferramentas de Diagnóstico

O CodeSprint inclui diversas ferramentas para diagnóstico de problemas de conectividade entre os serviços.

### 1. Diagnóstico via Interface Web

Acesse as ferramentas de diagnóstico pela interface web:

- **Diagnóstico Automático**: http://localhost:3000/diagnostico
- **Diagnóstico Manual**: http://localhost:3000/diagnostico/manual

A ferramenta de diagnóstico manual permite testar a conectividade com qualquer endpoint, facilitando a identificação de problemas específicos.

### 2. Script de Diagnóstico

Execute o script de diagnóstico para verificar todos os serviços:

```bash
./check_services.sh
```

Este script verifica:
- Status dos contêineres Docker
- Conectividade com cada serviço
- Logs de serviços com problemas
- Diagnóstico de rede interno

### 3. Endpoints de Diagnóstico no Backend

O backend expõe endpoints específicos para diagnóstico:

- **Health Check**: http://localhost:8000/health
- **Diagnóstico CrewAI**: http://localhost:8000/diagnose-crewai
- **Diagnóstico de Rede**: http://localhost:8000/diagnose-network

### 4. Comandos Docker Úteis

Verifique o status e os logs dos serviços:

```bash
# Verificar status dos contêineres
docker-compose ps

# Ver logs do serviço backend
docker-compose logs backend

# Ver logs do serviço crewai
docker-compose logs crewai

# Ver logs do serviço ollama
docker-compose logs ollama

# Executar diagnóstico de rede interno
docker-compose exec backend python -m app.services.network_diagnostics
```

## Conectividade entre Contêineres

Ao usar o sistema em contêineres Docker, lembre-se que:

1. **Nomes de serviços vs Localhost**: 
   - Use `backend`, `crewai` e `ollama` como nomes de hosts dentro da rede Docker
   - Use `localhost` apenas quando acessar os serviços de fora dos contêineres

2. **Exemplo de URLs**:
   - Dentro dos contêineres: `http://backend:8000/health`
   - Acesso externo: `http://localhost:8000/health`

3. **Variáveis de ambiente**:
   - A variável `NEXT_PUBLIC_BACKEND_URL` define a URL do backend
   - O valor padrão nos contêineres é `http://backend:8000`
   - Ao rodar localmente, defina como `http://localhost:8000`

4. **Testando conectividade**:
   - Use a ferramenta de diagnóstico manual em http://localhost:3000/diagnostico/manual
   - Ao testar dentro dos contêineres, use os nomes dos serviços (`backend`, `crewai`, etc.)

## Resolução de Problemas Comuns

### Erro de Conexão Recusada (Connection Refused)

Isso geralmente indica que o serviço não está rodando ou não está acessível na porta configurada.

**Solução**: Verifique se o contêiner está em execução com `docker-compose ps` e analise os logs com `docker-compose logs [serviço]`.

### Erro 500 do CrewAI

Se o backend consegue se comunicar com o CrewAI, mas recebe um erro 500, geralmente é um problema com o modelo do Ollama.

**Solução**: Verifique se o Ollama está rodando e se o modelo especificado está disponível:

```bash
# Verificar status do Ollama
docker-compose logs ollama

# Verificar a comunicação Ollama-CrewAI
docker-compose exec backend python -m app.test_crewai_connection
```

### Timeout em Requisições

Timeouts podem ocorrer quando o Ollama está carregando o modelo pela primeira vez, o que pode levar alguns minutos.

**Solução**: Aguarde alguns minutos após iniciar os serviços e tente novamente. Verifique os logs do Ollama para acompanhar o progresso.

### Erro "Failed to fetch" no Frontend

Esse erro geralmente ocorre quando o frontend tenta acessar o backend usando `localhost` em vez do nome do serviço Docker.

**Solução**: 
1. Verifique se a configuração da URL do backend está correta no frontend
2. Use o diagnóstico manual para testar com a URL correta (`http://backend:8000/...`)
3. Reinicie o contêiner frontend após modificar variáveis de ambiente: `docker-compose restart frontend`

Desenvolvido com ❤️ pelo time CodeSprint
