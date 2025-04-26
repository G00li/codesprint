#!/bin/bash

# Cores para saída
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}  CORREÇÃO DE CONECTIVIDADE ENTRE SERVIÇOS          ${NC}"
echo -e "${BLUE}====================================================${NC}"

# Verifica qual ambiente estamos rodando (container ou local)
IN_CONTAINER=0
if [ -f /.dockerenv ]; then
    echo -e "${YELLOW}Detectado ambiente de contêiner Docker${NC}"
    IN_CONTAINER=1
else
    echo -e "${YELLOW}Detectado ambiente local (fora de contêiner)${NC}"
fi

# Verifica o arquivo .env do frontend
echo -e "\n${YELLOW}Verificando configuração do frontend...${NC}"

if [ -f ./frontend/.env ]; then
    FRONTEND_ENV_BACKEND_URL=$(grep NEXT_PUBLIC_BACKEND_URL ./frontend/.env | cut -d '=' -f2)
    
    if [ -z "$FRONTEND_ENV_BACKEND_URL" ]; then
        echo -e "${RED}Variável NEXT_PUBLIC_BACKEND_URL não encontrada no arquivo .env do frontend${NC}"
        
        if [ $IN_CONTAINER -eq 1 ]; then
            echo -e "${YELLOW}Criando variável com valor para ambiente de contêiner...${NC}"
            echo "NEXT_PUBLIC_BACKEND_URL=http://backend:8000" >> ./frontend/.env
            echo -e "${GREEN}Adicionado NEXT_PUBLIC_BACKEND_URL=http://backend:8000${NC}"
        else
            echo -e "${YELLOW}Criando variável com valor para ambiente local...${NC}"
            echo "NEXT_PUBLIC_BACKEND_URL=http://localhost:8000" >> ./frontend/.env
            echo -e "${GREEN}Adicionado NEXT_PUBLIC_BACKEND_URL=http://localhost:8000${NC}"
        fi
    else
        echo -e "Valor atual de NEXT_PUBLIC_BACKEND_URL: ${YELLOW}$FRONTEND_ENV_BACKEND_URL${NC}"
        
        if [ $IN_CONTAINER -eq 1 ] && [[ "$FRONTEND_ENV_BACKEND_URL" == *"localhost"* ]]; then
            echo -e "${RED}Configuração incorreta para ambiente de contêiner!${NC}"
            echo -e "${YELLOW}Corrigindo...${NC}"
            
            # Substitui a linha no arquivo .env
            sed -i 's|NEXT_PUBLIC_BACKEND_URL=.*|NEXT_PUBLIC_BACKEND_URL=http://backend:8000|g' ./frontend/.env
            
            echo -e "${GREEN}Atualizado para NEXT_PUBLIC_BACKEND_URL=http://backend:8000${NC}"
            
        elif [ $IN_CONTAINER -eq 0 ] && [[ "$FRONTEND_ENV_BACKEND_URL" == *"backend"* ]]; then
            echo -e "${RED}Configuração incorreta para ambiente local!${NC}"
            echo -e "${YELLOW}Corrigindo...${NC}"
            
            # Substitui a linha no arquivo .env
            sed -i 's|NEXT_PUBLIC_BACKEND_URL=.*|NEXT_PUBLIC_BACKEND_URL=http://localhost:8000|g' ./frontend/.env
            
            echo -e "${GREEN}Atualizado para NEXT_PUBLIC_BACKEND_URL=http://localhost:8000${NC}"
        else
            echo -e "${GREEN}Configuração está correta para o ambiente atual.${NC}"
        fi
    fi
else
    echo -e "${RED}Arquivo .env não encontrado no diretório frontend${NC}"
    echo -e "${YELLOW}Criando arquivo .env...${NC}"
    
    if [ $IN_CONTAINER -eq 1 ]; then
        echo "NEXT_PUBLIC_BACKEND_URL=http://backend:8000" > ./frontend/.env
        echo -e "${GREEN}Criado arquivo .env com NEXT_PUBLIC_BACKEND_URL=http://backend:8000${NC}"
    else
        echo "NEXT_PUBLIC_BACKEND_URL=http://localhost:8000" > ./frontend/.env
        echo -e "${GREEN}Criado arquivo .env com NEXT_PUBLIC_BACKEND_URL=http://localhost:8000${NC}"
    fi
fi

# Verificando se temos acesso ao Docker
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo -e "\n${YELLOW}Verificando status dos serviços Docker...${NC}"
    docker-compose ps
    
    echo -e "\n${YELLOW}Deseja reiniciar o serviço frontend para aplicar as alterações? (s/n)${NC}"
    read -r resposta
    
    if [[ "$resposta" =~ ^[Ss]$ ]]; then
        echo -e "${YELLOW}Reiniciando o serviço frontend...${NC}"
        docker-compose restart frontend
        echo -e "${GREEN}Serviço frontend reiniciado!${NC}"
    fi
else
    echo -e "\n${RED}Docker ou Docker Compose não encontrados. Não é possível reiniciar os serviços.${NC}"
    echo -e "${YELLOW}Por favor, reinicie o serviço frontend manualmente para aplicar as alterações.${NC}"
fi

echo -e "\n${GREEN}Configuração concluída!${NC}"
echo -e "Agora acesse: ${BLUE}http://localhost:3000/diagnostico/manual${NC} para testar a conectividade." 