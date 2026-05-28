'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import Cookies from 'js-cookie';
import {
    ChevronLeft,
    Mail,
    Phone,
    Building2,
    MapPin,
    Calendar,
    BadgeCheck,
    Clock,
    AlertCircle,
    XCircle,
    FileText,
    Image as ImageIcon,
    Eye,
    Check,
    X,
    Send,
    Loader2,
    Shield,
    MessageSquare,
    ExternalLink,
    KeyRound,
    Ban,
    ToggleLeft,
    ToggleRight,
} from 'lucide-react';
import Link from 'next/link';

// ===========================================
// TYPES
// ===========================================

interface UserDocument {
    id: string;
    name: string;
    type: string;
    fileUrl: string;
    status: 'PENDING' | 'APPROVED' | 'REJECTED';
    comment?: string;
    createdAt: string;
}

interface AdminNote {
    id: string;
    content: string;
    createdAt: string;
    admin: {
        email: string;
        profile?: {
            firstName?: string;
            lastName?: string;
        };
    };
}

interface UserDetail {
    id: string;
    email: string;
    phone?: string;
    role: 'CLIENT' | 'TALENT' | 'ADMIN';
    status: 'PENDING' | 'VERIFIED' | 'SUSPENDED' | 'BANNED';
    clientType?: 'PARTICULAR' | 'ESTABLISHMENT';
    isVerified: boolean;
    onboardingStep: number;
    createdAt: string;
    profile?: {
        firstName: string;
        lastName: string;
        avatarUrl?: string;
        city?: string;
        postalCode?: string;
        address?: string;
        bio?: string;
        specialties?: string[];
    };
    establishment?: {
        name: string;
        siret?: string;
        type?: string;
        city?: string;
        address?: string;
    };
    documents: UserDocument[];
    adminNotesReceived: AdminNote[];
    _count?: {
        bookingsAsClient: number;
        bookingsAsProvider: number;
        missionsAsClient: number;
        missionsAsTalent: number;
    };
}

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

// ===========================================
// STATUS BADGE COMPONENT
// ===========================================

