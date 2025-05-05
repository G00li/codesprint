from crewai import Agent, Task, Crew
from app.core.llm_client import OllamaLLM
from app.core.litellm_adapter import llm_adapter
import logging
import threading
import time
import concurrent.futures
import multiprocessing
import os

# Desativa a telemetria do CrewAI para evitar erros SSL
os.environ["CREWAI_TRACING"] = "false"

# Configure logger
logger = logging.getLogger("crewai_generator")

# instancia o LLM - usar diretamente o adaptador LiteLLM para evitar erros
llm = llm_adapter
logger.info("Usando adaptador LiteLLM como modelo de linguagem principal")
    
def create_agents(selected_areas: list[str]):
    """
    Versão simplificada e otimizada para criar agentes
    Reduz o número de agentes para melhorar performance
    """
    # Cria apenas dois agentes: um especialista principal e um gerente
    
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
    primary_specialist = Agent(
        role=primary_role,
        goal=primary_goal,
        backstory=primary_backstory,
        verbose=False,  # Reduzir saídas de log
        llm=llm
    )
    
    # Criar o gerente de projeto
    project_manager = Agent(
        role="Gerente de Projeto",
        goal="Organizar o plano de projeto",
        backstory="Gerente de projeto técnico com foco em entrega prática.",
        verbose=False,  # Reduzir saídas de log
        llm=llm
    )
    
    return [primary_specialist, project_manager]

def execute_task_directly(agent, task_description, expected_output):
    """
    Executa o agente com timeout reduzido e prompt simplificado
    """
    try:
        logger.info(f"Executando agente diretamente: {agent.role}")
        
        # Prompt simplificado para reduzir o tempo de processamento
        full_prompt = f"""
        {agent.role} deve responder de forma objetiva. Tarefa:
        {task_description}
        Resposta curta, sem explicações longas.
        """

        
        start_time = time.time()
        
        # Sempre usar o adaptador do LiteLLM
        agent_llm = llm_adapter
        
        # Adicionar timeout para a chamada
        from concurrent.futures import ThreadPoolExecutor, TimeoutError
        with ThreadPoolExecutor() as executor:
            # Iniciar chamada com timeout
            future = executor.submit(agent_llm.chat, [{"role": "user", "content": full_prompt}])
            
            try:
                # Aguardar no máximo 60 segundos
                result = future.result(timeout=90)
            except TimeoutError:
                logger.warning(f"Timeout ao processar {agent.role}, usando resposta padrão")
                # Resposta simples em caso de timeout
                return {
                    "agent": agent.role,
                    "result": f"Análise técnica simplificada para projeto utilizando as tecnologias solicitadas.",
                    "success": True
                }
        
        execution_time = time.time() - start_time
        logger.info(f"Execução direta de {agent.role} concluída em {execution_time:.2f} segundos")
        
        return {
            "agent": agent.role,
            "result": result,
            "success": True
        }
    except Exception as e:
        logger.error(f"Erro ao executar agente diretamente {agent.role}: {str(e)}")
        return {
            "agent": agent.role,
            "result": f"Análise técnica simplificada (erro: {str(e)[:50]}...)",
            "success": False
        }

