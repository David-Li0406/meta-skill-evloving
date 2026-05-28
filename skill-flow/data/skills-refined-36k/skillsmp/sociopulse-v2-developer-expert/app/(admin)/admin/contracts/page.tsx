'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import Cookies from 'js-cookie';
import {
    Shield,
    ChevronLeft,
    Search,
    FileText,
    FileCheck,
    Clock,
    CheckCircle,
    XCircle,
    AlertTriangle,
    User,
    Building2,
    Calendar,
    Euro,
    Loader2,
    ChevronRight,
    Eye,
    Download,
    RefreshCw,
    Filter,
    PenTool,
} from 'lucide-react';

// ===========================================
// TYPES
// ===========================================

interface Contract {
    id: string;
    reference?: string;
    type: 'MISSION_SOS' | 'SERVICE_BOOKING' | 'FRAMEWORK';
    status: 'DRAFT' | 'PENDING' | 'PENDING_CLIENT' | 'PENDING_TALENT' | 'SIGNED' | 'IN_PROGRESS' | 'COMPLETED' | 'DISPUTED' | 'CANCELLED';
    title?: string;
    totalAmount?: number;
    startDate?: string;
    endDate?: string;
    signedAt?: string;
    extraSignedAt?: string;
    clientSignedAt?: string;
    pdfUrl?: string;
    createdAt: string;
    talent: {
        id: string;
        email: string;
        profile?: {
            firstName: string;
            lastName: string;
            avatarUrl?: string;
        };
    };
    client?: {
        id: string;
        email: string;
        establishment?: {
            name: string;
        };
        profile?: {
            firstName: string;
            lastName: string;
        };
    };
    mission?: {
        id: string;
        title: string;
        city: string;
    };
    quote?: {
        id: string;
        reference: string;
    };
}

type StatusFilter = 'ALL' | 'PENDING' | 'SIGNED' | 'IN_PROGRESS' | 'COMPLETED' | 'DISPUTED';
type TypeFilter = 'ALL' | 'MISSION_SOS' | 'SERVICE_BOOKING' | 'FRAMEWORK';

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

const formatCurrency = (cents: number) => {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR',
    }).format(cents / 100);
};

// ===========================================
// STATUS BADGE
// ===========================================

