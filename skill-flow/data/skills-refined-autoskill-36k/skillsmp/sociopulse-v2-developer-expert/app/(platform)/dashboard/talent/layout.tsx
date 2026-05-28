'use client';

import { ReactNode, useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
    LayoutDashboard,
    Siren,
    Package,
    Calendar,
    FileText,
    UserCircle,
    ChevronLeft,
    ChevronRight,
    Bell,
    Settings,
    Moon,
    Sun,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { currentBrand, isMedical } from '@/lib/brand';
import { useTheme } from '@/components/providers/ThemeProvider';

// =============================================================================
// TYPES
// =============================================================================

interface NavItem {
    label: string;
    href: string;
    icon: React.ElementType;
    variant?: 'default' | 'alert' | 'creator';
    description?: string;
}

// =============================================================================
// NAVIGATION CONFIG
// =============================================================================

const navItems: NavItem[] = [
    {
        label: 'Cockpit',
        href: '/dashboard/talent',
        icon: LayoutDashboard,
        variant: 'default',
        description: 'Vue d\'ensemble',
    },
    {
        label: 'Missions SOS',
        href: '/dashboard/talent/missions',
        icon: Siren,
        variant: 'alert',
        description: 'Renforts urgents',
    },
    {
        label: 'Mes Services',
        href: '/dashboard/talent/services',
        icon: Package,
        variant: 'creator',
        description: 'Mon catalogue',
    },
    {
        label: 'Mon Planning',
        href: '/dashboard/talent/planning',
        icon: Calendar,
        variant: 'default',
        description: 'Disponibilités',
    },
    {
        label: 'Administratif',
        href: '/dashboard/talent/admin',
        icon: FileText,
        variant: 'default',
        description: 'Contrats & Factures',
    },
    {
        label: 'Mon Profil Public',
        href: '/dashboard/talent/profile',
        icon: UserCircle,
        variant: 'default',
        description: 'Bio & Médias',
    },
];

// =============================================================================
// SIDEBAR COMPONENT
// =============================================================================

function TalentSidebar({ collapsed, onToggle }: { collapsed: boolean; onToggle: () => void }) {
    const pathname = usePathname();
    const { isDark, toggleColorMode } = useTheme();

    const getVariantStyles = (variant: NavItem['variant'], isActive: boolean) => {
        if (isActive) {
            switch (variant) {
                case 'alert':
                    return 'bg-rose-100 dark:bg-rose-950/50 text-rose-700 dark:text-rose-300 border-rose-200 dark:border-rose-900';
                case 'creator':
                    return 'bg-teal-100 dark:bg-teal-950/50 text-teal-700 dark:text-teal-300 border-teal-200 dark:border-teal-900';
                default:
                    return 'bg-primary-100 dark:bg-primary-950/50 text-primary-700 dark:text-primary-300 border-primary-200 dark:border-primary-900';
            }
        }
        return 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 border-transparent';
    };

    const getIconVariantStyles = (variant: NavItem['variant'], isActive: boolean) => {
        if (isActive) {
            switch (variant) {
                case 'alert':
                    return 'text-rose-600';
                case 'creator':
                    return 'text-teal-600';
                default:
                    return 'text-primary-600';
            }
        }
        switch (variant) {
            case 'alert':
                return 'text-rose-500';
            case 'creator':
                return 'text-teal-500';
            default:
                return 'text-slate-500';
        }
    };

    return (
        <aside
            className={cn(
                'fixed left-0 top-0 z-40 h-screen transition-all duration-300 flex flex-col',
                'bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800',
                collapsed ? 'w-20' : 'w-64'
            )}
        >
            {/* Logo */}
            <div className="h-16 flex items-center justify-between px-4 border-b border-slate-100 dark:border-slate-800">
                {!collapsed && (
                    <Link href="/dashboard/talent" className="flex items-center gap-2">
                        <div className={cn(
                            'h-9 w-9 rounded-xl flex items-center justify-center text-white font-semibold text-sm',
                            isMedical() ? 'bg-gradient-to-br from-rose-500 to-rose-600' : 'bg-gradient-to-br from-teal-500 to-indigo-600'
                        )}>
                            {currentBrand.appName.substring(0, 2).toUpperCase()}
                        </div>
                        <span className="font-semibold text-slate-900 dark:text-white">Talent Hub</span>
                    </Link>
                )}
                <button
                    onClick={onToggle}
                    className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500 dark:text-slate-400 transition-colors"
                >
                    {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
                </button>
            </div>

            {/* Navigation */}
            <nav className="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
                {navItems.map((item) => {
                    const isActive = pathname === item.href || 
                        (item.href !== '/dashboard/talent' && pathname.startsWith(item.href));
                    const Icon = item.icon;

                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                'flex items-center gap-3 px-3 py-2.5 rounded-xl border transition-all duration-200',
                                getVariantStyles(item.variant, isActive),
                                collapsed && 'justify-center'
                            )}
                            title={collapsed ? item.label : undefined}
                        >
                            <Icon
                                size={20}
                                className={cn(
                                    'flex-shrink-0 transition-colors',
                                    getIconVariantStyles(item.variant, isActive)
                                )}
                            />
                            {!collapsed && (
                                <div className="flex flex-col min-w-0">
                                    <span className="font-medium text-sm truncate">{item.label}</span>
                                    {item.description && (
                                        <span className="text-xs text-slate-400 truncate">{item.description}</span>
                                    )}
                                </div>
                            )}
                        </Link>
                    );
                })}
            </nav>

            {/* Footer */}
            <div className="p-3 border-t border-slate-100 dark:border-slate-800 space-y-1">
                {/* Theme Toggle */}
                <button
                    onClick={toggleColorMode}
                    className={cn(
                        'flex w-full items-center gap-3 px-3 py-2.5 rounded-xl text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800 transition-colors',
                        collapsed && 'justify-center'
                    )}
                    title={isDark ? 'Mode clair' : 'Mode sombre'}
                >
                    {isDark ? (
                        <Sun size={20} className="text-amber-500" />
                    ) : (
                        <Moon size={20} />
                    )}
                    {!collapsed && (
                        <span className="text-sm font-medium">
                            {isDark ? 'Mode clair' : 'Mode sombre'}
                        </span>
                    )}
                </button>
                
                <Link
                    href="/settings"
                    className={cn(
                        'flex items-center gap-3 px-3 py-2.5 rounded-xl text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800 transition-colors',
                        collapsed && 'justify-center'
                    )}
                >
                    <Settings size={20} />
                    {!collapsed && <span className="text-sm font-medium">Paramètres</span>}
                </Link>
            </div>
        </aside>
    );
}