def run_project_pipeline(area_selection: list[str], tech_stack: str, description: str):
    """
    Pipeline otimizado para gerar projeto mais rapidamente
    """
    pm_result = None
    try:
        logger.info(f"Iniciando geração do projeto com áreas: {area_selection}, tecnologias: {tech_stack}")
        
        # Validação básica dos inputs
        if not isinstance(description, str) or len(description) < 3:
            return {"error": "Descrição inválida ou muito curta"}
            
        # Preparar descrição simplificada
        full_description = f"""
        Projeto: {description}
        Tecnologias: {tech_stack}
        Áreas: {', '.join(area_selection)}
        """
        
        # Criar apenas dois agentes
        agents = create_agents(area_selection)
        logger.info(f"Agentes criados: {len(agents)}")
        
        # Separar os agentes
        specialist = agents[0]
        project_manager = agents[1]
        
        # Definir timeout geral
        overall_timeout = 90  # segundos para todo o processo
        start_time = time.time()
        
        # Executar especialista primeiro - com prompt simplificado
        specialist_task = f"""
        Analisar o seguinte projeto e fornecer recomendações técnicas:
        {full_description}
        
        Forneça a resposta no seguinte formato:
        
        # Análise Técnica
        [Sua análise técnica aqui]
        
        # Estrutura do Projeto
        [Estrutura de diretórios e arquivos]
        
        # Tecnologias Recomendadas
        [Lista de tecnologias]
        
        Seja conciso e específico.
        """
        
        specialist_result = execute_task_directly(specialist, specialist_task, "Análise técnica concisa")
        
        # Verificar timeout geral
        if time.time() - start_time > overall_timeout:
            # Se demorou demais, retornar resultado parcial
            return {
                "resumo": f"Análise básica com {tech_stack}",
                "tecnologias": tech_stack,
                "areas": area_selection,
                "estrutura": f"Estrutura padrão para projeto com {tech_stack}",
                "codigo": "",
                "recursos": []
            }
        
        # Executar gerente com resultado do especialista - prompt simplificado
        pm_task = f"""
        Com base na análise técnica abaixo:

        {specialist_result.get('result', 'N/A')}

        E na descrição do projeto:

        {full_description}

        Crie um plano de projeto no formato abaixo, **seguindo rigorosamente os títulos e a estrutura indicada**. 
        **Não adicione ou remova seções**. **Use exatamente os nomes de seção a seguir.**

        ---

        # Resumo do Projeto
        [Um parágrafo conciso descrevendo o projeto. Exemplo: "Este projeto visa desenvolver uma aplicação full-stack para gestão de tarefas usando React no frontend e FastAPI no backend."]

        # Estrutura do Projeto
        - /frontend
        - index.html
        - app.js
        - /backend
        - main.py
        - requirements.txt

        # Tecnologias Recomendadas
        - React
        - FastAPI
        - PostgreSQL

        # Próximos Passos
        - Criar repositório no GitHub
        - Configurar estrutura inicial
        - Definir endpoints principais da API

        ---

        **IMPORTANTE:**
        - Mantenha a ordem e os títulos exatamente como estão.
        - Use `N/A` se não souber a resposta para uma seção.
        - Não insira explicações extras fora das seções.
        """
        if time.time() - start_time > overall_timeout:
        # Se demorou demais, retornar resultado parcial
            return {
                "resumo": f"Análise básica com {tech_stack}",
                "tecnologias": tech_stack,
                "areas": area_selection,
                "estrutura": f"Estrutura padrão para projeto com {tech_stack}",
                "codigo": "",
                "recursos": []
            }

        pm_result = execute_task_directly(project_manager, pm_task, "Plano de projeto estruturado")

        # Verificar resultado e formatar resposta (simplificada)
        result_text = (
            pm_result.get('result') if pm_result and pm_result.get('result')
            else specialist_result.get('result', 'Não foi possível gerar resultado completo')
        )

        
        try:
            processed_result = {
                "resumo": extract_section(result_text, "Resumo do Projeto") or result_text[:250],
                "tecnologias": tech_stack,
                "areas": area_selection,
                "estrutura": extract_section(result_text, "Estrutura do Projeto") or f"Estrutura padrão para {tech_stack}",
                "codigo": "",  # Se quiser gerar código, adicione seção no prompt e extraia aqui
                "recursos": extract_resources(extract_section(result_text, "Próximos Passos"))
            }
                
            logger.info("Resultado processado com sucesso")
            return processed_result
        except Exception as e:
            logger.error(f"Erro ao processar resultado: {str(e)}")
            # Formato mínimo garantido
            return {
                "resumo": result_text[:250] + "...",
                "tecnologias": tech_stack,
                "areas": area_selection,
                "estrutura": f"Estrutura padrão para projeto {tech_stack}",
                "codigo": "",
                "recursos": []
            }
    except Exception as e:
        # Garantir que nunca quebra
        logger.error(f"Erro durante geração do projeto: {str(e)}")
        return {
            "resumo": f"Não foi possível processar completamente o projeto com {tech_stack}. Por favor, tente novamente.",
            "tecnologias": tech_stack, 
            "areas": area_selection,
            "estrutura": "",
            "codigo": "",
            "recursos": []
        }

def extract_section(text, section_name):
    """Extrai uma seção específica do resultado - versão simplificada"""
    try:
        if not text or not section_name in text.lower():
            return ""
            
        lines = text.split('\n')
        section_content = []
        found_section = False
        
        for line in lines:
            # Detectar início da seção
            if not found_section and section_name.lower() in line.lower():
                found_section = True
                continue
            
            # Se encontrou seção, adicionar conteúdo
            if found_section:
                # Parar quando encontrar outra seção
                if line.strip().startswith('#') or line.strip().startswith('##'):
                    break
                section_content.append(line)
        
        return '\n'.join(section_content).strip()
    except:
        return ""

def extract_resources(resources_text):
    """Converte recursos de texto para uma lista - simplificado"""
    if not resources_text:
        return []
    
    # Dividir por linhas e remover espaços
    lines = [line.strip() for line in resources_text.split('\n') if line.strip()]
    return lines
