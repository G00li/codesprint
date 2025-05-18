# CrewAI - Sistema de Geração de Projetos

## Arquitetura do Sistema

O sistema CrewAI é uma implementação de um pipeline de geração de projetos utilizando uma arquitetura baseada em agentes (Agent-Based Architecture). O sistema utiliza o framework CrewAI para orquestrar múltiplos agentes especializados que trabalham em conjunto para gerar projetos técnicos completos.

### Componentes Principais

#### 1. Agentes Especializados

O sistema implementa dois tipos principais de agentes:

1. **Agente Especialista Técnico**
   - Responsável pela análise técnica inicial do projeto
   - Adapta sua especialidade com base nas áreas selecionadas (Web, Mobile, Desktop, API, IA/ML, Jogos)
   - Gera recomendações técnicas, estrutura de projeto e stack tecnológico
   - Utiliza o modelo de linguagem para análise contextual

2. **Agente Gerente de Projeto**
   - Processa a análise técnica do especialista
   - Gera um plano de projeto estruturado
   - Define próximos passos e recursos necessários
   - Coordena a documentação final do projeto

#### 2. Pipeline de Processamento

O pipeline segue uma sequência específica:

1. **Validação de Input**
   - Verificação da descrição do projeto
   - Validação das áreas e tecnologias selecionadas
   - Timeout global configurado para 700.000 segundos

2. **Geração de Análise Técnica**
   - O especialista analisa o projeto
   - Gera recomendações técnicas
   - Define estrutura de diretórios
   - Seleciona stack tecnológico

3. **Planejamento do Projeto**
   - O gerente processa a análise técnica
   - Cria plano de implementação
   - Define recursos e próximos passos
   - Estrutura a documentação final

4. **Processamento de Resultados**
   - Extração de seções específicas
   - Formatação da resposta final
   - Tratamento de erros e fallbacks

### Integração com LLM

O sistema utiliza o LiteLLM como adaptador para comunicação com o modelo de linguagem:

- **Modelo Base**: Ollama/LLama2:7b-chat
- **Configuração**:
  - Temperature: 0.3 (para respostas mais consistentes)
  - Timeout: 10.000 segundos por chamada
  - Retry Policy: 3 tentativas com backoff exponencial

### Estrutura de Resposta

A resposta final é estruturada em seções específicas:

```json
{
    "resumo": "Visão geral do projeto",
    "tecnologias": "Stack tecnológico recomendado",
    "areas": ["Áreas do projeto"],
    "estrutura": "Estrutura de diretórios",
    "recursos": ["Lista de recursos e referências"]
}
```

### Tratamento de Erros

O sistema implementa múltiplas camadas de tratamento de erros:

1. **Validação de Input**
   - Verificação de tipos e tamanhos
   - Sanitização de dados

2. **Retry Mechanism**
   - Tentativas automáticas em caso de falha
   - Fallback para prompts simplificados

3. **Timeout Handling**
   - Timeout global configurável
   - Timeouts individuais por chamada

4. **Error Recovery**
   - Respostas de fallback em caso de erro
   - Logging detalhado para debugging

### Performance e Otimizações

- **Concurrent Processing**: Utilização de ThreadPoolExecutor para execução paralela
- **Caching**: Reutilização de resultados intermediários
- **Prompt Engineering**: Otimização de prompts para respostas mais precisas
- **Resource Management**: Controle de memória e CPU

### Logging e Monitoramento

O sistema implementa logging em múltiplos níveis:

- **Application Logs**: Operações principais
- **Agent Logs**: Interações dos agentes
- **Error Logs**: Tratamento de exceções
- **Performance Logs**: Métricas de execução

### Dependências Principais

- crewai: ^0.114.0
- langchain: ^0.3.23
- ollama: ^0.4.8
- litellm: Para integração com LLMs
- FastAPI: Para API REST

### Configuração

O sistema requer as seguintes variáveis de ambiente:

```env
CREWAI_BASE_URL=http://crewai:8004
OLLAMA_HOST=http://ollama:11434
LITELLM_MODEL_NAME=ollama/llama2:7b-chat
LITELLM_API_BASE=http://ollama:11434
LITELLM_PROVIDER=ollama
``` 