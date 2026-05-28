// =============================================================================
// SOS CONFIG - Exhaustive Job Definitions for SocioPulse & MedicoPulse
// =============================================================================
// This file defines every job type and its constraints for both brands.
// Used by SOS Renfort forms, talent profiles, and mission matching.

// =============================================================================
// TYPES & INTERFACES
// =============================================================================

/**
 * Job category classification
 */
export type JobCategory = 'SOIN' | 'EDUC' | 'HOTELLERIE' | 'ADMIN' | 'MANAGEMENT' | 'PARAMEDICAL';

/**
 * Complete job definition with all constraints
 */
export interface JobDefinition {
  /** Unique identifier (slug format) */
  id: string;
  /** Display label in French */
  label: string;
  /** Short code/acronym */
  shortCode?: string;
  /** Job category for filtering and grouping */
  category: JobCategory;
  /** Whether a diploma/certification upload is required */
  requiresDiploma: boolean;
  /** Whether ADELI number verification is required (Medical professionals) */
  requiresAdeli: boolean;
  /** Whether the job can include night shifts */
  canDoNight: boolean;
  /** Whether a driver's license (Permis B) is typically required */
  requiresDriverLicense: boolean;
  /** List of specialty/context tags for filtering */
  specialties: string[];
  /** Optional description of the role */
  description?: string;
  /** Minimum hourly rate suggestion (€) */
  minHourlyRate?: number;
  /** Maximum hourly rate suggestion (€) */
  maxHourlyRate?: number;
}

/**
 * Brand-specific configuration
 */
export interface BrandSOSConfig {
  brand: 'MEDICAL' | 'SOCIAL';
  brandName: string;
  jobs: JobDefinition[];
  categories: JobCategory[];
  defaultUrgencyLevels: string[];
}

// =============================================================================
// MEDICAL JOBS (MedicoPulse)
// =============================================================================

