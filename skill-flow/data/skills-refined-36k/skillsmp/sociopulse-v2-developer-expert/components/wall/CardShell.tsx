'use client';

import type { ReactNode, MouseEvent } from 'react';
import { motion } from 'framer-motion';
import { Heart, Share2 } from 'lucide-react';

export type CardVariant = 'need' | 'offer';

export interface CardShellProps {
    /** Card variant - determines border and theme colors */
    variant: CardVariant;
    /** Card content */
    children: ReactNode;
    /** Whether the card has an image hero */
    hasImage?: boolean;
    /** Hero section content (image or pattern) */
    heroContent?: ReactNode;
    /** Click handler for the entire card */
    onClick?: () => void;
    /** Whether the card is favorited */
    isFavorite?: boolean;
    /** Callback when favorite is toggled */
    onFavoriteToggle?: (e: MouseEvent<HTMLButtonElement>) => void;
    /** Callback when share is clicked */
    onShare?: (e: MouseEvent<HTMLButtonElement>) => void;
    /** Whether to show social actions */
    showSocialActions?: boolean;
    /** Additional footer content (like contact button) */
    footerContent?: ReactNode;
}

const variantStyles = {
    need: {
        border: 'border-l-4 border-blue-500',
        hoverBorder: 'group-hover:border-blue-200',
    },
    offer: {
        border: 'border-l-4 border-rose-500',
        hoverBorder: 'group-hover:border-rose-200',
    },
};

export function CardShell({
    variant,
    children,
    hasImage = false,
    heroContent,
    onClick,
    isFavorite = false,
    onFavoriteToggle,
    onShare,
    showSocialActions = true,
    footerContent,
}: CardShellProps) {
    const styles = variantStyles[variant];

    const handleFavorite = (e: MouseEvent<HTMLButtonElement>) => {
        e.stopPropagation();
        onFavoriteToggle?.(e);
    };

    const handleShare = (e: MouseEvent<HTMLButtonElement>) => {
        e.stopPropagation();
        onShare?.(e);
    };

    return (
        <motion.article
            whileHover={{ y: -4, transition: { duration: 0.2 } }}
            whileTap={{ scale: 0.98 }}
            onClick={onClick}
            className={`
                group relative card-surface cursor-pointer overflow-hidden
                ${styles.border}
            `}
        >
            {/* Hero Section */}
            {heroContent && (
                <div className="relative">
                    {heroContent}
                </div>
            )}

            {/* Pattern Hero Fallback for cards without images */}
            {!hasImage && !heroContent && (
                <div className={variant === 'need' ? 'pattern-hero-need' : 'pattern-hero'}>
                    {/* Decorative elements can be added here */}
                </div>
            )}

            {/* Card Content */}
            <div className="p-6">
                {children}
            </div>

            {/* Footer with Social Actions */}
            {(showSocialActions || footerContent) && (
                <div className="px-6 pb-6 pt-0">
                    <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                        {/* Social Actions */}
                        {showSocialActions && (
                            <div className="flex items-center gap-2">
                                <motion.button
                                    whileHover={{ scale: 1.1 }}
                                    whileTap={{ scale: 0.9 }}
                                    onClick={handleFavorite}
                                    className={`btn-social ${isFavorite ? 'text-rose-500 border-rose-200 bg-rose-50' : ''}`}
                                    aria-label={isFavorite ? 'Retirer des favoris' : 'Ajouter aux favoris'}
                                >
                                    <Heart className={`w-4 h-4 ${isFavorite ? 'fill-rose-500' : ''}`} />
                                </motion.button>
                                <motion.button
                                    whileHover={{ scale: 1.1 }}
                                    whileTap={{ scale: 0.9 }}
                                    onClick={handleShare}
                                    className="btn-social"
                                    aria-label="Partager"
                                >
                                    <Share2 className="w-4 h-4" />
                                </motion.button>
                            </div>
                        )}

                        {/* Footer Content (Contact button, etc.) */}
                        {footerContent && (
                            <div className="ml-auto">
                                {footerContent}
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Hover Effect Overlay */}
            <div className={`absolute inset-0 rounded-2xl border-2 border-transparent ${styles.hoverBorder} transition-colors pointer-events-none`} />
        </motion.article>
    );
}
