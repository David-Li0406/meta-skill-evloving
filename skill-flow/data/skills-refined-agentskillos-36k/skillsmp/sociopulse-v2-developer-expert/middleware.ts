import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { jwtVerify } from 'jose';

type TokenCheckResult = {
    valid: boolean;
    role?: string;
};

const ADMIN_PREFIX = '/admin';
const DASH_SUBDOMAIN_PREFIX = 'dash.';
const AUTH_PATH_PREFIXES = ['/auth', '/onboarding'];
const JWT_SECRET = process.env.JWT_SECRET;

if (!JWT_SECRET) {
    throw new Error('JWT_SECRET is required');
}

// V2 Protected Routes - Role-based dashboards
const PLATFORM_PROTECTED_PATHS = [
    '/dashboard/client',
    '/dashboard/talent',
    '/bookings',
    '/messages',
    '/finance',
    '/settings',
    '/notifications',
    '/fil-pro',
];

function isAuthPath(pathname: string) {
    return AUTH_PATH_PREFIXES.some((prefix) => pathname.startsWith(prefix));
}

async function verifyToken(token?: string): Promise<TokenCheckResult> {
    if (!token) return { valid: false };

    try {
        const secret = new TextEncoder().encode(JWT_SECRET);
        const { payload } = await jwtVerify(token, secret);
        return {
            valid: true,
            role: typeof payload.role === 'string' ? payload.role : undefined,
        };
    } catch {
        return { valid: false };
    }
}

export async function middleware(request: NextRequest) {
    const { pathname } = request.nextUrl;
    const hostname = request.nextUrl.hostname;
    const token = request.cookies.get('accessToken')?.value;

    const tokenCheck = await verifyToken(token);
    const role = tokenCheck.role?.toUpperCase();
    const isAdmin = role === 'ADMIN';
    const isClientOrTalent = role === 'CLIENT' || role === 'TALENT';

    const loginUrl = new URL('/auth/login', request.url);

    // === Mode Production: dash.sociopulse.com ===
    if (hostname.startsWith(DASH_SUBDOMAIN_PREFIX)) {
        if (isAuthPath(pathname)) {
            if (tokenCheck.valid && isAdmin) {
                return NextResponse.redirect(new URL('/admin', request.url));
            }
            return NextResponse.next();
        }

        if (!tokenCheck.valid || !isAdmin) {
            const response = NextResponse.redirect(loginUrl);
            if (token) response.cookies.delete('accessToken');
            return response;
        }

        const adminPath = pathname.startsWith(ADMIN_PREFIX)
            ? pathname
            : `${ADMIN_PREFIX}${pathname === '/' ? '' : pathname}`;

        if (adminPath !== pathname) {
            const url = request.nextUrl.clone();
            url.pathname = adminPath;
            return NextResponse.rewrite(url);
        }

        return NextResponse.next();
    }

    // === Mode Temporaire: URL unique / coolify ===
    // V2: Role-based redirect when authenticated user visits auth pages
    if (isAuthPath(pathname)) {
        if (tokenCheck.valid) {
            let target = '/';
            if (isAdmin) {
                target = '/admin';
            } else if (role === 'CLIENT') {
                target = '/dashboard/client';
            } else if (role === 'TALENT') {
                target = '/dashboard/talent';
            }
            return NextResponse.redirect(new URL(target, request.url));
        }
        return NextResponse.next();
    }

    if (pathname.startsWith(ADMIN_PREFIX)) {
        if (!tokenCheck.valid || !isAdmin) {
            const response = NextResponse.redirect(loginUrl);
            if (token) response.cookies.delete('accessToken');
            return response;
        }
        return NextResponse.next();
    }

    if (pathname.startsWith('/dashboard/client')) {
        if (!tokenCheck.valid) {
            const response = NextResponse.redirect(loginUrl);
            if (token) response.cookies.delete('accessToken');
            return response;
        }
        if (role !== 'CLIENT') {
            const target = isAdmin ? '/admin' : role === 'TALENT' ? '/dashboard/talent' : '/';
            return NextResponse.redirect(new URL(target, request.url));
        }
    }

    if (pathname.startsWith('/dashboard/talent')) {
        if (!tokenCheck.valid) {
            const response = NextResponse.redirect(loginUrl);
            if (token) response.cookies.delete('accessToken');
            return response;
        }
        if (role !== 'TALENT') {
            const target = isAdmin ? '/admin' : role === 'CLIENT' ? '/dashboard/client' : '/';
            return NextResponse.redirect(new URL(target, request.url));
        }
    }

    if (PLATFORM_PROTECTED_PATHS.some((route) => pathname.startsWith(route))) {
        if (!tokenCheck.valid || (!isClientOrTalent && !isAdmin)) {
            const response = NextResponse.redirect(loginUrl);
            if (token) response.cookies.delete('accessToken');
            return response;
        }
    }

    return NextResponse.next();
}

export const config = {
    matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
