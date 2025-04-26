export default function Loading() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[50vh] p-4">
      <div className="relative">
        <div className="h-24 w-24 rounded-full border-t-4 border-b-4 border-blue-600 dark:border-blue-400 animate-spin"></div>
        <div className="h-24 w-24 rounded-full border-r-4 border-l-4 border-transparent border-r-indigo-500 dark:border-r-indigo-400 border-l-indigo-500 dark:border-l-indigo-400 absolute top-0 left-0 animate-ping opacity-40"></div>
      </div>
      <div className="mt-8 text-center">
        <h2 className="text-2xl font-bold mb-2 text-gray-800 dark:text-white">
          Gerando seu projeto
        </h2>
        <p className="text-gray-600 dark:text-gray-400 max-w-md mx-auto">
          Este processo pode levar alguns segundos enquanto criamos seu projeto personalizado...
        </p>
        
        <div className="mt-10">
          <div className="grid grid-cols-3 gap-3 max-w-xs mx-auto">
            <div className="bg-blue-100 dark:bg-blue-900/40 h-2 rounded-full animate-pulse" style={{ animationDelay: '0ms' }}></div>
            <div className="bg-blue-100 dark:bg-blue-900/40 h-2 rounded-full animate-pulse" style={{ animationDelay: '300ms' }}></div>
            <div className="bg-blue-100 dark:bg-blue-900/40 h-2 rounded-full animate-pulse" style={{ animationDelay: '600ms' }}></div>
          </div>
        </div>
        
        <div className="mt-8 text-gray-500 dark:text-gray-400 text-sm animate-pulse">
          <span className="inline-block px-3 py-1 rounded-full bg-gray-100 dark:bg-gray-800">
            Processando dados...
          </span>
        </div>
      </div>
    </div>
  );
} 