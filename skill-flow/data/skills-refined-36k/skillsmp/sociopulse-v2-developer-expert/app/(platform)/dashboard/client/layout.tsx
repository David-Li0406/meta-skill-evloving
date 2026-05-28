'use client';

import { useState, useEffect } from 'react';
import { ClientSidebar } from '@/components/dashboard/client/ClientSidebar';
import { ClientHeader } from '@/components/dashboard/client/ClientHeader';

interface ClientDashboardLayoutProps {
    children: React.ReactNode;
}

// Key for localStorage persistence
const SIDEBAR_COLLAPSED_KEY = 'client-sidebar-collapsed';

export default function ClientDashboardLayout({ children }: ClientDashboardLayoutProps) {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

    // Persist collapsed state in localStorage
    useEffect(() => {
        const saved = localStorage.getItem(SIDEBAR_COLLAPSED_KEY);
        if (saved === 'true') {
            setSidebarCollapsed(true);
        }
    }, []);

    const handleToggleCollapse = () => {
        const newValue = !sidebarCollapsed;
        setSidebarCollapsed(newValue);
        localStorage.setItem(SIDEBAR_COLLAPSED_KEY, String(newValue));
    };

    // Mock user data - replace with actual auth context
    const mockUser = {
        name: 'Jean Dupont',
        establishmentName: 'EHPAD Les Jardins',
        isVerified: true,
    };

    // Mock badge counts - replace with real data from API
    const mockBadges = {
        missions: 3,
        messages: 2,
        notifications: 5,
        bookings: 0,
    };

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-950 transition-colors">
            {/* Mobile overlay */}
            {sidebarOpen && (
                <div
                    className="fixed inset-0 z-40 bg-black/50 lg:hidden"
                    onClick={() => setSidebarOpen(false)}
                    aria-hidden="true"
                />
            )}

            {/* Sidebar */}
            <ClientSidebar
                isOpen={sidebarOpen}
                onClose={() => setSidebarOpen(false)}
                collapsed={sidebarCollapsed}
                onToggleCollapse={handleToggleCollapse}
                user={mockUser}
                badges={mockBadges}
            />

            {/* Main content area - adjusts based on collapsed state */}
            <div className={sidebarCollapsed ? 'lg:pl-[72px]' : 'lg:pl-64'}>
                <ClientHeader onMenuClick={() => setSidebarOpen(true)} />
                <main className="min-h-[calc(100vh-4rem)] transition-colors">
                    {children}
                </main>
            </div>
        </div>
    );
}
