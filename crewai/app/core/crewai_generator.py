from crewai import Agent, Task, Crew
from app.core.llm_client import OllamaLLM

# instancia o LLM
llm = OllamaLLM(
    model_name="llama3",
    temperature=0.3
    )

def create_agents(selected_areas: list[str]):
    """
    Cria agentes baseados nas áreas selecionadas pelo usuário.
    Suporta todas as áreas do frontend: Web, Mobile, Desktop, API,
    Inteligência Artificial, Machine Learning, Jogos, IoT, Blockchain, Segurança
    """
    area_agents = []
    
    # Mapeamento de áreas do frontend para as categorias internas se necessário
    mapped_areas = []
    
    # Adiciona categorias internas com base nas áreas selecionadas no frontend
    if "Web" in selected_areas:
        mapped_areas.append("frontend")
        mapped_areas.append("backend")
    
    if "Mobile" in selected_areas:
        mapped_areas.append("mobile")
    
    if "Desktop" in selected_areas:
        mapped_areas.append("desktop")
    
    if "API" in selected_areas:
        mapped_areas.append("backend")
        mapped_areas.append("api")
    
    if "Inteligência Artificial" in selected_areas or "Machine Learning" in selected_areas:
        mapped_areas.append("ai_ml")
    
    if "Jogos" in selected_areas:
        mapped_areas.append("games")
    
    if "IoT" in selected_areas:
        mapped_areas.append("iot")
    
    if "Blockchain" in selected_areas:
        mapped_areas.append("blockchain")
    
    if "Segurança" in selected_areas:
        mapped_areas.append("security")
    
    # Sempre inclui devops para uma estrutura de projeto completa
    mapped_areas.append("devops")
    
    # Remove duplicatas
    mapped_areas = list(set(mapped_areas))

    # Frontend Web Agents
    if "frontend" in mapped_areas:
        frontend_architect = Agent(
            role="Arquiteto de Frontend",
            goal="Definir uma arquitetura frontend escalável, moderna e desafiadora",
            backstory="""Você é um especialista em frontend com anos de experiência em 
            frameworks modernos como Next.js, React, Tailwind. Seu objetivo é propor 
            uma estrutura robusta e explicar como ela pode ser escalada.""",
            verbose=True,
            llm=llm
        )

        ui_ux_specialist = Agent(
            role="Especialista em UI/UX",
            goal="Projetar experiências visuais interativas e desafiadoras",
            backstory="""Você é um expert em interfaces bonitas, acessíveis e intuitivas. 
            Vai sugerir uso de animações com Framer Motion, temas escuros, responsividade 
            e boas práticas de design moderno.""",
            verbose=True,
            llm=llm
        )

        task_designer = Agent(
            role="Designer de Tarefas de Frontend",
            goal="Quebrar o projeto em passos claros de frontend",
            backstory="Você transforma qualquer proposta visual em um conjunto lógico e eficiente de tarefas.",
            verbose=True,
            llm=llm
        )

        area_agents += [frontend_architect, ui_ux_specialist, task_designer]

    # Mobile Agents
    if "mobile" in mapped_areas:
        mobile_architect = Agent(
            role="Arquiteto de Aplicações Móveis",
            goal="Definir uma arquitetura móvel robusta e multiplataforma",
            backstory="""Você é especialista em desenvolvimento móvel com React Native, Flutter, 
            Swift e Kotlin. Tem experiência em criar apps performáticos com boas práticas de UX.""",
            verbose=True,
            llm=llm
        )
        
        mobile_ux_specialist = Agent(
            role="Especialista em UX/UI Mobile",
            goal="Criar uma experiência móvel intuitiva e agradável",
            backstory="""Você é especialista em design de interfaces mobile-first, 
            com conhecimento profundo em padrões de interação em iOS e Android, 
            acessibilidade em dispositivos móveis e micro-interações.""",
            verbose=True,
            llm=llm
        )
        
        area_agents += [mobile_architect, mobile_ux_specialist]

    # Desktop Agents
    if "desktop" in mapped_areas:
        desktop_architect = Agent(
            role="Arquiteto de Aplicações Desktop",
            goal="Definir arquitetura para aplicações desktop eficientes",
            backstory="""Você é especialista em desenvolvimento desktop com Electron, 
            Qt, .NET ou outras tecnologias cross-platform. Tem experiência em 
            criar aplicações robustas, performáticas e com boa UX.""",
            verbose=True,
            llm=llm
        )
        
        area_agents += [desktop_architect]

    # Backend/API Agents
    if "backend" in mapped_areas:
        backend_engineer = Agent(
            role="Engenheiro Backend",
            goal="Propor uma arquitetura backend performática e segura",
            backstory="Você é um especialista em APIs rápidas e seguras com conhecimento em FastAPI, Django, etc.",
            verbose=True,
            llm=llm
        )

        security_advisor = Agent(
            role="Especialista em Segurança",
            goal="Garantir que o backend esteja protegido contra falhas comuns",
            backstory="Você revisa práticas de segurança, autenticação, rate limiting, etc.",
            verbose=True,
            llm=llm
        )

        backend_tasker = Agent(
            role="Designer de Tarefas de Backend",
            goal="Quebrar o backend em módulos/tarefas para o usuário desenvolver",
            backstory="Você organiza endpoints, banco de dados e lógica em tarefas compreensíveis.",
            verbose=True,
            llm=llm
        )

        area_agents += [backend_engineer, security_advisor, backend_tasker]

    # API Especialistas (quando API é explicitamente escolhida)
    if "api" in mapped_areas:
        api_specialist = Agent(
            role="Especialista em APIs",
            goal="Definir padrões REST/GraphQL e estruturar documentação",
            backstory="""Você é um expert em design de APIs com foco em consistência,
            segurança e documentação clara. Conhece OpenAPI, Swagger e ferramentas de teste.""",
            verbose=True,
            llm=llm
        )
        
        area_agents += [api_specialist]

    # AI/ML Agents
    if "ai_ml" in mapped_areas:
        ai_ml_architect = Agent(
            role="Arquiteto de IA/ML",
            goal="Projetar sistemas de machine learning escaláveis e responsáveis",
            backstory="""Você é um especialista em IA e ML com experiência em frameworks como 
            TensorFlow, PyTorch, Scikit-learn. Você sabe como estruturar projetos de dados, 
            definir pipelines de treinamento e implantar modelos.""",
            verbose=True,
            llm=llm
        )
        
        data_engineer = Agent(
            role="Engenheiro de Dados",
            goal="Estruturar pipelines de dados eficientes para modelos de ML",
            backstory="""Você é especialista em ETL, data lakes, processamento de dados em larga escala, 
            e integrações com diversas fontes de dados. Seu foco é garantir dados de qualidade 
            para os projetos de ML.""",
            verbose=True,
            llm=llm
        )
        
        ml_ops_engineer = Agent(
            role="MLOps Engenheiro",
            goal="Garantir implantação, monitoramento e manutenção de modelos ML em produção",
            backstory="""Você é especialista em implementar boas práticas de MLOps, incluindo 
            versionamento de modelos, monitoramento de desempenho, detecção de drift e escalabilidade.""",
            verbose=True,
            llm=llm
        )
        
        area_agents += [ai_ml_architect, data_engineer, ml_ops_engineer]

    # Game Development Agents
    if "games" in mapped_areas:
        game_architect = Agent(
            role="Arquiteto de Jogos",
            goal="Definir arquitetura e mecânicas para desenvolvimento de jogos",
            backstory="""Você é um especialista em desenvolvimento de jogos com experiência em engines
            como Unity e Unreal. Conhece padrões de arquitetura para jogos, sistemas de componentes,
            e otimização de performance em jogos.""",
            verbose=True,
            llm=llm
        )
        
        game_designer = Agent(
            role="Game Designer",
            goal="Criar mecânicas de jogos envolventes e equilibradas",
            backstory="""Você é especialista em design de jogos, balanceamento, sistemas de progressão,
            e criação de experiências envolventes para os jogadores. Você tem habilidade para
            documentar regras e mecânicas de forma clara.""",
            verbose=True,
            llm=llm
        )
        
        area_agents += [game_architect, game_designer]

    # IoT Agents
    if "iot" in mapped_areas:
        iot_architect = Agent(
            role="Arquiteto de IoT",
            goal="Projetar sistemas IoT seguros, eficientes e escaláveis",
            backstory="""Você é um especialista em arquiteturas de IoT, desde dispositivos embarcados
            até sistemas na nuvem. Conhece protocolos como MQTT, CoAP, segurança em IoT e
            estratégias para lidar com conectividade intermitente e eficiência energética.""",
            verbose=True,
            llm=llm
        )
        
        embedded_systems_engineer = Agent(
            role="Engenheiro de Sistemas Embarcados",
            goal="Projetar firmware e software para dispositivos IoT",
            backstory="""Você é especialista em desenvolvimento para sistemas embarcados,
            microcontroladores e hardware IoT. Conhece linguagens como C/C++, Python para
            sistemas embarcados e práticas de otimização.""",
            verbose=True,
            llm=llm
        )
        
        area_agents += [iot_architect, embedded_systems_engineer]

    # Blockchain Agents
    if "blockchain" in mapped_areas:
        blockchain_architect = Agent(
            role="Arquiteto Blockchain",
            goal="Projetar sistemas descentralizados seguros e eficientes",
            backstory="""Você é especialista em blockchain, smart contracts e sistemas descentralizados.
            Conhece plataformas como Ethereum, Solana, e conceitos como DeFi, NFTs, DAO, além de
            padrões de segurança em contratos inteligentes.""",
            verbose=True,
            llm=llm
        )
        
        smart_contracts_developer = Agent(
            role="Desenvolvedor de Smart Contracts",
            goal="Projetar contratos inteligentes seguros e eficientes",
            backstory="""Você é especialista em desenvolver smart contracts usando Solidity ou outras
            linguagens blockchain. Conhece padrões, boas práticas de segurança, técnicas de otimização
            de gas e auditorias de código.""",
            verbose=True,
            llm=llm
        )
        
        area_agents += [blockchain_architect, smart_contracts_developer]

    # Security Agents
    if "security" in mapped_areas:
        security_architect = Agent(
            role="Arquiteto de Segurança",
            goal="Definir uma estratégia de segurança abrangente para o projeto",
            backstory="""Você é um especialista em segurança de aplicações com anos de experiência
            em análise de ameaças, proteção de dados, e implementação de controles de segurança.
            Conhece padrões como OWASP Top 10, SAST/DAST, e gestão de vulnerabilidades.""",
            verbose=True,
            llm=llm
        )
        
        penetration_tester = Agent(
            role="Pentester",
            goal="Identificar vulnerabilidades potenciais e recomendar mitigações",
            backstory="""Você é especialista em testes de penetração e encontrar falhas de segurança
            em aplicações. Tem experiência em identificar vulnerabilidades em diferentes camadas
            de aplicações e propor contramedidas eficazes.""",
            verbose=True,
            llm=llm
        )
        
        area_agents += [security_architect, penetration_tester]

    # DevOps Agents (sempre incluídos para uma estrutura completa)
    if "devops" in mapped_areas:
        infra_engineer = Agent(
            role="Engenheiro DevOps",
            goal="Propor infraestrutura para CI/CD, Docker, monitoramento e boas práticas",
            backstory="Você é focado em automatizar, escalar e manter a infraestrutura de projetos modernos.",
            verbose=True,
            llm=llm
        )

        infra_tasker = Agent(
            role="Designer de Tarefas DevOps",
            goal="Transformar sugestões em tarefas de setup de ambientes e deploy",
            backstory="Você cria um roadmap técnico de infraestrutura, deploy e monitoramento.",
            verbose=True,
            llm=llm
        )

        area_agents += [infra_engineer, infra_tasker]

    # Se não houver agentes específicos, adicione um agente genérico
    if not area_agents:
        generic_architect = Agent(
            role="Arquiteto de Solução",
            goal="Projetar uma solução completa baseada nas necessidades do usuário",
            backstory="""Você é um arquiteto versátil com experiência em múltiplas tecnologias.
            Seu objetivo é criar um plano de projeto abrangente que possa ser implementado
            por desenvolvedores com diferentes níveis de experiência.""",
            verbose=True,
            llm=llm
        )
        
        area_agents = [generic_architect]

    # Adicione um agente final para integração
    project_manager = Agent(
        role="Gerente de Projeto",
        goal="Integrar todas as recomendações em um plano de projeto coeso",
        backstory="""Você é um gerente de projeto experiente que sabe como integrar diferentes 
        componentes técnicos em um roadmap unificado. Foca em criar um plano claro, 
        priorizando tarefas e estabelecendo dependências.""",
        verbose=True,
        llm=llm
    )
    
    area_agents.append(project_manager)

    return area_agents


