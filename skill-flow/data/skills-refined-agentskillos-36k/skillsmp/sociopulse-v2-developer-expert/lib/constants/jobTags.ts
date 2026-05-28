// =============================================================================
// JOB TAGS BIBLE - Exhaustive Job Identification System
// Ultra-fast onboarding with tag-based profession identification
// =============================================================================

import type { AppMode } from '../brand';
import { isMedical, isSocial } from '../brand';

// =============================================================================
// TYPES
// =============================================================================

export type JobCategory = 'SOIN' | 'SOCIAL' | 'ATELIER';

export interface JobTag {
    /** Unique identifier */
    id: string;
    /** Display label */
    label: string;
    /** Short label for chips */
    shortLabel: string;
    /** Category for filtering */
    category: JobCategory;
    /** Emoji for visual identification */
    emoji: string;
    /** Related search keywords */
    keywords: string[];
    /** Is this a popular/featured tag? */
    featured?: boolean;
}

// =============================================================================
// SOIN CATEGORY - Medical Jobs (MedicoPulse)
// =============================================================================

const SOIN_TAGS: JobTag[] = [
    // Infirmiers
    {
        id: 'ide',
        label: 'Infirmier(ère) Diplômé(e) d\'État',
        shortLabel: 'IDE',
        category: 'SOIN',
        emoji: '💉',
        keywords: ['infirmier', 'infirmière', 'ide', 'nurse', 'soins', 'injections'],
        featured: true,
    },
    {
        id: 'ibode',
        label: 'Infirmier(ère) de Bloc Opératoire',
        shortLabel: 'IBODE',
        category: 'SOIN',
        emoji: '🏥',
        keywords: ['ibode', 'bloc', 'opératoire', 'chirurgie'],
    },
    {
        id: 'iade',
        label: 'Infirmier(ère) Anesthésiste',
        shortLabel: 'IADE',
        category: 'SOIN',
        emoji: '😴',
        keywords: ['iade', 'anesthésiste', 'anesthésie', 'réanimation'],
    },
    {
        id: 'ide-puer',
        label: 'Infirmier(ère) Puéricultrice',
        shortLabel: 'Puéricultrice',
        category: 'SOIN',
        emoji: '👶',
        keywords: ['puéricultrice', 'pédiatrie', 'enfants', 'néonat'],
    },
    {
        id: 'ide-liberal',
        label: 'Infirmier(ère) Libéral(e)',
        shortLabel: 'IDE Libéral',
        category: 'SOIN',
        emoji: '🚗',
        keywords: ['libéral', 'domicile', 'had', 'ssiad'],
    },
    // Aides-soignants
    {
        id: 'as',
        label: 'Aide-Soignant(e)',
        shortLabel: 'AS',
        category: 'SOIN',
        emoji: '🩺',
        keywords: ['aide-soignant', 'aide soignant', 'as', 'soins', 'nursing'],
        featured: true,
    },
    {
        id: 'as-nuit',
        label: 'Aide-Soignant(e) de Nuit',
        shortLabel: 'AS Nuit',
        category: 'SOIN',
        emoji: '🌙',
        keywords: ['nuit', 'veille', 'garde'],
    },
    // AES/AMP
    {
        id: 'aes',
        label: 'Accompagnant Éducatif et Social',
        shortLabel: 'AES',
        category: 'SOIN',
        emoji: '🤝',
        keywords: ['aes', 'accompagnant', 'amp', 'aide médico'],
        featured: true,
    },
    {
        id: 'amp',
        label: 'Aide Médico-Psychologique',
        shortLabel: 'AMP',
        category: 'SOIN',
        emoji: '💜',
        keywords: ['amp', 'aide médico', 'psychologique'],
    },
    // Rééducation
    {
        id: 'kine',
        label: 'Masseur-Kinésithérapeute',
        shortLabel: 'Kiné',
        category: 'SOIN',
        emoji: '💪',
        keywords: ['kiné', 'kinésithérapeute', 'masseur', 'rééducation', 'motricité'],
    },
    {
        id: 'ergo',
        label: 'Ergothérapeute',
        shortLabel: 'Ergo',
        category: 'SOIN',
        emoji: '🖐️',
        keywords: ['ergothérapeute', 'ergo', 'ergothérapie', 'autonomie'],
    },
    {
        id: 'psychomot',
        label: 'Psychomotricien(ne)',
        shortLabel: 'Psychomot',
        category: 'SOIN',
        emoji: '🎯',
        keywords: ['psychomotricien', 'psychomot', 'motricité', 'corps'],
    },
    {
        id: 'orthophoniste',
        label: 'Orthophoniste',
        shortLabel: 'Ortho',
        category: 'SOIN',
        emoji: '🗣️',
        keywords: ['orthophoniste', 'ortho', 'langage', 'parole', 'déglutition'],
    },
    {
        id: 'orthoptiste',
        label: 'Orthoptiste',
        shortLabel: 'Orthoptiste',
        category: 'SOIN',
        emoji: '👁️',
        keywords: ['orthoptiste', 'vision', 'yeux', 'basse vision'],
    },
    // Autres soignants
    {
        id: 'ash',
        label: 'Agent de Service Hospitalier',
        shortLabel: 'ASH',
        category: 'SOIN',
        emoji: '🧹',
        keywords: ['ash', 'agent', 'service', 'hospitalier', 'hygiène'],
    },
    {
        id: 'brancardier',
        label: 'Brancardier',
        shortLabel: 'Brancardier',
        category: 'SOIN',
        emoji: '🛏️',
        keywords: ['brancardier', 'transport', 'malade'],
    },
    {
        id: 'dieteticien',
        label: 'Diététicien(ne)',
        shortLabel: 'Diététicien',
        category: 'SOIN',
        emoji: '🥗',
        keywords: ['diététicien', 'nutrition', 'alimentation'],
    },
    {
        id: 'psychologue',
        label: 'Psychologue',
        shortLabel: 'Psy',
        category: 'SOIN',
        emoji: '🧠',
        keywords: ['psychologue', 'psy', 'psychologie', 'écoute'],
    },
    {
        id: 'medecin-co',
        label: 'Médecin Coordonnateur',
        shortLabel: 'Médecin Co',
        category: 'SOIN',
        emoji: '👨‍⚕️',
        keywords: ['médecin', 'coordonnateur', 'ehpad', 'gériatrie'],
    },
    {
        id: 'pharmacien',
        label: 'Pharmacien(ne)',
        shortLabel: 'Pharmacien',
        category: 'SOIN',
        emoji: '💊',
        keywords: ['pharmacien', 'pharmacie', 'médicaments'],
    },
];

