import Link from 'next/link';

export default function Sobre() {
  return (
    <div className="max-w-4xl mx-auto pt-20">
      <h1 className="text-4xl md:text-5xl font-bold mb-8 animate-slide-up bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">Sobre o CodeSprint</h1>
      
      <div className="card p-8 mb-8 animate-slide-up" style={{ animationDelay: '0.1s' }}>
        <div className="flex items-center mb-6">
          <div className="w-12 h-12 rounded-xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-600 dark:text-blue-400 mr-4">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Nossa Missão</h2>
        </div>
        <p className="mb-4 text-gray-700 dark:text-gray-300">
          O CodeSprint foi criado para ajudar desenvolvedores a iniciarem novos projetos de forma rápida e eficiente, 
          utilizando o poder da inteligência artificial para gerar estruturas de código, recomendações e guias de desenvolvimento.
        </p>
        <p className="text-gray-700 dark:text-gray-300">
          Nossa plataforma utiliza modelos avançados de IA para entender suas necessidades e gerar sugestões 
          personalizadas que se alinham com as melhores práticas de desenvolvimento.
        </p>
      </div>
      
      <div className="card p-8 mb-8 animate-slide-up" style={{ animationDelay: '0.2s' }}>
        <div className="flex items-center mb-6">
          <div className="w-12 h-12 rounded-xl bg-green-100 dark:bg-green-900/30 flex items-center justify-center text-green-600 dark:text-green-400 mr-4">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
              <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Como Funciona</h2>
        </div>
        <ol className="list-decimal pl-5 space-y-4">
          <li className="text-gray-700 dark:text-gray-300 pl-2">
            <div className="font-semibold text-gray-900 dark:text-white mb-1">Descreva seu projeto</div>
            <p>Informe as áreas de interesse, tecnologias preferidas e uma descrição 
            detalhada do que você deseja construir.</p>
          </li>
          <li className="text-gray-700 dark:text-gray-300 pl-2">
            <div className="font-semibold text-gray-900 dark:text-white mb-1">Processamento por IA</div>
            <p>Nossa inteligência artificial analisa sua descrição e gera um plano 
            completo para seu projeto.</p>
          </li>
          <li className="text-gray-700 dark:text-gray-300 pl-2">
            <div className="font-semibold text-gray-900 dark:text-white mb-1">Obtenha resultados personalizados</div>
            <p>Receba uma estrutura de projeto, exemplos de código 
            e recursos adicionais para começar a desenvolver imediatamente.</p>
          </li>
        </ol>
      </div>
      
      <div className="card p-8 animate-slide-up" style={{ animationDelay: '0.3s' }}>
        <div className="flex items-center mb-6">
          <div className="w-12 h-12 rounded-xl bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center text-purple-600 dark:text-purple-400 mr-4">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
              <path strokeLinecap="round" strokeLinejoin="round" d="M6.429 9.75L2.25 12l4.179 2.25m0-4.5l5.571 3 5.571-3m-11.142 0L2.25 7.5 12 2.25l9.75 5.25-4.179 2.25m0 0L21.75 12l-4.179 2.25m0 0l4.179 2.25L12 21.75 2.25 16.5l4.179-2.25m11.142 0l-5.571 3-5.571-3" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Tecnologias Utilizadas</h2>
        </div>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="group p-4 rounded-xl bg-blue-50 dark:bg-blue-900/20 border border-blue-100 dark:border-blue-800 transition-all hover:shadow-md hover:shadow-blue-500/10 hover:-translate-y-1">
            <h3 className="font-semibold text-xl mb-3 text-blue-700 dark:text-blue-400">Frontend</h3>
            <ul className="list-disc pl-5 space-y-1 text-gray-700 dark:text-gray-300">
              <li>Next.js</li>
              <li>React</li>
              <li>Tailwind CSS</li>
              <li>TypeScript</li>
            </ul>
          </div>
          <div className="group p-4 rounded-xl bg-green-50 dark:bg-green-900/20 border border-green-100 dark:border-green-800 transition-all hover:shadow-md hover:shadow-green-500/10 hover:-translate-y-1">
            <h3 className="font-semibold text-xl mb-3 text-green-700 dark:text-green-400">Backend</h3>
            <ul className="list-disc pl-5 space-y-1 text-gray-700 dark:text-gray-300">
              <li>FastAPI</li>
              <li>Python</li>
              <li>Redis</li>
              <li>CrewAI</li>
            </ul>
          </div>
        </div>
      </div>
      
      <div className="mt-12 text-center animate-slide-up" style={{ animationDelay: '0.4s' }}>
        <Link 
          href="/gerar-projeto" 
          className="inline-flex items-center btn btn-primary py-3 px-8 rounded-full text-lg transition-all duration-300 hover:-translate-y-1"
        >
          <span className="mr-2">Experimentar Agora</span>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
            <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
          </svg>
        </Link>
      </div>
    </div>
  );
} 