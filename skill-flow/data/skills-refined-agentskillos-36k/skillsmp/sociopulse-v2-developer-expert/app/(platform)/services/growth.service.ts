'use client';

import { getApiBaseWithVersion } from '@/lib/config';

export type TagCategory = 'JOB' | 'STRUCTURE' | 'SKILL';
export type PointLogStatus = 'PENDING' | 'CONFIRMED' | 'CANCELLED';

export interface GrowthTag {
    id: string;
    name: string;
    category: TagCategory;
}

export interface GrowthSummary {
    userId: string;
    points: number;
    pendingPoints: number;
    referralCode: string | null;
    tags: GrowthTag[];
    profile: {
        avatarUrl: string | null;
        bio: string | null;
    } | null;
    referrals: {
        pendingCount: number;
        confirmedCount: number;
    };
}

export type PointActionType = 'PROFILE_PHOTO';

export interface AwardPointsResult {
    awarded: boolean;
    amount: number;
    status: PointLogStatus;
    points: number;
    pendingPoints: number;
}

const getApiBase = getApiBaseWithVersion;

const getToken = () => {
    if (typeof window === 'undefined') return null;

    const candidates = [
        window.localStorage.getItem('accessToken'),
        window.localStorage.getItem('token'),
        window.localStorage.getItem('jwt'),
    ].filter(Boolean) as string[];

    if (candidates.length > 0) return candidates[0];

    const cookieToken = document.cookie
        ?.split(';')
        .map((c) => c.trim())
        .find((c) => c.startsWith('accessToken=') || c.startsWith('token='));

    if (cookieToken) {
        const [, value] = cookieToken.split('=');
        return value;
    }

    return null;
};

const getAuthHeaders = (): Record<string, string> => {
    const token = getToken();
    if (!token) return {};

    const cleaned = token.replace(/^Bearer\s+/i, '').trim();
    return { Authorization: `Bearer ${cleaned}` };
};

async function handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
        const errorText = await response.text().catch(() => '');
        throw new Error(`Request failed ${response.status}: ${errorText}`);
    }

    return response.json() as Promise<T>;
}

export async function listTags(params?: { category?: TagCategory; search?: string; limit?: number }) {
    const search = new URLSearchParams();
    if (params?.category) search.set('category', params.category);
    if (params?.search) search.set('search', params.search);
    if (typeof params?.limit === 'number') search.set('limit', String(params.limit));

    const url = `${getApiBase()}/growth/tags${search.toString() ? `?${search.toString()}` : ''}`;
    const response = await fetch(url, { cache: 'no-store' });
    return handleResponse<GrowthTag[]>(response);
}

export async function getMyGrowthSummary() {
    const url = `${getApiBase()}/growth/me`;
    const response = await fetch(url, {
        method: 'GET',
        headers: { ...getAuthHeaders() },
        cache: 'no-store',
    });

    return handleResponse<GrowthSummary>(response);
}

export async function updateMyTags(tagIds: string[]) {
    const url = `${getApiBase()}/growth/me/tags`;
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...getAuthHeaders(),
        },
        body: JSON.stringify({ tagIds }),
        cache: 'no-store',
    });

    return handleResponse<unknown>(response);
}

export async function awardPoints(action: PointActionType, referenceId?: string) {
    const url = `${getApiBase()}/growth/points/award`;
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...getAuthHeaders(),
        },
        body: JSON.stringify({ action, referenceId }),
        cache: 'no-store',
    });

    return handleResponse<AwardPointsResult>(response);
}

