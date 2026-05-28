'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import {
    Search,
    ChevronDown,
    ChevronLeft,
    ChevronRight,
    Users,
    Building2,
    UserCheck,
    Clock,
    AlertCircle,
    CheckCircle,
    Loader2,
    Settings,
    Filter,
} from 'lucide-react';
import Cookies from 'js-cookie';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000/api/v1';

// Types
interface UserProfile {
    firstName: string;
    lastName: string;
    avatarUrl?: string;
    city?: string;
}

interface Establishment {
    name: string;
    type?: string;
    city?: string;
}

interface UserData {
    id: string;
    email: string;
    role: 'CLIENT' | 'TALENT' | 'ADMIN';
    status: 'PENDING' | 'VERIFIED' | 'SUSPENDED' | 'BANNED';
    clientType?: 'PARTICULAR' | 'ESTABLISHMENT';
    isVerified: boolean;
    createdAt: string;
    profile?: UserProfile;
    establishment?: Establishment;
    _count: {
        bookingsAsClient: number;
        bookingsAsProvider: number;
        adminNotesReceived: number;
        documents: number;
    };
}

interface PaginatedResponse {
    data: UserData[];
    meta: {
        total: number;
        page: number;
        limit: number;
        totalPages: number;
    };
}

// Role badge component
function RoleBadge({ role, clientType }: { role: string; clientType?: string }) {
    const config = {
        ADMIN: { label: 'Admin', bg: 'bg-slate-100', text: 'text-slate-700', border: 'border-slate-200' },
        TALENT: { label: 'Talent', bg: 'bg-purple-50', text: 'text-purple-700', border: 'border-purple-200' },
        CLIENT: clientType === 'ESTABLISHMENT'
            ? { label: 'Établissement', bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200' }
            : { label: 'Particulier', bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200' },
    };

    const { label, bg, text, border } = config[role as keyof typeof config] || config.CLIENT;

    return (
        <span className={`inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-semibold border ${bg} ${text} ${border}`}>
            {label}
        </span>
    );
}

// Status badge component
function StatusBadge({ status, isVerified }: { status: string; isVerified: boolean }) {
    if (status === 'BANNED') {
        return (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold bg-red-50 text-red-700 border border-red-200">
                <AlertCircle className="h-3 w-3" />
                Banni
            </span>
        );
    }
    if (status === 'SUSPENDED') {
        return (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold bg-orange-50 text-orange-700 border border-orange-200">
                <AlertCircle className="h-3 w-3" />
                Suspendu
            </span>
        );
    }
    if (isVerified || status === 'VERIFIED') {
        return (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold bg-green-50 text-green-700 border border-green-200">
                <CheckCircle className="h-3 w-3" />
                Vérifié
            </span>
        );
    }
    return (
        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold bg-amber-50 text-amber-700 border border-amber-200">
            <Clock className="h-3 w-3" />
            En attente
        </span>
    );
}

// Document status indicator
function DocStatusIndicator({ count }: { count: number }) {
    if (count === 0) {
        return (
            <span className="inline-flex items-center gap-1 text-slate-400 text-sm">
                <AlertCircle className="h-4 w-4" />
                Aucun
            </span>
        );
    }
    return (
        <span className="inline-flex items-center gap-1 text-green-600 text-sm">
            <CheckCircle className="h-4 w-4" />
            {count} doc{count > 1 ? 's' : ''}
        </span>
    );
}

// Format date
function formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
    });
}

// Get user display name
function getUserDisplayName(user: UserData): string {
    if (user.profile?.firstName && user.profile?.lastName) {
        return `${user.profile.firstName} ${user.profile.lastName}`;
    }
    if (user.establishment?.name) {
        return user.establishment.name;
    }
    return user.email.split('@')[0];
}

// Get user initials
function getUserInitials(user: UserData): string {
    if (user.profile?.firstName && user.profile?.lastName) {
        return `${user.profile.firstName[0]}${user.profile.lastName[0]}`.toUpperCase();
    }
    if (user.establishment?.name) {
        return user.establishment.name.substring(0, 2).toUpperCase();
    }
    return user.email.substring(0, 2).toUpperCase();
}

