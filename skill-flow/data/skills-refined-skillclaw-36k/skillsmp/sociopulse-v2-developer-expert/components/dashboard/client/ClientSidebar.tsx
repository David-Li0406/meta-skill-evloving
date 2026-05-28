'use client';

import { useMemo, useState, useCallback } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import {
    LayoutDashboard,
    Siren,
    Calendar,
    FileSignature,
    Wallet,
    Users,
    Settings,
    LogOut,
    X,
    CalendarClock,
    Sparkles,
    FolderKanban,
    ChevronLeft,
    ChevronRight,
    ChevronDown,
    Building2,
    Shield,
    HelpCircle,
    MessageSquare,
    Bell,
    Moon,
    Sun,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { currentBrand, isMedical } from '@/lib/brand';
import { domainConfig, getTerm, isFeatureEnabled } from '@/lib/domain-config';
import { useTheme } from '@/components/providers/ThemeProvider';
import { auth } from '@/lib/auth';

interface ClientSidebarProps {
    isOpen?: boolean;
    onClose?: () => void;
    collapsed?: boolean;
    onToggleCollapse?: () => void;
    user?: {
        name: string;
        avatarUrl?: string;
        establishmentName?: string;
        role?: string;
        isVerified?: boolean;
    };
    /** Badge counts for nav items */
    badges?: {
        missions?: number;
        messages?: number;
        notifications?: number;
        bookings?: number;
    };
}

interface MenuItem {
    label: string;
    href: string;
    icon: React.ElementType;
    alertStyle?: boolean;
    badgeKey?: keyof NonNullable<ClientSidebarProps['badges']>;
    featureFlag?: keyof typeof domainConfig.features;
}

interface MenuGroup {
    title: string;
    items: MenuItem[];
}

/**
 * Build grouped menu items dynamically based on domain config
 */
function useMenuGroups(): MenuGroup[] {
    return useMemo(() => {
        // ───────────────────────────────────────────────────────────
        // GROUP 1: Principal (always visible)
        // ───────────────────────────────────────────────────────────
        const principalGroup: MenuGroup = {
            title: 'Principal',
            items: [
                {
                    label: getTerm('dashboardTitle'),
                    href: '/dashboard/client',
                    icon: LayoutDashboard,
                },
                {
                    label: getTerm('urgentAction'),
                    href: '/dashboard/client/missions',
                    icon: Siren,
                    alertStyle: true,
                    badgeKey: 'missions',
                },
            ],
        };

        // ───────────────────────────────────────────────────────────
        // GROUP 2: Activité (domain-specific)
        // ───────────────────────────────────────────────────────────
        const activityItems: MenuItem[] = [];

        // Medical: Shift Planner
        if (isFeatureEnabled('enableShiftView')) {
            activityItems.push({
                label: 'Planning Vacations',
                href: '/dashboard/client/shifts',
                icon: CalendarClock,
            });
        }

        // Social: Projects
        if (isFeatureEnabled('enableProjects')) {
            activityItems.push({
                label: 'Mes Projets',
                href: '/dashboard/client/projects',
                icon: FolderKanban,
            });
        }

        // Social: Workshops
        if (isFeatureEnabled('enableWorkshops')) {
            activityItems.push({
                label: 'Ateliers',
                href: '/dashboard/client/workshops',
                icon: Sparkles,
            });
        }

        // Common activity items
        activityItems.push(
            {
                label: getTerm('bookingPlural'),
                href: '/dashboard/client/bookings',
                icon: Calendar,
                badgeKey: 'bookings',
            },
            {
                label: 'Messages',
                href: '/messages',
                icon: MessageSquare,
                badgeKey: 'messages',
            }
        );

        const activityGroup: MenuGroup = {
            title: 'Activité',
            items: activityItems,
        };

        // ───────────────────────────────────────────────────────────
        // GROUP 3: Gestion
        // ───────────────────────────────────────────────────────────
        const gestionGroup: MenuGroup = {
            title: 'Gestion',
            items: [
                {
                    label: 'Administratif',
                    href: '/dashboard/client/admin',
                    icon: FileSignature,
                },
                {
                    label: 'Finance',
                    href: '/dashboard/client/finance',
                    icon: Wallet,
                },
                {
                    label: 'Mon Vivier',
                    href: '/dashboard/client/team',
                    icon: Users,
                },
            ],
        };

        // ───────────────────────────────────────────────────────────
        // GROUP 4: Compte
        // ───────────────────────────────────────────────────────────
        const compteGroup: MenuGroup = {
            title: 'Compte',
            items: [
                {
                    label: 'Paramètres',
                    href: '/dashboard/client/settings',
                    icon: Settings,
                },
                {
                    label: "Centre d'aide",
                    href: '/help',
                    icon: HelpCircle,
                },
            ],
        };

        return [principalGroup, activityGroup, gestionGroup, compteGroup];
    }, []);
}

export function ClientSidebar({ 
    isOpen = true, 
    onClose, 
    collapsed = false,
    onToggleCollapse,
    user,
    badges = {},
}: ClientSidebarProps) {
    const pathname = usePathname();
    const router = useRouter();
    const menuGroups = useMenuGroups();
    const [showUserMenu, setShowUserMenu] = useState(false);
    const { isDark, toggleColorMode } = useTheme();

    const isActive = (href: string) => {
        if (href === '/dashboard/client') {
            return pathname === href;
        }
        return pathname.startsWith(href);
    };

    const handleLogout = useCallback(async () => {
        await auth.logout();
        router.push('/auth/login');
    }, [router]);

    // Theme toggle item for dropdown
    const ThemeToggleItem = () => (
        <button
            onClick={toggleColorMode}
            className="flex w-full items-center gap-2 px-3 py-2 text-sm text-slate-600 hover:bg-slate-50 hover:text-slate-900 dark:text-slate-300 dark:hover:bg-slate-700 dark:hover:text-white"
        >
            {isDark ? <Sun className="h-4 w-4 text-amber-500" /> : <Moon className="h-4 w-4" />}
            {isDark ? 'Mode clair' : 'Mode sombre'}
        </button>
    );

    // Brand-specific gradient for logo - using polymorphic primary colors
    const logoGradient = isMedical()
        ? 'from-rose-400 to-rose-600'
        : 'from-primary-400 to-primary-600';

    // Badge renderer
    const renderBadge = (count?: number) => {
        if (!count || count <= 0) return null;
        return (
            <span className={cn(
                'ml-auto flex h-5 min-w-5 items-center justify-center rounded-full px-1.5 text-xs font-semibold',
                'bg-rose-500 text-white',
                collapsed && 'absolute -right-1 -top-1 h-4 min-w-4 text-[10px]'
            )}>
                {count > 99 ? '99+' : count}
            </span>
        );
    };

    return (
        <aside
            className={cn(
                'fixed inset-y-0 left-0 z-50 flex h-full flex-col transition-all duration-300 ease-in-out',
                // Light/Dark mode background
                'bg-white text-slate-900 dark:bg-slate-900 dark:text-slate-100',
                // Border
                'border-r border-slate-200 dark:border-slate-800',
                // Width based on collapsed state
                collapsed ? 'w-[72px]' : 'w-64',
                // Mobile transform
                'lg:translate-x-0',
                isOpen ? 'translate-x-0' : '-translate-x-full'
            )}
            role="navigation"
            aria-label="Navigation principale"
        >
            {/* Header */}
            <div className={cn(
                'flex h-16 items-center border-b border-slate-200 dark:border-slate-800',
                collapsed ? 'justify-center px-2' : 'justify-between px-4'
            )}>
                <Link 
                    href="/dashboard/client" 
                    className="flex items-center gap-2"
                    title={currentBrand.appName}
                >
                    <div className={cn(
                        'flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br font-bold text-white shadow-lg',
                        logoGradient,
                        'transition-transform hover:scale-105'
                    )}>
                        {currentBrand.appName.charAt(0)}
                    </div>
                    {!collapsed && (
                        <span className="text-lg font-semibold tracking-tight text-slate-900">
                            {currentBrand.appName}
                        </span>
                    )}
                </Link>
                
                {/* Mobile close button */}
                {onClose && !collapsed && (
                    <button
                        onClick={onClose}
                        className="rounded-lg p-1.5 text-slate-500 hover:bg-slate-100 hover:text-slate-700 lg:hidden"
                        aria-label="Fermer le menu"
                    >
                        <X className="h-5 w-5" />
                    </button>
                )}
            </div>

            {/* Collapse toggle (desktop only) */}
            {onToggleCollapse && (
                <button
                    onClick={onToggleCollapse}
                    className={cn(
                        'absolute -right-3 top-20 z-10 hidden lg:flex',
                        'h-6 w-6 items-center justify-center rounded-full',
                        'border border-slate-200 bg-white text-slate-500 shadow-sm',
                        'hover:bg-slate-50 hover:text-slate-700',
                        'transition-colors'
                    )}
                    aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
                >
                    {collapsed ? (
                        <ChevronRight className="h-3.5 w-3.5" />
                    ) : (
                        <ChevronLeft className="h-3.5 w-3.5" />
                    )}
                </button>
            )}

            {/* Navigation with grouped sections */}
            <nav className="flex-1 overflow-y-auto py-4" aria-label="Menu principal">
                {menuGroups.map((group, groupIndex) => (
                    <div key={group.title} className={cn(groupIndex > 0 && 'mt-6')}>
                        {/* Group title - hidden when collapsed */}
                        {!collapsed && (
                            <h3 className="mb-2 px-4 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                                {group.title}
                            </h3>
                        )}
                        
                        {/* Group separator when collapsed */}
                        {collapsed && groupIndex > 0 && (
                            <div className="mx-3 mb-3 border-t border-slate-200" />
                        )}

                        <div className={cn('space-y-1', collapsed ? 'px-2' : 'px-3')}>
                            {group.items.map((item) => {
                                const active = isActive(item.href);
                                const badgeCount = item.badgeKey ? badges[item.badgeKey] : undefined;
                                
                                return (
                                    <Link
                                        key={item.href}
                                        href={item.href}
                                        onClick={onClose}
                                        title={collapsed ? item.label : undefined}
                                        className={cn(
                                            'group relative flex items-center rounded-lg text-sm font-medium transition-all',
                                            collapsed 
                                                ? 'h-10 w-10 justify-center' 
                                                : 'gap-3 px-3 py-2.5',
                                            // Active state
                                            active
                                                ? cn(
                                                    isMedical() 
                                                        ? 'bg-rose-50 text-rose-700' 
                                                        : 'bg-primary-50 text-primary-700'
                                                )
                                                : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900',
                                            // Alert style for urgent actions
                                            item.alertStyle && !active && 'text-rose-500 hover:text-rose-600'
                                        )}
                                        aria-current={active ? 'page' : undefined}
                                    >
                                        {/* Active indicator bar */}
                                        {active && (
                                            <span 
                                                className={cn(
                                                    'absolute left-0 h-full w-1 rounded-r-full',
                                                    isMedical() ? 'bg-rose-500' : 'bg-primary-500'
                                                )} 
                                            />
                                        )}
                                        
                                        <item.icon
                                            className={cn(
                                                'h-5 w-5 flex-shrink-0 transition-transform group-hover:scale-110',
                                                item.alertStyle && !active && 'text-rose-500',
                                                active && (isMedical() ? 'text-rose-600' : 'text-primary-600')
                                            )}
                                        />
                                        
                                        {!collapsed && (
                                            <>
                                                <span>{item.label}</span>
                                                {renderBadge(badgeCount)}
                                            </>
                                        )}
                                        
                                        {collapsed && renderBadge(badgeCount)}
                                        
                                        {/* Tooltip on hover when collapsed */}
                                        {collapsed && (
                                            <span className={cn(
                                                'pointer-events-none absolute left-full ml-2 whitespace-nowrap rounded-md px-2 py-1 text-xs font-medium',
                                                'bg-slate-900 text-white opacity-0 shadow-lg',
                                                'transition-opacity group-hover:opacity-100',
                                                'z-50'
                                            )}>
                                                {item.label}
                                            </span>
                                        )}
                                    </Link>
                                );
                            })}
                        </div>
                    </div>
                ))}
            </nav>

            {/* Footer - Enhanced User Profile */}
            <div className="border-t border-slate-200 dark:border-slate-800 p-3">
                <div 
                    className={cn(
                        'relative rounded-lg transition-colors',
                        showUserMenu ? 'bg-slate-100 dark:bg-slate-800' : 'hover:bg-slate-50 dark:hover:bg-slate-800/50'
                    )}
                >
                    <button
                        onClick={() => !collapsed && setShowUserMenu(!showUserMenu)}
                        className={cn(
                            'flex w-full items-center gap-3 p-2',
                            collapsed && 'justify-center'
                        )}
                        {...(!collapsed && {
                            'aria-expanded': showUserMenu,
                            'aria-haspopup': 'menu' as const,
                        })}
                    >
                        {/* Avatar with status indicator */}
                        <div className="relative">
                            <div className={cn(
                                'flex items-center justify-center rounded-full text-sm font-semibold',
                                collapsed ? 'h-9 w-9' : 'h-10 w-10',
                                'bg-gradient-to-br',
                                isMedical() ? 'from-rose-400 to-rose-600' : 'from-primary-400 to-primary-600'
                            )}>
                                {user?.avatarUrl ? (
                                    <img
                                        src={user.avatarUrl}
                                        alt={user.name || 'User'}
                                        className="h-full w-full rounded-full object-cover"
                                    />
                                ) : (
                                    user?.name?.charAt(0).toUpperCase() || 'U'
                                )}
                            </div>
                            {/* Verification badge */}
                            {user?.isVerified && (
                                <div className={cn(
                                    'absolute -bottom-0.5 -right-0.5 flex items-center justify-center rounded-full',
                                    'h-4 w-4 bg-emerald-500 ring-2 ring-white'
                                )}>
                                    <Shield className="h-2.5 w-2.5 text-white" />
                                </div>
                            )}
                        </div>
                        
                        {!collapsed && (
                            <>
                                <div className="flex-1 text-left">
                                    <p className="truncate text-sm font-medium text-slate-900">
                                        {user?.name || 'Utilisateur'}
                                    </p>
                                    <p className="flex items-center gap-1 truncate text-xs text-slate-500">
                                        <Building2 className="h-3 w-3" />
                                        {user?.establishmentName || 'Mon Établissement'}
                                    </p>
                                </div>
                                <ChevronDown className={cn(
                                    'h-4 w-4 text-slate-500 transition-transform',
                                    showUserMenu && 'rotate-180'
                                )} />
                            </>
                        )}
                    </button>
                    
                    {/* Dropdown menu */}
                    {showUserMenu && !collapsed && (
                        <div className="absolute bottom-full left-0 mb-2 w-full rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 py-1 shadow-xl">
                            <Link
                                href="/dashboard/client/settings"
                                className="flex items-center gap-2 px-3 py-2 text-sm text-slate-600 hover:bg-slate-50 hover:text-slate-900 dark:text-slate-300 dark:hover:bg-slate-700 dark:hover:text-white"
                                onClick={() => setShowUserMenu(false)}
                            >
                                <Settings className="h-4 w-4" />
                                Paramètres du compte
                            </Link>
                            <Link
                                href="/notifications"
                                className="flex items-center gap-2 px-3 py-2 text-sm text-slate-600 hover:bg-slate-50 hover:text-slate-900 dark:text-slate-300 dark:hover:bg-slate-700 dark:hover:text-white"
                                onClick={() => setShowUserMenu(false)}
                            >
                                <Bell className="h-4 w-4" />
                                Notifications
                                {badges.notifications && badges.notifications > 0 && (
                                    <span className="ml-auto rounded-full bg-rose-500 px-1.5 py-0.5 text-xs text-white">
                                        {badges.notifications}
                                    </span>
                                )}
                            </Link>
                            <ThemeToggleItem />
                            <div className="my-1 border-t border-slate-200 dark:border-slate-700" />
                            <button
                                onClick={handleLogout}
                                className="flex w-full items-center gap-2 px-3 py-2 text-sm text-rose-500 hover:bg-rose-50 hover:text-rose-600 dark:text-rose-400 dark:hover:bg-rose-950/50 dark:hover:text-rose-300"
                            >
                                <LogOut className="h-4 w-4" />
                                Déconnexion
                            </button>
                        </div>
                    )}
                </div>
                
                {/* Collapsed state: simple logout button */}
                {collapsed && (
                    <button
                        onClick={handleLogout}
                        className="mt-2 flex h-9 w-full items-center justify-center rounded-lg text-slate-500 hover:bg-slate-100 hover:text-rose-500 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-rose-400"
                        title="Déconnexion"
                        aria-label="Déconnexion"
                    >
                        <LogOut className="h-4 w-4" />
                    </button>
                )}
            </div>
        </aside>
    );
}
