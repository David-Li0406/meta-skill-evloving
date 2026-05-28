'use client';

import { getApiBaseWithVersion } from '@/lib/config';

export interface CreatePaymentIntentPayload {
    amount: number;
    currency: string;
    metadata?: Record<string, string | number | boolean>;
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
        throw new Error(`Payment request failed ${response.status}: ${errorText}`);
    }

    return response.json();
}

export async function createPaymentIntent(
    amount: number,
    currency: string,
    metadata: CreatePaymentIntentPayload['metadata'] = {}
) {
    const body: CreatePaymentIntentPayload = {
        amount,
        currency,
        metadata,
    };

    const response = await fetch(`${getApiBase()}/payments/create-intent`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...getAuthHeaders(),
        },
        body: JSON.stringify(body),
        cache: 'no-store',
    });

    return handleResponse(response) as Promise<{ clientSecret: string }>;
}

export async function createPaymentIntentForBooking(bookingId: string) {
    const response = await fetch(`${getApiBase()}/payments/create-intent/${bookingId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...getAuthHeaders(),
        },
        cache: 'no-store',
    });

    return handleResponse(response) as Promise<{
        clientSecret: string;
        paymentIntentId: string;
        amount: number;
    }>;
}

export async function confirmMockPayment(bookingId: string) {
    const response = await fetch(`${getApiBase()}/payments/confirm-mock/${bookingId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...getAuthHeaders(),
        },
        cache: 'no-store',
    });

    return handleResponse(response) as Promise<{
        success: boolean;
        bookingId: string;
        status: string;
    }>;
}

export async function getBookingForCheckout(bookingId: string) {
    const response = await fetch(`${getApiBase()}/payments/booking/${bookingId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            ...getAuthHeaders(),
        },
        cache: 'no-store',
    });

    return handleResponse(response);
}

