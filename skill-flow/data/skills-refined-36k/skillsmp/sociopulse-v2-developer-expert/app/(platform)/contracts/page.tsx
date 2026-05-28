'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import Cookies from 'js-cookie';
import {
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
    Plus,
    PenTool,
    Filter,
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
    TALENTSignedAt?: string;
    clientSignedAt?: string;
    pdfUrl?: string;
    createdAt: string;
    TALENT: {
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
        establishment?: { name: string };
        profile?: { firstName: string; lastName: string };
    };
    mission?: {
        id: string;
        title: string;
        city: string;
    };
}

interface Quote {
    id: string;
    reference: string;
    status: 'DRAFT' | 'SENT' | 'VIEWED' | 'ACCEPTED' | 'REJECTED' | 'EXPIRED';
    title: string;
    total: number;
    validUntil: string;
    createdAt: string;
    TALENT: {
        id: string;
        profile?: { firstName: string; lastName: string };
    };
    client: {
        id: string;
        establishment?: { name: string };
        profile?: { firstName: string; lastName: string };
    };
}

type TabType = 'contracts' | 'quotes';

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
// STATUS BADGES
// ===========================================

function ContractStatusBadge({ status }: { status: Contract['status'] }) {
    const config: Record<string, { bg: string; text: string; icon: React.ReactNode; label: string }> = {
        DRAFT: { bg: 'bg-slate-100', text: 'text-slate-600', icon: <FileText className="w-3.5 h-3.5" />, label: 'Brouillon' },
        PENDING: { bg: 'bg-amber-100', text: 'text-amber-700', icon: <Clock className="w-3.5 h-3.5" />, label: 'En attente' },
        PENDING_CLIENT: { bg: 'bg-orange-100', text: 'text-orange-700', icon: <PenTool className="w-3.5 h-3.5" />, label: 'Votre signature requise' },
        PENDING_TALENT: { bg: 'bg-purple-100', text: 'text-purple-700', icon: <PenTool className="w-3.5 h-3.5" />, label: 'Signature TALENT' },
        SIGNED: { bg: 'bg-green-100', text: 'text-green-700', icon: <CheckCircle className="w-3.5 h-3.5" />, label: 'Signé' },
        IN_PROGRESS: { bg: 'bg-blue-100', text: 'text-blue-700', icon: <Clock className="w-3.5 h-3.5" />, label: 'En cours' },
        COMPLETED: { bg: 'bg-emerald-100', text: 'text-emerald-700', icon: <FileCheck className="w-3.5 h-3.5" />, label: 'Terminé' },
        DISPUTED: { bg: 'bg-red-100', text: 'text-red-700', icon: <AlertTriangle className="w-3.5 h-3.5" />, label: 'Litige' },
        CANCELLED: { bg: 'bg-slate-100', text: 'text-slate-500', icon: <XCircle className="w-3.5 h-3.5" />, label: 'Annulé' },
    };

    const c = config[status] || config.PENDING;

    return (
        <span className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium ${c.bg} ${c.text}`}>
            {c.icon}
            {c.label}
        </span>
    );
}

function QuoteStatusBadge({ status }: { status: Quote['status'] }) {
    const config: Record<string, { bg: string; text: string; label: string }> = {
        DRAFT: { bg: 'bg-slate-100', text: 'text-slate-600', label: 'Brouillon' },
        SENT: { bg: 'bg-blue-100', text: 'text-blue-700', label: 'Envoyé' },
        VIEWED: { bg: 'bg-purple-100', text: 'text-purple-700', label: 'Consulté' },
        ACCEPTED: { bg: 'bg-green-100', text: 'text-green-700', label: 'Accepté' },
        REJECTED: { bg: 'bg-red-100', text: 'text-red-700', label: 'Refusé' },
        EXPIRED: { bg: 'bg-slate-100', text: 'text-slate-500', label: 'Expiré' },
    };

    const c = config[status] || config.DRAFT;

    return (
        <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium ${c.bg} ${c.text}`}>
            {c.label}
        </span>
    );
}

// ===========================================
// CONTRACT CARD
// ===========================================

