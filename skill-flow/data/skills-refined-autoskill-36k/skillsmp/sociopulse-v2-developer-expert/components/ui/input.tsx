import * as React from 'react';
import { cn } from '@/lib/utils';

// =============================================================================
// INPUT COMPONENT — Standardized Form Input
// Uses polymorphic rounded-theme-* for brand consistency
// =============================================================================

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    /**
     * Shows error state (red border)
     */
    error?: boolean;
    /**
     * Error message to display below input
     */
    errorMessage?: string;
    /**
     * Left icon component
     */
    leftIcon?: React.ReactNode;
    /**
     * Right icon component
     */
    rightIcon?: React.ReactNode;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
    ({ className, type, error, errorMessage, leftIcon, rightIcon, ...props }, ref) => {
        return (
            <div className="relative w-full">
                {leftIcon && (
                    <div className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">
                        {leftIcon}
                    </div>
                )}
                <input
                    type={type}
                    className={cn(
                        // Base styles
                        `flex h-11 w-full rounded-theme-lg border bg-white px-4 py-2
                         text-sm text-slate-900 placeholder:text-slate-400
                         transition-colors duration-200`,
                        // Focus states
                        `focus-visible:outline-none focus-visible:ring-2 
                         focus-visible:ring-primary-200 focus-visible:border-primary-400`,
                        // Disabled state
                        'disabled:cursor-not-allowed disabled:opacity-50 disabled:bg-slate-50',
                        // File input styles
                        `file:border-0 file:bg-transparent file:text-sm file:font-medium 
                         file:text-slate-700 file:mr-4`,
                        // Normal vs Error border
                        error
                            ? 'border-red-400 focus-visible:ring-red-200 focus-visible:border-red-400'
                            : 'border-slate-200',
                        // Icon padding adjustments
                        leftIcon && 'pl-10',
                        rightIcon && 'pr-10',
                        className
                    )}
                    ref={ref}
                    {...props}
                />
                {rightIcon && (
                    <div className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400">
                        {rightIcon}
                    </div>
                )}
                {errorMessage && (
                    <p className="mt-1.5 text-xs text-red-500">{errorMessage}</p>
                )}
            </div>
        );
    }
);
Input.displayName = 'Input';

export { Input };
