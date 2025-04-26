#!/bin/bash

# Cores para saída
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}  DIAGNÓSTICO DO CODESPRINT - VERIFICAÇÃO SERVIÇOS  ${NC}"
echo -e "${BLUE}====================================================${NC}"

# Função para verificar se um contêiner está em execução
check_container() {
    local container_name=$1
    local state=$(docker-compose ps -q $container_name 2>/dev/null)
    
    if [ -z "$state" ]; then
        echo -e "${RED}✘ Contêiner $container_name não encontrado${NC}"
        return 1
    else
        local status=$(docker inspect --format='{{.State.Status}}' $state 2>/dev/null)
        if [ "$status" == "running" ]; then
            echo -e "${GREEN}✓ Contêiner $container_name está rodando${NC}"
            return 0
        else
            echo -e "${RED}✘ Contêiner $container_name está $status${NC}"
            return 1
        fi
    fi
}

# Função para testar conectividade HTTP
test_http() {
    local url=$1
    local description=$2
    
    echo -e "\n${YELLOW}Testando $description ($url)...${NC}"
    
    response=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 $url 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        if [ "$response" -ge 200 ] && [ "$response" -lt 400 ]; then
            echo -e "${GREEN}✓ $description está acessível ($response)${NC}"
            return 0
        else
            echo -e "${RED}✘ $description retornou erro HTTP $response${NC}"
            return 1
        fi
    else
        echo -e "${RED}✘ Não foi possível conectar com $description${NC}"
        return 1
    fi
}

# Função para mostrar os logs de um contêiner
show_logs() {
    local container_name=$1
    local lines=${2:-20}
    
    echo -e "\n${YELLOW}Últimas $lines linhas de log do $container_name:${NC}"
    docker-compose logs --tail=$lines $container_name
}

# Verifica o docker-compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Erro: docker-compose não encontrado${NC}"
    exit 1
fi

# Status dos contêineres
echo -e "\n${YELLOW}Verificando status dos contêineres...${NC}"
docker-compose ps

# Verifica cada serviço individualmente
echo -e "\n${YELLOW}Verificando status individual de cada serviço...${NC}"
frontend_ok=0
backend_ok=0
crewai_ok=0
redis_ok=0
ollama_ok=0

# Verifica o serviço Frontend
check_container "frontend" && frontend_ok=1

# Verifica o serviço Backend
check_container "backend" && backend_ok=1

# Verifica o serviço CrewAI
check_container "crewai" && crewai_ok=1

# Verifica o serviço Redis
check_container "redis" && redis_ok=1

# Verifica o serviço Ollama
check_container "ollama" && ollama_ok=1

# Testes de conectividade
echo -e "\n${YELLOW}Realizando testes de conectividade...${NC}"

# Testes de conectividade HTTP
[ $frontend_ok -eq 1 ] && test_http "http://localhost:3000" "Frontend"
[ $backend_ok -eq 1 ] && test_http "http://localhost:8000/health" "Backend (health endpoint)"
[ $backend_ok -eq 1 ] && test_http "http://localhost:8000/diagnose-crewai" "Backend (diagnóstico CrewAI)"
[ $crewai_ok -eq 1 ] && test_http "http://localhost:8004/health" "CrewAI (health endpoint)"
[ $ollama_ok -eq 1 ] && test_http "http://localhost:11434/api/version" "Ollama (version endpoint)"

# Mostra logs para serviços com problemas
if [ $backend_ok -eq 0 ]; then
    show_logs "backend" 30
fi

if [ $crewai_ok -eq 0 ]; then
    show_logs "crewai" 30
fi

if [ $ollama_ok -eq 0 ]; then
    show_logs "ollama" 30
fi

# Diagnóstico de rede interno (executado do contêiner backend)
if [ $backend_ok -eq 1 ]; then
    echo -e "\n${YELLOW}Executando diagnóstico de rede interno (do contêiner backend)...${NC}"
    docker-compose exec backend python -m app.services.network_diagnostics
fi

echo -e "\n${YELLOW}Diagnóstico concluído.${NC}"
echo -e "\nPara diagnóstico via UI, acesse: http://localhost:3000/diagnostico/manual"
echo -e "Para ver os logs completos: docker-compose logs [serviço]" 