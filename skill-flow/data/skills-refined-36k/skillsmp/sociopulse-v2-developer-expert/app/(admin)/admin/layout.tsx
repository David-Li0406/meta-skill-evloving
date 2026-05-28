'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import type { MouseEvent, ReactNode } from 'react';
import {
    LayoutDashboard,
    Users,
    ShieldCheck,
    ShieldAlert,
    FileText,
    Briefcase,
    BarChart3,
    ArrowLeft,
} from 'lucide-react';

type NavItem = {
    href: string;
    label: string;
    icon: typeof LayoutDashboard;
    available: boolean;
};

const NAV_ITEMS: NavItem[] = [
    { href: '/admin', label: "Vue d'ensemble", icon: LayoutDashboard, available: true },
    { href: '/admin/users', label: 'Utilisateurs', icon: Users, available: true },
    { href: '/admin/profiles', label: 'Profils', icon: ShieldCheck, available: true },
    { href: '/admin/missions', label: 'Missions', icon: Briefcase, available: true },
    { href: '/admin/contracts', label: 'Contrats', icon: FileText, available: true },
    { href: '/admin/moderation', label: 'Modération', icon: ShieldAlert, available: true },
    { href: '/admin/stats', label: 'Statistiques', icon: BarChart3, available: false },
];

export default function AdminLayout({ children }: { children: ReactNode }) {
    const pathname = usePathname();

    const handleUnavailable = (event: MouseEvent<HTMLButtonElement>) => {
        event.preventDefault();
        alert('Bientôt');
    };

    return (
        <div className="min-h-screen bg-slate-900 text-slate-100">
            <div className="flex min-h-screen">
                <aside className="hidden lg:flex w-72 flex-col gap-8 bg-slate-950 border-r border-slate-800 px-5 py-6">
                    <Link href="/admin" className="flex items-center gap-3">
                        <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-indigo-600 to-teal-500 flex items-center justify-center text-white font-semibold shadow-soft">
                            LX
                        </div>
                        <div className="leading-tight">
                            <p className="text-sm font-semibold text-white">Admin Desk</p>
                            <p className="text-xs text-white/60">Contrôles & modération</p>
                        </div>
                    </Link>

                    <nav className="space-y-1">
                        {NAV_ITEMS.map((item) => {
                            const Icon = item.icon;
                            const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
                            const baseClasses =
                                'flex w-full items-center gap-2 px-3 py-2.5 rounded-xl text-sm font-semibold transition-colors';

                            if (!item.available) {
                                return (
                                    <button
                                        key={item.href}
                                        type="button"
                                        onClick={handleUnavailable}
                                        className={`${baseClasses} text-slate-500 hover:text-slate-200 hover:bg-slate-900`}
                                        aria-disabled="true"
                                    >
                                        <Icon className="h-4 w-4" />
                                        {item.label}
                                    </button>
                                );
                            }

                            return (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    className={`${baseClasses} ${
                                        isActive
                                            ? 'bg-slate-800 text-white shadow-soft'
                                            : 'text-slate-200 hover:bg-slate-900'
                                    }`}
                                >
                                    <Icon className="h-4 w-4" />
                                    {item.label}
                                </Link>
                            );
                        })}
                    </nav>

                    <Link
                        href="/"
                        className="inline-flex items-center gap-2 px-3 py-2 rounded-xl border border-slate-800 text-sm font-semibold text-white/80 hover:bg-slate-900 hover:text-white transition-colors"
                    >
                        <LayoutDashboard className="h-4 w-4" />
                        Retour plateforme
                    </Link>
                </aside>

                <div className="flex-1 bg-slate-50">
                    <header className="lg:hidden sticky top-0 z-40 bg-slate-900 text-white border-b border-slate-800 px-4 py-4 flex items-center justify-between">
                        <Link href="/" className="inline-flex items-center gap-2 text-sm font-semibold text-white">
                            <ArrowLeft className="h-4 w-4" />
                            Plateforme
                        </Link>
                        <span className="text-xs text-white/60">Admin Desk</span>
                    </header>
                    <main className="min-h-screen">{children}</main>
                </div>
            </div>
        </div>
    );
}