export const MEDICAL_JOBS: JobDefinition[] = [
  // -------------------------------------------------------------------------
  // SOINS - Nursing & Care
  // -------------------------------------------------------------------------
  {
    id: 'ide',
    label: 'Infirmier(ère) Diplômé(e) d\'État',
    shortCode: 'IDE',
    category: 'SOIN',
    requiresDiploma: true,
    requiresAdeli: true,
    canDoNight: true,
    requiresDriverLicense: false,
    specialties: [
      'Urgences',
      'Gériatrie',
      'Soins Palliatifs',
      'Psychiatrie',
      'Chirurgie',
      'Réanimation',
      'Pédiatrie',
      'Oncologie',
      'Cardiologie',
      'Dialyse',
      'HAD (Hospitalisation à Domicile)',
      'SSIAD',
      'Médecine Générale',
    ],
    description: 'Infirmier diplômé d\'État avec numéro ADELI valide',
    minHourlyRate: 22,
    maxHourlyRate: 35,
  },
  {
    id: 'as',
    label: 'Aide-Soignant(e)',
    shortCode: 'AS',
    category: 'SOIN',
    requiresDiploma: true,
    requiresAdeli: false,
    canDoNight: true,
    requiresDriverLicense: false,
    specialties: [
      'Gériatrie',
      'Handicap',
      'EHPAD',
      'SSR (Soins de Suite)',
      'Psychiatrie',
      'Domicile',
      'Long Séjour',
      'Médecine',
      'Chirurgie',
    ],
    description: 'Aide-soignant(e) diplômé(e) d\'État (DEAS)',
    minHourlyRate: 14,
    maxHourlyRate: 20,
  },
  {
    id: 'aes-soin',
    label: 'Accompagnant Éducatif et Social (Soin)',
    shortCode: 'AES',
    category: 'SOIN',
    requiresDiploma: true,
    requiresAdeli: false,
    canDoNight: true,
    requiresDriverLicense: false,
    specialties: [
      'Domicile',
      'Structure',
      'EHPAD',
      'Handicap',
      'Vie Quotidienne',
      'Aide aux Actes Essentiels',
    ],
    description: 'AES spécialisé accompagnement soins et vie quotidienne',
    minHourlyRate: 13,
    maxHourlyRate: 18,
  },
  {
    id: 'ash',
    label: 'Agent de Service Hospitalier',
    shortCode: 'ASH',
    category: 'HOTELLERIE',
    requiresDiploma: false,
    requiresAdeli: false,
    canDoNight: true,
    requiresDriverLicense: false,
    specialties: [
      'Bio-nettoyage',
      'Hôtellerie',
      'Distribution Repas',
      'Hygiène des Locaux',
      'Lingerie',
    ],
    description: 'Agent de service hospitalier - entretien et hygiène',
    minHourlyRate: 12,
    maxHourlyRate: 15,
  },
  {
    id: 'ash-ff',
    label: 'ASH Faisant Fonction Aide-Soignant',
    shortCode: 'ASH FF',
    category: 'SOIN',
    requiresDiploma: false,
    requiresAdeli: false,
    canDoNight: true,
    requiresDriverLicense: false,
    specialties: [
      'Soins de Base',
      'Aide à la Toilette',
      'Accompagnement Repas',
      'Mobilisation',
      'EHPAD',
    ],
    description: 'ASH avec missions de soins de base sous supervision',
    minHourlyRate: 12,
    maxHourlyRate: 16,
  },

  // -------------------------------------------------------------------------
  // BLOC OPÉRATOIRE - Surgical
  // -------------------------------------------------------------------------
  {
    id: 'ibode',
    label: 'Infirmier(ère) de Bloc Opératoire',
    shortCode: 'IBODE',
    category: 'SOIN',
    requiresDiploma: true,
    requiresAdeli: true,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'Chirurgie Orthopédique',
      'Chirurgie Viscérale',
      'Chirurgie Cardiaque',
      'Neurochirurgie',
      'Urologie',
      'ORL',
      'Ophtalmologie',
      'Gynécologie',
      'Instrumentation',
      'Aide Opératoire',
    ],
    description: 'Infirmier(ère) de bloc opératoire diplômé(e) d\'État',
    minHourlyRate: 28,
    maxHourlyRate: 45,
  },
  {
    id: 'iade',
    label: 'Infirmier(ère) Anesthésiste',
    shortCode: 'IADE',
    category: 'SOIN',
    requiresDiploma: true,
    requiresAdeli: true,
    canDoNight: true,
    requiresDriverLicense: false,
    specialties: [
      'Réanimation',
      'Bloc Opératoire',
      'SSPI (Salle de Réveil)',
      'Urgences',
      'SMUR',
      'Obstétrique',
    ],
    description: 'Infirmier(ère) anesthésiste diplômé(e) d\'État',
    minHourlyRate: 32,
    maxHourlyRate: 50,
  },

  // -------------------------------------------------------------------------
  // PARAMÉDICAL - Allied Health
  // -------------------------------------------------------------------------
  {
    id: 'kine',
    label: 'Masseur-Kinésithérapeute',
    shortCode: 'MK',
    category: 'PARAMEDICAL',
    requiresDiploma: true,
    requiresAdeli: true,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'SSR (Soins de Suite et Réadaptation)',
      'Rééducation',
      'Neurologie',
      'Orthopédie',
      'Respiratoire',
      'Gériatrie',
      'Pédiatrie',
      'Sport',
    ],
    description: 'Masseur-kinésithérapeute diplômé d\'État',
    minHourlyRate: 25,
    maxHourlyRate: 40,
  },
  {
    id: 'ergo',
    label: 'Ergothérapeute',
    shortCode: 'Ergo',
    category: 'PARAMEDICAL',
    requiresDiploma: true,
    requiresAdeli: true,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'SSR',
      'Rééducation',
      'Gériatrie',
      'Handicap',
      'Neurologie',
      'Pédiatrie',
      'Aménagement Domicile',
      'Aides Techniques',
    ],
    description: 'Ergothérapeute diplômé(e) d\'État',
    minHourlyRate: 22,
    maxHourlyRate: 35,
  },
  {
    id: 'psychomot',
    label: 'Psychomotricien(ne)',
    shortCode: 'Psychomot',
    category: 'PARAMEDICAL',
    requiresDiploma: true,
    requiresAdeli: true,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'SSR',
      'Rééducation',
      'Gériatrie',
      'Pédiatrie',
      'Psychiatrie',
      'Handicap',
      'Autisme',
      'Troubles DYS',
    ],
    description: 'Psychomotricien(ne) diplômé(e) d\'État',
    minHourlyRate: 22,
    maxHourlyRate: 35,
  },
  {
    id: 'orthophoniste',
    label: 'Orthophoniste',
    shortCode: 'Ortho',
    category: 'PARAMEDICAL',
    requiresDiploma: true,
    requiresAdeli: true,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'Troubles du Langage',
      'Troubles de la Déglutition',
      'Neurologie',
      'Pédiatrie',
      'Gériatrie',
      'AVC',
    ],
    description: 'Orthophoniste diplômé(e)',
    minHourlyRate: 25,
    maxHourlyRate: 40,
  },
  {
    id: 'dieteticien',
    label: 'Diététicien(ne)',
    shortCode: 'Diét',
    category: 'PARAMEDICAL',
    requiresDiploma: true,
    requiresAdeli: true,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'Nutrition Clinique',
      'Diabétologie',
      'Oncologie',
      'Gériatrie',
      'Pédiatrie',
      'TCA (Troubles Alimentaires)',
    ],
    description: 'Diététicien(ne) diplômé(e)',
    minHourlyRate: 20,
    maxHourlyRate: 32,
  },

  // -------------------------------------------------------------------------
  // MANAGEMENT & ADMIN
  // -------------------------------------------------------------------------
  {
    id: 'cadre-sante',
    label: 'Cadre de Santé',
    shortCode: 'CDS',
    category: 'MANAGEMENT',
    requiresDiploma: true,
    requiresAdeli: false,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'Management d\'Équipe',
      'Gestion de Service',
      'Coordination',
      'Qualité',
      'Formation',
    ],
    description: 'Cadre de santé diplômé - management et coordination',
    minHourlyRate: 28,
    maxHourlyRate: 45,
  },
  {
    id: 'secretaire-medicale',
    label: 'Secrétaire Médicale',
    shortCode: 'SM',
    category: 'ADMIN',
    requiresDiploma: false, // Optional but preferred
    requiresAdeli: false,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'Accueil',
      'Gestion RDV',
      'Facturation',
      'DIM (Information Médicale)',
      'Archives',
      'Standard',
    ],
    description: 'Secrétaire médicale - accueil et gestion administrative',
    minHourlyRate: 13,
    maxHourlyRate: 18,
  },
  {
    id: 'brancardier',
    label: 'Brancardier',
    shortCode: 'Branc',
    category: 'SOIN',
    requiresDiploma: false,
    requiresAdeli: false,
    canDoNight: true,
    requiresDriverLicense: false,
    specialties: [
      'Transport Patient',
      'Bloc Opératoire',
      'Imagerie',
      'Urgences',
    ],
    description: 'Brancardier - transport des patients',
    minHourlyRate: 12,
    maxHourlyRate: 16,
  },
  {
    id: 'agent-accueil',
    label: 'Agent d\'Accueil',
    shortCode: 'AA',
    category: 'ADMIN',
    requiresDiploma: false,
    requiresAdeli: false,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'Accueil Physique',
      'Standard Téléphonique',
      'Orientation',
      'Admission',
    ],
    description: 'Agent d\'accueil et d\'orientation',
    minHourlyRate: 12,
    maxHourlyRate: 15,
  },
];

