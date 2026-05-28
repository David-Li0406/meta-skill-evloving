'use client';

import {
    Eye,
    Users,
    Sparkles,
    Rocket,
    Clock,
    MapPin,
    ChevronRight
} from 'lucide-react';
import { Badge } from '@/components/ui';

interface ActiveMissionCardProps {
    mission: {
        id: string;
        title: string;
        date: string;
        location: string;
        status: 'PUBLISHED' | 'DRAFT' | 'CLOSED';
        urgency: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
        views: number;
        applicants: number;
        matchingProfiles: number;
        createdAt: Date;
    };
}

export function ActiveMissionCard({ mission }: ActiveMissionCardProps) {
    const isUrgentAndLowActivity = mission.urgency === 'CRITICAL' && mission.applicants === 0;

    return (
        <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
            {/* Header */}
            <div className="flex flex-col gap-4 border-b border-slate-100 p-6 sm:flex-row sm:items-start sm:justify-between">
                <div>
                    <div className="flex items-center gap-3">
                        <h1 className="text-xl font-bold text-slate-900">{mission.title}</h1>
                        <Badge variant={mission.status === 'PUBLISHED' ? 'success' : 'secondary'}>
                            {mission.status === 'PUBLISHED' ? 'Diffusée' : mission.status}
                        </Badge>
                        {mission.urgency === 'CRITICAL' && (
                            <Badge variant="destructive">Urgent</Badge>
                        )}
                    </div>
                    <div className="mt-2 flex items-center gap-4 text-sm text-slate-500">
                        <span className="flex items-center gap-1">
                            <Clock className="h-4 w-4" />
                            {mission.date}
                        </span>
                        <span className="flex items-center gap-1">
                            <MapPin className="h-4 w-4" />
                            {mission.location}
                        </span>
                    </div>
                </div>

                {isUrgentAndLowActivity && (
                    <div className="flex items-center gap-3 rounded-lg border border-amber-200 bg-amber-50 p-3">
                        <div className="rounded-full bg-amber-100 p-2 text-amber-600">
                            <Rocket className="h-4 w-4" />
                        </div>
                        <div>
                            <p className="text-sm font-medium text-amber-900">Peu de candidats ?</p>
                            <button className="text-xs font-medium text-amber-700 hover:text-amber-800 hover:underline">
                                Booster la visibilité
                            </button>
                        </div>
                    </div>
                )}
            </div>

            {/* KPI Section */}
            <div className="grid grid-cols-1 divide-y divide-slate-100 sm:grid-cols-3 sm:divide-x sm:divide-y-0">
                <div className="p-6 text-center sm:text-left">
                    <div className="flex items-center justify-center gap-2 sm:justify-start">
                        <div className="rounded-lg bg-blue-50 p-2 text-blue-600">
                            <Eye className="h-5 w-5" />
                        </div>
                        <span className="text-sm font-medium text-slate-500">Vues</span>
                    </div>
                    <p className="mt-2 text-2xl font-bold text-slate-900">{mission.views}</p>
                </div>

                <div className="p-6 text-center sm:text-left">
                    <div className="flex items-center justify-center gap-2 sm:justify-start">
                        <div className="rounded-lg bg-teal-50 p-2 text-teal-600">
                            <Users className="h-5 w-5" />
                        </div>
                        <span className="text-sm font-medium text-slate-500">Candidatures</span>
                    </div>
                    <p className="mt-2 text-2xl font-bold text-slate-900">{mission.applicants}</p>
                </div>

                <div className="bg-gradient-to-br from-indigo-50 to-purple-50 p-6 text-center sm:text-left">
                    <div className="flex items-center justify-center gap-2 sm:justify-start">
                        <div className="rounded-lg bg-white p-2 text-indigo-600 shadow-sm">
                            <Sparkles className="h-5 w-5" />
                        </div>
                        <span className="text-sm font-medium text-indigo-900">AI Matching</span>
                    </div>
                    <div className="mt-2 text-left">
                        <p className="font-semibold text-indigo-900">
                            {mission.matchingProfiles} profils correspondent
                        </p>
                        <button className="mt-2 inline-flex items-center gap-1 text-sm font-medium text-indigo-600 hover:text-indigo-700">
                            Inviter à postuler
                            <ChevronRight className="h-4 w-4" />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
