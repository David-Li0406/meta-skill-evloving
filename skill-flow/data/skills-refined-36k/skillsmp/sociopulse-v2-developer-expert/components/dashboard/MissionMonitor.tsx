'use client';

import { useEffect, useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import {
    Search,
    CheckCircle2,
    Clock,
    User,
    MoreHorizontal,
    Phone,
    MessageSquare,
    XCircle,
    Users
} from 'lucide-react';
import { ToastContainer, useToasts } from '@/components/ui/Toast';
import { getActiveMissions } from '@/app/(platform)/services/matching.service';

type MissionStatus = 'SEARCHING' | 'ASSIGNED' | 'CANCELLED';

interface Mission {
    id: string;
    jobTitle: string;
    startTime?: string;
    status: MissionStatus;
    candidateName: string | null;
    urgencyLevel: 'HIGH' | 'CRITICAL';
    createdAt: string;
    candidatesCount?: number;
}

interface MissionMonitorProps {
    initialMissions?: Mission[];
    onRefresh?: () => void;
}

const statusConfig = {
    SEARCHING: {
        label: 'En recherche',
        color: 'text-amber-500',
        bgColor: 'bg-amber-500/10',
        icon: Search,
        pulse: true,
    },
    ASSIGNED: {
        label: 'Pourvu',
        color: 'text-green-500',
        bgColor: 'bg-green-500/10',
        icon: CheckCircle2,
        pulse: false,
    },
    CANCELLED: {
        label: 'Annulee',
        color: 'text-slate-400',
        bgColor: 'bg-slate-500/10',
        icon: XCircle,
        pulse: false,
    },
};

function formatTimeAgo(dateString: string): string {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);

    if (diffMins < 1) return 'A l instant';
    if (diffMins < 60) return `Il y a ${diffMins} min`;
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `Il y a ${diffHours}h`;
    return `Il y a ${Math.floor(diffHours / 24)}j`;
}

