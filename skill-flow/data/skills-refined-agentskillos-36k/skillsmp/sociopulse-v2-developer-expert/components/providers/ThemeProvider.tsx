'use client';

import { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { currentBrand, isMedical } from '@/lib/brand';

// =============================================================================
// THEME PROVIDER - Polymorphic Design System with Dark Mode
// Manages both brand theme (medical/social) and color mode (light/dark)
// =============================================================================

type ColorMode = 'light' | 'dark' | 'system';
type BrandTheme = 'medical' | 'social';

interface ThemeContextType {
    colorMode: ColorMode;
    resolvedMode: 'light' | 'dark';
    brandTheme: BrandTheme;
    setColorMode: (mode: ColorMode) => void;
    toggleColorMode: () => void;
    isDark: boolean;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

const COLOR_MODE_KEY = 'color-mode-preference';

interface ThemeProviderProps {
    children: React.ReactNode;
}

/**
 * ThemeProvider applies brand-specific theme AND color mode to the document
 * - Brand: SOCIAL (teal/indigo) | MEDICAL (rose/blue)
 * - Mode: light | dark | system
 */
export function ThemeProvider({ children }: ThemeProviderProps) {
    const [colorMode, setColorModeState] = useState<ColorMode>('light');
    const [resolvedMode, setResolvedMode] = useState<'light' | 'dark'>('light');
    const brandTheme: BrandTheme = isMedical() ? 'medical' : 'social';

    // Initialize from localStorage
    useEffect(() => {
        const saved = localStorage.getItem(COLOR_MODE_KEY) as ColorMode | null;
        if (saved && ['light', 'dark', 'system'].includes(saved)) {
            setColorModeState(saved);
        }
    }, []);

    // Resolve system preference and apply theme
    useEffect(() => {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        
        const resolveMode = () => {
            if (colorMode === 'system') {
                return mediaQuery.matches ? 'dark' : 'light';
            }
            return colorMode;
        };

        const applyTheme = () => {
            const resolved = resolveMode();
            setResolvedMode(resolved);

            // Apply brand theme
            document.documentElement.setAttribute('data-theme', brandTheme);
            document.documentElement.classList.remove('theme-medical', 'theme-social');
            document.documentElement.classList.add(`theme-${brandTheme}`);

            // Apply color mode
            document.documentElement.setAttribute('data-mode', resolved);
            document.documentElement.classList.remove('light', 'dark');
            document.documentElement.classList.add(resolved);

            console.log(`🎨 Theme: ${brandTheme} | Mode: ${resolved}`);
        };

        applyTheme();

        // Listen for system preference changes
        const handleChange = () => {
            if (colorMode === 'system') {
                applyTheme();
            }
        };

        mediaQuery.addEventListener('change', handleChange);
        return () => mediaQuery.removeEventListener('change', handleChange);
    }, [colorMode, brandTheme]);

    const setColorMode = useCallback((mode: ColorMode) => {
        setColorModeState(mode);
        localStorage.setItem(COLOR_MODE_KEY, mode);
    }, []);

    const toggleColorMode = useCallback(() => {
        setColorMode(resolvedMode === 'light' ? 'dark' : 'light');
    }, [resolvedMode, setColorMode]);

    const value: ThemeContextType = {
        colorMode,
        resolvedMode,
        brandTheme,
        setColorMode,
        toggleColorMode,
        isDark: resolvedMode === 'dark',
    };

    return (
        <ThemeContext.Provider value={value}>
            {children}
        </ThemeContext.Provider>
    );
}

/**
 * Hook to access theme context
 */
export function useTheme(): ThemeContextType {
    const context = useContext(ThemeContext);
    if (!context) {
        throw new Error('useTheme must be used within a ThemeProvider');
    }
    return context;
}

/**
 * Get current brand theme value (for SSR-safe usage)
 */
export function getTheme(): BrandTheme {
    return isMedical() ? 'medical' : 'social';
}

/**
 * Theme-aware class helper
 * Returns different classes based on current brand theme
 */
export function themeClass(
    socialClass: string,
    medicalClass: string
): string {
    return isMedical() ? medicalClass : socialClass;
}