function StatusBadge({ status }: { status: string }) {
    const config: Record<string, { bg: string; text: string; icon: React.ReactNode; label: string }> = {
        PENDING: { bg: 'bg-amber-100', text: 'text-amber-700', icon: <Clock className="w-3.5 h-3.5" />, label: 'En attente' },
        VERIFIED: { bg: 'bg-green-100', text: 'text-green-700', icon: <BadgeCheck className="w-3.5 h-3.5" />, label: 'Vérifié' },
        APPROVED: { bg: 'bg-green-100', text: 'text-green-700', icon: <Check className="w-3.5 h-3.5" />, label: 'Approuvé' },
        SUSPENDED: { bg: 'bg-orange-100', text: 'text-orange-700', icon: <AlertCircle className="w-3.5 h-3.5" />, label: 'Suspendu' },
        BANNED: { bg: 'bg-red-100', text: 'text-red-700', icon: <XCircle className="w-3.5 h-3.5" />, label: 'Banni' },
        REJECTED: { bg: 'bg-red-100', text: 'text-red-700', icon: <X className="w-3.5 h-3.5" />, label: 'Rejeté' },
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
// DOCUMENT ROW COMPONENT
// ===========================================

function DocumentRow({
    doc,
    isLoading,
    onApprove,
    onReject,
}: {
    doc: UserDocument;
    isLoading: boolean;
    onApprove: () => void;
    onReject: () => void;
}) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="group p-4 rounded-xl border border-slate-100 hover:border-slate-200 hover:shadow-sm transition-all bg-white"
        >
            <div className="flex items-start gap-3">
                <div className={`
                    w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0
                    ${doc.status === 'APPROVED' ? 'bg-green-100 text-green-600' :
                        doc.status === 'REJECTED' ? 'bg-red-100 text-red-600' :
                            'bg-amber-100 text-amber-600'}
                `}>
                    {getFileIcon(doc.type)}
                </div>

                <div className="flex-1 min-w-0">
                    <p className="font-medium text-slate-900 text-sm truncate">{doc.name}</p>
                    <p className="text-xs text-slate-500 mt-0.5">{doc.type} • {formatDate(doc.createdAt)}</p>
                    <div className="mt-2">
                        <StatusBadge status={doc.status} />
                    </div>
                    {doc.comment && (
                        <p className="mt-2 text-xs text-slate-500 italic bg-slate-50 p-2 rounded-lg">"{doc.comment}"</p>
                    )}
                </div>

                {/* Actions */}
                <div className="flex flex-col gap-2">
                    <a
                        href={doc.fileUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-100 text-slate-600 hover:bg-slate-200 text-xs font-medium transition-colors"
                    >
                        <Eye className="w-3.5 h-3.5" />
                        Voir
                    </a>

                    {doc.status === 'PENDING' && (
                        <div className="flex gap-1">
                            <button
                                onClick={onApprove}
                                disabled={isLoading}
                                className="flex-1 p-2 rounded-lg bg-green-100 text-green-600 hover:bg-green-200 transition-colors disabled:opacity-50"
                                title="Valider"
                            >
                                {isLoading ? <Loader2 className="w-4 h-4 animate-spin mx-auto" /> : <Check className="w-4 h-4 mx-auto" />}
                            </button>
                            <button
                                onClick={onReject}
                                disabled={isLoading}
                                className="flex-1 p-2 rounded-lg bg-red-100 text-red-600 hover:bg-red-200 transition-colors disabled:opacity-50"
                                title="Rejeter"
                            >
                                <X className="w-4 h-4 mx-auto" />
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </motion.div>
    );
}

// ===========================================
// MAIN COMPONENT
// ===========================================

export default function AdminUserDetailPage() {
    const params = useParams();
    const router = useRouter();
    const userId = params.id as string;

    const [user, setUser] = useState<UserDetail | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [newNote, setNewNote] = useState('');
    const [isSendingNote, setIsSendingNote] = useState(false);
    const [actionLoading, setActionLoading] = useState<string | null>(null);

    // Fetch user details
    useEffect(() => {
        const fetchUser = async () => {
            setIsLoading(true);
            try {
                const token = getToken();
                const headers: Record<string, string> = { 'Content-Type': 'application/json' };
                if (token) {
                    headers['Authorization'] = `Bearer ${token}`;
                }
                const res = await fetch(`${getApiBase()}/admin/users/${userId}`, {
                    headers,
                });

                if (!res.ok) throw new Error('Utilisateur non trouvé');

                const data = await res.json();
                setUser(data);
            } catch (err: any) {
                setError(err.message);
            } finally {
                setIsLoading(false);
            }
        };

        if (userId) fetchUser();
    }, [userId]);

    // Toggle verification
    const handleToggleVerification = async () => {
        if (!user) return;
        setActionLoading('verify');

        try {
            const token = getToken();
            const endpoint = user.isVerified ? 'unverify' : 'verify';
            const verifyHeaders: Record<string, string> = {
                'Content-Type': 'application/json',
            };
            if (token) {
                verifyHeaders['Authorization'] = `Bearer ${token}`;
            }
            const res = await fetch(`${getApiBase()}/admin/users/${userId}/${endpoint}`, {
                method: 'PATCH',
                headers: verifyHeaders,
            });

            if (res.ok) {
                setUser(prev => prev ? {
                    ...prev,
                    isVerified: !prev.isVerified,
                    status: !prev.isVerified ? 'VERIFIED' : 'PENDING'
                } : null);
            }
        } catch (err) {
            console.error('Erreur vérification:', err);
        } finally {
            setActionLoading(null);
        }
    };

    // Suspend user
    const handleSuspend = async () => {
        if (!user || user.status === 'SUSPENDED') return;
        const reason = prompt('Raison de la suspension :');
        if (!reason) return;

        setActionLoading('suspend');
        try {
            const token = getToken();
            const suspendHeaders: Record<string, string> = {
                'Content-Type': 'application/json',
            };
            if (token) {
                suspendHeaders['Authorization'] = `Bearer ${token}`;
            }
            const res = await fetch(`${getApiBase()}/admin/users/${userId}/suspend`, {
                method: 'PATCH',
                headers: suspendHeaders,
                body: JSON.stringify({ reason }),
            });

            if (res.ok) {
                setUser(prev => prev ? { ...prev, status: 'SUSPENDED' } : null);
            }
        } catch (err) {
            console.error('Erreur suspension:', err);
        } finally {
            setActionLoading(null);
        }
    };

    // Reset password
    const handleResetPassword = async () => {
        if (!confirm('Envoyer un email de réinitialisation de mot de passe ?')) return;

        setActionLoading('password');
        try {
            const token = getToken();
            const resetHeaders: Record<string, string> = { 'Content-Type': 'application/json' };
            if (token) {
                resetHeaders['Authorization'] = `Bearer ${token}`;
            }
            await fetch(`${getApiBase()}/admin/users/${userId}/reset-password`, {
                method: 'POST',
                headers: resetHeaders,
            });
            alert('Email de réinitialisation envoyé !');
        } catch (err) {
            console.error('Erreur reset password:', err);
        } finally {
            setActionLoading(null);
        }
    };

    // Update document status
    const handleDocumentAction = async (docId: string, status: 'APPROVED' | 'REJECTED', comment?: string) => {
        setActionLoading(docId);

        try {
            const token = getToken();
            const docHeaders: Record<string, string> = {
                'Content-Type': 'application/json',
            };
            if (token) {
                docHeaders['Authorization'] = `Bearer ${token}`;
            }
            const res = await fetch(`${getApiBase()}/admin/documents/${docId}/status`, {
                method: 'PATCH',
                headers: docHeaders,
                body: JSON.stringify({ status, comment }),
            });

            if (res.ok) {
                setUser(prev => {
                    if (!prev) return null;
                    return {
                        ...prev,
                        documents: prev.documents.map(d =>
                            d.id === docId ? { ...d, status, comment } : d
                        ),
                    };
                });
            }
        } catch (err) {
            console.error('Erreur document:', err);
        } finally {
            setActionLoading(null);
        }
    };

    // Add note
    const handleAddNote = async () => {
        if (!newNote.trim()) return;
        setIsSendingNote(true);

        try {
            const token = getToken();
            const noteHeaders: Record<string, string> = {
                'Content-Type': 'application/json',
            };
            if (token) {
                noteHeaders['Authorization'] = `Bearer ${token}`;
            }
            const res = await fetch(`${getApiBase()}/admin/users/${userId}/notes`, {
                method: 'POST',
                headers: noteHeaders,
                body: JSON.stringify({ content: newNote }),
            });

            if (res.ok) {
                const note = await res.json();
                setUser(prev => {
                    if (!prev) return null;
                    return {
                        ...prev,
                        adminNotesReceived: [note, ...prev.adminNotesReceived],
                    };
                });
                setNewNote('');
            }
        } catch (err) {
            console.error('Erreur note:', err);
        } finally {
            setIsSendingNote(false);
        }
    };

    // Loading state
    if (isLoading) {
        return (
            <div className="min-h-screen bg-slate-50 flex items-center justify-center">
                <div className="text-center">
                    <Loader2 className="w-10 h-10 animate-spin text-brand-600 mx-auto mb-4" />
                    <p className="text-slate-500">Chargement du profil...</p>
                </div>
            </div>
        );
    }

    // Error state
    if (error || !user) {
        return (
            <div className="min-h-screen bg-slate-50 flex items-center justify-center">
                <div className="text-center bg-white p-8 rounded-2xl shadow-soft">
                    <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
                    <h2 className="text-xl font-semibold text-slate-900 mb-2">Erreur</h2>
                    <p className="text-slate-500 mb-4">{error || 'Utilisateur non trouvé'}</p>
                    <Link href="/admin/users" className="text-brand-600 font-medium hover:underline">
                        Retour à l'annuaire
                    </Link>
                </div>
            </div>
        );
    }

    const displayName = user.profile
        ? `${user.profile.firstName} ${user.profile.lastName}`
        : user.establishment?.name || user.email;

    const initials = user.profile
        ? `${user.profile.firstName?.charAt(0) || ''}${user.profile.lastName?.charAt(0) || ''}`
        : user.establishment?.name?.charAt(0) || user.email.charAt(0).toUpperCase();

    const pendingDocsCount = user.documents.filter(d => d.status === 'PENDING').length;

    return (
        <div className="min-h-screen bg-slate-100">
            {/* Header */}
            <header className="bg-white border-b border-slate-200 sticky top-0 z-40">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        <div className="flex items-center gap-4">
                            <button
                                onClick={() => router.back()}
                                className="p-2 rounded-xl hover:bg-slate-100 transition-colors"
                            >
                                <ChevronLeft className="w-5 h-5 text-slate-600" />
                            </button>
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                                    <Shield className="w-5 h-5 text-white" />
                                </div>
                                <div>
                                    <h1 className="font-bold text-slate-900">Fiche Utilisateur</h1>
                                    <p className="text-xs text-slate-500">Vue 360° - CRM Admin</p>
                                </div>
                            </div>
                        </div>
                        <StatusBadge status={user.status} />
                    </div>
                </div>
            </header>

            {/* Main Content - Grid 2/3 - 1/3 */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

                    {/* ========================================= */}
                    {/* COLONNE GAUCHE (2/3) */}
                    {/* ========================================= */}
                    <div className="lg:col-span-2 space-y-6">

                        {/* CARTE IDENTITÉ */}
                        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
                            {/* Header avec gradient */}
                            <div className="h-28 bg-gradient-to-r from-brand-100 via-slate-50 to-indigo-100 relative">
                                {/* SWITCH VÉRIFIÉ en haut à droite */}
                                <div className="absolute top-4 right-4">
                                    <button
                                        onClick={handleToggleVerification}
                                        disabled={actionLoading === 'verify'}
                                        className={`
                                            flex items-center gap-2 px-4 py-2 rounded-full font-semibold text-sm transition-all
                                            ${user.isVerified
                                                ? 'bg-green-500 text-white hover:bg-green-600'
                                                : 'bg-slate-200 text-slate-600 hover:bg-slate-300'}
                                        `}
                                    >
                                        {actionLoading === 'verify' ? (
                                            <Loader2 className="w-5 h-5 animate-spin" />
                                        ) : user.isVerified ? (
                                            <ToggleRight className="w-5 h-5" />
                                        ) : (
                                            <ToggleLeft className="w-5 h-5" />
                                        )}
                                        {user.isVerified ? 'COMPTE VÉRIFIÉ' : 'NON VÉRIFIÉ'}
                                    </button>
                                </div>
                            </div>

                            {/* Avatar + Infos */}
                            <div className="px-6 -mt-14 pb-6">
                                <div className="flex items-end gap-4 mb-6">
                                    {/* Avatar géant */}
                                    <div className="relative">
                                        {user.profile?.avatarUrl ? (
                                            <img
                                                src={user.profile.avatarUrl}
                                                alt={displayName}
                                                className="w-28 h-28 rounded-2xl border-4 border-white shadow-lg object-cover"
                                            />
                                        ) : (
                                            <div className="w-28 h-28 rounded-2xl border-4 border-white shadow-lg bg-gradient-to-br from-brand-600 to-brand-500 flex items-center justify-center">
                                                <span className="text-3xl font-bold text-white">{initials}</span>
                                            </div>
                                        )}
                                        {user.isVerified && (
                                            <div className="absolute -bottom-2 -right-2 w-8 h-8 rounded-full bg-green-500 border-2 border-white flex items-center justify-center">
                                                <BadgeCheck className="w-4 h-4 text-white" />
                                            </div>
                                        )}
                                    </div>

                                    {/* Nom et badges */}
                                    <div className="flex-1 pb-2">
                                        <h2 className="text-2xl font-bold text-slate-900">{displayName}</h2>
                                        <div className="flex flex-wrap gap-2 mt-2">
                                            <span className={`
                                                px-3 py-1 rounded-lg text-xs font-semibold
                                                ${user.role === 'TALENT' ? 'bg-purple-100 text-purple-700' :
                                                    user.role === 'CLIENT' ? 'bg-blue-100 text-blue-700' :
                                                        'bg-slate-100 text-slate-700'}
                                            `}>
                                                {user.role === 'TALENT' ? 'Talent Extra' : user.role === 'CLIENT' ? 'Client' : 'Admin'}
                                            </span>
                                            {user.clientType && (
                                                <span className="px-3 py-1 rounded-lg bg-indigo-100 text-indigo-700 text-xs font-semibold">
                                                    {user.clientType === 'ESTABLISHMENT' ? 'Établissement' : 'Particulier'}
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                </div>

                                {/* Grille d'infos */}
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-slate-100">
                                    <div className="flex items-center gap-3 p-3 bg-slate-50 rounded-xl">
                                        <Mail className="w-5 h-5 text-brand-600" />
                                        <div>
                                            <p className="text-xs text-slate-500">Email</p>
                                            <p className="text-sm font-medium text-slate-900">{user.email}</p>
                                        </div>
                                    </div>
                                    {user.phone && (
                                        <div className="flex items-center gap-3 p-3 bg-slate-50 rounded-xl">
                                            <Phone className="w-5 h-5 text-brand-600" />
                                            <div>
                                                <p className="text-xs text-slate-500">Téléphone</p>
                                                <p className="text-sm font-medium text-slate-900">{user.phone}</p>
                                            </div>
                                        </div>
                                    )}
                                    {(user.profile?.address || user.establishment?.address || user.profile?.city || user.establishment?.city) && (
                                        <div className="flex items-center gap-3 p-3 bg-slate-50 rounded-xl">
                                            <MapPin className="w-5 h-5 text-brand-600" />
                                            <div>
                                                <p className="text-xs text-slate-500">Adresse</p>
                                                <p className="text-sm font-medium text-slate-900">
                                                    {user.profile?.address || user.establishment?.address || user.profile?.city || user.establishment?.city}
                                                </p>
                                            </div>
                                        </div>
                                    )}
                                    {user.establishment?.siret && (
                                        <div className="flex items-center gap-3 p-3 bg-slate-50 rounded-xl">
                                            <Building2 className="w-5 h-5 text-brand-600" />
                                            <div>
                                                <p className="text-xs text-slate-500">SIRET</p>
                                                <p className="text-sm font-medium text-slate-900">{user.establishment.siret}</p>
                                            </div>
                                        </div>
                                    )}
                                    <div className="flex items-center gap-3 p-3 bg-slate-50 rounded-xl">
                                        <Calendar className="w-5 h-5 text-brand-600" />
                                        <div>
                                            <p className="text-xs text-slate-500">Inscription</p>
                                            <p className="text-sm font-medium text-slate-900">{formatDate(user.createdAt)}</p>
                                        </div>
                                    </div>
                                </div>

                                {/* Stats */}
                                {user._count && (
                                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-6">
                                        <div className="text-center p-4 bg-gradient-to-br from-brand-50 to-brand-100 rounded-xl border border-brand-100">
                                            <p className="text-2xl font-bold text-brand-600">
                                                {user._count.bookingsAsClient + user._count.bookingsAsProvider}
                                            </p>
                                            <p className="text-xs text-slate-500">Réservations</p>
                                        </div>
                                        <div className="text-center p-4 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl border border-indigo-100">
                                            <p className="text-2xl font-bold text-indigo-600">
                                                {user._count.missionsAsClient + user._count.missionsAsTalent}
                                            </p>
                                            <p className="text-xs text-slate-500">Missions</p>
                                        </div>
                                        <div className="text-center p-4 bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl border border-green-100">
                                            <p className="text-2xl font-bold text-green-600">
                                                {user.documents.filter(d => d.status === 'APPROVED').length}
                                            </p>
                                            <p className="text-xs text-slate-500">Docs validés</p>
                                        </div>
                                        <div className="text-center p-4 bg-gradient-to-br from-amber-50 to-yellow-50 rounded-xl border border-amber-100">
                                            <p className="text-2xl font-bold text-amber-600">{user.onboardingStep}</p>
                                            <p className="text-xs text-slate-500">Étape onboarding</p>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* CARTE DOCUMENTS */}
                        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
                            <div className="p-6 border-b border-slate-100 flex items-center justify-between">
                                <h3 className="font-semibold text-slate-900 flex items-center gap-2">
                                    <FileText className="w-5 h-5 text-slate-400" />
                                    Documents justificatifs
                                </h3>
                                {pendingDocsCount > 0 && (
                                    <span className="px-3 py-1 rounded-full bg-amber-100 text-amber-700 text-xs font-semibold">
                                        {pendingDocsCount} en attente
                                    </span>
                                )}
                            </div>

                            <div className="p-4 space-y-3 max-h-[400px] overflow-y-auto bg-slate-50">
                                {user.documents.length === 0 ? (
                                    <div className="text-center py-12 bg-white rounded-xl border border-dashed border-slate-200">
                                        <FileText className="w-12 h-12 text-slate-300 mx-auto mb-3" />
                                        <p className="text-slate-500 font-medium">Aucun document uploadé</p>
                                        <p className="text-slate-400 text-sm">L'utilisateur n'a pas encore soumis de documents</p>
                                    </div>
                                ) : (
                                    user.documents.map((doc) => (
                                        <DocumentRow
                                            key={doc.id}
                                            doc={doc}
                                            isLoading={actionLoading === doc.id}
                                            onApprove={() => handleDocumentAction(doc.id, 'APPROVED')}
                                            onReject={() => {
                                                const reason = prompt('Raison du rejet :');
                                                if (reason) handleDocumentAction(doc.id, 'REJECTED', reason);
                                            }}
                                        />
                                    ))
                                )}
                            </div>
                        </div>
                    </div>

                    {/* ========================================= */}
                    {/* COLONNE DROITE (1/3) */}
                    {/* ========================================= */}
                    <div className="space-y-6">

                        {/* CARTE NOTES INTERNES */}
                        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden flex flex-col">
                            <div className="p-5 border-b border-slate-100 bg-gradient-to-r from-indigo-50 to-purple-50">
                                <h3 className="font-semibold text-slate-900 flex items-center gap-2">
                                    <MessageSquare className="w-5 h-5 text-indigo-500" />
                                    Notes Admin (Privé)
                                </h3>
                                <p className="text-xs text-slate-500 mt-1">Communication interne sur ce dossier</p>
                            </div>

                            {/* Messages list */}
                            <div className="flex-1 p-4 space-y-4 max-h-[350px] overflow-y-auto bg-slate-50">
                                {user.adminNotesReceived.length === 0 ? (
                                    <div className="text-center py-8">
                                        <MessageSquare className="w-10 h-10 text-slate-200 mx-auto mb-3" />
                                        <p className="text-slate-500 text-sm">Aucune note</p>
                                        <p className="text-slate-400 text-xs">Ajoutez une note pour cet utilisateur</p>
                                    </div>
                                ) : (
                                    <AnimatePresence>
                                        {user.adminNotesReceived.map((note) => {
                                            const adminName = note.admin.profile
                                                ? `${note.admin.profile.firstName || ''} ${note.admin.profile.lastName || ''}`
                                                : note.admin.email.split('@')[0];
                                            const adminInitials = note.admin.profile
                                                ? `${note.admin.profile.firstName?.charAt(0) || ''}${note.admin.profile.lastName?.charAt(0) || ''}`
                                                : note.admin.email.charAt(0).toUpperCase();

                                            return (
                                                <motion.div
                                                    key={note.id}
                                                    initial={{ opacity: 0, y: 10 }}
                                                    animate={{ opacity: 1, y: 0 }}
                                                    className="flex gap-3"
                                                >
                                                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center flex-shrink-0">
                                                        <span className="text-xs font-bold text-white">{adminInitials}</span>
                                                    </div>
                                                    <div className="flex-1 bg-white rounded-xl rounded-tl-none p-3 shadow-sm border border-slate-100">
                                                        <div className="flex items-center justify-between mb-1">
                                                            <span className="text-xs font-semibold text-indigo-600">{adminName}</span>
                                                            <span className="text-xs text-slate-400">{formatDate(note.createdAt)}</span>
                                                        </div>
                                                        <p className="text-sm text-slate-700">{note.content}</p>
                                                    </div>
                                                </motion.div>
                                            );
                                        })}
                                    </AnimatePresence>
                                )}
                            </div>

                            {/* Input */}
                            <div className="p-4 border-t border-slate-100 bg-white">
                                <div className="flex gap-2">
                                    <input
                                        type="text"
                                        value={newNote}
                                        onChange={(e) => setNewNote(e.target.value)}
                                        onKeyDown={(e) => e.key === 'Enter' && handleAddNote()}
                                        placeholder="Ajouter une note..."
                                        className="flex-1 px-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                                    />
                                    <button
                                        onClick={handleAddNote}
                                        disabled={!newNote.trim() || isSendingNote}
                                        className="px-4 py-2.5 rounded-xl bg-brand-600 text-white font-medium hover:bg-brand-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                                    >
                                        {isSendingNote ? (
                                            <Loader2 className="w-5 h-5 animate-spin" />
                                        ) : (
                                            <Send className="w-5 h-5" />
                                        )}
                                    </button>
                                </div>
                            </div>
                        </div>

                        {/* CARTE ACTIONS RAPIDES */}
                        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
                            <div className="p-5 border-b border-slate-100">
                                <h3 className="font-semibold text-slate-900">Actions rapides</h3>
                            </div>

                            <div className="p-4 space-y-3">
                                {/* Voir profil public */}
                                <Link
                                    href={`/profile/${user.id}`}
                                    target="_blank"
                                    className="flex items-center gap-3 w-full px-4 py-3 rounded-xl border border-slate-200 hover:bg-slate-50 hover:border-slate-300 transition-all group"
                                >
                                    <div className="w-10 h-10 rounded-lg bg-blue-100 text-blue-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                                        <ExternalLink className="w-5 h-5" />
                                    </div>
                                    <div className="flex-1 text-left">
                                        <p className="font-medium text-slate-900 text-sm">Voir le profil public</p>
                                        <p className="text-xs text-slate-500">Ouvrir dans un nouvel onglet</p>
                                    </div>
                                </Link>

                                {/* Réinitialiser mot de passe */}
                                <button
                                    onClick={handleResetPassword}
                                    disabled={actionLoading === 'password'}
                                    className="flex items-center gap-3 w-full px-4 py-3 rounded-xl border border-slate-200 hover:bg-slate-50 hover:border-slate-300 transition-all group disabled:opacity-50"
                                >
                                    <div className="w-10 h-10 rounded-lg bg-amber-100 text-amber-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                                        {actionLoading === 'password' ? (
                                            <Loader2 className="w-5 h-5 animate-spin" />
                                        ) : (
                                            <KeyRound className="w-5 h-5" />
                                        )}
                                    </div>
                                    <div className="flex-1 text-left">
                                        <p className="font-medium text-slate-900 text-sm">Réinitialiser mot de passe</p>
                                        <p className="text-xs text-slate-500">Envoie un email à l'utilisateur</p>
                                    </div>
                                </button>

                                {/* Suspendre le compte */}
                                <button
                                    onClick={handleSuspend}
                                    disabled={actionLoading === 'suspend' || user.status === 'SUSPENDED' || user.status === 'BANNED'}
                                    className="flex items-center gap-3 w-full px-4 py-3 rounded-xl border border-red-200 bg-red-50 hover:bg-red-100 hover:border-red-300 transition-all group disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    <div className="w-10 h-10 rounded-lg bg-red-100 text-red-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                                        {actionLoading === 'suspend' ? (
                                            <Loader2 className="w-5 h-5 animate-spin" />
                                        ) : (
                                            <Ban className="w-5 h-5" />
                                        )}
                                    </div>
                                    <div className="flex-1 text-left">
                                        <p className="font-medium text-red-700 text-sm">
                                            {user.status === 'SUSPENDED' ? 'Compte suspendu' : 'Suspendre le compte'}
                                        </p>
                                        <p className="text-xs text-red-500">
                                            {user.status === 'SUSPENDED' ? 'Déjà suspendu' : 'Bloque temporairement l\'accès'}
                                        </p>
                                    </div>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}

