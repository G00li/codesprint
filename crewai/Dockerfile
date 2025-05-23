# Estágio de build
FROM python:3.12-slim as builder

# Instalar dependências necessárias para build
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Configurar Poetry
ENV POETRY_VERSION=1.8.2
ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false

# Configurar diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY pyproject.toml poetry.lock* ./

# Instalar dependências
RUN poetry install --no-root --no-interaction --no-ansi --no-dev

# Estágio final
FROM python:3.12-slim

# Configurar timezone
ENV TZ=Europe/Lisbon
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copiar apenas os arquivos necessários do estágio de build
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Configurar diretório de trabalho
WORKDIR /app

# Copiar código da aplicação
COPY . .

# Limpar caches e arquivos temporários
RUN find /app -type d -name "__pycache__" -exec rm -r {} + \
    && find /app -type f -name "*.pyc" -delete \
    && find /app -type f -name "*.pyo" -delete \
    && find /app -type f -name "*.pyd" -delete \
    && find /app -type f -name ".coverage" -delete \
    && find /app -type d -name "*.egg-info" -exec rm -r {} + \
    && find /app -type d -name "*.egg" -exec rm -r {} + \
    && find /app -type d -name ".pytest_cache" -exec rm -r {} + \
    && find /app -type d -name ".coverage" -exec rm -r {} + \
    && find /app -type d -name "htmlcov" -exec rm -r {} + \
    && find /app -type d -name ".mypy_cache" -exec rm -r {} + \
    && find /app -type d -name ".ruff_cache" -exec rm -r {} + \
    && find /app -type d -name ".hypothesis" -exec rm -r {} + \
    && rm -rf /root/.cache/pip/* \
    && rm -rf /root/.cache/pytest/* \
    && rm -rf /root/.cache/mypy/* \
    && rm -rf /root/.cache/ruff/*

# Expor porta
EXPOSE 8004

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004", "--timeout-keep-alive", "1200"]
