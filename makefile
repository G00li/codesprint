

# Cores para mensagens
GREEN = \033[0;32m
BLUE = \033[0;34m
NC = \033[0m # No Color


help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n",$$1,$$2}'


up: ## Start all containers
	@echo "${BLUE}Subindo containers...${NC}"
	docker-compose up -d --build backend crewai
	@echo "${BLUE}Aguardando backend iniciar...${NC}"

down: ## Stop all containers
	@echo "${BLUE}Parando containers...${NC}"
	docker compose down --volumes
	@echo "${GREEN}Todos os serviços foram parados!${NC}"

restart: ## Restart all containers
	@echo "${BLUE}Reiniciando containers...${NC}"
	docker compose restart
	@echo "${GREEN}Todos os serviços foram reiniciados!${NC}"

clean: ## Clean all containers and volumes
	@echo "${BLUE}Limpando ambiente...${NC}"
	docker compose down -v --remove-orphans
	@echo "${GREEN}Ambiente limpo!${NC}"

up_crewai: ## Start crewai container
	@echo "${BLUE}Subindo container crewai...${NC}"
	docker compose build --no-cache crewai
	@echo "${GREEN}Container crewai subido com sucesso!${NC}"

down_crewai: ## Stop crewai container
	@echo "${BLUE}Parando container crewai...${NC}"
	docker compose down crewai
	@echo "${GREEN}Container Crewai Encerrado!${NC}"


env_backend:
	$(poetry env activate backend)

env_crewai:
	$(poetry env activate crewai)

env_desactivate:
	deactivate