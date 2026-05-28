import * as React from 'react';
import { cn } from '@/lib/utils';

// =============================================================================
// CARD COMPONENT — Composable Card System
// Uses polymorphic shadow-theme-* and rounded-theme-* for brand consistency
// =============================================================================

// -----------------------------------------------------------------------------
// Card Root
// -----------------------------------------------------------------------------
const Card = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement> & {
        /** Card style variant */
        variant?: 'default' | 'elevated' | 'glass' | 'interactive';
    }
>(({ className, variant = 'default', ...props }, ref) => {
    const variants = {
        default: 'bg-white border border-slate-200 shadow-theme-sm',
        elevated: 'bg-white border border-slate-100 shadow-theme-md',
        glass: 'bg-white/70 backdrop-blur-md border border-white/60 shadow-soft',
        interactive: `bg-white border border-slate-200 shadow-theme-sm 
                      hover:shadow-theme-md hover:border-slate-300 
                      transition-all duration-200 cursor-pointer`,
    };

    return (
        <div
            ref={ref}
            className={cn(
                'rounded-theme-xl text-slate-900',
                variants[variant],
                className
            )}
            {...props}
        />
    );
});
Card.displayName = 'Card';

// -----------------------------------------------------------------------------
// Card Header
// -----------------------------------------------------------------------------
const CardHeader = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
    <div
        ref={ref}
        className={cn('flex flex-col space-y-1.5 p-6', className)}
        {...props}
    />
));
CardHeader.displayName = 'CardHeader';

// -----------------------------------------------------------------------------
// Card Title
// -----------------------------------------------------------------------------
const CardTitle = React.forwardRef<
    HTMLParagraphElement,
    React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
    <h3
        ref={ref}
        className={cn('text-lg font-semibold leading-none tracking-tight', className)}
        {...props}
    />
));
CardTitle.displayName = 'CardTitle';

// -----------------------------------------------------------------------------
// Card Description
// -----------------------------------------------------------------------------
const CardDescription = React.forwardRef<
    HTMLParagraphElement,
    React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
    <p
        ref={ref}
        className={cn('text-sm text-slate-500', className)}
        {...props}
    />
));
CardDescription.displayName = 'CardDescription';

// -----------------------------------------------------------------------------
// Card Content
// -----------------------------------------------------------------------------
const CardContent = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
    <div ref={ref} className={cn('p-6 pt-0', className)} {...props} />
));
CardContent.displayName = 'CardContent';

// -----------------------------------------------------------------------------
// Card Footer
// -----------------------------------------------------------------------------
const CardFooter = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
    <div
        ref={ref}
        className={cn('flex items-center p-6 pt-0', className)}
        {...props}
    />
));
CardFooter.displayName = 'CardFooter';

export { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter };
