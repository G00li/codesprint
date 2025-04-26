import { NextResponse } from 'next/server';

// Definindo os tipos para resultados dos testes
interface TestResult {
  name: string;
  status: 'success' | 'error' | 'failed';
  statusCode?: number;
  data?: unknown;
  error?: string;
  summary?: string;
  details?: unknown;
}

export async function GET() {
  try {
    // Usar o nome do serviço definido no docker-compose se estiver no ambiente de contêiner
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://backend:8000';
    console.log(`Usando URL do backend: ${backendUrl}`);
    
    const results = {
      config: {
        backendUrl,
        nodeEnv: process.env.NODE_ENV
      },
      tests: [] as TestResult[]
    };
    
    // Teste 1: Verificar se o backend está respondendo
    try {
      console.log(`Testando conexão com backend em ${backendUrl}/health`);
      const healthResponse = await fetch(`${backendUrl}/health`, { 
        method: 'GET',
        cache: 'no-store'
      });
      
      const healthData = await healthResponse.json();
      results.tests.push({
        name: 'Conexão com backend',
        status: healthResponse.ok ? 'success' : 'failed',
        statusCode: healthResponse.status,
        data: healthData
      });
    } catch (error) {
      console.error(`Erro ao testar conexão com backend: ${error instanceof Error ? error.message : 'Erro desconhecido'}`);
      results.tests.push({
        name: 'Conexão com backend',
        status: 'error',
        error: error instanceof Error ? error.message : 'Erro desconhecido'
      });
    }
    
    // Teste 2: Verificar se o CrewAI está respondendo
    try {
      console.log(`Testando conexão com CrewAI via backend em ${backendUrl}/diagnose-crewai`);
      const crewaiResponse = await fetch(`${backendUrl}/diagnose-crewai`, { 
        method: 'GET',
        cache: 'no-store'
      });
      
      const crewaiData = await crewaiResponse.json();
      results.tests.push({
        name: 'Conexão com CrewAI',
        status: crewaiResponse.ok ? 'success' : 'failed',
        statusCode: crewaiResponse.status,
        data: crewaiData
      });
    } catch (error) {
      console.error(`Erro ao testar conexão com CrewAI: ${error instanceof Error ? error.message : 'Erro desconhecido'}`);
      results.tests.push({
        name: 'Conexão com CrewAI',
        status: 'error',
        error: error instanceof Error ? error.message : 'Erro desconhecido'
      });
    }
    
    // Teste 3: Verificar diagnóstico completo da rede
    try {
      console.log(`Executando diagnóstico de rede via backend em ${backendUrl}/diagnose-network`);
      const networkResponse = await fetch(`${backendUrl}/diagnose-network`, { 
        method: 'GET',
        cache: 'no-store'
      });
      
      const networkData = await networkResponse.json();
      results.tests.push({
        name: 'Diagnóstico completo de rede',
        status: networkResponse.ok ? 'success' : 'failed',
        statusCode: networkResponse.status,
        summary: 'Veja detalhes completos na resposta',
        details: networkData
      });
    } catch (error) {
      console.error(`Erro ao executar diagnóstico de rede: ${error instanceof Error ? error.message : 'Erro desconhecido'}`);
      results.tests.push({
        name: 'Diagnóstico completo de rede',
        status: 'error',
        error: error instanceof Error ? error.message : 'Erro desconhecido'
      });
    }
    
    return NextResponse.json(results);
  } catch (error) {
    console.error('Erro ao executar diagnóstico:', error);
    return NextResponse.json(
      { error: 'Ocorreu um erro ao executar o diagnóstico', 
        details: error instanceof Error ? error.message : 'Erro desconhecido' 
      },
      { status: 500 }
    );
  }
} 