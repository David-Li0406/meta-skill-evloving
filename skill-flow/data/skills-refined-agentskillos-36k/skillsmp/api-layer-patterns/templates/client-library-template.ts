/**
 * Client Library Template
 *
 * Copy this template when adding a new client-side API library.
 * Replace RESOURCE_NAME placeholders with your resource name.
 *
 * Location: lib/api/RESOURCE_NAME.ts
 *
 * NOTE: This is a documentation template. When implementing, use these imports:
 * - import { getInternalApiUrl, buildRESOURCE_NAMEQuery } from "@utils/api-helpers";
 *
 * The code below is wrapped in a namespace to prevent TypeScript errors
 * while still providing syntax highlighting and type checking guidance.
 */

export namespace ClientLibraryTemplate {
  // Type definitions - import from types/api/RESOURCE_NAME.ts in actual code
  export interface RESOURCE_NAMEParams {
    page?: number;
    size?: number;
    // Add other params
  }

  export interface RESOURCE_NAMEDTO {
    id: string;
    // Add other fields
  }

  export interface PagedResponse<T> {
    content: T[];
    totalElements: number;
    totalPages: number;
    currentPage: number;
    pageSize: number;
    last: boolean;
  }

  // These would be imported from @utils/api-helpers in actual code
  export function getInternalApiUrl(): string {
    // In actual code: import { getInternalApiUrl } from "@utils/api-helpers"
    return process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000";
  }

  export function buildRESOURCE_NAMEQuery(
    params: RESOURCE_NAMEParams
  ): URLSearchParams {
    // In actual code: import { buildRESOURCE_NAMEQuery } from "@utils/api-helpers"
    // Or create a new query builder following the pattern in api-helpers.ts
    const searchParams = new URLSearchParams();
    if (params.page !== undefined)
      searchParams.set("page", String(params.page));
    if (params.size !== undefined)
      searchParams.set("size", String(params.size));
    return searchParams;
  }

  /**
   * Fetch RESOURCE_NAME list from internal API
   *
   * Use this in pages/components. It calls the internal API route
   * which handles HMAC signing server-side.
   */
  export async function fetchRESOURCE_NAME(
    params: RESOURCE_NAMEParams = {}
  ): Promise<PagedResponse<RESOURCE_NAMEDTO>> {
    try {
      // Build query using centralized query builder
      const searchParams = buildRESOURCE_NAMEQuery(params);
      const queryString = searchParams.toString();

      // Call internal API route (NOT external API directly)
      const url = `${getInternalApiUrl()}/api/RESOURCE_NAME${
        queryString ? `?${queryString}` : ""
      }`;

      // IMPORTANT: When calling the internal API from a Server Component, use the standard `fetch` API.
      // You can include Next.js caching options like `next: { revalidate, tags }`.
      // For fetching within Client Components, a library like SWR is recommended.
      //
      // This template uses raw `fetch()` as it assumes a Server Component context.
      const response = await fetch(url, {
        next: { revalidate: 600, tags: ["RESOURCE_NAME"] },
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch RESOURCE_NAME: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error("[fetchRESOURCE_NAME] Error:", error);

      // Return safe fallback
      return {
        content: [],
        totalElements: 0,
        totalPages: 0,
        currentPage: 0,
        pageSize: 20,
        last: true,
      };
    }
  }

  /**
   * Fetch single RESOURCE_NAME by ID/slug
   */
  export async function fetchRESOURCE_NAMEBySlug(
    slug: string
  ): Promise<RESOURCE_NAMEDTO | null> {
    try {
      const url = `${getInternalApiUrl()}/api/RESOURCE_NAME/${encodeURIComponent(
        slug
      )}`;

      // Include ISR cache options for Next.js caching
      const response = await fetch(url, {
        next: { revalidate: 600, tags: ["RESOURCE_NAME", `RESOURCE_NAME-${slug}`] },
      });

      if (!response.ok) {
        if (response.status === 404) return null;
        throw new Error(`Failed to fetch RESOURCE_NAME: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error("[fetchRESOURCE_NAMEBySlug] Error:", error);
      return null;
    }
  }
}
