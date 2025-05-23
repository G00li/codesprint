import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col gap-12 pt-16">
      {/* Hero Section */}
      <section className="py-20 md:py-28">
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-4xl md:text-6xl font-extrabold mb-6 animate-slide-up bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
              Desenvolva projetos com a ajuda da IA
            </h1>
            <p className="text-lg md:text-xl text-gray-700 dark:text-gray-300 mb-10 max-w-3xl mx-auto animate-slide-up" style={{ animationDelay: '0.1s' }}>
              CodeSprint é uma plataforma que usa inteligência artificial para gerar e guiar o desenvolvimento de seus projetos de forma rápida e eficiente.
            </p>
            <div className="animate-slide-up" style={{ animationDelay: '0.2s' }}>
              <Link 
                href="/gerar-projeto" 
                className="btn btn-primary text-lg px-8 py-4 rounded-full shadow-lg hover:shadow-blue-500/20 transform hover:-translate-y-1"
              >
                Começar Agora
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 rounded-3xl mx-4 shadow-xl">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold mb-2 text-center">Como funciona</h2>
          <p className="text-gray-600 dark:text-gray-400 text-center mb-12 max-w-2xl mx-auto">
            Transforme sua ideia em um projeto completo em apenas três passos simples
          </p>
          <div className="grid md:grid-cols-3 gap-8 lg:gap-12">
            <div className="card p-6 transition-all animate-slide-up hover:shadow-blue-500/10" style={{ animationDelay: '0.1s' }}>
              <div className="bg-blue-100 dark:bg-blue-900/30 w-16 h-16 flex items-center justify-center rounded-2xl mb-6 text-blue-600 dark:text-blue-400">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-8 h-8">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-gray-900 dark:text-white">Descreva seu projeto</h3>
              <p className="text-gray-600 dark:text-gray-400">
                Conte-nos sobre a ideia do seu projeto, as tecnologias que gostaria de usar e as áreas que deseja explorar.
              </p>
            </div>

            <div className="card p-6 transition-all animate-slide-up hover:shadow-green-500/10" style={{ animationDelay: '0.2s' }}>
              <div className="bg-green-100 dark:bg-green-900/30 w-16 h-16 flex items-center justify-center rounded-2xl mb-6 text-green-600 dark:text-green-400">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-8 h-8">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 9.776c.112-.017.227-.026.344-.026h15.812c.117 0 .232.009.344.026m-16.5 0a2.25 2.25 0 00-1.883 2.542l.857 6a2.25 2.25 0 002.227 1.932H19.05a2.25 2.25 0 002.227-1.932l.857-6a2.25 2.25 0 00-1.883-2.542m-16.5 0V6A2.25 2.25 0 016 3.75h3.879a1.5 1.5 0 011.06.44l2.122 2.12a1.5 1.5 0 001.06.44H18A2.25 2.25 0 0120.25 9v.776" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-gray-900 dark:text-white">Nossa IA trabalha</h3>
              <p className="text-gray-600 dark:text-gray-400">
                Nossa inteligência artificial processa sua descrição e gera um plano detalhado para seu projeto em poucos minutos.
              </p>
            </div>

            <div className="card p-6 transition-all animate-slide-up hover:shadow-purple-500/10" style={{ animationDelay: '0.3s' }}>
              <div className="bg-purple-100 dark:bg-purple-900/30 w-16 h-16 flex items-center justify-center rounded-2xl mb-6 text-purple-600 dark:text-purple-400">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-8 h-8">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-gray-900 dark:text-white">Receba seu projeto</h3>
              <p className="text-gray-600 dark:text-gray-400">
                Você recebe um plano completo com estrutura, códigos e guias para iniciar seu desenvolvimento imediatamente.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold mb-2 text-center">Por que usar o CodeSprint?</h2>
          <p className="text-gray-600 dark:text-gray-400 text-center mb-12 max-w-2xl mx-auto">
            Economize tempo e recursos iniciando seu desenvolvimento com uma base sólida
          </p>
          
          <div className="grid md:grid-cols-2 gap-8 lg:gap-16">
            <div className="animate-slide-right" style={{ animationDelay: '0.1s' }}>
              <div className="space-y-8">
                <div className="flex gap-4">
                  <div className="flex-shrink-0 w-12 h-12 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-600 dark:text-blue-400">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">Economize tempo</h3>
                    <p className="text-gray-600 dark:text-gray-400">Pule a parte de configuração inicial e estruturação do projeto, poupando horas de desenvolvimento.</p>
                  </div>
                </div>
                
                <div className="flex gap-4">
                  <div className="flex-shrink-0 w-12 h-12 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center text-green-600 dark:text-green-400">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">Melhores práticas</h3>
                    <p className="text-gray-600 dark:text-gray-400">Projetos gerados seguem padrões modernos de desenvolvimento e boas práticas da indústria.</p>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="animate-slide-right" style={{ animationDelay: '0.3s' }}>
              <div className="space-y-8">
                <div className="flex gap-4">
                  <div className="flex-shrink-0 w-12 h-12 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center text-purple-600 dark:text-purple-400">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">Personalização</h3>
                    <p className="text-gray-600 dark:text-gray-400">Projetos adaptados às suas necessidades específicas, tecnologias e áreas de interesse.</p>
                  </div>
                </div>
                
                <div className="flex gap-4">
                  <div className="flex-shrink-0 w-12 h-12 rounded-full bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center text-amber-600 dark:text-amber-400">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M4.26 10.147a60.436 60.436 0 00-.491 6.347A48.627 48.627 0 0112 20.904a48.627 48.627 0 018.232-4.41 60.46 60.46 0 00-.491-6.347m-15.482 0a50.57 50.57 0 00-2.658-.813A59.905 59.905 0 0112 3.493a59.902 59.902 0 0110.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.697 50.697 0 0112 13.489a50.702 50.702 0 017.74-3.342M6.75 15a.75.75 0 100-1.5.75.75 0 000 1.5zm0 0v-3.675A55.378 55.378 0 0112 8.443m-7.007 11.55A5.981 5.981 0 006.75 15.75v-1.5" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">Aprendizado</h3>
                    <p className="text-gray-600 dark:text-gray-400">Ideal para estudantes e profissionais que desejam aprender novas tecnologias de forma prática.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-blue-600 to-indigo-700 rounded-3xl mx-4 text-white shadow-xl">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Pronto para revolucionar seus projetos?</h2>
          <p className="text-xl md:text-2xl mb-10 opacity-90 max-w-2xl mx-auto">
            Transforme suas ideias em projetos reais com ajuda da nossa inteligência artificial.
          </p>
          <Link 
            href="/gerar-projeto" 
            className="inline-block bg-white text-blue-700 hover:bg-blue-50 font-bold py-4 px-8 rounded-full text-lg shadow-lg transform transition-all hover:-translate-y-1"
          >
            Gerar Meu Projeto
          </Link>
        </div>
      </section>
    </div>
  );
}
