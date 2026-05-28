// ===========================================
// SOCIOPULSE SEED DATA - Representative Sample
// For Static Landing Page Rendering
// ===========================================

export interface SeedItem {
    type: 'MISSION' | 'PROFILE';
    category: 'SOIN' | 'EDUC' | 'HANDICAP' | 'SOCIAL' | 'SOCIOLIVE' | 'PETITE_ENFANCE';
    city: string;
    createdAt: string;
    data: {
        title: string;
        firstName: string | null;
        lastName: string | null;
        structureName: string | null;
        logoUrl?: string;
        description: string;
        tags: string[];
        hourlyRate: number;
        isAvailable: boolean;
    };
}

// Curated subset of seed data for landing page
export const SEED_DATA: SeedItem[] = [
    // === SOIN (6 items) ===
    {
        type: 'MISSION',
        category: 'SOIN',
        city: 'Paris',
        createdAt: '2026-01-02T18:37:26.789Z',
        data: {
            title: 'Remplacement arrêt maladie - Infirmier (IDE)',
            firstName: null,
            lastName: null,
            structureName: 'SSIAD La Victoire Paris',
            logoUrl: 'https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=400',
            description: 'Nous recherchons un(e) Infirmier (IDE) pour rejoindre notre équipe professionnelle à Paris.',
            tags: ['Technique', 'Handicap', 'FAM', 'MAS', 'Urgence'],
            hourlyRate: 33,
            isAvailable: true
        }
    },
    {
        type: 'MISSION',
        category: 'SOIN',
        city: 'Lyon',
        createdAt: '2026-01-02T23:16:07.885Z',
        data: {
            title: 'Accroissement d\'activité - Infirmier (IDE)',
            firstName: null,
            lastName: null,
            structureName: 'EHPAD Les Mimosas Lyon',
            logoUrl: 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=400',
            description: 'Nous recherchons un(e) Infirmier (IDE) pour rejoindre notre équipe familiale à Lyon.',
            tags: ['Coordination', 'EHPAD', 'Gériatrie', 'Urgence'],
            hourlyRate: 31,
            isAvailable: true
        }
    },
    {
        type: 'MISSION',
        category: 'SOIN',
        city: 'Toulouse',
        createdAt: '2026-01-02T00:32:12.230Z',
        data: {
            title: 'Besoin urgent suite désistement - Aide-Soignant (AS)',
            firstName: null,
            lastName: null,
            structureName: 'Clinique du Parc Toulouse',
            logoUrl: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=400',
            description: 'Nous recherchons un(e) Aide-Soignant (AS) pour rejoindre notre équipe professionnelle.',
            tags: ['Domicile', 'SSIAD', 'Autonomie', 'Urgence'],
            hourlyRate: 21,
            isAvailable: true
        }
    },
    {
        type: 'MISSION',
        category: 'SOIN',
        city: 'Bordeaux',
        createdAt: '2026-01-02T16:45:23.802Z',
        data: {
            title: 'Accroissement d\'activité - Infirmier (IDE)',
            firstName: null,
            lastName: null,
            structureName: 'SSIAD La Victoire Bordeaux',
            logoUrl: 'https://images.unsplash.com/photo-1631815588090-d4bfec5b1ccb?w=400',
            description: 'Nous recherchons un(e) Infirmier (IDE) pour rejoindre notre équipe familiale.',
            tags: ['Coordination', 'EHPAD', 'Gériatrie', 'Urgence'],
            hourlyRate: 33,
            isAvailable: true
        }
    },
    {
        type: 'MISSION',
        category: 'SOIN',
        city: 'Nantes',
        createdAt: '2026-01-03T05:24:17.529Z',
        data: {
            title: 'Besoin urgent suite désistement - Infirmier (IDE)',
            firstName: null,
            lastName: null,
            structureName: 'SSIAD La Victoire Nantes',
            logoUrl: 'https://images.unsplash.com/photo-1551076805-e1869033e561?w=400',
            description: 'Nous recherchons un(e) Infirmier (IDE) pour rejoindre notre équipe familiale à Nantes.',
            tags: ['Coordination', 'EHPAD', 'Gériatrie', 'Urgence'],
            hourlyRate: 34,
            isAvailable: true
        }
    },
    {
        type: 'MISSION',
        category: 'SOIN',
        city: 'Lille',
        createdAt: '2026-01-02T16:27:44.886Z',
        data: {
            title: 'Renfort week-end - Infirmier (IDE)',
            firstName: null,
            lastName: null,
            structureName: 'Hôpital St-Jean Lille',
            logoUrl: 'https://images.unsplash.com/photo-1584820927498-cfe5211fd8bf?w=400',
            description: 'Nous recherchons un(e) Infirmier (IDE) pour rejoindre notre équipe dynamique à Lille.',
            tags: ['Coordination', 'EHPAD', 'Gériatrie', 'Urgence'],
            hourlyRate: 33,
            isAvailable: true
        }
    },

    // === EDUC / HANDICAP / SOCIAL (6 items) ===
    {
        type: 'MISSION',
        category: 'EDUC',
        city: 'Paris',
        createdAt: '2026-01-02T05:36:37.921Z',
        data: {
            title: 'Besoin urgent suite désistement - Éducateur Spécialisé (ES)',
            firstName: null,
            lastName: null,
            structureName: 'Foyer du Bonheur Paris',
            logoUrl: 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=400',
            description: 'Nous recherchons un(e) Éducateur Spécialisé (ES) pour rejoindre notre équipe.',
            tags: ['MECS', 'Enfance', 'Protection', 'Urgence'],
            hourlyRate: 21,
            isAvailable: true
        }
    },
    {
        type: 'MISSION',
        category: 'HANDICAP',
        city: 'Lyon',
        createdAt: '2026-01-02T01:11:27.642Z',
        data: {
            title: 'Mission longue durée - Éducateur Spécialisé',
            firstName: null,
            lastName: null,
            structureName: 'Foyer de Vie Solaire Lyon',
            logoUrl: 'https://images.unsplash.com/photo-1582213782179-e0d53f98f2ca?w=400',
            description: 'Nous recherchons un(e) Éducateur Spécialisé pour rejoindre notre équipe dynamique.',
            tags: ['Autisme', 'TSA', 'ABA', 'Urgence'],
            hourlyRate: 25,
            isAvailable: true
        }
    },
    {
        type: 'MISSION',
        category: 'SOCIAL',
        city: 'Marseille',
        createdAt: '2026-01-02T14:25:59.047Z',
        data: {
            title: 'Besoin urgent suite désistement - CESF',
            firstName: null,
            lastName: null,
            structureName: 'CCAS Marseille',
            logoUrl: 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400',
            description: 'Nous recherchons un(e) CESF pour rejoindre notre équipe professionnelle.',
            tags: ['Budget', 'Logement', 'CESF', 'Urgence'],
            hourlyRate: 22,
            isAvailable: true
        }
    },
    {
        type: 'PROFILE',
        category: 'HANDICAP',
        city: 'Paris',
        createdAt: '2026-01-02T14:07:46.402Z',
        data: {
            title: 'Psychomotricien - TND / Petite Enfance - Paris',
            firstName: 'Emma',
            lastName: 'E.',
            structureName: null,
            description: 'Professionnel(le) engagé(e) en tant que Psychomotricien.',
            tags: ['TND', 'PetiteEnfance', 'Psychomotricité'],
            hourlyRate: 32,
            isAvailable: true
        }
    },
    {
        type: 'MISSION',
        category: 'EDUC',
        city: 'Bordeaux',
        createdAt: '2026-01-02T13:43:58.305Z',
        data: {
            title: 'Mission longue durée - Éducateur Spécialisé (ES)',
            firstName: null,
            lastName: null,
            structureName: 'Maison de l\'Enfance Bordeaux',
            logoUrl: 'https://images.unsplash.com/photo-1544717305-2782549b5136?w=400',
            description: 'Nous recherchons un(e) Éducateur Spécialisé (ES) pour rejoindre notre équipe.',
            tags: ['MECS', 'Enfance', 'Protection', 'Urgence'],
            hourlyRate: 21,
            isAvailable: true
        }
    },
    {
        type: 'MISSION',
        category: 'HANDICAP',
        city: 'Nantes',
        createdAt: '2026-01-02T11:44:46.151Z',
        data: {
            title: 'Accroissement d\'activité - Psychomotricien',
            firstName: null,
            lastName: null,
            structureName: 'IME Les Tilleuls Nantes',
            logoUrl: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400',
            description: 'Nous recherchons un(e) Psychomotricien pour rejoindre notre équipe dynamique.',
            tags: ['TND', 'PetiteEnfance', 'Psychomotricité', 'Urgence'],
            hourlyRate: 41,
            isAvailable: true
        }
    },

    // === SOCIOLIVE (8 items) ===
    {
        type: 'PROFILE',
        category: 'SOCIOLIVE',
        city: 'Strasbourg',
        createdAt: '2026-01-03T19:59:46.507Z',
        data: {
            title: 'Sophrologue - QVT Soignants - Strasbourg',
            firstName: 'Léa',
            lastName: 'O.',
            structureName: null,
            description: 'Professionnel(le) engagé(e) en tant que Sophrologue pour le bien-être des soignants.',
            tags: ['Sophrologie', 'QVT', 'Soignants'],
            hourlyRate: 72,
            isAvailable: false
        }
    },
    {
        type: 'PROFILE',
        category: 'SOCIOLIVE',
        city: 'Nice',
        createdAt: '2026-01-02T09:54:42.302Z',
        data: {
            title: 'Enseignant APA (Sport) - Prévention Chutes - Nice',
            firstName: 'Manon',
            lastName: 'B.',
            structureName: null,
            description: 'Professionnel(le) engagé(e) en tant que Enseignant APA (Sport).',
            tags: ['APA', 'Sport', 'Seniors'],
            hourlyRate: 71,
            isAvailable: true
        }
    },
    {
        type: 'PROFILE',
        category: 'SOCIOLIVE',
        city: 'Nantes',
        createdAt: '2026-01-02T07:16:10.931Z',
        data: {
            title: 'Sophrologue - QVT Soignants - Nantes',
            firstName: 'Inès',
            lastName: 'B.',
            structureName: null,
            description: 'Professionnel(le) engagé(e) en tant que Sophrologue.',
            tags: ['Sophrologie', 'QVT', 'Soignants'],
            hourlyRate: 57,
            isAvailable: false
        }
    },
    {
        type: 'MISSION',
        category: 'SOCIOLIVE',
        city: 'Paris',
        createdAt: '2026-01-02T05:37:15.295Z',
        data: {
            title: 'Mission longue durée - Sophrologue',
            firstName: null,
            lastName: null,
            structureName: 'Centre Social Paris',
            logoUrl: 'https://images.unsplash.com/photo-1545205597-3d9d02c29597?w=400',
            description: 'Nous recherchons un(e) Sophrologue pour rejoindre notre équipe bienveillante.',
            tags: ['Sophrologie', 'QVT', 'Soignants', 'Urgence'],
            hourlyRate: 76,
            isAvailable: true
        }
    },
    {
        type: 'PROFILE',
        category: 'SOCIOLIVE',
        city: 'Toulouse',
        createdAt: '2026-01-02T02:30:06.473Z',
        data: {
            title: 'Sophrologue - QVT Soignants - Toulouse',
            firstName: 'Hugo',
            lastName: 'F.',
            structureName: null,
            description: 'Professionnel(le) engagé(e) en tant que Sophrologue.',
            tags: ['Sophrologie', 'QVT', 'Soignants'],
            hourlyRate: 64,
            isAvailable: false
        }
    },
    {
        type: 'MISSION',
        category: 'SOCIOLIVE',
        city: 'Montpellier',
        createdAt: '2026-01-02T02:27:21.525Z',
        data: {
            title: 'Mission longue durée - Sophrologue',
            firstName: null,
            lastName: null,
            structureName: 'Résidence Services Seniors Montpellier',
            logoUrl: 'https://images.unsplash.com/photo-1544027993-37dbfe43562a?w=400',
            description: 'Nous recherchons un(e) Sophrologue pour rejoindre notre équipe.',
            tags: ['Sophrologie', 'QVT', 'Soignants', 'Urgence'],
            hourlyRate: 79,
            isAvailable: true
        }
    },
    {
        type: 'PROFILE',
        category: 'SOCIOLIVE',
        city: 'Lyon',
        createdAt: '2026-01-01T15:30:00.000Z',
        data: {
            title: 'Art-Thérapeute - Ateliers Créatifs - Lyon',
            firstName: 'Claire',
            lastName: 'M.',
            structureName: null,
            description: 'Art-thérapeute certifiée proposant des ateliers créatifs pour tous publics.',
            tags: ['ArtThérapie', 'Créativité', 'BienÊtre'],
            hourlyRate: 55,
            isAvailable: true
        }
    },
    {
        type: 'PROFILE',
        category: 'SOCIOLIVE',
        city: 'Marseille',
        createdAt: '2026-01-01T12:00:00.000Z',
        data: {
            title: 'Musicothérapeute - Séances Individuelles - Marseille',
            firstName: 'Thomas',
            lastName: 'R.',
            structureName: null,
            description: 'Musicothérapeute expérimenté pour séances individuelles et collectives.',
            tags: ['Musicothérapie', 'Relaxation', 'Seniors'],
            hourlyRate: 60,
            isAvailable: true
        }
    }
];

// Helper functions to filter by category
export const getSoinItems = () => SEED_DATA.filter(item => item.category === 'SOIN');
export const getEducItems = () => SEED_DATA.filter(item =>
    item.category === 'EDUC' || item.category === 'HANDICAP' || item.category === 'SOCIAL'
);
export const getSocioliveItems = () => SEED_DATA.filter(item => item.category === 'SOCIOLIVE');
