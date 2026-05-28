/**
 * Events API Example
 *
 * This example shows the complete three-layer pattern implementation
 * for the events API. Use this as a reference when implementing new APIs.
 *
 * NOTE: This is a documentation example. The actual implementation lives in:
 * - lib/api/events.ts (client library)
 * - app/api/events/route.ts (internal route)
 * - lib/api/events-external.ts (external wrapper)
 */

// =============================================================================
// Layer 1: Client Library (lib/api/events.ts)
// Called by pages/components - uses internal API routes
// =============================================================================

/*
import { getInternalApiUrl, buildEventsQuery } from "@utils/api-helpers";
import type { EventResponseDTO, PagedResponseDTO } from "@/types/api/event";

interface EventsParams {
  page?: number;
  size?: number;
  place?: string;
  category?: string;
  from?: string;
  to?: string;
}

export async function fetchEvents(
  params: EventsParams = {}
): Promise<PagedResponseDTO<EventResponseDTO>> {
  try {
    // Use centralized query builder
    const searchParams = buildEventsQuery(params);
    const queryString = searchParams.toString();

    // Call INTERNAL route, not external API
    const url = `${getInternalApiUrl()}/api/events${
      queryString ? `?${queryString}` : ""
    }`;

    const response = await fetch(url, {
      next: { revalidate: 600, tags: ["events"] },
    });

    if (!response.ok) {
      throw new Error(`Events API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("[fetchEvents] Error:", error);
    return { content: [], currentPage: 0, pageSize: 20, totalElements: 0, totalPages: 0, last: true };
  }
}
*/

// =============================================================================
// Layer 2: Internal API Route (app/api/events/route.ts)
// Handles caching headers, calls external wrapper
// =============================================================================

/*
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { fetchEventsExternal } from "@lib/api/events-external";

const CACHE_MAX_AGE = 600;
const STALE_WHILE_REVALIDATE = 300;

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);

  const data = await fetchEventsExternal({
    page: parseInt(searchParams.get("page") || "0", 10),
    size: parseInt(searchParams.get("size") || "20", 10),
    place: searchParams.get("place") || undefined,
    category: searchParams.get("category") || undefined,
  });

  return NextResponse.json(data, {
    headers: {
      "Cache-Control": `public, s-maxage=${CACHE_MAX_AGE}, stale-while-revalidate=${STALE_WHILE_REVALIDATE}`,
    },
  });
}
*/

// =============================================================================
// Layer 3: External Wrapper (lib/api/events-external.ts)
// Handles HMAC signing, Sentry logging, safe fallbacks
// =============================================================================

/*
import { fetchWithHmac } from "@lib/api/fetch-wrapper";
import { captureException } from "@sentry/nextjs";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

interface EventsExternalParams {
  page?: number;
  size?: number;
  place?: string;
  category?: string;
}

export async function fetchEventsExternal(params: EventsExternalParams = {}) {
  // Environment guard
  if (!API_URL) {
    return { content: [], currentPage: 0, pageSize: 20, totalElements: 0, totalPages: 0, last: true };
  }

  try {
    const searchParams = new URLSearchParams();
    if (params.page != null) searchParams.set("page", String(params.page));
    if (params.size != null) searchParams.set("size", String(params.size));
    if (params.place) searchParams.set("place", params.place);
    if (params.category) searchParams.set("category", params.category);

    const url = `${API_URL}/api/events?${searchParams}`;
    const response = await fetchWithHmac(url);

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    captureException(error, { tags: { api: "events" }, extra: { params } });
    return { content: [], currentPage: 0, pageSize: 20, totalElements: 0, totalPages: 0, last: true };
  }
}
*/

// =============================================================================
// Usage in a Server Component
// =============================================================================

/*
// app/[place]/page.tsx
import { fetchEvents } from "@lib/api/events";

export default async function PlacePage({ params }) {
  const { place } = await params;

  // This calls the internal API route, which handles HMAC
  const events = await fetchEvents({ place, page: 0, size: 20 });

  return (
    <div>
      <h1>Events in {place}</h1>
      <EventsList events={events.content} />
    </div>
  );
}
*/
