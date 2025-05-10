import requests
from typing import List, Optional, Dict
from dotenv import load_dotenv
import os
import time
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("crewai_service")

load_dotenv()

class CrewAiService: 
    def __init__(self):
        self.base_url = os.getenv("CREWAI_BASE_URL", "http://crewai:8004")
        logger.info(f"CrewAiService inicializado com base_url: {self.base_url}")
        # Testar a conexão durante a inicialização
        self._test_connection()

    def _test_connection(self):
        """Testa a conexão com o serviço CrewAI"""
        max_retries = 5
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                logger.info(f"Tentando conexão com CrewAI em {self.base_url}/health")
                response = requests.get(f"{self.base_url}/health", timeout=5)
                if response.status_code == 200:
                    logger.info(f"Conexão com CrewAI estabelecida com sucesso: {response.json()}")
                    return True
                else:
                    logger.warning(f"CrewAI respondeu com código de status inesperado: {response.status_code}")
            except Exception as e:
                logger.error(f"Erro ao conectar com CrewAI: {str(e)}")
            
            retry_count += 1
            if retry_count < max_retries:
                wait_time = 2 * retry_count
                logger.info(f"Tentando novamente em {wait_time} segundos... (tentativa {retry_count}/{max_retries})")
                time.sleep(wait_time)
        
        logger.warning("Aviso: Não foi possível estabelecer conexão com CrewAI durante a inicialização, mas continuando...")
        return False

    def gerar_projeto(self, areas: List[str], tecnologias: str, descricao: str, usar_exa: bool = False) -> Dict:
        try:
            response = requests.post(
                f"{self.base_url}/gerar-projeto",
                json={
                    "areas": areas,
                    "tecnologias": tecnologias,
                    "descricao": descricao,
                    "usar_exa": usar_exa
                },
                timeout=30
            )
            response.raise_for_status()
            return {
                "status": "success",
                "data": response.json()
            }
        except Exception as e:
            logger.error(f"Erro ao comunicar com o CrewAi: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    def check_health(self) -> Dict:
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            return {
                "status": response.json().get("status", "ok"),
                "success": True
            }
        except Exception as e:
            logger.error(f"Erro ao verificar saúde do CrewAI: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
