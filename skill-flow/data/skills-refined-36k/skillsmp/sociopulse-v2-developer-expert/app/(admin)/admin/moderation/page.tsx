'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import Cookies from 'js-cookie';
import {
    Shield,
    FileText,
    Image as ImageIcon,
    Eye,
    Check,
    X,
    Loader2,
    Clock,
    AlertCircle,
    ChevronLeft,
    Filter,
    Search,
    User,
    Calendar,
    CheckCircle,
    XCircle,
    RefreshCw,
} from 'lucide-react';

// ===========================================
// TYPES
// ===========================================

interface DocumentToModerate {
    id: string;
    name: string;
    type: string;
    fileUrl: string;
    status: 'PENDING' | 'APPROVED' | 'REJECTED';
    comment?: string;
    createdAt: string;
    user: {
        id: string;
        email: string;
        role: 'CLIENT' | 'TALENT' | 'ADMIN';
        profile?: {
            firstName: string;
            lastName: string;
            avatarUrl?: string;
        };
        establishment?: {
            name: string;
        };
    };
}

type TabType = 'pending' | 'approved' | 'rejected';

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
        hour: '2-digit',
        minute: '2-digit',
    });
};

const getFileIcon = (type: string) => {
    if (type.includes('image') || type === 'ID_CARD' || type === 'PHOTO') {
        return <ImageIcon className="w-5 h-5" />;
    }
    return <FileText className="w-5 h-5" />;
};

const getDocTypeName = (type: string) => {
    const types: Record<string, string> = {
        ID_CARD: 'Carte d\'identité',
        DIPLOMA: 'Diplôme',
        CERTIFICATE: 'Certificat',
        INSURANCE: 'Assurance RC Pro',
        PHOTO: 'Photo de profil',
        KBIS: 'TALENTit Kbis',
        OTHER: 'Autre document',
    };
    return types[type] || type;
};

// ===========================================
// STATUS BADGE
// ===========================================

