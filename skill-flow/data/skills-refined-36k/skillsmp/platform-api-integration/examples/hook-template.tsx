/**
 * API Hook Template
 *
 * This template provides the standard pattern for creating SWR-based API hooks
 * in the Squareone application. Copy this template and customize it for your
 * specific API endpoint.
 *
 * Replace:
 * - YourApiHook -> Your hook name (e.g., useUserTokens)
 * - YourResponseType -> Your response type (e.g., TokenInfo[])
 * - /api/v1/your-endpoint -> Your actual endpoint path
 */

import React from 'react';
import useSWR from 'swr';

// =============================================================================
// Type Definitions
// =============================================================================

/**
 * Response type based on OpenAPI schema
 *
 * Use WebFetch to download the OpenAPI spec and extract the response schema:
 * WebFetch({
 *   url: 'https://service.lsst.io/_static/openapi.json',
 *   prompt: 'Show me the response schema for this endpoint'
 * })
 */
type YourResponseType = {
  id: string;
  name: string;
  created_at?: string;
  // ... add all fields from OpenAPI schema
};

/**
 * Hook return type
 *
 * Standard return type for all API hooks
 */
type UseYourApiHookResult = {
  /** Response data (undefined during initial load) */
  data: YourResponseType | undefined;
  /** True during initial data fetch */
  isLoading: boolean;
  /** Error object if request failed */
  error: Error | undefined;
  /** Function to manually revalidate the data */
  mutate: () => void;
};

// =============================================================================
// Fetcher Function
// =============================================================================

/**
 * Standard fetcher with error handling
 *
 * Handles HTTP errors and parses responses
 */
const fetcher = async (...args: Parameters<typeof fetch>) => {
  const response = await fetch(...args);

  if (!response.ok) {
    // Try to parse error response
    const errorData = await response.json().catch(() => ({}));
    throw parseError(response, errorData);
  }

  return response.json();
};

/**
 * Type for Pydantic validation error detail
 */
type PydanticErrorDetail = {
  msg: string;
  loc?: (string | number)[];
  type?: string;
};

/**
 * Parse API errors into user-friendly messages
 *
 * Handles common error formats:
 * - Pydantic validation errors (array of errors)
 * - Simple error messages (detail string)
 * - HTTP status codes
 */
function parseError(response: Response, data: unknown): Error {
  // Handle Pydantic validation errors (FastAPI)
  if (
    typeof data === 'object' &&
    data !== null &&
    'detail' in data &&
    Array.isArray(data.detail)
  ) {
    const errors = data.detail
      .map((err: PydanticErrorDetail) => err.msg)
      .join(', ');
    return new Error(errors);
  }

  // Handle simple error messages
  if (
    typeof data === 'object' &&
    data !== null &&
    'detail' in data &&
    typeof data.detail === 'string'
  ) {
    return new Error(data.detail);
  }

  if (
    typeof data === 'object' &&
    data !== null &&
    'message' in data &&
    typeof data.message === 'string'
  ) {
    return new Error(data.message);
  }

  // Fallback to HTTP status
  return new Error(`HTTP ${response.status}: ${response.statusText}`);
}

// =============================================================================
// Hook Implementation
// =============================================================================

/**
 * Custom hook for fetching [description of what this endpoint does]
 *
 * Usage:
 * ```typescript
 * const { data, isLoading, error, mutate } = useYourApiHook();
 *
 * if (isLoading) return <div>Loading...</div>;
 * if (error) return <div>Error: {error.message}</div>;
 * if (!data) return null;
 *
 * return <div>{data.name}</div>;
 * ```
 *
 * @returns Hook result with data, loading state, error, and mutate function
 */
