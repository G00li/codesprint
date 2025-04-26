#!/bin/bash

# Cores para saída
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}  TESTE DE CONECTIVIDADE ENTRE SERVIÇOS CODESPRINT  ${NC}"
echo -e "${BLUE}====================================================${NC}"

# Verifica se os serviços estão rodando
echo -e "\n${YELLOW}Verificando status dos contêineres Docker...${NC}"
docker-compose ps

# Verificar status do serviço CrewAI
echo -e "\n${YELLOW}Verificando logs recentes do serviço CrewAI...${NC}"
docker-compose logs --tail=20 crewai

# Verificar status do serviço Backend
echo -e "\n${YELLOW}Verificando logs recentes do serviço Backend...${NC}"
docker-compose logs --tail=20 backend

# Verificar status do serviço Ollama
echo -e "\n${YELLOW}Verificando logs recentes do serviço Ollama...${NC}"
docker-compose logs --tail=20 ollama

# Executar o teste de diagnóstico
echo -e "\n${YELLOW}Executando diagnóstico de rede entre serviços...${NC}"
echo -e "Acessando o contêiner do backend..."
docker-compose exec backend python -m app.services.network_diagnostics

# Testar o endpoint de geração de projeto
echo -e "\n${YELLOW}Testando o endpoint de geração de projeto...${NC}"
echo -e "Payload de teste:"
cat <<EOF
{
  "areas": ["Web", "API"],
  "tecnologias": "Python, FastAPI, React, TailwindCSS",
  "descricao": "Um sistema simples de gerenciamento de tarefas",
  "usar_exa": false
}
EOF

echo -e "\n${YELLOW}Enviando requisição...${NC}"
curl -X POST http://backend:8000/gerar-projeto \
  -H "Content-Type: application/json" \
  -d '{"areas":["Web", "API"],"tecnologias":"Python, FastAPI, React, TailwindCSS","descricao":"Um sistema simples de gerenciamento de tarefas","usar_exa":false}' \
  -w "\n\nStatus: %{http_code}, Tempo: %{time_total}s\n"

echo -e "\n${GREEN}Testes concluídos!${NC}"
echo -e "${YELLOW}Verifique os resultados acima para identificar possíveis problemas.${NC}"
echo -e "${YELLOW}Se encontrar erros, verifique os logs completos dos serviços:${NC}"
echo -e "  docker-compose logs crewai"
echo -e "  docker-compose logs backend"
echo -e "  docker-compose logs ollama" 