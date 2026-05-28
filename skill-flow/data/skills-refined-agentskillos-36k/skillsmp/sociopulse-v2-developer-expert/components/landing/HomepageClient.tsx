'use client';

import { HomeHero, FinalCTA } from '@/components/landing';
import { MainContent } from './MainContent';

// ===========================================
// PUBLIC HOMEPAGE CLIENT - Premium 2026
// Full-page experience with 5 body modules
// Motion, marquees, bentos, and conversion-focused
// ===========================================

interface HomepageClientProps {
    initialItems?: unknown[];
    initialMeta?: {
        page: number;
        hasNextPage: boolean;
        total?: number;
    };
}

export function HomepageClient({ }: HomepageClientProps) {
    return (
        <main className="min-h-screen">
            {/* Hero Section - Word Reveal Slider (UNTOUCHED) */}
            <HomeHero />

            {/* Main Content - The 5 Body Modules */}
            <MainContent />

            {/* Final CTA - Conversion Section */}
            <FinalCTA />
        </main>
    );
}