export function useYourApiHook(): UseYourApiHookResult {
  const { data, error, isLoading, mutate } = useSWR<YourResponseType>(
    '/api/v1/your-endpoint', // Replace with actual endpoint
    fetcher,
    {
      // Standard configuration
      revalidateOnFocus: true, // Refresh when window gains focus
      revalidateOnReconnect: true, // Refresh on network recovery
      dedupingInterval: 10000, // Cache for 10 seconds

      // Optional: Adjust based on data characteristics
      // revalidateIfStale: false,   // Don't revalidate stale data
      // refreshInterval: 0,          // Disable polling
      // errorRetryCount: 3,          // Retry failed requests
    }
  );

  return {
    data,
    isLoading,
    error,
    mutate,
  };
}

// =============================================================================
// Hook with Parameters
// =============================================================================

/**
 * Custom hook with URL parameters
 *
 * Use this pattern when the endpoint requires path or query parameters
 */
type UseYourApiHookWithParamsResult = {
  data: YourResponseType | undefined;
  isLoading: boolean;
  error: Error | undefined;
  mutate: () => void;
};

export function useYourApiHookWithParams(
  id: string,
  options?: { enabled?: boolean }
): UseYourApiHookWithParamsResult {
  // Conditionally fetch based on parameters
  const shouldFetch = options?.enabled !== false && id !== '';

  const { data, error, isLoading, mutate } = useSWR<YourResponseType>(
    shouldFetch ? `/api/v1/your-endpoint/${id}` : null, // null disables fetching
    fetcher,
    {
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
      dedupingInterval: 10000,
    }
  );

  return {
    data,
    isLoading: shouldFetch ? isLoading : false,
    error,
    mutate,
  };
}

// =============================================================================
// Hook with Query Parameters
// =============================================================================

/**
 * Custom hook with query parameters
 *
 * Use this pattern for endpoints that accept query string parameters
 */
export function useYourApiHookWithQuery(params: {
  filter?: string;
  limit?: number;
  offset?: number;
}): UseYourApiHookWithParamsResult {
  // Build query string
  const queryString = new URLSearchParams();
  if (params.filter) queryString.set('filter', params.filter);
  if (params.limit) queryString.set('limit', String(params.limit));
  if (params.offset) queryString.set('offset', String(params.offset));

  const url = `/api/v1/your-endpoint?${queryString.toString()}`;

  const { data, error, isLoading, mutate } = useSWR<YourResponseType>(
    url,
    fetcher,
    {
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
      dedupingInterval: 10000,
    }
  );

  return {
    data,
    isLoading,
    error,
    mutate,
  };
}

// =============================================================================
// Hook with Polling
// =============================================================================

/**
 * Custom hook with polling for status endpoints
 *
 * Use this pattern for endpoints that track operation status
 */
export function useYourApiHookWithPolling(
  id: string,
  enabled: boolean = true
): UseYourApiHookWithParamsResult {
  const { data, error, isLoading, mutate } = useSWR<YourResponseType>(
    enabled ? `/api/v1/your-endpoint/${id}/status` : null,
    fetcher,
    {
      refreshInterval: enabled ? 1000 : 0, // Poll every 1 second when enabled
      revalidateOnFocus: false, // Don't revalidate on focus during polling
      revalidateOnReconnect: true,
    }
  );

  return {
    data,
    isLoading,
    error,
    mutate,
  };
}

// =============================================================================
// Mutation Hook (POST/PUT/DELETE)
// =============================================================================

/**
 * Request payload type
 */
type YourMutationPayload = {
  name: string;
  value: string;
  // ... add fields based on OpenAPI schema
};

/**
 * Error type for mutations
 */
type YourMutationError = {
  type: 'validation' | 'network' | 'server';
  message: string;
  statusCode?: number;
  details?: unknown;
};

/**
 * Mutation result type
 */
type MutationResult = {
  success: boolean;
  data?: YourResponseType;
  error?: YourMutationError;
};

/**
 * Custom hook for mutations (POST/PUT/DELETE)
 *
 * Usage:
 * ```typescript
 * const { mutate, isLoading } = useYourMutation();
 *
 * const handleSubmit = async () => {
 *   const result = await mutate({ name: 'test', value: 'data' });
 *   if (result.success) {
 *     console.log('Success:', result.data);
 *   } else {
 *     console.error('Error:', result.error);
 *   }
 * };
 * ```
 */
