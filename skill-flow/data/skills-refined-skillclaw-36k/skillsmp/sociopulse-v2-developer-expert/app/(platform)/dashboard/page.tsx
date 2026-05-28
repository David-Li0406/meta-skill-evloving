'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/useAuth';
import { Loader2 } from 'lucide-react';

// =============================================================================
// DASHBOARD HUB - Role-Based Redirect
// Routes users to their appropriate dashboard based on role
// =============================================================================

export default function DashboardHubPage() {
    const router = useRouter();
    const { user, isLoading, isAuthenticated } = useAuth();

    useEffect(() => {
        if (!isLoading) {
            if (!isAuthenticated || !user) {
                // Not authenticated - redirect to login
                router.replace('/auth/login');
                return;
            }

            // Route based on user role
            switch (user.role) {
                case 'CLIENT':
                    router.replace('/dashboard/client');
                    break;
                case 'TALENT':
                    router.replace('/dashboard/talent');
                    break;
                case 'ADMIN':
                    router.replace('/admin');
                    break;
                default:
                    // Fallback to fil-pro for unknown roles
                    router.replace('/fil-pro');
            }
        }
    }, [user, isLoading, isAuthenticated, router]);

    // Show loading while determining redirect
    return (
        <div className="min-h-screen bg-slate-50 flex items-center justify-center">
            <div className="text-center space-y-4">
                <Loader2 className="w-10 h-10 animate-spin text-primary-600 mx-auto" />
                <p className="text-slate-500">Redirection vers votre espace...</p>
            </div>
        </div>
    );
}
