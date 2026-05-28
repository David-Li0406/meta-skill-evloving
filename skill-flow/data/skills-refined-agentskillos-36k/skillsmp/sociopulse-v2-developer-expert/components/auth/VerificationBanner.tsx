'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Rocket, ArrowRight, AlertCircle } from 'lucide-react';
import Link from 'next/link';
import type { OnboardingStatus } from './VerificationGuard';

// =============================================================================
// VERIFICATION BANNER - Dashboard Nudge Component
// Sticky banner prompting users to complete their profile
// =============================================================================

interface VerificationBannerProps {
    /** Current user's onboarding status */
    status: OnboardingStatus;
    /** User's first name for personalization */
    firstName?: string;
    /** Allow user to dismiss the banner */
    dismissible?: boolean;
    /** Callback when banner is dismissed */
    onDismiss?: () => void;
}

export function VerificationBanner({
    status,
    firstName,
    dismissible = true,
    onDismiss,
}: VerificationBannerProps) {
    const [isDismissed, setIsDismissed] = useState(false);

    // Don't show if verified or dismissed
    if (status === 'VERIFIED' || isDismissed) {
        return null;
    }

    const handleDismiss = () => {
        setIsDismissed(true);
        onDismiss?.();
    };

    // Get banner content based on status
    const getBannerContent = () => {
        switch (status) {
            case 'REGISTERED':
                return {
                    icon: Rocket,
                    title: `🚀 Bienvenue${firstName ? ` ${firstName}` : ''} !`,
                    message: 'Votre profil est complété à 20%.',
                    cta: 'Terminer mon profil pour postuler',
                    percent: 20,
                    bgClass: 'bg-gradient-to-r from-amber-500 to-orange-500',
                };
            case 'PROFILE_COMPLETE':
                return {
                    icon: AlertCircle,
                    title: 'Presque terminé !',
                    message: 'Ajoutez vos documents pour valider votre profil.',
                    cta: 'Ajouter mes documents',
                    percent: 60,
                    bgClass: 'bg-gradient-to-r from-blue-500 to-indigo-500',
                };
            case 'DOCUMENTS_PENDING':
                return {
                    icon: AlertCircle,
                    title: 'Documents en cours de vérification',
                    message: 'Notre équipe vérifie vos documents. Vous serez notifié.',
                    cta: 'Voir le statut',
                    percent: 80,
                    bgClass: 'bg-gradient-to-r from-teal-500 to-cyan-500',
                };
            default:
                return null;
        }
    };

    const content = getBannerContent();
    if (!content) return null;

    const Icon = content.icon;

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className={`${content.bgClass} text-white shadow-lg`}
            >
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="py-3 flex items-center justify-between gap-4">
                        {/* Content */}
                        <div className="flex items-center gap-3 flex-1 min-w-0">
                            <div className="flex-shrink-0 hidden sm:block">
                                <Icon className="w-5 h-5" />
                            </div>
                            <div className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-3 min-w-0">
                                <span className="font-semibold text-sm sm:text-base">
                                    {content.title}
                                </span>
                                <span className="text-sm text-white/90 truncate">
                                    {content.message}
                                </span>
                            </div>
                        </div>

                        {/* CTA + Dismiss */}
                        <div className="flex items-center gap-2 flex-shrink-0">
                            <Link
                                href="/onboarding/complete"
                                className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white/20 hover:bg-white/30 rounded-full text-sm font-medium transition-colors"
                            >
                                <span className="hidden sm:inline">{content.cta}</span>
                                <span className="sm:hidden">Compléter</span>
                                <ArrowRight className="w-4 h-4" />
                            </Link>

                            {dismissible && (
                                <button
                                    onClick={handleDismiss}
                                    className="p-1.5 hover:bg-white/20 rounded-full transition-colors"
                                    aria-label="Fermer"
                                >
                                    <X className="w-4 h-4" />
                                </button>
                            )}
                        </div>
                    </div>

                    {/* Progress bar */}
                    <div className="pb-2">
                        <div className="h-1 bg-white/20 rounded-full overflow-hidden">
                            <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${content.percent}%` }}
                                transition={{ duration: 0.8, ease: 'easeOut' }}
                                className="h-full bg-white rounded-full"
                            />
                        </div>
                    </div>
                </div>
            </motion.div>
        </AnimatePresence>
    );
}

// =============================================================================
// COMPACT BADGE VERSION (for sidebar or cards)
// =============================================================================

interface VerificationBadgeProps {
    status: OnboardingStatus;
}

export function VerificationBadge({ status }: VerificationBadgeProps) {
    if (status === 'VERIFIED') {
        return (
            <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700">
                ✓ Vérifié
            </span>
        );
    }

    const getStatusInfo = () => {
        switch (status) {
            case 'REGISTERED':
                return { label: 'Profil à compléter', color: 'bg-amber-100 text-amber-700' };
            case 'PROFILE_COMPLETE':
                return { label: 'Documents manquants', color: 'bg-blue-100 text-blue-700' };
            case 'DOCUMENTS_PENDING':
                return { label: 'En vérification', color: 'bg-teal-100 text-teal-700' };
            default:
                return { label: 'Non vérifié', color: 'bg-slate-100 text-slate-600' };
        }
    };

    const { label, color } = getStatusInfo();

    return (
        <Link
            href="/onboarding/complete"
            className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${color} hover:opacity-80 transition-opacity`}
        >
            {label}
        </Link>
    );
}
