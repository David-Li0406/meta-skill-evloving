'use client';

import Link from 'next/link';
import {
    Users,
    TrendingUp,
    Siren,
    ChevronRight,
    Star,
    Plus,
    MapPin
} from 'lucide-react';
import { Badge } from '@/components/ui';

// Mock suggestions data
const suggestedTalents = [
    { id: '1', name: 'Sophie Martin', role: 'Art-thérapeute', rating: 5.0, city: 'Lyon' },
    { id: '2', name: 'Pierre Dubois', role: 'AMP', rating: 4.6, city: 'Villeurbanne' },
    { id: '3', name: 'Claire Bernard', role: 'Infirmière', rating: 4.9, city: 'Lyon' },
];

const trendingMissions = [
    { id: '1', title: 'Aide-soignant(e) Nuit', city: 'Lyon 3ème', count: 5 },
    { id: '2', title: 'Éducateur spécialisé', city: 'Villeurbanne', count: 3 },
    { id: '3', title: 'AMP Weekend', city: 'Lyon 6ème', count: 2 },
];

export function FeedSuggestions() {
    return (
        <div className="space-y-4">
            {/* Who to Follow */}
            <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
                <div className="flex items-center justify-between border-b border-slate-100 px-4 py-3">
                    <h3 className="font-semibold text-slate-900">Talents à suivre</h3>
                    <Users className="h-4 w-4 text-slate-400" />
                </div>
                <div className="divide-y divide-slate-100">
                    {suggestedTalents.map((talent) => (
                        <div key={talent.id} className="flex items-center gap-3 p-3">
                            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-purple-100 text-sm font-medium text-purple-600">
                                {talent.name.charAt(0)}
                            </div>
                            <div className="flex-1 min-w-0">
                                <p className="font-medium text-slate-900 truncate">{talent.name}</p>
                                <p className="text-xs text-slate-500">{talent.role}</p>
                            </div>
                            <button className="rounded-full border border-teal-200 px-3 py-1 text-xs font-medium text-teal-600 transition-colors hover:bg-teal-50">
                                <Plus className="h-3 w-3" />
                            </button>
                        </div>
                    ))}
                </div>
                <Link
                    href="/vivier"
                    className="flex items-center justify-between border-t border-slate-100 px-4 py-3 text-sm font-medium text-teal-600 transition-colors hover:bg-slate-50"
                >
                    Voir plus de talents
                    <ChevronRight className="h-4 w-4" />
                </Link>
            </div>

            {/* Trending Missions */}
            <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
                <div className="flex items-center justify-between border-b border-slate-100 px-4 py-3">
                    <h3 className="font-semibold text-slate-900">Missions tendance</h3>
                    <TrendingUp className="h-4 w-4 text-slate-400" />
                </div>
                <div className="divide-y divide-slate-100">
                    {trendingMissions.map((mission) => (
                        <Link
                            key={mission.id}
                            href="/sos"
                            className="flex items-center gap-3 p-3 transition-colors hover:bg-slate-50"
                        >
                            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-rose-50 text-rose-600">
                                <Siren className="h-5 w-5" />
                            </div>
                            <div className="flex-1 min-w-0">
                                <p className="font-medium text-slate-900 truncate">{mission.title}</p>
                                <p className="flex items-center gap-1 text-xs text-slate-500">
                                    <MapPin className="h-3 w-3" />
                                    {mission.city}
                                </p>
                            </div>
                            <Badge variant="secondary" size="sm">
                                {mission.count} offres
                            </Badge>
                        </Link>
                    ))}
                </div>
                <Link
                    href="/fil-pro"
                    className="flex items-center justify-between border-t border-slate-100 px-4 py-3 text-sm font-medium text-teal-600 transition-colors hover:bg-slate-50"
                >
                    Toutes les missions
                    <ChevronRight className="h-4 w-4" />
                </Link>
            </div>

            {/* Footer */}
            <div className="px-2 text-xs text-slate-400">
                <p>SocioPulse © 2026</p>
                <p className="mt-1">Conditions · Confidentialité · Aide</p>
            </div>
        </div>
    );
}