// =============================================================================
// HEADER COMPONENT
// =============================================================================

interface TalentHeaderProps {
    sosAvailable: boolean;
    onToggleSOS: () => void;
    sidebarCollapsed: boolean;
}

function TalentHeader({ sosAvailable, onToggleSOS, sidebarCollapsed }: TalentHeaderProps) {
    return (
        <header
            className={cn(
                'fixed top-0 right-0 z-30 h-16 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 transition-all duration-300',
                sidebarCollapsed ? 'left-20' : 'left-64'
            )}
        >
            <div className="h-full px-6 flex items-center justify-between">
                {/* Left: Page Title Area */}
                <div className="flex items-center gap-4">
                    <h1 className="text-lg font-semibold text-slate-900 dark:text-white">Tableau de Bord Talent</h1>
                </div>

                {/* Right: Actions */}
                <div className="flex items-center gap-4">
                    {/* SOS Availability Toggle */}
                    <div className="flex items-center gap-3 px-4 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                        <div className="flex items-center gap-2">
                            <Siren 
                                size={18} 
                                className={cn(
                                    'transition-colors',
                                    sosAvailable ? 'text-rose-500' : 'text-slate-400'
                                )}
                            />
                            <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                                Renfort Immédiat
                            </span>
                        </div>
                        <button
                            onClick={onToggleSOS}
                            className={cn(
                                'relative w-12 h-6 rounded-full transition-colors duration-300',
                                sosAvailable 
                                    ? 'bg-gradient-to-r from-rose-500 to-rose-600' 
                                    : 'bg-slate-300 dark:bg-slate-600'
                            )}
                            aria-label="Toggle SOS availability"
                        >
                            <span
                                className={cn(
                                    'absolute top-1 w-4 h-4 rounded-full bg-white shadow-md transition-all duration-300',
                                    sosAvailable ? 'left-7' : 'left-1'
                                )}
                            />
                        </button>
                        <span className={cn(
                            'text-xs font-semibold px-2 py-0.5 rounded-full',
                            sosAvailable 
                                ? 'bg-rose-100 text-rose-700' 
                                : 'bg-slate-200 text-slate-500'
                        )}>
                            {sosAvailable ? 'ON' : 'OFF'}
                        </span>
                    </div>

                    {/* Notifications */}
                    <button className="relative p-2 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-400 transition-colors">
                        <Bell size={20} />
                        <span className="absolute top-1 right-1 w-2 h-2 bg-rose-500 rounded-full" />
                    </button>
                </div>
            </div>
        </header>
    );
}

// =============================================================================
// LAYOUT
// =============================================================================

export default function TalentDashboardLayout({ children }: { children: ReactNode }) {
    const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
    const [sosAvailable, setSosAvailable] = useState(false);

    return (
        <div className="min-h-screen bg-canvas dark:bg-slate-950 transition-colors">
            <TalentSidebar 
                collapsed={sidebarCollapsed} 
                onToggle={() => setSidebarCollapsed(!sidebarCollapsed)} 
            />
            <TalentHeader 
                sosAvailable={sosAvailable}
                onToggleSOS={() => setSosAvailable(!sosAvailable)}
                sidebarCollapsed={sidebarCollapsed}
            />
            <main
                className={cn(
                    'pt-16 min-h-screen transition-all duration-300',
                    sidebarCollapsed ? 'pl-20' : 'pl-64'
                )}
            >
                <div className="p-6">
                    {children}
                </div>
            </main>
        </div>
    );
}
