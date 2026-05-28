import { User, FileText, Package } from 'lucide-react';
import type { SearchResultItem } from './mock-api';

export interface ApiResultProps {
  item: SearchResultItem;
  query: string;
}

export function ApiResult({ item, query }: ApiResultProps) {
  return (
    <div className="flex items-start gap-3 px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
      {/* Icon based on type */}
      <div className="flex-shrink-0 mt-1">
        {item.type === 'user' && (
          <div className="w-10 h-10 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
            {item.avatar ? (
              <img
                src={item.avatar}
                alt={item.title}
                className="w-10 h-10 rounded-full object-cover"
              />
            ) : (
              <User className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            )}
          </div>
        )}
        {item.type === 'post' && (
          <div className="w-10 h-10 rounded-full bg-green-100 dark:bg-green-900 flex items-center justify-center">
            <FileText className="w-5 h-5 text-green-600 dark:text-green-400" />
          </div>
        )}
        {item.type === 'product' && (
          <div className="w-10 h-10 rounded-full bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
            <Package className="w-5 h-5 text-purple-600 dark:text-purple-400" />
          </div>
        )}
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        {/* Title with highlighting */}
        <div className="font-medium text-gray-900 dark:text-gray-100 truncate">
          <HighlightedText text={item.title} query={query} />
        </div>

        {/* Description */}
        {item.description && (
          <div className="mt-1 text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
            <HighlightedText text={item.description} query={query} />
          </div>
        )}

        {/* Metadata */}
        <div className="mt-2 flex items-center gap-3 text-xs text-gray-500 dark:text-gray-500">
          {/* Type badge */}
          <span className="px-2 py-0.5 bg-gray-100 dark:bg-gray-800 rounded capitalize">
            {item.type}
          </span>

          {/* Date */}
          {item.date && (
            <span>{new Date(item.date).toLocaleDateString()}</span>
          )}

          {/* Tags */}
          {item.tags && item.tags.length > 0 && (
            <div className="flex items-center gap-1">
              {item.tags.slice(0, 3).map((tag) => (
                <span
                  key={tag}
                  className="px-1.5 py-0.5 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded"
                >
                  {tag}
                </span>
              ))}
              {item.tags.length > 3 && (
                <span className="text-gray-400">+{item.tags.length - 3}</span>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Relevance score (optional) */}
      {item.relevanceScore !== undefined && (
        <div className="flex-shrink-0 text-xs font-medium text-gray-400">
          {Math.round(item.relevanceScore * 100)}%
        </div>
      )}
    </div>
  );
}

/**
 * Highlights matching terms in text
 */
function HighlightedText({ text, query }: { text: string; query: string }) {
  if (!query.trim()) {
    return <>{text}</>;
  }

  // Split query into words and create case-insensitive regex
  const terms = query
    .trim()
    .split(/\s+/)
    .filter((term) => term.length > 0);

  if (terms.length === 0) {
    return <>{text}</>;
  }

  // Create regex that matches any of the query terms
  const regex = new RegExp(`(${terms.map(escapeRegex).join('|')})`, 'gi');
  const parts = text.split(regex);

  return (
    <>
      {parts.map((part, i) => {
        const isMatch = terms.some(
          (term) => part.toLowerCase() === term.toLowerCase()
        );
        return isMatch ? (
          <mark
            key={i}
            className="bg-yellow-200 dark:bg-yellow-900 text-gray-900 dark:text-gray-100"
          >
            {part}
          </mark>
        ) : (
          <span key={i}>{part}</span>
        );
      })}
    </>
  );
}

/**
 * Escape special regex characters
 */
function escapeRegex(str: string): string {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
