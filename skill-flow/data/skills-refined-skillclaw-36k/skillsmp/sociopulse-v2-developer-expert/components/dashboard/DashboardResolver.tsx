'use client';

import { isMedical } from '@/lib/brand';
import { getDashboardLayout, DashboardLayoutType } from '@/lib/domain-config';

// Lazy imports for code splitting
import dynamic from 'next/dynamic';
import type { ComponentType } from 'react';

// =============================================================================
// TYPES
// =============================================================================

export type UserRole = 'CLIENT' | 'TALENT';

export interface DashboardUser {
    id: string;
    name: string;
    email: string;
    role: UserRole;
    avatarUrl?: string;
    establishmentName?: string;
    profileCompletion?: number;
}

export interface DashboardResolverProps {
    role: UserRole;
    user?: DashboardUser;
}

interface DashboardComponentProps {
    user?: DashboardUser;
}

// =============================================================================
// SKELETON LOADER
// =============================================================================

function DashboardSkeleton() {
    return (
        <div className="p-6 space-y-6 animate-pulse">
            {/* Header skeleton */}
            <div className="h-24 bg-slate-200 rounded-2xl" />
            
            {/* Grid skeleton */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 h-64 bg-slate-200 rounded-xl" />
                <div className="h-64 bg-slate-200 rounded-xl" />
            </div>
            
            {/* Cards skeleton */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="h-20 bg-slate-200 rounded-xl" />
                <div className="h-20 bg-slate-200 rounded-xl" />
                <div className="h-20 bg-slate-200 rounded-xl" />
            </div>
        </div>
    );
}

// =============================================================================
// DYNAMIC IMPORTS - Code splitting by dashboard variant
// =============================================================================

const MedicalClientDashboard = dynamic<DashboardComponentProps>(
    () => import('./client/MedicalClientDashboard'),
    { loading: () => <DashboardSkeleton /> }
);

const SocialClientDashboard = dynamic<DashboardComponentProps>(
    () => import('./client/SocialClientDashboard'),
    { loading: () => <DashboardSkeleton /> }
);

const MedicalTalentDashboard = dynamic<DashboardComponentProps>(
    () => import('./talent/MedicalTalentDashboard'),
    { loading: () => <DashboardSkeleton /> }
);

const SocialTalentDashboard = dynamic<DashboardComponentProps>(
    () => import('./talent/SocialTalentDashboard'),
    { loading: () => <DashboardSkeleton /> }
);

// =============================================================================
// DASHBOARD RESOLVER
// Component injection based on role + domain config
// =============================================================================

export function DashboardResolver({ role, user }: DashboardResolverProps) {
    const layout = getDashboardLayout(role.toLowerCase() as 'client' | 'talent');
    
    return resolveDashboard(layout, user);
}

/**
 * Resolves the correct dashboard component based on layout type
 */
function resolveDashboard(layout: DashboardLayoutType, user?: DashboardUser) {
    switch (layout) {
        case 'shift-planner':
            return <MedicalClientDashboard user={user} />;
        case 'project-hub':
            return <SocialClientDashboard user={user} />;
        case 'job-ticker':
            return <MedicalTalentDashboard user={user} />;
        case 'portfolio-feed':
            return <SocialTalentDashboard user={user} />;
        default:
            // Fallback based on brand
            if (isMedical()) {
                return <MedicalClientDashboard user={user} />;
            }
            return <SocialClientDashboard user={user} />;
    }
}

export default DashboardResolver;
