'use client';

import { getApiBaseWithVersion } from '@/lib/config';

export type WallFeedParams = Record<string, string | number | boolean | undefined | null>;

export type PostCategory = 'EXPERIENCE' | 'NEWS';
export type ServiceType = 'WORKSHOP' | 'COACHING_VIDEO';

export interface CreateSocialPostPayload {
    title?: string;
    content: string;
    category: PostCategory;
    mediaUrls?: string[];
    ethicsConfirmed: true;
    city?: string;
    postalCode?: string;
    tags?: string[];
}

export interface CreateServicePayload {
    name: string;
    shortDescription?: string;
    description?: string;
    type?: ServiceType;
    category?: string;
    basePrice?: number;
    imageUrl?: string;
    tags?: string[];
    galleryUrls?: string[];
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

export async function getFeed(params: WallFeedParams = {}) {
    const search = new URLSearchParams();

    Object.entries(params).forEach(([key, value]) => {
        if (value === undefined || value === null) return;
        search.set(key, String(value));
    });

    const url = `${getApiBase()}/wall/feed${search.toString() ? `?${search.toString()}` : ''}`;

    try {
        const response = await fetch(url, { cache: 'no-store' });

        if (!response.ok) {
            throw new Error(`getFeed failed with status ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('getFeed error:', error);
        return { items: [] };
    }
}

export async function createSocialPost(payload: CreateSocialPostPayload) {
    const url = `${getApiBase()}/wall/posts`;

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...getAuthHeaders(),
        },
        body: JSON.stringify(payload),
        cache: 'no-store',
    });

    return handleResponse<unknown>(response);
}

export async function createService(payload: CreateServicePayload) {
    const url = `${getApiBase()}/wall/services`;

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...getAuthHeaders(),
        },
        body: JSON.stringify(payload),
        cache: 'no-store',
    });

    return handleResponse<unknown>(response);
}
