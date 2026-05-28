'use client';

import { usePathname } from 'next/navigation';
import { Menu, Bell, Plus } from 'lucide-react';
import { PublishModal, usePublishModal } from '@/components/publish';

interface ClientHeaderProps {
    onMenuClick?: () => void;
}

const pageTitles: Record<string, string> = {
    '/dashboard/client': 'Tableau de bord',
    '/dashboard/client/missions': 'Gestion des Missions',
    '/dashboard/client/bookings': 'Réservations',
    '/dashboard/client/admin': 'Administratif',
    '/dashboard/client/finance': 'Finance',
    '/dashboard/client/team': 'Mon Équipe',
    '/dashboard/client/settings': 'Paramètres',
};

export function ClientHeader({ onMenuClick }: ClientHeaderProps) {
    const pathname = usePathname();
    const { isOpen, open, close } = usePublishModal();

    // Find the matching title (exact match or starts with for nested routes)
    const getPageTitle = () => {
        if (pageTitles[pathname]) {
            return pageTitles[pathname];
        }
        // Check for nested routes
        const matchingPath = Object.keys(pageTitles)
            .filter(path => path !== '/dashboard/client')
            .find(path => pathname.startsWith(path));
        return matchingPath ? pageTitles[matchingPath] : 'Dashboard';
    };

    return (
        <>
            <header className="sticky top-0 z-40 flex h-16 items-center justify-between border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 px-4 lg:px-6 transition-colors">
                {/* Left side */}
                <div className="flex items-center gap-4">
                    <button
                        onClick={onMenuClick}
                        className="rounded-md p-2 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 lg:hidden"
                        aria-label="Ouvrir le menu"
                    >
                        <Menu className="h-5 w-5" />
                    </button>
                    <h1 className="text-xl font-semibold text-slate-900 dark:text-white">
                        {getPageTitle()}
                    </h1>
                </div>

                {/* Right side */}
                <div className="flex items-center gap-3">
                    <button
                        onClick={open}
                        className="hidden sm:inline-flex items-center gap-2 rounded-full bg-slate-900 dark:bg-white px-4 py-2 text-sm font-medium text-white dark:text-slate-900 transition-colors hover:bg-slate-800 dark:hover:bg-slate-100"
                    >
                        <Plus className="h-4 w-4" />
                        Publier
                    </button>

                    <button
                        className="relative rounded-md p-2 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
                        aria-label="Notifications"
                    >
                        <Bell className="h-5 w-5" />
                        {/* Notification badge */}
                        <span className="absolute right-1 top-1 flex h-2 w-2">
                            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-red-400 opacity-75"></span>
                            <span className="relative inline-flex h-2 w-2 rounded-full bg-red-500"></span>
                        </span>
                    </button>
                </div>
            </header>

            <PublishModal isOpen={isOpen} onClose={close} />
        </>
    );
}
