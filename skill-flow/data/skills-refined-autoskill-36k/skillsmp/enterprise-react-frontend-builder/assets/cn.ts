import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

/**
 * Utility function to merge Tailwind CSS classes
 * 
 * Uses clsx to conditionally construct class names and
 * tailwind-merge to merge Tailwind classes intelligently
 * 
 * @example
 * cn('px-4 py-2', 'bg-blue-500', 'hover:bg-blue-600')
 * cn('px-4', condition && 'py-2')
 * cn('base-class', props.className)
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}