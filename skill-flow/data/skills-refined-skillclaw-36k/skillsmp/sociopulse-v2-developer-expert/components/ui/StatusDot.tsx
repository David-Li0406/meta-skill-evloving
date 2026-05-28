'use client';

import { cn } from '@/lib/utils';

interface StatusDotProps {
    status?: 'live' | 'active' | 'idle' | 'offline';
    size?: 'sm' | 'md' | 'lg';
    pulse?: boolean;
    className?: string;
}

const statusColors = {
    live: 'bg-rose-500',
    active: 'bg-emerald-500',
    idle: 'bg-amber-500',
    offline: 'bg-slate-400',
};

const sizeClasses = {
    sm: 'h-2 w-2',
    md: 'h-2.5 w-2.5',
    lg: 'h-3 w-3',
};

export function StatusDot({
    status = 'active',
    size = 'md',
    pulse = true,
    className
}: StatusDotProps) {
    return (
        <span className={cn('relative flex', sizeClasses[size], className)}>
            {pulse && (status === 'live' || status === 'active') && (
                <span
                    className={cn(
                        'absolute inline-flex h-full w-full animate-ping rounded-full opacity-75',
                        statusColors[status]
                    )}
                />
            )}
            <span
                className={cn(
                    'relative inline-flex rounded-full',
                    sizeClasses[size],
                    statusColors[status]
                )}
            />
        </span>
    );
}