// =============================================================================
// SOCIAL JOBS (SocioPulse)
// =============================================================================

export const SOCIAL_JOBS: JobDefinition[] = [
  // -------------------------------------------------------------------------
  // ÉDUCATIF - Educational & Social Work
  // -------------------------------------------------------------------------
  {
    id: 'es',
    label: 'Éducateur(trice) Spécialisé(e)',
    shortCode: 'ES',
    category: 'EDUC',
    requiresDiploma: true,
    requiresAdeli: false,
    canDoNight: true,
    requiresDriverLicense: true,
    specialties: [
      'ASE (Aide Sociale à l\'Enfance)',
      'Handicap',
      'Insertion',
      'Prévention Spécialisée',
      'Protection Judiciaire',
      'MECS (Maison d\'Enfants)',
      'IME',
      'ITEP',
      'Foyer de Vie',
      'MAS/FAM',
      'CHRS',
      'Addictologie',
    ],
    description: 'Éducateur spécialisé diplômé d\'État (DEES)',
    minHourlyRate: 16,
    maxHourlyRate: 25,
  },
  {
    id: 'me',
    label: 'Moniteur(trice) Éducateur(trice)',
    shortCode: 'ME',
    category: 'EDUC',
    requiresDiploma: true,
    requiresAdeli: false,
    canDoNight: true,
    requiresDriverLicense: true,
    specialties: [
      'Internat',
      'Foyer',
      'MECS',
      'IME',
      'ITEP',
      'Handicap',
      'Accueil de Jour',
      'Semi-Internat',
    ],
    description: 'Moniteur éducateur diplômé d\'État (DEME)',
    minHourlyRate: 14,
    maxHourlyRate: 20,
  },
  {
    id: 'eje',
    label: 'Éducateur(trice) de Jeunes Enfants',
    shortCode: 'EJE',
    category: 'EDUC',
    requiresDiploma: true,
    requiresAdeli: false,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'Crèche',
      'Multi-Accueil',
      'Pouponnière',
      'PMI',
      'Halte-Garderie',
      'LAEP',
      'ASE Petite Enfance',
    ],
    description: 'Éducateur de jeunes enfants diplômé d\'État (DEEJE)',
    minHourlyRate: 16,
    maxHourlyRate: 24,
  },
  {
    id: 'aes-educ',
    label: 'Accompagnant Éducatif et Social',
    shortCode: 'AES',
    category: 'EDUC',
    requiresDiploma: true,
    requiresAdeli: false,
    canDoNight: true,
    requiresDriverLicense: false,
    specialties: [
      'Vie en Structure',
      'Domicile',
      'Éducation Inclusive',
      'Handicap',
      'EHPAD',
      'Autisme',
      'AESH (Scolaire)',
    ],
    description: 'AES diplômé - accompagnement social et éducatif',
    minHourlyRate: 13,
    maxHourlyRate: 18,
  },
  {
    id: 'tisf',
    label: 'Technicien(ne) Intervention Sociale et Familiale',
    shortCode: 'TISF',
    category: 'EDUC',
    requiresDiploma: true,
    requiresAdeli: false,
    canDoNight: false,
    requiresDriverLicense: true,
    specialties: [
      'Domicile',
      'Soutien à la Parentalité',
      'Protection de l\'Enfance',
      'PMI',
      'Aide à Domicile',
      'Gestion du Quotidien',
    ],
    description: 'TISF diplômé - intervention sociale et familiale à domicile',
    minHourlyRate: 14,
    maxHourlyRate: 20,
  },
  {
    id: 'ass',
    label: 'Assistant(e) de Service Social',
    shortCode: 'ASS',
    category: 'EDUC',
    requiresDiploma: true,
    requiresAdeli: false,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'Accès aux Droits',
      'Polyvalence de Secteur',
      'Protection de l\'Enfance',
      'Hôpital',
      'Entreprise',
      'CPAM',
      'CAF',
      'Insertion',
    ],
    description: 'Assistant de service social diplômé d\'État (DEASS)',
    minHourlyRate: 18,
    maxHourlyRate: 28,
  },
  {
    id: 'cesf',
    label: 'Conseiller(ère) en Économie Sociale et Familiale',
    shortCode: 'CESF',
    category: 'EDUC',
    requiresDiploma: true,
    requiresAdeli: false,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'Budget',
      'Logement',
      'Insertion',
      'Accompagnement Social',
      'Prévention Expulsions',
      'Éducation Budgétaire',
    ],
    description: 'CESF diplômé - conseil en économie sociale familiale',
    minHourlyRate: 16,
    maxHourlyRate: 24,
  },
  {
    id: 'animateur',
    label: 'Animateur(trice) Socio-Éducatif',
    shortCode: 'Anim',
    category: 'EDUC',
    requiresDiploma: false,
    requiresAdeli: false,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'BPJEPS',
      'Centre Social',
      'EHPAD',
      'Handicap',
      'Jeunesse',
      'Loisirs',
      'Activités Manuelles',
    ],
    description: 'Animateur socio-éducatif (BPJEPS, BAFA+)',
    minHourlyRate: 12,
    maxHourlyRate: 18,
  },

  // -------------------------------------------------------------------------
  // NUIT & SURVEILLANCE
  // -------------------------------------------------------------------------
  {
    id: 'surveillant-nuit-qualifie',
    label: 'Surveillant(e) de Nuit Qualifié(e)',
    shortCode: 'SNQ',
    category: 'EDUC',
    requiresDiploma: true,
    requiresAdeli: false,
    canDoNight: true,
    requiresDriverLicense: false,
    specialties: [
      'SSIAP',
      'Gestion des Conflits',
      'Premiers Secours',
      'Internat',
      'Foyer',
      'MECS',
      'MAS/FAM',
      'CHRS',
    ],
    description: 'Surveillant de nuit qualifié avec certification',
    minHourlyRate: 14,
    maxHourlyRate: 20,
  },
  {
    id: 'veilleur-nuit',
    label: 'Veilleur(euse) de Nuit',
    shortCode: 'VN',
    category: 'EDUC',
    requiresDiploma: false,
    requiresAdeli: false,
    canDoNight: true,
    requiresDriverLicense: false,
    specialties: [
      'Sécurité',
      'Rondes',
      'Accompagnement Nuit',
      'CHRS',
      'Foyer',
      'EHPAD',
    ],
    description: 'Veilleur de nuit - surveillance et sécurité nocturne',
    minHourlyRate: 12,
    maxHourlyRate: 16,
  },

  // -------------------------------------------------------------------------
  // HOTELLERIE & LOGISTIQUE
  // -------------------------------------------------------------------------
  {
    id: 'maitresse-maison',
    label: 'Maître(sse) de Maison',
    shortCode: 'MM',
    category: 'HOTELLERIE',
    requiresDiploma: false,
    requiresAdeli: false,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'Cuisine',
      'Logistique',
      'Entretien',
      'Linge',
      'Vie Quotidienne',
      'Accompagnement Repas',
      'Foyer',
      'MECS',
    ],
    description: 'Maître(sse) de maison - gestion vie quotidienne',
    minHourlyRate: 12,
    maxHourlyRate: 16,
  },
  {
    id: 'agent-entretien',
    label: 'Agent d\'Entretien',
    shortCode: 'AE',
    category: 'HOTELLERIE',
    requiresDiploma: false,
    requiresAdeli: false,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'Nettoyage',
      'Hygiène',
      'Bio-nettoyage',
      'Espaces Verts',
    ],
    description: 'Agent d\'entretien des locaux',
    minHourlyRate: 11,
    maxHourlyRate: 14,
  },
  {
    id: 'cuisinier',
    label: 'Cuisinier(ère)',
    shortCode: 'Cuis',
    category: 'HOTELLERIE',
    requiresDiploma: false,
    requiresAdeli: false,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'Collectivité',
      'Régimes Spéciaux',
      'HACCP',
      'Textures Modifiées',
    ],
    description: 'Cuisinier en collectivité',
    minHourlyRate: 13,
    maxHourlyRate: 18,
  },

  // -------------------------------------------------------------------------
  // MANAGEMENT & ENCADREMENT
  // -------------------------------------------------------------------------
  {
    id: 'chef-service',
    label: 'Chef(fe) de Service',
    shortCode: 'CDS',
    category: 'MANAGEMENT',
    requiresDiploma: true,
    requiresAdeli: false,
    canDoNight: false,
    requiresDriverLicense: true,
    specialties: [
      'CAFERUIS',
      'Management d\'Équipe',
      'Coordination',
      'Projet de Service',
      'Évaluation',
      'Partenariat',
    ],
    description: 'Chef de service éducatif ou social (CAFERUIS)',
    minHourlyRate: 22,
    maxHourlyRate: 35,
  },
  {
    id: 'coordinateur',
    label: 'Coordinateur(trice)',
    shortCode: 'Coord',
    category: 'MANAGEMENT',
    requiresDiploma: false,
    requiresAdeli: false,
    canDoNight: false,
    requiresDriverLicense: true,
    specialties: [
      'Parcours',
      'Projet',
      'Équipe',
      'Réseau',
    ],
    description: 'Coordinateur de parcours ou de projet',
    minHourlyRate: 18,
    maxHourlyRate: 28,
  },

  // -------------------------------------------------------------------------
  // PSYCHOLOGIE & THÉRAPIE
  // -------------------------------------------------------------------------
  {
    id: 'psychologue',
    label: 'Psychologue',
    shortCode: 'Psy',
    category: 'PARAMEDICAL',
    requiresDiploma: true,
    requiresAdeli: true,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'Analyse des Pratiques',
      'Enfant',
      'Adolescent',
      'Adulte',
      'Clinique',
      'Neuropsychologie',
      'Travail',
      'Supervision',
      'Trauma',
    ],
    description: 'Psychologue diplômé avec numéro ADELI',
    minHourlyRate: 35,
    maxHourlyRate: 60,
  },
  {
    id: 'art-therapeute',
    label: 'Art-Thérapeute',
    shortCode: 'AT',
    category: 'PARAMEDICAL',
    requiresDiploma: true,
    requiresAdeli: false,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'Arts Plastiques',
      'Musique',
      'Danse',
      'Théâtre',
      'Handicap',
      'Psychiatrie',
      'Gériatrie',
    ],
    description: 'Art-thérapeute certifié',
    minHourlyRate: 25,
    maxHourlyRate: 40,
  },

  // -------------------------------------------------------------------------
  // ADMINISTRATIF
  // -------------------------------------------------------------------------
  {
    id: 'secretaire-social',
    label: 'Secrétaire Médico-Social',
    shortCode: 'SMS',
    category: 'ADMIN',
    requiresDiploma: false,
    requiresAdeli: false,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'Accueil',
      'Gestion Dossiers',
      'Planification',
      'Facturation',
      'Relations Familles',
    ],
    description: 'Secrétaire en établissement médico-social',
    minHourlyRate: 13,
    maxHourlyRate: 18,
  },
  {
    id: 'agent-administratif',
    label: 'Agent Administratif',
    shortCode: 'AA',
    category: 'ADMIN',
    requiresDiploma: false,
    requiresAdeli: false,
    canDoNight: false,
    requiresDriverLicense: false,
    specialties: [
      'Saisie',
      'Classement',
      'Courrier',
      'Standard',
      'Comptabilité',
    ],
    description: 'Agent administratif polyvalent',
    minHourlyRate: 12,
    maxHourlyRate: 16,
  },
];

