// =============================================================================
// JOB CONSTANTS - Brand-Aware Job Filtering
// Separates MEDICAL and SOCIAL job types for multi-brand architecture
// =============================================================================

import { currentBrand, isMedical, isSocial } from './brand';

/**
 * Job definition with metadata for filtering and display
 */
export interface JobDefinition {
    id: string;
    label: string;
    shortLabel: string;
    category: 'SOIN' | 'EDUC' | 'SOCIAL' | 'HANDICAP' | 'PETITE_ENFANCE';
    emoji: string;
    /** Keywords for search matching */
    keywords: string[];
}

// =============================================================================
// MEDICAL JOBS - Pôle Soin (MedicoPulse)
// =============================================================================

export const MEDICAL_JOBS: JobDefinition[] = [
    {
        id: 'ide',
        label: 'Infirmier(ère) Diplômé(e) d\'État',
        shortLabel: 'IDE',
        category: 'SOIN',
        emoji: '💉',
        keywords: ['infirmier', 'infirmière', 'ide', 'nurse', 'soignant'],
    },
    {
        id: 'as',
        label: 'Aide-Soignant(e)',
        shortLabel: 'AS',
        category: 'SOIN',
        emoji: '🩺',
        keywords: ['aide-soignant', 'aide soignant', 'as', 'soins'],
    },
    {
        id: 'aes-medical',
        label: 'Accompagnant Éducatif et Social',
        shortLabel: 'AES',
        category: 'SOIN',
        emoji: '🤝',
        keywords: ['aes', 'accompagnant', 'éducatif', 'social'],
    },
    {
        id: 'kine',
        label: 'Masseur-Kinésithérapeute',
        shortLabel: 'Kiné',
        category: 'SOIN',
        emoji: '💪',
        keywords: ['kiné', 'kinésithérapeute', 'masseur', 'rééducation'],
    },
    {
        id: 'ergo',
        label: 'Ergothérapeute',
        shortLabel: 'Ergo',
        category: 'SOIN',
        emoji: '🖐️',
        keywords: ['ergothérapeute', 'ergo', 'ergothérapie'],
    },
    {
        id: 'psycho-medical',
        label: 'Psychologue',
        shortLabel: 'Psy',
        category: 'SOIN',
        emoji: '🧠',
        keywords: ['psychologue', 'psy', 'psychologie'],
    },
    {
        id: 'orthophoniste',
        label: 'Orthophoniste',
        shortLabel: 'Ortho',
        category: 'SOIN',
        emoji: '🗣️',
        keywords: ['orthophoniste', 'ortho', 'orthophonie'],
    },
    {
        id: 'ash',
        label: 'Agent de Service Hospitalier',
        shortLabel: 'ASH',
        category: 'SOIN',
        emoji: '🧹',
        keywords: ['ash', 'agent', 'service', 'hospitalier'],
    },
];

// =============================================================================
// SOCIAL JOBS - Pôle Éducatif & Social (SocioPulse)
// =============================================================================

export const SOCIAL_JOBS: JobDefinition[] = [
    // Éducatif
    {
        id: 'es',
        label: 'Éducateur(trice) Spécialisé(e)',
        shortLabel: 'ES',
        category: 'EDUC',
        emoji: '🎓',
        keywords: ['éducateur', 'éducatrice', 'spécialisé', 'es', 'dees'],
    },
    {
        id: 'me',
        label: 'Moniteur(trice) Éducateur(trice)',
        shortLabel: 'ME',
        category: 'EDUC',
        emoji: '👨‍🏫',
        keywords: ['moniteur', 'monitrice', 'éducateur', 'me'],
    },
    {
        id: 'eje',
        label: 'Éducateur(trice) de Jeunes Enfants',
        shortLabel: 'EJE',
        category: 'PETITE_ENFANCE',
        emoji: '👶',
        keywords: ['eje', 'éducateur', 'jeunes', 'enfants', 'petite enfance'],
    },
    {
        id: 'aes-social',
        label: 'Accompagnant Éducatif et Social',
        shortLabel: 'AES',
        category: 'SOCIAL',
        emoji: '🤝',
        keywords: ['aes', 'accompagnant', 'éducatif', 'social'],
    },
    // Social
    {
        id: 'tisf',
        label: 'Technicien(ne) d\'Intervention Sociale et Familiale',
        shortLabel: 'TISF',
        category: 'SOCIAL',
        emoji: '👨‍👩‍👧',
        keywords: ['tisf', 'technicien', 'intervention', 'sociale', 'familiale'],
    },
    {
        id: 'cesf',
        label: 'Conseiller(ère) en Économie Sociale Familiale',
        shortLabel: 'CESF',
        category: 'SOCIAL',
        emoji: '📋',
        keywords: ['cesf', 'conseiller', 'économie', 'sociale', 'familiale'],
    },
    {
        id: 'ass',
        label: 'Assistant(e) de Service Social',
        shortLabel: 'ASS',
        category: 'SOCIAL',
        emoji: '🏛️',
        keywords: ['assistant', 'service', 'social', 'ass'],
    },
    // Handicap
    {
        id: 'amp',
        label: 'Aide Médico-Psychologique',
        shortLabel: 'AMP',
        category: 'HANDICAP',
        emoji: '💜',
        keywords: ['amp', 'aide', 'médico', 'psychologique'],
    },
    {
        id: 'psychomotricien',
        label: 'Psychomotricien(ne)',
        shortLabel: 'Psychomot',
        category: 'HANDICAP',
        emoji: '🎯',
        keywords: ['psychomotricien', 'psychomot', 'psychomotricité'],
    },
    // Petite enfance
    {
        id: 'auxiliaire-puericulture',
        label: 'Auxiliaire de Puériculture',
        shortLabel: 'AP',
        category: 'PETITE_ENFANCE',
        emoji: '🍼',
        keywords: ['auxiliaire', 'puériculture', 'ap', 'crèche'],
    },
    {
        id: 'animateur',
        label: 'Animateur(trice) Socio-Éducatif',
        shortLabel: 'Animateur',
        category: 'EDUC',
        emoji: '🎨',
        keywords: ['animateur', 'animatrice', 'socio', 'éducatif', 'bafa'],
    },
];

