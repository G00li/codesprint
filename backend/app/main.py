from fastapi import FastAPI 
from typing import List, Optional
from pydantic import BaseModel
import requests
from app.services.crewai import CrewAiService

app = FastAPI(
    app_name="CodeSpark",
    description="Uma plataforma de desenvolvimento de projetos guiada por IA"
    )


client = CrewAiService()

class ProjetoRequest(BaseModel):
    areas: List[str]
    tecnologias: str
    descricao: str
    usar_exa: Optional[bool] = False

@app.get("/health")
async def health_check():
    return {"status": "Tudo correto"}


@app.get("/")
async def root():
    return {"messagem": "Bem vindo ao backend do Codesprint"}


@app.post("/gerar-projeto")
async def gerar_projeto(req: ProjetoRequest):
    resultado = client.gerar_projeto(
        areas=req.areas,
        tecnologias=req.tecnologias,
        descricao=req.descricao,
        usar_exa=req.usar_exa or False 
        )
    return resultado