import { Metadata } from 'next';
import { SeoFooter, type PublicOpportunityItem } from '@/components/landing';
import { HomepageClient } from '@/components/landing/HomepageClient';
import { currentBrand, isMedical, isCategoryAllowed } from '@/lib/brand';
import { SEED_DATA, type SeedItem } from '@/lib/seedData';

// ===========================================
// LANDING PAGE - Public Smart Feed Architecture
// SSR with Client-Side Interactivity
// ===========================================

export const metadata: Metadata = {
    title: currentBrand.metaTitle,
    description: currentBrand.metaDescription,
    keywords: isMedical()
        ? 'renfort soignant, interim santé, infirmier, aide-soignant, EHPAD, clinique, IDE, AS, AES'
        : 'renfort médico-social, interim social, SocioLive, atelier, éducateur, travailleur social, MECS, IME',
    openGraph: {
        title: currentBrand.metaTitle,
        description: currentBrand.metaDescription,
        type: 'website',
        siteName: currentBrand.appName,
    },
    twitter: {
        card: 'summary_large_image',
        title: currentBrand.appName,
        description: currentBrand.heroSubtitle,
    },
};

// Transform seed data to PublicOpportunityItem format
function transformSeedToFeedItems(data: SeedItem[]): PublicOpportunityItem[] {
    return data
        .filter(item => isCategoryAllowed(item.category))
        .slice(0, 12) // Initial 12 items for SSR
        .map((item, index) => {
            // Determine type based on item.type and category
            const opportunityType: 'mission' | 'profile' | 'service' =
                item.type === 'MISSION' ? 'mission'
                    : item.category === 'SOCIOLIVE' ? 'service'
                        : 'profile';

            // Build display name
            const displayName = item.data.firstName && item.data.lastName
                ? `${item.data.firstName} ${item.data.lastName}`
                : item.data.structureName || item.data.title;

            return {
                id: `seed-${index}-${item.type}`,
                type: opportunityType,
                title: displayName,
                subtitle: item.data.description,
                location: item.city,
                price: item.data.hourlyRate,
                imageUrl: item.data.logoUrl,
                isUrgent: item.data.tags.includes('Urgence'),
                isAvailable: item.data.isAvailable,
                tags: item.data.tags.filter(tag => tag !== 'Urgence'),
                category: item.category,
            };
        });
}

export default function LandingPage() {
    // Transform seed data for initial SSR render
    const initialItems = transformSeedToFeedItems(SEED_DATA);

    const initialMeta = {
        page: 1,
        hasNextPage: SEED_DATA.length > 12,
        total: SEED_DATA.length,
    };

    return (
        <div className="relative min-h-screen bg-canvas overflow-hidden">
            {/* Client-side interactive components */}
            <HomepageClient
                initialItems={initialItems}
                initialMeta={initialMeta}
            />

            {/* SEO Footer - Server rendered */}
            <SeoFooter />
        </div>
    );
}
