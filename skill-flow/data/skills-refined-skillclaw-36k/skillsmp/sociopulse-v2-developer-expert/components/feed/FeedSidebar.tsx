'use client';

import Link from 'next/link';
import {
    Users,
    Activity,
    Star,
    ChevronRight,
    Clock
} from 'lucide-react';

// ===========================================
// TYPES
// ===========================================

export interface TalentPoolItem {
    id: string;
    name: string;
    role: string;
    avatar: string | null;
    rating: number;
}

export interface ActivityItem {
    id: string;
    text: string;
    time: string;
}

export interface FeedSidebarProps {
    talentPool: TalentPoolItem[];
    activity: ActivityItem[];
}

// ===========================================
// COMPONENT
// ===========================================

export function FeedSidebar({ talentPool, activity }: FeedSidebarProps) {
    return (
        <aside className="hidden lg:block w-80 flex-shrink-0 space-y-6">
            {/* Mon Vivier */}
            <div className="card-surface p-5">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="font-semibold text-slate-900 flex items-center gap-2">
                        <Users className="w-4 h-4 text-brand-600" />
                        Mon Vivier
                    </h2>
                    <Link
                        href="/vivier"
                        className="text-xs text-brand-600 font-medium hover:underline"
                    >
                        Voir tout
                    </Link>
                </div>

                <div className="space-y-3">
                    {talentPool.map((talent) => (
                        <Link
                            key={talent.id}
                            href={`/profile/${talent.id}`}
                            className="flex items-center gap-3 p-2 rounded-xl hover:bg-slate-50 transition-colors cursor-pointer group"
                        >
                            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-brand-100 to-indigo-100 flex items-center justify-center overflow-hidden">
                                {talent.avatar ? (
                                    <img
                                        src={talent.avatar}
                                        alt={talent.name}
                                        className="w-full h-full object-cover"
                                    />
                                ) : (
                                    <span className="text-sm font-semibold text-brand-600">
                                        {(talent.name || '?').charAt(0)}
                                    </span>
                                )}
                            </div>
                            <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-slate-900 truncate">
                                    {talent.name}
                                </p>
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

                {talentPool.length === 0 && (
                    <p className="text-sm text-slate-400 text-center py-4">
                        Aucun favori pour le moment
                    </p>
                )}
            </div>

            {/* Activité Récente */}
            <div className="card-surface p-5">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="font-semibold text-slate-900 flex items-center gap-2">
                        <Activity className="w-4 h-4 text-blue-500" />
                        Activité récente
                    </h2>
                </div>

                <div className="space-y-3">
                    {activity.map((item) => (
                        <div
                            key={item.id}
                            className="flex items-start gap-3 p-2 rounded-xl hover:bg-slate-50 transition-colors cursor-pointer"
                        >
                            <div className="w-2 h-2 rounded-full bg-brand-400 mt-2 flex-shrink-0" />
                            <div className="flex-1 min-w-0">
                                <p className="text-sm text-slate-700 leading-snug">
                                    {item.text}
                                </p>
                                <p className="text-xs text-slate-400 mt-1 flex items-center gap-1">
                                    <Clock className="w-3 h-3" />
                                    Il y a {item.time}
                                </p>
                            </div>
                        </div>
                    ))}
                </div>

                {activity.length === 0 && (
                    <p className="text-sm text-slate-400 text-center py-4">
                        Aucune activité récente
                    </p>
                )}
            </div>

            {/* Quick Stats Card */}
            <div className="bg-gradient-to-br from-brand-600 to-brand-700 rounded-2xl p-5 text-white">
                <h3 className="font-semibold mb-3">Cette semaine</h3>
                <div className="grid grid-cols-2 gap-3">
                    <div className="bg-white/20 rounded-xl p-3 backdrop-blur-sm">
                        <p className="text-2xl font-bold">12</p>
                        <p className="text-xs text-white/80">Nouvelles missions</p>
                    </div>
                    <div className="bg-white/20 rounded-xl p-3 backdrop-blur-sm">
                        <p className="text-2xl font-bold">5</p>
                        <p className="text-xs text-white/80">Contacts reçus</p>
                    </div>
                </div>
            </div>
        </aside>
    );
}
