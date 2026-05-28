'use client';

import { getApiBaseWithVersion } from '@/lib/config';

export interface CreateReliefMissionInput {
    title?: string;
    jobTitle?: string;
    jobId?: string;
    hourlyRate?: number;
    isNightShift?: boolean;
    urgencyLevel?: string;
    description?: string;
    startDate?: string;
    endDate?: string;
    city?: string;
    postalCode?: string;
    address?: string;
    latitude?: number;
    longitude?: number;
    radiusKm?: number;
    requiredSkills?: string[];
    requiredDiplomas?: string[];
    specialtiesTags?: string[];
    requiresCar?: boolean;
    requiresNight?: boolean;
    requiresDiploma?: boolean;
    serviceName?: string;
    targetPublic?: string;
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

async function handleResponse(response: Response) {
    if (!response.ok) {
        const errorText = await response.text().catch(() => '');
        throw new Error(`Request failed ${response.status}: ${errorText}`);
    }

    return response.json();
}

export async function createReliefMission(data: CreateReliefMissionInput) {
    const payload = {
        ...data,
        title: data.title || `Renfort - ${data.jobTitle || 'Mission'}`,
        requiredSkills: data.requiredSkills ?? data.specialtiesTags ?? [],
        specialtiesTags: data.specialtiesTags ?? data.requiredSkills ?? [],
        requiresNight: data.requiresNight ?? data.isNightShift,
    };

    const response = await fetch(`${getApiBase()}/matching/missions`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...getAuthHeaders(),
        },
        body: JSON.stringify(payload),
        cache: 'no-store',
    });

    return handleResponse(response);
}

export async function getActiveMissions() {
    const response = await fetch(`${getApiBase()}/matching/missions`, {
        method: 'GET',
        headers: {
            ...getAuthHeaders(),
        },
        cache: 'no-store',
    });

    return handleResponse(response);
}

export async function getMissionCandidates(missionId: string) {
    const response = await fetch(`${getApiBase()}/matching/missions/${missionId}/candidates`, {
        method: 'GET',
        headers: {
            ...getAuthHeaders(),
        },
        cache: 'no-store',
    });

    return handleResponse(response);
}

export async function getMissionById(missionId: string) {
    const response = await fetch(`${getApiBase()}/matching/missions/${missionId}`, {
        method: 'GET',
        headers: {
            ...getAuthHeaders(),
        },
        cache: 'no-store',
    });

    return handleResponse(response);
}
