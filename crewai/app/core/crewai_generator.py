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

def run_project_pipeline(area_selection: list[str], tech_stack: str, description: str):
    """
    Pipeline otimizado para gerar projeto mais rapidamente
    """
    pm_result = None
    try:
        logger.info(f"Iniciando geração do projeto com áreas: {area_selection}, tecnologias: {tech_stack}")
        logger.info(f"Descrição do projeto: {description[:100]}...")  # Log dos primeiros 100 caracteres
        
        # Validação básica dos inputs
        if not isinstance(description, str) or len(description) < 3:
            logger.error("Descrição inválida ou muito curta")
            return {"error": "Descrição inválida ou muito curta"}
            
        # Preparar descrição simplificada
        full_description = f"""
        Projeto: {description}
        Tecnologias: {tech_stack}
        Áreas: {', '.join(area_selection)}
        """
        
        # Criar apenas dois agentes
        agents = create_agents(area_selection)
        logger.info(f"Agentes criados: {[agent.role for agent in agents]}")
        
        # Separar os agentes
        specialist = agents[0]
        project_manager = agents[1]
        
        # Definir timeout geral
        overall_timeout = 7000  # segundos para todo o processo
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
        
        logger.info("Executando tarefa do especialista...")
        specialist_result = execute_task_directly(specialist, specialist_task, "Análise técnica concisa")
        logger.info(f"Resultado do especialista: {specialist_result.get('result', '')[:200]}...")  # Log dos primeiros 200 caracteres
        
        # Verificar timeout geral
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
        
        # Verificar se o resultado do especialista é válido
        if not specialist_result.get('success', False) or not specialist_result.get('result'):
            logger.warning("Resultado do especialista inválido, tentando novamente")
            specialist_result = execute_task_directly(specialist, specialist_task, "Análise técnica concisa")
        
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
        logger.info(f"Resultado do gerente: {pm_result.get('result', '')[:200]}...")  # Log dos primeiros 200 caracteres

        # Verificar se o resultado do gerente é válido
        if not pm_result.get('success', False) or not pm_result.get('result'):
            logger.warning("Resultado do gerente inválido, tentando novamente")
            pm_result = execute_task_directly(project_manager, pm_task, "Plano de projeto estruturado")

        # Verificar resultado e formatar resposta (simplificada)
        result_text = (
            pm_result.get('result') if pm_result and pm_result.get('result')
            else specialist_result.get('result', 'Não foi possível gerar resultado completo')
        )
        
        logger.info("Processando resultado final...")
        try:
            # Extrair cada seção e logar
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
    """Extrai uma seção específica do resultado - versão melhorada"""
    try:
        if not text or not section_name:
            return ""
            
        # Normaliza o texto e o nome da seção para comparação
        text_lower = text.lower()
        section_name_lower = section_name.lower()
        
        # Procura pelo título da seção
        section_start = text_lower.find(f"# {section_name_lower}")
        if section_start == -1:
            # Tenta encontrar sem o #
            section_start = text_lower.find(section_name_lower)
            if section_start == -1:
                return ""
        
        # Encontra o início do conteúdo (após o título)
        content_start = text.find('\n', section_start)
        if content_start == -1:
            return ""
        content_start += 1  # Pula a quebra de linha
        
        # Encontra o próximo título de seção
        next_section = text.find('#', content_start)
        if next_section == -1:
            # Se não houver próxima seção, pega todo o conteúdo até o final
            return text[content_start:].strip()
        
        # Retorna o conteúdo entre o título atual e o próximo título
        return text[content_start:next_section].strip()
    except Exception as e:
        logger.error(f"Erro ao extrair seção {section_name}: {str(e)}")
        return ""

def extract_resources(resources_text):
    """Converte recursos de texto para uma lista - versão melhorada"""
    if not resources_text:
        return []
    
    # Dividir por linhas e remover espaços
    lines = [line.strip() for line in resources_text.split('\n') if line.strip()]
    
    # Filtrar linhas que começam com - ou *
    resources = []
    for line in lines:
        if line.startswith('- ') or line.startswith('* '):
            # Remove o marcador e espaços extras
            resource = line[2:].strip()
            if resource:
                resources.append(resource)
        elif line.startswith('## '):
            # Adiciona o título da subseção como um recurso
            resources.append(line[3:].strip())
    
    return resources
