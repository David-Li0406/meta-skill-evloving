'use client';

import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import Link from 'next/link';
import { Building2, User, ArrowRight, Sparkles } from 'lucide-react';
import { isMedical } from '@/lib/brand';

// ===========================================
// FINAL CTA SECTION
// Dual CTA for Establishments vs Professionals
// ===========================================

export function FinalCTA() {
    const ref = useRef(null);
    const isInView = useInView(ref, { once: true, amount: 0.5 });

    const brandGradient = isMedical()
        ? 'from-rose-500 via-pink-500 to-violet-600'
        : 'from-teal-500 via-brand-500 to-indigo-600';

    return (
        <section
            ref={ref}
            className={`relative py-24 px-4 sm:px-6 overflow-hidden bg-gradient-to-br ${brandGradient}`}
        >
            {/* Background Pattern */}
            <div className="absolute inset-0 opacity-10">
                <div className="absolute inset-0" style={{
                    backgroundImage: `radial-gradient(circle at 2px 2px, white 1px, transparent 0)`,
                    backgroundSize: '40px 40px',
                }} />
            </div>

            {/* Floating Elements */}
            <motion.div
                animate={{ y: [-10, 10, -10] }}
                transition={{ duration: 6, repeat: Infinity }}
                className="absolute top-20 left-10 w-20 h-20 rounded-full bg-white/10 blur-xl"
            />
            <motion.div
                animate={{ y: [10, -10, 10] }}
                transition={{ duration: 8, repeat: Infinity }}
                className="absolute bottom-20 right-20 w-32 h-32 rounded-full bg-white/10 blur-xl"
            />

            <div className="max-w-5xl mx-auto relative z-10">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={isInView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-12"
                >
                    {/* Badge */}
                    <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/20 text-white text-sm font-semibold mb-6 backdrop-blur-sm">
                        <Sparkles className="h-4 w-4" />
                        Rejoignez-nous gratuitement
                    </span>

                    {/* Title */}
                    <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-4">
                        Prêt à transformer votre recrutement ?
                    </h2>
                    <p className="text-lg sm:text-xl text-white/80 max-w-2xl mx-auto">
                        Que vous soyez un établissement à la recherche de renforts ou un professionnel disponible, inscrivez-vous en 2 minutes.
                    </p>
                </motion.div>

                {/* Dual CTA Cards */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={isInView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.6, delay: 0.2 }}
                    className="grid sm:grid-cols-2 gap-6 max-w-3xl mx-auto"
                >
                    {/* Establishment Card */}
                    <Link href="/auth/login?type=establishment" className="group">
                        <div className="p-8 rounded-3xl bg-white text-center shadow-2xl shadow-slate-900/10 transition-all duration-300 ease-out group-hover:scale-[1.03] group-hover:shadow-3xl group-hover:-translate-y-1">
                            <div className={`inline-flex p-4 rounded-2xl mb-6 transition-transform group-hover:scale-110 ${isMedical() ? 'bg-rose-100 text-rose-600' : 'bg-teal-100 text-teal-600'
                                }`}>
                                <Building2 className="h-8 w-8" />
                            </div>
                            <h3 className="text-xl font-bold text-slate-900 mb-2">
                                Je suis un établissement
                            </h3>
                            <p className="text-slate-600 mb-6">
                                Publiez vos besoins, recevez des candidatures qualifiées.
                            </p>
                            <span className={`inline-flex items-center gap-2 px-6 py-3 rounded-xl font-semibold text-white shadow-lg transition-all group-hover:shadow-xl ${isMedical()
                                ? 'bg-gradient-to-r from-rose-500 via-rose-500 to-pink-500'
                                : 'bg-gradient-to-r from-teal-500 via-teal-500 to-emerald-500'
                                }`}>
                                Commencer
                                <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                            </span>
                        </div>
                    </Link>

                    {/* Professional Card */}
                    <Link href="/auth/login?type=professional" className="group">
                        <div className="p-8 rounded-3xl bg-white/10 backdrop-blur-md border border-white/30 text-center transition-all duration-300 ease-out group-hover:scale-[1.03] group-hover:bg-white/20 group-hover:-translate-y-1 group-hover:border-white/40">
                            <div className="inline-flex p-4 rounded-2xl bg-white/20 text-white mb-6 transition-transform group-hover:scale-110">
                                <User className="h-8 w-8" />
                            </div>
                            <h3 className="text-xl font-bold text-white mb-2">
                                Je suis un professionnel
                            </h3>
                            <p className="text-white/80 mb-6">
                                Trouvez des missions près de chez vous, en toute flexibilité.
                            </p>
                            <span className="inline-flex items-center gap-2 px-6 py-3 rounded-xl font-semibold text-slate-900 bg-white shadow-lg transition-all group-hover:shadow-xl">
                                S'inscrire
                                <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                            </span>
                        </div>
                    </Link>
                </motion.div>
            </div>
        </section>
    );
}
