import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Validação básica
    if (!body.areas || !Array.isArray(body.areas) || body.areas.length === 0) {
      return NextResponse.json({ error: 'Selecione pelo menos uma área' }, { status: 400 });
    }
    
    if (!body.tecnologias || typeof body.tecnologias !== 'string' || !body.tecnologias.trim()) {
      return NextResponse.json({ error: 'Informe as tecnologias desejadas' }, { status: 400 });
    }
    
    if (!body.descricao || typeof body.descricao !== 'string' || !body.descricao.trim()) {
      return NextResponse.json({ error: 'Descreva seu projeto' }, { status: 400 });
    }
    
    // Prepara o payload para o backend
    const payload = {
      areas: body.areas,
      tecnologias: body.tecnologias,
      descricao: body.descricao,
      usar_exa: !!body.usar_exa
    };
    
    // URL do backend configurada via variável de ambiente ou usando o nome do serviço Docker
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://backend:8000';
    const endpoint = `${backendUrl}/gerar-projeto`;
    
    console.log(`Enviando requisição para: ${endpoint}`);
    console.log('Payload:', JSON.stringify(payload));
    
    // Faz a requisição para o backend
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
      // Aumenta o timeout para dar tempo ao processamento
      signal: AbortSignal.timeout(5 * 60 * 1000) // 5 minutos
    });
    
    console.log(`Resposta do backend - Status: ${response.status}`);
    
    // Pega a resposta do backend
    const data = await response.json();
    
    console.log('Dados recebidos:', JSON.stringify(data).substring(0, 200) + '...');
    
    // Se o backend retornar um erro
    if (!response.ok) {
      console.error('Erro retornado pelo backend:', data.error || 'Erro desconhecido');
      return NextResponse.json(
        { error: data.error || 'Erro ao comunicar com o backend', details: data.details || '' },
        { status: response.status }
      );
    }
    
    // Retorna a resposta do backend
    return NextResponse.json(data);
  } catch (error) {
    console.error('Erro ao processar requisição:', error);
    
    // Para desenvolvimento, retorna um projeto dummy para testes de UI
    if (process.env.NODE_ENV === 'development' && !process.env.NEXT_PUBLIC_BACKEND_URL) {
      console.warn('Usando dados de exemplo porque o backend não está disponível');
      return NextResponse.json({
        resultado: {
          resumo: "Este é um projeto de exemplo para desenvolvimento da UI. Os dados foram gerados localmente porque não foi possível conectar ao backend.",
          tecnologias: "React, Node.js, MongoDB",
          areas: ["Web", "API"],
          estrutura: `
project/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.js
│   ├── public/
│   └── package.json
├── backend/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   └── server.js
└── README.md
          `,
          codigo: `
// Exemplo de componente React
import React, { useState, useEffect } from 'react';

function ExampleComponent() {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    fetch('/api/data')
      .then(res => res.json())
      .then(result => setData(result));
  }, []);
  
  return (
    <div>
      <h1>Exemplo</h1>
      <ul>
        {data.map(item => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
}
          `,
          recursos: [
            "React Documentation: https://reactjs.org/docs/getting-started.html",
            "Node.js Guide: https://nodejs.org/en/docs/guides/",
            "MongoDB University: https://university.mongodb.com/"
          ]
        }
      });
    }
    
    const errorMessage = error instanceof Error ? error.message : 'Erro desconhecido';
    return NextResponse.json(
      { error: 'Ocorreu um erro ao processar sua solicitação', details: errorMessage },
      { status: 500 }
    );
  }
} 