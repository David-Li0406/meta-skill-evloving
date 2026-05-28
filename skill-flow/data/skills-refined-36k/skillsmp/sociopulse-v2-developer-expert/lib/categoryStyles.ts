import type { LucideIcon } from 'lucide-react';
import { Stethoscope, Users, Video, Sparkles } from 'lucide-react';

// ===========================================
// CATEGORY STYLES - SocioPulse Design System
// Provides visual styling per category type
// ===========================================

export type CategoryType = 'SOIN' | 'EDUC' | 'SOCIOLIVE' | 'DEFAULT';

export interface CategoryStyle {
    /** Tailwind border color class */
    borderColor: string;
    /** Tailwind badge background class */
    badgeColor: string;
    /** Tailwind badge text class */
    badgeTextColor: string;
    /** Lucide icon component */
    Icon: LucideIcon;
    /** Icon name for reference */
    iconName: string;
    /** Tailwind gradient class for fallback */
    gradientClass: string;
    /** Raw CSS gradient for inline styles */
    gradientCss: string;
    /** Category label */
    label: string;
    /** Emoji for quick visual identification */
    emoji: string;
}

const categoryStyles: Record<CategoryType, CategoryStyle> = {
    SOIN: {
        borderColor: 'border-blue-600',
        badgeColor: 'bg-blue-100',
        badgeTextColor: 'text-blue-700',
        Icon: Stethoscope,
        iconName: 'Stethoscope',
        gradientClass: 'category-gradient-soin',
        gradientCss: 'linear-gradient(135deg, #DBEAFE 0%, #60A5FA 50%, #2563EB 100%)',
        label: 'Soin',
        emoji: '🩺',
    },
    EDUC: {
        borderColor: 'border-amber-500',
        badgeColor: 'bg-amber-100',
        badgeTextColor: 'text-amber-700',
        Icon: Users,
        iconName: 'Users',
        gradientClass: 'category-gradient-educ',
        gradientCss: 'linear-gradient(135deg, #FEF3C7 0%, #F59E0B 50%, #D97706 100%)',
        label: 'Éducatif',
        emoji: '👥',
    },
    SOCIOLIVE: {
        borderColor: 'border-teal-500',
        badgeColor: 'bg-teal-100',
        badgeTextColor: 'text-teal-700',
        Icon: Video,
        iconName: 'Video',
        gradientClass: 'category-gradient-sociolive',
        gradientCss: 'linear-gradient(135deg, #CCFBF1 0%, #14B8A6 50%, #0D9488 100%)',
        label: 'SocioLive',
        emoji: '🎥',
    },
    DEFAULT: {
        borderColor: 'border-slate-400',
        badgeColor: 'bg-slate-100',
        badgeTextColor: 'text-slate-600',
        Icon: Sparkles,
        iconName: 'Sparkles',
        gradientClass: 'category-gradient-default',
        gradientCss: 'linear-gradient(135deg, #F1F5F9 0%, #94A3B8 50%, #64748B 100%)',
        label: 'Service',
        emoji: '✨',
    },
};

/**
 * Normalizes category string to match CategoryType
 */
function normalizeCategory(category?: string): CategoryType {
    if (!category) return 'DEFAULT';

    const upper = category.toUpperCase().trim();

    // SOIN variations: AS, IDE, SOIN, MEDICAL, NURSE, AIDE-SOIGNANT
    if (['SOIN', 'AS', 'IDE', 'MEDICAL', 'NURSE', 'AIDE-SOIGNANT', 'INFIRMIER', 'INFIRMIÈRE'].some(k => upper.includes(k))) {
        return 'SOIN';
    }

    // EDUC variations: MECS, ASE, EDUC, EDUCATEUR, EDUCATION
    if (['EDUC', 'MECS', 'ASE', 'EDUCATEUR', 'ÉDUCATEUR', 'EDUCATION', 'ÉDUCATION', 'SOCIAL'].some(k => upper.includes(k))) {
        return 'EDUC';
    }

    // SOCIOLIVE variations: SOCIOLIVE, ATELIER, WORKSHOP, VIDEO, COACHING
    if (['SOCIOLIVE', 'ATELIER', 'WORKSHOP', 'VIDEO', 'COACHING', 'LIVE', 'VISIO'].some(k => upper.includes(k))) {
        return 'SOCIOLIVE';
    }

    return 'DEFAULT';
}

/**
 * Get visual styling for a category
 * @param category - Raw category string from API
 * @returns CategoryStyle object with all visual properties
 */
export function getCardStyle(category?: string): CategoryStyle {
    const normalized = normalizeCategory(category);
    return categoryStyles[normalized];
}

/**
 * Get all available category styles
 */
export function getAllCategoryStyles(): Record<CategoryType, CategoryStyle> {
    return categoryStyles;
}

/**
 * Check if a category is valid
 */
export function isValidCategory(category?: string): boolean {
    return normalizeCategory(category) !== 'DEFAULT';
}
