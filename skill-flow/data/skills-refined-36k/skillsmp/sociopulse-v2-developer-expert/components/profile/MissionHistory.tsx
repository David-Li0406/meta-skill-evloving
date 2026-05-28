'use client';

import { motion } from 'framer-motion';
import {
    CheckCircle2,
    Clock,
    XCircle,
    Building2,
    Briefcase,
    Calendar
} from 'lucide-react';
import { EmptyState } from './EmptyState';

export type MissionHistoryStatus =
    | 'COMPLETED'
    | 'IN_PROGRESS'
    | 'CANCELLED'
    | 'FILLED'    // For client: mission pourvue
    | 'OPEN';

export interface MissionHistoryItem {
    id: string;
    title: string;
    /** Establishment or TALENT name */
    partnerName: string;
    /** City/Location */
    city?: string;
    /** Date of the mission */
    date: Date | string;
    /** Mission status */
    status: MissionHistoryStatus;
    /** For freelance: earnings, for client: cost */
    amount?: number;
}

export interface MissionHistoryProps {
    /** List of past missions */
    missions: MissionHistoryItem[];
    /** User role to determine label variations */
    role: 'TALENT' | 'CLIENT' | 'ADMIN';
    /** User's first name for personalization */
    userName?: string;
    /** Whether viewing own profile */
    isOwnProfile?: boolean;
    /** Empty state message */
    emptyMessage?: string;
    /** Callback for empty state action */
    onEmptyAction?: () => void;
}

const statusConfig: Record<MissionHistoryStatus, {
    label: { TALENT: string; CLIENT: string; ADMIN: string };
    className: string;
    icon: typeof CheckCircle2;
}> = {
    COMPLETED: {
        label: { TALENT: 'Mission réussie', CLIENT: 'Terminée', ADMIN: 'Terminée' },
        className: 'bg-green-100 text-green-700 border-green-200',
        icon: CheckCircle2,
    },
    IN_PROGRESS: {
        label: { TALENT: 'En cours', CLIENT: 'En cours', ADMIN: 'En cours' },
        className: 'bg-blue-100 text-blue-700 border-blue-200',
        icon: Clock,
    },
    CANCELLED: {
        label: { TALENT: 'Annulée', CLIENT: 'Annulée', ADMIN: 'Annulée' },
        className: 'bg-red-100 text-red-700 border-red-200',
        icon: XCircle,
    },
    FILLED: {
        label: { TALENT: 'Pourvue', CLIENT: 'Mission pourvue', ADMIN: 'Pourvue' },
        className: 'bg-slate-100 text-slate-600 border-slate-200',
        icon: CheckCircle2,
    },
    OPEN: {
        label: { TALENT: 'Ouverte', CLIENT: 'Recrutement', ADMIN: 'Ouverte' },
        className: 'bg-amber-100 text-amber-700 border-amber-200',
        icon: Clock,
    },
};

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: {
            staggerChildren: 0.08,
        },
    },
};

const itemVariants = {
    hidden: { opacity: 0, x: -20 },
    visible: {
        opacity: 1,
        x: 0,
        transition: {
            type: 'spring' as const,
            stiffness: 100,
            damping: 15,
        },
    },
};

function formatDate(date: Date | string): { day: string; month: string } {
    const d = new Date(date);
    return {
        day: d.getDate().toString(),
        month: d.toLocaleDateString('fr-FR', { month: 'short' }).replace('.', ''),
    };
}

export function MissionHistory({
    missions,
    role,
    userName,
    isOwnProfile = false,
    emptyMessage,
    onEmptyAction
}: MissionHistoryProps) {
    if (missions.length === 0) {
        return (
            <EmptyState
                type="missions"
                userName={userName}
                isOwnProfile={isOwnProfile}
                customMessage={emptyMessage}
                onAction={onEmptyAction}
                actionLabel={isOwnProfile
                    ? (role === 'TALENT' ? 'Trouver des missions' : 'Publier une mission')
                    : 'Collaborer maintenant'
                }
            />
        );
    }

    return (
        <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="relative py-4"
        >
            {/* Vertical Timeline Line */}
            <div className="absolute left-[52px] sm:left-[62px] top-0 bottom-0 w-px bg-slate-200" />

            <div className="space-y-1">
                {missions.map((mission, index) => {
                    const { day, month } = formatDate(mission.date);
                    const config = statusConfig[mission.status];
                    const StatusIcon = config.icon;
                    const statusLabel = config.label[role];

                    return (
                        <motion.div
                            key={mission.id}
                            variants={itemVariants}
                            className="relative flex items-start gap-4 py-4 px-4 rounded-2xl hover:bg-slate-50/80 transition-all cursor-pointer group"
                        >
                            {/* Date Column */}
                            <div className="flex-shrink-0 w-12 sm:w-14 text-center">
                                <div className="text-lg sm:text-xl font-bold text-slate-900">
                                    {day}
                                </div>
                                <div className="text-xs font-medium text-slate-400 uppercase">
                                    {month}
                                </div>
                            </div>

                            {/* Timeline Dot */}
                            <div className="relative flex-shrink-0 z-10">
                                <div className={`
                                    w-3 h-3 rounded-full border-2 border-white shadow-sm
                                    ${mission.status === 'COMPLETED' ? 'bg-green-500' :
                                        mission.status === 'IN_PROGRESS' ? 'bg-brand-600' :
                                            mission.status === 'CANCELLED' ? 'bg-red-400' :
                                                'bg-slate-300'
                                    }
                                `} />
                            </div>

                            {/* Content */}
                            <div className="flex-1 min-w-0">
                                <div className="flex flex-wrap items-start justify-between gap-2">
                                    {/* Mission Info */}
                                    <div className="min-w-0">
                                        <h4 className="text-sm font-semibold text-slate-900 truncate group-hover:text-brand-600 transition-colors">
                                            {mission.title}
                                        </h4>
                                        <div className="flex items-center gap-2 mt-0.5 text-xs text-slate-500">
                                            <span className="inline-flex items-center gap-1">
                                                <Building2 className="w-3 h-3" />
                                                {mission.partnerName}
                                            </span>
                                            {mission.city && (
                                                <span className="text-slate-300">•</span>
                                            )}
                                            {mission.city && (
                                                <span>{mission.city}</span>
                                            )}
                                        </div>
                                    </div>

                                    {/* Status Pill */}
                                    <div className="flex items-center gap-2">
                                        {mission.amount && role === 'TALENT' && (
                                            <span className="text-sm font-semibold text-slate-700">
                                                +{mission.amount}€
                                            </span>
                                        )}
                                        <span className={`
                                            inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium border
                                            ${config.className}
                                        `}>
                                            <StatusIcon className="w-3 h-3" />
                                            {statusLabel}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    );
                })}
            </div>

            {/* View More Link */}
            {missions.length >= 5 && (
                <div className="mt-6 text-center">
                    <button className="btn-secondary">
                        Voir tout l'historique →
                    </button>
                </div>
            )}
        </motion.div>
    );
}