// =============================================================================
// SOCIAL CATEGORY - Éducatif & Social Jobs (SocioPulse)
// =============================================================================

const SOCIAL_TAGS: JobTag[] = [
    // Éducateurs
    {
        id: 'es',
        label: 'Éducateur(trice) Spécialisé(e)',
        shortLabel: 'ES',
        category: 'SOCIAL',
        emoji: '🎓',
        keywords: ['éducateur', 'éducatrice', 'spécialisé', 'es', 'dees'],
        featured: true,
    },
    {
        id: 'me',
        label: 'Moniteur(trice) Éducateur(trice)',
        shortLabel: 'ME',
        category: 'SOCIAL',
        emoji: '👨‍🏫',
        keywords: ['moniteur', 'monitrice', 'éducateur', 'me', 'deme'],
        featured: true,
    },
    {
        id: 'eje',
        label: 'Éducateur(trice) de Jeunes Enfants',
        shortLabel: 'EJE',
        category: 'SOCIAL',
        emoji: '👶',
        keywords: ['eje', 'éducateur', 'jeunes enfants', 'petite enfance', 'crèche'],
        featured: true,
    },
    {
        id: 'educateur-technique',
        label: 'Éducateur(trice) Technique Spécialisé(e)',
        shortLabel: 'ETS',
        category: 'SOCIAL',
        emoji: '🔧',
        keywords: ['éducateur technique', 'ets', 'atelier', 'professionnel'],
    },
    // Travailleurs sociaux
    {
        id: 'aes-social',
        label: 'Accompagnant Éducatif et Social',
        shortLabel: 'AES',
        category: 'SOCIAL',
        emoji: '🤝',
        keywords: ['aes', 'accompagnant', 'éducatif', 'social'],
        featured: true,
    },
    {
        id: 'tisf',
        label: 'Technicien(ne) Intervention Sociale Familiale',
        shortLabel: 'TISF',
        category: 'SOCIAL',
        emoji: '👨‍👩‍👧',
        keywords: ['tisf', 'technicien', 'intervention', 'sociale', 'familiale'],
    },
    {
        id: 'cesf',
        label: 'Conseiller(ère) Économie Sociale Familiale',
        shortLabel: 'CESF',
        category: 'SOCIAL',
        emoji: '📋',
        keywords: ['cesf', 'conseiller', 'économie', 'sociale', 'familiale', 'budget'],
    },
    {
        id: 'ass',
        label: 'Assistant(e) de Service Social',
        shortLabel: 'ASS',
        category: 'SOCIAL',
        emoji: '🏛️',
        keywords: ['assistant', 'service', 'social', 'ass', 'deass'],
    },
    // Encadrement
    {
        id: 'chef-service',
        label: 'Chef(fe) de Service Éducatif',
        shortLabel: 'Chef de Service',
        category: 'SOCIAL',
        emoji: '👔',
        keywords: ['chef', 'service', 'caferuis', 'encadrement', 'management'],
    },
    {
        id: 'coordinateur',
        label: 'Coordinateur(trice) de Projet',
        shortLabel: 'Coordinateur',
        category: 'SOCIAL',
        emoji: '🎯',
        keywords: ['coordinateur', 'projet', 'coordination'],
    },
    // Petite enfance
    {
        id: 'auxiliaire-puer',
        label: 'Auxiliaire de Puériculture',
        shortLabel: 'AP',
        category: 'SOCIAL',
        emoji: '🍼',
        keywords: ['auxiliaire', 'puériculture', 'ap', 'crèche', 'bébé'],
    },
    {
        id: 'cap-aepe',
        label: 'Titulaire CAP AEPE',
        shortLabel: 'CAP AEPE',
        category: 'SOCIAL',
        emoji: '🧸',
        keywords: ['cap', 'aepe', 'petite enfance', 'crèche'],
    },
    {
        id: 'agent-creche',
        label: 'Agent de Crèche',
        shortLabel: 'Agent Crèche',
        category: 'SOCIAL',
        emoji: '🎈',
        keywords: ['agent', 'crèche', 'petite enfance'],
    },
    // Animation
    {
        id: 'animateur-bafa',
        label: 'Animateur(trice) BAFA',
        shortLabel: 'Animateur',
        category: 'SOCIAL',
        emoji: '🎨',
        keywords: ['animateur', 'animatrice', 'bafa', 'animation', 'loisirs'],
    },
    {
        id: 'animateur-social',
        label: 'Animateur(trice) Socio-Éducatif',
        shortLabel: 'Animateur Socio',
        category: 'SOCIAL',
        emoji: '🎪',
        keywords: ['animateur', 'socio', 'éducatif', 'animation'],
    },
    // Autres
    {
        id: 'veilleur-nuit',
        label: 'Veilleur(se) de Nuit',
        shortLabel: 'Veilleur',
        category: 'SOCIAL',
        emoji: '🌙',
        keywords: ['veilleur', 'nuit', 'surveillance', 'internat'],
    },
    {
        id: 'maitresse-maison',
        label: 'Maître(sse) de Maison',
        shortLabel: 'Maître Maison',
        category: 'SOCIAL',
        emoji: '🏠',
        keywords: ['maître', 'maîtresse', 'maison', 'intendance'],
    },
    {
        id: 'surveillant-nuit',
        label: 'Surveillant(e) de Nuit Qualifié(e)',
        shortLabel: 'Surveillant Nuit',
        category: 'SOCIAL',
        emoji: '🔦',
        keywords: ['surveillant', 'nuit', 'qualifié', 'internat'],
    },
];

