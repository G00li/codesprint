import os
import time
import logging
from ollama import Client

class OllamaLLM:
    def __init__(self, model_name="llama3:8b", temperature=0.3):
        host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
        print(f"Inicializando OllamaLLM com host: {host}, modelo: {model_name}")
        self.client = None
        self.model = model_name
        self.temperature = temperature
        self._init_client(host)
        
    def _init_client(self, host):
        # Tenta inicializar o cliente algumas vezes, com espera entre tentativas
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            try:
                print(f"Tentativa {retry_count+1} de conectar ao Ollama em {host}")
                self.client = Client(host=host)
                # Testa a conexão com um request simples
                self.client.list()
                print(f"Conexão estabelecida com sucesso com Ollama em {host}")
                return
            except Exception as e:
                print(f"Erro conectando ao Ollama: {str(e)}")
                retry_count += 1
                if retry_count < max_retries:
                    wait_time = 2 * retry_count  # Backoff exponencial
                    print(f"Tentando novamente em {wait_time} segundos...")
                    time.sleep(wait_time)
                else:
                    print("Falha ao conectar com o Ollama após várias tentativas.")
                    raise

    def chat(self, messages):
        try:
            response = self.client.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": self.temperature
                }
            )
            return response["message"]["content"]
        except Exception as e:
            error_msg = f"Erro durante a chamada ao Ollama: {str(e)}"
            print(error_msg)
            raise Exception(error_msg)

    def generate(self, prompt):
        return self.chat([
            {"role": "user", "content": prompt}
        ])
