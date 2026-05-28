// =============================================================================
// DOMAIN CONFIG - Polymorphic Feature Configuration
// Extends brand.ts with feature flags, terminology, and compliance rules
// =============================================================================

import { AppMode, currentBrand, isMedical, isSocial } from './brand';

// =============================================================================
// TYPES
// =============================================================================

export type DashboardLayoutType =
    | 'shift-planner'    // Medical Client: Calendar-dense shift management
    | 'project-hub'      // Social Client: Card-based project overview
    | 'job-ticker'       // Medical Talent: Fast list of urgent shifts
    | 'portfolio-feed';  // Social Talent: Skills showcase + mission feed

export type DocumentType =
    | 'DIPLOMA'
    | 'ADELI_PROOF'
    | 'ID_CARD'
    | 'DRIVER_LICENSE'
    | 'INSURANCE'
    | 'CRIMINAL_RECORD'
    | 'CERTIFICATE';

export type ProfessionalBodyCheck = 'ADELI' | 'DRJSCS' | null;

export interface DocumentRequirement {
    type: DocumentType;
    label: string;
    required: boolean;
    description?: string;
    expiresAfterMonths?: number;
}

export interface ComplianceRules {
    requiredDocuments: DocumentRequirement[];
    requiresADELI: boolean;
    requiresDriverLicense: boolean;
    professionalBodyCheck: ProfessionalBodyCheck;
}

export interface FeatureFlags {
    /** Social: true, Medical: false - Enables SocioLive workshops/ateliers */
    enableWorkshops: boolean;
    /** Medical: true, Social: false - Calendar-dense shift view for clients */
    enableShiftView: boolean;
    /** Social Talent: true - Portfolio showcase section */
    enablePortfolio: boolean;
    /** Medical Talent: true - Fast scrolling urgent shifts ticker */
    enableJobTicker: boolean;
    /** Medical: true - CRITICAL urgency level for missions */
    enableCriticalUrgency: boolean;
    /** Both: true - TalentPool/Vivier team management */
    enableTeamVivier: boolean;
    /** Social: true - Project-based mission grouping */
    enableProjects: boolean;
}

export interface Terminology {
    /** Medical: "Vacation" | Social: "Mission" */
    mission: string;
    missionPlural: string;
    /** Medical: "Soignant" | Social: "Intervenant" */
    talent: string;
    talentPlural: string;
    /** Medical: "Établissement de santé" | Social: "Structure" */
    client: string;
    clientPlural: string;
    /** Medical: "Garde" | Social: "Réservation" */
    booking: string;
    bookingPlural: string;
    /** Medical: "Vacation urgente" | Social: "Mission SOS" */
    urgentAction: string;
    /** Medical: "Planning des vacations" | Social: "Tableau de bord" */
    dashboardTitle: string;
    /** Medical: "Disponibilités" | Social: "Créneaux" */
    availability: string;
}

export interface DashboardLayouts {
    client: DashboardLayoutType;
    talent: DashboardLayoutType;
}

export interface DomainConfig {
    mode: AppMode;
    features: FeatureFlags;
    terms: Terminology;
    compliance: ComplianceRules;
    dashboardLayouts: DashboardLayouts;
}

// =============================================================================
// COMPLIANCE CONFIGURATIONS
// =============================================================================

const MEDICAL_COMPLIANCE: ComplianceRules = {
    requiredDocuments: [
        {
            type: 'DIPLOMA',
            label: "Diplôme d'État (IDE, AS, AES)",
            required: true,
            description: 'Diplôme validant votre qualification professionnelle'
        },
        {
            type: 'ADELI_PROOF',
            label: 'Attestation ADELI',
            required: true,
            description: 'Numéro ADELI délivré par l\'ARS'
        },
        {
            type: 'INSURANCE',
            label: 'RCP Professionnelle',
            required: true,
            description: 'Assurance Responsabilité Civile Professionnelle',
            expiresAfterMonths: 12
        },
        {
            type: 'ID_CARD',
            label: "Pièce d'identité",
            required: true,
            description: 'CNI ou Passeport en cours de validité'
        },
    ],
    requiresADELI: true,
    requiresDriverLicense: false,
    professionalBodyCheck: 'ADELI',
};

const SOCIAL_COMPLIANCE: ComplianceRules = {
    requiredDocuments: [
        {
            type: 'DIPLOMA',
            label: 'Diplôme (DEES, DEASS, DEEJE, etc.)',
            required: true,
            description: 'Diplôme validant votre qualification dans le social'
        },
        {
            type: 'DRIVER_LICENSE',
            label: 'Permis B',
            required: true,
            description: 'Requis pour les déplacements en mission'
        },
        {
            type: 'INSURANCE',
            label: 'RC Professionnelle',
            required: true,
            description: 'Assurance Responsabilité Civile',
            expiresAfterMonths: 12
        },
        {
            type: 'CRIMINAL_RECORD',
            label: 'Extrait de casier judiciaire (B3)',
            required: true,
            description: 'Requis pour travail avec public vulnérable',
            expiresAfterMonths: 6
        },
        {
            type: 'ID_CARD',
            label: "Pièce d'identité",
            required: true,
            description: 'CNI ou Passeport en cours de validité'
        },
    ],
    requiresADELI: false,
    requiresDriverLicense: true,
    professionalBodyCheck: 'DRJSCS',
};

