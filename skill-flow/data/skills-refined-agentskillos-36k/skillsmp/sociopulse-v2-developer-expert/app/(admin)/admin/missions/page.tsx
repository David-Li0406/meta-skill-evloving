'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import Cookies from 'js-cookie';
import {
    Shield,
    ChevronLeft,
    Search,
    Filter,
    Briefcase,
    MapPin,
    Calendar,
    Clock,
    Euro,
    User,
    AlertTriangle,
    CheckCircle,
    XCircle,
    Play,
    Loader2,
    Eye,
    ChevronRight,
    Zap,
    RefreshCw,
    FileText,
} from 'lucide-react';

// ===========================================
// TYPES
// ===========================================

interface Mission {
    id: string;
    title: string;
    jobTitle: string;
    description: string;
    status: 'OPEN' | 'ASSIGNED' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED';
    urgencyLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
    startDate: string;
    endDate: string;
    hourlyRate: number;
    estimatedHours?: number;
    totalBudget?: number;
    city: string;
    address: string;
    isNightShift: boolean;
    client: {
        id: string;
        email: string;
        establishment?: {
            name: string;
            logoUrl?: string;
        };
    };
    assignedTalent?: {
        id: string;
        email: string;
        profile?: {
            firstName: string;
            lastName: string;
            avatarUrl?: string;
        };
    };
    contract?: {
        id: string;
        status: 'PENDING' | 'SIGNED';
    };
    _count?: {
        applications: number;
    };
    createdAt: string;
}

type StatusFilter = 'ALL' | 'OPEN' | 'ASSIGNED' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED';
type UrgencyFilter = 'ALL' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

// ===========================================
// HELPERS
// ===========================================

const getApiBase = () => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';
    const normalized = apiBase.replace(/\/+$/, '');
    return normalized.endsWith('/api/v1') ? normalized : `${normalized}/api/v1`;
};

const getToken = () => Cookies.get('accessToken');

const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
    });
};

const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR',
    }).format(amount);
};

// ===========================================
// STATUS BADGE
// ===========================================

function StatusBadge({ status }: { status: Mission['status'] }) {
    const config: Record<string, { bg: string; text: string; icon: React.ReactNode; label: string }> = {
        OPEN: { bg: 'bg-blue-100', text: 'text-blue-700', icon: <Briefcase className="w-3.5 h-3.5" />, label: 'Ouverte' },
        ASSIGNED: { bg: 'bg-purple-100', text: 'text-purple-700', icon: <User className="w-3.5 h-3.5" />, label: 'Attribuée' },
        IN_PROGRESS: { bg: 'bg-amber-100', text: 'text-amber-700', icon: <Play className="w-3.5 h-3.5" />, label: 'En cours' },
        COMPLETED: { bg: 'bg-green-100', text: 'text-green-700', icon: <CheckCircle className="w-3.5 h-3.5" />, label: 'Terminée' },
        CANCELLED: { bg: 'bg-red-100', text: 'text-red-700', icon: <XCircle className="w-3.5 h-3.5" />, label: 'Annulée' },
    };

    const c = config[status] || config.OPEN;

    return (
        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${c.bg} ${c.text}`}>
            {c.icon}
            {c.label}
        </span>
    );
}

// ===========================================
// URGENCY BADGE
// ===========================================

function UrgencyBadge({ urgency }: { urgency: Mission['urgencyLevel'] }) {
    const config: Record<string, { bg: string; text: string; label: string }> = {
        LOW: { bg: 'bg-slate-100', text: 'text-slate-600', label: 'Sous 1 semaine' },
        MEDIUM: { bg: 'bg-amber-100', text: 'text-amber-700', label: 'Sous 48h' },
        HIGH: { bg: 'bg-orange-100', text: 'text-orange-700', label: 'Sous 24h' },
        CRITICAL: { bg: 'bg-red-100', text: 'text-red-700', label: 'Immédiat' },
    };

    const c = config[urgency] || config.LOW;

    return (
        <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium ${c.bg} ${c.text}`}>
            <Zap className="w-3 h-3" />
            {c.label}
        </span>
    );
}

// ===========================================
// MISSION CARD
// ===========================================

