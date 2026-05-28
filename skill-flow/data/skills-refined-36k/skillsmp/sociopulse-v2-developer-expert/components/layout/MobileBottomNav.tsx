'use client';

import { usePathname } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import {
    Home,
    Siren,
    Calendar,
    User,
    Plus,
    Shield,
    ClipboardList
} from 'lucide-react';
import { useAuth } from '@/lib/useAuth';
import { useSocket } from '@/components/providers';
import { CreateActionModal } from '@/components/create/CreateActionModal';

interface NavItem {
    href: string;
    label: string;
    icon: React.ElementType;
    highlight?: boolean;
    badge?: boolean;
}

const NAV_ITEMS: NavItem[] = [
    { href: '/fil-pro', label: 'Accueil', icon: Home },
    { href: '/bookings', label: 'Agenda', icon: Calendar },
    { href: '/dashboard/tracking', label: 'Suivi', icon: ClipboardList, highlight: true, badge: true },
    { href: '/dashboard/relief', label: 'SOS', icon: Siren },
    { href: '/dashboard', label: 'Profil', icon: User },
];

export function MobileBottomNav() {
    const pathname = usePathname();
    const { user } = useAuth();
    const { activeMissionsCount } = useSocket();
    const isAdmin = user?.role === 'ADMIN';
    const canPublish = Boolean(user && (user.role === 'CLIENT' || user.role === 'TALENT'));

    // Use real-time count from socket, fallback to 0
    const activeMissionCount = activeMissionsCount;

    // Hide on onboarding pages only
    if (pathname.startsWith('/onboarding')) {
        return null;
    }

    // Build nav items - replace Agenda with Admin for admin users
    const navItems = isAdmin
        ? NAV_ITEMS.map(item =>
            item.href === '/bookings'
                ? { href: '/admin', label: 'Admin', icon: Shield }
                : item
        )
        : NAV_ITEMS;

    // Hide on desktop
    return (
        <nav className="fixed bottom-0 left-0 right-0 z-50 lg:hidden">
            {/* Glass background */}
            <div className="absolute inset-0 bg-white/80 backdrop-blur-xl border-t border-gray-200" />

            {/* Safe area padding for iPhone */}
            <div className="relative px-2 pb-safe">
                {canPublish && user ? (
                    <div className="absolute right-4 -top-6 z-10">
                        <CreateActionModal
                            user={user}
                            trigger={
                                <button
                                    type="button"
                                    className="w-14 h-14 rounded-full bg-gradient-to-br from-indigo-600 to-teal-500 flex items-center justify-center shadow-lg shadow-indigo-500/30"
                                    aria-label="Publier"
                                >
                                    <Plus className="w-6 h-6 text-white" />
                                </button>
                            }
                        />
                    </div>
                ) : null}

                <div className="flex items-center justify-around h-16">
                    {navItems.map((item) => {
                        const Icon = item.icon;
                        const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
                        const isHighlight = 'highlight' in item && item.highlight;
                        const isAdminItem = item.href === '/admin';
                        const showBadge = 'badge' in item && item.badge && activeMissionCount > 0;

                        // Center highlighted item (Suivi)
                        if (isHighlight) {
                            return (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    className="relative -mt-6"
                                >
                                    <motion.div
                                        whileTap={{ scale: 0.9 }}
                                        className={`w-14 h-14 rounded-full flex items-center justify-center shadow-lg ${isActive
                                            ? 'bg-gradient-to-br from-indigo-600 to-teal-500 shadow-indigo-500/30'
                                            : 'bg-gradient-to-br from-indigo-500 to-teal-400 shadow-indigo-400/20'
                                            }`}
                                    >
                                        <Icon className="w-6 h-6 text-white" />
                                        {/* Badge for active missions */}
                                        {showBadge && (
                                            <span className="absolute -top-1 -right-1 h-5 w-5 bg-rose-500 text-white text-xs font-bold rounded-full flex items-center justify-center">
                                                {activeMissionCount > 9 ? '9+' : activeMissionCount}
                                            </span>
                                        )}
                                    </motion.div>
                                    <span className={`absolute -bottom-5 left-1/2 -translate-x-1/2 text-[10px] font-medium ${isActive ? 'text-indigo-600' : 'text-indigo-500'
                                        }`}>
                                        {item.label}
                                    </span>
                                </Link>
                            );
                        }

                        return (
                            <Link
                                key={item.href}
                                href={item.href}
                                className="flex flex-col items-center gap-0.5 py-2 px-3"
                            >
                                <motion.div
                                    whileTap={{ scale: 0.9 }}
                                    className={`
                                        p-2 rounded-xl transition-colors
                                        ${isActive ? (isAdminItem ? 'bg-purple-100' : 'bg-brand-100') : ''}
                                    `}
                                >
                                    <Icon className={`
                                        w-5 h-5 transition-colors
                                        ${isActive ? (isAdminItem ? 'text-purple-600' : 'text-brand-600') : 'text-gray-400'}
                                    `} />
                                </motion.div>
                                <span className={`
                                    text-[10px] font-medium transition-colors
                                    ${isActive ? (isAdminItem ? 'text-purple-600' : 'text-brand-600') : 'text-gray-400'}
                                `}>
                                    {item.label}
                                </span>
                            </Link>
                        );
                    })}
                </div>
            </div>
        </nav>
    );
}

