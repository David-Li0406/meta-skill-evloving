'use client';

import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Newspaper,
    Activity,
    Sparkles,
    Lock,
    CheckCircle2,
    Clock,
    TrendingUp,
    Building2,
    UserCheck,
    Briefcase
} from 'lucide-react';
import { isMedical } from '@/lib/brand';

// ===========================================
// HERO LIVE SIDEBAR - Floating Activity Widget
// SaaS 2026 Aesthetic - Real-time Vibe
// ===========================================

// Fake news data for AI Veille section
const NEWS_ITEMS = isMedical()
    ? [
        { title: 'Ségur de la Santé : nouveaux décrets sur les revalorisations', time: '2h' },
        { title: 'Pénurie IDE : +15% de missions en Île-de-France', time: '5h' },
    ]
    : [
        { title: 'CASF : nouvelles recommandations pour les MECS', time: '3h' },
        { title: 'Formation continue : les aides disponibles en 2026', time: '6h' },
    ];

// Fake live activity data
const LIVE_ACTIVITIES = isMedical()
    ? [
        { type: 'hire', org: 'Clinique Pasteur', action: 'a recruté 2 IDE', time: '2m', icon: CheckCircle2, color: 'text-emerald-500' },
        { type: 'mission', org: 'EHPAD Les Tilleuls', action: 'nouvelle mission AS', time: '5m', icon: Briefcase, color: 'text-blue-500' },
        { type: 'signup', org: 'Marie L.', action: 's\'est inscrite (IDE)', time: '8m', icon: UserCheck, color: 'text-violet-500' },
        { type: 'hire', org: 'CH Bordeaux', action: 'a recruté 1 AES', time: '12m', icon: CheckCircle2, color: 'text-emerald-500' },
        { type: 'mission', org: 'SSIAD Nantes', action: '3 missions publiées', time: '15m', icon: Briefcase, color: 'text-blue-500' },
    ]
    : [
        { type: 'hire', org: 'MECS Les Oliviers', action: 'a recruté 1 Éducateur', time: '2m', icon: CheckCircle2, color: 'text-emerald-500' },
        { type: 'mission', org: 'IME Horizon', action: 'nouvelle mission ME', time: '4m', icon: Briefcase, color: 'text-blue-500' },
        { type: 'signup', org: 'Thomas D.', action: 's\'est inscrit (ES)', time: '7m', icon: UserCheck, color: 'text-violet-500' },
        { type: 'atelier', org: 'SocioLive', action: 'Atelier Sophrologie disponible', time: '10m', icon: Sparkles, color: 'text-amber-500' },
        { type: 'hire', org: 'Foyer Espérance', action: 'a recruté 2 Animateurs', time: '18m', icon: CheckCircle2, color: 'text-emerald-500' },
    ];

