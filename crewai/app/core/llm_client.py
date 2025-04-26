import os
from ollama import Client

class OllamaLLM:
    def __init__(self, model_name="llama3", temperature=0.3):
        host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.client = Client(host=host)
        self.model = model_name
        self.temperature = temperature

    def chat(self, messages):
        response = self.client.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": self.temperature
            }
        )
        return response["message"]["content"]

    def generate(self, prompt):
        return self.chat([
            {"role": "user", "content": prompt}
        ])
