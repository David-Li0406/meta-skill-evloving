'use client';

import { useState, useCallback, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/lib/useAuth';
import { Siren, Calendar, User, Search, ArrowRight } from 'lucide-react';
import { GrowthDashboardWidgets } from '@/components/growth';
import { currentBrand, isMedical } from '@/lib/brand';
import { Card } from '@/components/ui';
// =============================================================================
// DASHBOARD HUB PAGE
// =============================================================================

export default function DashboardHubPage() {
    // Polymorphic colors based on brand
    const primaryGradient = isMedical()
        ? 'from-alert-500 to-alert-600'
        : 'from-rose-500 to-rose-600';
    const primaryShadow = isMedical()
        ? 'shadow-alert-500/30'
        : 'shadow-rose-500/30';
    const primaryText = isMedical() ? 'text-alert-600' : 'text-rose-600';

    // Auth & Routing Logic
    const router = useRouter();
    const { user, isLoading } = useAuth();

    useEffect(() => {
        if (!isLoading && user) {
            if (user.role === 'CLIENT') {
                router.replace('/dashboard/client');
            }
            // Add other role redirects here if needed
        }
    }, [user, isLoading, router]);

    if (isLoading) {
        return (
            <div className="flex h-screen items-center justify-center bg-slate-50">
                <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-600 border-t-transparent"></div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-canvas relative">
            {/* Header */}
            <header className="bg-white border-b border-slate-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
                    <div>
                        <h1 className="text-2xl font-semibold text-slate-900 tracking-tight">Tableau de Bord</h1>
                        <p className="text-sm text-slate-500">Bienvenue sur votre espace {currentBrand.appName}</p>
                    </div>
                    <div className="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center text-primary-600 font-semibold">
                        {user?.profile?.firstName?.charAt(0) || user?.email?.charAt(0) || 'U'}
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 transition-all duration-300">
                <div className="mb-10">
                    <GrowthDashboardWidgets />
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

                    {/* SOS Renfort - Primary Card */}
                    <Link
                        href="/dashboard/relief"
                        className="group relative p-8 bg-white rounded-theme-xl border border-slate-100 shadow-soft hover:shadow-theme-md transition-all duration-300 md:col-span-2 lg:col-span-2 overflow-hidden"
                    >
                        <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:opacity-20 transition-opacity">
                            <Siren className={`w-48 h-48 ${primaryText}`} />
                        </div>
                        <div className="relative z-10">
                            <div className={`w-14 h-14 rounded-theme-lg bg-gradient-to-br ${primaryGradient} flex items-center justify-center shadow-lg ${primaryShadow} mb-6`}>
                                <Siren className="w-7 h-7 text-white" />
                            </div>
                            <div>
                                <h3 className="font-bold text-slate-900">Desk Admin</h3>
                                <p className="text-xs text-slate-500">{currentBrand.appName} V2</p>
                            </div>
                            <h2 className="text-2xl font-bold text-slate-900 mb-2">SOS Renfort</h2>
                            <p className="text-slate-500 max-w-md mb-8">
                                Publiez une mission urgente et trouvez un professionnel qualifié en moins de 30 minutes.
                            </p>
                            <span className={`inline-flex items-center gap-2 ${primaryText} font-medium group-hover:gap-3 transition-all`}>
                                Accéder au module
                                <ArrowRight className="w-4 h-4" />
                            </span>
                        </div>
                    </Link>

                    {/* Agenda - Secondary */}
                    <Card variant="default" className="group p-8 opacity-60">
                        <div className="w-12 h-12 rounded-theme-lg bg-slate-100 flex items-center justify-center mb-6 text-slate-400">
                            <Calendar className="w-6 h-6" />
                        </div>
                        <h3 className="text-xl font-semibold text-slate-900 mb-2">Agenda</h3>
                        <p className="text-sm text-slate-500 mb-6">
                            Gérez vos réservations d'ateliers et vos disponibilités.
                        </p>
                        <span className="inline-flex px-3 py-1 rounded-full bg-slate-100 text-slate-500 text-xs font-medium">
                            Bientôt disponible
                        </span>
                    </Card>

                    {/* Profil */}
                    <Link
                        href="/profile"
                        className="group p-8 bg-white rounded-theme-xl border border-slate-100 shadow-soft hover:shadow-theme-md hover:border-primary-100 transition-all duration-300"
                    >
                        <div className="w-12 h-12 rounded-theme-lg bg-primary-50 flex items-center justify-center mb-6 text-primary-600">
                            <User className="w-6 h-6" />
                        </div>
                        <h3 className="text-xl font-semibold text-slate-900 mb-2">Mon Profil</h3>
                        <p className="text-sm text-slate-500 mb-6">
                            Mettez à jour vos informations et vos préférences.
                        </p>
                    </Link>

                    {/* Recherche */}
                    <Link
                        href="/search"
                        className="group p-8 bg-white rounded-theme-xl border border-slate-100 shadow-soft hover:shadow-theme-md hover:border-primary-100 transition-all duration-300"
                    >
                        <div className="w-12 h-12 rounded-theme-lg bg-live-50 flex items-center justify-center mb-6 text-live-600">
                            <Search className="w-6 h-6" />
                        </div>
                        <h3 className="text-xl font-semibold text-slate-900 mb-2">Rechercher</h3>
                        <p className="text-sm text-slate-500 mb-6">
                            Trouvez des animateurs ou des services spécifiques.
                        </p>
                    </Link>

                </div>
            </main>
        </div>
    );
}
