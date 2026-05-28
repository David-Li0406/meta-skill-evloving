/** @type {import('next').NextConfig} */
const nextConfig = {
    output: "standalone",
    reactStrictMode: true,
    // ignoreBuildErrors SUPPRIMÉ pour garantir la qualité du code
    images: {
        remotePatterns: [
            {
                protocol: 'https',
                hostname: '**', // À restreindre en production
            },
        ],
    },
    async rewrites() {
        const apiUrl =
            process.env.NEXT_PUBLIC_API_URL ||
            process.env.API_URL ||
            'http://localhost:4000';
        const normalized = apiUrl.replace(/\/+$/, '');
        const base = normalized.endsWith('/api/v1')
            ? normalized
            : `${normalized}/api/v1`;

        return [
            {
                source: '/api/v1/:path*',
                destination: `${base}/:path*`,
            },
        ];
    },
};

module.exports = nextConfig;