export function useYourMutation() {
  const [isLoading, setIsLoading] = React.useState(false);

  const mutate = async (
    payload: YourMutationPayload
  ): Promise<MutationResult> => {
    setIsLoading(true);

    try {
      const response = await fetch('/api/v1/your-endpoint', {
        method: 'POST', // or 'PUT', 'DELETE'
        headers: {
          'Content-Type': 'application/json',
          // For Gafaelfawr mutations, include CSRF token:
          // 'x-csrf-token': csrfToken,
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const error = parseError(response, errorData);

        return {
          success: false,
          error: {
            type: response.status >= 500 ? 'server' : 'validation',
            message: error.message,
            statusCode: response.status,
            details: errorData,
          },
        };
      }

      const data = await response.json();

      return {
        success: true,
        data,
      };
    } catch (error) {
      return {
        success: false,
        error: {
          type: 'network',
          message: error instanceof Error ? error.message : 'Network error',
        },
      };
    } finally {
      setIsLoading(false);
    }
  };

  return {
    mutate,
    isLoading,
  };
}

// =============================================================================
// Hook with CSRF Token (Gafaelfawr Mutations)
// =============================================================================

/**
 * Custom hook for Gafaelfawr mutations requiring CSRF token
 *
 * Requires useLoginInfo to get CSRF token
 */
export function useYourGafaelfawrMutation() {
  const [isLoading, setIsLoading] = React.useState(false);

  // Get CSRF token from login endpoint
  // Note: You'll need to import this hook
  // import { useLoginInfo } from './useLoginInfo';
  // const { data: loginData } = useLoginInfo();
  // const csrfToken = loginData?.csrf;

  const mutate = async (
    payload: YourMutationPayload,
    csrfToken: string
  ): Promise<MutationResult> => {
    setIsLoading(true);

    try {
      const response = await fetch('/auth/api/v1/your-endpoint', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-csrf-token': csrfToken, // For POST
          // 'X-CSRF-Token': csrfToken, // For DELETE
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const error = parseError(response, errorData);

        return {
          success: false,
          error: {
            type: response.status >= 500 ? 'server' : 'validation',
            message: error.message,
            statusCode: response.status,
            details: errorData,
          },
        };
      }

      const data = await response.json();

      return {
        success: true,
        data,
      };
    } catch (error) {
      return {
        success: false,
        error: {
          type: 'network',
          message: error instanceof Error ? error.message : 'Network error',
        },
      };
    } finally {
      setIsLoading(false);
    }
  };

  return {
    mutate,
    isLoading,
  };
}

// =============================================================================
// Usage Examples
// =============================================================================

/**
 * Example component using the hook
 */
export function ExampleComponent() {
  const { data, isLoading, error, mutate } = useYourApiHook();

  // Handle loading state
  if (isLoading) {
    return <div>Loading...</div>;
  }

  // Handle error state
  if (error) {
    return (
      <div>
        <p>Error: {error.message}</p>
        <button type="button" onClick={() => mutate()}>
          Retry
        </button>
      </div>
    );
  }

  // Handle no data
  if (!data) {
    return <div>No data available</div>;
  }

  // Render data
  return (
    <div>
      <h1>{data.name}</h1>
      <button type="button" onClick={() => mutate()}>
        Refresh
      </button>
    </div>
  );
}

/**
 * Example component with mutation
 */
export function ExampleMutationComponent() {
  const { mutate, isLoading } = useYourMutation();
  const [result, setResult] = React.useState<MutationResult | null>(null);

  const handleSubmit = async () => {
    const result = await mutate({
      name: 'Test',
      value: 'Example',
    });
    setResult(result);
  };

  return (
    <div>
      <button type="button" onClick={handleSubmit} disabled={isLoading}>
        {isLoading ? 'Submitting...' : 'Submit'}
      </button>

      {result?.success && <p>Success! {result.data?.name}</p>}
      {result?.error && <p>Error: {result.error.message}</p>}
    </div>
  );
}
