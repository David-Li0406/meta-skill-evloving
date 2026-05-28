// =============================================================================
// BRAND ENGINE - Multi-Brand Configuration
// Single Codebase, Multi-Brand Architecture
// =============================================================================

/**
 * Application modes supported by the platform
 */
export type AppMode = 'SOCIAL' | 'MEDICAL';

/**
 * Category types that can be filtered by brand
 */
export type CategoryType =
    | 'SOIN'
    | 'EDUC'
    | 'SOCIAL'
    | 'HANDICAP'
    | 'PETITE_ENFANCE'
    | 'SOCIOLIVE';

/**
 * Accent color scheme for the brand
 */
export type AccentColor = 'teal' | 'indigo' | 'rose';

/**
 * Brand configuration interface
 * Defines all customizable aspects of a brand variant
 */
export interface BrandConfig {
    /** Internal mode identifier */
    mode: AppMode;

    /** Display name of the application */
    appName: string;

    /** Main headline (H1) for the homepage */
    heroTitle: string;

    /** Subheadline (H2) for the homepage */
    heroSubtitle: string;

    /** Primary accent color scheme */
    primaryColor: AccentColor;

    /** Secondary accent color for contrast elements */
    secondaryColor: AccentColor;

    /** Categories of professions to display in this brand */
    allowedCategories: CategoryType[];

    /** Whether to show SocioLive ateliers/workshops section */
    showAteliers: boolean;

    /** SEO meta title */
    metaTitle: string;

    /** SEO meta description */
    /** SEO meta description */
    metaDescription: string;

    /** Short tagline for logo (e.g. 'Le hub du social') */
    tagline: string;
}

// =============================================================================
// BRAND CONFIGURATIONS
// =============================================================================

/**
 * SocioPulse - Social/Éducatif focus
 * Target: MECS, IME, ITEP, Crèches, Foyers, CCAS
 */
const SOCIAL_CONFIG: BrandConfig = {
    mode: 'SOCIAL',
    appName: 'SocioPulse',
    heroTitle: "La plateforme des métiers de l'Humain et du Lien Social",
    heroSubtitle: 'Éducateurs, travailleurs sociaux, animateurs. Trouvez un renfort ou proposez vos services.',
    primaryColor: 'teal',
    secondaryColor: 'indigo',
    allowedCategories: ['EDUC', 'SOCIAL', 'HANDICAP', 'PETITE_ENFANCE', 'SOCIOLIVE'],
    showAteliers: true,
    metaTitle: 'SocioPulse - La plateforme du médico-social | Renforts & Ateliers',
    metaDescription: 'Trouvez des éducateurs, travailleurs sociaux et animateurs pour vos établissements. Ateliers bien-être et formations SocioLive.',
    tagline: 'Le hub du social',
};

/**
 * MedicoPulse - Medical/Soin focus
 * Target: EHPAD, SSIAD, Cliniques, Hôpitaux, HAD
 */
const MEDICAL_CONFIG: BrandConfig = {
    mode: 'MEDICAL',
    appName: 'MedicoPulse',
    heroTitle: 'La plateforme de gestion des Renforts Soignants',
    heroSubtitle: 'Infirmiers, aides-soignants, AES. Comblez vos absences en urgence.',
    primaryColor: 'rose',
    secondaryColor: 'indigo',
    allowedCategories: ['SOIN'],
    showAteliers: false,
    metaTitle: 'MedicoPulse - Renforts soignants en urgence | IDE, AS, AES',
    metaDescription: 'Plateforme de mise en relation pour établissements de santé. Trouvez des infirmiers et aides-soignants disponibles en moins de 24h.',
    tagline: 'Gestion des renforts',
};

// =============================================================================
// RUNTIME CONFIGURATION
// =============================================================================

/**
 * Current application mode from environment variable
 * Defaults to 'SOCIAL' if not specified
 */
const APP_MODE: AppMode =
    (process.env.NEXT_PUBLIC_APP_MODE as AppMode) || 'SOCIAL';

/**
 * Active brand configuration based on current mode
 */
export const currentBrand: BrandConfig =
    APP_MODE === 'MEDICAL' ? MEDICAL_CONFIG : SOCIAL_CONFIG;

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

/**
 * Check if current mode is MEDICAL (MedicoPulse)
 */
export function isMedical(): boolean {
    return currentBrand.mode === 'MEDICAL';
}

/**
 * Check if current mode is SOCIAL (SocioPulse)
 */
export function isSocial(): boolean {
    return currentBrand.mode === 'SOCIAL';
}

/**
 * Check if a category is allowed in the current brand
 * @param category - Category to check
 */
export function isCategoryAllowed(category: string): boolean {
    return currentBrand.allowedCategories.includes(category as CategoryType);
}

/**
 * Filter an array of items by allowed categories
 * @param items - Items with a category property
 */
export function filterByBrand<T extends { category?: string }>(items: T[]): T[] {
    return items.filter(item =>
        !item.category || isCategoryAllowed(item.category)
    );
}

/**
 * Get Tailwind color classes for the primary accent
 */
export function getPrimaryColorClasses(): {
    bg: string;
    bgLight: string;
    text: string;
    border: string;
    hover: string;
} {
    const colorMap = {
        teal: {
            bg: 'bg-live-500',
            bgLight: 'bg-live-100',
            text: 'text-live-600',
            border: 'border-live-500',
            hover: 'hover:bg-live-600',
        },
        indigo: {
            bg: 'bg-brand-500',
            bgLight: 'bg-brand-100',
            text: 'text-brand-600',
            border: 'border-brand-500',
            hover: 'hover:bg-brand-600',
        },
        rose: {
            bg: 'bg-alert-500',
            bgLight: 'bg-alert-100',
            text: 'text-alert-600',
            border: 'border-alert-500',
            hover: 'hover:bg-alert-600',
        },
    };

    return colorMap[currentBrand.primaryColor];
}

/**
 * Get the brand-specific gradient for hero sections
 */
export function getHeroGradient(): string {
    if (isMedical()) {
        return 'from-alert-600 via-alert-500 to-rose-400';
    }
    return 'from-live-500 via-brand-500 to-indigo-500';
}
