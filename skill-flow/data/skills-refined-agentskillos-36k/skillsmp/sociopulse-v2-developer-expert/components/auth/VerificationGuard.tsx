'use client';

import { useState, ReactNode } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, ShieldAlert, FileCheck, ArrowRight, Lock } from 'lucide-react';
import Link from 'next/link';

// =============================================================================
// VERIFICATION GUARD - Legal Compliance Wrapper
// Intercepts actions if user is not verified
// =============================================================================

export type OnboardingStatus = 'REGISTERED' | 'PROFILE_COMPLETE' | 'DOCUMENTS_PENDING' | 'VERIFIED';

interface VerificationGuardProps {
    /** Current user's onboarding status */
    status: OnboardingStatus;
    /** Children to render (button, link, etc.) */
    children: ReactNode;
    /** Action being protected (for modal messaging) */
    actionLabel?: string;
    /** Callback when verification is required */
    onVerificationRequired?: () => void;
    /** If true, completely disable the children instead of intercepting */
    disableCompletely?: boolean;
}

/**
 * Wraps actionable elements (buttons) and intercepts if user is not verified.
 * Shows a modal prompting user to complete their profile.
 */
export function VerificationGuard({
    status,
    children,
    actionLabel = 'cette action',
    onVerificationRequired,
    disableCompletely = false,
}: VerificationGuardProps) {
    const [showModal, setShowModal] = useState(false);

    // User is verified - render children normally
    const isVerified = status === 'VERIFIED';

    if (isVerified) {
        return <>{children}</>;
    }

    // Intercept click
    const handleClick = (e: React.MouseEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setShowModal(true);
        onVerificationRequired?.();
    };

    // If completely disabled, render with visual indication
    if (disableCompletely) {
        return (
            <div className="relative group">
                <div className="opacity-50 pointer-events-none">
                    {children}
                </div>
                <div className="absolute inset-0 flex items-center justify-center bg-slate-900/10 rounded-theme-lg cursor-not-allowed">
                    <Lock className="w-5 h-5 text-slate-500" />
                </div>
            </div>
        );
    }

    return (
        <>
            {/* Wrap children to intercept clicks */}
            <div onClick={handleClick} className="cursor-pointer">
                {children}
            </div>

            {/* Verification Modal */}
            <AnimatePresence>
                {showModal && (
                    <VerificationModal
                        status={status}
                        actionLabel={actionLabel}
                        onClose={() => setShowModal(false)}
                    />
                )}
            </AnimatePresence>
        </>
    );
}

// =============================================================================
// VERIFICATION MODAL
// =============================================================================

interface VerificationModalProps {
    status: OnboardingStatus;
    actionLabel: string;
    onClose: () => void;
}

function VerificationModal({ status, actionLabel, onClose }: VerificationModalProps) {
    // Determine completion percentage
    const getCompletionInfo = () => {
        switch (status) {
            case 'REGISTERED':
                return { percent: 20, missing: 'vos informations professionnelles et documents' };
            case 'PROFILE_COMPLETE':
                return { percent: 60, missing: 'vos documents légaux (diplôme, pièce d\'identité)' };
            case 'DOCUMENTS_PENDING':
                return { percent: 80, missing: 'la validation de vos documents (en cours de vérification)' };
            default:
                return { percent: 0, missing: 'votre profil' };
        }
    };

    const { percent, missing } = getCompletionInfo();

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4"
            onClick={onClose}
        >
            <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                transition={{ type: 'spring', damping: 25, stiffness: 300 }}
                className="bg-white rounded-theme-2xl shadow-2xl max-w-md w-full p-6"
                onClick={(e) => e.stopPropagation()}
            >
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                        <div className="w-12 h-12 rounded-full bg-amber-100 flex items-center justify-center">
                            <ShieldAlert className="w-6 h-6 text-amber-600" />
                        </div>
                        <div>
                            <h3 className="text-lg font-semibold text-slate-900">
                                Complétez votre profil
                            </h3>
                            <p className="text-sm text-slate-500">
                                Profil complété à {percent}%
                            </p>
                        </div>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-slate-100 rounded-full transition-colors"
                    >
                        <X className="w-5 h-5 text-slate-400" />
                    </button>
                </div>

                {/* Progress Bar */}
                <div className="mb-4">
                    <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                        <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${percent}%` }}
                            transition={{ duration: 0.5, delay: 0.2 }}
                            className="h-full bg-primary-500 rounded-full"
                        />
                    </div>
                </div>

                {/* Message */}
                <div className="mb-6">
                    <p className="text-slate-600">
                        Pour des raisons <strong>légales et de sécurité</strong>, vous devez compléter {missing} avant de pouvoir effectuer {actionLabel}.
                    </p>
                </div>

                {/* What's needed */}
                <div className="bg-slate-50 rounded-theme-lg p-4 mb-6 space-y-2">
                    <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">
                        Documents requis
                    </p>
                    <ul className="space-y-2">
                        <li className="flex items-center gap-2 text-sm text-slate-700">
                            <FileCheck className={`w-4 h-4 ${status !== 'REGISTERED' ? 'text-green-500' : 'text-slate-300'}`} />
                            <span>Informations professionnelles</span>
                        </li>
                        <li className="flex items-center gap-2 text-sm text-slate-700">
                            <FileCheck className={`w-4 h-4 ${status === 'DOCUMENTS_PENDING' || status === 'VERIFIED' ? 'text-green-500' : 'text-slate-300'}`} />
                            <span>Diplôme / Attestation</span>
                        </li>
                        <li className="flex items-center gap-2 text-sm text-slate-700">
                            <FileCheck className={`w-4 h-4 ${status === 'VERIFIED' ? 'text-green-500' : 'text-slate-300'}`} />
                            <span>Pièce d'identité</span>
                        </li>
                    </ul>
                </div>

                {/* CTA */}
                <div className="flex gap-3">
                    <button
                        onClick={onClose}
                        className="flex-1 px-4 py-3 rounded-theme-lg border border-slate-200 text-slate-700 font-medium hover:bg-slate-50 transition-colors"
                    >
                        Plus tard
                    </button>
                    <Link
                        href="/onboarding/complete"
                        className="flex-1 px-4 py-3 rounded-theme-lg bg-primary-600 text-white font-medium hover:bg-primary-700 transition-colors flex items-center justify-center gap-2"
                    >
                        Compléter
                        <ArrowRight className="w-4 h-4" />
                    </Link>
                </div>
            </motion.div>
        </motion.div>
    );
}

// =============================================================================
// EXPORTS
// =============================================================================

export { VerificationModal };
