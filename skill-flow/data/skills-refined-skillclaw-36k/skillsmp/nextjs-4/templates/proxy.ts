/**
 * Next.js 16 Proxy Template
 *
 * Usage:
 * 1. Copy this file to app/proxy.ts
 * 2. Configure protected and public paths
 * 3. Adjust cookie name for your auth provider
 */

import { NextRequest, NextResponse } from "next/server";

// === CONFIGURATION ===

// Paths that don't require authentication
const PUBLIC_PATHS = [
  "/",
  "/login",
  "/register",
  "/forgot-password",
  "/reset-password",
  "/api/auth", // Better Auth routes
];

// Paths that require authentication
const PROTECTED_PATHS = [
  "/dashboard",
  "/settings",
  "/profile",
  "/api/tasks",
  "/api/user",
];

// Cookie name for session (adjust for your auth provider)
const SESSION_COOKIE = "better-auth.session_token";

// === HELPERS ===

function matchesPath(pathname: string, paths: string[]): boolean {
  return paths.some(
    (path) => pathname === path || pathname.startsWith(`${path}/`)
  );
}

function isPublicPath(pathname: string): boolean {
  return matchesPath(pathname, PUBLIC_PATHS);
}

function isProtectedPath(pathname: string): boolean {
  return matchesPath(pathname, PROTECTED_PATHS);
}

function isAuthPage(pathname: string): boolean {
  return pathname === "/login" || pathname === "/register";
}

// === PROXY FUNCTION ===

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Get session token
  const sessionToken = request.cookies.get(SESSION_COOKIE);
  const isAuthenticated = !!sessionToken;

  // Redirect authenticated users away from auth pages
  if (isAuthenticated && isAuthPage(pathname)) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  // Redirect unauthenticated users to login for protected paths
  if (!isAuthenticated && isProtectedPath(pathname)) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("callbackUrl", pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Add security headers
  const response = NextResponse.next();
  response.headers.set("X-Frame-Options", "DENY");
  response.headers.set("X-Content-Type-Options", "nosniff");
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");

  return response;
}

// === MATCHER CONFIG ===

export const config = {
  matcher: [
    // Match all paths except static files and images
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
