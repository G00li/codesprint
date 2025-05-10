from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import requests
from app.services.crewai import CrewAiService
from app.services.network_diagnostics import debug_service_connectivity
import psycopg2
from psycopg2 import OperationalError
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    app_name="CodeSpark",
    description="Uma plataforma de desenvolvimento de projetos guiada por IA"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://frontend:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.get("/diagnose-crewai")
async def diagnose_crewai():
    """Endpoint para diagnóstico da conexão com o CrewAI"""
    import os
    crewai_url = os.getenv("CREWAI_BASE_URL", "http://crewai:8004")
    
    resultado = {
        "crewai_url": crewai_url,
        "connection_test": None,
        "error": None
    }
    
    try:
        # Testa conexão com timeout curto
        response = requests.get(f"{crewai_url}/health", timeout=5)
        resultado["connection_test"] = {
            "status_code": response.status_code,
            "response": response.json() if response.status_code == 200 else None
        }
    except Exception as e:
        resultado["error"] = str(e)
        
    return resultado

@app.get("/diagnose-network")
async def diagnose_network():
    """Endpoint para diagnóstico completo da rede entre os serviços"""
    results = debug_service_connectivity()
    return results

@app.get("/api/health/db")
async def check_db_health():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB", "codesprint"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "postgres"),
            host=os.getenv("POSTGRES_HOST", "db"),
            port=os.getenv("POSTGRES_PORT", "5432")
        )
        conn.close()
        return {"status": "healthy", "message": "Database connection successful"}
    except OperationalError as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")