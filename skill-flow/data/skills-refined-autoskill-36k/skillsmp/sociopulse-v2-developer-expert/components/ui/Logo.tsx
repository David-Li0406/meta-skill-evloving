'use client';

import Link from 'next/link';
import { Outfit } from 'next/font/google';
import { HeartHandshake, Cross } from 'lucide-react';
import { isMedical, currentBrand } from '@/lib/brand';

const outfit = Outfit({
    subsets: ['latin'],
    weight: ['700', '800'],
    display: 'swap',
});

export type LogoSize = 'sm' | 'md' | 'lg' | 'xl';

export interface LogoProps {
    size?: LogoSize;
    showBaseline?: boolean;
    showIcon?: boolean;
    href?: string | null;
    as?: 'h1' | 'span';
    className?: string;
}

const sizeStyles: Record<LogoSize, {
    icon: string;
    iconSize: string;
    text: string;
    baseline: string;
    baselineSpacing: string;
    gap: string;
}> = {
    sm: { icon: 'h-8 w-8', iconSize: 'h-4 w-4', text: 'text-xl', baseline: 'text-xs', baselineSpacing: 'mt-0.5', gap: 'gap-2' },
    md: { icon: 'h-10 w-10', iconSize: 'h-5 w-5', text: 'text-2xl', baseline: 'text-sm', baselineSpacing: 'mt-1', gap: 'gap-2.5' },
    lg: { icon: 'h-12 w-12', iconSize: 'h-6 w-6', text: 'text-3xl', baseline: 'text-base', baselineSpacing: 'mt-1.5', gap: 'gap-3' },
    xl: { icon: 'h-14 w-14', iconSize: 'h-7 w-7', text: 'text-4xl sm:text-5xl', baseline: 'text-lg sm:text-xl', baselineSpacing: 'mt-2', gap: 'gap-4' },
};

export function Logo({
    size = 'md',
    showBaseline = true,
    showIcon = true,
    href = '/',
    as = 'span',
    className
}: LogoProps) {
    const styles = sizeStyles[size];
    const TitleTag = as;
    const medical = isMedical();

    // Icon: HeartHandshake for SOCIAL (care + partnership), Cross for MEDICAL (ambulance cross)
    const IconComponent = medical ? Cross : HeartHandshake;

    const iconContainer = (
        <div className={`${styles.icon} rounded-2xl flex items-center justify-center shadow-lg transition-transform group-hover:scale-105 ${medical
            ? 'bg-rose-500 shadow-rose-500/30'
            : 'bg-gradient-to-br from-indigo-600 to-teal-500 shadow-indigo-500/30'
            }`}>
            <IconComponent className={`${styles.iconSize} text-white`} strokeWidth={medical ? 4 : 1.8} />
        </div>
    );

    const content = (
        <div className={`flex items-center ${styles.gap}`}>
            {showIcon && iconContainer}
            <div className="flex flex-col">
                <TitleTag className={`${styles.text} font-extrabold tracking-tight leading-none ${medical
                    ? 'text-rose-500'
                    : 'bg-gradient-to-r from-indigo-600 to-teal-500 bg-clip-text text-transparent'
                    }`}>
                    {currentBrand.appName}
                </TitleTag>
                {showBaseline && (
                    <p className={`${styles.baselineSpacing} ${styles.baseline} font-semibold tracking-tight leading-none ${medical ? 'text-rose-400/80' : 'text-slate-500'
                        }`}>
                        {currentBrand.tagline}
                    </p>
                )}
            </div>
        </div>
    );

    const wrapperClassName = `${outfit.className} inline-flex items-center whitespace-nowrap group ${className ?? ''}`;

    if (href) {
        return (
            <Link href={href} aria-label={currentBrand.appName} className={wrapperClassName}>
                {content}
            </Link>
        );
    }

    return <div className={wrapperClassName}>{content}</div>;
}

