'use client';

import { DashboardResolver } from '@/components/dashboard';

/**
 * Client Dashboard Page
 * 
 * Uses DashboardResolver to render the appropriate dashboard based on domain:
 * - MedicoPulse (MEDICAL): ShiftPlanner view (calendar-dense shift management)
 * - SocioPulse (SOCIAL): ProjectHub view (card-based project overview)
 */
export default function ClientDashboardPage() {
    return <DashboardResolver role="CLIENT" />;
}
