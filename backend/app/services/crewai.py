import requests
from typing import List, Optional
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

    def gerar_projeto(self, areas: List[str], tecnologias: str, descricao: str, usar_exa: bool = False):
        logger.info(f"Iniciando geração de projeto com áreas: {areas}, tecnologias: {tecnologias}")
        
        payload = {
            "areas": areas,
            "tecnologias": tecnologias, 
            "descricao": descricao,
            "usar_exa": usar_exa
        }

        # Implementação de retry para a geração do projeto
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                logger.info(f"Tentativa {retry_count+1}/{max_retries}: Enviando request para {self.base_url}/gerar-projeto")
                
                # Usar session para melhor gerenciamento de conexão
                with requests.Session() as session:
                    session.headers.update({"Content-Type": "application/json"})
                    response = session.post(
                        f"{self.base_url}/gerar-projeto", 
                        data=json.dumps(payload), 
                        timeout=1200
                    )
                
                logger.info(f"Status code: {response.status_code}")
                
                if response.status_code == 200:
                    logger.info("Resposta recebida com sucesso do CrewAI")
                    try:
                        return response.json()
                    except Exception as e:
                        logger.error(f"Erro ao decodificar JSON da resposta: {str(e)}")
                        return {"error": "Erro ao processar resposta do CrewAI", "details": str(e)}
                else:
                    error_msg = f"CrewAI respondeu com status code: {response.status_code}"
                    logger.error(error_msg)
                    try:
                        error_details = response.json()
                        logger.error(f"Detalhes do erro: {error_details}")
                        error_info = {"error": "Erro ao comunicar com o CrewAi", "details": error_details}
                    except:
                        error_info = {"error": "Erro ao comunicar com o CrewAi", "details": error_msg}
                    
                    # Se for erro 500, tentamos novamente
                    if response.status_code == 500 and retry_count < max_retries - 1:
                        retry_count += 1
                        wait_time = 2 * retry_count
                        logger.info(f"Tentando novamente em {wait_time} segundos devido a erro 500...")
                        time.sleep(wait_time)
                        continue
                    
                    return error_info
            
            except requests.Timeout:
                error_msg = "Timeout na conexão com CrewAI (1200s)"
                logger.error(error_msg)
                
                # Tenta novamente se não for a última tentativa
                if retry_count < max_retries - 1:
                    retry_count += 1
                    wait_time = 2 * retry_count
                    logger.info(f"Tentando novamente em {wait_time} segundos após timeout...")
                    time.sleep(wait_time)
                    continue
                    
                return {"error": "Timeout ao comunicar com o CrewAi", "details": error_msg}
            
            except Exception as e:
                error_msg = f"Erro ao comunicar com o CrewAi: {str(e)}"
                logger.error(error_msg)
                
                # Tenta novamente se não for a última tentativa
                if retry_count < max_retries - 1:
                    retry_count += 1
                    wait_time = 2 * retry_count
                    logger.info(f"Tentando novamente em {wait_time} segundos após erro geral...")
                    time.sleep(wait_time)
                    continue
                    
                return {"error": "Erro ao comunicar com o CrewAi", "details": str(e)}
            
            # Se chegou aqui, é porque houve sucesso na requisição
            break
