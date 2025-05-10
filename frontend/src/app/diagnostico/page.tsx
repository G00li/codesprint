'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface TestData {
  name: string;
  status: string;
  statusCode?: number;
  data?: Record<string, unknown>;
  error?: string;
  summary?: string;
}

interface DiagnosticoData {
  config: {
    backendUrl: string;
    nodeEnv: string;
  };
  tests: TestData[];
}

export default function DiagnosticoPage() {
  const [diagnostico, setDiagnostico] = useState<DiagnosticoData | null>(null);
  const [dbStatus, setDbStatus] = useState<TestData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const runDiagnostico = async () => {
      try {
        setLoading(true);
        const [diagnosticoResponse, dbResponse] = await Promise.all([
          fetch('/api/diagnostico'),
          fetch('/api/health/db')
        ]);

        if (!diagnosticoResponse.ok) {
          throw new Error(`Erro ao executar diagnóstico: ${diagnosticoResponse.status}`);
        }

        const diagnosticoData = await diagnosticoResponse.json();
        setDiagnostico(diagnosticoData);

        // Processar status do banco de dados
        const dbData = await dbResponse.json();
        setDbStatus({
          name: 'Banco de Dados',
          status: dbResponse.ok ? 'success' : 'error',
          statusCode: dbResponse.status,
          data: dbData,
          summary: dbResponse.ok ? 'Conexão com o banco de dados estabelecida com sucesso' : 'Falha na conexão com o banco de dados'
        });

      } catch (err) {
        setError(err instanceof Error ? err.message : 'Erro desconhecido');
      } finally {
        setLoading(false);
      }
    };

    runDiagnostico();
  }, []);

  const executeTest = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch('/api/gerar-projeto', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          areas: ['Web', 'API'],
          tecnologias: 'Python, FastAPI, React, TailwindCSS',
          descricao: 'Um sistema simples de teste para diagnóstico',
          usar_exa: false
        })
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `Erro ${response.status}`);
      }
      
      const data = await response.json();
      alert('Teste executado com sucesso! Verifique o console para detalhes.');
      console.log('Resposta do teste:', data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto pt-24 px-4 sm:px-6">
      <h1 className="text-4xl font-bold mb-2 text-center">Diagnóstico do Sistema</h1>
      
      <div className="flex justify-center mb-6">
        <Link 
          href="/diagnostico/manual" 
          className="px-4 py-2 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 rounded-md transition-colors text-sm"
        >
          Ir para Diagnóstico Manual →
        </Link>
      </div>
      
      <div className="mt-8 bg-white dark:bg-gray-800 p-6 rounded-xl shadow">
        <h2 className="text-xl font-bold mb-4">Status da Comunicação</h2>
        
        {loading ? (
          <div className="flex items-center justify-center h-40">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          </div>
        ) : error ? (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 p-4 rounded-lg">
            <p>{error}</p>
            <div className="mt-4">
              <p className="font-medium">Problemas de conectividade?</p>
              <p className="text-sm mt-1">
                Use a <Link href="/diagnostico/manual" className="text-blue-600 hover:underline">ferramenta de diagnóstico manual</Link> para verificar a conectividade com os serviços.
              </p>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-2">Configuração</h3>
              <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded">
                <p><strong>Backend URL:</strong> {diagnostico?.config?.backendUrl}</p>
                <p><strong>Ambiente:</strong> {diagnostico?.config?.nodeEnv}</p>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-2">Resultados dos Testes</h3>
              <div className="space-y-4">
                {dbStatus && (
                  <div className="border rounded-lg overflow-hidden">
                    <div className={`p-3 flex justify-between items-center ${
                      dbStatus.status === 'success' ? 'bg-green-50 dark:bg-green-900/20 text-green-800 dark:text-green-300' :
                      dbStatus.status === 'error' ? 'bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-300' :
                      'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-800 dark:text-yellow-300'
                    }`}>
                      <span className="font-medium">{dbStatus.name}</span>
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium uppercase">
                        {dbStatus.status}
                      </span>
                    </div>
                    <div className="p-3 bg-white dark:bg-gray-800">
                      {dbStatus.error ? (
                        <p className="text-red-600 dark:text-red-400">Erro: {dbStatus.error}</p>
                      ) : (
                        <div>
                          {dbStatus.statusCode && <p><strong>Status Code:</strong> {dbStatus.statusCode}</p>}
                          {dbStatus.data && (
                            <pre className="mt-2 bg-gray-50 dark:bg-gray-900 p-2 rounded overflow-x-auto text-xs">
                              {JSON.stringify(dbStatus.data, null, 2)}
                            </pre>
                          )}
                          {dbStatus.summary && <p className="mt-2">{dbStatus.summary}</p>}
                        </div>
                      )}
                    </div>
                  </div>
                )}
                
                {diagnostico?.tests?.map((test, index) => (
                  <div key={index} className="border rounded-lg overflow-hidden">
                    <div className={`p-3 flex justify-between items-center ${
                      test.status === 'success' ? 'bg-green-50 dark:bg-green-900/20 text-green-800 dark:text-green-300' :
                      test.status === 'error' ? 'bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-300' :
                      'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-800 dark:text-yellow-300'
                    }`}>
                      <span className="font-medium">{test.name}</span>
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium uppercase">
                        {test.status}
                      </span>
                    </div>
                    <div className="p-3 bg-white dark:bg-gray-800">
                      {test.error ? (
                        <p className="text-red-600 dark:text-red-400">Erro: {test.error}</p>
                      ) : (
                        <div>
                          {test.statusCode && <p><strong>Status Code:</strong> {test.statusCode}</p>}
                          {test.data && (
                            <pre className="mt-2 bg-gray-50 dark:bg-gray-900 p-2 rounded overflow-x-auto text-xs">
                              {JSON.stringify(test.data, null, 2)}
                            </pre>
                          )}
                          {test.summary && <p className="mt-2">{test.summary}</p>}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="pt-4 border-t">
              <h3 className="text-lg font-semibold mb-4">Teste Manual</h3>
              <button
                onClick={executeTest}
                disabled={loading}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors disabled:opacity-50"
              >
                {loading ? 'Executando...' : 'Testar Endpoint de Geração de Projeto'}
              </button>
              {error && (
                <div className="mt-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 p-4 rounded-lg">
                  <p>{error}</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 