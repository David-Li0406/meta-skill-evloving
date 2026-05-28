// =============================================================================
// FORM CONFIG - Brand-Aware Dynamic Form Fields
// Config-driven forms for MEDICAL (MedicoPulse) vs SOCIAL (SocioPulse)
// =============================================================================

import type { AppMode } from './brand';

// =============================================================================
// TYPES
// =============================================================================

export type FieldType =
    | 'text'
    | 'email'
    | 'tel'
    | 'number'
    | 'boolean'
    | 'select'
    | 'multiselect'
    | 'textarea'
    | 'date';

export interface FieldOption {
    value: string;
    label: string;
}

export interface FieldDefinition {
    /** Unique field name (maps to form data key) */
    name: string;
    /** Display label */
    label: string;
    /** Input type */
    type: FieldType;
    /** Is field required? */
    required: boolean;
    /** Placeholder text */
    placeholder?: string;
    /** Options for select/multiselect */
    options?: FieldOption[];
    /** Help text displayed below field */
    helpText?: string;
    /** Default value */
    defaultValue?: string | boolean | string[];
    /** Validation regex pattern */
    pattern?: string;
    /** Minimum length (for text) or value (for number) */
    min?: number;
    /** Maximum length (for text) or value (for number) */
    max?: number;
    /** Icon name (Lucide) */
    icon?: string;
    /** Conditional display: only show if another field has specific value */
    showIf?: { field: string; value: string | boolean };
}

export interface FormSection {
    id: string;
    title: string;
    description?: string;
    fields: FieldDefinition[];
}

// =============================================================================
// PROFILE FIELDS - MEDICAL (MedicoPulse)
// For: IDE, AS, Kiné, Ergo, Ortho, ASH
// =============================================================================

