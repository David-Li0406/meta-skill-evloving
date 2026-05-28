'use client';

import { useCallback, useEffect, useRef, useState, useTransition } from 'react';
import { getFeed } from '@/app/(platform)/services/wall.service';

// Helper to get initial page from URL
function getInitialPageFromUrl(): number {
    if (typeof window === 'undefined') return 1;
    const params = new URLSearchParams(window.location.search);
    const pageParam = params.get('page');
    const page = pageParam ? parseInt(pageParam, 10) : 1;
    return Number.isNaN(page) || page < 1 ? 1 : page;
}

// Helper to update URL silently without navigation
function updateUrlWithPage(page: number) {
    if (typeof window === 'undefined') return;
    const url = new URL(window.location.href);
    if (page > 1) {
        url.searchParams.set('page', String(page));
    } else {
        url.searchParams.delete('page');
    }
    window.history.pushState({}, '', url.toString());
}

// Page-based pagination meta
export interface FeedMeta {
    total: number;
    page: number;
    lastPage: number;
    hasNextPage: boolean;
}

export interface UseWallFeedOptions {
    initialItems?: any[];
    initialMeta?: FeedMeta;
    // Legacy cursor-based options
    initialNextCursor?: string | null;
    initialHasNextPage?: boolean;
    debounceMs?: number;
}

export interface UseWallFeedResult {
    feed: any[];
    isLoading: boolean;
    isLoadingMore: boolean;
    nextCursor: string | null;
    hasMore: boolean;
    searchTerm: string;
    setSearchTerm: (value: string) => void;
    refresh: () => Promise<void>;
    loadMore: () => Promise<void>;
}

type ParsedFeedResponse = {
    items: any[];
    nextCursor: string | null;
    hasNextPage: boolean;
    // New page-based fields
    page?: number;
    lastPage?: number;
    total?: number;
};

function parseFeedResponse(data: any): ParsedFeedResponse {
    // Support both new format (data) and legacy format (items)
    const items =
        (Array.isArray(data?.data) && data.data) ||
        (Array.isArray(data?.items) && data.items) ||
        (Array.isArray(data?.data?.items) && data.data.items) ||
        (Array.isArray(data?.feed?.items) && data.feed.items) ||
        (Array.isArray(data?.feed) && data.feed) ||
        (Array.isArray(data) && data) ||
        [];

    // Support new meta format
    const meta = data?.meta;

    // Legacy pageInfo format
    const pageInfo =
        (data?.pageInfo && data.pageInfo) ||
        (data?.data?.pageInfo && data.data.pageInfo) ||
        (data?.feed?.pageInfo && data.feed.pageInfo) ||
        null;

    const nextCursor = pageInfo && typeof pageInfo?.nextCursor === 'string' ? pageInfo.nextCursor : null;
    const hasNextPage = meta?.hasNextPage ?? Boolean(pageInfo?.hasNextPage);

    return {
        items: Array.isArray(items) ? items : [],
        nextCursor,
        hasNextPage,
        page: meta?.page,
        lastPage: meta?.lastPage,
        total: meta?.total,
    };
}

