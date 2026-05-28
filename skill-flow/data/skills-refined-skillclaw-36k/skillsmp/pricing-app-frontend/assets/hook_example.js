/**
 * Example custom hook following Pricing App patterns.
 * Shows: proper cleanup, dependencies, error handling.
 */
import { useState, useEffect, useCallback } from 'react';
import api from '@/services/api';

/**
 * Hook for server-side pagination with filters.
 * 
 * @param {string} endpoint - API endpoint to fetch from
 * @param {object} filters - Filter parameters
 * @param {number} pageSize - Items per page
 * @returns {object} Pagination state and controls
 */
export function useServerPagination(endpoint, filters = {}, pageSize = 50) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalItems, setTotalItems] = useState(0);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await api.get(endpoint, {
        params: {
          ...filters,
          page,
          page_size: pageSize
        }
      });

      setData(response.data.items || response.data);
      setTotalPages(response.data.total_pages || 1);
      setTotalItems(response.data.total_items || response.data.length);
    } catch (err) {
      setError(err.message || 'Error al cargar datos');
      console.error('Pagination error:', err);
    } finally {
      setLoading(false);
    }
  }, [endpoint, filters, page, pageSize]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const goToPage = (newPage) => {
    if (newPage >= 1 && newPage <= totalPages) {
      setPage(newPage);
    }
  };

  const nextPage = () => goToPage(page + 1);
  const prevPage = () => goToPage(page - 1);
  const refresh = () => fetchData();

  return {
    data,
    loading,
    error,
    page,
    totalPages,
    totalItems,
    goToPage,
    nextPage,
    prevPage,
    refresh,
    hasNextPage: page < totalPages,
    hasPrevPage: page > 1
  };
}

/**
 * Hook for debouncing values (e.g., search inputs).
 * 
 * @param {any} value - Value to debounce
 * @param {number} delay - Delay in ms
 * @returns {any} Debounced value
 */
export function useDebounce(value, delay = 500) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // Cleanup on unmount or value change
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

/**
 * Hook for keyboard navigation (arrow keys, enter, escape).
 * 
 * @param {object} options - Navigation options
 * @returns {object} Current index and handlers
 */
export function useKeyboardNavigation({ items, onSelect, onCancel }) {
  const [selectedIndex, setSelectedIndex] = useState(0);

  useEffect(() => {
    const handleKeyDown = (e) => {
      switch (e.key) {
        case 'ArrowDown':
          e.preventDefault();
          setSelectedIndex((prev) => 
            prev < items.length - 1 ? prev + 1 : prev
          );
          break;
        case 'ArrowUp':
          e.preventDefault();
          setSelectedIndex((prev) => (prev > 0 ? prev - 1 : prev));
          break;
        case 'Enter':
          e.preventDefault();
          if (items[selectedIndex]) {
            onSelect(items[selectedIndex]);
          }
          break;
        case 'Escape':
          e.preventDefault();
          if (onCancel) onCancel();
          break;
        default:
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    // Cleanup
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [items, selectedIndex, onSelect, onCancel]);

  return { selectedIndex, setSelectedIndex };
}
