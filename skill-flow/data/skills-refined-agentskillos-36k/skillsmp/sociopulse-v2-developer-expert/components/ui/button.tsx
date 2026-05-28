import * as React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

// =============================================================================
// BUTTON COMPONENT — Polymorphic Design System
// Uses CSS variables for brand adaptation (SocioPulse vs MedicoPulse)
// =============================================================================

const buttonVariants = cva(
    // Base styles applied to all buttons
    `inline-flex items-center justify-center gap-2 whitespace-nowrap 
     font-semibold transition-all duration-200 
     focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2
     disabled:pointer-events-none disabled:opacity-50
     active:scale-[0.98]`,
    {
        variants: {
            variant: {
                // Primary: Uses polymorphic brand color (adapts to SocioPulse/MedicoPulse)
                default: `bg-primary-600 text-white 
                          hover:bg-primary-700 
                          focus-visible:ring-primary-500
                          shadow-sm hover:shadow-md`,

                // Destructive: For dangerous actions
                destructive: `bg-red-500 text-white 
                              hover:bg-red-600 
                              focus-visible:ring-red-500
                              shadow-sm hover:shadow-md`,

                // Outline: Bordered button
                outline: `border border-slate-200 bg-white text-slate-900
                          hover:bg-slate-50 hover:border-slate-300
                          focus-visible:ring-slate-400`,

                // Secondary: Muted background
                secondary: `bg-slate-100 text-slate-900 
                            hover:bg-slate-200 
                            focus-visible:ring-slate-400`,

                // Ghost: Transparent until hovered
                ghost: `text-slate-700 
                        hover:bg-slate-100 hover:text-slate-900
                        focus-visible:ring-slate-400`,

                // Link: Text-only with underline
                link: `text-primary-600 underline-offset-4 
                       hover:underline hover:text-primary-700
                       focus-visible:ring-primary-500`,

                // Live: Uses the teal/live color for SocioLive features
                live: `bg-live-500 text-white 
                       hover:bg-live-600 
                       focus-visible:ring-live-500
                       shadow-sm hover:shadow-md`,

                // Alert: Uses rose/alert for urgent actions (MedicoPulse missions)
                alert: `bg-alert-500 text-white 
                        hover:bg-alert-600 
                        focus-visible:ring-alert-500
                        shadow-sm hover:shadow-md`,
            },
            size: {
                default: 'h-10 px-5 text-sm rounded-theme-lg',
                sm: 'h-9 px-3 text-xs rounded-theme-md',
                lg: 'h-12 px-6 text-base rounded-theme-xl',
                icon: 'h-10 w-10 rounded-theme-lg',
            },
        },
        defaultVariants: {
            variant: 'default',
            size: 'default',
        },
    }
);

export interface ButtonProps
    extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
    /**
     * If true, renders as the child element (useful for Link components)
     */
    asChild?: boolean;
    /**
     * Shows loading spinner and disables button
     */
    loading?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
    ({ className, variant, size, asChild = false, loading, disabled, children, ...props }, ref) => {
        const Comp = asChild ? Slot : 'button';

        return (
            <Comp
                className={cn(buttonVariants({ variant, size, className }))}
                ref={ref}
                disabled={disabled || loading}
                {...props}
            >
                {loading ? (
                    <>
                        <svg
                            className="h-4 w-4 animate-spin"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                        >
                            <circle
                                className="opacity-25"
                                cx="12"
                                cy="12"
                                r="10"
                                stroke="currentColor"
                                strokeWidth="4"
                            />
                            <path
                                className="opacity-75"
                                fill="currentColor"
                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                            />
                        </svg>
                        <span>Chargement...</span>
                    </>
                ) : (
                    children
                )}
            </Comp>
        );
    }
);
Button.displayName = 'Button';

export { Button, buttonVariants };
