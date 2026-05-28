'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import Cookies from 'js-cookie';
import { getApiUrl } from './config';

const API_URL = getApiUrl();

export type ComplianceStatus = 'PENDING' | 'SUBMITTED' | 'VALIDATED' | 'REJECTED' | 'EXPIRED';

export interface UserProfile {
    id: string;
    email: string;
    phone?: string;
    role: 'CLIENT' | 'TALENT' | 'ADMIN';
    status: string;
    walletBalance: number;
    createdAt: string;
    profile?: {
        id: string;
        firstName: string;
        lastName: string;
        avatarUrl?: string;
        coverUrl?: string;
        headline?: string;
        bio?: string;
        city?: string;
        specialties?: string[];
        diplomas?: any[];
        hourlyRate?: number;
        radiusKm?: number;
        isVideoEnabled?: boolean;
        complianceStatus?: ComplianceStatus;
    };
    establishment?: {
        id: string;
        name: string;
        type?: string;
        address?: string;
        city?: string;
        siret?: string;
    };
}

interface UseAuthReturn {
    user: UserProfile | null;
    isLoading: boolean;
    isAuthenticated: boolean;
    error: string | null;
    refetch: () => Promise<void>;
    logout: () => void;
}

export function useAuth(): UseAuthReturn {
    const router = useRouter();
    const [user, setUser] = useState<UserProfile | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchUser = useCallback(async () => {
        const token = Cookies.get('accessToken');

        if (!token) {
            setUser(null);
            setIsLoading(false);
            return;
        }

        try {
            const response = await fetch(`${API_URL}/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                if (response.status === 401) {
                    // Token expired or invalid
                    Cookies.remove('accessToken');
                    setUser(null);
                    setError('Session expirée');
                    return;
                }
                throw new Error('Erreur de récupération du profil');
            }

            const userData = await response.json();
            setUser(userData);
            setError(null);
        } catch (err: any) {
            console.error('Auth fetch error:', err);
            setError(err.message);
            setUser(null);
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchUser();
    }, [fetchUser]);

    const logout = useCallback(() => {
        Cookies.remove('accessToken');
        setUser(null);
        // V2: Redirect to landing page after logout
        router.push('/');
    }, [router]);

    return {
        user,
        isLoading,
        isAuthenticated: !!user,
        error,
        refetch: fetchUser,
        logout,
    };
}
