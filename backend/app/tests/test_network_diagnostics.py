from unittest.mock import patch, MagicMock
import requests

from app.services.network_diagnostics import debug_service_connectivity


@patch("requests.get")
def test_debug_service_connectivity_success(mock_get):
    # Configura o mock para simular respostas bem-sucedidas
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "ok"}
    mock_get.return_value = mock_response

    result = debug_service_connectivity()
    assert isinstance(result, dict)
    assert "services" in result
    assert all(service["success"] for service in result["services"])


@patch("requests.get")
def test_debug_service_connectivity_partial_failure(mock_get):
    # Configura o mock para simular algumas falhas
    def mock_get_side_effect(*args, **kwargs):
        if "crewai" in args[0]:
            raise requests.exceptions.RequestException("Erro de conexão")
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok"}
        return mock_response

    mock_get.side_effect = mock_get_side_effect

    result = debug_service_connectivity()
    assert isinstance(result, dict)
    assert "services" in result
    assert not all(
        service["success"] for service in result["services"]
    )


@patch("requests.get")
def test_debug_service_connectivity_all_failure(mock_get):
    # Configura o mock para simular falhas em todos os serviços
    mock_get.side_effect = requests.exceptions.RequestException("Erro de conexão")

    result = debug_service_connectivity()
    assert isinstance(result, dict)
    assert "services" in result
    assert not any(
        service["success"] for service in result["services"]
    )


def test_debug_service_connectivity_timeout():
    # Testa o comportamento com timeout
    with patch("requests.get", side_effect=requests.exceptions.Timeout("Timeout")):
        result = debug_service_connectivity()
        assert isinstance(result, dict)
        assert "services" in result
        assert not any(
            service["success"] for service in result["services"]
        )
