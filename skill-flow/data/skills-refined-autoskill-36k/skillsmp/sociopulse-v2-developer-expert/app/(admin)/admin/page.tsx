'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import Cookies from 'js-cookie';
import {
    Users,
    UserCheck,
    FileCheck,
    Clock,
    TrendingUp,
    AlertTriangle,
    Euro,
    Briefcase,
    Shield,
    ChevronRight,
    Bell,
    FileText,
    Calendar,
    Activity,
    ArrowUpRight,
    Loader2,
    Zap,
} from 'lucide-react';

// ===========================================
// TYPES
// ===========================================

interface DashboardStats {
    users: {
        total: number;
        talents: number;
        clients: number;
        pendingVerification: number;
        newThisWeek: number;
    };
    documents: {
        pending: number;
        approvedThisWeek: number;
        rejectedThisWeek: number;
    };
    missions: {
        active: number;
        completedThisMonth: number;
        inDispute: number;
    };
    finance: {
        revenueThisMonth: number;
        commissionsThisMonth: number;
        pendingPayouts: number;
    };
}

interface RecentActivity {
    id: string;
    type: 'USER_REGISTERED' | 'DOCUMENT_UPLOADED' | 'MISSION_CREATED' | 'CONTRACT_SIGNED' | 'MISSION_COMPLETED';
    message: string;
    timestamp: string;
    userId?: string;
    userName?: string;
}

// ===========================================
// HELPERS
// ===========================================

const getApiBase = () => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';
    const normalized = apiBase.replace(/\/+$/, '');
    return normalized.endsWith('/api/v1') ? normalized : `${normalized}/api/v1`;
};

const formatCurrency = (cents: number) => {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR',
    }).format(cents / 100);
};

const formatRelativeTime = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 60) return `Il y a ${diffMins} min`;
    if (diffHours < 24) return `Il y a ${diffHours}h`;
    return `Il y a ${diffDays}j`;
};

// ===========================================
// STAT CARD COMPONENT
// ===========================================

