import type { Route } from './mock-routes';
import { getBreadcrumbs, mockRoutes } from './mock-routes';

interface RouteResultProps {
  route: Route;
  isRecent?: boolean;
  searchQuery?: string;
}

/**
 * Highlight matching characters in text
 */
function highlightText(text: string, query: string): React.ReactNode {
  if (!query) return text;

  const lowerText = text.toLowerCase();
  const lowerQuery = query.toLowerCase();
  const result: React.ReactNode[] = [];

  let queryIndex = 0;
  let lastIndex = 0;

  for (let i = 0; i < text.length && queryIndex < lowerQuery.length; i++) {
    if (lowerText[i] === lowerQuery[queryIndex]) {
      // Add text before match
      if (i > lastIndex) {
        result.push(
          <span key={`text-${lastIndex}`}>{text.substring(lastIndex, i)}</span>
        );
      }

      // Add highlighted match
      result.push(
        <mark
          key={`mark-${i}`}
          className="bg-yellow-200 dark:bg-yellow-900/50 text-inherit rounded-sm px-0.5"
        >
          {text[i]}
        </mark>
      );

      queryIndex++;
      lastIndex = i + 1;
    }
  }

  // Add remaining text
  if (lastIndex < text.length) {
    result.push(<span key={`text-${lastIndex}`}>{text.substring(lastIndex)}</span>);
  }

  return result.length > 0 ? <>{result}</> : text;
}

/**
 * Route result item component for navigation palette
 */
export function RouteResult({ route, isRecent = false, searchQuery = '' }: RouteResultProps) {
  const breadcrumbs = getBreadcrumbs(route.id, mockRoutes);
  const showBreadcrumbs = breadcrumbs.length > 1;

  // Get section color
  const sectionColors: Record<Route['section'], string> = {
    App: 'text-blue-600 dark:text-blue-400',
    Settings: 'text-purple-600 dark:text-purple-400',
    Admin: 'text-red-600 dark:text-red-400',
    Public: 'text-green-600 dark:text-green-400',
  };

  const sectionColor = sectionColors[route.section];

  return (
    <div className="flex items-center gap-3 px-3 py-2 w-full">
      {/* Icon */}
      <span className="text-2xl flex-shrink-0" aria-hidden="true">
        {route.icon}
      </span>

      {/* Main content */}
      <div className="flex-1 min-w-0">
        {/* Route name */}
        <div className="flex items-center gap-2">
          <span className="font-medium text-gray-900 dark:text-gray-100">
            {highlightText(route.name, searchQuery)}
          </span>

          {/* Recent indicator */}
          {isRecent && (
            <span
              className="text-xs text-gray-500 dark:text-gray-400"
              title="Recently visited"
              aria-label="Recently visited"
            >
              ⏱️
            </span>
          )}

          {/* External link indicator */}
          {route.external && (
            <span
              className="text-xs text-gray-500 dark:text-gray-400"
              title="External link"
              aria-label="Opens in new tab"
            >
              ↗
            </span>
          )}
        </div>

        {/* Breadcrumbs or path */}
        <div className="flex items-center gap-1.5 text-sm text-gray-500 dark:text-gray-400 mt-0.5">
          {showBreadcrumbs ? (
            <>
              <span className={sectionColor}>{route.section}</span>
              <span aria-hidden="true">›</span>
              {breadcrumbs.slice(0, -1).map((crumb, index) => (
                <span key={crumb.id}>
                  <span>{crumb.name}</span>
                  {index < breadcrumbs.length - 2 && (
                    <span className="mx-1.5" aria-hidden="true">
                      ›
                    </span>
                  )}
                </span>
              ))}
            </>
          ) : (
            <>
              <span className={sectionColor}>{route.section}</span>
              <span aria-hidden="true">›</span>
              <span className="font-mono text-xs">
                {highlightText(route.path, searchQuery)}
              </span>
            </>
          )}
        </div>

        {/* Description */}
        {route.description && (
          <div className="text-xs text-gray-500 dark:text-gray-400 mt-1 line-clamp-1">
            {route.description}
          </div>
        )}
      </div>

      {/* Section badge */}
      <div
        className={`text-xs font-medium px-2 py-1 rounded-md flex-shrink-0 ${
          route.section === 'App'
            ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'
            : route.section === 'Settings'
              ? 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300'
              : route.section === 'Admin'
                ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300'
                : 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300'
        }`}
      >
        {route.section}
      </div>
    </div>
  );
}
