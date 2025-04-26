'use client';

import { useState } from 'react';

interface ResultadoDados {
  resumo?: string;
  tecnologias?: string;
  areas?: string[];
  estrutura?: string;
  codigo?: string;
  recursos?: string[];
}

interface ResultadoProjetoProps {
  resultado: {
    resultado?: ResultadoDados;
    error?: string;
    details?: string;
  } | ResultadoDados;
  onNovoClick: () => void;
}

export default function ResultadoProjeto({ resultado, onNovoClick }: ResultadoProjetoProps) {
  const [activeTab, setActiveTab] = useState('resumo');
  
  // Verifica se o resultado é válido
  if (!resultado) {
    return null;
  }
  
  // Extrai os dados do resultado (considerando ambos os formatos possíveis)
  const dados: ResultadoDados = 'resultado' in resultado && resultado.resultado 
    ? resultado.resultado 
    : resultado as ResultadoDados;
  
  return (
    <div className="card p-8 shadow-lg transition-all duration-300 animate-slide-up">
      <div className="mb-8 text-center">
        <div className="inline-block p-3 bg-green-100 dark:bg-green-900/30 rounded-full mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h2 className="text-2xl md:text-3xl font-bold mb-2 text-gray-900 dark:text-white">
          Projeto Gerado com Sucesso
        </h2>
        <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          Seu projeto foi gerado com base nos parâmetros fornecidos. Explore as diferentes seções abaixo.
        </p>
      </div>
      
      {/* Tabs para navegação */}
      <div className="flex flex-wrap border-b mb-6 overflow-x-auto">
        <button
          className={`px-4 py-3 font-medium text-sm transition-all duration-200 border-b-2 ${
            activeTab === 'resumo'
              ? 'border-blue-500 text-blue-600 dark:text-blue-400'
              : 'border-transparent text-gray-500 hover:text-blue-500 dark:text-gray-400 dark:hover:text-blue-400'
          }`}
          onClick={() => setActiveTab('resumo')}
        >
          <div className="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Resumo
          </div>
        </button>
        <button
          className={`px-4 py-3 font-medium text-sm transition-all duration-200 border-b-2 ${
            activeTab === 'estrutura'
              ? 'border-green-500 text-green-600 dark:text-green-400'
              : 'border-transparent text-gray-500 hover:text-green-500 dark:text-gray-400 dark:hover:text-green-400'
          }`}
          onClick={() => setActiveTab('estrutura')}
        >
          <div className="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
            </svg>
            Estrutura
          </div>
        </button>
        <button
          className={`px-4 py-3 font-medium text-sm transition-all duration-200 border-b-2 ${
            activeTab === 'codigo'
              ? 'border-purple-500 text-purple-600 dark:text-purple-400'
              : 'border-transparent text-gray-500 hover:text-purple-500 dark:text-gray-400 dark:hover:text-purple-400'
          }`}
          onClick={() => setActiveTab('codigo')}
        >
          <div className="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
            </svg>
            Código
          </div>
        </button>
        <button
          className={`px-4 py-3 font-medium text-sm transition-all duration-200 border-b-2 ${
            activeTab === 'recursos'
              ? 'border-amber-500 text-amber-600 dark:text-amber-400'
              : 'border-transparent text-gray-500 hover:text-amber-500 dark:text-gray-400 dark:hover:text-amber-400'
          }`}
          onClick={() => setActiveTab('recursos')}
        >
          <div className="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            Recursos
          </div>
        </button>
      </div>
      
      {/* Conteúdo das tabs */}
      <div className="relative overflow-hidden transition-all duration-500">
        {/* Tab Resumo */}
        <div 
          className={`transform transition-all duration-500 ${
            activeTab === 'resumo' ? 'opacity-100 translate-x-0' : 'opacity-0 absolute -translate-x-full'
          }`}
        >
          <div className="bg-gray-50 dark:bg-gray-800/50 p-6 rounded-lg">
            <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Resumo do Projeto</h3>
            <div className="prose dark:prose-invert max-w-none mb-6">
              <p className="text-gray-700 dark:text-gray-300">
                {dados.resumo || JSON.stringify(dados, null, 2)}
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
              <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-100 dark:border-blue-800">
                <h4 className="font-semibold text-blue-800 dark:text-blue-400 mb-2 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                  </svg>
                  Tecnologias
                </h4>
                <p className="text-gray-700 dark:text-gray-300">{dados.tecnologias || "Não especificado"}</p>
              </div>
              <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-100 dark:border-green-800">
                <h4 className="font-semibold text-green-800 dark:text-green-400 mb-2 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
                  </svg>
                  Áreas
                </h4>
                <p className="text-gray-700 dark:text-gray-300">{Array.isArray(dados.areas) ? dados.areas.join(", ") : "Não especificado"}</p>
              </div>
            </div>
          </div>
        </div>
        
        {/* Tab Estrutura */}
        <div 
          className={`transform transition-all duration-500 ${
            activeTab === 'estrutura' ? 'opacity-100 translate-x-0' : 'opacity-0 absolute -translate-x-full'
          }`}
        >
          <div className="bg-gray-50 dark:bg-gray-800/50 p-6 rounded-lg">
            <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
              </svg>
              Estrutura do Projeto
            </h3>
            <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm font-mono leading-relaxed">
              {dados.estrutura || "Estrutura não disponível"}
            </pre>
          </div>
        </div>
        
        {/* Tab Código */}
        <div 
          className={`transform transition-all duration-500 ${
            activeTab === 'codigo' ? 'opacity-100 translate-x-0' : 'opacity-0 absolute -translate-x-full'
          }`}
        >
          <div className="bg-gray-50 dark:bg-gray-800/50 p-6 rounded-lg">
            <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-purple-600 dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
              </svg>
              Exemplos de Código
            </h3>
            <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm font-mono leading-relaxed">
              {dados.codigo || "Código não disponível"}
            </pre>
          </div>
        </div>
        
        {/* Tab Recursos */}
        <div 
          className={`transform transition-all duration-500 ${
            activeTab === 'recursos' ? 'opacity-100 translate-x-0' : 'opacity-0 absolute -translate-x-full'
          }`}
        >
          <div className="bg-gray-50 dark:bg-gray-800/50 p-6 rounded-lg">
            <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-amber-600 dark:text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
              Recursos Adicionais
            </h3>
            <ul className="space-y-3">
              {dados.recursos && Array.isArray(dados.recursos) ? (
                dados.recursos.map((recurso: string, index: number) => (
                  <li key={index} className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700 flex items-start">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-3 text-amber-500 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    <span className="text-gray-700 dark:text-gray-300">{recurso}</span>
                  </li>
                ))
              ) : (
                <li className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
                  <span className="text-gray-700 dark:text-gray-300">Nenhum recurso adicional disponível</span>
                </li>
              )}
            </ul>
          </div>
        </div>
      </div>
      
      {/* Botão para gerar novo projeto */}
      <div className="mt-10 text-center">
        <button
          onClick={onNovoClick}
          className="group relative inline-flex items-center justify-center px-8 py-3 overflow-hidden font-bold rounded-full bg-gradient-to-br from-blue-600 to-indigo-600 text-white shadow-md transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/30 transform hover:-translate-y-1"
        >
          <span className="absolute top-0 left-0 w-full h-full bg-white/10 transform -translate-x-full group-hover:translate-x-0 transition-transform duration-700"></span>
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Gerar Novo Projeto
        </button>
      </div>
    </div>
  );
} 