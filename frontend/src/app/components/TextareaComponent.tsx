'use client';

import { ChangeEvent } from 'react';

interface TextareaProps {
  id: string;
  name: string;
  value: string;
  onChange: (e: ChangeEvent<HTMLTextAreaElement>) => void;
  label?: string;
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  helpText?: string;
  error?: string;
  rows?: number;
  maxLength?: number;
}

export default function TextareaComponent({
  id,
  name,
  value,
  onChange,
  label,
  placeholder,
  required = false,
  disabled = false,
  className = '',
  helpText,
  error,
  rows = 4,
  maxLength
}: TextareaProps) {
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
      
      <textarea
        id={id}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        disabled={disabled}
        required={required}
        rows={rows}
        maxLength={maxLength}
        className={`
          shadow appearance-none border rounded-lg w-full py-3 px-4 
          text-gray-700 dark:text-gray-300 leading-tight 
          focus:outline-none focus:ring-2 focus:ring-blue-500/50 
          bg-white dark:bg-gray-800/50 dark:border-gray-700
          resize-none
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
      
      {maxLength && (
        <div className="flex justify-end text-xs text-gray-500 dark:text-gray-400 mt-1">
          {value.length}/{maxLength}
        </div>
      )}
      
      {error && (
        <p className="text-red-500 dark:text-red-400 text-xs mt-1">
          {error}
        </p>
      )}
    </div>
  );
} 