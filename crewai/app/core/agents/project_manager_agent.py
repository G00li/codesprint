from crewai import Agent
from app.core.litellm_adapter import llm_adapter
from .base_agent import execute_task_directly
import logging

logger = logging.getLogger("crewai_agents")

def create_project_manager_agent() -> Agent:
    """
    Cria o agente gerente de projeto
    """
    project_manager = Agent(
        role="Gerente de Projeto",
        goal="Organizar o plano de projeto",
        backstory="Gerente de projeto técnico com foco em entrega prática.",
        verbose=False,  # Reduzir saídas de log
        llm=llm_adapter
    )
    
    return project_manager

def execute_project_manager_task(project_manager: Agent, specialist_result: dict, full_description: str) -> dict:
    """
    Executa a tarefa do gerente de projeto
    """
    pm_task = f"""
    Com base na análise técnica abaixo:

    {specialist_result.get('result', 'N/A')}

    E na descrição do projeto:

    {full_description}

    Crie um plano de projeto no formato abaixo, **seguindo rigorosamente os títulos e a estrutura indicada**. 
    **Não adicione ou remova seções**. **Use exatamente os nomes de seção a seguir.**

    ---

    # Resumo do Projeto
    [Forneça um resumo detalhado do projeto incluindo:
    - Visão geral completa do projeto e seu propósito
    - Principais funcionalidades e recursos
    - Público-alvo e necessidades atendidas
    - Benefícios e diferenciais do projeto
    - Considerações técnicas importantes
    Use parágrafos bem estruturados e seja específico.]

    # Estrutura do Projeto
    [Forneça a estrutura detalhada de diretórios e arquivos, incluindo:
    - Organização de pastas e arquivos
    - Arquivos de configuração necessários
    - Arquivos de dependências
    - Arquivos de ambiente
    - Estrutura de testes]

    # Tecnologias Recomendadas
    [Liste todas as tecnologias necessárias, incluindo:
    - Frameworks principais
    - Bibliotecas essenciais
    - Ferramentas de desenvolvimento
    - Banco de dados
    - Serviços externos]

    # Próximos Passos
    [Forneça um guia detalhado de implementação, incluindo:

    ## Configuração e Setup
    - Passos para configurar o ambiente de desenvolvimento
    - Instalação de dependências
    - Configuração de variáveis de ambiente
    - Setup inicial do projeto

    ## Desenvolvimento
    - Ordem recomendada de implementação das funcionalidades
    - Pontos de atenção durante o desenvolvimento
    - Estratégias de teste
    - Documentação necessária

    ## Dicas e Boas Práticas
    - Padrões de código recomendados
    - Estratégias de otimização
    - Armadilhas comuns a evitar
    - Dicas de performance

    ## Recursos de Aprendizado
    - Documentação oficial relevante
    - Tutoriais recomendados
    - Ferramentas úteis
    - Comunidades de suporte

    ## Conselhos para Produção
    - Estratégias de deploy
    - Monitoramento e logging
    - Manutenção e atualizações
    - Escalabilidade e performance
    - Segurança e backup
    - CI/CD e automação]

    Seja específico e forneça exemplos práticos quando possível.
    """
    
    logger.info("Executando tarefa do gerente de projeto...")
    pm_result = execute_task_directly(project_manager, pm_task, "Plano de projeto estruturado")
    logger.info(f"Resultado do gerente: {pm_result.get('result', '')[:200]}...")
    
    return pm_result 