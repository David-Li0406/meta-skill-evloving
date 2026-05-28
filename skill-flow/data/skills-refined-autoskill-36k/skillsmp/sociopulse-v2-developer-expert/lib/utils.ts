import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Utility function to merge Tailwind CSS classes with proper precedence.
 * Combines clsx for conditional classes and tailwind-merge for deduplication.
 * 
 * @example
 * cn('px-4 py-2', condition && 'bg-blue-500', 'px-6')
 * // Returns: 'py-2 px-6 bg-blue-500' (px-6 overrides px-4)
 */
export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}
