#!/bin/bash

# Ativa o ambiente virtual do Poetry
source $(poetry env info --path)/bin/activate

# Instala as dependências de desenvolvimento se necessário
poetry install

# Executa os testes com cobertura
poetry run pytest --cov=app --cov-report=term-missing -v

# Desativa o ambiente virtual
deactivate 