// =============================================================================
// ATELIER CATEGORY - SocioLive & Workshops
// =============================================================================

const ATELIER_TAGS: JobTag[] = [
    // Bien-être
    {
        id: 'sophrologue',
        label: 'Sophrologue',
        shortLabel: 'Sophrologue',
        category: 'ATELIER',
        emoji: '🧘',
        keywords: ['sophrologue', 'sophrologie', 'relaxation', 'bien-être'],
        featured: true,
    },
    {
        id: 'yoga',
        label: 'Professeur(e) de Yoga',
        shortLabel: 'Yoga',
        category: 'ATELIER',
        emoji: '🧘‍♀️',
        keywords: ['yoga', 'professeur', 'méditation', 'postures'],
        featured: true,
    },
    {
        id: 'reflexologue',
        label: 'Réflexologue',
        shortLabel: 'Réflexologue',
        category: 'ATELIER',
        emoji: '🦶',
        keywords: ['réflexologue', 'réflexologie', 'pieds', 'massage'],
    },
    {
        id: 'hypnotherapeute',
        label: 'Hypnothérapeute',
        shortLabel: 'Hypno',
        category: 'ATELIER',
        emoji: '💫',
        keywords: ['hypnothérapeute', 'hypnose', 'thérapie'],
    },
    {
        id: 'naturopathe',
        label: 'Naturopathe',
        shortLabel: 'Naturopathe',
        category: 'ATELIER',
        emoji: '🌿',
        keywords: ['naturopathe', 'naturopathie', 'naturel', 'plantes'],
    },
    // Art-thérapie
    {
        id: 'art-therapeute',
        label: 'Art-Thérapeute',
        shortLabel: 'Art-Thérapie',
        category: 'ATELIER',
        emoji: '🎨',
        keywords: ['art', 'thérapeute', 'art-thérapie', 'créatif'],
        featured: true,
    },
    {
        id: 'musicotherapeute',
        label: 'Musicothérapeute',
        shortLabel: 'Musico',
        category: 'ATELIER',
        emoji: '🎵',
        keywords: ['musicothérapeute', 'musicothérapie', 'musique'],
    },
    {
        id: 'danse-therapeute',
        label: 'Danse-Thérapeute',
        shortLabel: 'Danse-Thérapie',
        category: 'ATELIER',
        emoji: '💃',
        keywords: ['danse', 'thérapeute', 'mouvement'],
    },
    // Sport adapté
    {
        id: 'coach-sport-adapte',
        label: 'Coach Sport Adapté',
        shortLabel: 'APA',
        category: 'ATELIER',
        emoji: '🏋️',
        keywords: ['coach', 'sport', 'adapté', 'apa', 'activité physique'],
        featured: true,
    },
    {
        id: 'educateur-sportif',
        label: 'Éducateur(trice) Sportif(ve)',
        shortLabel: 'Éducateur Sport',
        category: 'ATELIER',
        emoji: '⚽',
        keywords: ['éducateur', 'sportif', 'sport', 'bpjeps'],
    },
    {
        id: 'aquagym',
        label: 'Animateur(trice) Aquagym',
        shortLabel: 'Aquagym',
        category: 'ATELIER',
        emoji: '🏊',
        keywords: ['aquagym', 'piscine', 'eau', 'natation'],
    },
    // Ateliers spécifiques
    {
        id: 'animateur-cuisine',
        label: 'Animateur(trice) Cuisine',
        shortLabel: 'Cuisine',
        category: 'ATELIER',
        emoji: '👨‍🍳',
        keywords: ['cuisine', 'atelier', 'culinaire', 'recettes'],
    },
    {
        id: 'animateur-jardinage',
        label: 'Animateur(trice) Jardinage',
        shortLabel: 'Jardinage',
        category: 'ATELIER',
        emoji: '🌱',
        keywords: ['jardinage', 'jardin', 'hortithérapie', 'plantes'],
    },
    {
        id: 'animateur-numerique',
        label: 'Animateur(trice) Numérique',
        shortLabel: 'Numérique',
        category: 'ATELIER',
        emoji: '💻',
        keywords: ['numérique', 'informatique', 'tablette', 'digital'],
    },
    {
        id: 'clown-hopital',
        label: 'Clown Hospitalier',
        shortLabel: 'Clown',
        category: 'ATELIER',
        emoji: '🤡',
        keywords: ['clown', 'hospitalier', 'rire', 'humour'],
    },
    {
        id: 'mediateur-animal',
        label: 'Médiateur(trice) Animal',
        shortLabel: 'Médiation Animale',
        category: 'ATELIER',
        emoji: '🐕',
        keywords: ['médiation', 'animale', 'zoothérapie', 'chien', 'animal'],
    },
];

