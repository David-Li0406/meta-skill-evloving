'use client';

import { TripleMarquee } from './TripleMarquee';
import { UniversBento, PowerBento } from './BentoGrids';
import { TrustSection } from './TrustSection';

// ===========================================
// MAIN CONTENT - Landing Page Body
// Assembles all 5 modules post-Hero
// ===========================================

export function MainContent() {
    return (
        <>
            {/* Module 1: The Pulse Explorer (Triple Marquee) */}
            <TripleMarquee />

            {/* Module 2: Univers Bento (Target Segmentation) */}
            <UniversBento />

            {/* Module 3: Power Bento (SaaS Features) */}
            <PowerBento />

            {/* Module 4: Trust & Authority Section */}
            <TrustSection />

            {/* Module 5: Final CTA is handled separately in HomepageClient */}
        </>
    );
}
