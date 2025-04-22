from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

from app.core.crewai_generator import run_project_pipeline
from app.service.exa_search import buscar_com_exa

app = FastAPI(title="Gerador de Projetos com CrewAI")


class ProjetoRequest(BaseModel):
    areas: List[str]
    tecnologias: str
    descricao: str
    usar_exa: Optional[bool] = False


@app.get("/")
def read_root():
    return {"message": "Bem vindo ao CrewAI do CodeSprint"}

@app.post("/gerar-projeto")
def gerar_projeto(req: ProjetoRequest):
    descricao_final = req.descricao

    if req.usar_exa:
        print("🔍 Buscando insights com EXA.ai...")
        resultados_exa = buscar_com_exa(req.descricao)
        descricao_final += "\n\nResultados da EXA:\n" + "\n".join(resultados_exa)

    resultado = run_project_pipeline(
        area_selection=req.areas,
        tech_stack=req.tecnologias,
        description=descricao_final
    )

    return {"resultado": resultado}
