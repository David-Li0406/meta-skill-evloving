'use client';

import { ReactNode } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import {
    User,
    Settings,
    Shield,
    CreditCard,
    ChevronLeft,
    Bell,
} from 'lucide-react';

// ===========================================
// NAVIGATION ITEMS
// ===========================================

const SETTINGS_TABS = [
    { href: '/settings/profile', label: 'Mon Profil', icon: User },
    { href: '/settings/preferences', label: 'Préférences', icon: Settings },
    { href: '/settings/security', label: 'Sécurité', icon: Shield },
    { href: '/settings/billing', label: 'Facturation', icon: CreditCard },
];

// ===========================================
// LAYOUT COMPONENT
// ===========================================

export default function SettingsLayout({ children }: { children: ReactNode }) {
    const pathname = usePathname();

    return (
        <div className="min-h-screen bg-slate-50">
            {/* Header */}
            <header className="sticky top-0 z-40 bg-white/80 backdrop-blur-xl border-b border-slate-100">
                <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        {/* Back Button + Title */}
                        <div className="flex items-center gap-3">
                            <Link
                                href="/dashboard"
                                className="p-2 rounded-xl hover:bg-slate-100 transition-colors"
                                aria-label="Retour au tableau de bord"
                            >
                                <ChevronLeft className="w-5 h-5 text-slate-600" />
                            </Link>
                            <h1 className="text-xl font-bold text-slate-900">
                                Paramètres
                            </h1>
                        </div>

                        {/* Notifications */}
                        <button
                            aria-label="Notifications"
                            className="relative p-2 rounded-xl hover:bg-slate-100 transition-colors"
                        >
                            <Bell className="w-5 h-5 text-slate-600" />
                            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-brand-600 rounded-full" />
                        </button>
                    </div>

                    {/* Mobile: Horizontal Tabs */}
                    <div className="lg:hidden -mx-4 px-4 pb-3">
                        <div className="flex gap-1 overflow-x-auto scrollbar-none">
                            {SETTINGS_TABS.map((tab) => {
                                const Icon = tab.icon;
                                const isActive = pathname === tab.href;

                                return (
                                    <Link
                                        key={tab.href}
                                        href={tab.href}
                                        className={`
                                            flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium
                                            whitespace-nowrap transition-colors flex-shrink-0
                                            ${isActive
                                                ? 'bg-brand-50 text-brand-600'
                                                : 'text-slate-600 hover:bg-slate-100'
                                            }
                                        `}
                                    >
                                        <Icon className="w-4 h-4" />
                                        {tab.label}
                                    </Link>
                                );
                            })}
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                <div className="flex gap-8">
                    {/* Desktop Sidebar */}
                    <aside className="hidden lg:block w-64 flex-shrink-0">
                        <nav className="card-surface p-2 sticky top-24">
                            <div className="space-y-1">
                                {SETTINGS_TABS.map((tab) => {
                                    const Icon = tab.icon;
                                    const isActive = pathname === tab.href;

                                    return (
                                        <Link
                                            key={tab.href}
                                            href={tab.href}
                                            className={`
                                                relative flex items-center gap-3 px-4 py-3 rounded-xl
                                                text-sm font-medium transition-all
                                                ${isActive
                                                    ? 'bg-brand-50 text-brand-600'
                                                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                                                }
                                            `}
                                        >
                                            {/* Active Indicator */}
                                            {isActive && (
                                                <motion.div
                                                    layoutId="activeTab"
                                                    className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-brand-600 rounded-r-full"
                                                    transition={{
                                                        type: 'spring',
                                                        stiffness: 300,
                                                        damping: 30,
                                                    }}
                                                />
                                            )}
                                            <Icon className={`w-5 h-5 ${isActive ? 'text-brand-600' : ''}`} />
                                            {tab.label}
                                        </Link>
                                    );
                                })}
                            </div>
                        </nav>
                    </aside>

                    {/* Page Content */}
                    <main className="flex-1 min-w-0">
                        {children}
                    </main>
                </div>
            </div>
        </div>
    );
}
