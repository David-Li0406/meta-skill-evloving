import { Metadata } from 'next';
import { WallFeedClient } from '@/components/wall/WallFeedClient';
import { getApiBaseWithVersion } from '@/lib/config';

// ===========================================
// SOCIOPULSE WALL FEED - /feed Route
// B2B2C Platform for Medical-Social Sector
// Moved from root to dedicated route
// ===========================================

export const metadata: Metadata = {
    title: 'Fil d\'actualité | Sociopulse - Renforts & SocioLive',
    description: 'Découvrez les offres de mission et services SocioLive disponibles. Trouvez votre prochain renfort ou atelier en temps réel.',
    keywords: 'renfort médico-social, interim social, SocioLive, atelier, EHPAD, IDE, aide-soignant, éducateur',
    openGraph: {
        title: 'Fil d\'actualité | Sociopulse',
        description: 'La plateforme de mise en relation médico-sociale B2B2C. Missions de renfort et services SocioLive.',
        type: 'website',
        siteName: 'Sociopulse',
    },
    twitter: {
        card: 'summary_large_image',
        title: 'Fil d\'actualité | Sociopulse',
        description: 'Un renfort demain. Une Visio ou un Atelier maintenant.',
    },
};

const getApiBase = getApiBaseWithVersion;

type InitialFeed = {
    items: any[];
    nextCursor: string | null;
    hasNextPage: boolean;
};

async function getInitialFeed(): Promise<InitialFeed> {
    try {
        const response = await fetch(`${getApiBase()}/wall/feed`, {
            cache: 'no-store'
        });
        if (!response.ok) return { items: [], nextCursor: null, hasNextPage: false };

        const data = await response.json();
        const items = Array.isArray(data?.items) ? data.items : Array.isArray(data) ? data : [];
        const nextCursor = typeof data?.pageInfo?.nextCursor === 'string' ? data.pageInfo.nextCursor : null;
        const hasNextPage = Boolean(data?.pageInfo?.hasNextPage);
        return { items, nextCursor, hasNextPage };
    } catch {
        return { items: [], nextCursor: null, hasNextPage: false };
    }
}

interface FeedPageProps {
    searchParams: Promise<{ mode?: string }>;
}

export default async function FeedPage({ searchParams }: FeedPageProps) {
    const feed = await getInitialFeed();
    const params = await searchParams;
    const mode = params.mode || 'all'; // 'client', 'talent', or 'all'

    return (
        <WallFeedClient
            initialData={feed.items}
            initialNextCursor={feed.nextCursor}
            initialHasNextPage={feed.hasNextPage}
            talentPool={[]}
            activity={[]}
        />
    );
}
