'use client';

import { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Calendar,
    Home,
    MessageCircle,
    Siren,
    LogIn,
    UserPlus,
    Bell,
    User,
    LogOut,
    Settings,
    ChevronDown,
    Shield,
    HeartHandshake,
    Cross,
    ClipboardList
} from 'lucide-react';
import { useAuth } from '@/lib/useAuth';
import { CreateActionModal } from '@/components/create/CreateActionModal';
import { isMedical, currentBrand } from '@/lib/brand';

// ===========================================
// DESKTOP TOP NAV - Rock-Solid Fixed Design
// Fixed positioning, scroll transition, z-100
// ===========================================

interface NavItem {
    href: string;
    label: string;
    icon: React.ElementType;
    highlight?: boolean;
    badge?: boolean;
    requiresAuth?: boolean;
}

const NAV_ITEMS: NavItem[] = [
    { href: '/fil-pro', label: 'Fil Pro', icon: Home },
    { href: '/dashboard/tracking', label: 'Suivi', icon: ClipboardList, badge: true, requiresAuth: true },
    { href: '/dashboard/relief', label: 'SOS', icon: Siren, highlight: true },
    { href: '/bookings', label: 'Agenda', icon: Calendar, requiresAuth: true },
    { href: '/messages', label: 'Messages', icon: MessageCircle, requiresAuth: true },
];

// Fixed nav height for CLS prevention
const NAV_HEIGHT = 'h-16';

