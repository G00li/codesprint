import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    console.log("Iniciando diagnóstico manual");
    
    // Extrai a URL do corpo da requisição
    const body = await request.json();
    let { url } = body;
    
    if (!url) {
      console.error("URL não fornecida");
      return NextResponse.json(
        { error: 'URL não fornecida' },
        { status: 400 }
      );
    }
    
    // Se a URL começa com /api, estamos tentando acessar um endpoint da API backend
    if (url.startsWith('/') && !url.startsWith('http')) {
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://backend:8000';
      url = `${backendUrl}${url}`;
      console.log(`URL convertida de caminho relativo para: ${url}`);
    }
    
    // Se a URL contém localhost:8000, substitua pelo nome do serviço Docker
    if (url.includes('localhost:8000')) {
      const originalUrl = url;
      url = url.replace('localhost:8000', 'backend:8000');
      console.log(`URL convertida de ${originalUrl} para ${url}`);
    }
    
    console.log(`Testando conectividade com: ${url}`);
    
    try {
      // Registra o momento de início
      const startTime = Date.now();
      
      // Tenta fazer a requisição com um timeout de 10 segundos
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000);
      
      console.log(`Iniciando fetch para: ${url}`);
      const response = await fetch(url, { 
        signal: controller.signal,
        cache: 'no-store'
      });
      
      // Limpa o timeout
      clearTimeout(timeoutId);
      
      // Calcula o tempo de resposta
      const responseTime = Date.now() - startTime;
      console.log(`Resposta recebida em ${responseTime}ms com status: ${response.status}`);
      
      // Tenta extrair o corpo da resposta como JSON
      let responseBody;
      const contentType = response.headers.get('content-type');
      
      if (contentType?.includes('application/json')) {
        responseBody = await response.json();
        console.log('Resposta JSON recebida');
      } else {
        responseBody = await response.text();
        console.log(`Resposta texto recebida (${responseBody.length} bytes)`);
        
        // Se o corpo parece ser JSON (mesmo que Content-Type não seja), tenta parsear
        if (responseBody.startsWith('{') || responseBody.startsWith('[')) {
          try {
            responseBody = JSON.parse(responseBody);
            console.log('Texto convertido para JSON com sucesso');
          } catch {
            // Mantém como texto se não conseguir parsear
            console.log('Falha ao converter texto para JSON');
          }
        }
        
        // Limita o tamanho do texto para não sobrecarregar a resposta
        if (typeof responseBody === 'string' && responseBody.length > 500) {
          responseBody = responseBody.substring(0, 500) + '... (truncado)';
          console.log('Resposta texto truncada por ser muito grande');
        }
      }
      
      // Prepara o resultado
      const result = {
        url,
        status: response.status,
        statusText: response.statusText,
        responseTime: `${responseTime}ms`,
        headers: Object.fromEntries(response.headers.entries()),
        body: responseBody
      };
      
      console.log('Resposta preparada com sucesso');
      
      // Retorna informações sobre a resposta
      return NextResponse.json(result);
      
    } catch (error) {
      // Captura erros específicos
      if (error instanceof Error) {
        console.error(`Erro ao conectar com ${url}: ${error.message}`);
        
        if (error.name === 'AbortError') {
          return NextResponse.json(
            { 
              url,
              error: 'Timeout de conexão (10s)', 
              type: 'timeout',
              message: 'A requisição excedeu o limite de tempo de 10 segundos'
            },
            { status: 504 }
          );
        } else if (error.message.includes('ECONNREFUSED')) {
          return NextResponse.json(
            { 
              url,
              error: 'Conexão recusada', 
              type: 'connection_refused',
              message: 'O servidor recusou a conexão. Verifique se o serviço está em execução e acessível.'
            },
            { status: 502 }
          );
        } else {
          return NextResponse.json(
            { 
              url,
              error: `Erro ao conectar: ${error.message}`, 
              type: 'connection_error',
              message: error.message
            },
            { status: 500 }
          );
        }
      } else {
        console.error(`Erro desconhecido ao conectar com ${url}`);
        return NextResponse.json(
          { 
            url,
            error: 'Erro desconhecido ao conectar', 
            type: 'unknown_error'
          },
          { status: 500 }
        );
      }
    }
    
  } catch (error) {
    console.error('Erro ao processar requisição:', error);
    
    // Retorna um erro genérico com detalhes, se disponíveis
    return NextResponse.json(
      { 
        error: 'Erro ao processar requisição', 
        details: error instanceof Error ? error.message : 'Erro desconhecido',
        stack: error instanceof Error ? error.stack : undefined
      },
      { status: 500 }
    );
  }
} 