// =============================================================================
// COMBINED EXPORTS
// =============================================================================

/** All job tags combined */
export const JOB_TAGS: JobTag[] = [...SOIN_TAGS, ...SOCIAL_TAGS, ...ATELIER_TAGS];

/** Tags by category */
export const TAGS_BY_CATEGORY: Record<JobCategory, JobTag[]> = {
    SOIN: SOIN_TAGS,
    SOCIAL: SOCIAL_TAGS,
    ATELIER: ATELIER_TAGS,
};

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

/**
 * Get job tags filtered by brand mode
 * MEDICAL -> SOIN only
 * SOCIAL -> SOCIAL + ATELIER
 */
export function getJobTagsByBrand(mode: AppMode): JobTag[] {
    if (mode === 'MEDICAL') {
        return SOIN_TAGS;
    }
    // SOCIAL mode
    return [...SOCIAL_TAGS, ...ATELIER_TAGS];
}

/**
 * Get featured/popular tags for current brand
 */
export function getFeaturedTags(mode: AppMode): JobTag[] {
    return getJobTagsByBrand(mode).filter(tag => tag.featured);
}

/**
 * Search tags by keyword
 */
export function searchTags(query: string, mode?: AppMode): JobTag[] {
    const tags = mode ? getJobTagsByBrand(mode) : JOB_TAGS;
    const lowerQuery = query.toLowerCase().trim();

    if (!lowerQuery) return tags;

    return tags.filter(tag =>
        tag.label.toLowerCase().includes(lowerQuery) ||
        tag.shortLabel.toLowerCase().includes(lowerQuery) ||
        tag.keywords.some(kw => kw.includes(lowerQuery)) ||
        tag.id.includes(lowerQuery)
    );
}

/**
 * Get tag by ID
 */
export function getTagById(id: string): JobTag | undefined {
    return JOB_TAGS.find(tag => tag.id === id);
}

/**
 * Get multiple tags by IDs
 */
export function getTagsByIds(ids: string[]): JobTag[] {
    return ids.map(id => getTagById(id)).filter((t): t is JobTag => t !== undefined);
}

/**
 * Get tags grouped by category for display
 */
export function getTagsGroupedByCategory(mode: AppMode): Record<string, JobTag[]> {
    const tags = getJobTagsByBrand(mode);
    return tags.reduce((acc, tag) => {
        if (!acc[tag.category]) acc[tag.category] = [];
        acc[tag.category].push(tag);
        return acc;
    }, {} as Record<string, JobTag[]>);
}

/**
 * Category display names
 */
export const CATEGORY_LABELS: Record<JobCategory, string> = {
    SOIN: '🏥 Soins & Santé',
    SOCIAL: '👥 Éducatif & Social',
    ATELIER: '🎨 Ateliers & Bien-être',
};
