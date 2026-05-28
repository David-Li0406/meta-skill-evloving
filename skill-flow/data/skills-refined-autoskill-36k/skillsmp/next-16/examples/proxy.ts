// proxy.ts replaces middleware.ts in Next.js 16
// Runs on Node.js runtime (not Edge)

import { NextRequest, NextResponse } from 'next/server'

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Auth check
  if (pathname.startsWith('/dashboard')) {
    const token = request.cookies.get('auth-token')
    if (!token) {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  }

  // Rewrite example
  if (pathname === '/old-path') {
    return NextResponse.rewrite(new URL('/new-path', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/old-path'],
}