export function useWallFeed({
    initialItems = [],
    initialMeta,
    initialNextCursor = null,
    initialHasNextPage = false,
    debounceMs = 320,
}: UseWallFeedOptions = {}): UseWallFeedResult {
    const [searchTerm, setSearchTerm] = useState('');
    const [feed, setFeed] = useState<any[]>(Array.isArray(initialItems) ? initialItems : []);
    const [isLoading, setIsLoading] = useState(false);
    const [isLoadingMore, setIsLoadingMore] = useState(false);
    const [nextCursor, setNextCursor] = useState<string | null>(initialNextCursor);

    // useTransition for non-blocking UI during Load More
    const [isPending, startTransition] = useTransition();

    // Page-based pagination state - initialize from URL if available
    const [currentPage, setCurrentPage] = useState(() => {
        const urlPage = getInitialPageFromUrl();
        return urlPage > 1 ? urlPage : (initialMeta?.page ?? 1);
    });
    const [hasMore, setHasMore] = useState(
        initialMeta?.hasNextPage ?? Boolean(initialHasNextPage && initialNextCursor)
    );

    const didInitFetchRef = useRef(false);

    const refresh = useCallback(async () => {
        setIsLoading(true);
        try {
            const normalizedSearch = searchTerm.trim();
            const params: Record<string, any> = {};
            if (normalizedSearch) params.search = normalizedSearch;

            const data = await getFeed(params);
            const parsed = parseFeedResponse(data);

            setFeed(parsed.items);
            setNextCursor(parsed.nextCursor);
            setHasMore(Boolean(parsed.hasNextPage && parsed.nextCursor));
        } catch (error) {
            console.error('useWallFeed.refresh error:', error);
        } finally {
            setIsLoading(false);
        }
    }, [searchTerm]);

    const loadMore = useCallback(async () => {
        if (!hasMore || isLoadingMore || isPending) return;

        setIsLoadingMore(true);
        try {
            const normalizedSearch = searchTerm.trim();
            const nextPage = currentPage + 1;

            // Use page-based pagination (preferred) or fallback to cursor
            const params: Record<string, any> = {
                page: nextPage,
                limit: 10
            };
            if (nextCursor) params.cursor = nextCursor;
            if (normalizedSearch) params.search = normalizedSearch;

            const data = await getFeed(params);
            const parsed = parseFeedResponse(data);

            // Use startTransition for non-blocking state updates
            startTransition(() => {
                setNextCursor(parsed.nextCursor);
                setCurrentPage(parsed.page ?? nextPage);
                setHasMore(parsed.hasNextPage);

                // Update URL silently with new page number for shareable links
                updateUrlWithPage(parsed.page ?? nextPage);

                if (parsed.items.length > 0) {
                    setFeed((prev) => {
                        const seen = new Set(prev.map((item) => String(item?.id ?? '')));
                        const merged = [...prev];
                        for (const item of parsed.items) {
                            const id = String(item?.id ?? '');
                            if (!id || seen.has(id)) continue;
                            seen.add(id);
                            merged.push(item);
                        }
                        return merged;
                    });
                }
            });
        } catch (error) {
            console.error('useWallFeed.loadMore error:', error);
        } finally {
            setIsLoadingMore(false);
        }
    }, [hasMore, isLoadingMore, isPending, nextCursor, searchTerm, currentPage]);

    useEffect(() => {
        const handler = (event: Event) => {
            const customEvent = event as CustomEvent<unknown>;
            const detail = customEvent.detail;
            if (!detail || typeof detail !== 'object') return;

            const record = detail as Record<string, unknown>;
            const status = record.status;
            const optimisticId = record.optimisticId;

            if (typeof status !== 'string' || typeof optimisticId !== 'string') return;

            if (status === 'optimistic') {
                const item = record.item;
                if (!item) return;
                setFeed((prev) => [item as any, ...prev]);
                return;
            }

            if (status === 'confirmed') {
                const item = record.item;
                if (!item) return;

                setFeed((prev) => {
                    const index = prev.findIndex((existing) => String(existing?.id) === optimisticId);
                    if (index === -1) return [item as any, ...prev];
                    const next = [...prev];
                    next[index] = item as any;
                    return next;
                });
                return;
            }

            if (status === 'failed') {
                setFeed((prev) => prev.filter((existing) => String(existing?.id) !== optimisticId));
            }
        };

        window.addEventListener('sociopulse:wall:feed-item', handler as EventListener);
        return () => window.removeEventListener('sociopulse:wall:feed-item', handler as EventListener);
    }, []);

    useEffect(() => {
        if (searchTerm.trim()) return;
        setFeed(Array.isArray(initialItems) ? initialItems : []);
        setNextCursor(initialNextCursor);
        setHasMore(Boolean(initialHasNextPage && initialNextCursor));
    }, [initialHasNextPage, initialItems, initialNextCursor, searchTerm]);

    useEffect(() => {
        const hasInitial = Array.isArray(initialItems) && initialItems.length > 0;
        const hasQuery = Boolean(searchTerm.trim());

        if (!didInitFetchRef.current) {
            didInitFetchRef.current = true;

            if (hasInitial && !hasQuery) return;
        }

        const timeout = window.setTimeout(() => {
            refresh();
        }, debounceMs);

        return () => window.clearTimeout(timeout);
    }, [debounceMs, initialItems, refresh, searchTerm]);

    return {
        feed,
        isLoading,
        isLoadingMore,
        nextCursor,
        hasMore,
        searchTerm,
        setSearchTerm,
        refresh,
        loadMore,
    };
}

