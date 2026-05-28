'use client';

import { useState } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { ArrowRight, Sparkles } from 'lucide-react';
import { currentBrand, isMedical } from '@/lib/brand';

// ===========================================
// REGISTRATION CTA - Floating bottom banner
// Encourages visitors to sign up
// ===========================================

interface RegistrationCTAProps {
    viewMode: 'establishment' | 'talent';
}

export function RegistrationCTA({ viewMode }: RegistrationCTAProps) {
    const [isVisible, setIsVisible] = useState(true);

    if (!isVisible) return null;

    const isEstablishment = viewMode === 'establishment';

    const headline = isEstablishment
        ? (isMedical() ? 'Trouvez vos renforts soignants' : 'Trouvez vos talents')
        : (isMedical() ? 'Trouvez des missions soins' : 'Trouvez des missions');

    const ctaLabel = isEstablishment ? 'Publier une mission' : 'Créer mon profil';
    const ctaHref = isEstablishment ? '/register?role=client' : '/register?role=talent';

    return (
        <motion.div
            initial={{ y: 100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 1.5, duration: 0.5 }}
            className="fixed bottom-0 left-0 right-0 z-50 p-4 pb-safe"
        >
            <div className="max-w-2xl mx-auto">
                <div className={`
                    relative overflow-hidden
                    rounded-2xl p-4 sm:p-5
                    bg-white/95 backdrop-blur-xl
                    border border-slate-200
                    shadow-soft-lg
                `}>
                    {/* Gradient accent */}
                    <div
                        className={`
                            absolute inset-x-0 top-0 h-1
                            bg-gradient-to-r
                            ${isMedical()
                                ? 'from-alert-500 via-alert-400 to-rose-400'
                                : 'from-live-500 via-brand-500 to-indigo-500'
                            }
                        `}
                    />

                    <div className="flex items-center justify-between gap-4">
                        <div className="flex items-center gap-3">
                            <div className={`
                                p-2 rounded-full
                                ${isMedical() ? 'bg-alert-100' : 'bg-live-100'}
                            `}>
                                <Sparkles className={`
                                    h-5 w-5
                                    ${isMedical() ? 'text-alert-600' : 'text-live-600'}
                                `} />
                            </div>
                            <div>
                                <p className="font-semibold text-slate-900">
                                    {headline}
                                </p>
                                <p className="text-sm text-slate-500 hidden sm:block">
                                    Inscription gratuite en 2 minutes
                                </p>
                            </div>
                        </div>

                        <Link
                            href={ctaHref}
                            className={`
                                inline-flex items-center gap-2
                                px-5 py-2.5 rounded-full
                                font-semibold text-sm text-white
                                bg-gradient-to-r
                                ${isMedical()
                                    ? 'from-alert-600 to-alert-700 hover:from-alert-700 hover:to-alert-800'
                                    : 'from-brand-600 to-brand-700 hover:from-brand-700 hover:to-brand-800'
                                }
                                shadow-sm hover:shadow-md
                                active:scale-[0.98]
                                transition-all duration-200
                            `}
                        >
                            {ctaLabel}
                            <ArrowRight className="h-4 w-4" />
                        </Link>
                    </div>

                    {/* Close button */}
                    <button
                        onClick={() => setIsVisible(false)}
                        className="absolute top-2 right-2 p-1 text-slate-400 hover:text-slate-600 transition-colors"
                        aria-label="Fermer"
                    >
                        <span className="text-lg">×</span>
                    </button>
                </div>
            </div>
        </motion.div>
    );
}