function StatusBadge({ status }: { status: string }) {
    const config: Record<string, { bg: string; text: string; icon: React.ReactNode; label: string }> = {
        PENDING: { bg: 'bg-amber-100', text: 'text-amber-700', icon: <Clock className="w-3.5 h-3.5" />, label: 'En attente' },
        APPROVED: { bg: 'bg-green-100', text: 'text-green-700', icon: <CheckCircle className="w-3.5 h-3.5" />, label: 'Approuvé' },
        REJECTED: { bg: 'bg-red-100', text: 'text-red-700', icon: <XCircle className="w-3.5 h-3.5" />, label: 'Rejeté' },
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
// DOCUMENT CARD
// ===========================================

function DocumentCard({
    doc,
    isLoading,
    onApprove,
    onReject,
    onView,
}: {
    doc: DocumentToModerate;
    isLoading: boolean;
    onApprove: () => void;
    onReject: () => void;
    onView: () => void;
}) {
    const userName = doc.user.profile
        ? `${doc.user.profile.firstName} ${doc.user.profile.lastName}`
        : doc.user.establishment?.name || doc.user.email;

    const userInitials = doc.user.profile
        ? `${doc.user.profile.firstName?.charAt(0) || ''}${doc.user.profile.lastName?.charAt(0) || ''}`
        : doc.user.establishment?.name?.charAt(0) || doc.user.email.charAt(0).toUpperCase();

    return (
        <motion.div
            layout
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden hover:shadow-md transition-all"
        >
            {/* Preview Image/Icon */}
            <div
                className="h-48 bg-slate-100 flex items-center justify-center cursor-pointer relative group"
                onClick={onView}
            >
                {doc.type.includes('image') || doc.type === 'ID_CARD' || doc.type === 'PHOTO' ? (
                    <img
                        src={doc.fileUrl}
                        alt={doc.name}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                            (e.target as HTMLImageElement).style.display = 'none';
                        }}
                    />
                ) : (
                    <FileText className="w-16 h-16 text-slate-300" />
                )}
                <div className="absolute inset-0 bg-slate-900/0 group-hover:bg-slate-900/50 flex items-center justify-center transition-all">
                    <Eye className="w-8 h-8 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>
                <StatusBadge status={doc.status} />
                <div className="absolute top-3 right-3">
                    <StatusBadge status={doc.status} />
                </div>
            </div>

            {/* Content */}
            <div className="p-4">
                {/* User Info */}
                <div className="flex items-center gap-3 mb-4">
                    {doc.user.profile?.avatarUrl ? (
                        <img
                            src={doc.user.profile.avatarUrl}
                            alt={userName}
                            className="w-10 h-10 rounded-full object-cover"
                        />
                    ) : (
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-brand-600 to-brand-500 flex items-center justify-center">
                            <span className="text-sm font-bold text-white">{userInitials}</span>
                        </div>
                    )}
                    <div className="flex-1 min-w-0">
                        <Link
                            href={`/admin/users/${doc.user.id}`}
                            className="font-medium text-slate-900 hover:text-brand-600 truncate block"
                        >
                            {userName}
                        </Link>
                        <p className="text-xs text-slate-500">
                            {doc.user.role === 'TALENT' ? 'Talent TALENT' : 'Client'}
                        </p>
                    </div>
                </div>

                {/* Document Info */}
                <div className="space-y-2 mb-4">
                    <div className="flex items-center gap-2">
                        {getFileIcon(doc.type)}
                        <span className="font-medium text-slate-900 text-sm">{getDocTypeName(doc.type)}</span>
                    </div>
                    <p className="text-xs text-slate-500 truncate">{doc.name}</p>
                    <div className="flex items-center gap-1 text-xs text-slate-400">
                        <Calendar className="w-3.5 h-3.5" />
                        {formatDate(doc.createdAt)}
                    </div>
                </div>

                {/* Comment if rejected */}
                {doc.status === 'REJECTED' && doc.comment && (
                    <div className="mb-4 p-3 bg-red-50 rounded-lg">
                        <p className="text-xs text-red-600">
                            <strong>Raison :</strong> {doc.comment}
                        </p>
                    </div>
                )}

                {/* Actions */}
                {doc.status === 'PENDING' && (
                    <div className="flex gap-2">
                        <button
                            onClick={onApprove}
                            disabled={isLoading}
                            className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-green-500 text-white font-medium hover:bg-green-600 transition-colors disabled:opacity-50"
                        >
                            {isLoading ? (
                                <Loader2 className="w-4 h-4 animate-spin" />
                            ) : (
                                <>
                                    <Check className="w-4 h-4" />
                                    Valider
                                </>
                            )}
                        </button>
                        <button
                            onClick={onReject}
                            disabled={isLoading}
                            className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-red-100 text-red-600 font-medium hover:bg-red-200 transition-colors disabled:opacity-50"
                        >
                            <X className="w-4 h-4" />
                            Rejeter
                        </button>
                    </div>
                )}

                {doc.status !== 'PENDING' && (
                    <button
                        onClick={onView}
                        className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-slate-100 text-slate-600 font-medium hover:bg-slate-200 transition-colors"
                    >
                        <Eye className="w-4 h-4" />
                        Voir le document
                    </button>
                )}
            </div>
        </motion.div>
    );
}

// ===========================================
// MAIN COMPONENT
// ===========================================

