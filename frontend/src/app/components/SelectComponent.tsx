'use client';

import { ChangeEvent } from 'react';

interface Option {
  value: string;
  label: string;
}

interface SelectProps {
  id: string;
  name: string;
  value: string;
  onChange: (e: ChangeEvent<HTMLSelectElement>) => void;
  options: Option[];
  label?: string;
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  helpText?: string;
  error?: string;
}

export default function SelectComponent({
  id,
  name,
  value,
  onChange,
  options,
  label,
  placeholder,
  required = false,
  disabled = false,
  className = '',
  helpText,
  error,
}: SelectProps) {
  return (
    <div className="mb-4">
      {label && (
        <label 
          htmlFor={id} 
          className="block text-gray-700 dark:text-gray-300 text-sm font-bold mb-2"
        >
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      
      <div className="relative">
        <select
          id={id}
          name={name}
          value={value}
          onChange={onChange}
          disabled={disabled}
          required={required}
          className={`
            shadow appearance-none border rounded-lg w-full py-3 px-4 
            text-gray-700 dark:text-gray-300 leading-tight 
            focus:outline-none focus:ring-2 focus:ring-blue-500/50 
            bg-white dark:bg-gray-800/50 dark:border-gray-700
            ${error ? 'border-red-500 dark:border-red-700' : 'border-gray-200 dark:border-gray-700'}
            ${disabled ? 'opacity-60 cursor-not-allowed' : ''}
            ${className}
          `}
        >
          {placeholder && (
            <option value="" disabled>
              {placeholder}
            </option>
          )}
          
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        
        <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700 dark:text-gray-300">
          <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
            <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
          </svg>
        </div>
      </div>
      
      {helpText && !error && (
        <p className="text-gray-500 dark:text-gray-400 text-xs mt-1">
          {helpText}
        </p>
      )}
      
      {error && (
        <p className="text-red-500 dark:text-red-400 text-xs mt-1">
          {error}
        </p>
      )}
    </div>
  );
} 