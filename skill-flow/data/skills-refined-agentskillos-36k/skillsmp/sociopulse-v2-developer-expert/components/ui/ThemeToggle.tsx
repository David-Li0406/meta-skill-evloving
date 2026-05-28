'use client';

import { Moon, Sun, Monitor } from 'lucide-react';
import { useTheme } from '@/components/providers/ThemeProvider';
import { cn } from '@/lib/utils';

// =============================================================================
// THEME TOGGLE - Dark/Light Mode Switcher
// =============================================================================

interface ThemeToggleProps {
    /** Compact mode - just icon button */
    compact?: boolean;
    /** Show system option */
    showSystem?: boolean;
    /** Additional className */
    className?: string;
}

/**
 * Simple toggle button for dark/light mode
 */
export function ThemeToggle({ compact = false, className }: ThemeToggleProps) {
    const { isDark, toggleColorMode } = useTheme();

    return (
        <button
            onClick={toggleColorMode}
            className={cn(
                'flex items-center gap-2 rounded-lg transition-all duration-200',
                compact 
                    ? 'p-2 hover:bg-slate-100 dark:hover:bg-slate-800' 
                    : 'px-3 py-2 hover:bg-slate-100 dark:hover:bg-slate-800',
                className
            )}
            title={isDark ? 'Passer en mode clair' : 'Passer en mode sombre'}
            aria-label={isDark ? 'Passer en mode clair' : 'Passer en mode sombre'}
        >
            {isDark ? (
                <Sun className="h-5 w-5 text-amber-500" />
            ) : (
                <Moon className="h-5 w-5 text-slate-500" />
            )}
            {!compact && (
                <span className="text-sm font-medium text-slate-600 dark:text-slate-300">
                    {isDark ? 'Mode clair' : 'Mode sombre'}
                </span>
            )}
        </button>
    );
}

/**
 * Pill-style toggle with animation
 */
export function ThemeTogglePill({ className }: { className?: string }) {
    const { isDark, toggleColorMode } = useTheme();

    return (
        <button
            onClick={toggleColorMode}
            className={cn(
                'relative flex h-8 w-16 items-center rounded-full p-1 transition-colors duration-300',
                isDark ? 'bg-slate-700' : 'bg-slate-200',
                className
            )}
            title={isDark ? 'Passer en mode clair' : 'Passer en mode sombre'}
            aria-label={isDark ? 'Passer en mode clair' : 'Passer en mode sombre'}
        >
            {/* Icons */}
            <Sun className={cn(
                'absolute left-1.5 h-4 w-4 transition-opacity duration-300',
                isDark ? 'opacity-50 text-slate-400' : 'opacity-0'
            )} />
            <Moon className={cn(
                'absolute right-1.5 h-4 w-4 transition-opacity duration-300',
                isDark ? 'opacity-0' : 'opacity-50 text-slate-400'
            )} />
            
            {/* Sliding circle */}
            <div
                className={cn(
                    'flex h-6 w-6 items-center justify-center rounded-full shadow-sm transition-all duration-300',
                    isDark 
                        ? 'translate-x-8 bg-slate-900' 
                        : 'translate-x-0 bg-white'
                )}
            >
                {isDark ? (
                    <Moon className="h-3.5 w-3.5 text-amber-400" />
                ) : (
                    <Sun className="h-3.5 w-3.5 text-amber-500" />
                )}
            </div>
        </button>
    );
}

/**
 * Segmented control with Light/Dark/System options
 */
export function ThemeToggleSegmented({ className }: { className?: string }) {
    const { colorMode, setColorMode, isDark } = useTheme();

    const options = [
        { value: 'light' as const, icon: Sun, label: 'Clair' },
        { value: 'dark' as const, icon: Moon, label: 'Sombre' },
        { value: 'system' as const, icon: Monitor, label: 'Auto' },
    ];

    return (
        <div className={cn(
            'flex rounded-lg p-1',
            isDark ? 'bg-slate-800' : 'bg-slate-100',
            className
        )}>
            {options.map(({ value, icon: Icon, label }) => (
                <button
                    key={value}
                    onClick={() => setColorMode(value)}
                    className={cn(
                        'flex items-center gap-1.5 rounded-md px-3 py-1.5 text-xs font-medium transition-all',
                        colorMode === value
                            ? isDark 
                                ? 'bg-slate-700 text-white shadow-sm' 
                                : 'bg-white text-slate-900 shadow-sm'
                            : isDark
                                ? 'text-slate-400 hover:text-slate-200'
                                : 'text-slate-500 hover:text-slate-700'
                    )}
                >
                    <Icon className="h-3.5 w-3.5" />
                    <span className="hidden sm:inline">{label}</span>
                </button>
            ))}
        </div>
    );
}
