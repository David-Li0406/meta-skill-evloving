'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    MoreHorizontal,
    MessageCircle,
    FileCheck,
    Clock,
    CheckCircle,
    AlertCircle
} from 'lucide-react';
import { Badge } from '@/components/ui';

// Mock Candidate Data
const mockCandidates = [
    {
        id: 'c1',
        name: 'Marie Lambert',
        role: 'Aide-soignante',
        match: 95,
        status: 'SELECTED',
        avatar: null,
    },
    {
        id: 'c2',
        name: 'Thomas Durand',
        role: 'Éducateur',
        match: 88,
        status: 'STUDYING',
        avatar: null,
    },
    {
        id: 'c3',
        name: 'Sophie Martin',
        role: 'AMP',
        match: 75,
        status: 'STUDYING',
        avatar: null,
    },
];

type KanbanColumnId = 'STUDYING' | 'SELECTED' | 'VALIDATED';

interface KanbanColumn {
    id: KanbanColumnId;
    title: string;
    color: string;
    icon: React.ElementType;
}

const columns: KanbanColumn[] = [
    { id: 'STUDYING', title: "À l'étude", color: 'bg-slate-100', icon: Clock },
    { id: 'SELECTED', title: 'Sélectionnés', color: 'bg-blue-50', icon: CheckCircle },
    { id: 'VALIDATED', title: 'Validés', color: 'bg-emerald-50', icon: FileCheck },
];

export function MissionKanban() {
    const [candidates, setCandidates] = useState(mockCandidates);

    const handleMove = (candidateId: string, newStatus: KanbanColumnId) => { // Simple click-to-move for accessibility
        if (newStatus === 'VALIDATED') {
            // Trigger Business Lock: Contract Generation
            const confirmed = window.confirm("Valider ce candidat déclenchera la génération du contrat. Continuer ?");
            if (!confirmed) return;
        }

        setCandidates(prev => prev.map(c =>
            c.id === candidateId ? { ...c, status: newStatus } : c
        ));
    };

    return (
        <div className="grid grid-cols-1 gap-6 md:grid-cols-3 h-full">
            {columns.map(column => (
                <div key={column.id} className={`flex flex-col rounded-xl border border-slate-200 ${column.color} p-4`}>
                    {/* Column Header */}
                    <div className="mb-4 flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <column.icon className="h-4 w-4 text-slate-500" />
                            <h3 className="font-semibold text-slate-700">{column.title}</h3>
                        </div>
                        <Badge variant="secondary" size="sm">
                            {candidates.filter(c => c.status === column.id).length}
                        </Badge>
                    </div>

                    {/* Candidates List */}
                    <div className="flex-1 space-y-3">
                        <AnimatePresence>
                            {candidates.filter(c => c.status === column.id).map(candidate => (
                                <motion.div
                                    key={candidate.id}
                                    layoutId={candidate.id}
                                    initial={{ opacity: 0, scale: 0.9 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    exit={{ opacity: 0, scale: 0.9 }}
                                    className="group relative rounded-lg border border-slate-200 bg-white p-4 shadow-sm hover:shadow-md transition-shadow"
                                >
                                    <div className="flex items-start justify-between">
                                        <div className="flex items-center gap-3">
                                            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-100 text-sm font-semibold text-slate-600">
                                                {candidate.name.charAt(0)}
                                            </div>
                                            <div>
                                                <p className="font-medium text-slate-900">{candidate.name}</p>
                                                <p className="text-xs text-slate-500">{candidate.role}</p>
                                            </div>
                                        </div>
                                        {candidate.match > 90 && (
                                            <span className="flex items-center gap-1 rounded-full bg-emerald-50 px-2 py-0.5 text-xs font-medium text-emerald-600">
                                                {candidate.match}% Match
                                            </span>
                                        )}
                                    </div>

                                    {/* Quick Actions (Hover) */}
                                    <div className="mt-4 flex items-center justify-between border-t border-slate-100 pt-3">
                                        <button className="text-slate-400 hover:text-slate-600">
                                            <MessageCircle className="h-4 w-4" />
                                        </button>

                                        {/* Move Controls */}
                                        <div className="flex gap-1">
                                            {column.id === 'STUDYING' && (
                                                <button
                                                    onClick={() => handleMove(candidate.id, 'SELECTED')}
                                                    className="text-xs font-medium text-blue-600 hover:underline"
                                                >
                                                    Sélectionner
                                                </button>
                                            )}
                                            {column.id === 'SELECTED' && (
                                                <button
                                                    onClick={() => handleMove(candidate.id, 'VALIDATED')}
                                                    className="text-xs font-medium text-emerald-600 hover:underline"
                                                >
                                                    Valider
                                                </button>
                                            )}
                                        </div>
                                    </div>
                                </motion.div>
                            ))}
                        </AnimatePresence>

                        {candidates.filter(c => c.status === column.id).length === 0 && (
                            <div className="flex h-32 items-center justify-center rounded-lg border border-dashed border-slate-300 text-sm text-slate-400">
                                Aucun candidat
                            </div>
                        )}
                    </div>
                </div>
            ))}
        </div>
    );
}
