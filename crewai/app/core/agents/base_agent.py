from crewai import Agent
from app.core.litellm_adapter import llm_adapter
import logging
import time

logger = logging.getLogger("crewai_agents")

def execute_task_directly(agent, task_description, expected_output):
    """
    Executa o agente com timeout aumentado e prompt simplificado
    """
    try:
        logger.info(f"Executando agente diretamente: {agent.role}")
        
        # Prompt simplificado para reduzir o tempo de processamento
        full_prompt = f"""
        {agent.role} deve responder de forma objetiva e relevante. Tarefa:
        {task_description}
        Resposta deve ser completa e específica para o projeto.
        """
        
        start_time = time.time()
        
        # Sempre usar o adaptador do LiteLLM
        agent_llm = llm_adapter
        
        # Adicionar timeout para a chamada
        from concurrent.futures import ThreadPoolExecutor, TimeoutError
        with ThreadPoolExecutor() as executor:
            # Iniciar chamada com timeout aumentado para 1000 segundos
            future = executor.submit(agent_llm.chat, [{"role": "user", "content": full_prompt}])
            
            try:
                # Aguardar no máximo 1000 segundos
                result = future.result(timeout=10000)
            except TimeoutError:
                logger.warning(f"Timeout ao processar {agent.role}, tentando novamente com prompt mais curto")
                # Tentar novamente com prompt mais curto
                retry_prompt = f"""
                {agent.role}, forneça uma resposta concisa para:
                {task_description}
                """
                try:
                    future = executor.submit(agent_llm.chat, [{"role": "user", "content": retry_prompt}])
                    result = future.result(timeout=500)  # Timeout menor para a segunda tentativa
                except TimeoutError:
                    logger.error(f"Timeout na segunda tentativa para {agent.role}")
                    return {
                        "agent": agent.role,
                        "result": f"Análise técnica simplificada para projeto utilizando as tecnologias solicitadas.",
                        "success": False
                    }
        
        execution_time = time.time() - start_time
        logger.info(f"Execução direta de {agent.role} concluída em {execution_time:.2f} segundos")
        
        # Verificar se a resposta é muito curta ou vazia
        if not result or len(result) < 50:
            logger.warning(f"Resposta muito curta de {agent.role}, tentando novamente")
            return execute_task_directly(agent, task_description, expected_output)
        
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