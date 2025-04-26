'use client';

import { useState } from 'react';
import ResultadoProjeto from '../components/ResultadoProjeto';

// Interface para os dados do formulário
interface FormData {
  areas: string[];
  tecnologias: string;
  descricao: string;
  usar_exa: boolean;
}

// Interface para a resposta da API
interface ProjetoResponse {
  resultado?: {
    resumo?: string;
    tecnologias?: string;
    areas?: string[];
    estrutura?: string;
    codigo?: string;
    recursos?: string[];
  };
  error?: string;
  details?: string;
}

export default function GerarProjeto() {
  // Lista de áreas disponíveis
  const areasDisponiveis = [
    'Web', 'Mobile', 'Desktop', 'API',
    'Inteligência Artificial', 'Machine Learning',
    'Jogos', 'IoT', 'Blockchain', 'Segurança'
  ];
  
  // Estado inicial do formulário
  const [formData, setFormData] = useState<FormData>({
    areas: [],
    tecnologias: '',
    descricao: '',
    usar_exa: false
  });
  
  // Estados para controlar o loading e resultado
  const [isLoading, setIsLoading] = useState(false);
  const [resultado, setResultado] = useState<ProjetoResponse | null>(null);
  const [erro, setErro] = useState<string | null>(null);
  
  // Lidar com mudanças nas áreas selecionadas
  const handleAreaChange = (area: string) => {
    if (formData.areas.includes(area)) {
      setFormData({
        ...formData,
        areas: formData.areas.filter(a => a !== area)
      });
    } else {
      setFormData({
        ...formData,
        areas: [...formData.areas, area]
      });
    }
  };
  
  // Lidar com mudanças nos campos de texto
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target as HTMLInputElement;
    
    if (type === 'checkbox') {
      const { checked } = e.target as HTMLInputElement;
      setFormData({
        ...formData,
        [name]: checked
      });
    } else {
      setFormData({
        ...formData,
        [name]: value
      });
    }
  };
  
  // Limpar o formulário e começar um novo projeto
  const handleNovoClick = () => {
    setResultado(null);
    setErro(null);
    setFormData({
      areas: [],
      tecnologias: '',
      descricao: '',
      usar_exa: false
    });
  };
  
  // Enviar formulário
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validação básica
    if (formData.areas.length === 0) {
      setErro('Selecione pelo menos uma área');
      return;
    }
    
    if (!formData.tecnologias.trim()) {
      setErro('Informe as tecnologias desejadas');
      return;
    }
    
    if (!formData.descricao.trim()) {
      setErro('Descreva seu projeto');
      return;
    }
    
    // Limpa erros anteriores
    setErro(null);
    setIsLoading(true);
    
    try {
      const response = await fetch('/api/gerar-projeto', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Ocorreu um erro ao gerar o projeto');
      }
      
      setResultado(data);
    } catch (error) {
      if (error instanceof Error) {
        setErro(error.message);
      } else {
        setErro('Ocorreu um erro desconhecido');
      }
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="max-w-4xl mx-auto pt-24 px-4 sm:px-6">
      <div className="animate-slide-up">
        <h1 className="text-4xl font-bold mb-2 text-center bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
          Gerador de Projetos
        </h1>
        <p className="text-center text-gray-600 dark:text-gray-400 mb-8 max-w-xl mx-auto">
          Descreva seu projeto e deixe nossa inteligência artificial criar um plano de desenvolvimento personalizado para você.
        </p>
      </div>
      
      {erro && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-lg mb-6 animate-slide-up shadow-sm">
          <div className="flex">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <p>{erro}</p>
          </div>
        </div>
      )}
      
      {resultado ? (
        <ResultadoProjeto 
          resultado={resultado} 
          onNovoClick={handleNovoClick} 
        />
      ) : (
        <form onSubmit={handleSubmit} className="card p-8 transition-all duration-300 animate-slide-up">
          <div className="mb-8">
            <label className="block text-gray-700 dark:text-gray-300 text-sm font-bold mb-3">
              Áreas do Projeto
            </label>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {areasDisponiveis.map((area) => (
                <div key={area} className="flex items-center">
                  <input
                    type="checkbox"
                    id={`area-${area}`}
                    checked={formData.areas.includes(area)}
                    onChange={() => handleAreaChange(area)}
                    className="sr-only peer"
                  />
                  <label 
                    htmlFor={`area-${area}`} 
                    className={`
                      cursor-pointer border rounded-full py-2 px-3 w-full text-sm text-center transition-all duration-200
                      ${formData.areas.includes(area) 
                        ? 'bg-blue-100 border-blue-300 text-blue-800 dark:bg-blue-900/30 dark:border-blue-700 dark:text-blue-300' 
                        : 'bg-gray-50 border-gray-200 text-gray-700 hover:bg-gray-100 dark:bg-gray-800/50 dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-800'
                      }
                    `}
                  >
                    {area}
                  </label>
                </div>
              ))}
            </div>
          </div>
          
          <div className="mb-6">
            <label htmlFor="tecnologias" className="block text-gray-700 dark:text-gray-300 text-sm font-bold mb-2">
              Tecnologias
            </label>
            <input
              type="text"
              id="tecnologias"
              name="tecnologias"
              value={formData.tecnologias}
              onChange={handleInputChange}
              placeholder="Ex: React, Node.js, MongoDB"
              className="shadow appearance-none border rounded-lg w-full py-3 px-4 text-gray-700 dark:text-gray-300 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500/50 bg-white dark:bg-gray-800/50 dark:border-gray-700"
            />
            <p className="text-gray-500 dark:text-gray-400 text-xs mt-1">
              Separe as tecnologias por vírgulas
            </p>
          </div>
          
          <div className="mb-8">
            <label htmlFor="descricao" className="block text-gray-700 dark:text-gray-300 text-sm font-bold mb-2">
              Descrição do Projeto
            </label>
            <textarea
              id="descricao"
              name="descricao"
              value={formData.descricao}
              onChange={handleInputChange}
              placeholder="Descreva seu projeto em detalhes..."
              rows={6}
              className="shadow appearance-none border rounded-lg w-full py-3 px-4 text-gray-700 dark:text-gray-300 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500/50 bg-white dark:bg-gray-800/50 dark:border-gray-700"
            />
            <p className="text-gray-500 dark:text-gray-400 text-xs mt-1">
              Quanto mais detalhes você fornecer, melhor será o resultado gerado
            </p>
          </div>
          
          <div className="mb-8">
            <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4 border border-blue-100 dark:border-blue-800">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="usar_exa"
                  name="usar_exa"
                  checked={formData.usar_exa}
                  onChange={handleInputChange}
                  className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <label htmlFor="usar_exa" className="ml-2 block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Usar EXA.ai para enriquecer a descrição
                </label>
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                A EXA.ai buscará informações adicionais na internet para melhorar os resultados do seu projeto
              </p>
            </div>
          </div>
          
          <div className="flex items-center justify-center">
            <button
              type="submit"
              disabled={isLoading}
              className={`
                relative overflow-hidden group bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 
                text-white font-bold py-3 px-8 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 
                shadow-lg hover:shadow-blue-500/30 transition-all duration-300
                ${isLoading ? 'opacity-80 cursor-not-allowed' : 'transform hover:-translate-y-1'}
              `}
            >
              {isLoading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Gerando...
                </>
              ) : (
                <>
                  <span className="absolute top-0 left-0 w-full h-full bg-white/10 transform -translate-x-full group-hover:translate-x-0 transition-transform duration-700"></span>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 inline-block mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  Gerar Projeto
                </>
              )}
            </button>
          </div>
        </form>
      )}
    </div>
  );
} 