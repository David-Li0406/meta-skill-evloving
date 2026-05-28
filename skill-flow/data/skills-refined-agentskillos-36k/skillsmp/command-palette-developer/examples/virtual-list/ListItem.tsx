/**
 * Optimized list item component for virtual scrolling
 *
 * Fixed height (48px) with React.memo for preventing unnecessary re-renders.
 */

import { memo } from 'react';
import type { MockItem } from './generate-mock-data';

export interface ListItemProps {
  /** Item data to display */
  item: MockItem;

  /** Item index in the list */
  index: number;

  /** Whether this item is currently selected */
  isSelected?: boolean;

  /** Click handler */
  onClick?: (item: MockItem, index: number) => void;

  /** Optional icon display override */
  showIcon?: boolean;
}

/**
 * List item component with fixed 48px height
 *
 * Optimized for virtual scrolling performance:
 * - Fixed height (no layout thrashing)
 * - Minimal DOM structure
 * - React.memo prevents unnecessary re-renders
 * - No expensive computations
 *
 * @example
 * ```tsx
 * <ListItem
 *   item={item}
 *   index={0}
 *   isSelected={selectedIndex === 0}
 *   onClick={(item) => console.log('Clicked:', item.title)}
 * />
 * ```
 */
export const ListItem = memo<ListItemProps>(function ListItem({
  item,
  index,
  isSelected = false,
  onClick,
  showIcon = true,
}) {
  const handleClick = () => {
    onClick?.(item, index);
  };

  return (
    <div
      className={`
        flex items-center gap-3 px-4 h-12
        border-b border-gray-100
        transition-colors duration-75
        cursor-pointer
        ${isSelected
          ? 'bg-blue-50 border-blue-200'
          : 'hover:bg-gray-50'
        }
      `}
      onClick={handleClick}
      role="option"
      aria-selected={isSelected}
      data-index={index}
    >
      {/* Index number (for debugging/demo purposes) */}
      <span className="text-xs text-gray-400 font-mono w-16 flex-shrink-0">
        #{index.toString().padStart(6, '0')}
      </span>

      {/* Optional icon */}
      {showIcon && item.icon && (
        <span className="text-gray-500 flex-shrink-0">
          <IconPlaceholder name={item.icon} />
        </span>
      )}

      {/* Item title */}
      <span className="text-sm text-gray-900 flex-1 truncate">
        {item.title}
      </span>

      {/* Category badge */}
      <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded flex-shrink-0">
        {item.category}
      </span>
    </div>
  );
});

/**
 * Simple icon placeholder component
 *
 * In a real app, you'd use lucide-react or similar.
 * This is a lightweight placeholder to avoid external dependencies.
 */
function IconPlaceholder({ name }: { name: string }) {
  return (
    <div
      className="w-4 h-4 rounded bg-gray-300 flex items-center justify-center"
      title={name}
      aria-label={name}
    >
      <span className="text-[8px] text-gray-600 font-bold">
        {name[0].toUpperCase()}
      </span>
    </div>
  );
}

/**
 * Compact list item variant (32px height)
 *
 * For even denser lists where more items need to be visible.
 */
export const ListItemCompact = memo<ListItemProps>(function ListItemCompact({
  item,
  index,
  isSelected = false,
  onClick,
  showIcon = false,
}) {
  const handleClick = () => {
    onClick?.(item, index);
  };

  return (
    <div
      className={`
        flex items-center gap-2 px-3 h-8
        border-b border-gray-50
        transition-colors duration-75
        cursor-pointer text-xs
        ${isSelected
          ? 'bg-blue-50 border-blue-200'
          : 'hover:bg-gray-50'
        }
      `}
      onClick={handleClick}
      role="option"
      aria-selected={isSelected}
      data-index={index}
    >
      <span className="text-[10px] text-gray-400 font-mono w-12 flex-shrink-0">
        #{index}
      </span>

      {showIcon && item.icon && (
        <span className="text-gray-400 flex-shrink-0">
          <div className="w-3 h-3 rounded-sm bg-gray-200" />
        </span>
      )}

      <span className="text-gray-900 flex-1 truncate">
        {item.title}
      </span>

      <span className="text-[10px] text-gray-500">
        {item.category}
      </span>
    </div>
  );
});