function StatusBadge({ status }: { status: Contract['status'] }) {
    const config: Record<string, { bg: string; text: string; icon: React.ReactNode; label: string }> = {
        DRAFT: { bg: 'bg-slate-100', text: 'text-slate-600', icon: <FileText className="w-3.5 h-3.5" />, label: 'Brouillon' },
        PENDING: { bg: 'bg-amber-100', text: 'text-amber-700', icon: <Clock className="w-3.5 h-3.5" />, label: 'En attente' },
        PENDING_CLIENT: { bg: 'bg-orange-100', text: 'text-orange-700', icon: <PenTool className="w-3.5 h-3.5" />, label: 'Sign. Client' },
        PENDING_TALENT: { bg: 'bg-purple-100', text: 'text-purple-700', icon: <PenTool className="w-3.5 h-3.5" />, label: 'Sign. Talent' },
        SIGNED: { bg: 'bg-green-100', text: 'text-green-700', icon: <CheckCircle className="w-3.5 h-3.5" />, label: 'Signé' },
        IN_PROGRESS: { bg: 'bg-blue-100', text: 'text-blue-700', icon: <Clock className="w-3.5 h-3.5" />, label: 'En cours' },
        COMPLETED: { bg: 'bg-emerald-100', text: 'text-emerald-700', icon: <FileCheck className="w-3.5 h-3.5" />, label: 'Terminé' },
        DISPUTED: { bg: 'bg-red-100', text: 'text-red-700', icon: <AlertTriangle className="w-3.5 h-3.5" />, label: 'Litige' },
        CANCELLED: { bg: 'bg-slate-100', text: 'text-slate-500', icon: <XCircle className="w-3.5 h-3.5" />, label: 'Annulé' },
    };

    const c = config[status] || config.PENDING;

    return (
        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${c.bg} ${c.text}`}>
            {c.icon}
            {c.label}
        </span>
    );
}

// ===========================================
// TYPE BADGE
// ===========================================

function TypeBadge({ type }: { type: Contract['type'] }) {
    const config: Record<string, { bg: string; text: string; label: string }> = {
        MISSION_SOS: { bg: 'bg-rose-100', text: 'text-rose-700', label: 'Mission SOS' },
        SERVICE_BOOKING: { bg: 'bg-indigo-100', text: 'text-indigo-700', label: 'Service' },
        FRAMEWORK: { bg: 'bg-purple-100', text: 'text-purple-700', label: 'Contrat Cadre' },
    };

    const c = config[type] || config.MISSION_SOS;

    return (
        <span className={`px-2 py-0.5 rounded text-xs font-medium ${c.bg} ${c.text}`}>
            {c.label}
        </span>
    );
}

// ===========================================
// CONTRACT ROW
// ===========================================

function ContractRow({ contract }: { contract: Contract }) {
    const talentName = contract.talent.profile
        ? `${contract.talent.profile.firstName} ${contract.talent.profile.lastName}`
        : contract.talent.email;

    const clientName = contract.client
        ? contract.client.establishment?.name ||
          (contract.client.profile ? `${contract.client.profile.firstName} ${contract.client.profile.lastName}` : contract.client.email)
        : 'N/A';

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-xl border border-slate-100 p-4 hover:shadow-md transition-all"
        >
            <div className="flex items-center gap-4">
                {/* Reference & Type */}
                <div className="w-32 flex-shrink-0">
                    <p className="font-mono text-sm font-semibold text-slate-900">
                        {contract.reference || `#${contract.id.slice(0, 8)}`}
                    </p>
                    <TypeBadge type={contract.type} />
                </div>

                {/* Parties */}
                <div className="flex-1 min-w-0 grid grid-cols-2 gap-4">
                    {/* Extra */}
                    <div className="flex items-center gap-2">
                        {contract.talent.profile?.avatarUrl ? (
                            <img src={contract.talent.profile.avatarUrl} alt="" className="w-8 h-8 rounded-full object-cover" />
                        ) : (
                            <div className="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center">
                                <User className="w-4 h-4 text-purple-600" />
                            </div>
                        )}
                        <div className="min-w-0">
                            <p className="text-sm font-medium text-slate-900 truncate">{talentName}</p>
                            <p className="text-xs text-slate-500">Extra</p>
                        </div>
                        {contract.extraSignedAt && (
                            <span title="Signé"><CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0" /></span>
                        )}
                    </div>

                    {/* Client */}
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center">
                            <Building2 className="w-4 h-4 text-indigo-600" />
                        </div>
                        <div className="min-w-0">
                            <p className="text-sm font-medium text-slate-900 truncate">{clientName}</p>
                            <p className="text-xs text-slate-500">Client</p>
                        </div>
                        {contract.clientSignedAt && (
                            <span title="Signé"><CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0" /></span>
                        )}
                    </div>
                </div>

                {/* Amount */}
                <div className="w-24 text-right">
                    {contract.totalAmount ? (
                        <p className="font-semibold text-slate-900">{formatCurrency(contract.totalAmount)}</p>
                    ) : (
                        <p className="text-slate-400 text-sm">-</p>
                    )}
                </div>

                {/* Status */}
                <div className="w-28">
                    <StatusBadge status={contract.status} />
                </div>

                {/* Date */}
                <div className="w-24 text-right">
                    <p className="text-xs text-slate-500">{formatDate(contract.createdAt)}</p>
                </div>

                {/* Actions */}
                <div className="flex items-center gap-2">
                    {contract.pdfUrl && (
                        <a
                            href={contract.pdfUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="p-2 rounded-lg hover:bg-slate-100 text-slate-500 transition-colors"
                            title="Télécharger PDF"
                        >
                            <Download className="w-4 h-4" />
                        </a>
                    )}
                    <Link
                        href={`/admin/contracts/${contract.id}`}
                        className="p-2 rounded-lg hover:bg-rose-50 text-rose-600 transition-colors"
                        title="Voir détails"
                    >
                        <Eye className="w-4 h-4" />
                    </Link>
                </div>
            </div>

            {/* Mission info */}
            {contract.mission && (
                <div className="mt-3 pt-3 border-t border-slate-50 flex items-center gap-2 text-xs text-slate-500">
                    <FileText className="w-3.5 h-3.5" />
                    <span>Mission : {contract.mission.title}</span>
                    <span className="text-slate-300">•</span>
                    <span>{contract.mission.city}</span>
                </div>
            )}
        </motion.div>
    );
}

// ===========================================
// MAIN COMPONENT
// ===========================================

export default function ContractsAdminPage() {
    const [contracts, setContracts] = useState<Contract[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [statusFilter, setStatusFilter] = useState<StatusFilter>('ALL');
    const [typeFilter, setTypeFilter] = useState<TypeFilter>('ALL');
    const [searchQuery, setSearchQuery] = useState('');

    // Stats
    const stats = {
        total: contracts.length,
        pending: contracts.filter(c => ['PENDING', 'PENDING_CLIENT', 'PENDING_TALENT'].includes(c.status)).length,
        signed: contracts.filter(c => c.status === 'SIGNED').length,
        disputed: contracts.filter(c => c.status === 'DISPUTED').length,
    };

    useEffect(() => {
        fetchContracts();
    }, [statusFilter, typeFilter]);

    const fetchContracts = async () => {
        setIsLoading(true);
        try {
            const token = getToken();
            const params = new URLSearchParams();
            if (statusFilter !== 'ALL') params.append('status', statusFilter);
            if (typeFilter !== 'ALL') params.append('type', typeFilter);

            const headers: Record<string, string> = { 'Content-Type': 'application/json' };
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
            const res = await fetch(`${getApiBase()}/admin/contracts?${params}`, {
                headers,
            });

            if (res.ok) {
                const data = await res.json();
                setContracts(data.contracts || data || []);
            }
        } catch (err) {
            console.error('Erreur fetch contracts:', err);
            // Mock data
            setContracts([
                {
                    id: 'ctr1',
                    reference: 'CTR-2024-001',
                    type: 'MISSION_SOS',
                    status: 'SIGNED',
                    title: 'Remplacement aide-soignant',
                    totalAmount: 32000,
                    extraSignedAt: new Date().toISOString(),
                    clientSignedAt: new Date().toISOString(),
                    createdAt: new Date(Date.now() - 86400000).toISOString(),
                    talent: {
                        id: 'e1',
                        email: 'marie@email.com',
                        profile: { firstName: 'Marie', lastName: 'Dupont' },
                    },
                    client: {
                        id: 'c1',
                        email: 'ehpad@email.com',
                        establishment: { name: 'EHPAD Les Lilas' },
                    },
                    mission: { id: 'm1', title: 'Remplacement weekend', city: 'Lyon' },
                },
                {
                    id: 'ctr2',
                    reference: 'CTR-2024-002',
                    type: 'SERVICE_BOOKING',
                    status: 'PENDING_CLIENT',
                    title: 'Atelier art-thérapie',
                    totalAmount: 45000,
                    extraSignedAt: new Date().toISOString(),
                    createdAt: new Date(Date.now() - 172800000).toISOString(),
                    talent: {
                        id: 'e2',
                        email: 'jean@email.com',
                        profile: { firstName: 'Jean', lastName: 'Martin' },
                    },
                    client: {
                        id: 'c2',
                        email: 'ime@email.com',
                        establishment: { name: 'IME Les Oliviers' },
                    },
                },
                {
                    id: 'ctr3',
                    type: 'MISSION_SOS',
                    status: 'DISPUTED',
                    totalAmount: 28000,
                    createdAt: new Date(Date.now() - 259200000).toISOString(),
                    talent: {
                        id: 'e3',
                        email: 'paul@email.com',
                        profile: { firstName: 'Paul', lastName: 'Durand' },
                    },
                    client: {
                        id: 'c3',
                        email: 'foyer@email.com',
                        establishment: { name: 'Foyer Saint-Michel' },
                    },
                    mission: { id: 'm3', title: 'Accompagnement nuit', city: 'Paris' },
                },
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    // Filter contracts
    const filteredContracts = contracts.filter(c => {
        if (searchQuery) {
            const search = searchQuery.toLowerCase();
            const talentName = c.talent.profile ? `${c.talent.profile.firstName} ${c.talent.profile.lastName}` : c.talent.email;
            const clientName = c.client?.establishment?.name || c.client?.email || '';
            return (
                c.reference?.toLowerCase().includes(search) ||
                talentName.toLowerCase().includes(search) ||
                clientName.toLowerCase().includes(search)
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
                                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center">
                                    <FileCheck className="w-5 h-5 text-white" />
                                </div>
                                <div>
                                    <h1 className="font-bold text-slate-900">Gestion des Contrats</h1>
                                    <p className="text-xs text-slate-500">Devis & Contrats</p>
                                </div>
                            </div>
                        </div>
                        <button
                            onClick={fetchContracts}
                            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-100 text-slate-600 hover:bg-slate-200 transition-colors"
                        >
                            <RefreshCw className="w-4 h-4" />
                            Actualiser
                        </button>
                    </div>
                </div>
            </header>

            {/* Stats */}
            <div className="bg-white border-b border-slate-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div className="bg-slate-50 rounded-xl p-4 text-center">
                            <p className="text-2xl font-bold text-slate-900">{stats.total}</p>
                            <p className="text-xs text-slate-500">Total contrats</p>
                        </div>
                        <div className="bg-amber-50 rounded-xl p-4 text-center">
                            <p className="text-2xl font-bold text-amber-600">{stats.pending}</p>
                            <p className="text-xs text-amber-600">En attente signature</p>
                        </div>
                        <div className="bg-green-50 rounded-xl p-4 text-center">
                            <p className="text-2xl font-bold text-green-600">{stats.signed}</p>
                            <p className="text-xs text-green-600">Signés</p>
                        </div>
                        <div className="bg-red-50 rounded-xl p-4 text-center">
                            <p className="text-2xl font-bold text-red-600">{stats.disputed}</p>
                            <p className="text-xs text-red-600">Litiges</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Filters */}
            <div className="bg-white border-b border-slate-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex flex-col md:flex-row gap-4">
                        <div className="relative flex-1">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                            <input
                                type="text"
                                placeholder="Rechercher par référence, talent, client..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                            />
                        </div>

                        <select
                            value={statusFilter}
                            onChange={(e) => setStatusFilter(e.target.value as StatusFilter)}
                            className="px-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                        >
                            <option value="ALL">Tous les statuts</option>
                            <option value="PENDING">En attente</option>
                            <option value="SIGNED">Signés</option>
                            <option value="IN_PROGRESS">En cours</option>
                            <option value="COMPLETED">Terminés</option>
                            <option value="DISPUTED">Litiges</option>
                        </select>

                        <select
                            value={typeFilter}
                            onChange={(e) => setTypeFilter(e.target.value as TypeFilter)}
                            className="px-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                        >
                            <option value="ALL">Tous les types</option>
                            <option value="MISSION_SOS">Mission SOS</option>
                            <option value="SERVICE_BOOKING">Service</option>
                            <option value="FRAMEWORK">Contrat Cadre</option>
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
                            <p className="text-slate-500">Chargement des contrats...</p>
                        </div>
                    </div>
                ) : filteredContracts.length === 0 ? (
                    <div className="text-center py-20 bg-white rounded-2xl border border-dashed border-slate-200">
                        <FileCheck className="w-16 h-16 text-slate-200 mx-auto mb-4" />
                        <h3 className="text-lg font-semibold text-slate-900 mb-2">Aucun contrat</h3>
                        <p className="text-slate-500">Aucun contrat ne correspond à vos critères.</p>
                    </div>
                ) : (
                    <div className="space-y-4">
                        {filteredContracts.map((contract) => (
                            <ContractRow key={contract.id} contract={contract} />
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}





