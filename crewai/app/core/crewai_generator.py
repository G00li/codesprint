from app.core.llm_client import OllamaLLM
from app.core.litellm_adapter import llm_adapter
from app.core.agents import (
    create_specialist_agent,
    execute_specialist_task,
    create_project_manager_agent,
    execute_project_manager_task,
    extract_section,
    extract_resources
)
import logging
import time
import os
os.environ["CREWAI_TRACING"] = "false"

logger = logging.getLogger("crewai_generator")

llm = llm_adapter
logger.info("Usando adaptador LiteLLM como modelo de linguagem principal")

def run_project_pipeline(area_selection: list[str], tech_stack: str, description: str):
    """
    Pipeline otimizado para gerar projeto mais rapidamente
    """
    pm_result = None
    try:
        logger.info(f"Iniciando geração do projeto com áreas: {area_selection}, tecnologias: {tech_stack}")
        logger.info(f"Descrição do projeto: {description[:100]}...")
        
        if not isinstance(description, str) or len(description) < 3:
            logger.error("Descrição inválida ou muito curta")
            return {"error": "Descrição inválida ou muito curta"}
            
        full_description = f"""
        # Descrição do Projeto
        {description}

        # Tecnologias Especificadas
        {tech_stack}

        # Áreas Selecionadas
        {', '.join(area_selection)}

        Por favor, analise cuidadosamente os requisitos acima e forneça uma análise técnica detalhada.
        """
        
        specialist = create_specialist_agent(area_selection)
        project_manager = create_project_manager_agent()
        logger.info(f"Agentes criados: {[specialist.role, project_manager.role]}")
        
        overall_timeout = 700000
        start_time = time.time()
        
        logger.info("Executando tarefa do especialista...")
        specialist_result = execute_specialist_task(specialist, full_description)
        
        if time.time() - start_time > overall_timeout:
            logger.warning("Timeout atingido durante execução do especialista")
            return {
                "resumo": f"Análise básica com {tech_stack}",
                "tecnologias": tech_stack,
                "areas": area_selection,
                "estrutura": f"Estrutura padrão para projeto com {tech_stack}",
                "codigo": "",
                "recursos": []
            }
        
        if not specialist_result.get('success', False) or not specialist_result.get('result'):
            logger.warning("Resultado do especialista inválido, tentando novamente")
            specialist_result = execute_specialist_task(specialist, full_description)
        
        logger.info("Executando tarefa do gerente de projeto...")
        pm_result = execute_project_manager_task(project_manager, specialist_result, full_description)

        if not pm_result.get('success', False) or not pm_result.get('result'):
            logger.warning("Resultado do gerente inválido, tentando novamente")
            pm_result = execute_project_manager_task(project_manager, specialist_result, full_description)

        result_text = (
            pm_result.get('result') if pm_result and pm_result.get('result')
            else specialist_result.get('result', 'Não foi possível gerar resultado completo')
        )
        
        logger.info("Processando resultado final...")
        try:
            resumo = extract_section(result_text, "Resumo do Projeto")
            estrutura = extract_section(result_text, "Estrutura do Projeto")
            tecnologias = extract_section(result_text, "Tecnologias Recomendadas")
            proximos_passos = extract_section(result_text, "Próximos Passos")
            recursos = extract_resources(proximos_passos)
            
            logger.info(f"Seções extraídas:")
            logger.info(f"- Resumo: {resumo[:100]}...")
            logger.info(f"- Estrutura: {estrutura[:100]}...")
            logger.info(f"- Tecnologias: {tecnologias[:100]}...")
            logger.info(f"- Próximos Passos: {proximos_passos[:100]}...")
            logger.info(f"- Recursos: {len(recursos)} itens encontrados")
            
            processed_result = {
                "resumo": resumo or result_text[:250],
                "tecnologias": tecnologias or tech_stack,
                "areas": area_selection,
                "estrutura": estrutura or f"Estrutura padrão para {tech_stack}",
                "codigo": "",  # Removido pois não é mais usado
                "recursos": recursos
            }
                
            logger.info("Resultado processado com sucesso")
            return processed_result
        except Exception as e:
            logger.error(f"Erro ao processar resultado: {str(e)}")
            return {
                "resumo": result_text[:250] + "...",
                "tecnologias": tech_stack,
                "areas": area_selection,
                "estrutura": f"Estrutura padrão para projeto {tech_stack}",
                "codigo": "",
                "recursos": []
            }
    except Exception as e:
        logger.error(f"Erro durante geração do projeto: {str(e)}")
        return {
            "resumo": f"Não foi possível processar completamente o projeto com {tech_stack}. Por favor, tente novamente.",
            "tecnologias": tech_stack, 
            "areas": area_selection,
            "estrutura": "",
            "codigo": "",
            "recursos": []
        }