function ContractCard({ contract, userRole }: { contract: Contract; userRole: 'TALENT' | 'CLIENT' }) {
    const otherParty = userRole === 'TALENT' ? contract.client : contract.TALENT;
    const establishmentName = otherParty && 'establishment' in otherParty
        ? (otherParty as any).establishment?.name
        : null;
    const otherName = otherParty
        ? establishmentName ||
          (otherParty.profile ? `${otherParty.profile.firstName} ${otherParty.profile.lastName}` : (otherParty as any).email)
        : 'N/A';

    const needsAction =
        (userRole === 'CLIENT' && contract.status === 'PENDING_CLIENT') ||
        (userRole === 'TALENT' && contract.status === 'PENDING_TALENT');

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`bg-white rounded-2xl border ${needsAction ? 'border-brand-200 shadow-brand-100' : 'border-slate-100'} overflow-hidden hover:shadow-lg transition-all`}
        >
            {needsAction && (
                <div className="px-4 py-2 bg-gradient-to-r from-rose-500 to-rose-600 text-white text-sm font-medium flex items-center gap-2">
                    <PenTool className="w-4 h-4" />
                    Action requise : Signez ce contrat
                </div>
            )}

            <div className="p-5">
                <div className="flex items-start justify-between mb-4">
                    <div>
                        <p className="font-mono text-sm text-slate-500 mb-1">
                            {contract.reference || `#${contract.id.slice(0, 8)}`}
                        </p>
                        <h3 className="font-semibold text-slate-900">
                            {contract.title || contract.mission?.title || 'Contrat'}
                        </h3>
                    </div>
                    <ContractStatusBadge status={contract.status} />
                </div>

                <div className="flex items-center gap-3 mb-4 p-3 bg-slate-50 rounded-xl">
                    <div className="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center">
                        {userRole === 'TALENT' ? (
                            <Building2 className="w-5 h-5 text-indigo-600" />
                        ) : (
                            <User className="w-5 h-5 text-indigo-600" />
                        )}
                    </div>
                    <div>
                        <p className="font-medium text-slate-900">{otherName}</p>
                        <p className="text-xs text-slate-500">{userRole === 'TALENT' ? 'Client' : 'TALENT'}</p>
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
                    {contract.totalAmount && (
                        <div className="flex items-center gap-2 text-slate-600">
                            <Euro className="w-4 h-4 text-slate-400" />
                            <span className="font-semibold">{formatCurrency(contract.totalAmount)}</span>
                        </div>
                    )}
                    <div className="flex items-center gap-2 text-slate-600">
                        <Calendar className="w-4 h-4 text-slate-400" />
                        <span>{formatDate(contract.createdAt)}</span>
                    </div>
                </div>

                <div className="flex gap-2">
                    <Link
                        href={`/contracts/${contract.id}`}
                        className={`flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl font-medium transition-colors ${
                            needsAction
                                ? 'bg-brand-600 text-white hover:bg-brand-700'
                                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                        }`}
                    >
                        {needsAction ? (
                            <>
                                <PenTool className="w-4 h-4" />
                                Signer
                            </>
                        ) : (
                            <>
                                <Eye className="w-4 h-4" />
                                Voir
                            </>
                        )}
                    </Link>
                    {contract.pdfUrl && (
                        <a
                            href={contract.pdfUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="px-4 py-2.5 rounded-xl bg-slate-100 text-slate-600 hover:bg-slate-200 transition-colors"
                        >
                            <Download className="w-4 h-4" />
                        </a>
                    )}
                </div>
            </div>
        </motion.div>
    );
}

// ===========================================
// QUOTE CARD
// ===========================================

function QuoteCard({ quote, userRole }: { quote: Quote; userRole: 'TALENT' | 'CLIENT' }) {
    const otherParty = userRole === 'TALENT' ? quote.client : quote.TALENT;
    const establishmentName = otherParty && 'establishment' in otherParty
        ? (otherParty as any).establishment?.name
        : null;
    const otherName = otherParty
        ? establishmentName ||
          (otherParty.profile ? `${otherParty.profile.firstName} ${otherParty.profile.lastName}` : '')
        : '';

    const needsAction = userRole === 'CLIENT' && (quote.status === 'SENT' || quote.status === 'VIEWED');
    const isExpired = new Date(quote.validUntil) < new Date();

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`bg-white rounded-2xl border ${needsAction ? 'border-blue-200' : 'border-slate-100'} p-5 hover:shadow-lg transition-all`}
        >
            <div className="flex items-start justify-between mb-4">
                <div>
                    <p className="font-mono text-sm text-slate-500 mb-1">{quote.reference}</p>
                    <h3 className="font-semibold text-slate-900">{quote.title}</h3>
                </div>
                <QuoteStatusBadge status={isExpired && quote.status !== 'ACCEPTED' ? 'EXPIRED' : quote.status} />
            </div>

            <div className="flex items-center gap-3 mb-4 p-3 bg-slate-50 rounded-xl">
                <div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center">
                    <User className="w-5 h-5 text-purple-600" />
                </div>
                <div>
                    <p className="font-medium text-slate-900">{otherName}</p>
                    <p className="text-xs text-slate-500">{userRole === 'TALENT' ? 'Client' : 'TALENT'}</p>
                </div>
            </div>

            <div className="flex items-center justify-between mb-4">
                <div>
                    <p className="text-xs text-slate-500">Montant</p>
                    <p className="text-xl font-bold text-slate-900">{formatCurrency(quote.total)}</p>
                </div>
                <div className="text-right">
                    <p className="text-xs text-slate-500">Valide jusqu'au</p>
                    <p className={`text-sm font-medium ${isExpired ? 'text-red-600' : 'text-slate-900'}`}>
                        {formatDate(quote.validUntil)}
                    </p>
                </div>
            </div>

            <div className="flex gap-2">
                <Link
                    href={`/quotes/${quote.id}`}
                    className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-slate-100 text-slate-700 hover:bg-slate-200 font-medium transition-colors"
                >
                    <Eye className="w-4 h-4" />
                    Voir le devis
                </Link>
                {needsAction && !isExpired && (
                    <Link
                        href={`/quotes/${quote.id}/respond`}
                        className="px-4 py-2.5 rounded-xl bg-green-500 text-white hover:bg-green-600 font-medium transition-colors"
                    >
                        Répondre
                    </Link>
                )}
            </div>
        </motion.div>
    );
}

