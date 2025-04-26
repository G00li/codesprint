from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import logging
import traceback

from app.core.crewai_generator import run_project_pipeline
from app.service.exa_search import buscar_com_exa

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("crewai_api")

app = FastAPI(title="Gerador de Projetos com CrewAI")


class ProjetoRequest(BaseModel):
    areas: List[str]
    tecnologias: str
    descricao: str
    usar_exa: Optional[bool] = False


@app.get("/")
def read_root():
    return {"message": "Bem vindo ao CrewAI do CodeSprint"}

@app.get("/health")
def health_check():
    # Certifica que o serviço está realmente saudável
    try:
        # Aqui poderia verificar conexão com Ollama se necessário
        return {"status": "healthy", "service": "crewai"}
    except Exception as e:
        logger.error(f"Erro no health check: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Serviço não está saudável: {str(e)}"
        )

@app.post("/gerar-projeto")
def gerar_projeto(req: ProjetoRequest):
    try:
        logger.info(f"Recebido pedido para gerar projeto com áreas: {req.areas}, tecnologias: {req.tecnologias}")
        
        descricao_final = req.descricao

        if req.usar_exa:
            logger.info("🔍 Buscando insights com EXA.ai...")
            try:
                resultados_exa = buscar_com_exa(req.descricao)
                descricao_final += "\n\nResultados da EXA:\n" + "\n".join(resultados_exa)
            except Exception as e:
                logger.warning(f"Erro ao buscar com EXA: {str(e)}")
                # Continua mesmo com erro na EXA

        logger.info("Iniciando pipeline de geração do projeto...")
        resultado = run_project_pipeline(
            area_selection=req.areas,
            tech_stack=req.tecnologias,
            description=descricao_final
        )
        
        # Verifica se ocorreu um erro na geração
        if isinstance(resultado, dict) and "error" in resultado:
            logger.error(f"Erro detectado na resposta: {resultado['error']}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=resultado.get("erro_detalhes", "Erro interno no serviço")
            )
            
        logger.info("Projeto gerado com sucesso!")
        return {"resultado": resultado}
    except HTTPException:
        # Re-lança HTTPExceptions
        raise
    except Exception as e:
        error_traceback = traceback.format_exc()
        error_message = f"Erro na API durante geração do projeto: {str(e)}"
        logger.error(f"{error_message}\n{error_traceback}")
        
        # Retorna um erro 500 com informações úteis para diagnóstico
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
