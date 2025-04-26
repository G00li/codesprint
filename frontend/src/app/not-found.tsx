import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center py-32 min-h-[80vh] text-center px-4">
      <div className="animate-slide-up">
        <h1 className="text-9xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600 mb-4 drop-shadow-lg">
          404
        </h1>
        <div className="w-16 h-1 bg-gradient-to-r from-blue-600 to-indigo-600 mx-auto rounded-full mb-6"></div>
        <h2 className="text-3xl font-bold mb-4 text-gray-900 dark:text-white">
          Página não encontrada
        </h2>
        <p className="text-gray-600 dark:text-gray-400 mb-10 max-w-md mx-auto">
          Oops! A página que você está procurando parece não existir ou foi movida para outro endereço.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center" style={{ animationDelay: '0.1s' }}>
          <Link 
            href="/" 
            className="btn btn-primary flex items-center justify-center py-3 px-6 rounded-full text-lg transform transition-all duration-300 hover:-translate-y-1"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 mr-2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
            </svg>
            Voltar para o Início
          </Link>
          <Link 
            href="/gerar-projeto" 
            className="btn btn-outline flex items-center justify-center py-3 px-6 rounded-full text-lg text-gray-700 dark:text-gray-300 transform transition-all duration-300 hover:-translate-y-1"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 mr-2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
            Gerar um Projeto
          </Link>
        </div>
      </div>
      
      <div className="mt-16 animate-slide-up" style={{ animationDelay: '0.2s' }}>
        <div className="flex justify-center space-x-4">
          <Link href="/" className="text-gray-500 hover:text-blue-600 transition-colors">
            Página Inicial
          </Link>
          <span className="text-gray-400">•</span>
          <Link href="/sobre" className="text-gray-500 hover:text-blue-600 transition-colors">
            Sobre
          </Link>
          <span className="text-gray-400">•</span>
          <Link href="/gerar-projeto" className="text-gray-500 hover:text-blue-600 transition-colors">
            Gerar Projeto
          </Link>
        </div>
      </div>
    </div>
  );
} 