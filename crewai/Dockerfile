FROM python:3.12

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry
RUN poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --no-interaction --no-ansi

COPY . .

EXPOSE 8004

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004"]
