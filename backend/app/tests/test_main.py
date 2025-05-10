import pytest
from fastapi.testclient import TestClient
from app.main import app
import os
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "Tudo correto"}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "messagem" in response.json()

def test_gerar_projeto():
    projeto_data = {
        "areas": ["web", "backend"],
        "tecnologias": "Python, FastAPI",
        "descricao": "Projeto de teste",
        "usar_exa": False
    }
    response = client.post("/gerar-projeto", json=projeto_data)
    assert response.status_code in [200, 503]  # 503 se o CrewAI não estiver disponível

def test_gerar_projeto_invalid_data():
    # Teste com dados inválidos
    invalid_data = {
        "areas": [],  # áreas vazias
        "tecnologias": "",  # tecnologias vazias
        "descricao": ""  # descrição vazia
    }
    response = client.post("/gerar-projeto", json=invalid_data)
    assert response.status_code == 422  # Erro de validação

def test_diagnose_crewai():
    response = client.get("/diagnose-crewai")
    assert response.status_code == 200
    data = response.json()
    assert "crewai_url" in data
    assert "connection_test" in data

@patch('requests.get')
def test_diagnose_crewai_with_mock(mock_get):
    # Configura o mock para simular uma resposta bem-sucedida
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "ok"}
    mock_get.return_value = mock_response

    response = client.get("/diagnose-crewai")
    assert response.status_code == 200
    data = response.json()
    assert data["connection_test"]["status_code"] == 200

def test_diagnose_network():
    response = client.get("/diagnose-network")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_db_health():
    response = client.get("/api/health/db")
    assert response.status_code in [200, 503]  # 503 se o banco não estiver disponível

def test_db_health_alt():
    response = client.get("/health/db")
    assert response.status_code in [200, 503]

def test_teste_rapido():
    response = client.get("/api/teste-rapido")
    assert response.status_code == 200
    data = response.json()
    assert "backendUrl" in data
    assert "testTime" in data
    assert "results" in data
    assert isinstance(data["results"], list)

def test_test_results():
    response = client.get("/api/test-results")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "tests" in data
    assert isinstance(data["tests"], list) 