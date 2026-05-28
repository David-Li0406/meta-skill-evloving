'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import {
    Plus,
    Filter,
    ChevronRight,
    MapPin,
    Clock,
    Siren
} from 'lucide-react';
import { Badge, StatusDot } from '@/components/ui';

type TabKey = 'drafts' | 'open' | 'in_progress' | 'completed';

const tabs: { key: TabKey; label: string; count: number }[] = [
    { key: 'drafts', label: 'Brouillons', count: 1 },
    { key: 'open', label: 'Ouvertes', count: 3 },
    { key: 'in_progress', label: 'En cours', count: 2 },
    { key: 'completed', label: 'Terminées', count: 8 },
];

// Mock data
const missions = {
    drafts: [
        {
            id: '1',
            title: 'Aide-soignant(e) de nuit',
            jobTitle: 'Aide-soignant(e)',
            urgency: 'CRITICAL' as const,
            date: 'Non planifiée',
            city: 'Lyon',
            candidates: [],
            status: 'draft',
        },
    ],
    open: [
        {
            id: '2',
            title: 'Renfort weekend EHPAD',
            jobTitle: 'Aide-soignant(e)',
            urgency: 'HIGH' as const,
            date: 'Sam 25 Jan, 07h - 19h',
            city: 'Lyon 3ème',
            candidates: [
                { id: 'c1', name: 'Marie L.', avatar: null },
                { id: 'c2', name: 'Thomas D.', avatar: null },
                { id: 'c3', name: 'Sophie M.', avatar: null },
                { id: 'c4', name: 'Pierre B.', avatar: null },
            ],
            status: 'open',
        },
        {
            id: '3',
            title: 'Éducateur spécialisé vacances',
            jobTitle: 'Éducateur spécialisé',
            urgency: 'MEDIUM' as const,
            date: '27-31 Jan',
            city: 'Villeurbanne',
            candidates: [
                { id: 'c5', name: 'Claire D.', avatar: null },
            ],
            status: 'open',
        },
        {
            id: '4',
            title: 'AMP accompagnement sortie',
            jobTitle: 'AMP',
            urgency: 'LOW' as const,
            date: 'Mer 29 Jan, 14h - 18h',
            city: 'Lyon 6ème',
            candidates: [],
            status: 'open',
        },
    ],
    in_progress: [
        {
            id: '5',
            title: 'Mission nuit EHPAD',
            jobTitle: 'Aide-soignant(e)',
            urgency: 'HIGH' as const,
            date: "Aujourd'hui, 20h - 06h",
            city: 'Lyon 3ème',
            assignedTalent: { name: 'Marie Lambert', avatar: null },
            status: 'in_progress',
        },
        {
            id: '6',
            title: 'Renfort équipe jour',
            jobTitle: 'AMP',
            urgency: 'MEDIUM' as const,
            date: 'Demain, 08h - 16h',
            city: 'Villeurbanne',
            assignedTalent: { name: 'Thomas Durand', avatar: null },
            status: 'in_progress',
        },
    ],
    completed: [],
};

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: { staggerChildren: 0.05 }
    }
};

const itemVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: { opacity: 1, y: 0 }
};

export default function ClientMissionsPage() {
    const [activeTab, setActiveTab] = useState<TabKey>('open');

    const currentMissions = missions[activeTab] || [];

    return (
        <div className="p-6 space-y-6">
            {/* Header */}
            <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
            >
                <div>
                    <h1 className="text-2xl font-bold text-slate-900">
                        Gestion des Missions
                    </h1>
                    <p className="text-slate-500">
                        Gérez vos demandes SOS Renfort et suivez les candidatures
                    </p>
                </div>
                <Link
                    href="/sos"
                    className="inline-flex items-center gap-2 rounded-full bg-rose-600 px-5 py-2.5 text-sm font-medium text-white shadow-sm transition-colors hover:bg-rose-700"
                >
                    <Plus className="h-4 w-4" />
                    Nouvelle Mission SOS
                </Link>
            </motion.div>

            {/* Tabs */}
            <div className="flex items-center gap-2 border-b border-slate-200">
                {tabs.map((tab) => (
                    <button
                        key={tab.key}
                        onClick={() => setActiveTab(tab.key)}
                        className={`relative flex items-center gap-2 px-4 py-3 text-sm font-medium transition-colors ${activeTab === tab.key
                            ? 'text-teal-600'
                            : 'text-slate-500 hover:text-slate-700'
                            }`}
                    >
                        {tab.label}
                        <span
                            className={`rounded-full px-2 py-0.5 text-xs ${activeTab === tab.key
                                ? 'bg-teal-100 text-teal-700'
                                : 'bg-slate-100 text-slate-600'
                                }`}
                        >
                            {tab.count}
                        </span>
                        {activeTab === tab.key && (
                            <motion.div
                                layoutId="activeTab"
                                className="absolute bottom-0 left-0 right-0 h-0.5 bg-teal-600"
                            />
                        )}
                    </button>
                ))}
            </div>

            {/* Filters */}
            <div className="flex items-center gap-2">
                <button className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-50">
                    <Filter className="h-4 w-4" />
                    Filtres
                </button>
            </div>

            {/* Missions List */}
            <AnimatePresence mode="wait">
                <motion.div
                    key={activeTab}
                    variants={containerVariants}
                    initial="hidden"
                    animate="visible"
                    exit="hidden"
                    className="space-y-3"
                >
                    {currentMissions.length === 0 ? (
                        <motion.div
                            variants={itemVariants}
                            className="rounded-xl border border-dashed border-slate-200 bg-slate-50 p-12 text-center"
                        >
                            <Siren className="mx-auto h-12 w-12 text-slate-300" />
                            <p className="mt-4 font-medium text-slate-600">
                                Aucune mission dans cette catégorie
                            </p>
                            <p className="mt-1 text-sm text-slate-400">
                                Les missions apparaîtront ici une fois créées
                            </p>
                        </motion.div>
                    ) : (
                        currentMissions.map((mission: any) => (
                            <MissionCard key={mission.id} mission={mission} />
                        ))
                    )}
                </motion.div>
            </AnimatePresence>
        </div>
    );
}

