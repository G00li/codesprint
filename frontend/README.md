# CodeSprint Frontend

Frontend responsivo para a plataforma CodeSprint, desenvolvido com Next.js e Tailwind CSS.

## Tecnologias Utilizadas

- Next.js 15.3.1
- React 19
- TypeScript
- Tailwind CSS 4
- Docker

## Estrutura do Projeto

```
src/
├── app/                    # Pasta principal da aplicação Next.js
│   ├── api/                # API routes
│   ├── components/         # Componentes reutilizáveis
│   ├── gerar-projeto/      # Página para geração de projetos
│   ├── sobre/              # Página sobre o projeto
│   ├── globals.css         # Estilos globais
│   ├── layout.tsx          # Layout principal
│   ├── not-found.tsx       # Página 404
│   └── page.tsx            # Página inicial
├── ...
```

## Instalação e Execução

### Utilizando Docker

```bash
# Na pasta raiz do projeto
docker-compose up frontend
```

### Desenvolvimento Local

```bash
# Instalar dependências
npm install

# Executar em modo de desenvolvimento
npm run dev
```

Acesse [http://localhost:3000](http://localhost:3000) para visualizar a aplicação.

## Integração com o Backend

O frontend se comunica com o backend através das rotas de API, configuradas em `src/app/api/`. 
As requisições são feitas para o backend em FastAPI rodando em `http://localhost:8000`.

## Variáveis de Ambiente

- `NEXT_PUBLIC_BACKEND_URL`: URL do backend (default: http://localhost:8000)

## Funcionalidades

- Página inicial com informações sobre o projeto
- Formulário para geração de projetos baseados em IA
- Exibição de resultados com estrutura, código e recursos
- Design responsivo para dispositivos móveis e desktop
