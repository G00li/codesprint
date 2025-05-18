# Cores para mensagens
GREEN = \033[0;32m
BLUE = \033[0;34m
RED = \033[0;31m
YELLOW = \033[0;33m
NC = \033[0m # No Color


help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n",$$1,$$2}'

install_llama: ## Install llama2:7b-chat model
	@echo "${BLUE}Instalando modelo llama2:7b-chat...${NC}"
	docker exec -it codesprint-ollama-1 ollama pull llama2:7b-chat
	@echo "${GREEN}Modelo instalado com sucesso!${NC}"

up: ## Start all containers
	@echo "${BLUE}Rebuildando containers...${NC}"
	docker-compose build
	@echo "${BLUE}Subindo containers...${NC}"
	docker-compose up -d
	@echo "${BLUE}Aguardando serviços iniciar...${NC}"
	sleep 10
	@echo "${BLUE}Verificando status dos serviços...${NC}"
	docker-compose ps
	@echo "${BLUE}Instalando modelo llama2:7b-chat...${NC}"
	docker exec -it codesprint-ollama-1 ollama pull llama2:7b-chat
	@echo "${GREEN}Todos os serviços foram iniciados e o modelo foi instalado com sucesso!${NC}"

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


test: ## Executar testes do backend
	@echo "${BLUE}Executando testes do backend...${NC}"
	cd backend && ./run_tests.sh
	@echo "${GREEN}Testes concluídos!${NC}"

fix_connection: ## Verifica e corrige a conectividade entre serviços
	@echo "${BLUE}====================================================${NC}"
	@echo "${BLUE}  CORREÇÃO DE CONECTIVIDADE ENTRE SERVIÇOS          ${NC}"
	@echo "${BLUE}====================================================${NC}"
	@if [ -f /.dockerenv ]; then \
		echo "${YELLOW}Detectado ambiente de contêiner Docker${NC}"; \
		BACKEND_URL="http://backend:8000"; \
	else \
		echo "${YELLOW}Detectado ambiente local (fora de contêiner)${NC}"; \
		BACKEND_URL="http://localhost:8000"; \
	fi
	@echo "\n${YELLOW}Verificando configuração do frontend...${NC}"
	@if [ -f ./frontend/.env ]; then \
		if grep -q "NEXT_PUBLIC_BACKEND_URL" ./frontend/.env; then \
			sed -i "s|NEXT_PUBLIC_BACKEND_URL=.*|NEXT_PUBLIC_BACKEND_URL=$$BACKEND_URL|g" ./frontend/.env; \
			echo "${GREEN}Configuração atualizada para NEXT_PUBLIC_BACKEND_URL=$$BACKEND_URL${NC}"; \
		else \
			echo "NEXT_PUBLIC_BACKEND_URL=$$BACKEND_URL" >> ./frontend/.env; \
			echo "${GREEN}Adicionado NEXT_PUBLIC_BACKEND_URL=$$BACKEND_URL${NC}"; \
		fi \
	else \
		echo "NEXT_PUBLIC_BACKEND_URL=$$BACKEND_URL" > ./frontend/.env; \
		echo "${GREEN}Criado arquivo .env com NEXT_PUBLIC_BACKEND_URL=$$BACKEND_URL${NC}"; \
	fi
	@echo "\n${YELLOW}Verificando status dos serviços Docker...${NC}"
	@docker-compose ps
	@echo "\n${YELLOW}Reiniciando o serviço frontend...${NC}"
	@docker-compose restart frontend
	@echo "${GREEN}Serviço frontend reiniciado!${NC}"
	@echo "\n${GREEN}Configuração concluída!${NC}"
	@echo "Acesse: ${BLUE}http://localhost:3000/diagnostico/manual${NC} para testar a conectividade."

check_services: ## Verifica status e conectividade de todos os serviços
	@echo "${BLUE}====================================================${NC}"
	@echo "${BLUE}  DIAGNÓSTICO DO CODESPRINT - VERIFICAÇÃO SERVIÇOS  ${NC}"
	@echo "${BLUE}====================================================${NC}"
	@echo "\n${YELLOW}Verificando status dos contêineres...${NC}"
	@docker-compose ps
	@echo "\n${YELLOW}Verificando status individual de cada serviço...${NC}"
	@for service in frontend backend crewai redis ollama; do \
		container_id=$$(docker-compose ps -q $$service 2>/dev/null); \
		if [ -z "$$container_id" ]; then \
			echo "${RED}✘ Contêiner $$service não encontrado${NC}"; \
		else \
			status=$$(docker inspect --format='{{.State.Status}}' $$container_id 2>/dev/null); \
			if [ "$$status" = "running" ]; then \
				echo "${GREEN}✓ Contêiner $$service está rodando${NC}"; \
			else \
				echo "${RED}✘ Contêiner $$service está $$status${NC}"; \
			fi; \
		fi; \
	done
	@echo "\n${YELLOW}Realizando testes de conectividade...${NC}"
	@echo "\n${YELLOW}Testando Frontend (http://localhost:3000)...${NC}"
	@if curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 http://localhost:3000 | grep -q "^[23]"; then \
		echo "${GREEN}✓ Frontend está acessível${NC}"; \
	else \
		echo "${RED}✘ Frontend não está acessível${NC}"; \
	fi
	@echo "\n${YELLOW}Testando Backend (http://localhost:8000/health)...${NC}"
	@if curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 http://localhost:8000/health | grep -q "^[23]"; then \
		echo "${GREEN}✓ Backend está acessível${NC}"; \
	else \
		echo "${RED}✘ Backend não está acessível${NC}"; \
	fi
	@echo "\n${YELLOW}Testando CrewAI (http://localhost:8004/health)...${NC}"
	@if curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 http://localhost:8004/health | grep -q "^[23]"; then \
		echo "${GREEN}✓ CrewAI está acessível${NC}"; \
	else \
		echo "${RED}✘ CrewAI não está acessível${NC}"; \
	fi
	@echo "\n${YELLOW}Testando Ollama (http://localhost:11434/api/version)...${NC}"
	@if curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 http://localhost:11434/api/version | grep -q "^[23]"; then \
		echo "${GREEN}✓ Ollama está acessível${NC}"; \
	else \
		echo "${RED}✘ Ollama não está acessível${NC}"; \
	fi
	@echo "\n${YELLOW}Mostrando logs dos serviços com problemas...${NC}"
	@for service in backend crewai ollama; do \
		if ! docker-compose ps -q $$service | xargs -r docker inspect --format='{{.State.Status}}' | grep -q "running"; then \
			echo "\n${YELLOW}Últimas 30 linhas de log do $$service:${NC}"; \
			docker-compose logs --tail=30 $$service; \
		fi; \
	done
	@if docker-compose ps -q backend | xargs -r docker inspect --format='{{.State.Status}}' | grep -q "running"; then \
		echo "\n${YELLOW}Executando diagnóstico de rede interno (do contêiner backend)...${NC}"; \
		docker-compose exec backend python -m app.services.network_diagnostics; \
	fi
	@echo "\n${YELLOW}Diagnóstico concluído.${NC}"
	@echo "\nPara diagnóstico via UI, acesse: http://localhost:3000/diagnostico/manual"
	@echo "Para ver os logs completos: docker-compose logs [serviço]"