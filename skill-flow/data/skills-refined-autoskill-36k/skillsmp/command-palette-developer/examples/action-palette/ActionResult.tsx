// Action result item with icon, name, description, and keyboard shortcut

import React from 'react';
import type { AppAction } from './actions-registry';

interface ActionResultProps {
  action: AppAction;
  isSelected: boolean;
  onClick: () => void;
}

export function ActionResult({ action, isSelected, onClick }: ActionResultProps): React.ReactElement {
  const Icon = action.icon;

  return (
    <button
      type="button"
      className={`
        w-full flex items-center gap-3 px-4 py-3 text-left
        transition-colors duration-150
        ${isSelected
          ? 'bg-blue-50 dark:bg-blue-900/20'
          : 'hover:bg-gray-50 dark:hover:bg-gray-800'
        }
        ${action.disabled
          ? 'opacity-50 cursor-not-allowed'
          : 'cursor-pointer'
        }
        ${action.destructive
          ? 'text-red-600 dark:text-red-400'
          : 'text-gray-900 dark:text-gray-100'
        }
      `}
      onClick={onClick}
      disabled={action.disabled}
      aria-label={action.name}
      aria-disabled={action.disabled}
    >
      {Icon && (
        <div className="flex-shrink-0">
          <Icon
            className={`w-5 h-5 ${
              action.destructive
                ? 'text-red-500 dark:text-red-400'
                : 'text-gray-500 dark:text-gray-400'
            }`}
          />
        </div>
      )}

      <div className="flex-1 min-w-0">
        <div className={`font-medium ${
          action.destructive
            ? 'text-red-600 dark:text-red-400'
            : 'text-gray-900 dark:text-gray-100'
        }`}>
          {action.name}
        </div>
        {action.description && (
          <div className="text-sm text-gray-500 dark:text-gray-400 truncate">
            {action.description}
          </div>
        )}
      </div>

      {action.shortcut && (
        <div className="flex-shrink-0">
          <ShortcutDisplay shortcut={action.shortcut} />
        </div>
      )}
    </button>
  );
}

interface ShortcutDisplayProps {
  shortcut: string;
}

function ShortcutDisplay({ shortcut }: ShortcutDisplayProps): React.ReactElement {
  const formatted = formatShortcut(shortcut);
  const keys = formatted.split('+').filter(Boolean);

  return (
    <div className="flex items-center gap-1">
      {keys.map((key, index) => (
        <kbd
          key={index}
          className="
            inline-flex items-center justify-center
            min-w-[24px] h-6 px-2
            text-xs font-mono font-medium
            bg-gray-100 dark:bg-gray-700
            border border-gray-300 dark:border-gray-600
            rounded
            text-gray-700 dark:text-gray-300
          "
        >
          {key}
        </kbd>
      ))}
    </div>
  );
}

function formatShortcut(shortcut: string): string {
  const isMac = /(Mac|iPhone|iPod|iPad)/i.test(navigator.platform);

  return shortcut
    .replace(/command/gi, isMac ? '⌘' : 'Ctrl')
    .replace(/shift/gi, isMac ? '⇧' : 'Shift')
    .replace(/option/gi, isMac ? '⌥' : 'Alt')
    .replace(/alt/gi, isMac ? '⌥' : 'Alt')
    .replace(/enter/gi, '↵')
    .replace(/escape/gi, 'Esc')
    .replace(/backspace/gi, '⌫');
}
