import React from 'react'
import Image from 'next/image'

export const Button: React.FC<React.ButtonHTMLAttributes<HTMLButtonElement>> = ({ children, ...props }) => (
  <button 
    {...props} 
    className={`px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 ${props.className || ''}`}
  >
    {children}
  </button>
)

export const Input: React.FC<React.InputHTMLAttributes<HTMLInputElement>> = (props) => (
  <input 
    {...props} 
    className={`px-3 py-2 border border-gray-300 rounded ${props.className || ''}`}
  />
)

export const Card: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, ...props }) => (
  <div {...props} className={`bg-white shadow rounded-lg ${props.className || ''}`}>
    {children}
  </div>
)

export const CardHeader: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, ...props }) => (
  <div {...props} className={`px-6 py-4 border-b ${props.className || ''}`}>
    {children}
  </div>
)

export const CardContent: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, ...props }) => (
  <div {...props} className={`px-6 py-4 ${props.className || ''}`}>
    {children}
  </div>
)

export const CardFooter: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, ...props }) => (
  <div {...props} className={`px-6 py-4 border-t ${props.className || ''}`}>
    {children}
  </div>
)

export const CardTitle: React.FC<React.HTMLAttributes<HTMLHeadingElement>> = ({ children, ...props }) => (
  <h2 {...props} className={`text-xl font-bold ${props.className || ''}`}>
    {children}
  </h2>
)

export const Avatar: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, ...props }) => (
  <div {...props} className={`inline-flex items-center justify-center bg-gray-100 rounded-full ${props.className || ''}`}>
    {children}
  </div>
)

export const AvatarImage: React.FC<React.ImgHTMLAttributes<HTMLImageElement> & { width?: number; height?: number }> = ({ 
  src, 
  alt = "Avatar", 
  width = 40,
  height = 40,
  ...props 
}) => (
  <Image 
    src={src || '/default-avatar.png'}
    alt={alt}
    width={width}
    height={height}
    className={`rounded-full ${props.className || ''}`} 
  />
)

export const AvatarFallback: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, ...props }) => (
  <div {...props} className={`flex items-center justify-center bg-gray-200 rounded-full text-gray-600 font-semibold ${props.className || ''}`}>
    {children}
  </div>
)

export const Badge: React.FC<React.HTMLAttributes<HTMLSpanElement>> = ({ children, ...props }) => (
  <span {...props} className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 ${props.className || ''}`}>
    {children}
  </span>
)

