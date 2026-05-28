import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

// =============================================================================
// BADGE COMPONENT — Semantic Status Badges
// Uses rounded-full as per audit recommendation
// =============================================================================

const badgeVariants = cva(
    // Base styles
    `inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 
     text-xs font-semibold transition-colors`,
    {
        variants: {
            variant: {
                // Default: Uses polymorphic primary color
                default: 'bg-primary-100 text-primary-700',

                // Secondary: Neutral/muted
                secondary: 'bg-slate-100 text-slate-700',

                // Success: Positive states
                success: 'bg-green-100 text-green-700',

                // Warning: Attention needed
                warning: 'bg-amber-100 text-amber-700',

                // Destructive: Errors/danger
                destructive: 'bg-red-100 text-red-700',

                // Outline: Bordered style
                outline: 'border border-slate-200 bg-transparent text-slate-700',

                // Live: For SocioLive/Ateliers
                live: 'bg-live-100 text-live-700',

                // Alert: For urgent missions (MedicoPulse)
                alert: 'bg-alert-100 text-alert-700',

                // Solid variants (filled background)
                'solid-primary': 'bg-primary-600 text-white',
                'solid-success': 'bg-green-500 text-white',
                'solid-warning': 'bg-amber-500 text-white',
                'solid-destructive': 'bg-red-500 text-white',
                'solid-live': 'bg-live-500 text-white',
                'solid-alert': 'bg-alert-500 text-white',
            },
            size: {
                default: 'px-2.5 py-1 text-xs',
                sm: 'px-2 py-0.5 text-[10px]',
                lg: 'px-3 py-1.5 text-sm',
            },
        },
        defaultVariants: {
            variant: 'default',
            size: 'default',
        },
    }
);

export interface BadgeProps
    extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {
    /**
     * Optional icon to display before the text
     */
    icon?: React.ReactNode;
}

function Badge({ className, variant, size, icon, children, ...props }: BadgeProps) {
    return (
        <span className={cn(badgeVariants({ variant, size }), className)} {...props}>
            {icon}
            {children}
        </span>
    );
}

export { Badge, badgeVariants };
