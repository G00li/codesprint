import requests
import socket
import os
import time
import logging
from dotenv import load_dotenv
from typing import Dict

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("network_diagnostics")

# Carrega variáveis de ambiente
load_dotenv()

def check_host_connectivity(host, port):
    """Verifica se um host está acessível na rede"""
    logger.info(f"Verificando conectividade com {host}:{port}")
    
    # Primeiro tenta resolver o nome do host
    try:
        ip_address = socket.gethostbyname(host)
        logger.info(f"Nome de host {host} resolvido para IP: {ip_address}")
    except socket.gaierror:
        logger.error(f"Não foi possível resolver o nome de host: {host}")
        return False, f"Erro ao resolver nome de host {host}"
    
    # Tenta estabelecer conexão TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    
    try:
        result = sock.connect_ex((ip_address, port))
        if result == 0:
            logger.info(f"Conexão TCP estabelecida com sucesso para {host}:{port}")
            return True, f"Conexão TCP estabelecida com sucesso para {host}:{port}"
        else:
            logger.error(f"Falha ao conectar com {host}:{port}. Código de erro: {result}")
            return False, f"Falha ao conectar com {host}:{port}. Código de erro: {result}"
    except Exception as e:
        logger.error(f"Erro ao verificar conectividade com {host}:{port}: {str(e)}")
        return False, f"Erro ao verificar conectividade: {str(e)}"
    finally:
        sock.close()

def check_http_connectivity(url, expected_status=200, timeout=5):
    """Verifica conectividade HTTP com um serviço"""
    logger.info(f"Verificando conectividade HTTP com {url}")
    
    try:
        start_time = time.time()
        response = requests.get(url, timeout=timeout)
        elapsed = time.time() - start_time
        
        logger.info(f"Resposta recebida de {url} em {elapsed:.2f}s com status {response.status_code}")
        
        if response.status_code == expected_status:
            return True, {
                "status": response.status_code,
                "response_time": f"{elapsed:.2f}s",
                "body": response.text[:200] + "..." if len(response.text) > 200 else response.text
            }
        else:
            return False, {
                "status": response.status_code,
                "response_time": f"{elapsed:.2f}s",
                "error": f"Status code inesperado: {response.status_code}"
            }
    except requests.exceptions.Timeout:
        logger.error(f"Timeout ao conectar com {url} após {timeout}s")
        return False, {"error": f"Timeout após {timeout}s"}
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Erro de conexão com {url}: {str(e)}")
        return False, {"error": f"Erro de conexão: {str(e)}"}
    except Exception as e:
        logger.error(f"Erro inesperado ao conectar com {url}: {str(e)}")
        return False, {"error": f"Erro inesperado: {str(e)}"}

def run_network_diagnostics():
    """Executa diagnóstico completo da rede entre serviços"""
    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "services": {}
    }
    
    # Obter configurações do ambiente
    crewai_host = os.getenv("CREWAI_HOST", "crewai")
    crewai_port = int(os.getenv("CREWAI_PORT", "8004"))
    crewai_url = os.getenv("CREWAI_BASE_URL", f"http://{crewai_host}:{crewai_port}")
    
    # Cuidado com a URL do Ollama - não deve conter porta duplicada
    ollama_host_url = os.getenv("OLLAMA_HOST", "http://ollama:11434")
    # Extrair o host sem http:// e sem porta
    ollama_host = ollama_host_url.replace("http://", "").split(":")[0]
    ollama_port = 11434  # Porta padrão do Ollama
    
    # Diagnóstico CrewAI
    results["services"]["crewai"] = {}
    
    # Verificar conectividade TCP
    tcp_success, tcp_result = check_host_connectivity(crewai_host, crewai_port)
    results["services"]["crewai"]["tcp_connectivity"] = {
        "success": tcp_success,
        "details": tcp_result
    }
    
    # Verificar conectividade HTTP
    http_success, http_result = check_http_connectivity(f"{crewai_url}/health")
    results["services"]["crewai"]["http_connectivity"] = {
        "success": http_success,
        "details": http_result
    }
    
    # Diagnóstico Ollama
    results["services"]["ollama"] = {}
    
    # Verificar conectividade TCP
    tcp_success, tcp_result = check_host_connectivity(ollama_host, ollama_port)
    results["services"]["ollama"]["tcp_connectivity"] = {
        "success": tcp_success,
        "details": tcp_result
    }
    
    # Verificar conectividade HTTP
    ollama_url = f"http://{ollama_host}:{ollama_port}/api/version"
    http_success, http_result = check_http_connectivity(ollama_url)
    results["services"]["ollama"]["http_connectivity"] = {
        "success": http_success,
        "details": http_result
    }
    
    return results

def debug_service_connectivity() -> Dict:
    results = []
    services = [
        {
            "name": "CrewAI",
            "url": f"{os.getenv('CREWAI_BASE_URL', 'http://crewai:8004')}/health",
            "timeout": 5
        },
        {
            "name": "Ollama",
            "url": f"{os.getenv('OLLAMA_BASE_URL', 'http://ollama:11434')}/api/version",
            "timeout": 5
        }
    ]

    for service in services:
        try:
            start_time = time.time()
            response = requests.get(service["url"], timeout=service["timeout"])
            response_time = time.time() - start_time

            results.append({
                "name": service["name"],
                "url": service["url"],
                "success": response.ok,
                "status_code": response.status_code,
                "response_time": f"{response_time:.2f}s",
                "data": response.json() if response.ok else None
            })
        except requests.exceptions.Timeout:
            results.append({
                "name": service["name"],
                "url": service["url"],
                "success": False,
                "error": f"Timeout após {service['timeout']}s"
            })
        except requests.exceptions.ConnectionError as e:
            results.append({
                "name": service["name"],
                "url": service["url"],
                "success": False,
                "error": str(e)
            })
        except Exception as e:
            results.append({
                "name": service["name"],
                "url": service["url"],
                "success": False,
                "error": f"Erro inesperado: {str(e)}"
            })

    all_success = all(service["success"] for service in results)
    return {
        "success": all_success,
        "services": results,
        "message": "✅ Todos os serviços estão conectados e respondendo corretamente" if all_success else "❌ ALGUNS SERVIÇOS NÃO ESTÃO CONECTADOS OU RESPONDENDO CORRETAMENTE"
    }

if __name__ == "__main__":
    debug_service_connectivity() 