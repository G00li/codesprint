from crewai import Agent
from app.core.litellm_adapter import llm_adapter
from .base_agent import execute_task_directly
import logging

logger = logging.getLogger("crewai_agents")

def create_specialist_agent(selected_areas: list[str]) -> Agent:
    """
    Cria o agente especialista com base nas áreas selecionadas
    """
    # Determinar o especialista principal com base nas áreas selecionadas
    primary_role = "Especialista Web"  # default
    primary_goal = "Definir arquitetura técnica completa"
    primary_backstory = "Especialista em desenvolvimento de software com conhecimento em múltiplas tecnologias."
    
    # Escolher especialidade principal com base na primeira área selecionada
    if "Web" in selected_areas or len(selected_areas) == 0:
        primary_role = "Especialista Web"
        primary_backstory = "Especialista em desenvolvimento web full-stack."
    elif "Mobile" in selected_areas:
        primary_role = "Especialista Mobile"
        primary_backstory = "Especialista em desenvolvimento mobile com React Native ou Flutter."
    elif "Desktop" in selected_areas:
        primary_role = "Especialista Desktop"
        primary_backstory = "Especialista em aplicações desktop."
    elif "API" in selected_areas:
        primary_role = "Especialista Backend/API"
        primary_backstory = "Especialista em desenvolvimento backend e APIs."
    elif "Inteligência Artificial" in selected_areas or "Machine Learning" in selected_areas:
        primary_role = "Especialista IA/ML"
        primary_backstory = "Especialista em IA/ML e implementações práticas."
    elif "Jogos" in selected_areas:
        primary_role = "Especialista em Jogos"
        primary_backstory = "Especialista em desenvolvimento de jogos."
    
    # Criar o especialista principal
    specialist = Agent(
        role=primary_role,
        goal=primary_goal,
        backstory=primary_backstory,
        verbose=False,  # Reduzir saídas de log
        llm=llm_adapter
    )
    
    return specialist

def execute_specialist_task(specialist: Agent, full_description: str) -> dict:
    """
    Executa a tarefa do especialista
    """
    specialist_task = f"""
    Analise o seguinte projeto e forneça recomendações técnicas detalhadas:

    {full_description}
    
    Forneça sua análise no seguinte formato:
    
    # Análise Técnica
    [Forneça uma análise técnica detalhada do projeto, considerando:
    - Arquitetura recomendada
    - Padrões de design a serem utilizados
    - Considerações de segurança
    - Escalabilidade e performance
    - Integrações necessárias
    - Requisitos de infraestrutura]
    
    # Estrutura do Projeto
    [Forneça uma estrutura detalhada de diretórios e arquivos, incluindo:
    - Organização de pastas
    - Arquivos principais
    - Configurações necessárias
    - Estrutura de testes
    - Documentação
    - Scripts de automação]
    
    # Tecnologias Recomendadas
    [Liste e justifique todas as tecnologias necessárias, incluindo:
    - Frameworks principais
    - Bibliotecas essenciais
    - Ferramentas de desenvolvimento
    - Banco de dados
    - Serviços externos
    - Ferramentas de CI/CD
    - Monitoramento e logging]
    
    # Considerações de Implementação
    [Forneça diretrizes importantes para implementação:
    - Ordem recomendada de desenvolvimento
    - Pontos de atenção
    - Boas práticas
    - Armadilhas comuns a evitar]
    
    Seja específico e forneça exemplos práticos quando possível.
    """
    
    logger.info("Executando tarefa do especialista...")
    specialist_result = execute_task_directly(specialist, specialist_task, "Análise técnica concisa")
    logger.info(f"Resultado do especialista: {specialist_result.get('result', '')[:200]}...")
    
    return specialist_result 