function MissionCard({ mission }: { mission: Mission }) {
    const clientName = mission.client.establishment?.name || mission.client.email;

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden hover:shadow-md transition-all"
        >
            {/* Header */}
            <div className="p-5 border-b border-slate-50">
                <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-2">
                            <StatusBadge status={mission.status} />
                            <UrgencyBadge urgency={mission.urgencyLevel} />
                        </div>
                        <h3 className="font-semibold text-slate-900 truncate">{mission.title}</h3>
                        <p className="text-sm text-slate-500">{mission.jobTitle}</p>
                    </div>
                    {mission.isNightShift && (
                        <span className="px-2 py-1 bg-indigo-100 text-indigo-700 text-xs rounded-lg font-medium">
                            Nuit
                        </span>
                    )}
                </div>
            </div>

            {/* Content */}
            <div className="p-5 space-y-4">
                {/* Client */}
                <div className="flex items-center gap-3">
                    {mission.client.establishment?.logoUrl ? (
                        <img
                            src={mission.client.establishment.logoUrl}
                            alt={clientName}
                            className="w-10 h-10 rounded-lg object-cover"
                        />
                    ) : (
                        <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center">
                            <span className="text-sm font-bold text-white">
                                {clientName.charAt(0).toUpperCase()}
                            </span>
                        </div>
                    )}
                    <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-slate-900 truncate">{clientName}</p>
                        <p className="text-xs text-slate-500">Client</p>
                    </div>
                </div>

                {/* Talent assigné */}
                {mission.assignedTalent && (
                    <div className="flex items-center gap-3 p-3 bg-green-50 rounded-xl">
                        {mission.assignedTalent.profile?.avatarUrl ? (
                            <img
                                src={mission.assignedTalent.profile.avatarUrl}
                                alt=""
                                className="w-8 h-8 rounded-full object-cover"
                            />
                        ) : (
                            <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center">
                                <span className="text-xs font-bold text-white">
                                    {mission.assignedTalent.profile?.firstName?.charAt(0) || 'T'}
                                </span>
                            </div>
                        )}
                        <div className="flex-1">
                            <p className="text-sm font-medium text-green-700">
                                {mission.assignedTalent.profile
                                    ? `${mission.assignedTalent.profile.firstName} ${mission.assignedTalent.profile.lastName}`
                                    : mission.assignedTalent.email}
                            </p>
                            <p className="text-xs text-green-600">Talent assigné</p>
                        </div>
                        {mission.contract && (
                            <span className={`px-2 py-1 rounded text-xs font-medium ${
                                mission.contract.status === 'SIGNED'
                                    ? 'bg-green-100 text-green-700'
                                    : 'bg-amber-100 text-amber-700'
                            }`}>
                                {mission.contract.status === 'SIGNED' ? 'Contrat signé' : 'Signature en attente'}
                            </span>
                        )}
                    </div>
                )}

                {/* Infos */}
                <div className="grid grid-cols-2 gap-3 text-sm">
                    <div className="flex items-center gap-2 text-slate-600">
                        <MapPin className="w-4 h-4 text-slate-400" />
                        <span className="truncate">{mission.city}</span>
                    </div>
                    <div className="flex items-center gap-2 text-slate-600">
                        <Euro className="w-4 h-4 text-slate-400" />
                        <span>{formatCurrency(mission.hourlyRate)}/h</span>
                    </div>
                    <div className="flex items-center gap-2 text-slate-600">
                        <Calendar className="w-4 h-4 text-slate-400" />
                        <span>{formatDate(mission.startDate)}</span>
                    </div>
                    <div className="flex items-center gap-2 text-slate-600">
                        <Clock className="w-4 h-4 text-slate-400" />
                        <span>{mission.estimatedHours || '?'}h estimées</span>
                    </div>
                </div>

                {/* Candidatures */}
                {mission.status === 'OPEN' && mission._count && (
                    <div className="flex items-center gap-2 p-3 bg-slate-50 rounded-xl">
                        <User className="w-4 h-4 text-slate-500" />
                        <span className="text-sm text-slate-600">
                            <strong>{mission._count.applications}</strong> candidature(s)
                        </span>
                    </div>
                )}
            </div>

            {/* Footer */}
            <div className="px-5 py-3 bg-slate-50 border-t border-slate-100 flex items-center justify-between">
                <span className="text-xs text-slate-400">
                    Créée le {formatDate(mission.createdAt)}
                </span>
                <Link
                    href={`/admin/missions/${mission.id}`}
                    className="flex items-center gap-1 text-sm text-brand-600 font-medium hover:text-brand-700"
                >
                    Détails
                    <ChevronRight className="w-4 h-4" />
                </Link>
            </div>
        </motion.div>
    );
}

// ===========================================
// MAIN COMPONENT
// ===========================================