// =============================================================================
// BRAND CONFIGURATIONS
// =============================================================================

export const MEDICAL_CONFIG: BrandSOSConfig = {
  brand: 'MEDICAL',
  brandName: 'MedicoPulse',
  jobs: MEDICAL_JOBS,
  categories: ['SOIN', 'PARAMEDICAL', 'HOTELLERIE', 'ADMIN', 'MANAGEMENT'],
  defaultUrgencyLevels: ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
};

export const SOCIAL_CONFIG: BrandSOSConfig = {
  brand: 'SOCIAL',
  brandName: 'SocioPulse',
  jobs: SOCIAL_JOBS,
  categories: ['EDUC', 'PARAMEDICAL', 'HOTELLERIE', 'ADMIN', 'MANAGEMENT'],
  defaultUrgencyLevels: ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
};

// =============================================================================
// HELPERS & HOOKS
// =============================================================================

/**
 * Get the SOS configuration based on the current app mode
 * Automatically detects brand from NEXT_PUBLIC_APP_MODE env variable
 */
export function getSOSConfig(): BrandSOSConfig {
  const appMode = process.env.NEXT_PUBLIC_APP_MODE || 'SOCIAL';
  return appMode === 'MEDICAL' ? MEDICAL_CONFIG : SOCIAL_CONFIG;
}

