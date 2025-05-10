import pytest
from unittest.mock import patch, MagicMock
from app.services.crewai import CrewAiService
import os

@pytest.fixture
def crewai_service():
    return CrewAiService()

def test_crewai_service_initialization():
    service = CrewAiService()
    assert service.base_url == os.getenv("CREWAI_BASE_URL", "http://crewai:8004")

@patch('requests.post')
def test_gerar_projeto_success(mock_post):
    # Configura o mock para simular uma resposta bem-sucedida
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "projeto": "Teste de projeto",
        "status": "success"
    }
    mock_post.return_value = mock_response

    service = CrewAiService()
    result = service.gerar_projeto(
        areas=["web", "backend"],
        tecnologias="Python, FastAPI",
        descricao="Projeto de teste",
        usar_exa=False
    )

    assert result["status"] == "success"
    assert "projeto" in result["data"]

@patch('requests.post')
def test_gerar_projeto_error(mock_post):
    # Configura o mock para simular um erro
    mock_post.side_effect = Exception("Erro de conexão")

    service = CrewAiService()
    result = service.gerar_projeto(
        areas=["web", "backend"],
        tecnologias="Python, FastAPI",
        descricao="Projeto de teste",
        usar_exa=False
    )

    assert result["status"] == "error"
    assert "error" in result

@patch('requests.get')
def test_health_check_success(mock_get):
    # Configura o mock para simular uma resposta bem-sucedida
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "ok"}
    mock_get.return_value = mock_response

    service = CrewAiService()
    result = service.check_health()

    assert result["status"] == "ok"
    assert result["success"] is True

@patch('requests.get')
def test_health_check_error(mock_get):
    # Configura o mock para simular um erro
    mock_get.side_effect = Exception("Erro de conexão")

    service = CrewAiService()
    result = service.check_health()

    assert result["success"] is False
    assert "error" in result 