'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';
import { usePathname } from 'next/navigation';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const pathname = usePathname();

  // Manipular evento de rolagem para mudar o estilo da navbar
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 10) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  // Verificar se o link está ativo
  const isActive = (path: string) => {
    return pathname === path;
  };

  return (
    <nav 
      className={`fixed w-full z-20 transition-all duration-300 ${
        scrolled 
          ? 'bg-white/90 dark:bg-gray-900/90 backdrop-blur-sm shadow-md py-2' 
          : 'bg-gradient-primary text-white py-4'
      }`}
    >
      <div className="container mx-auto px-4 sm:px-6">
        <div className="flex justify-between items-center">
          <div className="flex items-center">
            <Link 
              href="/" 
              className="group flex items-center font-bold text-xl"
            >
              <span className="mr-2 transition-transform group-hover:scale-110">
                ⚡
              </span>
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600 font-extrabold">
                CodeSprint
              </span>
            </Link>
          </div>
          
          {/* Menu para desktop */}
          <div className="hidden md:block">
            <div className="flex items-center space-x-1">
              <Link 
                href="/" 
                className={`px-3 py-2 rounded-md transition-all duration-200 text-sm font-medium ${
                  isActive('/') 
                    ? 'bg-blue-600 text-white' 
                    : 'hover:bg-blue-500/10 dark:hover:bg-white/10'
                }`}
              >
                Início
              </Link>
              <Link 
                href="/gerar-projeto" 
                className={`px-3 py-2 rounded-md transition-all duration-200 text-sm font-medium ${
                  isActive('/gerar-projeto') 
                    ? 'bg-blue-600 text-white' 
                    : 'hover:bg-blue-500/10 dark:hover:bg-white/10'
                }`}
              >
                Gerar Projeto
              </Link>
              <Link 
                href="/sobre" 
                className={`px-3 py-2 rounded-md transition-all duration-200 text-sm font-medium ${
                  isActive('/sobre') 
                    ? 'bg-blue-600 text-white' 
                    : 'hover:bg-blue-500/10 dark:hover:bg-white/10'
                }`}
              >
                Sobre
              </Link>
            </div>
          </div>
          
          {/* Botão de menu para mobile */}
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md hover:bg-blue-600/10 dark:hover:bg-white/10 focus:outline-none"
              aria-expanded={isOpen}
            >
              <span className="sr-only">Abrir menu principal</span>
              <svg
                className={`h-6 w-6 transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                {isOpen ? (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                ) : (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      {/* Menu mobile - com animação de deslizamento */}
      <div 
        className={`md:hidden transition-all duration-300 overflow-hidden ${
          isOpen ? 'max-h-64 opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
          <Link 
            href="/" 
            className={`block px-3 py-2 rounded-md text-base font-medium transition-colors ${
              isActive('/') 
                ? 'bg-blue-600 text-white' 
                : 'hover:bg-blue-500/10 dark:hover:bg-white/10'
            }`}
            onClick={() => setIsOpen(false)}
          >
            Início
          </Link>
          <Link 
            href="/gerar-projeto" 
            className={`block px-3 py-2 rounded-md text-base font-medium transition-colors ${
              isActive('/gerar-projeto') 
                ? 'bg-blue-600 text-white' 
                : 'hover:bg-blue-500/10 dark:hover:bg-white/10'
            }`}
            onClick={() => setIsOpen(false)}
          >
            Gerar Projeto
          </Link>
          <Link 
            href="/sobre" 
            className={`block px-3 py-2 rounded-md text-base font-medium transition-colors ${
              isActive('/sobre') 
                ? 'bg-blue-600 text-white' 
                : 'hover:bg-blue-500/10 dark:hover:bg-white/10'
            }`}
            onClick={() => setIsOpen(false)}
          >
            Sobre
          </Link>
        </div>
      </div>
    </nav>
  );
} 