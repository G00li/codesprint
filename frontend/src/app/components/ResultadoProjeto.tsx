'use client';

import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

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
  
  // Log inicial dos dados recebidos
  console.log('ResultadoProjeto - Dados recebidos:', {
    resultado,
    temResultado: 'resultado' in resultado,
    tipoResultado: typeof resultado,
    keys: Object.keys(resultado)
  });
  
  // Verifica se o resultado é válido
  if (!resultado) {
    console.warn('ResultadoProjeto - Nenhum resultado recebido');
    return null;
  }
  
  // Extrai os dados do resultado (considerando ambos os formatos possíveis)
  const dados: ResultadoDados = 'resultado' in resultado && resultado.resultado 
    ? resultado.resultado 
    : resultado as ResultadoDados;
    
  // Log dos dados processados
  console.log('ResultadoProjeto - Dados processados:', {
    resumo: dados.resumo?.substring(0, 100),
    tecnologias: dados.tecnologias,
    areas: dados.areas,
    estrutura: dados.estrutura?.substring(0, 100),
    codigo: dados.codigo?.substring(0, 100),
    recursos: dados.recursos
  });

  // Função auxiliar para formatar o texto
  const formatarTexto = (texto: string | undefined) => {
    if (!texto) {
      console.warn('ResultadoProjeto - Texto não disponível');
      return "Não disponível";
    }
    return texto.trim();
  };

  // Log quando a tab muda
  const handleTabChange = (tab: string) => {
    console.log('ResultadoProjeto - Mudando para tab:', tab);
    setActiveTab(tab);
  };

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
          onClick={() => handleTabChange('resumo')}
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
          onClick={() => handleTabChange('estrutura')}
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
            activeTab === 'recursos'
              ? 'border-amber-500 text-amber-600 dark:text-amber-400'
              : 'border-transparent text-gray-500 hover:text-amber-500 dark:text-gray-400 dark:hover:text-amber-400'
          }`}
          onClick={() => handleTabChange('recursos')}
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
              <div className="text-gray-700 dark:text-gray-300">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    h1: ({...props}) => <h1 className="text-2xl font-bold mb-4" {...props} />,
                    h2: ({...props}) => <h2 className="text-xl font-bold mb-3" {...props} />,
                    h3: ({...props}) => <h3 className="text-lg font-bold mb-2" {...props} />,
                    p: ({...props}) => <p className="mb-4" {...props} />,
                    ul: ({...props}) => <ul className="list-disc pl-6 mb-4" {...props} />,
                    ol: ({...props}) => <ol className="list-decimal pl-6 mb-4" {...props} />,
                    li: ({...props}) => <li className="mb-2" {...props} />,
                    code: ({...props}) => <code className="bg-gray-200 dark:bg-gray-700 px-1 rounded" {...props} />,
                    pre: ({...props}) => <pre className="bg-gray-200 dark:bg-gray-700 p-4 rounded-lg mb-4 overflow-x-auto" {...props} />,
                    blockquote: ({...props}) => <blockquote className="border-l-4 border-gray-300 dark:border-gray-600 pl-4 italic mb-4" {...props} />,
                    a: ({...props}) => <a className="text-blue-600 dark:text-blue-400 hover:underline" {...props} />,
                    table: ({...props}) => <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700 mb-4" {...props} />,
                    thead: ({...props}) => <thead className="bg-gray-50 dark:bg-gray-800" {...props} />,
                    tbody: ({...props}) => <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700" {...props} />,
                    tr: ({...props}) => <tr className="hover:bg-gray-50 dark:hover:bg-gray-800" {...props} />,
                    th: ({...props}) => <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider" {...props} />,
                    td: ({...props}) => <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400" {...props} />,
                  }}
                >
                  {formatarTexto(dados.resumo)}
                </ReactMarkdown>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
              <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-100 dark:border-blue-800">
                <h4 className="font-semibold text-blue-800 dark:text-blue-400 mb-2 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                  </svg>
                  Tecnologias
                </h4>
                <div className="prose dark:prose-invert max-w-none">
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                      ul: ({...props}) => <ul className="list-disc pl-6" {...props} />,
                      li: ({...props}) => <li className="text-gray-700 dark:text-gray-300" {...props} />,
                    }}
                  >
                    {formatarTexto(dados.tecnologias)}
                  </ReactMarkdown>
                </div>
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
            <div className="prose dark:prose-invert max-w-none">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  pre: ({...props}) => <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm font-mono leading-relaxed" {...props} />,
                  code: ({...props}) => <code className="bg-gray-900 text-gray-100 px-1 rounded" {...props} />,
                }}
              >
                {formatarTexto(dados.estrutura)}
              </ReactMarkdown>
            </div>
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
            <div className="prose dark:prose-invert max-w-none">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  h2: ({...props}) => <h2 className="text-xl font-bold mb-3 text-gray-900 dark:text-white" {...props} />,
                  h3: ({...props}) => <h3 className="text-lg font-bold mb-2 text-gray-900 dark:text-white" {...props} />,
                  ul: ({...props}) => <ul className="list-disc pl-6 mb-4" {...props} />,
                  li: ({...props}) => <li className="mb-2 text-gray-700 dark:text-gray-300" {...props} />,
                }}
              >
                {formatarTexto(dados.recursos?.join('\n'))}
              </ReactMarkdown>
            </div>
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