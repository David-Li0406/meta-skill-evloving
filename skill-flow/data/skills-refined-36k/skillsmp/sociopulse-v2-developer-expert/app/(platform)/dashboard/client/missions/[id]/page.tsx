'use client';

import Link from 'next/link';
import { ChevronLeft } from 'lucide-react';
import { ActiveMissionCard } from '@/components/dashboard/client/ActiveMissionCard';
import { MissionKanban } from '@/components/dashboard/client/MissionKanban';

// Mock Data
const activeMission = {
    id: 'mis-001',
    title: 'Renfort weekend EHPAD - Nuit',
    date: '25 Jan 2026 - 26 Jan 2026',
    location: 'Lyon 3ème',
    status: 'PUBLISHED' as const,
    urgency: 'CRITICAL' as const,
    views: 142,
    applicants: 3,
    matchingProfiles: 5,
    createdAt: new Date('2026-01-18'),
};

export default function MissionDetailPage({ params }: { params: { id: string } }) {
    return (
        <div className="p-6 space-y-6">
            {/* Back Navigation */}
            <Link
                href="/dashboard/client/missions"
                className="inline-flex items-center gap-2 text-sm font-medium text-slate-500 hover:text-slate-900"
            >
                <ChevronLeft className="h-4 w-4" />
                Retour aux missions
            </Link>

            {/* Hero Card */}
            <ActiveMissionCard mission={activeMission} />

            {/* Filters & Actions would go here */}

            {/* Kanban Board */}
            <div className="min-h-[500px]">
                <h2 className="mb-4 text-lg font-semibold text-slate-900">Suivi des candidatures</h2>
                <MissionKanban />
            </div>
        </div>
    );
}