def run_project_pipeline(area_selection: list[str], tech_stack: str, description: str):
    # Adiciona o tech stack à descrição para melhor contextualização
    full_description = f"""
    Descrição do Projeto: {description}
    
    Tecnologias Desejadas: {tech_stack}
    
    Áreas Selecionadas: {', '.join(area_selection)}
    """
    
    agents = create_agents(area_selection)

    tasks = []
    previous_output = full_description

    for i, agent in enumerate(agents):
        # O primeiro agente recebe a descrição completa
        if i == 0:
            task_description = f"""
            Baseado na descrição do projeto:
            {full_description}
            
            Forneça sua análise e recomendações específicas para sua área de expertise.
            """
        # Agentes intermediários recebem a saída do agente anterior
        else:
            task_description = f"""
            Baseado na análise anterior:
            {previous_output}
            
            E na descrição original do projeto:
            {full_description}
            
            Forneça sua análise e recomendações específicas para sua área de expertise.
            """
        
        # O último agente (project manager) recebe instruções para integrar tudo
        if i == len(agents) - 1:
            task_description = f"""
            Baseado em todas as análises anteriores e na descrição original:
            {full_description}
            
            Crie um plano de projeto integrado e coeso que inclua:
            1. Resumo executivo do projeto
            2. Arquitetura proposta
            3. Estrutura de diretórios recomendada
            4. Lista de tecnologias e bibliotecas
            5. Roadmap de desenvolvimento com tarefas priorizadas
            6. Exemplos de código para partes cruciais
            7. Recursos e referências para o desenvolvedor
            
            Formate as seções com clareza usando Markdown.
            """
            
            expected_output = """
            # Plano de Projeto Completo
            
            ## Resumo Executivo
            [resumo do projeto]
            
            ## Arquitetura Proposta
            [diagrama textual da arquitetura]
            
            ## Estrutura de Diretórios
            ```
            [estrutura de pastas e arquivos]
            ```
            
            ## Tecnologias e Bibliotecas
            [lista detalhada]
            
            ## Roadmap de Desenvolvimento
            [lista de tarefas com prioridades]
            
            ## Exemplos de Código
            ```
            [exemplos relevantes]
            ```
            
            ## Recursos e Referências
            [links e recursos úteis]
            """
        else:
            expected_output = "Análise detalhada e recomendações específicas para a próxima etapa"

        task = Task(
            description=task_description,
            expected_output=expected_output,
            agent=agent
        )
        tasks.append(task)
        previous_output = task.expected_output  # simula encadeamento

    crew = Crew(
        tasks=tasks,
        agents=agents,
        verbose=True
    )

    result = crew.kickoff()
    
    # Processa o resultado para um formato mais estruturado
    processed_result = {
        "resumo": extract_section(result, "Resumo Executivo"),
        "tecnologias": tech_stack,
        "areas": area_selection,
        "estrutura": extract_section(result, "Estrutura de Diretórios"),
        "codigo": extract_section(result, "Exemplos de Código"),
        "recursos": extract_resources(extract_section(result, "Recursos e Referências"))
    }
    
    return processed_result

def extract_section(text, section_name):
    """Extrai uma seção específica do resultado"""
    try:
        if not section_name in text:
            return ""
            
        start_marker = f"## {section_name}"
        start_index = text.find(start_marker)
        
        if start_index == -1:
            return ""
            
        start_index = start_index + len(start_marker)
        
        # Encontra a próxima seção (se houver)
        next_section = text.find("##", start_index)
        
        if next_section == -1:
            section_content = text[start_index:].strip()
        else:
            section_content = text[start_index:next_section].strip()
            
        return section_content
    except:
        return "Não foi possível extrair esta seção."

def extract_resources(resources_text):
    """Converte recursos de texto para uma lista"""
    if not resources_text:
        return []
        
    # Remove marcadores de lista Markdown e divide por linhas
    lines = resources_text.strip().split("\n")
    resources = []
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            # Remove marcadores de lista Markdown como "- " ou "* "
            if line.startswith("- ") or line.startswith("* "):
                line = line[2:]
            resources.append(line.strip())
            
    return resources