// =============================================================================
// SERVICE TYPE FILTERS
// =============================================================================

export interface ServiceTypeFilter {
    id: string;
    label: string;
    emoji: string;
    description: string;
}

export const SERVICE_TYPES: ServiceTypeFilter[] = [
    {
        id: 'mission',
        label: 'Mission Renfort',
        emoji: '🚀',
        description: 'Intervention sur site',
    },
    {
        id: 'atelier',
        label: 'Atelier',
        emoji: '🎓',
        description: 'Animation collective',
    },
    {
        id: 'visio',
        label: 'Visio',
        emoji: '📹',
        description: 'Coaching à distance',
    },
];

// =============================================================================
// URGENCY LEVELS - Brand-Aware
// =============================================================================

export type UrgencyLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface UrgencyDefinition {
    id: UrgencyLevel;
    label: string;
    color: string;
    bgColor: string;
    description: string;
}

/**
 * Get available urgency levels based on brand
 * CRITICAL is only available for MEDICAL (soignants)
 */
export function getAvailableUrgencyLevels(): UrgencyDefinition[] {
    const baseUrgencies: UrgencyDefinition[] = [
        { id: 'LOW', label: 'Standard', color: 'text-slate-600', bgColor: 'bg-slate-100', description: 'Sous 1 semaine' },
        { id: 'MEDIUM', label: 'Pressé', color: 'text-amber-600', bgColor: 'bg-amber-100', description: 'Sous 48h' },
        { id: 'HIGH', label: 'Urgent', color: 'text-orange-600', bgColor: 'bg-orange-100', description: 'Sous 24h' },
    ];

    // CRITICAL only for medical
    if (isMedical()) {
        baseUrgencies.push({
            id: 'CRITICAL',
            label: 'Critique',
            color: 'text-red-600',
            bgColor: 'bg-red-100',
            description: 'Immédiat',
        });
    }

    return baseUrgencies;
}

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

/**
 * Get available jobs based on current brand configuration
 */
export function getAvailableJobs(): JobDefinition[] {
    if (isMedical()) {
        return MEDICAL_JOBS;
    }

    if (isSocial()) {
        return SOCIAL_JOBS;
    }

    // Fallback: return all jobs (shouldn't happen)
    return [...MEDICAL_JOBS, ...SOCIAL_JOBS];
}

/**
 * Get available service types based on brand
 * Hides Atelier and Visio for MEDICAL mode
 */
export function getAvailableServiceTypes(): ServiceTypeFilter[] {
    if (!currentBrand.showAteliers) {
        // Only show missions for MEDICAL
        return SERVICE_TYPES.filter(s => s.id === 'mission');
    }
    return SERVICE_TYPES;
}

/**
 * Check if a job is available in the current brand
 */
export function isJobAvailable(jobId: string): boolean {
    const availableJobs = getAvailableJobs();
    return availableJobs.some(j => j.id === jobId);
}

/**
 * Search jobs by keyword
 */
export function searchJobs(query: string): JobDefinition[] {
    const availableJobs = getAvailableJobs();
    const lowerQuery = query.toLowerCase().trim();

    if (!lowerQuery) return availableJobs;

    return availableJobs.filter(job =>
        job.label.toLowerCase().includes(lowerQuery) ||
        job.shortLabel.toLowerCase().includes(lowerQuery) ||
        job.keywords.some(kw => kw.includes(lowerQuery))
    );
}

/**
 * Get job by ID
 */
export function getJobById(jobId: string): JobDefinition | undefined {
    const allJobs = [...MEDICAL_JOBS, ...SOCIAL_JOBS];
    return allJobs.find(j => j.id === jobId);
}

/**
 * Get jobs grouped by category
 */
export function getJobsByCategory(): Record<string, JobDefinition[]> {
    const jobs = getAvailableJobs();
    return jobs.reduce((acc, job) => {
        if (!acc[job.category]) acc[job.category] = [];
        acc[job.category].push(job);
        return acc;
    }, {} as Record<string, JobDefinition[]>);
}
