'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Newspaper, CheckCircle2, Users, Star, ChevronRight, TrendingUp, ExternalLink, Sparkles } from 'lucide-react';

// ===========================================
// FEED SIDEBAR - Sticky Widgets
// Veille Pro + Activité + Stats
// ===========================================

export interface NewsItem {
    id: string;
    title: string;
    source?: string;
    url?: string;
    date?: string;
}

export interface SuccessItem {
    id: string;
    text: string;
    time: string;
    avatar?: string;
}

export interface SidebarData {
    news: NewsItem[];
    recentSuccess: SuccessItem[];
}

export interface TalentPoolItem {
    id: string;
    name: string;
    role: string;
    avatar: string | null;
    rating: number;
}

export interface FeedSidebarProps {
    talentPool?: TalentPoolItem[];
    initialData?: SidebarData;
}

const MOCK_NEWS: NewsItem[] = [
    { id: '1', title: 'Réforme Grand Âge : ce qui change en 2025', source: 'Le Monde', date: 'Il y a 2h' },
    { id: '2', title: 'Ségur de la santé : revalorisation des salaires', source: 'Ministère', date: 'Il y a 5h' },
    { id: '3', title: 'Pénurie de soignants : les solutions innovantes', source: 'Hospimedia', date: 'Hier' },
];

const MOCK_SUCCESS: SuccessItem[] = [
    { id: '1', text: 'EHPAD Les Lilas a trouvé un IDE', time: 'Il y a 15 min' },
    { id: '2', text: 'Marie D. a rejoint un atelier bien-être', time: 'Il y a 1h' },
    { id: '3', text: 'FAM Soleil a recruté 2 AES', time: 'Il y a 3h' },
];