/**
 * Get all jobs for the current brand
 */
export function getJobs(): JobDefinition[] {
  return getSOSConfig().jobs;
}

/**
 * Get a specific job by ID
 */
export function getJobById(id: string): JobDefinition | undefined {
  const config = getSOSConfig();
  return config.jobs.find((job) => job.id === id);
}

/**
 * Get jobs filtered by category
 */
export function getJobsByCategory(category: JobCategory): JobDefinition[] {
  return getSOSConfig().jobs.filter((job) => job.category === category);
}

/**
 * Get jobs that require ADELI number
 */
export function getAdeliRequiredJobs(): JobDefinition[] {
  return getSOSConfig().jobs.filter((job) => job.requiresAdeli);
}

/**
 * Get jobs that can do night shifts
 */
export function getNightShiftJobs(): JobDefinition[] {
  return getSOSConfig().jobs.filter((job) => job.canDoNight);
}

/**
 * Get jobs that require driver's license
 */
export function getDriverLicenseJobs(): JobDefinition[] {
  return getSOSConfig().jobs.filter((job) => job.requiresDriverLicense);
}

/**
 * Get all unique specialties for a category
 */
export function getSpecialtiesByCategory(category: JobCategory): string[] {
  const jobs = getJobsByCategory(category);
  const specialties = new Set<string>();
  jobs.forEach((job) => job.specialties.forEach((s) => specialties.add(s)));
  return Array.from(specialties).sort();
}

