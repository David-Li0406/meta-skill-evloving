// Theme utility functions

export type Theme = 'light' | 'dark' | 'system';
export type ResolvedTheme = 'light' | 'dark';

export function getSystemTheme(): ResolvedTheme {
  if (typeof window === 'undefined') return 'light';
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

export function applyTheme(theme: ResolvedTheme): void {
  document.documentElement.setAttribute('data-theme', theme);

  if (theme === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
}

export interface ThemeConfig {
  bg: string;
  bgSecondary: string;
  text: string;
  textMuted: string;
  border: string;
  accent: string;
  accentHover: string;
}

export function createThemeVariables(config: ThemeConfig): React.CSSProperties {
  return {
    '--palette-bg': config.bg,
    '--palette-bg-secondary': config.bgSecondary,
    '--palette-text': config.text,
    '--palette-text-muted': config.textMuted,
    '--palette-border': config.border,
    '--palette-accent': config.accent,
    '--palette-accent-hover': config.accentHover,
  } as React.CSSProperties;
}
