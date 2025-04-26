'use client';

import { ChangeEvent } from 'react';

interface InputProps {
  id: string;
  name: string;
  type?: 'text' | 'email' | 'password' | 'number' | 'tel';
  value: string;
  onChange: (e: ChangeEvent<HTMLInputElement>) => void;
  label?: string;
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  helpText?: string;
  error?: string;
}

export default function InputComponent({
  id,
  name,
  type = 'text',
  value,
  onChange,
  label,
  placeholder,
  required = false,
  disabled = false,
  className = '',
  helpText,
  error
}: InputProps) {
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
      
      <input
        id={id}
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
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
      />
      
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