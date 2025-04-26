import { NextResponse } from 'next/server';

export async function GET() {
  try {
    console.log("Iniciando teste de conectividade com o backend");
    
    // Obtém a URL do backend da variável de ambiente ou usa o valor padrão
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://backend:8000';
    console.log(`URL do backend configurada: ${backendUrl}`);
    
    // URLs para testar
    const urls = [
      `${backendUrl}/health`,
      'http://backend:8000/health',
      'http://localhost:8000/health'
    ];
    
    const results = [];
    
    // Testa cada URL
    for (const url of urls) {
      try {
        console.log(`Testando URL: ${url}`);
        const startTime = Date.now();
        
        const response = await fetch(url, { 
          method: 'GET',
          cache: 'no-store',
          headers: {
            'Accept': 'application/json'
          },
          // Timeout curto para não bloquear muito tempo
          signal: AbortSignal.timeout(3000)
        });
        
        const responseTime = Date.now() - startTime;
        
        let responseData;
        try {
          responseData = await response.json();
        } catch {
          responseData = { error: 'Não foi possível obter JSON da resposta' };
        }
        
        results.push({
          url,
          success: response.ok,
          status: response.status,
          statusText: response.statusText,
          responseTime: `${responseTime}ms`,
          data: responseData
        });
        
        console.log(`URL ${url} testada com sucesso: ${response.status}`);
      } catch (error) {
        console.error(`Erro ao testar ${url}:`, error);
        
        results.push({
          url,
          success: false,
          error: error instanceof Error ? error.message : 'Erro desconhecido'
        });
      }
    }
    
    return NextResponse.json({
      backendUrl,
      testTime: new Date().toISOString(),
      results
    });
    
  } catch (error) {
    console.error('Erro ao executar o teste de backend:', error);
    
    return NextResponse.json({
      error: 'Erro ao executar o teste de backend',
      details: error instanceof Error ? error.message : 'Erro desconhecido',
      stack: error instanceof Error ? error.stack : undefined
    }, { status: 500 });
  }
} 