export default function MissionsPage() {
    const [missions, setMissions] = useState<Mission[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [statusFilter, setStatusFilter] = useState<StatusFilter>('ALL');
    const [urgencyFilter, setUrgencyFilter] = useState<UrgencyFilter>('ALL');
    const [searchQuery, setSearchQuery] = useState('');

    // Stats
    const stats = {
        total: missions.length,
        open: missions.filter(m => m.status === 'OPEN').length,
        inProgress: missions.filter(m => m.status === 'IN_PROGRESS').length,
        critical: missions.filter(m => m.urgencyLevel === 'CRITICAL' && m.status === 'OPEN').length,
    };

    useEffect(() => {
        fetchMissions();
    }, [statusFilter, urgencyFilter]);

    const fetchMissions = async () => {
        setIsLoading(true);
        try {
            const token = getToken();
            const params = new URLSearchParams();
            if (statusFilter !== 'ALL') params.append('status', statusFilter);
            if (urgencyFilter !== 'ALL') params.append('urgency', urgencyFilter);

            const headers: Record<string, string> = { 'Content-Type': 'application/json' };
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
            const res = await fetch(`${getApiBase()}/admin/missions?${params}`, {
                headers,
            });

            if (res.ok) {
                const data = await res.json();
                setMissions(data.missions || data || []);
            }
        } catch (err) {
            console.error('Erreur fetch missions:', err);
            // Mock data
            setMissions([
                {
                    id: '1',
                    title: 'Remplacement aide-soignant(e) urgent',
                    jobTitle: 'Aide-soignant(e)',
                    description: 'Remplacement urgent pour la nuit',
                    status: 'OPEN',
                    urgencyLevel: 'CRITICAL',
                    startDate: new Date(Date.now() + 86400000).toISOString(),
                    endDate: new Date(Date.now() + 172800000).toISOString(),
                    hourlyRate: 25,
                    estimatedHours: 8,
                    city: 'Lyon',
                    address: '12 rue de la Santé',
                    isNightShift: true,
                    client: {
                        id: 'c1',
                        email: 'contact@ehpad-lyon.fr',
                        establishment: { name: 'EHPAD Les Lilas' },
                    },
                    _count: { applications: 3 },
                    createdAt: new Date().toISOString(),
                },
                {
                    id: '2',
                    title: 'Atelier art-thérapie enfants',
                    jobTitle: 'Éducateur spécialisé',
                    description: 'Animation atelier créatif',
                    status: 'ASSIGNED',
                    urgencyLevel: 'MEDIUM',
                    startDate: new Date(Date.now() + 259200000).toISOString(),
                    endDate: new Date(Date.now() + 273600000).toISOString(),
                    hourlyRate: 35,
                    estimatedHours: 4,
                    city: 'Marseille',
                    address: 'IME Les Oliviers',
                    isNightShift: false,
                    client: {
                        id: 'c2',
                        email: 'ime@oliviers.fr',
                        establishment: { name: 'IME Les Oliviers' },
                    },
                    assignedTalent: {
                        id: 'e1',
                        email: 'marie@email.com',
                        profile: { firstName: 'Marie', lastName: 'Dupont' },
                    },
                    contract: { id: 'ctr1', status: 'SIGNED' },
                    _count: { applications: 5 },
                    createdAt: new Date(Date.now() - 86400000).toISOString(),
                },
                {
                    id: '3',
                    title: 'Accompagnement weekend',
                    jobTitle: 'Accompagnant éducatif',
                    description: 'Accompagnement le weekend',
                    status: 'IN_PROGRESS',
                    urgencyLevel: 'LOW',
                    startDate: new Date().toISOString(),
                    endDate: new Date(Date.now() + 172800000).toISOString(),
                    hourlyRate: 20,
                    estimatedHours: 16,
                    city: 'Paris',
                    address: 'Foyer Saint-Michel',
                    isNightShift: false,
                    client: {
                        id: 'c3',
                        email: 'foyer@stmichel.fr',
                        establishment: { name: 'Foyer Saint-Michel' },
                    },
                    assignedTalent: {
                        id: 'e2',
                        email: 'jean@email.com',
                        profile: { firstName: 'Jean', lastName: 'Martin' },
                    },
                    contract: { id: 'ctr2', status: 'SIGNED' },
                    createdAt: new Date(Date.now() - 172800000).toISOString(),
                },
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    // Filter missions
    const filteredMissions = missions.filter(m => {
        if (statusFilter !== 'ALL' && m.status !== statusFilter) return false;
        if (urgencyFilter !== 'ALL' && m.urgencyLevel !== urgencyFilter) return false;
        if (searchQuery) {
            const searchLower = searchQuery.toLowerCase();
            return (
                m.title.toLowerCase().includes(searchLower) ||
                m.city.toLowerCase().includes(searchLower) ||
                m.client.establishment?.name?.toLowerCase().includes(searchLower)
            );
        }
        return true;
    });

    return (
        <div className="min-h-screen bg-slate-100">
            {/* Header */}
            <header className="bg-white border-b border-slate-200 sticky top-0 z-40">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        <div className="flex items-center gap-4">
                            <Link href="/admin" className="p-2 rounded-xl hover:bg-slate-100 transition-colors">
                                <ChevronLeft className="w-5 h-5 text-slate-600" />
                            </Link>
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-600 to-brand-500 flex items-center justify-center">
                                    <Briefcase className="w-5 h-5 text-white" />
                                </div>
                                <div>
                                    <h1 className="font-bold text-slate-900">Gestion des Missions</h1>
                                    <p className="text-xs text-slate-500">SOS Renfort</p>
                                </div>
                            </div>
                        </div>
                        <button
                            onClick={fetchMissions}
                            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-100 text-slate-600 hover:bg-slate-200 transition-colors"
                        >
                            <RefreshCw className="w-4 h-4" />
                            Actualiser
                        </button>
                    </div>
                </div>
            </header>

            {/* Stats Bar */}
            <div className="bg-white border-b border-slate-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div className="bg-slate-50 rounded-xl p-4 text-center">
                            <p className="text-2xl font-bold text-slate-900">{stats.total}</p>
                            <p className="text-xs text-slate-500">Total missions</p>
                        </div>
                        <div className="bg-blue-50 rounded-xl p-4 text-center">
                            <p className="text-2xl font-bold text-blue-600">{stats.open}</p>
                            <p className="text-xs text-blue-600">Ouvertes</p>
                        </div>
                        <div className="bg-amber-50 rounded-xl p-4 text-center">
                            <p className="text-2xl font-bold text-amber-600">{stats.inProgress}</p>
                            <p className="text-xs text-amber-600">En cours</p>
                        </div>
                        <div className="bg-red-50 rounded-xl p-4 text-center">
                            <p className="text-2xl font-bold text-red-600">{stats.critical}</p>
                            <p className="text-xs text-red-600">Urgentes</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Filters */}
            <div className="bg-white border-b border-slate-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex flex-col md:flex-row gap-4">
                        {/* Search */}
                        <div className="relative flex-1">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                            <input
                                type="text"
                                placeholder="Rechercher une mission..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                            />
                        </div>

                        {/* Status Filter */}
                        <select
                            value={statusFilter}
                            onChange={(e) => setStatusFilter(e.target.value as StatusFilter)}
                            className="px-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                        >
                            <option value="ALL">Tous les statuts</option>
                            <option value="OPEN">Ouvertes</option>
                            <option value="ASSIGNED">Attribuées</option>
                            <option value="IN_PROGRESS">En cours</option>
                            <option value="COMPLETED">Terminées</option>
                            <option value="CANCELLED">Annulées</option>
                        </select>

                        {/* Urgency Filter */}
                        <select
                            value={urgencyFilter}
                            onChange={(e) => setUrgencyFilter(e.target.value as UrgencyFilter)}
                            className="px-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                        >
                            <option value="ALL">Toutes urgences</option>
                            <option value="CRITICAL">Immédiat</option>
                            <option value="HIGH">Sous 24h</option>
                            <option value="MEDIUM">Sous 48h</option>
                            <option value="LOW">Sous 1 semaine</option>
                        </select>
                    </div>
                </div>
            </div>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {isLoading ? (
                    <div className="flex items-center justify-center py-20">
                        <div className="text-center">
                            <Loader2 className="w-10 h-10 animate-spin text-brand-600 mx-auto mb-4" />
                            <p className="text-slate-500">Chargement des missions...</p>
                        </div>
                    </div>
                ) : filteredMissions.length === 0 ? (
                    <div className="text-center py-20 bg-white rounded-2xl border border-dashed border-slate-200">
                        <Briefcase className="w-16 h-16 text-slate-200 mx-auto mb-4" />
                        <h3 className="text-lg font-semibold text-slate-900 mb-2">Aucune mission</h3>
                        <p className="text-slate-500">Aucune mission ne correspond à vos critères.</p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {filteredMissions.map((mission) => (
                            <MissionCard key={mission.id} mission={mission} />
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}