const MEDICAL_PROFILE_SECTIONS: FormSection[] = [
    {
        id: 'identity',
        title: 'Identité',
        fields: [
            { name: 'firstName', label: 'Prénom', type: 'text', required: true, placeholder: 'Jean' },
            { name: 'lastName', label: 'Nom', type: 'text', required: true, placeholder: 'Dupont' },
            { name: 'phone', label: 'Téléphone', type: 'tel', required: true, placeholder: '06 12 34 56 78' },
        ],
    },
    {
        id: 'professional',
        title: 'Informations professionnelles',
        description: 'Données obligatoires pour les établissements de santé',
        fields: [
            {
                name: 'adeliNumber',
                label: 'Numéro ADELI',
                type: 'text',
                required: true,
                placeholder: '75 99 12345 6',
                helpText: 'Numéro à 9 chiffres délivré par l\'ARS',
                pattern: '^[0-9]{2}\\s?[0-9]{2}\\s?[0-9]{5}\\s?[0-9]$',
                icon: 'BadgeCheck',
            },
            {
                name: 'rppsNumber',
                label: 'Numéro RPPS',
                type: 'text',
                required: false,
                placeholder: '10 123 456 789',
                helpText: 'Répertoire Partagé des Professionnels de Santé (facultatif)',
                icon: 'FileText',
            },
            {
                name: 'diploma',
                label: 'Diplôme principal',
                type: 'select',
                required: true,
                options: [
                    { value: 'dei', label: 'DEI - Diplôme d\'État Infirmier' },
                    { value: 'deas', label: 'DEAS - Diplôme d\'État d\'Aide-Soignant' },
                    { value: 'deaes', label: 'DEAES - Accompagnant Éducatif et Social' },
                    { value: 'de-kine', label: 'DE Masseur-Kinésithérapeute' },
                    { value: 'de-ergo', label: 'DE Ergothérapeute' },
                    { value: 'de-ortho', label: 'CCO Orthophoniste' },
                    { value: 'doctorat', label: 'Doctorat en Médecine' },
                ],
                icon: 'GraduationCap',
            },
            {
                name: 'diplomaYear',
                label: 'Année d\'obtention',
                type: 'number',
                required: true,
                min: 1970,
                max: 2026,
                placeholder: '2020',
            },
        ],
    },
    {
        id: 'clinical',
        title: 'Compétences cliniques',
        fields: [
            {
                name: 'vaccinationStatus',
                label: 'Vaccinations à jour (selon réglementation)',
                type: 'boolean',
                required: true,
                helpText: 'Hépatite B, DTP, Grippe (recommandé)',
                defaultValue: false,
            },
            {
                name: 'technicalSkills',
                label: 'Soins techniques maîtrisés',
                type: 'multiselect',
                required: false,
                options: [
                    { value: 'perf', label: 'Perfusion / Cathéter' },
                    { value: 'pansements', label: 'Pansements complexes' },
                    { value: 'dialyse', label: 'Dialyse' },
                    { value: 'stomie', label: 'Soins de stomie' },
                    { value: 'palliatifs', label: 'Soins palliatifs' },
                    { value: 'geriatrie', label: 'Gériatrie' },
                    { value: 'pediatrie', label: 'Pédiatrie' },
                ],
            },
            {
                name: 'softwareKnowledge',
                label: 'Logiciels de soin maîtrisés',
                type: 'multiselect',
                required: false,
                options: [
                    { value: 'netsoins', label: 'NetSoins' },
                    { value: 'titan', label: 'Titan' },
                    { value: 'mediboard', label: 'Mediboard' },
                    { value: 'hopital-manager', label: 'Hôpital Manager' },
                    { value: 'autres', label: 'Autres' },
                ],
            },
        ],
    },
    {
        id: 'availability',
        title: 'Disponibilités',
        fields: [
            {
                name: 'nightShiftOk',
                label: 'Disponible pour les nuits',
                type: 'boolean',
                required: false,
                defaultValue: false,
            },
            {
                name: 'weekendOk',
                label: 'Disponible le weekend',
                type: 'boolean',
                required: false,
                defaultValue: true,
            },
            {
                name: 'hourlyRate',
                label: 'Taux horaire souhaité (€)',
                type: 'number',
                required: true,
                min: 15,
                max: 100,
                placeholder: '25',
                helpText: 'Tarif horaire brut',
            },
        ],
    },
];

// =============================================================================
// PROFILE FIELDS - SOCIAL (SocioPulse)
// For: ES, ME, EJE, TISF, CESF, ASS, AMP, Animateur
// =============================================================================

