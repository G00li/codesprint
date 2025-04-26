#!/bin/bash

# Cores para saída
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}     INICIALIZAÇÃO DOS SERVIÇOS DO CODESPRINT      ${NC}"
echo -e "${BLUE}====================================================${NC}"

# Parar e remover todos os contêineres
echo -e "\n${YELLOW}Parando todos os contêineres existentes...${NC}"
docker-compose down

# Iniciar apenas o Ollama primeiro
echo -e "\n${YELLOW}Iniciando o serviço Ollama...${NC}"
docker-compose up -d ollama redis

# Aguardar o Ollama iniciar completamente
echo -e "\n${YELLOW}Aguardando o Ollama iniciar (pode demorar alguns minutos)...${NC}"
attempt=1
max_attempts=30
while [ $attempt -le $max_attempts ]; do
    echo -e "Verificando disponibilidade do Ollama (tentativa $attempt/$max_attempts)"
    
    # Verifica se o Ollama está respondendo, usando curl do host
    if curl -s http://localhost:11434/api/version > /dev/null; then
        echo -e "${GREEN}Ollama está funcionando!${NC}"
        break
    else
        echo -e "${YELLOW}Ollama ainda não está pronto, aguardando...${NC}"
        sleep 5
        attempt=$((attempt+1))
    fi
done

if [ $attempt -gt $max_attempts ]; then
    echo -e "${RED}Erro: Ollama não iniciou após várias tentativas.${NC}"
    echo -e "${YELLOW}Verifique os logs para mais detalhes:${NC} docker-compose logs ollama"
    exit 1
fi

# Baixar o modelo manualmente usando a API REST
echo -e "\n${YELLOW}Verificando status do modelo llama3:8b...${NC}"
curl -s http://localhost:11434/api/tags | grep -q "llama3:8b"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Modelo llama3:8b já está disponível.${NC}"
else
    echo -e "${YELLOW}Baixando o modelo llama3:8b (isso pode demorar vários minutos)...${NC}"
    # Usando o comando curl para baixar o modelo
    curl -X POST http://localhost:11434/api/pull -d '{"name": "llama3:8b"}' &
    
    # Iniciar monitoramento do download em segundo plano
    (
        progress=0
        while [ $progress -lt 100 ]; do
            sleep 10
            echo -n "."
            # Verificar se o modelo já foi baixado
            if curl -s http://localhost:11434/api/tags | grep -q "llama3:8b"; then
                echo -e "\n${GREEN}Download do modelo llama3:8b concluído!${NC}"
                progress=100
            else
                progress=$((progress+5))
                if [ $progress -ge 100 ]; then
                    echo -e "\n${YELLOW}Tempo de download esgotado, continuando mesmo assim...${NC}"
                fi
            fi
        done
    ) &
    
    # Aguardar um tempo para o download iniciar
    echo -e "${YELLOW}Aguardando o download iniciar (continue observando os logs)...${NC}"
    sleep 20
fi

# Iniciar os demais serviços mesmo que o download não tenha terminado
echo -e "\n${YELLOW}Iniciando os demais serviços...${NC}"
docker-compose up -d

# Verificar se todos os serviços estão rodando
echo -e "\n${YELLOW}Verificando o status dos serviços...${NC}"
docker-compose ps

echo -e "\n${GREEN}Todos os serviços foram iniciados!${NC}"
echo -e "${YELLOW}Aguarde alguns instantes para que todos estejam completamente operacionais.${NC}"
echo -e "${YELLOW}Se o Ollama ainda estiver baixando o modelo, outros serviços podem ficar em estado 'starting'.${NC}"
echo -e "${YELLOW}Para testar a conexão, execute:${NC} ./backend/test_connection.sh" 