// =============================================================================
// TERMINOLOGY CONFIGURATIONS
// =============================================================================

const MEDICAL_TERMS: Terminology = {
    mission: 'Vacation',
    missionPlural: 'Vacations',
    talent: 'Soignant',
    talentPlural: 'Soignants',
    client: 'Établissement',
    clientPlural: 'Établissements',
    booking: 'Garde',
    bookingPlural: 'Gardes',
    urgentAction: 'Vacation urgente',
    dashboardTitle: 'Planning des vacations',
    availability: 'Disponibilités',
};

const SOCIAL_TERMS: Terminology = {
    mission: 'Mission',
    missionPlural: 'Missions',
    talent: 'Intervenant',
    talentPlural: 'Intervenants',
    client: 'Structure',
    clientPlural: 'Structures',
    booking: 'Réservation',
    bookingPlural: 'Réservations',
    urgentAction: 'Mission SOS',
    dashboardTitle: 'Tableau de bord',
    availability: 'Créneaux',
};

// =============================================================================
// FEATURE FLAGS CONFIGURATIONS
// =============================================================================

const MEDICAL_FEATURES: FeatureFlags = {
    enableWorkshops: false,
    enableShiftView: true,
    enablePortfolio: false,
    enableJobTicker: true,
    enableCriticalUrgency: true,
    enableTeamVivier: true,
    enableProjects: false,
};

const SOCIAL_FEATURES: FeatureFlags = {
    enableWorkshops: true,
    enableShiftView: false,
    enablePortfolio: true,
    enableJobTicker: false,
    enableCriticalUrgency: false,
    enableTeamVivier: true,
    enableProjects: true,
};

// =============================================================================
// DASHBOARD LAYOUTS
// =============================================================================

const MEDICAL_LAYOUTS: DashboardLayouts = {
    client: 'shift-planner',
    talent: 'job-ticker',
};

const SOCIAL_LAYOUTS: DashboardLayouts = {
    client: 'project-hub',
    talent: 'portfolio-feed',
};

// =============================================================================
// DOMAIN CONFIGURATIONS
// =============================================================================

const MEDICAL_CONFIG: DomainConfig = {
    mode: 'MEDICAL',
    features: MEDICAL_FEATURES,
    terms: MEDICAL_TERMS,
    compliance: MEDICAL_COMPLIANCE,
    dashboardLayouts: MEDICAL_LAYOUTS,
};

const SOCIAL_CONFIG: DomainConfig = {
    mode: 'SOCIAL',
    features: SOCIAL_FEATURES,
    terms: SOCIAL_TERMS,
    compliance: SOCIAL_COMPLIANCE,
    dashboardLayouts: SOCIAL_LAYOUTS,
};

// =============================================================================
// EXPORTS
// =============================================================================

/**
 * Current domain configuration based on NEXT_PUBLIC_APP_MODE
 */
export const domainConfig: DomainConfig = isMedical() ? MEDICAL_CONFIG : SOCIAL_CONFIG;

/**
 * Get a specific term with fallback
 */
export function getTerm(key: keyof Terminology): string {
    return domainConfig.terms[key];
}

/**
 * Check if a feature is enabled
 */
export function isFeatureEnabled(feature: keyof FeatureFlags): boolean {
    return domainConfig.features[feature];
}

/**
 * Get required documents for the current domain
 */
export function getRequiredDocuments(): DocumentRequirement[] {
    return domainConfig.compliance.requiredDocuments;
}

/**
 * Get the dashboard layout type for a given role
 */
export function getDashboardLayout(role: 'client' | 'talent'): DashboardLayoutType {
    return domainConfig.dashboardLayouts[role];
}

/**
 * Check if ADELI verification is required (Medical only)
 */
export function requiresADELI(): boolean {
    return domainConfig.compliance.requiresADELI;
}

/**
 * Check if driver license is required (Social only)
 */
export function requiresDriverLicense(): boolean {
    return domainConfig.compliance.requiresDriverLicense;
}

// =============================================================================
// CROSS-BRAND ONBOARDING
// =============================================================================

/**
 * Cross-brand onboarding upsell content
 */
export interface CrossBrandContent {
    title: string;
    description: string;
    icon: 'Users' | 'Stethoscope';
    target: 'SocioPulse' | 'MedicoPulse';
}

/**
 * Get cross-brand upsell content based on current mode
 * Used in onboarding to offer cross-brand registration
 */
export function getCrossBrandOnboardingContent(
    currentMode: 'SOCIAL' | 'MEDICAL'
): CrossBrandContent {
    if (currentMode === 'MEDICAL') {
        return {
            title: "Besoin d'intervenants sociaux ?",
            description: "Activez SocioPulse pour vos besoins en Éducateurs et Moniteurs.",
            icon: 'Users',
            target: 'SocioPulse',
        };
    }

    return {
        title: "Besoin de renforts soignants ?",
        description: "Activez MedicoPulse pour recruter vos IDE/AS avec le même compte.",
        icon: 'Stethoscope',
        target: 'MedicoPulse',
    };
}