function StatCard({
    title,
    value,
    subtitle,
    icon: Icon,
    trend,
    trendLabel,
    color,
    href,
}: {
    title: string;
    value: string | number;
    subtitle?: string;
    icon: React.ElementType;
    trend?: number;
    trendLabel?: string;
    color: 'coral' | 'indigo' | 'green' | 'amber' | 'purple';
    href?: string;
}) {
    const colorMap = {
        coral: 'from-rose-500 to-rose-600',
        indigo: 'from-indigo-500 to-purple-500',
        green: 'from-green-500 to-emerald-400',
        amber: 'from-amber-500 to-yellow-400',
        purple: 'from-purple-500 to-pink-500',
    };

    const content = (
        <motion.div
            whileHover={{ scale: 1.02 }}
            className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition-all cursor-pointer"
        >
            <div className="flex items-start justify-between">
                <div className="flex-1">
                    <p className="text-sm font-medium text-slate-500">{title}</p>
                    <p className="text-3xl font-bold text-slate-900 mt-1">{value}</p>
                    {subtitle && <p className="text-xs text-slate-400 mt-1">{subtitle}</p>}
                    {trend !== undefined && (
                        <div className={`flex items-center gap-1 mt-2 text-xs font-medium ${trend >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                            <TrendingUp className={`w-3 h-3 ${trend < 0 ? 'rotate-180' : ''}`} />
                            <span>{trend >= 0 ? '+' : ''}{trend}%</span>
                            {trendLabel && <span className="text-slate-400 font-normal">{trendLabel}</span>}
                        </div>
                    )}
                </div>
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${colorMap[color]} flex items-center justify-center shadow-lg`}>
                    <Icon className="w-6 h-6 text-white" />
                </div>
            </div>
        </motion.div>
    );

    return href ? <Link href={href}>{content}</Link> : content;
}

// ===========================================
// ALERT CARD COMPONENT
// ===========================================

function AlertCard({
    title,
    count,
    icon: Icon,
    href,
    variant,
}: {
    title: string;
    count: number;
    icon: React.ElementType;
    href: string;
    variant: 'warning' | 'danger' | 'info';
}) {
    const variantMap = {
        warning: 'bg-amber-50 border-amber-200 text-amber-700',
        danger: 'bg-red-50 border-red-200 text-red-700',
        info: 'bg-blue-50 border-blue-200 text-blue-700',
    };

    if (count === 0) return null;

    return (
        <Link href={href}>
            <motion.div
                whileHover={{ scale: 1.02 }}
                className={`flex items-center gap-3 p-4 rounded-xl border ${variantMap[variant]} cursor-pointer`}
            >
                <Icon className="w-5 h-5" />
                <div className="flex-1">
                    <span className="font-bold">{count}</span>
                    <span className="ml-1">{title}</span>
                </div>
                <ChevronRight className="w-4 h-4 opacity-50" />
            </motion.div>
        </Link>
    );
}

// ===========================================
// ACTIVITY ICON
// ===========================================

function ActivityIcon({ type }: { type: RecentActivity['type'] }) {
    const config = {
        USER_REGISTERED: { icon: Users, bg: 'bg-indigo-100', color: 'text-indigo-600' },
        DOCUMENT_UPLOADED: { icon: FileText, bg: 'bg-amber-100', color: 'text-amber-600' },
        MISSION_CREATED: { icon: Briefcase, bg: 'bg-rose-100', color: 'text-rose-600' },
        CONTRACT_SIGNED: { icon: FileCheck, bg: 'bg-green-100', color: 'text-green-600' },
        MISSION_COMPLETED: { icon: Calendar, bg: 'bg-purple-100', color: 'text-purple-600' },
    };

    const c = config[type] || config.USER_REGISTERED;
    const Icon = c.icon;

    return (
        <div className={`w-10 h-10 rounded-full ${c.bg} flex items-center justify-center`}>
            <Icon className={`w-5 h-5 ${c.color}`} />
        </div>
    );
}

// ===========================================
// QUICK ACTION BUTTON
// ===========================================

function QuickAction({ label, href, icon: Icon, highlight }: { label: string; href: string; icon: React.ElementType; highlight?: boolean }) {
    return (
        <Link href={href}>
            <motion.div
                whileHover={{ scale: 1.02 }}
                className={`flex items-center gap-3 p-4 rounded-xl border transition-all ${
                    highlight 
                        ? 'bg-gradient-to-r from-indigo-50 to-purple-50 border-indigo-200 hover:border-indigo-300 shadow-sm' 
                        : 'bg-white border-slate-100 hover:border-slate-200 hover:shadow-sm'
                }`}
            >
                <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                    highlight ? 'bg-indigo-100' : 'bg-slate-100'
                }`}>
                    <Icon className={`w-5 h-5 ${highlight ? 'text-indigo-600' : 'text-slate-600'}`} />
                </div>
                <span className={`flex-1 font-medium ${highlight ? 'text-indigo-700' : 'text-slate-700'}`}>{label}</span>
                <ArrowUpRight className="w-4 h-4 text-slate-400" />
            </motion.div>
        </Link>
    );
}

// ===========================================
// MAIN COMPONENT
// ===========================================

export default function AdminDashboardPage() {
    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [activities, setActivities] = useState<RecentActivity[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchDashboard = async () => {
            try {
                const token = Cookies.get('accessToken');
                const headers: Record<string, string> = { 'Content-Type': 'application/json' };
                if (token) {
                    headers['Authorization'] = `Bearer ${token}`;
                }

                const statsRes = await fetch(`${getApiBase()}/admin/dashboard/stats`, { headers });
                if (statsRes.ok) {
                    setStats(await statsRes.json());
                }

                const activityRes = await fetch(`${getApiBase()}/admin/dashboard/activity`, { headers });
                if (activityRes.ok) {
                    setActivities(await activityRes.json());
                }
            } catch (err) {
                console.error('Erreur dashboard:', err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchDashboard();
    }, []);

    // Mock data for demo (remplacé par l'API quand disponible)
    const mockStats: DashboardStats = stats || {
        users: { total: 247, talents: 89, clients: 156, pendingVerification: 12, newThisWeek: 23 },
        documents: { pending: 8, approvedThisWeek: 34, rejectedThisWeek: 3 },
        missions: { active: 15, completedThisMonth: 47, inDispute: 2 },
        finance: { revenueThisMonth: 1245000, commissionsThisMonth: 124500, pendingPayouts: 89000 },
    };

    const mockActivities: RecentActivity[] = activities.length > 0 ? activities : [
        { id: '1', type: 'USER_REGISTERED', message: 'Nouveau Talent inscrit : Marie Dupont', timestamp: new Date(Date.now() - 300000).toISOString() },
        { id: '2', type: 'DOCUMENT_UPLOADED', message: 'Document uploadé par Jean-Pierre Martin', timestamp: new Date(Date.now() - 1800000).toISOString() },
        { id: '3', type: 'MISSION_CREATED', message: 'Nouvelle mission SOS créée à Lyon', timestamp: new Date(Date.now() - 3600000).toISOString() },
        { id: '4', type: 'CONTRACT_SIGNED', message: 'Contrat signé : Mission #CTR-2024-089', timestamp: new Date(Date.now() - 7200000).toISOString() },
        { id: '5', type: 'MISSION_COMPLETED', message: 'Mission terminée : Atelier EHPAD Marseille', timestamp: new Date(Date.now() - 10800000).toISOString() },
    ];

    return (
        <div className="min-h-screen bg-slate-100">
            {/* Header */}
            <header className="bg-white border-b border-slate-200 sticky top-0 z-40">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                                <Shield className="w-5 h-5 text-white" />
                            </div>
                            <div>
                                <h1 className="font-bold text-slate-900">Desk Admin</h1>
                                <p className="text-xs text-slate-500">Les Extras V2</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-4">
                            <Link href="/admin/moderation" className="relative p-2 rounded-xl hover:bg-slate-100 transition-colors">
                                <Bell className="w-5 h-5 text-slate-600" />
                                {mockStats.documents.pending > 0 && (
                                    <span className="absolute -top-1 -right-1 w-5 h-5 bg-rose-500 text-white text-xs rounded-full flex items-center justify-center font-bold">
                                        {mockStats.documents.pending}
                                    </span>
                                )}
                            </Link>
                        </div>
                    </div>
                </div>
            </header>

            {/* Navigation Tabs */}
            <nav className="bg-white border-b border-slate-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex gap-1 overflow-x-auto py-2">
                        {[
                            { label: 'Dashboard', href: '/admin', active: true },
                            { label: 'Utilisateurs', href: '/admin/users' },
                            { label: 'Modération', href: '/admin/moderation', badge: mockStats.documents.pending },
                            { label: 'Missions', href: '/admin/missions' },
                            { label: 'Contrats', href: '/admin/contracts' },
                        ].map((tab) => (
                            <Link
                                key={tab.href}
                                href={tab.href}
                                className={`relative px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-colors ${
                                    tab.active
                                        ? 'bg-indigo-100 text-indigo-700'
                                        : 'text-slate-600 hover:bg-slate-100'
                                }`}
                            >
                                {tab.label}
                                {tab.badge && tab.badge > 0 && (
                                    <span className="ml-2 px-1.5 py-0.5 bg-rose-500 text-white text-xs rounded-full">
                                        {tab.badge}
                                    </span>
                                )}
                            </Link>
                        ))}
                    </div>
                </div>
            </nav>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Alertes urgentes */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                    <AlertCard
                        title="documents en attente"
                        count={mockStats.documents.pending}
                        icon={FileCheck}
                        href="/admin/moderation"
                        variant="warning"
                    />
                    <AlertCard
                        title="profils à vérifier"
                        count={mockStats.users.pendingVerification}
                        icon={UserCheck}
                        href="/admin/users?status=PENDING"
                        variant="warning"
                    />
                    <AlertCard
                        title="litiges en cours"
                        count={mockStats.missions.inDispute}
                        icon={AlertTriangle}
                        href="/admin/contracts?status=DISPUTED"
                        variant="danger"
                    />
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <StatCard
                        title="Utilisateurs"
                        value={mockStats.users.total}
                        subtitle={`${mockStats.users.talents} Talents • ${mockStats.users.clients} Clients`}
                        icon={Users}
                        trend={12}
                        trendLabel="vs mois dernier"
                        color="indigo"
                        href="/admin/users"
                    />
                    <StatCard
                        title="Missions actives"
                        value={mockStats.missions.active}
                        subtitle={`${mockStats.missions.completedThisMonth} terminées ce mois`}
                        icon={Briefcase}
                        color="coral"
                        href="/admin/missions"
                    />
                    <StatCard
                        title="Revenus du mois"
                        value={formatCurrency(mockStats.finance.revenueThisMonth)}
                        subtitle={`Commission: ${formatCurrency(mockStats.finance.commissionsThisMonth)}`}
                        icon={Euro}
                        trend={8}
                        trendLabel="vs mois dernier"
                        color="green"
                    />
                    <StatCard
                        title="Nouveaux inscrits"
                        value={mockStats.users.newThisWeek}
                        subtitle="Cette semaine"
                        icon={TrendingUp}
                        color="purple"
                    />
                </div>

                {/* Two Columns Layout - Actions en premier */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Actions rapides - EN PREMIER */}
                    <div className="lg:col-span-1 lg:order-first order-last space-y-4">
                        <h2 className="font-semibold text-slate-900 px-1 flex items-center gap-2">
                            <Zap className="w-5 h-5 text-amber-500" />
                            Actions rapides
                        </h2>
                        <QuickAction label="Valider les documents" href="/admin/moderation" icon={FileCheck} highlight />
                        <QuickAction label="Gérer les utilisateurs" href="/admin/users" icon={Users} />
                        <QuickAction label="Voir les missions SOS" href="/admin/missions" icon={Briefcase} />
                        <QuickAction label="Consulter les contrats" href="/admin/contracts" icon={FileText} />
                        <QuickAction label="Calendrier des missions" href="/admin/calendar" icon={Calendar} />
                    </div>

                    {/* Activité récente */}
                    <div className="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
                        <div className="p-6 border-b border-slate-100 flex items-center justify-between">
                            <h2 className="font-semibold text-slate-900 flex items-center gap-2">
                                <Activity className="w-5 h-5 text-slate-400" />
                                Activité récente
                            </h2>
                            <span className="text-xs text-slate-400">Temps réel</span>
                        </div>
                        <div className="divide-y divide-slate-50">
                            {mockActivities.map((activity) => (
                                <div key={activity.id} className="p-4 flex items-center gap-4 hover:bg-slate-50 transition-colors">
                                    <ActivityIcon type={activity.type} />
                                    <div className="flex-1 min-w-0">
                                        <p className="text-sm text-slate-700 truncate">{activity.message}</p>
                                        <p className="text-xs text-slate-400">{formatRelativeTime(activity.timestamp)}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                        <div className="p-4 border-t border-slate-100 text-center">
                            <Link href="/admin/activity" className="text-sm text-indigo-600 font-medium hover:underline">
                                Voir tout l'historique
                            </Link>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
