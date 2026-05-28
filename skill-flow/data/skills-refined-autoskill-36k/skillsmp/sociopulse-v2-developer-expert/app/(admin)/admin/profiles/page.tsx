'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import {
    Search,
    Filter,
    Check,
    X,
    Eye,
    FileText,
    Download,
    ChevronDown,
    Clock,
    User,
    Shield,
    AlertTriangle
} from 'lucide-react';
import Link from 'next/link';

interface PendingProfile {
    id: string;
    firstName: string;
    lastName: string;
    email: string;
    city: string;
    specialties: string[];
    yearsExperience: string;
    submittedAt: string;
    status: 'PENDING' | 'APPROVED' | 'REJECTED';
    documents: {
        type: string;
        name: string;
        url: string;
    }[];
}

// Mock data
const MOCK_PROFILES: PendingProfile[] = [
    {
        id: '1',
        firstName: 'Marie',
        lastName: 'Dupont',
        email: 'marie.dupont@email.com',
        city: 'Lyon',
        specialties: ['Aide-soignant(e)', 'Auxiliaire de vie'],
        yearsExperience: '5-10',
        submittedAt: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        status: 'PENDING',
        documents: [
            { type: 'ID', name: 'CNI_Marie_Dupont.pdf', url: '#' },
            { type: 'Diploma', name: 'DEAS_2019.pdf', url: '#' },
            { type: 'Insurance', name: 'RC_Pro_2024.pdf', url: '#' },
        ],
    },
    {
        id: '2',
        firstName: 'Thomas',
        lastName: 'Martin',
        email: 'thomas.martin@email.com',
        city: 'Paris',
        specialties: ['Éducateur spécialisé'],
        yearsExperience: '3-5',
        submittedAt: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
        status: 'PENDING',
        documents: [
            { type: 'ID', name: 'Passeport_Thomas.pdf', url: '#' },
            { type: 'Diploma', name: 'DEES_2021.pdf', url: '#' },
            { type: 'Insurance', name: 'Assurance_Pro.pdf', url: '#' },
        ],
    },
    {
        id: '3',
        firstName: 'Sophie',
        lastName: 'Lefèvre',
        email: 'sophie.lefevre@email.com',
        city: 'Marseille',
        specialties: ['Infirmier(ère)', 'Ergothérapeute'],
        yearsExperience: '10+',
        submittedAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
        status: 'APPROVED',
        documents: [
            { type: 'ID', name: 'CNI_Sophie.pdf', url: '#' },
            { type: 'Diploma', name: 'DEI_2015.pdf', url: '#' },
            { type: 'Insurance', name: 'RC_Pro.pdf', url: '#' },
        ],
    },
];

function formatTimeAgo(dateString: string): string {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);

    if (diffMins < 60) return `Il y a ${diffMins} min`;
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `Il y a ${diffHours}h`;
    const diffDays = Math.floor(diffHours / 24);
    return `Il y a ${diffDays}j`;
}