/**
 * Get all unique specialties for all jobs
 */
export function getAllSpecialties(): string[] {
  const jobs = getJobs();
  const specialties = new Set<string>();
  jobs.forEach((job) => job.specialties.forEach((s) => specialties.add(s)));
  return Array.from(specialties).sort();
}

/**
 * Search jobs by query (label, shortCode, or specialty)
 */
export function searchJobs(query: string): JobDefinition[] {
  const normalizedQuery = query.toLowerCase().trim();
  if (!normalizedQuery) return getJobs();

  return getSOSConfig().jobs.filter((job) => {
    return (
      job.label.toLowerCase().includes(normalizedQuery) ||
      job.shortCode?.toLowerCase().includes(normalizedQuery) ||
      job.specialties.some((s) => s.toLowerCase().includes(normalizedQuery))
    );
  });
}

// =============================================================================
// REACT HOOK
// =============================================================================

/**
 * React hook to get SOS configuration for the current brand
 * Automatically returns the correct list based on NEXT_PUBLIC_APP_MODE
 * 
 * @example
 * ```tsx
 * function MyComponent() {
 *   const { jobs, brand, categories } = useSOSConfig();
 *   return (
 *     <select>
 *       {jobs.map(job => (
 *         <option key={job.id} value={job.id}>{job.label}</option>
 *       ))}
 *     </select>
 *   );
 * }
 * ```
 */
