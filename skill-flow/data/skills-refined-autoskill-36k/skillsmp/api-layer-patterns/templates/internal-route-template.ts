/**
 * Internal API Route Template
 *
 * Copy this template when adding a new internal API route.
 * Replace RESOURCE_NAME placeholders with your resource name.
 *
 * Location: app/api/RESOURCE_NAME/route.ts
 *
 * NOTE: This is a documentation template. When implementing, use these imports:
 * - import { NextResponse } from "next/server";
 * - import type { NextRequest } from "next/server";
 * - import { fetchRESOURCE_NAME } from "@lib/api/RESOURCE_NAME-external";
 */

// Mock types for template validation
type NextRequest = { url: string };
const NextResponse = {
  json: <T>(
    data: T,
    init?: { headers?: Record<string, string>; status?: number }
  ) => ({ data, ...init }),
};

// This would be imported from your external wrapper
declare function fetchRESOURCE_NAME(params: {
  page: number;
  size: number;
}): Promise<{
  content: unknown[];
  currentPage: number;
  pageSize: number;
  totalElements: number;
  totalPages: number;
  last: boolean;
}>;

// Cache configuration - adjust TTL based on data freshness needs
const CACHE_MAX_AGE = 600; // 10 minutes
const STALE_WHILE_REVALIDATE = 300; // 5 minutes

export async function GET(request: NextRequest) {
  try {
    // Extract query parameters with safe parsing
    // Note: Number("abc") returns NaN, so || 0 provides fallback
    const { searchParams } = new URL(request.url);
    const rawPage = searchParams.get("page");
    const rawSize = searchParams.get("size");

    // Parse with fallbacks - Number(null) = 0, Number("abc") = NaN
    const page = rawPage ? Number(rawPage) || 0 : 0;
    const size = rawSize ? Number(rawSize) || 20 : 20;
    // Add more params as needed

    // Call external wrapper (handles HMAC signing)
    const data = await fetchRESOURCE_NAME({
      page,
      size,
      // Pass other params
    });

    // Return with cache headers
    return NextResponse.json(data, {
      headers: {
        "Cache-Control": `public, s-maxage=${CACHE_MAX_AGE}, stale-while-revalidate=${STALE_WHILE_REVALIDATE}`,
      },
    });
  } catch (error) {
    console.error("[API] RESOURCE_NAME fetch error:", error);

    // Return safe fallback for read endpoints
    return NextResponse.json(
      {
        content: [],
        currentPage: 0,
        pageSize: 20,
        totalElements: 0,
        totalPages: 0,
        last: true,
      },
      { status: 200 } // Don't fail - return empty data
    );
  }
}
