'use client';

import { DashboardResolver } from '@/components/dashboard';

/**
 * Talent Dashboard Page
 * 
 * Uses DashboardResolver to render the appropriate dashboard based on domain:
 * - MedicoPulse (MEDICAL): JobTicker view (fast list of urgent shifts)
 * - SocioPulse (SOCIAL): PortfolioFeed view (skills showcase + mission feed)
 */
export default function TalentDashboardPage() {
    return <DashboardResolver role="TALENT" />;
}