export function HeroLiveSidebar() {
    const [visibleActivities, setVisibleActivities] = useState(LIVE_ACTIVITIES.slice(0, 3));
    const [activityIndex, setActivityIndex] = useState(3);

    // Rotate activities every 4 seconds
    useEffect(() => {
        const interval = setInterval(() => {
            setActivityIndex((prev) => {
                const next = (prev + 1) % LIVE_ACTIVITIES.length;
                setVisibleActivities((current) => {
                    const newActivities = [...current.slice(1), LIVE_ACTIVITIES[next]];
                    return newActivities;
                });
                return next;
            });
        }, 4000);

        return () => clearInterval(interval);
    }, []);

    return (
        <motion.aside
            initial={{ opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.8, ease: [0.22, 1, 0.36, 1] }}
            className="hidden lg:block w-[350px] flex-shrink-0"
        >
            <div className="glass-panel rounded-3xl overflow-hidden animate-float">
                {/* ========== SECTION 1: AI NEWS / VEILLE ========== */}
                <div className="p-5 border-b border-slate-200/50">
                    <div className="flex items-center gap-2 mb-4">
                        <div className="h-8 w-8 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center">
                            <Newspaper className="h-4 w-4 text-white" />
                        </div>
                        <div>
                            <h3 className="text-sm font-bold text-slate-900">Veille Pro AI</h3>
                            <p className="text-[10px] text-slate-500 uppercase tracking-wider">Powered by Vertex</p>
                        </div>
                        <Sparkles className="h-4 w-4 text-amber-400 ml-auto" />
                    </div>

                    <div className="space-y-3">
                        {NEWS_ITEMS.map((news, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 1 + i * 0.15 }}
                                className="group cursor-pointer"
                            >
                                <p className="text-sm text-slate-700 leading-snug group-hover:text-brand-600 transition-colors line-clamp-2">
                                    {news.title}
                                </p>
                                <div className="flex items-center gap-1.5 mt-1">
                                    <Clock className="h-3 w-3 text-slate-400" />
                                    <span className="text-[11px] text-slate-400">il y a {news.time}</span>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>

                {/* ========== SECTION 2: LIVE ACTIVITY ========== */}
                <div className="p-5 border-b border-slate-200/50">
                    <div className="flex items-center gap-2 mb-4">
                        <div className="relative h-8 w-8 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center">
                            <Activity className="h-4 w-4 text-white" />
                            {/* Live Pulse */}
                            <span className="absolute -top-1 -right-1 h-3 w-3 bg-red-500 rounded-full border-2 border-white animate-pulse" />
                        </div>
                        <div>
                            <h3 className="text-sm font-bold text-slate-900">Activité en direct</h3>
                            <p className="text-[10px] text-slate-500 uppercase tracking-wider">Temps réel</p>
                        </div>
                        <TrendingUp className="h-4 w-4 text-emerald-500 ml-auto" />
                    </div>

                    <div className="space-y-2.5 min-h-[140px]">
                        <AnimatePresence mode="popLayout">
                            {visibleActivities.map((activity, i) => {
                                const Icon = activity.icon;
                                return (
                                    <motion.div
                                        key={`${activity.org}-${activity.time}-${i}`}
                                        initial={{ opacity: 0, y: -20, scale: 0.95 }}
                                        animate={{ opacity: 1, y: 0, scale: 1 }}
                                        exit={{ opacity: 0, y: 20, scale: 0.95 }}
                                        transition={{ duration: 0.4 }}
                                        className="flex items-start gap-3 p-2.5 rounded-xl bg-white/50 hover:bg-white/80 transition-colors"
                                    >
                                        <div className={`h-8 w-8 rounded-full bg-slate-100 flex items-center justify-center flex-shrink-0`}>
                                            <Icon className={`h-4 w-4 ${activity.color}`} />
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <p className="text-sm text-slate-800 leading-snug">
                                                <span className="font-semibold">{activity.org}</span>{' '}
                                                <span className="text-slate-600">{activity.action}</span>
                                            </p>
                                            <span className="text-[11px] text-slate-400">il y a {activity.time}</span>
                                        </div>
                                    </motion.div>
                                );
                            })}
                        </AnimatePresence>
                    </div>
                </div>

                {/* ========== SECTION 3: PREMIUM TEASER ========== */}
                <div className="p-5 relative">
                    {/* Blur Overlay */}
                    <div className="absolute inset-0 bg-gradient-to-t from-white/90 via-white/70 to-transparent backdrop-blur-[2px] z-10 flex items-center justify-center">
                        <div className="text-center">
                            <div className="h-12 w-12 rounded-2xl bg-slate-900/90 flex items-center justify-center mx-auto mb-3 shadow-lg">
                                <Lock className="h-5 w-5 text-white" />
                            </div>
                            <p className="text-sm font-bold text-slate-900">Fonctionnalité Premium</p>
                            <p className="text-xs text-slate-500 mt-1">Bientôt disponible</p>
                        </div>
                    </div>

                    {/* Blurred Content Behind */}
                    <div className="opacity-40 pointer-events-none select-none">
                        <div className="flex items-center gap-2 mb-3">
                            <div className="h-8 w-8 rounded-xl bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center">
                                <Building2 className="h-4 w-4 text-white" />
                            </div>
                            <div>
                                <h3 className="text-sm font-bold text-slate-900">Analytics Pro</h3>
                                <p className="text-[10px] text-slate-500">Tableaux de bord avancés</p>
                            </div>
                        </div>
                        <div className="h-20 bg-slate-100 rounded-xl" />
                    </div>
                </div>
            </div>
        </motion.aside>
    );
}