const SOCIAL_PROFILE_SECTIONS: FormSection[] = [
    {
        id: 'identity',
        title: 'Identité',
        fields: [
            { name: 'firstName', label: 'Prénom', type: 'text', required: true, placeholder: 'Marie' },
            { name: 'lastName', label: 'Nom', type: 'text', required: true, placeholder: 'Martin' },
            { name: 'phone', label: 'Téléphone', type: 'tel', required: true, placeholder: '06 12 34 56 78' },
        ],
    },
    {
        id: 'professional',
        title: 'Parcours professionnel',
        fields: [
            {
                name: 'diploma',
                label: 'Diplôme principal',
                type: 'select',
                required: true,
                options: [
                    { value: 'dees', label: 'DEES - Éducateur Spécialisé' },
                    { value: 'deme', label: 'DEME - Moniteur Éducateur' },
                    { value: 'deeje', label: 'DEEJE - Éducateur de Jeunes Enfants' },
                    { value: 'deaes', label: 'DEAES - Accompagnant Éducatif et Social' },
                    { value: 'detisf', label: 'DETISF - Technicien Intervention Sociale' },
                    { value: 'decesf', label: 'DECESF - Conseiller Économie Sociale' },
                    { value: 'deass', label: 'DEASS - Assistant de Service Social' },
                    { value: 'caferuis', label: 'CAFERUIS - Responsable d\'Unité' },
                    { value: 'bafa', label: 'BAFA / BAFD' },
                    { value: 'cap-petite-enfance', label: 'CAP Petite Enfance / AEPE' },
                ],
                icon: 'GraduationCap',
            },
            {
                name: 'diplomaYear',
                label: 'Année d\'obtention',
                type: 'number',
                required: true,
                min: 1970,
                max: 2026,
                placeholder: '2020',
            },
            {
                name: 'experienceYears',
                label: 'Années d\'expérience',
                type: 'number',
                required: true,
                min: 0,
                max: 50,
                placeholder: '5',
            },
        ],
    },
    {
        id: 'publics',
        title: 'Publics accompagnés',
        description: 'Quelles populations savez-vous accompagner ?',
        fields: [
            {
                name: 'publicAudiences',
                label: 'Publics cibles',
                type: 'multiselect',
                required: true,
                options: [
                    { value: 'mna', label: 'MNA - Mineurs Non Accompagnés' },
                    { value: 'ase', label: 'ASE - Protection de l\'enfance' },
                    { value: 'handicap-enfant', label: 'Handicap enfant (IME, ITEP)' },
                    { value: 'handicap-adulte', label: 'Handicap adulte (FH, FAM, MAS)' },
                    { value: 'petite-enfance', label: 'Petite enfance (0-6 ans)' },
                    { value: 'insertion', label: 'Insertion / CHRS' },
                    { value: 'psychiatrie', label: 'Psychiatrie' },
                    { value: 'seniors', label: 'Personnes âgées' },
                ],
                icon: 'Users',
            },
        ],
    },
    {
        id: 'mobility',
        title: 'Mobilité',
        fields: [
            {
                name: 'driverLicense',
                label: 'Permis B',
                type: 'boolean',
                required: true,
                defaultValue: false,
                helpText: 'Obligatoire pour beaucoup de missions éducatives',
            },
            {
                name: 'hasVehicle',
                label: 'Véhicule personnel',
                type: 'boolean',
                required: false,
                defaultValue: false,
                showIf: { field: 'driverLicense', value: true },
            },
            {
                name: 'radiusKm',
                label: 'Rayon d\'intervention (km)',
                type: 'number',
                required: true,
                min: 5,
                max: 100,
                placeholder: '30',
                defaultValue: '30',
            },
        ],
    },
    {
        id: 'services',
        title: 'Services proposés',
        fields: [
            {
                name: 'offersWorkshops',
                label: 'Je propose des ateliers (SocioLive)',
                type: 'boolean',
                required: false,
                defaultValue: false,
                helpText: 'Sophrologie, Art-thérapie, Sport adapté...',
            },
            {
                name: 'workshopTypes',
                label: 'Types d\'ateliers',
                type: 'multiselect',
                required: false,
                showIf: { field: 'offersWorkshops', value: true },
                options: [
                    { value: 'sophrologie', label: 'Sophrologie / Relaxation' },
                    { value: 'art-therapie', label: 'Art-thérapie' },
                    { value: 'sport-adapte', label: 'Sport adapté' },
                    { value: 'musique', label: 'Musicothérapie' },
                    { value: 'cuisine', label: 'Ateliers cuisine' },
                    { value: 'numerique', label: 'Initiation numérique' },
                ],
            },
            {
                name: 'hourlyRate',
                label: 'Taux horaire souhaité (€)',
                type: 'number',
                required: true,
                min: 12,
                max: 80,
                placeholder: '20',
                helpText: 'Tarif horaire brut',
            },
        ],
    },
];

// =============================================================================
// MISSION FIELDS - MEDICAL
// =============================================================================

