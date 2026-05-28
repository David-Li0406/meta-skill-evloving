'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import {
    ClipboardList,
    Calendar,
    MapPin,
    Clock,
    ChevronRight,
    CheckCircle2,
    PlayCircle,
    AlertCircle,
    Loader2
} from 'lucide-react';

interface Mission {
    id: string;
    title: string;
    jobTitle: string;
    status: 'ASSIGNED' | 'IN_PROGRESS';
    startDate: string;
    endDate: string;
    city: string;
    client?: {
        id: string;
        establishment?: {
            name: string;
            logoUrl?: string;
        };
    };
    assignedTalent?: {
        id: string;
        profile?: {
            firstName: string;
            lastName: string;
            avatarUrl?: string;
        };
    };
    instructions?: {
        isAcknowledged: boolean;
    };
}

export default function TrackingDashboardPage() {
    const [missions, setMissions] = useState<Mission[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchActiveMissions = async () => {
            try {
                // TODO: Replace with actual API call
                // const response = await fetch('/api/missions/active');
                // const data = await response.json();
                // setMissions(data);

                // Mock data for now
                setMissions([]);
                setIsLoading(false);
            } catch (err) {
                setError('Erreur lors du chargement des missions');
                setIsLoading(false);
            }
        };

        fetchActiveMissions();
    }, []);

    const getStatusBadge = (mission: Mission) => {
        if (mission.status === 'IN_PROGRESS') {
            return (
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700">
                    <PlayCircle className="w-3 h-3" />
                    En cours
                </span>
            );
        }

        const instructionsAcknowledged = mission.instructions?.isAcknowledged;
        if (!instructionsAcknowledged) {
            return (
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-amber-100 text-amber-700">
                    <AlertCircle className="w-3 h-3" />
                    Consignes à valider
                </span>
            );
        }

        return (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-700">
                <CheckCircle2 className="w-3 h-3" />
                Prêt à démarrer
            </span>
        );
    };

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('fr-FR', {
            weekday: 'short',
            day: 'numeric',
            month: 'short',
        });
    };

    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Loader2 className="w-8 h-8 animate-spin text-indigo-600" />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
            {/* Header */}
            <header className="bg-white/80 backdrop-blur-sm border-b border-slate-200 sticky top-0 z-10">
                <div className="max-w-4xl mx-auto px-4 py-4">
                    <div className="flex items-center gap-3">
                        <div className="p-2 rounded-xl bg-gradient-to-br from-indigo-600 to-teal-500">
                            <ClipboardList className="w-5 h-5 text-white" />
                        </div>
                        <div>
                            <h1 className="text-xl font-bold text-slate-900">Suivi de Missions</h1>
                            <p className="text-sm text-slate-500">Vos missions actives</p>
                        </div>
                    </div>
                </div>
            </header>

            {/* Content */}
            <main className="max-w-4xl mx-auto px-4 py-6">
                {error && (
                    <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">
                        {error}
                    </div>
                )}

                {missions.length === 0 ? (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-center py-16"
                    >
                        <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-slate-100 flex items-center justify-center">
                            <ClipboardList className="w-10 h-10 text-slate-400" />
                        </div>
                        <h2 className="text-xl font-semibold text-slate-900 mb-2">
                            Aucune mission active
                        </h2>
                        <p className="text-slate-500 max-w-md mx-auto">
                            Vos missions assignées et en cours apparaîtront ici.
                            Consultez le flux SOS Renfort pour trouver des missions.
                        </p>
                        <Link
                            href="/dashboard/relief"
                            className="inline-flex items-center gap-2 mt-6 px-6 py-3 bg-gradient-to-r from-rose-500 to-rose-600 text-white font-medium rounded-xl shadow-sm hover:shadow-md transition-all"
                        >
                            Voir les missions SOS
                            <ChevronRight className="w-4 h-4" />
                        </Link>
                    </motion.div>
                ) : (
                    <div className="space-y-4">
                        {missions.map((mission, index) => (
                            <motion.div
                                key={mission.id}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1 }}
                            >
                                <Link
                                    href={`/dashboard/missions/${mission.id}/tracking`}
                                    className="block bg-white rounded-2xl border border-slate-200 p-4 hover:shadow-lg hover:border-slate-300 transition-all group"
                                >
                                    <div className="flex items-start justify-between gap-4">
                                        <div className="flex-1 min-w-0">
                                            {/* Title and Job */}
                                            <div className="flex items-start gap-3 mb-3">
                                                {mission.client?.establishment?.logoUrl ? (
                                                    <img
                                                        src={mission.client.establishment.logoUrl}
                                                        alt=""
                                                        className="w-10 h-10 rounded-xl object-cover flex-shrink-0"
                                                    />
                                                ) : (
                                                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-teal-400 flex-shrink-0" />
                                                )}
                                                <div className="min-w-0">
                                                    <h3 className="font-semibold text-slate-900 truncate group-hover:text-indigo-600 transition-colors">
                                                        {mission.title}
                                                    </h3>
                                                    <p className="text-sm text-slate-500 truncate">
                                                        {mission.client?.establishment?.name || 'Établissement'}
                                                    </p>
                                                </div>
                                            </div>

                                            {/* Meta info */}
                                            <div className="flex flex-wrap gap-x-4 gap-y-2 text-sm text-slate-600">
                                                <span className="inline-flex items-center gap-1.5">
                                                    <Calendar className="w-4 h-4 text-slate-400" />
                                                    {formatDate(mission.startDate)}
                                                </span>
                                                <span className="inline-flex items-center gap-1.5">
                                                    <MapPin className="w-4 h-4 text-slate-400" />
                                                    {mission.city}
                                                </span>
                                                <span className="inline-flex items-center gap-1.5">
                                                    <Clock className="w-4 h-4 text-slate-400" />
                                                    {mission.jobTitle}
                                                </span>
                                            </div>
                                        </div>

                                        {/* Status & Arrow */}
                                        <div className="flex flex-col items-end gap-2">
                                            {getStatusBadge(mission)}
                                            <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-indigo-600 transition-colors" />
                                        </div>
                                    </div>
                                </Link>
                            </motion.div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}
