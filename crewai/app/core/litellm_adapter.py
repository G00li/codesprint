import os
import time
import logging
from typing import Dict, List, Any, Optional

# Configuração do LiteLLM para usar nossa instância de Ollama com tolerância a falhas
class CustomLiteLLM:
    def __init__(self):
        # Configurar variáveis de ambiente para o LiteLLM
        os.environ["LITELLM_MODEL_NAME"] = "ollama/llama2:7b-chat"  # Formato correto com provider
        os.environ["LITELLM_API_BASE"] = "http://ollama:11434"  # Usar o nome do serviço do Docker Compose
        os.environ["LITELLM_PROVIDER"] = "ollama"
        os.environ["LITELLM_API_KEY"] = "dummy"
        
        # Imprimir configuração para debug
        print(f"Configurando LiteLLM com:")
        print(f"  - Model: {os.environ['LITELLM_MODEL_NAME']}")
        print(f"  - API Base: {os.environ['LITELLM_API_BASE']}")
        print(f"  - Provider: {os.environ['LITELLM_PROVIDER']}")
        
        # Inicializar o módulo litellm
        import litellm
        os.environ["LITELLM_LOG"] = "INFO"  # Usar variável de ambiente em vez de set_verbose
        
        # Configurar tentativas para lidar com problemas de conexão
        litellm.num_retries = 3
        litellm.request_timeout = 1200
        
        # Armazenar o módulo para uso posterior
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
        
    def chat(self, messages):
        """
        Implementa o método chat para compatibilidade com a interface esperada
        por execute_task_directly no crewai_generator.py
        """
        try:
            from litellm import completion
            
            # Usar o formato correto para o modelo
            response = completion(
                model="ollama/llama2:7b-chat",  # Nome completo do modelo com o provider
                api_base="http://ollama:11434",  # URL do serviço Ollama
                messages=messages,
                temperature=0.3,
                max_tokens=500,  # Limitar o tamanho da resposta
                timeout=10000  # Timeout específico para a chamada
            )
            
            # Extrair a resposta do modelo
            if hasattr(response, 'choices') and len(response.choices) > 0:
                if hasattr(response.choices[0], 'message') and hasattr(response.choices[0].message, 'content'):
                    return response.choices[0].message.content
            
            # Fallback caso a estrutura da resposta seja diferente
            return str(response)
            
        except Exception as e:
            error_msg = f"Erro ao gerar resposta via LiteLLM: {str(e)}"
            print(error_msg)
            # Retornar uma resposta de erro que ainda pode ser usada pelo sistema
            return f"Não foi possível gerar uma análise devido a um erro técnico. Por favor, tente novamente mais tarde."

# Configurar o LiteLLM uma única vez na inicialização
llm_adapter = CustomLiteLLM() 