const MEDICAL_MISSION_SECTIONS: FormSection[] = [
    {
        id: 'basics',
        title: 'Informations de la mission',
        fields: [
            { name: 'title', label: 'Intitulé du poste', type: 'text', required: true, placeholder: 'IDE - Remplacement arrêt maladie' },
            { name: 'description', label: 'Description', type: 'textarea', required: true, placeholder: 'Décrivez le contexte et les tâches...' },
            {
                name: 'jobType',
                label: 'Métier recherché',
                type: 'select',
                required: true,
                options: [
                    { value: 'ide', label: 'Infirmier(ère) - IDE' },
                    { value: 'as', label: 'Aide-Soignant(e) - AS' },
                    { value: 'aes', label: 'AES' },
                    { value: 'kine', label: 'Kinésithérapeute' },
                    { value: 'ergo', label: 'Ergothérapeute' },
                    { value: 'ash', label: 'ASH' },
                ],
            },
        ],
    },
    {
        id: 'clinical',
        title: 'Exigences cliniques',
        fields: [
            {
                name: 'technicalCare',
                label: 'Soins techniques requis',
                type: 'multiselect',
                required: false,
                options: [
                    { value: 'perf', label: 'Perfusion / IV' },
                    { value: 'pansements', label: 'Pansements' },
                    { value: 'stomie', label: 'Stomie' },
                    { value: 'diabete', label: 'Glycémie / Insuline' },
                    { value: 'oxygeno', label: 'Oxygénothérapie' },
                ],
            },
            {
                name: 'softwareRequired',
                label: 'Logiciel utilisé',
                type: 'select',
                required: false,
                options: [
                    { value: 'netsoins', label: 'NetSoins' },
                    { value: 'titan', label: 'Titan' },
                    { value: 'mediboard', label: 'Mediboard' },
                    { value: 'autre', label: 'Autre' },
                    { value: 'aucun', label: 'Formation sur place' },
                ],
            },
        ],
    },
    {
        id: 'schedule',
        title: 'Horaires',
        fields: [
            { name: 'startDate', label: 'Date de début', type: 'date', required: true },
            { name: 'endDate', label: 'Date de fin', type: 'date', required: true },
            {
                name: 'shiftType',
                label: 'Type de poste',
                type: 'select',
                required: true,
                options: [
                    { value: 'day', label: 'Jour (7h-19h)' },
                    { value: 'night', label: 'Nuit (19h-7h)' },
                    { value: 'morning', label: 'Matin (7h-14h)' },
                    { value: 'afternoon', label: 'Après-midi (14h-21h)' },
                ],
            },
            {
                name: 'isNightShift',
                label: 'Travail de nuit',
                type: 'boolean',
                required: false,
                defaultValue: false,
                helpText: 'Prime de nuit applicable',
            },
        ],
    },
    {
        id: 'compensation',
        title: 'Rémunération',
        fields: [
            { name: 'hourlyRate', label: 'Taux horaire proposé (€)', type: 'number', required: true, min: 15, max: 80, placeholder: '28' },
        ],
    },
];

// =============================================================================
// MISSION FIELDS - SOCIAL
// =============================================================================

