/**
 * ThemeProvider - Theme context with Zustand
 *
 * Features:
 * - Theme state: 'light' | 'dark' | 'system'
 * - Resolved theme based on system preference
 * - System theme detection (prefers-color-scheme)
 * - CSS variable injection
 * - Theme persistence (localStorage)
 *
 * @example
 * ```tsx
 * // In App.tsx
 * import { ThemeProvider } from './providers/ThemeProvider';
 *
 * function App() {
 *   return (
 *     <ThemeProvider>
 *       <YourApp />
 *     </ThemeProvider>
 *   );
 * }
 *
 * // In any component
 * const { theme, resolvedTheme, setTheme } = useTheme();
 * ```
 */

import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { useEffect } from 'react';

export type Theme = 'light' | 'dark' | 'system';
export type ResolvedTheme = 'light' | 'dark';

interface ThemeState {
  theme: Theme;
  resolvedTheme: ResolvedTheme;
  setTheme: (theme: Theme) => void;
  setResolvedTheme: (theme: ResolvedTheme) => void;
}

/**
 * Get the system theme preference
 */
function getSystemTheme(): ResolvedTheme {
  if (typeof window === 'undefined') return 'light';
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

/**
 * Apply theme to document
 */
function applyTheme(theme: ResolvedTheme): void {
  document.documentElement.setAttribute('data-theme', theme);

  if (theme === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
}

/**
 * Theme Zustand store
 */
export const useThemeStore = create<ThemeState>()(
  devtools(
    persist(
      (set, get) => ({
        theme: 'system',
        resolvedTheme: getSystemTheme(),

        setTheme: (theme) => {
          const resolved = theme === 'system' ? getSystemTheme() : theme;
          set({ theme, resolvedTheme: resolved });
          applyTheme(resolved);
        },

        setResolvedTheme: (resolvedTheme) => {
          set({ resolvedTheme });
          applyTheme(resolvedTheme);
        },
      }),
      {
        name: 'theme-storage',
        partialize: (state) => ({
          theme: state.theme,
        }),
      }
    ),
    { name: 'Theme' }
  )
);

/**
 * Hook for theme state
 */
export function useTheme() {
  const theme = useThemeStore((state) => state.theme);
  const resolvedTheme = useThemeStore((state) => state.resolvedTheme);
  const setTheme = useThemeStore((state) => state.setTheme);
  const setResolvedTheme = useThemeStore((state) => state.setResolvedTheme);

  // Listen for system theme changes
  useEffect(() => {
    if (theme !== 'system') return;

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = () => {
      const systemTheme = getSystemTheme();
      setResolvedTheme(systemTheme);
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [theme, setResolvedTheme]);

  // Apply theme on mount
  useEffect(() => {
    const resolved = theme === 'system' ? getSystemTheme() : theme;
    applyTheme(resolved);
  }, [theme]);

  return {
    theme,
    resolvedTheme,
    setTheme,
  };
}

/**
 * ThemeProvider component for SSR-safe initialization
 */
export function ThemeProvider({ children }: { children: React.ReactNode }): JSX.Element {
  const theme = useThemeStore((state) => state.theme);
  const setResolvedTheme = useThemeStore((state) => state.setResolvedTheme);

  // Initialize theme on mount
  useEffect(() => {
    const resolved = theme === 'system' ? getSystemTheme() : theme;
    setResolvedTheme(resolved);
    applyTheme(resolved);

    // Add smooth transition after initial render
    const style = document.createElement('style');
    style.textContent = `
      * {
        transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out, border-color 0.2s ease-in-out;
      }

      @media (prefers-reduced-motion: reduce) {
        * {
          transition: none !important;
        }
      }
    `;
    document.head.appendChild(style);

    return () => {
      document.head.removeChild(style);
    };
  }, [theme, setResolvedTheme]);

  return <>{children}</>;
}

/**
 * Script to inject in HTML head to prevent FOUC
 * Add this to your index.html or _document.tsx
 *
 * @example
 * ```html
 * <script dangerouslySetInnerHTML={{ __html: getThemeScript() }} />
 * ```
 */
export function getThemeScript(): string {
  return `
    (function() {
      try {
        const stored = localStorage.getItem('theme-storage');
        const theme = stored ? JSON.parse(stored).state.theme : 'system';
        const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        const resolvedTheme = theme === 'system' ? systemTheme : theme;

        document.documentElement.setAttribute('data-theme', resolvedTheme);
        if (resolvedTheme === 'dark') {
          document.documentElement.classList.add('dark');
        }
      } catch (e) {}
    })();
  `;
}

/**
 * Hook for checking if system prefers dark mode
 */
export function useSystemTheme(): ResolvedTheme {
  const [systemTheme, setSystemTheme] = React.useState<ResolvedTheme>(getSystemTheme);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = () => setSystemTheme(getSystemTheme());

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  return systemTheme;
}

/**
 * Hook for checking if reduced motion is preferred
 */
export function useReducedMotion(): boolean {
  const [prefersReduced, setPrefersReduced] = React.useState(
    () => typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches
  );

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    const handleChange = () => setPrefersReduced(mediaQuery.matches);

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  return prefersReduced;
}

/**
 * Hook for checking high contrast mode
 */
export function useHighContrast(): boolean {
  const [highContrast, setHighContrast] = React.useState(
    () => typeof window !== 'undefined' && window.matchMedia('(prefers-contrast: high)').matches
  );

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-contrast: high)');
    const handleChange = () => setHighContrast(mediaQuery.matches);

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  return highContrast;
}

// Re-export React for hooks
import * as React from 'react';