export default function ModerationPage() {
    const [documents, setDocuments] = useState<DocumentToModerate[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [actionLoading, setActionLoading] = useState<string | null>(null);
    const [activeTab, setActiveTab] = useState<TabType>('pending');
    const [searchQuery, setSearchQuery] = useState('');

    // Fetch documents
    useEffect(() => {
        fetchDocuments();
    }, [activeTab]);

    const fetchDocuments = async () => {
        setIsLoading(true);
        try {
            const token = getToken();
            const headers: Record<string, string> = { 'Content-Type': 'application/json' };
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
            const res = await fetch(`${getApiBase()}/admin/documents?status=${activeTab.toUpperCase()}`, {
                headers,
            });

            if (res.ok) {
                const data = await res.json();
                setDocuments(data.documents || data || []);
            }
        } catch (err) {
            console.error('Erreur fetch documents:', err);
            // Mock data for demo
            setDocuments([
                {
                    id: '1',
                    name: 'carte-identite-recto.jpg',
                    type: 'ID_CARD',
                    fileUrl: 'https://picsum.photos/400/300?random=1',
                    status: 'PENDING' as const,
                    createdAt: new Date(Date.now() - 3600000).toISOString(),
                    user: {
                        id: 'user1',
                        email: 'marie.dupont@email.com',
                        role: 'TALENT' as const,
                        profile: { firstName: 'Marie', lastName: 'Dupont' },
                    },
                },
                {
                    id: '2',
                    name: 'diplome-dees-2020.pdf',
                    type: 'DIPLOMA',
                    fileUrl: '/documents/diplome.pdf',
                    status: 'PENDING' as const,
                    createdAt: new Date(Date.now() - 7200000).toISOString(),
                    user: {
                        id: 'user2',
                        email: 'jean.martin@email.com',
                        role: 'TALENT' as const,
                        profile: { firstName: 'Jean', lastName: 'Martin' },
                    },
                },
                {
                    id: '3',
                    name: 'assurance-rc-pro.pdf',
                    type: 'INSURANCE',
                    fileUrl: '/documents/assurance.pdf',
                    status: 'PENDING' as const,
                    createdAt: new Date(Date.now() - 10800000).toISOString(),
                    user: {
                        id: 'user3',
                        email: 'contact@ehpad-soleil.fr',
                        role: 'CLIENT' as const,
                        establishment: { name: 'EHPAD Le Soleil' },
                    },
                },
            ].filter(d => d.status === activeTab.toUpperCase()));
        } finally {
            setIsLoading(false);
        }
    };

    // Handle approve
    const handleApprove = async (docId: string) => {
        setActionLoading(docId);
        try {
            const token = getToken();
            const approveHeaders: Record<string, string> = {
                'Content-Type': 'application/json',
            };
            if (token) {
                approveHeaders['Authorization'] = `Bearer ${token}`;
            }
            const res = await fetch(`${getApiBase()}/admin/documents/${docId}/status`, {
                method: 'PATCH',
                headers: approveHeaders,
                body: JSON.stringify({ status: 'APPROVED' }),
            });

            if (res.ok) {
                setDocuments(prev => prev.filter(d => d.id !== docId));
            }
        } catch (err) {
            console.error('Erreur approve:', err);
        } finally {
            setActionLoading(null);
        }
    };

    // Handle reject
    const handleReject = async (docId: string) => {
        const reason = prompt('Raison du rejet (sera visible par l\'utilisateur) :');
        if (!reason) return;

        setActionLoading(docId);
        try {
            const token = getToken();
            const rejectHeaders: Record<string, string> = {
                'Content-Type': 'application/json',
            };
            if (token) {
                rejectHeaders['Authorization'] = `Bearer ${token}`;
            }
            const res = await fetch(`${getApiBase()}/admin/documents/${docId}/status`, {
                method: 'PATCH',
                headers: rejectHeaders,
                body: JSON.stringify({ status: 'REJECTED', comment: reason }),
            });

            if (res.ok) {
                setDocuments(prev => prev.filter(d => d.id !== docId));
            }
        } catch (err) {
            console.error('Erreur reject:', err);
        } finally {
            setActionLoading(null);
        }
    };

    // Handle view
    const handleView = (doc: DocumentToModerate) => {
        window.open(doc.fileUrl, '_blank');
    };

    // Filter documents
    const filteredDocuments = documents.filter(doc => {
        if (!searchQuery) return true;
        const userName = doc.user.profile
            ? `${doc.user.profile.firstName} ${doc.user.profile.lastName}`
            : doc.user.establishment?.name || doc.user.email;
        return userName.toLowerCase().includes(searchQuery.toLowerCase()) ||
            doc.name.toLowerCase().includes(searchQuery.toLowerCase());
    });

    const tabCounts = {
        pending: documents.filter(d => d.status === 'PENDING').length,
        approved: 0,
        rejected: 0,
    };

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
                                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center">
                                    <FileText className="w-5 h-5 text-white" />
                                </div>
                                <div>
                                    <h1 className="font-bold text-slate-900">Centre de Modération</h1>
                                    <p className="text-xs text-slate-500">Validation des documents</p>
                                </div>
                            </div>
                        </div>
                        <button
                            onClick={fetchDocuments}
                            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-100 text-slate-600 hover:bg-slate-200 transition-colors"
                        >
                            <RefreshCw className="w-4 h-4" />
                            Actualiser
                        </button>
                    </div>
                </div>
            </header>

            {/* Tabs & Search */}
            <div className="bg-white border-b border-slate-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 py-4">
                        {/* Tabs */}
                        <div className="flex gap-2">
                            {[
                                { key: 'pending', label: 'En attente', icon: Clock },
                                { key: 'approved', label: 'Approuvés', icon: CheckCircle },
                                { key: 'rejected', label: 'Rejetés', icon: XCircle },
                            ].map((tab) => (
                                <button
                                    key={tab.key}
                                    onClick={() => setActiveTab(tab.key as TabType)}
                                    className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-colors ${
                                        activeTab === tab.key
                                            ? 'bg-brand-600 text-white'
                                            : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                                    }`}
                                >
                                    <tab.icon className="w-4 h-4" />
                                    {tab.label}
                                    {tab.key === 'pending' && tabCounts.pending > 0 && (
                                        <span className={`px-1.5 py-0.5 rounded-full text-xs ${
                                            activeTab === tab.key ? 'bg-white/20' : 'bg-brand-600 text-white'
                                        }`}>
                                            {tabCounts.pending}
                                        </span>
                                    )}
                                </button>
                            ))}
                        </div>

                        {/* Search */}
                        <div className="relative">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                            <input
                                type="text"
                                placeholder="Rechercher un utilisateur..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="pl-10 pr-4 py-2 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent w-full sm:w-64"
                            />
                        </div>
                    </div>
                </div>
            </div>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {isLoading ? (
                    <div className="flex items-center justify-center py-20">
                        <div className="text-center">
                            <Loader2 className="w-10 h-10 animate-spin text-brand-600 mx-auto mb-4" />
                            <p className="text-slate-500">Chargement des documents...</p>
                        </div>
                    </div>
                ) : filteredDocuments.length === 0 ? (
                    <div className="text-center py-20 bg-white rounded-2xl border border-dashed border-slate-200">
                        <FileText className="w-16 h-16 text-slate-200 mx-auto mb-4" />
                        <h3 className="text-lg font-semibold text-slate-900 mb-2">
                            {activeTab === 'pending' ? 'Aucun document en attente' : 'Aucun document'}
                        </h3>
                        <p className="text-slate-500">
                            {activeTab === 'pending'
                                ? 'Tous les documents ont été traités !'
                                : 'Aucun document dans cette catégorie.'}
                        </p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        <AnimatePresence mode="popLayout">
                            {filteredDocuments.map((doc) => (
                                <DocumentCard
                                    key={doc.id}
                                    doc={doc}
                                    isLoading={actionLoading === doc.id}
                                    onApprove={() => handleApprove(doc.id)}
                                    onReject={() => handleReject(doc.id)}
                                    onView={() => handleView(doc)}
                                />
                            ))}
                        </AnimatePresence>
                    </div>
                )}
            </main>
        </div>
    );
}

