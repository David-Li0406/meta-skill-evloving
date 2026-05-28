'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Newspaper,
    Activity,
    TrendingUp,
    CheckCircle2,
    UserCheck,
    Briefcase,
    Clock,
    ArrowRight,
    Sparkles
} from 'lucide-react';
import { isMedical, currentBrand } from '@/lib/brand';

// ===========================================
// SOCIAL PROOF SIDEBAR
// Sticky sidebar with Veille Pro, Activity, Stats, Premium
// Inspired by original SocioPulse design
// ===========================================

// Fake news data
const NEWS_ITEMS = isMedical()
    ? [
        { title: "Réforme Grand Âge : ce qui change en 2026", source: "Le Monde", time: "2h" },
        { title: "Ségur de la santé : revalorisation des salaires", source: "Ministère", time: "8h" },
        { title: "Pénurie de soignants : les solutions innovantes", source: "Hospimedia", time: "Hier" },
    ]
    : [
        { title: "Réforme Grand Âge : ce qui change en 2026", source: "Le Monde", time: "2h" },
        { title: "Ségur de la santé : revalorisation des salaires", source: "Ministère", time: "8h" },
        { title: "Pénurie de soignants : les solutions innovantes", source: "Hospimedia", time: "Hier" },
    ];

// Fake activity data
const ACTIVITY_ITEMS = isMedical()
    ? [
        { icon: CheckCircle2, text: "EHPAD Les Lilas a trouvé un IDE", time: "13min", color: "text-emerald-500" },
        { icon: UserCheck, text: "Marie D. a rejoint un atelier bien-être", time: "1h", color: "text-violet-500" },
        { icon: Briefcase, text: "FAM Soleil a recruté 2 AES", time: "3h", color: "text-blue-500" },
    ]
    : [
        { icon: CheckCircle2, text: "MECS Horizon a trouvé un Éducateur", time: "15min", color: "text-emerald-500" },
        { icon: UserCheck, text: "Thomas D. a rejoint un atelier Sophrologie", time: "1h", color: "text-violet-500" },
        { icon: Briefcase, text: "IME Les Oliviers a recruté 2 ME", time: "2h", color: "text-blue-500" },
    ];

export function SocialProofSidebar() {
    const [activityIndex, setActivityIndex] = useState(0);

    // Rotate activity items
    useEffect(() => {
        const interval = setInterval(() => {
            setActivityIndex(prev => (prev + 1) % ACTIVITY_ITEMS.length);
        }, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <aside className="hidden lg:block w-80 flex-shrink-0">
            <div className="sticky top-24 space-y-4 sidebar-tilt">

                {/* ========== VEILLE PRO ========== */}
                <div className="glass-card-premium shine-sweep rounded-2xl p-5">
                    <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-2">
                            <Newspaper className="h-4 w-4 text-violet-500" />
                            <h3 className="font-bold text-slate-900 text-sm">Veille Pro</h3>
                        </div>
                        <span className="text-[10px] text-slate-400 uppercase tracking-wider">Actualités</span>
                    </div>

                    <div className="space-y-4">
                        {NEWS_ITEMS.map((news, i) => (
                            <div key={i} className="group cursor-pointer">
                                <p className="text-sm text-slate-700 leading-snug group-hover:text-brand-600 transition-colors">
                                    {news.title}
                                </p>
                                <div className="flex items-center gap-2 mt-1 text-xs text-slate-400">
                                    <span>{news.source}</span>
                                    <span>•</span>
                                    <span>Il y a {news.time}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* ========== ACTIVITÉ ========== */}
                <div className="glass-card-premium rounded-2xl p-5">
                    <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-2">
                            <div className="relative">
                                <Activity className="h-4 w-4 text-emerald-500" />
                                <span className="absolute -top-1 -right-1 h-2 w-2 bg-red-500 rounded-full animate-pulse" />
                            </div>
                            <h3 className="font-bold text-slate-900 text-sm">Activité</h3>
                        </div>
                        <TrendingUp className="h-4 w-4 text-emerald-500" />
                    </div>

                    <div className="space-y-3">
                        <AnimatePresence mode="popLayout">
                            {ACTIVITY_ITEMS.map((item, i) => {
                                const Icon = item.icon;
                                return (
                                    <motion.div
                                        key={`${item.text}-${i}`}
                                        initial={{ opacity: 0, x: -10 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ delay: i * 0.1 }}
                                        className="flex items-start gap-3"
                                    >
                                        <div className="h-8 w-8 rounded-full bg-slate-100 flex items-center justify-center flex-shrink-0">
                                            <Icon className={`h-4 w-4 ${item.color}`} />
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <p className="text-sm text-slate-700 leading-snug">{item.text}</p>
                                            <span className="text-xs text-slate-400">Il y a {item.time}</span>
                                        </div>
                                    </motion.div>
                                );
                            })}
                        </AnimatePresence>
                    </div>
                </div>

                {/* ========== STATS CETTE SEMAINE ========== */}
                <div className={`rounded-2xl p-5 ${isMedical()
                    ? 'bg-gradient-to-br from-rose-500 to-rose-600'
                    : 'bg-gradient-to-br from-teal-500 to-teal-600'
                    }`}>
                    <div className="flex items-center gap-2 mb-4">
                        <Clock className="h-4 w-4 text-white/80" />
                        <h3 className="font-semibold text-white text-sm">Cette semaine</h3>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div className="text-center">
                            <p className="text-3xl font-black text-white">12</p>
                            <p className="text-xs text-white/80 mt-1">Nouvelles missions</p>
                        </div>
                        <div className="text-center">
                            <p className="text-3xl font-black text-white">5</p>
                            <p className="text-xs text-white/80 mt-1">Contacts reçus</p>
                        </div>
                    </div>
                </div>

                {/* ========== PREMIUM TEASER ========== */}
                <div className="bg-slate-900 rounded-2xl p-5 text-white">
                    <div className="flex items-center gap-2 mb-3">
                        <Sparkles className="h-4 w-4 text-amber-400" />
                        <span className="text-xs text-slate-400 uppercase tracking-wider">Premium</span>
                    </div>

                    <h4 className="font-bold text-white mb-2">Boostez votre visibilité</h4>
                    <p className="text-sm text-slate-400 mb-4">
                        Mettez-vous en avant auprès des établissements.
                    </p>

                    <Link
                        href="/premium"
                        className={`inline-flex items-center justify-center w-full gap-2 px-4 py-2.5 rounded-xl font-semibold text-sm transition-all ${isMedical()
                            ? 'bg-rose-500 hover:bg-rose-400 text-white'
                            : 'bg-teal-500 hover:bg-teal-400 text-white'
                            }`}
                    >
                        Découvrir
                        <ArrowRight className="h-4 w-4" />
                    </Link>
                </div>

            </div>
        </aside>
    );
}