export function useSOSConfig(): BrandSOSConfig & {
  getJobById: (id: string) => JobDefinition | undefined;
  getJobsByCategory: (category: JobCategory) => JobDefinition[];
  searchJobs: (query: string) => JobDefinition[];
  getAdeliRequiredJobs: () => JobDefinition[];
  getNightShiftJobs: () => JobDefinition[];
  getDriverLicenseJobs: () => JobDefinition[];
  getAllSpecialties: () => string[];
} {
  const config = getSOSConfig();

  return {
    ...config,
    getJobById: (id: string) => config.jobs.find((job) => job.id === id),
    getJobsByCategory: (category: JobCategory) =>
      config.jobs.filter((job) => job.category === category),
    searchJobs: (query: string) => {
      const normalizedQuery = query.toLowerCase().trim();
      if (!normalizedQuery) return config.jobs;
      return config.jobs.filter(
        (job) =>
          job.label.toLowerCase().includes(normalizedQuery) ||
          job.shortCode?.toLowerCase().includes(normalizedQuery) ||
          job.specialties.some((s) => s.toLowerCase().includes(normalizedQuery))
      );
    },
    getAdeliRequiredJobs: () => config.jobs.filter((job) => job.requiresAdeli),
    getNightShiftJobs: () => config.jobs.filter((job) => job.canDoNight),
    getDriverLicenseJobs: () => config.jobs.filter((job) => job.requiresDriverLicense),
    getAllSpecialties: () => {
      const specialties = new Set<string>();
      config.jobs.forEach((job) => job.specialties.forEach((s) => specialties.add(s)));
      return Array.from(specialties).sort();
    },
  };
}

// =============================================================================
// CONSTANTS FOR FORM BUILDING
// =============================================================================

export const CATEGORY_LABELS: Record<JobCategory, string> = {
  SOIN: 'Soins',
  EDUC: 'Éducatif & Social',
  HOTELLERIE: 'Hôtellerie & Logistique',
  ADMIN: 'Administratif',
  MANAGEMENT: 'Encadrement',
  PARAMEDICAL: 'Paramédical',
};

export const URGENCY_LABELS = {
  CRITICAL: { label: 'Immédiat', color: 'red', description: 'Dans les 2h' },
  HIGH: { label: 'Urgent', color: 'orange', description: 'Sous 24h' },
  MEDIUM: { label: 'Standard', color: 'yellow', description: 'Sous 48h' },
  LOW: { label: 'Planifié', color: 'green', description: 'Sous 1 semaine' },
} as const;

export const SHIFT_TYPES = {
  JOUR: { label: 'Journée', hours: '07h-19h' },
  NUIT: { label: 'Nuit', hours: '19h-07h' },
  MATIN: { label: 'Matin', hours: '07h-14h' },
  APRES_MIDI: { label: 'Après-midi', hours: '14h-21h' },
  COUPE: { label: 'Coupé', hours: 'Variable' },
} as const;

export type ShiftType = keyof typeof SHIFT_TYPES;
export type UrgencyLevel = keyof typeof URGENCY_LABELS;
