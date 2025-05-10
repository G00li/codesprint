from fastapi import FastAPI, HTTPException
from typing import List, Optional, Dict
from pydantic import BaseModel
import requests
from app.services.crewai import CrewAiService
from app.services.network_diagnostics import debug_service_connectivity
import psycopg2
from psycopg2 import OperationalError
import os
import time
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

class TestResult(BaseModel):
    url: str
    success: bool
    status: Optional[int] = None
    statusText: Optional[str] = None
    responseTime: Optional[str] = None
    data: Optional[Dict] = None
    error: Optional[str] = None

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

@app.get("/health/db")
async def check_db_health_alt():
    """Endpoint alternativo para verificação de saúde do banco de dados"""
    return await check_db_health()

@app.get("/api/teste-rapido")
async def teste_rapido():
    """Endpoint para teste rápido de conectividade com todos os serviços"""
    results = []
    start_time = time.time()
    
    # Teste do banco de dados
    db_start = time.time()
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB", "codesprint"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "postgres"),
            host=os.getenv("POSTGRES_HOST", "db"),
            port=os.getenv("POSTGRES_PORT", "5432")
        )
        conn.close()
        db_time = time.time() - db_start
        results.append(TestResult(
            url="postgresql://db:5432/codesprint",
            success=True,
            status=200,
            statusText="OK",
            responseTime=f"{db_time:.2f}s",
            data={"message": "Database connection successful"}
        ))
    except Exception as e:
        results.append(TestResult(
            url="postgresql://db:5432/codesprint",
            success=False,
            error=str(e)
        ))

    # Teste do CrewAI
    crewai_url = os.getenv("CREWAI_BASE_URL", "http://crewai:8004")
    crewai_start = time.time()
    try:
        response = requests.get(f"{crewai_url}/health", timeout=5)
        crewai_time = time.time() - crewai_start
        results.append(TestResult(
            url=f"{crewai_url}/health",
            success=response.ok,
            status=response.status_code,
            statusText=response.reason,
            responseTime=f"{crewai_time:.2f}s",
            data=response.json() if response.ok else None
        ))
    except Exception as e:
        results.append(TestResult(
            url=f"{crewai_url}/health",
            success=False,
            error=str(e)
        ))

    # Teste do backend
    backend_start = time.time()
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        backend_time = time.time() - backend_start
        results.append(TestResult(
            url="http://localhost:8000/health",
            success=response.ok,
            status=response.status_code,
            statusText=response.reason,
            responseTime=f"{backend_time:.2f}s",
            data=response.json() if response.ok else None
        ))
    except Exception as e:
        results.append(TestResult(
            url="http://localhost:8000/health",
            success=False,
            error=str(e)
        ))

    total_time = time.time() - start_time
    
    return {
        "backendUrl": os.getenv("BACKEND_URL", "http://backend:8000"),
        "testTime": f"{total_time:.2f}s",
        "results": results
    }