export function MissionMonitor({ initialMissions = [], onRefresh }: MissionMonitorProps) {
    const [missions, setMissions] = useState<Mission[]>(initialMissions);
    const [selectedMission, setSelectedMission] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const { toasts, addToast, removeToast } = useToasts();

    const mapMission = useMemo(
        () => (mission: any): Mission => {
            const startDate = mission?.startDate || mission?.startTime || mission?.createdAt;
            return {
                id: mission?.id || mission?.missionId || '',
                jobTitle: mission?.jobTitle || mission?.title || 'Mission',
                startTime: startDate
                    ? new Date(startDate).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
                    : '',
                status: (mission?.status || 'SEARCHING') as MissionStatus,
                candidateName: mission?.candidateName || null,
                urgencyLevel: mission?.urgencyLevel || 'HIGH',
                createdAt: mission?.createdAt || startDate || new Date().toISOString(),
                candidatesCount:
                    mission?.candidatesCount ??
                    (Array.isArray(mission?.candidates) ? mission.candidates.length : undefined),
            };
        },
        []
    );

    useEffect(() => {
        setMissions(initialMissions.map(mapMission));
    }, [initialMissions, mapMission]);

    useEffect(() => {
        const fetchMissions = async () => {
            setIsLoading(true);
            try {
                const response = await getActiveMissions();
                const list =
                    (Array.isArray(response) && response) ||
                    (Array.isArray(response?.items) && response.items) ||
                    (Array.isArray(response?.data) && response.data) ||
                    (Array.isArray(response?.missions) && response.missions) ||
                    [];
                setMissions(list.map(mapMission));
            } catch (error) {
                console.error('getActiveMissions error', error);
                addToast({ message: 'Erreur lors du chargement des missions', type: 'error' });
            } finally {
                setIsLoading(false);
            }
        };

        fetchMissions();
    }, [addToast, mapMission]);

    const searchingCount = missions.filter(m => m.status === 'SEARCHING').length;
    const assignedCount = missions.filter(m => m.status === 'ASSIGNED').length;

    return (
        <div className="bg-white rounded-2xl shadow-soft overflow-hidden">
            <ToastContainer toasts={toasts} onRemove={removeToast} />
            {/* Header */}
            <div className="px-6 py-4 border-b border-slate-100">
                <div className="flex items-center justify-between">
                    <div>
                        <h2 className="text-lg font-semibold text-slate-900">Suivi des missions</h2>
                        <p className="text-sm text-slate-500">Temps reel</p>
                    </div>
                    <div className="flex items-center gap-3">
                        {/* Stats */}
                        <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-50">
                            <div className="w-2 h-2 rounded-full bg-amber-500 animate-pulse" />
                            <span className="text-xs font-medium text-amber-700">{searchingCount} en cours</span>
                        </div>
                        <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-green-50">
                            <div className="w-2 h-2 rounded-full bg-green-500" />
                            <span className="text-xs font-medium text-green-700">{assignedCount} pourvu(s)</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Table */}
            <div className="overflow-x-auto">
                <table className="w-full">
                    <thead>
                        <tr className="bg-slate-50">
                            <th className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                                Poste
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                                Heure
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                                Status
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                                Candidat
                            </th>
                            <th className="px-6 py-3 text-right text-xs font-semibold text-slate-500 uppercase tracking-wider">
                                Actions
                            </th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                        {missions.length === 0 ? (
                            <tr>
                                <td colSpan={5} className="px-6 py-12 text-center">
                                    <div className="flex flex-col items-center">
                                        <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mb-3">
                                            <Clock className="w-6 h-6 text-slate-400" />
                                        </div>
                                        <p className="text-sm text-slate-500">Aucune mission en cours</p>
                                        <p className="text-xs text-slate-400 mt-1">Utilisez le formulaire ci-dessus pour lancer une alerte</p>
                                    </div>
                                </td>
                            </tr>
                        ) : (
                            missions.map((mission, index) => {
                                const status = statusConfig[mission.status];
                                const StatusIcon = status.icon;

                                return (
                                    <motion.tr
                                        key={mission.id}
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: index * 0.05 }}
                                        className={`
                      group hover:bg-slate-50 transition-colors cursor-pointer
                      ${selectedMission === mission.id ? 'bg-slate-50' : ''}
                    `}
                                        onClick={() => setSelectedMission(mission.id === selectedMission ? null : mission.id)}
                                    >
                                        {/* Job Title */}
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-3">
                                                <div className={`
                          w-10 h-10 rounded-xl flex items-center justify-center
                          ${mission.urgencyLevel === 'CRITICAL'
                                                        ? 'bg-red-100 text-red-600'
                                                        : 'bg-orange-100 text-orange-600'
                                                    }
                        `}>
                                                    <span className="text-sm font-bold">
                                                        {(mission.jobTitle || '?').charAt(0)}
                                                    </span>
                                                </div>
                                                <div>
                                                    <p className="font-medium text-slate-900">{mission.jobTitle}</p>
                                                    <p className="text-xs text-slate-400">{formatTimeAgo(mission.createdAt)}</p>
                                                </div>
                                            </div>
                                        </td>

                                        {/* Time */}
                                        <td className="px-6 py-4">
                                            <span className="text-sm font-medium text-slate-900">{mission.startTime}</span>
                                        </td>

                                        {/* Status */}
                                        <td className="px-6 py-4">
                                            <div className={`
                        inline-flex items-center gap-2 px-3 py-1.5 rounded-full
                        ${status.bgColor}
                      `}>
                                                {status.pulse ? (
                                                    <motion.div
                                                        animate={{ scale: [1, 1.2, 1] }}
                                                        transition={{ repeat: Infinity, duration: 1.5 }}
                                                    >
                                                        <StatusIcon className={`w-4 h-4 ${status.color}`} />
                                                    </motion.div>
                                                ) : (
                                                    <StatusIcon className={`w-4 h-4 ${status.color}`} />
                                                )}
                                                <span className={`text-xs font-medium ${status.color}`}>
                                                    {status.label}
                                                </span>
                                                {status.pulse && (
                                                    <span className="relative flex h-2 w-2">
                                                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75" />
                                                        <span className="relative inline-flex rounded-full h-2 w-2 bg-amber-500" />
                                                    </span>
                                                )}
                                            </div>
                                        </td>

                                        {/* Candidate */}
                                        <td className="px-6 py-4">
                                            {mission.candidateName ? (
                                                <div className="flex items-center gap-2">
                                                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-brand-100 to-indigo-100 flex items-center justify-center">
                                                        <span className="text-xs font-semibold text-brand-600">
                                                            {(mission.candidateName || '?').charAt(0)}
                                                        </span>
                                                    </div>
                                                    <span className="text-sm font-medium text-slate-900">
                                                        {mission.candidateName}
                                                    </span>
                                                </div>
                                            ) : (
                                                <span className="text-sm text-slate-400">-</span>
                                            )}
                                        </td>

                                        {/* Actions */}
                                        <td className="px-6 py-4 text-right">
                                            <div className="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                                <div className="flex items-center gap-1 px-2 py-1 rounded-lg bg-slate-100 text-xs text-slate-600">
                                                    <Users className="w-3 h-3" />
                                                    <span>{mission.candidatesCount ?? 0}</span>
                                                </div>
                                                <Link
                                                    href={`/dashboard/missions/${mission.id}`}
                                                    className="p-2 rounded-lg hover:bg-blue-100 text-slate-400 hover:text-blue-600 transition-colors text-xs font-medium"
                                                >
                                                    Voir les candidats
                                                </Link>
                                                {mission.candidateName && (
                                                    <>
                                                        <button
                                                            className="p-2 rounded-lg hover:bg-green-100 text-slate-400 hover:text-green-600 transition-colors"
                                                            title="Appeler"
                                                        >
                                                            <Phone className="w-4 h-4" />
                                                        </button>
                                                        <button
                                                            className="p-2 rounded-lg hover:bg-blue-100 text-slate-400 hover:text-blue-600 transition-colors"
                                                            title="Message"
                                                        >
                                                            <MessageSquare className="w-4 h-4" />
                                                        </button>
                                                    </>
                                                )}
                                                <button
                                                    className="p-2 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition-colors"
                                                    title="Plus d'options"
                                                >
                                                    <MoreHorizontal className="w-4 h-4" />
                                                </button>
                                            </div>
                                        </td>
                                    </motion.tr>
                                );
                            })
                        )}
                    </tbody>
                </table>
            </div>

            {/* Footer */}
            {missions.length > 0 && (
                <div className="px-6 py-3 bg-slate-50 border-t border-slate-100">
                    <p className="text-xs text-slate-500 text-center">
                        Mise a jour automatique - Derniere actualisation: maintenant
                    </p>
                </div>
            )}
        </div>
    );
}