export function DesktopTopNav() {
    const pathname = usePathname();
    const { user, isAuthenticated, logout } = useAuth();
    const [showUserMenu, setShowUserMenu] = useState(false);
    const [notificationCount] = useState(3);
    const [messageCount] = useState(2);
    const [isScrolled, setIsScrolled] = useState(false);
    const menuRef = useRef<HTMLDivElement>(null);

    const activeMissionCount = 0;

    // Scroll detection for transparency transition
    useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 10);
        };
        handleScroll(); // Check initial state
        window.addEventListener('scroll', handleScroll, { passive: true });
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    // Close menu on outside click
    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
                setShowUserMenu(false);
            }
        }
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    // Hide on onboarding pages only
    if (pathname.startsWith('/onboarding')) {
        return null;
    }

    const getInitials = () => {
        if (user?.profile?.firstName && user?.profile?.lastName) {
            return `${user.profile.firstName[0]}${user.profile.lastName[0]}`.toUpperCase();
        }
        if (user?.profile?.firstName) {
            return user.profile.firstName.substring(0, 2).toUpperCase();
        }
        return 'U';
    };

    return (
        <>
            {/* Spacer to prevent content jump under fixed nav */}
            <div className={`hidden lg:block ${NAV_HEIGHT}`} aria-hidden="true" />

            {/* Fixed Navigation */}
            <header
                className={`
                    hidden lg:block fixed top-0 left-0 right-0 z-[100]
                    ${NAV_HEIGHT} transition-all duration-300 ease-out
                    ${isScrolled
                        ? 'bg-white/98 backdrop-blur-2xl border-b border-slate-200/60 shadow-lg shadow-slate-900/5'
                        : 'bg-white/95 backdrop-blur-xl border-b border-slate-100'
                    }
                `}
            >
                <div className="max-w-7xl mx-auto px-6 h-full flex items-center justify-between gap-6">

                    {/* Logo */}
                    <Link href="/" className="flex items-center gap-2.5 group flex-shrink-0">
                        <div className={`h-10 w-10 rounded-2xl flex items-center justify-center transition-transform group-hover:scale-105 shadow-lg ${isMedical()
                            ? 'bg-rose-500 shadow-rose-500/30'
                            : 'bg-gradient-to-br from-indigo-600 to-teal-500 shadow-indigo-500/30'
                            }`}>
                            {isMedical() ? (
                                <Cross className="h-6 w-6 text-white" strokeWidth={4} />
                            ) : (
                                <HeartHandshake className="h-6 w-6 text-white" strokeWidth={1.8} />
                            )}
                        </div>
                        <span className={`hidden sm:inline text-lg font-bold tracking-tight ${isMedical()
                            ? 'text-rose-500'
                            : 'bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-teal-500'
                            }`}>
                            {currentBrand.appName}
                        </span>
                    </Link>

                    {/* Nav Links - Center */}
                    <nav className="flex items-center gap-1 flex-1 justify-center">
                        {NAV_ITEMS.map((item) => {
                            const Icon = item.icon;
                            const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
                            const isHighlight = item.highlight;
                            const isMessages = item.href === '/messages';
                            const isSuivi = item.href === '/dashboard/tracking';
                            const showBadge = item.badge && activeMissionCount > 0;

                            // Determine link destination - redirect to login if auth required but not authenticated
                            const linkHref = (item.requiresAuth && !isAuthenticated) ? '/auth/login' : item.href;

                            // SOS Button - Always prominent
                            if (isHighlight) {
                                return (
                                    <Link key={item.href} href={linkHref} className="relative mx-2">
                                        <motion.span
                                            whileHover={{ scale: 1.05, y: -1 }}
                                            whileTap={{ scale: 0.95 }}
                                            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-gradient-to-r from-rose-500 via-rose-500 to-pink-500 text-white font-bold text-sm shadow-lg shadow-rose-500/25 hover:shadow-xl hover:shadow-rose-500/30 transition-shadow"
                                        >
                                            <Icon className="h-4 w-4" />
                                            {item.label}
                                        </motion.span>
                                    </Link>
                                );
                            }

                            return (
                                <Link
                                    key={item.href}
                                    href={linkHref}
                                    className={`relative inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 ease-out ${isActive
                                        ? `bg-slate-100/80 text-slate-900 shadow-sm ring-1 ring-slate-200/50`
                                        : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900 hover:shadow-sm'
                                        }`}
                                >
                                    <Icon className={`h-4 w-4 transition-colors ${isActive
                                        ? (isMedical() ? 'text-rose-500' : 'text-indigo-600')
                                        : 'text-slate-400'
                                        }`} />
                                    {item.label}

                                    {/* Message Badge */}
                                    {isMessages && isAuthenticated && messageCount > 0 && (
                                        <span className="absolute -top-1 -right-1 h-5 w-5 bg-indigo-600 text-white text-xs font-bold rounded-full flex items-center justify-center shadow-sm">
                                            {messageCount > 9 ? '9+' : messageCount}
                                        </span>
                                    )}

                                    {/* Active Mission Badge */}
                                    {showBadge && (
                                        <span className="absolute -top-1 -right-1 h-5 w-5 bg-teal-600 text-white text-xs font-bold rounded-full flex items-center justify-center shadow-sm">
                                            {activeMissionCount > 9 ? '9+' : activeMissionCount}
                                        </span>
                                    )}
                                </Link>
                            );
                        })}
                    </nav>

                    {/* Right Section - Auth */}
                    <div className="flex items-center gap-3 flex-shrink-0">
                        {isAuthenticated ? (
                            <>
                                {user ? <CreateActionModal user={user} /> : null}

                                {/* Notifications */}
                                <button className="relative p-2.5 rounded-xl bg-slate-50 hover:bg-slate-100 transition-colors">
                                    <Bell className="h-5 w-5 text-slate-600" />
                                    {notificationCount > 0 && (
                                        <span className="absolute -top-1 -right-1 h-5 w-5 bg-indigo-600 text-white text-xs font-bold rounded-full flex items-center justify-center">
                                            {notificationCount > 9 ? '9+' : notificationCount}
                                        </span>
                                    )}
                                </button>

                                {/* User Menu */}
                                <div className="relative" ref={menuRef}>
                                    <button
                                        onClick={() => setShowUserMenu(!showUserMenu)}
                                        className="flex items-center gap-2 px-2 py-1.5 rounded-xl bg-slate-50 hover:bg-slate-100 transition-colors"
                                    >
                                        {user?.profile?.avatarUrl ? (
                                            <img src={user.profile.avatarUrl} alt="Avatar" className="h-8 w-8 rounded-lg object-cover" />
                                        ) : (
                                            <div className={`h-8 w-8 rounded-lg flex items-center justify-center text-xs font-bold text-white ${isMedical()
                                                ? 'bg-gradient-to-br from-rose-500 to-rose-600'
                                                : 'bg-gradient-to-br from-indigo-600 to-teal-500'
                                                }`}>
                                                {getInitials()}
                                            </div>
                                        )}
                                        <ChevronDown className={`h-4 w-4 text-slate-400 transition-transform ${showUserMenu ? 'rotate-180' : ''}`} />
                                    </button>

                                    {/* Dropdown Menu */}
                                    <AnimatePresence>
                                        {showUserMenu && (
                                            <motion.div
                                                initial={{ opacity: 0, y: -10, scale: 0.95 }}
                                                animate={{ opacity: 1, y: 0, scale: 1 }}
                                                exit={{ opacity: 0, y: -10, scale: 0.95 }}
                                                transition={{ duration: 0.15 }}
                                                className="absolute right-0 mt-2 w-56 py-2 bg-white rounded-2xl shadow-xl border border-slate-200 z-50"
                                            >
                                                <div className="px-4 py-3 border-b border-slate-100">
                                                    <p className="text-sm font-semibold text-slate-900">
                                                        {user?.profile?.firstName} {user?.profile?.lastName}
                                                    </p>
                                                    <p className="text-xs text-slate-500 truncate">
                                                        {user?.email}
                                                    </p>
                                                </div>

                                                <Link
                                                    href="/dashboard"
                                                    className="flex items-center gap-3 px-4 py-2.5 text-sm text-slate-700 hover:bg-slate-50"
                                                    onClick={() => setShowUserMenu(false)}
                                                >
                                                    <User className="h-4 w-4 text-slate-400" />
                                                    Mon espace
                                                </Link>

                                                <Link
                                                    href="/settings"
                                                    className="flex items-center gap-3 px-4 py-2.5 text-sm text-slate-700 hover:bg-slate-50"
                                                    onClick={() => setShowUserMenu(false)}
                                                >
                                                    <Settings className="h-4 w-4 text-slate-400" />
                                                    Paramètres
                                                </Link>

                                                {user?.role === 'ADMIN' && (
                                                    <Link
                                                        href="/admin"
                                                        className="flex items-center gap-3 px-4 py-2.5 text-sm text-purple-700 hover:bg-purple-50"
                                                        onClick={() => setShowUserMenu(false)}
                                                    >
                                                        <Shield className="h-4 w-4 text-purple-500" />
                                                        Administration
                                                    </Link>
                                                )}

                                                <div className="border-t border-slate-100 mt-2 pt-2">
                                                    <button
                                                        onClick={() => {
                                                            logout();
                                                            setShowUserMenu(false);
                                                        }}
                                                        className="flex items-center gap-3 w-full px-4 py-2.5 text-sm text-red-600 hover:bg-red-50"
                                                    >
                                                        <LogOut className="h-4 w-4" />
                                                        Se déconnecter
                                                    </button>
                                                </div>
                                            </motion.div>
                                        )}
                                    </AnimatePresence>
                                </div>
                            </>
                        ) : (
                            <>
                                <Link
                                    href="/auth/register"
                                    className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold border border-slate-300 text-slate-700 hover:bg-slate-50 transition-colors"
                                >
                                    <UserPlus className="h-4 w-4" />
                                    S'inscrire
                                </Link>

                                <Link
                                    href="/auth/login"
                                    className={`inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-bold text-white shadow-lg transition-all duration-200 hover:scale-[1.02] hover:shadow-xl active:scale-[0.98] ${isMedical()
                                        ? 'bg-gradient-to-r from-rose-500 via-rose-500 to-pink-500 shadow-rose-500/25 hover:shadow-rose-500/35'
                                        : 'bg-gradient-to-r from-indigo-600 via-indigo-500 to-teal-500 shadow-indigo-500/25 hover:shadow-indigo-500/35'
                                        }`}
                                >
                                    <LogIn className="h-4 w-4" />
                                    Se connecter
                                </Link>
                            </>
                        )}
                    </div>
                </div>
            </header>
        </>
    );
}
