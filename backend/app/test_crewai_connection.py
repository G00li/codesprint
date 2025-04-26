import requests
import json
import os
import time
from dotenv import load_dotenv
import sys

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações
CREWAI_BASE_URL = os.getenv("CREWAI_BASE_URL", "http://crewai:8004")
BACKEND_BASE_URL = "http://backend:8000"  # Ajuste conforme necessário

def test_crewai_health():
    """Testa se o serviço CrewAI está acessível e respondendo"""
    try:
        print(f"Testando conexão com CrewAI em {CREWAI_BASE_URL}/health...")
        response = requests.get(f"{CREWAI_BASE_URL}/health", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Erro ao testar conexão com CrewAI: {str(e)}")
        return False

def test_backend_health():
    """Testa se o backend está acessível e respondendo"""
    try:
        print(f"Testando conexão com Backend em {BACKEND_BASE_URL}/health...")
        response = requests.get(f"{BACKEND_BASE_URL}/health", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Erro ao testar conexão com Backend: {str(e)}")
        return False

def test_gerar_projeto():
    """Testa a funcionalidade de geração de projeto"""
    payload = {
        "areas": ["Web", "API"],
        "tecnologias": "Python, FastAPI, React, TailwindCSS",
        "descricao": "Um sistema simples de gerenciamento de tarefas com backend e frontend.",
        "usar_exa": False
    }
    
    try:
        print(f"Enviando request para {BACKEND_BASE_URL}/gerar-projeto...")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        # Longa timeout para dar tempo suficiente para o processamento
        response = requests.post(f"{BACKEND_BASE_URL}/gerar-projeto", json=payload, timeout=300)
        
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code != 200 or "error" in response.json():
            print("❌ TESTE FALHOU: A API retornou um erro!")
            return False
        else:
            print("✅ TESTE PASSOU: Projeto gerado com sucesso!")
            return True
    except Exception as e:
        print(f"❌ TESTE FALHOU: Erro ao enviar request: {str(e)}")
        return False

def diagnose_network():
    """Realiza diagnóstico de rede entre os serviços"""
    print("\n🔍 DIAGNÓSTICO DE REDE:")
    
    # Verifica se o backend está acessando o crewai corretamente
    try:
        response = requests.get(f"{BACKEND_BASE_URL}/diagnose-crewai", timeout=5)
        print(f"Diagnóstico de conexão backend -> crewai: {response.json()}")
    except Exception as e:
        print(f"Não foi possível obter diagnóstico: {str(e)}")
    
    # Tenta um curl direto do backend para o crewai
    print("\nTentando executar curl do backend para o crewai...")
    try:
        import subprocess
        result = subprocess.run(["curl", "-s", f"{CREWAI_BASE_URL}/health"], 
                                capture_output=True, text=True, timeout=5)
        print(f"Resultado do curl: {result.stdout}")
        if result.stderr:
            print(f"Erros: {result.stderr}")
    except Exception as e:
        print(f"Erro ao executar curl: {str(e)}")

def main():
    print("🧪 INICIANDO TESTES DE CONEXÃO COM CREWAI 🧪")
    print("-" * 50)
    
    # Primeiro teste de saúde dos serviços
    crewai_health = test_crewai_health()
    backend_health = test_backend_health()
    
    if not crewai_health:
        print("\n⚠️  O serviço CrewAI não está respondendo!")
        print("Sugestões:")
        print("1. Verifique se o contêiner do CrewAI está em execução: docker-compose ps")
        print("2. Verifique os logs do CrewAI: docker-compose logs crewai")
        print("3. Verifique se as variáveis de ambiente CREWAI_BASE_URL estão configuradas corretamente")
        return False
    
    if not backend_health:
        print("\n⚠️  O serviço de Backend não está respondendo!")
        print("Sugestões:")
        print("1. Verifique se o contêiner do Backend está em execução: docker-compose ps")
        print("2. Verifique os logs do Backend: docker-compose logs backend")
        return False
    
    # Se os serviços estão saudáveis, testa a geração de projeto
    if crewai_health and backend_health:
        print("\n🔄 Testando geração de projeto...")
        resultado = test_gerar_projeto()
        
        if not resultado:
            print("\n🔍 Executando diagnóstico de rede...")
            diagnose_network()
            
            print("\n⚠️  Dicas para solucionar o problema:")
            print("1. Verifique os logs do CrewAI: docker-compose logs crewai")
            print("2. Verifique se o Ollama está rodando e acessível pelo CrewAI")
            print("3. Verifique se as portas estão mapeadas corretamente no docker-compose.yml")
            print("4. Verifique se há erros no log do backend relacionados à conexão com CrewAI")
    
    print("\n✨ TESTE CONCLUÍDO ✨")

if __name__ == "__main__":
    main() 