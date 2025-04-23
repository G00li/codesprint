from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama


llm = Ollama(
    model="llama3",
    base_url="http://host.docker.internal:11434")

def create_agents(selected_areas: list[str]):
    area_agents = []

    if "frontend" in selected_areas:
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

    if "backend" in selected_areas:
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

    if "devops" in selected_areas:
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

    return area_agents


def run_project_pipeline(area_selection: list[str], tech_stack: str, description: str):
    agents = create_agents(area_selection)

    tasks = []
    previous_output = description

    for agent in agents:
        task = Task(
            description=f"Baseado em: {previous_output}",
            expected_output="Resposta detalhada para o próximo agente",
            agent=agent
        )
        tasks.append(task)
        previous_output = task.expected_output  # simula encadeamento

    crew = Crew(
        tasks=tasks,
        agents=agents,
        verbose=True
    )

    return crew.kickoff()