const SOCIAL_MISSION_SECTIONS: FormSection[] = [
    {
        id: 'basics',
        title: 'Informations de la mission',
        fields: [
            { name: 'title', label: 'Intitulé du poste', type: 'text', required: true, placeholder: 'Éducateur Spécialisé - Remplacement congés' },
            { name: 'description', label: 'Description', type: 'textarea', required: true, placeholder: 'Décrivez le contexte et les principales missions...' },
            {
                name: 'jobType',
                label: 'Métier recherché',
                type: 'select',
                required: true,
                options: [
                    { value: 'es', label: 'Éducateur Spécialisé - ES' },
                    { value: 'me', label: 'Moniteur Éducateur - ME' },
                    { value: 'eje', label: 'EJE' },
                    { value: 'aes', label: 'AES' },
                    { value: 'tisf', label: 'TISF' },
                    { value: 'animateur', label: 'Animateur' },
                ],
            },
        ],
    },
    {
        id: 'public',
        title: 'Public accompagné',
        fields: [
            {
                name: 'targetAudience',
                label: 'Type de public',
                type: 'select',
                required: true,
                options: [
                    { value: 'mna', label: 'MNA - Mineurs Non Accompagnés' },
                    { value: 'ase', label: 'Protection de l\'enfance (ASE)' },
                    { value: 'handicap-enfant', label: 'Handicap enfant' },
                    { value: 'handicap-adulte', label: 'Handicap adulte' },
                    { value: 'petite-enfance', label: 'Petite enfance' },
                    { value: 'insertion', label: 'Insertion / Sans-abri' },
                ],
            },
            {
                name: 'structureType',
                label: 'Type de structure',
                type: 'select',
                required: true,
                options: [
                    { value: 'mecs', label: 'MECS' },
                    { value: 'ime', label: 'IME' },
                    { value: 'itep', label: 'ITEP' },
                    { value: 'fam', label: 'FAM' },
                    { value: 'mas', label: 'MAS' },
                    { value: 'chrs', label: 'CHRS' },
                    { value: 'creche', label: 'Crèche / Multi-accueil' },
                    { value: 'foyer', label: 'Foyer de vie' },
                ],
            },
            {
                name: 'residentialType',
                label: 'Mode d\'accueil',
                type: 'select',
                required: true,
                options: [
                    { value: 'internat', label: 'Internat (avec nuits)' },
                    { value: 'semi-internat', label: 'Semi-internat' },
                    { value: 'externat', label: 'Externat (jour uniquement)' },
                ],
            },
        ],
    },
    {
        id: 'requirements',
        title: 'Exigences',
        fields: [
            {
                name: 'driverLicenseRequired',
                label: 'Permis B obligatoire',
                type: 'boolean',
                required: false,
                defaultValue: true,
                helpText: 'Transports éducatifs, accompagnements',
            },
            {
                name: 'vehicleRequired',
                label: 'Véhicule personnel requis',
                type: 'boolean',
                required: false,
                defaultValue: false,
            },
        ],
    },
    {
        id: 'schedule',
        title: 'Horaires',
        fields: [
            { name: 'startDate', label: 'Date de début', type: 'date', required: true },
            { name: 'endDate', label: 'Date de fin', type: 'date', required: true },
            {
                name: 'shiftType',
                label: 'Type d\'horaires',
                type: 'select',
                required: true,
                options: [
                    { value: 'day', label: 'Journée' },
                    { value: 'split', label: 'Coupé (matin + soir)' },
                    { value: 'internat', label: 'Internat (avec nuitées)' },
                ],
            },
        ],
    },
    {
        id: 'compensation',
        title: 'Rémunération',
        fields: [
            { name: 'hourlyRate', label: 'Taux horaire proposé (€)', type: 'number', required: true, min: 12, max: 50, placeholder: '18' },
        ],
    },
];

// =============================================================================
// EXPORTS - Brand-Aware Getters
// =============================================================================

export const PROFILE_FIELDS: Record<AppMode, FormSection[]> = {
    MEDICAL: MEDICAL_PROFILE_SECTIONS,
    SOCIAL: SOCIAL_PROFILE_SECTIONS,
};

export const MISSION_FIELDS: Record<AppMode, FormSection[]> = {
    MEDICAL: MEDICAL_MISSION_SECTIONS,
    SOCIAL: SOCIAL_MISSION_SECTIONS,
};

/**
 * Get profile form sections for current brand
 */
export function getProfileSections(mode: AppMode): FormSection[] {
    return PROFILE_FIELDS[mode];
}

/**
 * Get mission form sections for current brand
 */
export function getMissionSections(mode: AppMode): FormSection[] {
    return MISSION_FIELDS[mode];
}

/**
 * Get all fields from sections as flat array
 */
export function getFlatFields(sections: FormSection[]): FieldDefinition[] {
    return sections.flatMap(section => section.fields);
}

/**
 * Get required field names for Zod validation
 */
export function getRequiredFieldNames(sections: FormSection[]): string[] {
    return getFlatFields(sections)
        .filter(f => f.required)
        .map(f => f.name);
}
