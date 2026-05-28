'use client';

import { motion } from 'framer-motion';
import {
    MessageCircle,
    Send,
    Phone,
    Heart,
    Share2
} from 'lucide-react';

export interface MobileActionBarProps {
    /** User role being viewed */
    role: 'TALENT' | 'CLIENT' | 'ADMIN';
    /** Whether this is the current user's own profile */
    isOwnProfile?: boolean;
    /** Whether the user is in favorites */
    isFavorite?: boolean;
    /** Primary CTA click handler */
    onPrimaryAction?: () => void;
    /** Secondary action (message) click handler */
    onMessageClick?: () => void;
    /** Favorite toggle handler */
    onFavoriteToggle?: () => void;
    /** Share profile handler */
    onShare?: () => void;
}

export function MobileActionBar({
    role,
    isOwnProfile = false,
    isFavorite = false,
    onPrimaryAction,
    onMessageClick,
    onFavoriteToggle,
    onShare,
}: MobileActionBarProps) {
    // Don't show action bar on own profile
    if (isOwnProfile) return null;

    // Role-specific CTA text
    // TALENT profile = propose a mission, CLIENT profile = send application
    const primaryCTA = role === 'TALENT'
        ? 'Proposer une mission'
        : 'Envoyer une candidature';

    const PrimaryIcon = Send;

    return (
        <>
            {/* Spacer to prevent content being hidden behind fixed bar */}
            <div className="lg:hidden h-24" />

            {/* Fixed Bottom Action Bar - Mobile Only */}
            <motion.div
                initial={{ y: 100, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ type: 'spring', stiffness: 300, damping: 30, delay: 0.3 }}
                className="lg:hidden fixed bottom-0 left-0 right-0 z-50"
            >
                {/* Glass Background - Enhanced Glassmorphism */}
                <div className="absolute inset-0 bg-white/80 backdrop-blur-xl border-t border-slate-200/80" />

                {/* Safe Area Padding for iPhone */}
                <div className="relative px-4 py-3 pb-safe">
                    <div className="flex items-center gap-3">
                        {/* Secondary Actions */}
                        <div className="flex items-center gap-2">
                            {/* Favorite Button */}
                            <motion.button
                                whileTap={{ scale: 0.9 }}
                                onClick={onFavoriteToggle}
                                className={`
                                    btn-social !w-11 !h-11
                                    ${isFavorite
                                        ? 'bg-rose-50 border-rose-200 text-rose-500'
                                        : ''
                                    }
                                `}
                                aria-label={isFavorite ? 'Retirer des favoris' : 'Ajouter aux favoris'}
                            >
                                <Heart
                                    className={`w-5 h-5 ${isFavorite ? 'fill-rose-500' : ''}`}
                                />
                            </motion.button>

                            {/* Share Button */}
                            <motion.button
                                whileTap={{ scale: 0.9 }}
                                onClick={onShare}
                                className="btn-social !w-11 !h-11"
                                aria-label="Partager le profil"
                            >
                                <Share2 className="w-5 h-5" />
                            </motion.button>

                            {/* Message Button */}
                            <motion.button
                                whileTap={{ scale: 0.9 }}
                                onClick={onMessageClick}
                                className="btn-secondary !w-11 !h-11 !p-0"
                                aria-label="Envoyer un message"
                            >
                                <MessageCircle className="w-5 h-5" />
                            </motion.button>
                        </div>

                        {/* Primary CTA Button */}
                        <motion.button
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            onClick={onPrimaryAction}
                            className="btn-primary flex-1 !py-3 shadow-lg shadow-brand-600/30"
                        >
                            <PrimaryIcon className="w-5 h-5" />
                            <span>{primaryCTA}</span>
                        </motion.button>
                    </div>
                </div>
            </motion.div>
        </>
    );
}

/**
 * Desktop Action Buttons (inline in profile)
 * Use this inside the profile content area on desktop
 */
export interface DesktopActionsProps {
    role: 'TALENT' | 'CLIENT' | 'ADMIN';
    isOwnProfile?: boolean;
    isFavorite?: boolean;
    onPrimaryAction?: () => void;
    onMessageClick?: () => void;
    onFavoriteToggle?: () => void;
    onShare?: () => void;
    onCall?: () => void;
}

export function DesktopActions({
    role,
    isOwnProfile = false,
    isFavorite = false,
    onPrimaryAction,
    onMessageClick,
    onFavoriteToggle,
    onShare,
    onCall,
}: DesktopActionsProps) {
    if (isOwnProfile) return null;

    // TALENT profile = propose a mission, CLIENT profile = send application
    const primaryCTA = role === 'TALENT' ? 'Proposer une mission' : 'Envoyer une candidature';
    const PrimaryIcon = Send;

    return (
        <div className="hidden lg:flex items-center gap-3 mt-6">
            {/* Primary CTA */}
            <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={onPrimaryAction}
                className="btn-primary !py-3 shadow-lg shadow-brand-600/25"
            >
                <PrimaryIcon className="w-5 h-5" />
                {primaryCTA}
            </motion.button>

            {/* Message Button */}
            <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={onMessageClick}
                className="btn-secondary !py-3"
            >
                <MessageCircle className="w-5 h-5" />
                Contacter
            </motion.button>

            {/* Call Button (if phone available) */}
            {onCall && (
                <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={onCall}
                    className="btn-social !w-11 !h-11 !bg-green-100 !text-green-700 hover:!bg-green-200"
                    aria-label="Appeler"
                >
                    <Phone className="w-5 h-5" />
                </motion.button>
            )}

            {/* Favorite Button */}
            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={onFavoriteToggle}
                className={`
                    btn-social !w-11 !h-11
                    ${isFavorite
                        ? '!bg-rose-100 !text-rose-500'
                        : ''
                    }
                `}
                aria-label={isFavorite ? 'Retirer des favoris' : 'Ajouter aux favoris'}
            >
                <Heart className={`w-5 h-5 ${isFavorite ? 'fill-rose-500' : ''}`} />
            </motion.button>

            {/* Share Button */}
            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={onShare}
                className="btn-social !w-11 !h-11"
                aria-label="Partager"
            >
                <Share2 className="w-5 h-5" />
            </motion.button>
        </div>
    );
}