export function FeedSidebar({ talentPool = [], initialData }: FeedSidebarProps) {
    const [sidebarData, setSidebarData] = useState<SidebarData>(initialData || { news: MOCK_NEWS, recentSuccess: MOCK_SUCCESS });

    const news = sidebarData.news.length > 0 ? sidebarData.news : MOCK_NEWS;
    const recentSuccess = sidebarData.recentSuccess.length > 0 ? sidebarData.recentSuccess : MOCK_SUCCESS;

    return (
        <div className="space-y-6">
            {/* Widget 1: Veille Sectorielle */}
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.1 }} className="bg-white rounded-2xl shadow-soft overflow-hidden">
                <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <div className="h-8 w-8 rounded-xl bg-indigo-50 grid place-items-center">
                            <Newspaper className="w-4 h-4 text-indigo-600" />
                        </div>
                        <h3 className="font-semibold text-slate-900">Veille Pro</h3>
                    </div>
                    <span className="text-[10px] uppercase tracking-wider text-slate-400 font-semibold">Actualités</span>
                </div>
                <div className="divide-y divide-slate-50">
                    {news.slice(0, 3).map((item) => (
                        <Link key={item.id} href={item.url || '#'} target={item.url ? '_blank' : undefined} className="block px-5 py-3.5 hover:bg-slate-50 transition-colors group">
                            <p className="text-sm font-medium text-slate-800 leading-snug line-clamp-2 group-hover:text-indigo-600 transition-colors">{item.title}</p>
                            <div className="flex items-center gap-2 mt-1.5 text-xs text-slate-400">
                                {item.source && <span>{item.source}</span>}
                                {item.source && item.date && <span>•</span>}
                                {item.date && <span>{item.date}</span>}
                                {item.url && <ExternalLink className="w-3 h-3 ml-auto opacity-0 group-hover:opacity-100 transition-opacity" />}
                            </div>
                        </Link>
                    ))}
                </div>
            </motion.div>

            {/* Widget 2: Activité */}
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.2 }} className="bg-white rounded-2xl shadow-soft overflow-hidden">
                <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <div className="h-8 w-8 rounded-xl bg-teal-50 grid place-items-center">
                            <CheckCircle2 className="w-4 h-4 text-teal-600" />
                        </div>
                        <h3 className="font-semibold text-slate-900">Activité</h3>
                    </div>
                    <span className="relative flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-teal-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-teal-500"></span>
                    </span>
                </div>
                <div className="divide-y divide-slate-50">
                    {recentSuccess.slice(0, 4).map((item) => (
                        <div key={item.id} className="px-5 py-3.5 flex items-center gap-3">
                            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-teal-400 to-teal-500 grid place-items-center">
                                <CheckCircle2 className="w-4 h-4 text-white" />
                            </div>
                            <div className="flex-1 min-w-0">
                                <p className="text-sm text-slate-700 leading-snug">{item.text}</p>
                                <p className="text-xs text-slate-400 mt-0.5">{item.time}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </motion.div>

            {/* Widget 3: Mon Vivier */}
            {talentPool.length > 0 && (
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.3 }} className="bg-white rounded-2xl shadow-soft overflow-hidden">
                    <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <div className="h-8 w-8 rounded-xl bg-violet-50 grid place-items-center">
                                <Users className="w-4 h-4 text-violet-600" />
                            </div>
                            <h3 className="font-semibold text-slate-900">Mon Vivier</h3>
                        </div>
                        <Link href="/vivier" className="text-xs text-indigo-600 font-medium hover:underline">Voir tout</Link>
                    </div>
                    <div className="divide-y divide-slate-50">
                        {talentPool.slice(0, 5).map((talent) => (
                            <Link key={talent.id} href={`/profile/${talent.id}`} className="flex items-center gap-3 px-5 py-3 hover:bg-slate-50 transition-colors group">
                                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-100 to-violet-100 flex items-center justify-center overflow-hidden">
                                    {talent.avatar ? <img src={talent.avatar} alt={talent.name} className="w-full h-full object-cover" /> : <span className="text-sm font-semibold text-indigo-600">{(talent.name || '?').charAt(0)}</span>}
                                </div>
                                <div className="flex-1 min-w-0">
                                    <p className="text-sm font-medium text-slate-900 truncate">{talent.name}</p>
                                    <p className="text-xs text-slate-500">{talent.role}</p>
                                </div>
                                <div className="flex items-center gap-1 text-xs">
                                    <Star className="w-3 h-3 text-amber-400 fill-amber-400" />
                                    <span className="font-medium">{talent.rating}</span>
                                </div>
                                <ChevronRight className="w-4 h-4 text-slate-300 group-hover:text-slate-500 transition-colors" />
                            </Link>
                        ))}
                    </div>
                </motion.div>
            )}

            {/* Widget 4: Quick Stats */}
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.4 }} className="bg-gradient-to-br from-indigo-600 via-indigo-600 to-teal-500 rounded-2xl p-5 text-white shadow-lg">
                <div className="flex items-center gap-2 mb-4">
                    <div className="h-8 w-8 rounded-xl bg-white/20 grid place-items-center">
                        <TrendingUp className="w-4 h-4" />
                    </div>
                    <h3 className="font-semibold">Cette semaine</h3>
                </div>
                <div className="grid grid-cols-2 gap-3">
                    <div className="bg-white/15 rounded-xl p-4 backdrop-blur-sm">
                        <p className="text-3xl font-bold">12</p>
                        <p className="text-xs text-white/80 mt-0.5">Nouvelles missions</p>
                    </div>
                    <div className="bg-white/15 rounded-xl p-4 backdrop-blur-sm">
                        <p className="text-3xl font-bold">5</p>
                        <p className="text-xs text-white/80 mt-0.5">Contacts reçus</p>
                    </div>
                </div>
            </motion.div>

            {/* Widget 5: CTA Premium */}
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.5 }} className="relative bg-white rounded-2xl shadow-soft overflow-hidden border border-slate-200">
                <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-indigo-100 to-transparent rounded-bl-[100px]" />
                <div className="relative p-5">
                    <div className="flex items-center gap-2 mb-3">
                        <Sparkles className="w-5 h-5 text-indigo-600" />
                        <span className="text-[10px] uppercase tracking-wider text-indigo-600 font-bold">Premium</span>
                    </div>
                    <h4 className="font-bold text-slate-900 mb-1">Boostez votre visibilité</h4>
                    <p className="text-sm text-slate-600 mb-4">Mettez-vous en avant auprès des établissements.</p>
                    <button className="w-full py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-teal-500 text-white text-sm font-semibold hover:shadow-md transition-shadow">Découvrir</button>
                </div>
            </motion.div>
        </div>
    );
}
