'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { cn } from '@/lib/utils';
import { LucideIcon } from 'lucide-react';

interface ActionCardProps {
    title: string;
    description?: string;
    icon: LucideIcon;
    href: string;
    variant?: 'urgency' | 'project' | 'neutral';
    className?: string;
    iconPulse?: boolean;
}

const variantStyles = {
    urgency: {
        border: 'border-rose-200 hover:border-rose-300',
        iconBg: 'bg-rose-50',
        iconColor: 'text-rose-600',
        accent: 'bg-rose-600',
    },
    project: {
        border: 'border-teal-200 hover:border-teal-300',
        iconBg: 'bg-teal-50',
        iconColor: 'text-teal-600',
        accent: 'bg-teal-600',
    },
    neutral: {
        border: 'border-slate-200 hover:border-slate-300',
        iconBg: 'bg-slate-50',
        iconColor: 'text-slate-600',
        accent: 'bg-slate-600',
    },
};

export function ActionCard({
    title,
    description,
    icon: Icon,
    href,
    variant = 'neutral',
    className,
    iconPulse = false,
}: ActionCardProps) {
    const styles = variantStyles[variant];

    return (
        <Link href={href} className={cn('block', className)}>
            <motion.div
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
                transition={{ type: 'spring', stiffness: 400, damping: 25 }}
                className={cn(
                    'relative overflow-hidden rounded-xl border bg-white p-6 shadow-sm transition-shadow hover:shadow-md',
                    styles.border
                )}
            >
                {/* Accent line at top */}
                <div className={cn('absolute left-0 right-0 top-0 h-1', styles.accent)} />

                <div className="flex items-center gap-4">
                    <div
                        className={cn(
                            'relative flex h-14 w-14 items-center justify-center rounded-xl',
                            styles.iconBg
                        )}
                    >
                        {iconPulse && (
                            <span
                                className={cn(
                                    'absolute inset-0 animate-ping rounded-xl opacity-30',
                                    styles.iconBg
                                )}
                            />
                        )}
                        <Icon className={cn('h-7 w-7', styles.iconColor)} />
                    </div>
                    <div className="flex-1">
                        <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
                        {description && (
                            <p className="mt-0.5 text-sm text-slate-500">{description}</p>
                        )}
                    </div>
                    <svg
                        className="h-5 w-5 text-slate-400"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M9 5l7 7-7 7"
                        />
                    </svg>
                </div>
            </motion.div>
        </Link>
    );
}
