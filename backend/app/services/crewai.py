import requests
from typing import List, Optional
from dotenv import load_dotenv
import os

load_dotenv()

class CrewAiService: 
    def __init__(self):
        self.base_url = os.getenv("CREWAI_BASE_URL", "http://crewai:8004/")

    def gerar_projeto(self, areas: List[str], tecnologias: str, descricao: str, usar_exa: bool = False):
        payload = {
            "areas": areas,
            "tecnologias": tecnologias, 
            "descricao": descricao,
            "usar_exa": usar_exa
        }

        try:
            response = requests.post(f"{self.base_url}/gerar-projeto", json=payload)
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            return {"error": "Erro ao comunicar com o CrewAi", "details": str(e)}