export default function AdminProfilesPage() {
    const [profiles, setProfiles] = useState<PendingProfile[]>(MOCK_PROFILES);
    const [filter, setFilter] = useState<'ALL' | 'PENDING' | 'APPROVED' | 'REJECTED'>('PENDING');
    const [searchQuery, setSearchQuery] = useState('');
    const [expandedProfile, setExpandedProfile] = useState<string | null>(null);
    const [actionLoading, setActionLoading] = useState<string | null>(null);

    const filteredProfiles = profiles.filter(p => {
        if (filter !== 'ALL' && p.status !== filter) return false;
        if (searchQuery) {
            const query = searchQuery.toLowerCase();
            return (
                p.firstName.toLowerCase().includes(query) ||
                p.lastName.toLowerCase().includes(query) ||
                p.email.toLowerCase().includes(query) ||
                p.city.toLowerCase().includes(query)
            );
        }
        return true;
    });

    const handleAction = async (profileId: string, action: 'APPROVED' | 'REJECTED') => {
        setActionLoading(profileId);

        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));

        setProfiles(prev =>
            prev.map(p =>
                p.id === profileId ? { ...p, status: action } : p
            )
        );

        setActionLoading(null);
        setExpandedProfile(null);
    };

    const pendingCount = profiles.filter(p => p.status === 'PENDING').length;

    return (
        <div className="min-h-screen bg-slate-50">
            {/* Header */}
            <header className="bg-white border-b border-slate-100 sticky top-0 z-40">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        <div className="flex items-center gap-4">
                            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-indigo-500 flex items-center justify-center">
                                <Shield className="w-5 h-5 text-white" />
                            </div>
                            <div>
                                <h1 className="font-bold text-slate-900">Admin Desk</h1>
                                <p className="text-xs text-slate-500">Validation des profils</p>
                            </div>
                        </div>

                        {pendingCount > 0 && (
                            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-100 text-amber-700">
                                <AlertTriangle className="w-4 h-4" />
                                <span className="text-sm font-medium">{pendingCount} en attente</span>
                            </div>
                        )}
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Filters */}
                <div className="flex flex-col sm:flex-row gap-4 mb-6">
                    <div className="flex-1 relative">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                        <input
                            type="text"
                            placeholder="Rechercher par nom, email, ville..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="input-premium pl-12"
                        />
                    </div>

                    <div className="flex gap-2">
                        {(['ALL', 'PENDING', 'APPROVED', 'REJECTED'] as const).map((status) => (
                            <button
                                key={status}
                                onClick={() => setFilter(status)}
                                className={`
                  px-4 py-2 rounded-lg text-sm font-medium transition-all
                  ${filter === status
                                        ? 'bg-slate-900 text-white'
                                        : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
                                    }
                `}
                            >
                                {status === 'ALL' && 'Tous'}
                                {status === 'PENDING' && 'En attente'}
                                {status === 'APPROVED' && 'Validés'}
                                {status === 'REJECTED' && 'Refusés'}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Table */}
                <div className="bg-white rounded-2xl shadow-soft overflow-hidden">
                    <table className="w-full">
                        <thead>
                            <tr className="bg-slate-50 border-b border-slate-100">
                                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">
                                    Candidat
                                </th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase hidden md:table-cell">
                                    Spécialités
                                </th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase hidden lg:table-cell">
                                    Documents
                                </th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">
                                    Status
                                </th>
                                <th className="px-6 py-4 text-right text-xs font-semibold text-slate-500 uppercase">
                                    Actions
                                </th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {filteredProfiles.length === 0 ? (
                                <tr>
                                    <td colSpan={5} className="px-6 py-12 text-center">
                                        <User className="w-12 h-12 mx-auto text-slate-300 mb-3" />
                                        <p className="text-slate-500">Aucun profil trouvé</p>
                                    </td>
                                </tr>
                            ) : (
                                filteredProfiles.map((profile) => (
                                    <motion.tr
                                        key={profile.id}
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        className="group hover:bg-slate-50 transition-colors"
                                    >
                                        {/* Candidate */}
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-3">
                                                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-brand-100 to-brand-50 flex items-center justify-center">
                                                    <span className="text-sm font-semibold text-brand-600">
                                                        {(profile.firstName || '?').charAt(0)}{(profile.lastName || '?').charAt(0)}
                                                    </span>
                                                </div>
                                                <div>
                                                    <p className="font-medium text-slate-900">
                                                        {profile.firstName} {profile.lastName}
                                                    </p>
                                                    <p className="text-xs text-slate-500">{profile.email}</p>
                                                    <p className="text-xs text-slate-400">{profile.city} • {profile.yearsExperience} ans exp.</p>
                                                </div>
                                            </div>
                                        </td>

                                        {/* Specialties */}
                                        <td className="px-6 py-4 hidden md:table-cell">
                                            <div className="flex flex-wrap gap-1">
                                                {profile.specialties.slice(0, 2).map((s, i) => (
                                                    <span
                                                        key={i}
                                                        className="px-2 py-0.5 rounded-md bg-slate-100 text-slate-600 text-xs"
                                                    >
                                                        {s}
                                                    </span>
                                                ))}
                                                {profile.specialties.length > 2 && (
                                                    <span className="text-xs text-slate-400">
                                                        +{profile.specialties.length - 2}
                                                    </span>
                                                )}
                                            </div>
                                        </td>

                                        {/* Documents */}
                                        <td className="px-6 py-4 hidden lg:table-cell">
                                            <div className="flex items-center gap-2">
                                                {profile.documents.map((doc, i) => (
                                                    <a
                                                        key={i}
                                                        href={doc.url}
                                                        target="_blank"
                                                        rel="noopener noreferrer"
                                                        className="p-2 rounded-lg bg-slate-100 hover:bg-slate-200 transition-colors"
                                                        title={doc.name}
                                                    >
                                                        <FileText className="w-4 h-4 text-slate-600" />
                                                    </a>
                                                ))}
                                            </div>
                                        </td>

                                        {/* Status */}
                                        <td className="px-6 py-4">
                                            <span className={`
                        inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium
                        ${profile.status === 'PENDING' && 'bg-amber-100 text-amber-700'}
                        ${profile.status === 'APPROVED' && 'bg-green-100 text-green-700'}
                        ${profile.status === 'REJECTED' && 'bg-red-100 text-red-700'}
                      `}>
                                                {profile.status === 'PENDING' && <Clock className="w-3 h-3" />}
                                                {profile.status === 'APPROVED' && <Check className="w-3 h-3" />}
                                                {profile.status === 'REJECTED' && <X className="w-3 h-3" />}
                                                {profile.status === 'PENDING' && 'En attente'}
                                                {profile.status === 'APPROVED' && 'Validé'}
                                                {profile.status === 'REJECTED' && 'Refusé'}
                                            </span>
                                            <p className="text-xs text-slate-400 mt-1">
                                                {formatTimeAgo(profile.submittedAt)}
                                            </p>
                                        </td>

                                        {/* Actions */}
                                        <td className="px-6 py-4">
                                            <div className="flex items-center justify-end gap-2">
                                                {profile.status === 'PENDING' ? (
                                                    <>
                                                        <button
                                                            onClick={() => handleAction(profile.id, 'APPROVED')}
                                                            disabled={actionLoading === profile.id}
                                                            className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-green-500 text-white text-sm font-medium hover:bg-green-600 transition-colors disabled:opacity-50"
                                                        >
                                                            <Check className="w-4 h-4" />
                                                            Valider
                                                        </button>
                                                        <button
                                                            onClick={() => handleAction(profile.id, 'REJECTED')}
                                                            disabled={actionLoading === profile.id}
                                                            className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-red-500 text-white text-sm font-medium hover:bg-red-600 transition-colors disabled:opacity-50"
                                                        >
                                                            <X className="w-4 h-4" />
                                                            Refuser
                                                        </button>
                                                    </>
                                                ) : (
                                                    <button
                                                        onClick={() => setExpandedProfile(profile.id === expandedProfile ? null : profile.id)}
                                                        className="p-2 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition-colors"
                                                    >
                                                        <Eye className="w-4 h-4" />
                                                    </button>
                                                )}
                                            </div>
                                        </td>
                                    </motion.tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-3 gap-4 mt-8">
                    <div className="bg-white rounded-xl p-4 shadow-soft text-center">
                        <p className="text-3xl font-bold text-amber-600">{profiles.filter(p => p.status === 'PENDING').length}</p>
                        <p className="text-sm text-slate-500">En attente</p>
                    </div>
                    <div className="bg-white rounded-xl p-4 shadow-soft text-center">
                        <p className="text-3xl font-bold text-green-600">{profiles.filter(p => p.status === 'APPROVED').length}</p>
                        <p className="text-sm text-slate-500">Validés</p>
                    </div>
                    <div className="bg-white rounded-xl p-4 shadow-soft text-center">
                        <p className="text-3xl font-bold text-red-600">{profiles.filter(p => p.status === 'REJECTED').length}</p>
                        <p className="text-sm text-slate-500">Refusés</p>
                    </div>
                </div>
            </main>
        </div>
    );
}
