/**
 * Centralized API Configuration
 * Single source of truth for API URL across the application
 */

export const ENV = {
    API_URL: process.env.NEXT_PUBLIC_API_URL,
    IS_PROD: process.env.NODE_ENV === 'production',
};

// Runtime warning for missing API URL (only in browser)
if (!ENV.API_URL && typeof window !== 'undefined') {
    console.error('❌ CRITICAL: NEXT_PUBLIC_API_URL is not defined!');
}

/**
 * Get the base API URL with trailing slash removed
 * @returns API base URL (e.g., "https://api.sociopulse.fr/api/v1")
 */
export const getApiUrl = (): string => {
    // Helper to ensure URL ends with /api/v1
    const ensureApiVersion = (url: string): string => {
        const cleanedUrl = url.replace(/\/+$/, ''); // Remove trailing slashes first
        if (cleanedUrl.endsWith('/api/v1')) {
            return cleanedUrl;
        }
        return `${cleanedUrl}/api/v1`;
    };

    // Client-side: dynamic fallback based on hostname
    if (typeof window !== 'undefined') {
        let url = 'https://api.sociopulse.fr/api/v1'; // Default production URL

        const envUrl = process.env.NEXT_PUBLIC_API_URL;

        if (envUrl) {
            url = envUrl;
        } else if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            url = 'http://localhost:4000';
        }

        return ensureApiVersion(url);
    }

    // Server-side (SSR):
    // 1. Explicit internal networking URL (Recommended for Docker)
    if (process.env.INTERNAL_API_URL) {
        return ensureApiVersion(process.env.INTERNAL_API_URL);
    }

    // 2. Fallback to public URL if no internal one is set
    if (process.env.NEXT_PUBLIC_API_URL) {
        return process.env.NEXT_PUBLIC_API_URL.replace(/\/+$/, '');
    }

    // 3. Production fallback: use the public API URL
    // The internal Docker hostname 'api' may not resolve across networks
    if (process.env.NODE_ENV === 'production') {
        return 'https://api.sociopulse.fr/api/v1';
    }

    // 4. Local Development
    return 'http://localhost:4000';
};

/**
 * Get the API URL with /api/v1 path if not already present
 * Use this for endpoints that need the versioned path
 */
export const getApiBaseWithVersion = (): string => {
    const url = getApiUrl();
    // If URL already contains /api/v1, return as-is
    if (url.includes('/api/v1')) {
        return url;
    }
    return `${url}/api/v1`;
};
