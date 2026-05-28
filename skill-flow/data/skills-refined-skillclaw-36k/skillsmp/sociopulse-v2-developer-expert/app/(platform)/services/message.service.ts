'use client';

import { getApiBaseWithVersion } from '@/lib/config';

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
        .find((c) => c.startsWith('token=') || c.startsWith('accessToken='));

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

export async function sendMessage(recipientId: string, content: string) {
    const response = await fetch(`${getApiBase()}/messages`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...getAuthHeaders(),
        },
        body: JSON.stringify({ recipientId, content }),
        cache: 'no-store',
    });

    if (!response.ok) {
        const errorText = await response.text().catch(() => '');
        throw new Error(`sendMessage failed: ${response.status} ${errorText}`);
    }

    return response.json();
}
