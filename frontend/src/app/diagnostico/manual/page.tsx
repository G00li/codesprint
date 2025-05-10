'use client';

import { useState } from 'react';

interface ApiResponse {
  url?: string;
  status?: number;
  statusCode?: number;
  statusText?: string;
  responseTime?: string;
  headers?: Record<string, string>;
  body?: unknown;
  error?: string;
  message?: string;
  type?: string;
  details?: string;
  stack?: string;
}

interface ErrorDetails {
  message: string;
  details?: string;
  stack?: string;
}

interface BackendTestResult {
  url: string;
  success: boolean;
  status?: number;
  statusText?: string;
  responseTime?: string;
  data?: Record<string, unknown>;
  error?: string;
}

interface BackendTestResponse {
  backendUrl?: string;
  testTime?: string;
  results?: BackendTestResult[];
  error?: string;
  details?: string;
}

export default function ManualDiagnostico() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ApiResponse | null>(null);
  const [error, setError] = useState<ErrorDetails | null>(null);
  const [url, setUrl] = useState('http://backend:8000/health');
  const [backendTest, setBackendTest] = useState<BackendTestResponse | null>(null);
  const [backendTestLoading, setBackendTestLoading] = useState(false);

  const testConnection = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      console.log(`Testando URL: ${url}`);
      const response = await fetch('/api/diagnose-manual', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });
      
      const data = await response.json();
      console.log('Resposta recebida:', data);
      
      if (!response.ok) {
        throw new Error(data.error || data.message || `Erro ${response.status}`);
      }
      
      setResult(data);
    } catch (err) {
      console.error('Erro ao testar conexão:', err);
      
      if (err instanceof Error) {
        setError({
          message: err.message,
          details: err.cause as string
        });
      } else {
        setError({
          message: 'Erro desconhecido ao testar conexão'
        });
      }
    } finally {
      setLoading(false);
    }
  };

  const testBackend = async () => {
    setBackendTestLoading(true);
    setBackendTest(null);
    
    try {
      console.log('Iniciando teste rápido do backend');
      const response = await fetch('/api/teste-rapido');
      const data = await response.json();
      console.log('Resultado do teste rápido:', data);
      setBackendTest(data);
    } catch (err) {
      console.error('Erro no teste rápido:', err);
      setBackendTest({ error: err instanceof Error ? err.message : 'Erro desconhecido' });
    } finally {
      setBackendTestLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto pt-24 px-4 sm:px-6">
      <h1 className="text-4xl font-bold mb-2 text-center">Diagnóstico Manual</h1>
      <p className="text-center text-gray-600 mb-8">
        Use esta ferramenta para testar a conectividade com endpoints específicos.
      </p>
      
      <div className="mb-4 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-lg font-medium text-blue-800 dark:text-blue-300">Teste Rápido de Conectividade</h3>
            <p className="text-sm text-blue-600 dark:text-blue-400">
              Verifica rapidamente a conectividade com todos os serviços
            </p>
          </div>
          <button
            onClick={testBackend}
            disabled={backendTestLoading}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors disabled:opacity-50 text-sm"
          >
            {backendTestLoading ? 'Testando...' : 'Testar Conectividade'}
          </button>
        </div>
        
        {backendTest && (
          <div className="mt-4">
            {backendTest.error ? (
              <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md">
                <p className="text-red-700 dark:text-red-400">{backendTest.error}</p>
                {backendTest.details && (
                  <p className="text-red-600 dark:text-red-400 text-sm mt-1">{backendTest.details}</p>
                )}
              </div>
            ) : (
              <div className="text-sm">
                <p className="mb-2"><strong>URL do backend configurada:</strong> {backendTest.backendUrl}</p>
                <p className="mb-2"><strong>Tempo total do teste:</strong> {backendTest.testTime}</p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                  {backendTest.results?.map((result: BackendTestResult, index: number) => (
                    <div 
                      key={index} 
                      className={`p-3 rounded-md ${
                        result.success 
                          ? 'bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800' 
                          : 'bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800'
                      }`}
                    >
                      <p className="font-medium text-sm mb-1 break-all">{result.url}</p>
                      {result.success ? (
                        <>
                          <p className="text-green-700 dark:text-green-400 text-xs">
                            ✅ Status: {result.status} {result.statusText}
                          </p>
                          <p className="text-green-600 dark:text-green-400 text-xs">
                            Tempo: {result.responseTime}
                          </p>
                          {result.data && (
                            <pre className="text-xs mt-1 bg-white dark:bg-gray-800 p-1 rounded">
                              {JSON.stringify(result.data, null, 2)}
                            </pre>
                          )}
                        </>
                      ) : (
                        <p className="text-red-700 dark:text-red-400 text-xs">
                          ❌ Erro: {result.error}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
      
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow p-6 mb-8">
        <div className="mb-6">
          <label htmlFor="url" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            URL para testar
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              id="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="flex-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
              placeholder="https://exemplo.com/api/endpoint"
            />
            <button
              onClick={testConnection}
              disabled={loading}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors disabled:opacity-50"
            >
              {loading ? 'Testando...' : 'Testar'}
            </button>
          </div>
        </div>
        
        <div className="space-y-4 mt-4">
          <h2 className="text-lg font-medium">Endpoints comuns para testar:</h2>
          <ul className="list-disc pl-5 space-y-2 text-sm">
            <li>Backend: <code className="bg-gray-100 dark:bg-gray-800 px-1 py-0.5 rounded">http://backend:8000/health</code></li>
            <li>Diagnóstico backend-crewai: <code className="bg-gray-100 dark:bg-gray-800 px-1 py-0.5 rounded">http://backend:8000/diagnose-crewai</code></li>
            <li>Diagnóstico de rede: <code className="bg-gray-100 dark:bg-gray-800 px-1 py-0.5 rounded">http://backend:8000/diagnose-network</code></li>
            <li>CrewAI: <code className="bg-gray-100 dark:bg-gray-800 px-1 py-0.5 rounded">http://crewai:8004/health</code></li>
            <li>Ollama: <code className="bg-gray-100 dark:bg-gray-800 px-1 py-0.5 rounded">http://ollama:11434/api/version</code></li>
            <li>DB: <code className="bg-gray-100 dark:bg-gray-800 px-1 py-0.5 rounded">http://backend:8000/api/health/db</code></li>
          </ul>
          <p className="text-xs text-gray-500 mt-2">
            Nota: Use os nomes dos serviços Docker (backend, crewai, ollama) em vez de localhost 
            quando estiver rodando em contêineres.
          </p>
        </div>
        
        {error && (
          <div className="mt-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md">
            <p className="text-red-700 dark:text-red-400 font-medium">{error.message}</p>
            {error.details && (
              <p className="text-red-600 dark:text-red-400 text-sm mt-2">{error.details}</p>
            )}
            <p className="text-xs text-gray-500 mt-4">
              Tente usar um endpoint diferente ou verificar se o serviço está em execução.
              Se o problema persistir, veja se a URL do backend está correta no arquivo de ambiente.
            </p>
          </div>
        )}
        
        {result && (
          <div className="mt-6">
            <h3 className="text-lg font-medium mb-2">Resultado:</h3>
            <div className="bg-gray-50 dark:bg-gray-900 p-4 rounded-md overflow-x-auto">
              <div className="mb-2 pb-2 border-b border-gray-200 dark:border-gray-700">
                <p><strong>URL:</strong> {result.url}</p>
                <p><strong>Status:</strong> {result.status} {result.statusText}</p>
                <p><strong>Tempo de resposta:</strong> {result.responseTime}</p>
              </div>
              <p className="text-sm font-medium mb-1 mt-2">Resposta:</p>
              <pre className="text-sm">{JSON.stringify(result.body, null, 2)}</pre>
            </div>
          </div>
        )}
      </div>
      
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow p-6">
        <h2 className="text-xl font-medium mb-4">Possíveis problemas e soluções</h2>
        
        <div className="space-y-4">
          <div>
            <h3 className="font-medium">Erro de conexão recusada</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm mt-1">
              Isso indica que o serviço não está rodando ou está inacessível.
              Verifique se os contêineres estão em execução com <code className="bg-gray-100 dark:bg-gray-800 px-1 py-0.5 rounded">docker-compose ps</code>
            </p>
          </div>
          
          <div>
            <h3 className="font-medium">Timeout de conexão</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm mt-1">
              O serviço pode estar em execução, mas lento demais para responder.
              Verifique os logs com <code className="bg-gray-100 dark:bg-gray-800 px-1 py-0.5 rounded">docker-compose logs nome-do-serviço</code>
            </p>
          </div>
          
          <div>
            <h3 className="font-medium">Erro 404 (Not Found)</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm mt-1">
              O endpoint não existe. Verifique se o caminho está correto.
            </p>
          </div>
          
          <div>
            <h3 className="font-medium">Erro 500 (Internal Server Error)</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm mt-1">
              O serviço está em execução mas ocorreu um erro interno.
              Verifique os logs para mais detalhes.
            </p>
          </div>
          
          <div>
            <h3 className="font-medium">Erro com o nome dos serviços</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm mt-1">
              Se estiver usando os nomes como <code>backend</code>, <code>crewai</code>, mas não consegue acessá-los,
              tente usar <code>http://localhost:8000</code> em vez disso, ou execute o script <code>./fix_connection.sh</code> 
              na raiz do projeto para corrigir as configurações de URL.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
} 