export default function AdminUsersPage() {
    const router = useRouter();
    const searchParams = useSearchParams();

    // State
    const [users, setUsers] = useState<UserData[]>([]);
    const [meta, setMeta] = useState({ total: 0, page: 1, limit: 20, totalPages: 1 });
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Filters from URL
    const [search, setSearch] = useState(searchParams.get('search') || '');
    const [roleFilter, setRoleFilter] = useState(searchParams.get('role') || '');
    const [statusFilter, setStatusFilter] = useState(searchParams.get('status') || '');
    const [page, setPage] = useState(parseInt(searchParams.get('page') || '1', 10));

    // Fetch users
    const fetchUsers = useCallback(async () => {
        setIsLoading(true);
        setError(null);

        try {
            const token = Cookies.get('accessToken');
            if (!token) {
                router.push('/auth/login');
                return;
            }

            const params = new URLSearchParams();
            if (search) params.set('search', search);
            if (roleFilter) params.set('role', roleFilter);
            if (statusFilter) params.set('status', statusFilter);
            params.set('page', page.toString());
            params.set('limit', '20');

            const response = await fetch(`${API_URL}/admin/users?${params.toString()}`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                if (response.status === 401 || response.status === 403) {
                    router.push('/auth/login');
                    return;
                }
                throw new Error('Erreur lors du chargement des utilisateurs');
            }

            const data: PaginatedResponse = await response.json();
            setUsers(data.data);
            setMeta(data.meta);
        } catch (err: any) {
            setError(err.message || 'Erreur inconnue');
        } finally {
            setIsLoading(false);
        }
    }, [search, roleFilter, statusFilter, page, router]);

    // Update URL when filters change
    useEffect(() => {
        const params = new URLSearchParams();
        if (search) params.set('search', search);
        if (roleFilter) params.set('role', roleFilter);
        if (statusFilter) params.set('status', statusFilter);
        if (page > 1) params.set('page', page.toString());

        const newUrl = params.toString() ? `?${params.toString()}` : '';
        router.replace(`/admin/users${newUrl}`, { scroll: false });
    }, [search, roleFilter, statusFilter, page, router]);

    // Fetch on mount and filter change
    useEffect(() => {
        const debounce = setTimeout(() => {
            fetchUsers();
        }, 300);

        return () => clearTimeout(debounce);
    }, [fetchUsers]);

    // Handle search with debounce
    const handleSearchChange = (value: string) => {
        setSearch(value);
        setPage(1);
    };

    return (
        <div className="min-h-screen bg-slate-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-2xl font-bold text-slate-900">Annuaire Utilisateurs</h1>
                    <p className="text-slate-500 mt-1">
                        Gérez et consultez tous les utilisateurs de la plateforme
                    </p>
                </div>

                {/* Stats Cards */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <div className="bg-white rounded-xl border border-slate-200 p-4">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-blue-50 rounded-lg">
                                <Users className="h-5 w-5 text-blue-600" />
                            </div>
                            <div>
                                <p className="text-2xl font-bold text-slate-900">{meta.total}</p>
                                <p className="text-xs text-slate-500">Total utilisateurs</p>
                            </div>
                        </div>
                    </div>
                    <div className="bg-white rounded-xl border border-slate-200 p-4">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-purple-50 rounded-lg">
                                <UserCheck className="h-5 w-5 text-purple-600" />
                            </div>
                            <div>
                                <p className="text-2xl font-bold text-slate-900">—</p>
                                <p className="text-xs text-slate-500">Talents</p>
                            </div>
                        </div>
                    </div>
                    <div className="bg-white rounded-xl border border-slate-200 p-4">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-emerald-50 rounded-lg">
                                <Building2 className="h-5 w-5 text-emerald-600" />
                            </div>
                            <div>
                                <p className="text-2xl font-bold text-slate-900">—</p>
                                <p className="text-xs text-slate-500">Établissements</p>
                            </div>
                        </div>
                    </div>
                    <div className="bg-white rounded-xl border border-slate-200 p-4">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-amber-50 rounded-lg">
                                <Clock className="h-5 w-5 text-amber-600" />
                            </div>
                            <div>
                                <p className="text-2xl font-bold text-slate-900">—</p>
                                <p className="text-xs text-slate-500">En attente</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Filters Bar */}
                <div className="bg-white rounded-xl border border-slate-200 p-4 mb-6">
                    <div className="flex flex-col md:flex-row gap-4">
                        {/* Search */}
                        <div className="flex-1 relative">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                            <input
                                type="text"
                                placeholder="Rechercher par nom ou email..."
                                value={search}
                                onChange={(e) => handleSearchChange(e.target.value)}
                                className="w-full pl-10 pr-4 py-2.5 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all text-sm"
                            />
                        </div>

                        {/* Role Filter */}
                        <div className="relative">
                            <select
                                value={roleFilter}
                                onChange={(e) => { setRoleFilter(e.target.value); setPage(1); }}
                                className="appearance-none pl-4 pr-10 py-2.5 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all text-sm min-w-[160px]"
                            >
                                <option value="">Tous les rôles</option>
                                <option value="TALENT">Talents</option>
                                <option value="CLIENT">Clients</option>
                                <option value="ADMIN">Admins</option>
                            </select>
                            <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400 pointer-events-none" />
                        </div>

                        {/* Status Filter */}
                        <div className="relative">
                            <select
                                value={statusFilter}
                                onChange={(e) => { setStatusFilter(e.target.value); setPage(1); }}
                                className="appearance-none pl-4 pr-10 py-2.5 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all text-sm min-w-[160px]"
                            >
                                <option value="">Tous les statuts</option>
                                <option value="PENDING">En attente</option>
                                <option value="VERIFIED">Vérifiés</option>
                                <option value="SUSPENDED">Suspendus</option>
                                <option value="BANNED">Bannis</option>
                            </select>
                            <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400 pointer-events-none" />
                        </div>

                        {/* Filter indicator */}
                        {(search || roleFilter || statusFilter) && (
                            <button
                                onClick={() => { setSearch(''); setRoleFilter(''); setStatusFilter(''); setPage(1); }}
                                className="px-4 py-2.5 text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors"
                            >
                                Réinitialiser
                            </button>
                        )}
                    </div>
                </div>

                {/* Data Table */}
                <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
                    {isLoading ? (
                        <div className="flex items-center justify-center py-20">
                            <Loader2 className="h-8 w-8 text-blue-500 animate-spin" />
                        </div>
                    ) : error ? (
                        <div className="flex flex-col items-center justify-center py-20">
                            <AlertCircle className="h-12 w-12 text-red-400 mb-4" />
                            <p className="text-slate-600">{error}</p>
                            <button
                                onClick={fetchUsers}
                                className="mt-4 px-4 py-2 bg-brand-600 text-white rounded-xl hover:bg-brand-700 shadow-sm hover:shadow-md active:scale-95 transition-all"
                            >
                                Réessayer
                            </button>
                        </div>
                    ) : users.length === 0 ? (
                        <div className="flex flex-col items-center justify-center py-20">
                            <Users className="h-12 w-12 text-slate-300 mb-4" />
                            <p className="text-slate-500">Aucun utilisateur trouvé</p>
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead className="bg-slate-50 border-b border-slate-200">
                                    <tr>
                                        <th className="px-6 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                                            Utilisateur
                                        </th>
                                        <th className="px-6 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                                            Rôle
                                        </th>
                                        <th className="px-6 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                                            Statut
                                        </th>
                                        <th className="px-6 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                                            Documents
                                        </th>
                                        <th className="px-6 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                                            Inscription
                                        </th>
                                        <th className="px-6 py-4 text-right text-xs font-semibold text-slate-600 uppercase tracking-wider">
                                            Actions
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-100">
                                    {users.map((user, index) => (
                                        <motion.tr
                                            key={user.id}
                                            initial={{ opacity: 0, y: 10 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            transition={{ delay: index * 0.03 }}
                                            className="hover:bg-slate-50/50 transition-colors"
                                        >
                                            {/* User */}
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-3">
                                                    {user.profile?.avatarUrl ? (
                                                        <img
                                                            src={user.profile.avatarUrl}
                                                            alt=""
                                                            className="h-10 w-10 rounded-full object-cover"
                                                        />
                                                    ) : (
                                                        <div className="h-10 w-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
                                                            <span className="text-white text-sm font-semibold">
                                                                {getUserInitials(user)}
                                                            </span>
                                                        </div>
                                                    )}
                                                    <div>
                                                        <p className="font-semibold text-slate-900">
                                                            {getUserDisplayName(user)}
                                                        </p>
                                                        <p className="text-sm text-slate-500">{user.email}</p>
                                                    </div>
                                                </div>
                                            </td>

                                            {/* Role */}
                                            <td className="px-6 py-4">
                                                <RoleBadge role={user.role} clientType={user.clientType} />
                                            </td>

                                            {/* Status */}
                                            <td className="px-6 py-4">
                                                <StatusBadge status={user.status} isVerified={user.isVerified} />
                                            </td>

                                            {/* Documents */}
                                            <td className="px-6 py-4">
                                                <DocStatusIndicator count={user._count.documents} />
                                            </td>

                                            {/* Date */}
                                            <td className="px-6 py-4">
                                                <span className="text-sm text-slate-600">
                                                    {formatDate(user.createdAt)}
                                                </span>
                                            </td>

                                            {/* Actions */}
                                            <td className="px-6 py-4 text-right">
                                                <Link
                                                    href={`/admin/users/${user.id}`}
                                                    className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-sm font-medium transition-colors"
                                                >
                                                    <Settings className="h-4 w-4" />
                                                    Gérer
                                                </Link>
                                            </td>
                                        </motion.tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}

                    {/* Pagination */}
                    {!isLoading && !error && users.length > 0 && (
                        <div className="flex items-center justify-between px-6 py-4 border-t border-slate-200 bg-slate-50">
                            <p className="text-sm text-slate-600">
                                Page {meta.page} sur {meta.totalPages} • {meta.total} utilisateur{meta.total > 1 ? 's' : ''}
                            </p>
                            <div className="flex items-center gap-2">
                                <button
                                    onClick={() => setPage(Math.max(1, page - 1))}
                                    disabled={page === 1}
                                    className="inline-flex items-center gap-1 px-3 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                                >
                                    <ChevronLeft className="h-4 w-4" />
                                    Précédent
                                </button>
                                <button
                                    onClick={() => setPage(Math.min(meta.totalPages, page + 1))}
                                    disabled={page >= meta.totalPages}
                                    className="inline-flex items-center gap-1 px-3 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                                >
                                    Suivant
                                    <ChevronRight className="h-4 w-4" />
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
