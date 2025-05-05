# CodeSprint - Plataforma de Desenvolvimento de Projetos

## 🔍 Sobre o Projeto

O **CodeSprint** é uma plataforma inovadora que utiliza Inteligência Artificial para acelerar o desenvolvimento de novos projetos. Com uma interface intuitiva e responsiva, desenvolvedores podem especificar suas necessidades e obter um projeto base completo em questão de minutos.

## 🛠️ Arquitetura do Sistema

O CodeSprint é composto por vários serviços interconectados:

- **Frontend**: Interface de usuário React/Next.js (porta 3000)
- **Backend**: API REST em Python/FastAPI (porta 8000)
- **CrewAI**: Serviço de orquestração de IA (porta 8004)
- **Ollama**: Serviço de execução de modelos de linguagem (porta 11434)
- **Redis**: Cache e filas de tarefas (porta 6379)

Os serviços se comunicam entre si através de uma rede Docker dedicada.

## 📋 Requisitos

- Docker e Docker Compose
- 8GB+ de RAM disponível
- 20GB+ de espaço em disco
- Conexão estável com a internet (para download inicial dos modelos)

## 🚀 Instalação e Execução

### Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/codesprint.git
cd codesprint

# Inicie os serviços (com download automático do modelo LLM)
./start_services.sh
```

### Usando Makefile

```bash
# Inicia todos os contêineres
make up

# Para todos os contêineres
make down

# Reinicia todos os contêineres
make restart

# Limpa ambiente (remove contêineres e volumes)
make clean
```

### Verificação da Instalação

```bash
# Verifica o status dos serviços
./check_services.sh
```

## 🔧 Ferramentas de Diagnóstico

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

### 4. Script de Correção de Conectividade

Para corrigir problemas comuns de conectividade:

```bash
./fix_connection.sh
```

Este script detecta e corrige automaticamente problemas de configuração entre os serviços.

### 5. Comandos Docker Úteis

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

## 🔄 Conectividade entre Contêineres

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

## 🚨 Resolução de Problemas Comuns

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

## 📊 Monitoramento e Desempenho

### Verificação de Recursos

Para monitorar o uso de recursos pelos contêineres:

```bash
docker stats
```

### Verificação de Modelos Ollama

Para verificar os modelos disponíveis no Ollama:

```bash
docker exec -it codesprint-ollama-1 ollama list
```

### Download Manual de Modelos

Para baixar manualmente o modelo LLM usado pelo sistema:

```bash
docker exec -it codesprint-ollama-1 ollama pull llama3:8b
```

## 📚 Documentação Adicional

Consulte estes arquivos para informações específicas:

- `CHANGELOG.md`: Histórico de alterações e melhorias no sistema
- `backend/README_TROUBLESHOOTING.md`: Guia detalhado de solução de problemas

## 🧪 Desenvolvimento e Contribuição

Para contribuir com o projeto:

1. Escolha uma issue aberta ou crie uma nova
2. Faça fork do repositório
3. Crie um branch para sua feature (`git checkout -b feature/nome-da-feature`)
4. Implemente suas alterações
5. Execute os testes necessários
6. Faça commit das alterações (`git commit -am 'Adiciona nova feature'`)
7. Faça push para o branch (`git push origin feature/nome-da-feature`)
8. Abra um Pull Request

## 📄 Licença

Desenvolvido com ❤️ pelo time CodeSprint

[Incluir informações de licença se aplicável]