interface MissionCardProps {
    mission: {
        id: string;
        title: string;
        jobTitle: string;
        urgency: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
        date: string;
        city: string;
        candidates?: { id: string; name: string; avatar: string | null }[];
        assignedTalent?: { name: string; avatar: string | null };
        status: string;
    };
}

function MissionCard({ mission }: MissionCardProps) {
    const urgencyConfig = {
        CRITICAL: { label: 'Critique', variant: 'destructive' as const },
        HIGH: { label: 'Urgent', variant: 'warning' as const },
        MEDIUM: { label: 'Normal', variant: 'secondary' as const },
        LOW: { label: 'Flexible', variant: 'secondary' as const },
    };

    const config = urgencyConfig[mission.urgency];

    return (
        <motion.div variants={itemVariants}>
            <Link
                href={`/dashboard/missions/${mission.id}`}
                className="group flex items-center gap-4 rounded-xl border border-slate-200 bg-white p-4 shadow-sm transition-all hover:border-slate-300 hover:bg-slate-50 hover:shadow-md"
            >
                {/* Status Badge */}
                <Badge variant={config.variant} size="sm">
                    {config.label}
                </Badge>

                {/* Main Content */}
                <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-slate-900 truncate group-hover:text-teal-600">
                        {mission.title}
                    </h3>
                    <div className="mt-1 flex items-center gap-3 text-sm text-slate-500">
                        <span className="flex items-center gap-1">
                            <Clock className="h-3.5 w-3.5" />
                            {mission.date}
                        </span>
                        <span className="flex items-center gap-1">
                            <MapPin className="h-3.5 w-3.5" />
                            {mission.city}
                        </span>
                    </div>
                </div>

                {/* Candidates / Assigned */}
                <div className="hidden sm:block">
                    {mission.assignedTalent ? (
                        <div className="flex items-center gap-2">
                            <StatusDot status="live" />
                            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-teal-100 text-sm font-medium text-teal-600">
                                {mission.assignedTalent.name.charAt(0)}
                            </div>
                            <span className="text-sm text-slate-600">
                                {mission.assignedTalent.name}
                            </span>
                        </div>
                    ) : mission.candidates && mission.candidates.length > 0 ? (
                        <div className="flex items-center gap-2">
                            <AvatarStack candidates={mission.candidates} />
                            <span className="text-sm text-slate-500">
                                {mission.candidates.length} candidature{mission.candidates.length > 1 ? 's' : ''}
                            </span>
                        </div>
                    ) : (
                        <span className="text-sm text-slate-400">
                            En attente de candidatures
                        </span>
                    )}
                </div>

                {/* Arrow */}
                <ChevronRight className="h-5 w-5 text-slate-400 transition-transform group-hover:translate-x-0.5" />
            </Link>
        </motion.div>
    );
}

interface AvatarStackProps {
    candidates: { id: string; name: string; avatar: string | null }[];
    max?: number;
}

function AvatarStack({ candidates, max = 3 }: AvatarStackProps) {
    const visible = candidates.slice(0, max);
    const remaining = candidates.length - max;

    return (
        <div className="flex -space-x-2">
            {visible.map((candidate, index) => (
                <div
                    key={candidate.id}
                    className="flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-slate-200 text-xs font-medium text-slate-600"
                    style={{ zIndex: max - index }}
                >
                    {candidate.name.charAt(0)}
                </div>
            ))}
            {remaining > 0 && (
                <div className="flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-slate-100 text-xs font-medium text-slate-500">
                    +{remaining}
                </div>
            )}
        </div>
    );
}
