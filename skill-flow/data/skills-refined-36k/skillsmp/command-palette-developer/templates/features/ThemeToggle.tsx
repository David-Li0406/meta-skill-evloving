/**
 * ThemeToggle - Toggle between light/dark/system themes
 *
 * Features:
 * - Toggle between light/dark/system themes
 * - Button with icon (sun/moon/auto)
 * - Dropdown menu with 3 options
 * - Persist preference to localStorage
 * - Smooth transition between themes
 * - CSS variable updates
 *
 * @example
 * ```tsx
 * <ThemeToggle position="right" />
 * ```
 */

import { useState, useEffect, useRef } from 'react';

export type Theme = 'light' | 'dark' | 'system';

export interface ThemeToggleProps {
  /** Optional className for styling */
  className?: string;
  /** Position of dropdown menu */
  position?: 'left' | 'right';
  /** Show label text (default: false) */
  showLabel?: boolean;
}

/**
 * Get the system theme preference
 */
function getSystemTheme(): 'light' | 'dark' {
  if (typeof window === 'undefined') return 'light';
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

/**
 * ThemeToggle component
 *
 * Provides a button to toggle between light, dark, and system themes with dropdown menu.
 */
export function ThemeToggle({
  className = '',
  position = 'right',
  showLabel = false,
}: ThemeToggleProps): JSX.Element {
  const [theme, setTheme] = useState<Theme>(() => {
    if (typeof window === 'undefined') return 'system';
    return (localStorage.getItem('theme') as Theme) || 'system';
  });

  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Apply theme on mount and when theme changes
  useEffect(() => {
    const resolvedTheme = theme === 'system' ? getSystemTheme() : theme;
    document.documentElement.setAttribute('data-theme', resolvedTheme);

    if (resolvedTheme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }

    localStorage.setItem('theme', theme);
  }, [theme]);

  // Listen for system theme changes
  useEffect(() => {
    if (theme !== 'system') return;

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = () => {
      const resolvedTheme = getSystemTheme();
      document.documentElement.setAttribute('data-theme', resolvedTheme);

      if (resolvedTheme === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [theme]);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [isOpen]);

  const handleThemeChange = (newTheme: Theme) => {
    setTheme(newTheme);
    setIsOpen(false);
  };

  const currentIcon = {
    light: '☀️',
    dark: '🌙',
    system: '💻',
  }[theme];

  const currentLabel = {
    light: 'Light',
    dark: 'Dark',
    system: 'System',
  }[theme];

  return (
    <div className={`theme-toggle ${className}`.trim()} ref={dropdownRef} style={{ position: 'relative' }}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="theme-toggle-button"
        aria-label="Toggle theme"
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '8px 12px',
          background: 'var(--palette-bg-secondary)',
          border: '1px solid var(--palette-border)',
          borderRadius: '8px',
          color: 'var(--palette-text)',
          cursor: 'pointer',
          fontSize: '14px',
          fontWeight: 500,
          transition: 'all 0.2s ease',
        }}
      >
        <span style={{ fontSize: '16px' }}>{currentIcon}</span>
        {showLabel && <span>{currentLabel}</span>}
        <svg
          width="12"
          height="12"
          viewBox="0 0 12 12"
          fill="none"
          style={{
            transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)',
            transition: 'transform 0.2s ease',
          }}
        >
          <path
            d="M3 4.5L6 7.5L9 4.5"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>

      {isOpen && (
        <div
          className="theme-dropdown"
          style={{
            position: 'absolute',
            top: 'calc(100% + 8px)',
            [position]: 0,
            minWidth: '160px',
            background: 'var(--palette-bg)',
            border: '1px solid var(--palette-border)',
            borderRadius: '8px',
            boxShadow: '0 8px 16px var(--palette-shadow)',
            padding: '4px',
            zIndex: 1000,
          }}
        >
          <ThemeOption
            icon="☀️"
            label="Light"
            isActive={theme === 'light'}
            onClick={() => handleThemeChange('light')}
          />
          <ThemeOption
            icon="🌙"
            label="Dark"
            isActive={theme === 'dark'}
            onClick={() => handleThemeChange('dark')}
          />
          <ThemeOption
            icon="💻"
            label="System"
            isActive={theme === 'system'}
            onClick={() => handleThemeChange('system')}
          />
        </div>
      )}
    </div>
  );
}

/**
 * Theme option component for dropdown menu
 */
function ThemeOption({
  icon,
  label,
  isActive,
  onClick,
}: {
  icon: string;
  label: string;
  isActive: boolean;
  onClick: () => void;
}): JSX.Element {
  return (
    <button
      onClick={onClick}
      className="theme-option"
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        width: '100%',
        padding: '8px 12px',
        background: isActive ? 'var(--palette-selection-bg)' : 'transparent',
        border: 'none',
        borderRadius: '6px',
        color: 'var(--palette-text)',
        cursor: 'pointer',
        fontSize: '14px',
        fontWeight: isActive ? 600 : 400,
        textAlign: 'left',
        transition: 'all 0.15s ease',
      }}
    >
      <span style={{ fontSize: '16px' }}>{icon}</span>
      <span>{label}</span>
      {isActive && (
        <span style={{ marginLeft: 'auto', fontSize: '16px' }}>✓</span>
      )}
    </button>
  );
}

/**
 * Simple theme toggle button without dropdown
 */
export function SimpleThemeToggle({ className = '' }: { className?: string }): JSX.Element {
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    if (typeof window === 'undefined') return 'light';
    const stored = localStorage.getItem('theme');
    if (stored === 'dark') return 'dark';
    return getSystemTheme();
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  return (
    <button
      onClick={toggleTheme}
      className={`simple-theme-toggle ${className}`.trim()}
      aria-label="Toggle theme"
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        width: '40px',
        height: '40px',
        background: 'var(--palette-bg-secondary)',
        border: '1px solid var(--palette-border)',
        borderRadius: '8px',
        color: 'var(--palette-text)',
        cursor: 'pointer',
        fontSize: '18px',
        transition: 'all 0.2s ease',
      }}
    >
      {theme === 'light' ? '🌙' : '☀️'}
    </button>
  );
}
