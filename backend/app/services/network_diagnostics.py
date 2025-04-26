import requests
import socket
import os
import time
import logging
from dotenv import load_dotenv

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

def debug_service_connectivity():
    """Função principal para diagnóstico de conectividade entre serviços"""
    logger.info("Iniciando diagnóstico de rede entre serviços...")
    
    try:
        results = run_network_diagnostics()
        
        # Imprime resultados formatados
        logger.info("=== Resultados do Diagnóstico de Rede ===")
        
        for service_name, service_results in results["services"].items():
            logger.info(f"\n--- Serviço: {service_name} ---")
            
            tcp_result = service_results.get("tcp_connectivity", {})
            http_result = service_results.get("http_connectivity", {})
            
            logger.info(f"TCP: {'✅ Conectado' if tcp_result.get('success') else '❌ Falha'}")
            if not tcp_result.get('success'):
                logger.info(f"  Detalhes: {tcp_result.get('details')}")
                
            logger.info(f"HTTP: {'✅ Conectado' if http_result.get('success') else '❌ Falha'}")
            if http_result.get('success'):
                http_details = http_result.get('details', {})
                logger.info(f"  Status: {http_details.get('status')}")
                logger.info(f"  Tempo de resposta: {http_details.get('response_time')}")
            else:
                http_details = http_result.get('details', {})
                logger.info(f"  Erro: {http_details.get('error')}")
        
        # Verificar se todos os serviços estão conectados
        all_connected = all([
            results["services"][svc].get("tcp_connectivity", {}).get("success", False) and 
            results["services"][svc].get("http_connectivity", {}).get("success", False)
            for svc in results["services"]
        ])
        
        if all_connected:
            logger.info("\n✅ TODOS OS SERVIÇOS ESTÃO CONECTADOS E RESPONDENDO CORRETAMENTE")
        else:
            logger.error("\n❌ ALGUNS SERVIÇOS NÃO ESTÃO CONECTADOS OU RESPONDENDO CORRETAMENTE")
            
            # Sugestões de troubleshooting
            logger.info("\n=== Sugestões para Troubleshooting ===")
            
            for service_name, service_results in results["services"].items():
                tcp_success = service_results.get("tcp_connectivity", {}).get("success", False)
                http_success = service_results.get("http_connectivity", {}).get("success", False)
                
                if not tcp_success or not http_success:
                    logger.info(f"\nProblemas com {service_name}:")
                    
                    if not tcp_success:
                        logger.info(f"  • Verifique se o contêiner do {service_name} está em execução: docker-compose ps")
                        logger.info(f"  • Verifique as configurações de rede no docker-compose.yml")
                        logger.info(f"  • Verifique se o serviço está expondo a porta correta")
                    
                    if tcp_success and not http_success:
                        logger.info(f"  • O serviço {service_name} está ativo, mas a API não está respondendo como esperado")
                        logger.info(f"  • Verifique os logs do serviço: docker-compose logs {service_name}")
                        logger.info(f"  • Verifique se a aplicação está sendo inicializada corretamente")
        
        return results
        
    except Exception as e:
        logger.error(f"Erro durante diagnóstico de rede: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    debug_service_connectivity() 