// ===========================================
// MAIN COMPONENT
// ===========================================

export default function ContractsPage() {
    const [contracts, setContracts] = useState<Contract[]>([]);
    const [quotes, setQuotes] = useState<Quote[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [activeTab, setActiveTab] = useState<TabType>('contracts');
    const [userRole, setUserRole] = useState<'TALENT' | 'CLIENT'>('CLIENT');

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        setIsLoading(true);
        try {
            const token = getToken();
            const headers: Record<string, string> = { 'Content-Type': 'application/json' };
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }

            // Fetch user to get role
            const meRes = await fetch(`${getApiBase()}/auth/me`, { headers });
            if (meRes.ok) {
                const user = await meRes.json();
                setUserRole(user.role === 'TALENT' ? 'TALENT' : 'CLIENT');
            }

            // Fetch contracts
            const contractsRes = await fetch(`${getApiBase()}/contracts`, { headers });
            if (contractsRes.ok) {
                const data = await contractsRes.json();
                setContracts(data.contracts || data || []);
            }

            // Fetch quotes
            const quotesRes = await fetch(`${getApiBase()}/quotes`, { headers });
            if (quotesRes.ok) {
                const data = await quotesRes.json();
                setQuotes(data.quotes || data || []);
            }
        } catch (err) {
            console.error('Erreur fetch:', err);
            // Mock data
            setContracts([
                {
                    id: 'ctr1',
                    reference: 'CTR-2024-001',
                    type: 'MISSION_SOS',
                    status: 'PENDING_CLIENT',
                    title: 'Remplacement aide-soignant weekend',
                    totalAmount: 32000,
                    TALENTSignedAt: new Date().toISOString(),
                    createdAt: new Date(Date.now() - 86400000).toISOString(),
                    TALENT: { id: 'e1', email: 'marie@email.com', profile: { firstName: 'Marie', lastName: 'Dupont' } },
                    client: { id: 'c1', email: 'ehpad@email.com', establishment: { name: 'EHPAD Les Lilas' } },
                    mission: { id: 'm1', title: 'Remplacement weekend', city: 'Lyon' },
                },
                {
                    id: 'ctr2',
                    reference: 'CTR-2024-002',
                    type: 'SERVICE_BOOKING',
                    status: 'SIGNED',
                    title: 'Atelier art-thérapie mensuel',
                    totalAmount: 45000,
                    TALENTSignedAt: new Date().toISOString(),
                    clientSignedAt: new Date().toISOString(),
                    pdfUrl: '/contracts/ctr2.pdf',
                    createdAt: new Date(Date.now() - 604800000).toISOString(),
                    TALENT: { id: 'e2', email: 'jean@email.com', profile: { firstName: 'Jean', lastName: 'Martin' } },
                    client: { id: 'c1', email: 'ehpad@email.com', establishment: { name: 'EHPAD Les Lilas' } },
                },
            ]);
            setQuotes([
                {
                    id: 'q1',
                    reference: 'DEV-2024-005',
                    status: 'SENT',
                    title: 'Proposition atelier bien-être',
                    total: 35000,
                    validUntil: new Date(Date.now() + 604800000).toISOString(),
                    createdAt: new Date(Date.now() - 172800000).toISOString(),
                    TALENT: { id: 'e3', profile: { firstName: 'Sophie', lastName: 'Bernard' } },
                    client: { id: 'c1', establishment: { name: 'EHPAD Les Lilas' } },
                },
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    const pendingContracts = contracts.filter(c =>
        (userRole === 'CLIENT' && c.status === 'PENDING_CLIENT') ||
        (userRole === 'TALENT' && c.status === 'PENDING_TALENT')
    );

    const pendingQuotes = quotes.filter(q =>
        userRole === 'CLIENT' && (q.status === 'SENT' || q.status === 'VIEWED')
    );

    return (
        <div className="min-h-screen bg-slate-50 pb-20">
            {/* Header */}
            <header className="bg-white border-b border-slate-200 sticky top-0 z-40">
                <div className="max-w-4xl mx-auto px-4 py-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-xl font-bold text-slate-900">Mes Contrats</h1>
                            <p className="text-sm text-slate-500">Gérez vos contrats et devis</p>
                        </div>
                        {userRole === 'TALENT' && (
                            <Link
                                href="/quotes/new"
                                className="flex items-center gap-2 px-4 py-2 rounded-xl bg-brand-600 text-white font-medium hover:bg-brand-700 transition-colors"
                            >
                                <Plus className="w-4 h-4" />
                                Nouveau devis
                            </Link>
                        )}
                    </div>
                </div>
            </header>

            {/* Alerts */}
            {(pendingContracts.length > 0 || pendingQuotes.length > 0) && (
                <div className="max-w-4xl mx-auto px-4 py-4">
                    {pendingContracts.length > 0 && (
                        <div className="mb-3 p-4 bg-brand-50 border border-brand-200 rounded-xl flex items-center gap-3">
                            <PenTool className="w-5 h-5 text-brand-600" />
                            <p className="text-sm text-brand-700 font-medium">
                                {pendingContracts.length} contrat(s) en attente de votre signature
                            </p>
                        </div>
                    )}
                    {pendingQuotes.length > 0 && (
                        <div className="p-4 bg-blue-50 border border-blue-200 rounded-xl flex items-center gap-3">
                            <FileText className="w-5 h-5 text-blue-600" />
                            <p className="text-sm text-blue-700 font-medium">
                                {pendingQuotes.length} devis en attente de votre réponse
                            </p>
                        </div>
                    )}
                </div>
            )}

            {/* Tabs */}
            <div className="max-w-4xl mx-auto px-4 py-2">
                <div className="flex gap-2 bg-white rounded-xl p-1 border border-slate-200">
                    <button
                        onClick={() => setActiveTab('contracts')}
                        className={`flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                            activeTab === 'contracts'
                                ? 'bg-brand-600 text-white'
                                : 'text-slate-600 hover:bg-slate-100'
                        }`}
                    >
                        <FileCheck className="w-4 h-4" />
                        Contrats ({contracts.length})
                    </button>
                    <button
                        onClick={() => setActiveTab('quotes')}
                        className={`flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                            activeTab === 'quotes'
                                ? 'bg-brand-600 text-white'
                                : 'text-slate-600 hover:bg-slate-100'
                        }`}
                    >
                        <FileText className="w-4 h-4" />
                        Devis ({quotes.length})
                    </button>
                </div>
            </div>

            {/* Content */}
            <main className="max-w-4xl mx-auto px-4 py-6">
                {isLoading ? (
                    <div className="flex items-center justify-center py-20">
                        <Loader2 className="w-8 h-8 animate-spin text-brand-600" />
                    </div>
                ) : activeTab === 'contracts' ? (
                    contracts.length === 0 ? (
                        <div className="text-center py-20 bg-white rounded-2xl border border-dashed border-slate-200">
                            <FileCheck className="w-16 h-16 text-slate-200 mx-auto mb-4" />
                            <h3 className="text-lg font-semibold text-slate-900 mb-2">Aucun contrat</h3>
                            <p className="text-slate-500">Vos contrats apparaîtront ici</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {contracts.map((contract) => (
                                <ContractCard key={contract.id} contract={contract} userRole={userRole} />
                            ))}
                        </div>
                    )
                ) : quotes.length === 0 ? (
                    <div className="text-center py-20 bg-white rounded-2xl border border-dashed border-slate-200">
                        <FileText className="w-16 h-16 text-slate-200 mx-auto mb-4" />
                        <h3 className="text-lg font-semibold text-slate-900 mb-2">Aucun devis</h3>
                        <p className="text-slate-500">
                            {userRole === 'TALENT' ? 'Créez votre premier devis' : 'Vos devis apparaîtront ici'}
                        </p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {quotes.map((quote) => (
                            <QuoteCard key={quote.id} quote={quote} userRole={userRole} />
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}

