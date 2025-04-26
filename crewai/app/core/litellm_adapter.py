import os
import time
import logging
from typing import Dict, List, Any, Optional

# Configuração do LiteLLM para usar nossa instância de Ollama com tolerância a falhas
class CustomLiteLLM:
    def __init__(self):
        # Configurar variáveis de ambiente para o LiteLLM
        os.environ["LITELLM_MODEL_NAME"] = "llama3"
        os.environ["LITELLM_API_BASE"] = "http://ollama:11434"  # Usar o nome do serviço do Docker Compose
        os.environ["LITELLM_PROVIDER"] = "ollama"
        os.environ["LITELLM_API_KEY"] = "dummy"
        
        # Imprimir configuração para debug
        print(f"Configurando LiteLLM com:")
        print(f"  - Model: {os.environ['LITELLM_MODEL_NAME']}")
        print(f"  - API Base: {os.environ['LITELLM_API_BASE']}")
        print(f"  - Provider: {os.environ['LITELLM_PROVIDER']}")
        
        import litellm
        litellm.set_verbose = True
        
        # Configurar tentativas para lidar com problemas de conexão
        litellm.num_retries = 3
        litellm.request_timeout = 120
        
        # Configurar para usar nossa API local do Ollama
        litellm.api_base = os.environ["LITELLM_API_BASE"]
        
        self.litellm = litellm
        self._test_connection()
    
    def _test_connection(self):
        """Testa a conexão com o Ollama e espera até estar pronto"""
        import requests
        
        max_retries = 5
        retry_count = 0
        
        print("Testando conexão com o Ollama...")
        
        while retry_count < max_retries:
            try:
                # Tenta fazer uma requisição simples à API do Ollama
                response = requests.get(f"{os.environ['LITELLM_API_BASE']}/api/version")
                if response.status_code == 200:
                    print(f"Conexão com Ollama estabelecida: {response.json()}")
                    return
                else:
                    print(f"Ollama respondeu com status code: {response.status_code}")
            except Exception as e:
                print(f"Erro ao conectar com Ollama: {str(e)}")
            
            retry_count += 1
            wait_time = 2 * retry_count
            print(f"Tentando novamente em {wait_time} segundos... (tentativa {retry_count}/{max_retries})")
            time.sleep(wait_time)
        
        print("Aviso: Não foi possível conectar ao Ollama após várias tentativas, mas continuando mesmo assim...")

# Configurar o LiteLLM uma única vez na inicialização
llm_adapter = CustomLiteLLM() 