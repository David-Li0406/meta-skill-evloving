// ===========================================
// MOCK DATA - Landing Page Body Architecture
// APP_MODE aware content for SocioPulse/MedicoPulse
// ===========================================

import { isMedical } from '@/lib/brand';

// ========== TYPES ==========

export interface MissionItem {
    id: number;
    title: string;
    establishment: string;
    location: string;
    price: string;
    urgent: boolean;
    date: string;
    duration: string;
}

export interface TalentItem {
    id: number;
    name: string;
    role: string;
    available: boolean;
    rating: number;
    avatar: string;
    experience: string;
    verified: boolean;
}

export interface AtelierItem {
    id: number;
    title: string;
    host: string;
    date: string;
    time: string;
    price: string;
    image: string;
    category: string;
    spots: number;
}

export interface PartnerLogo {
    id: number;
    name: string;
    logo: string;
}

export interface BlogArticle {
    id: number;
    title: string;
    excerpt: string;
    category: string;
    readTime: string;
    image: string;
    slug: string;
}

export interface ImpactStat {
    label: string;
    value: number;
    suffix: string;
    prefix?: string;
}

// ========== MISSIONS DATA ==========

const SOCIAL_MISSIONS: MissionItem[] = [
    { id: 1, title: 'Éducateur Spécialisé', establishment: 'MECS Les Tilleuls', location: 'Lyon 7', price: '28€/h', urgent: true, date: '22 Jan', duration: 'Nuit' },
    { id: 2, title: 'Moniteur-Éducateur', establishment: 'IME Soleil Levant', location: 'Paris 15', price: '24€/h', urgent: false, date: '23 Jan', duration: 'Journée' },
    { id: 3, title: 'AES Internat', establishment: 'Foyer Espérance', location: 'Bordeaux', price: '22€/h', urgent: true, date: '21 Jan', duration: 'Week-end' },
    { id: 4, title: 'TISF Famille', establishment: 'CCAS Villeurbanne', location: 'Villeurbanne', price: '25€/h', urgent: false, date: '24 Jan', duration: 'Matinée' },
    { id: 5, title: 'Éducateur Jeunes Enfants', establishment: 'Crèche Arc-en-Ciel', location: 'Nantes', price: '26€/h', urgent: false, date: '25 Jan', duration: 'Journée' },
    { id: 6, title: 'Animateur Socio-culturel', establishment: 'MJC Confluence', location: 'Lyon 2', price: '20€/h', urgent: true, date: '22 Jan', duration: 'Soirée' },
    { id: 7, title: 'CESF', establishment: 'CAF Métropole', location: 'Toulouse', price: '27€/h', urgent: false, date: '26 Jan', duration: '3 jours' },
    { id: 8, title: 'Médiateur Familial', establishment: 'ASE Loire', location: 'Saint-Étienne', price: '30€/h', urgent: false, date: '27 Jan', duration: 'Demi-journée' },
    { id: 9, title: 'ES Appartement Thérapeutique', establishment: 'EPSM', location: 'Marseille', price: '29€/h', urgent: true, date: '21 Jan', duration: 'Nuit' },
    { id: 10, title: 'ME ITEP', establishment: 'ITEP Les Cèdres', location: 'Grenoble', price: '25€/h', urgent: false, date: '28 Jan', duration: 'Semaine' },
];

const MEDICAL_MISSIONS: MissionItem[] = [
    { id: 1, title: 'Infirmier DE Nuit', establishment: 'EHPAD Bel Automne', location: 'Lyon 3', price: '35€/h', urgent: true, date: '22 Jan', duration: 'Nuit' },
    { id: 2, title: 'Aide-Soignant', establishment: 'Clinique Pasteur', location: 'Paris 11', price: '22€/h', urgent: false, date: '23 Jan', duration: 'Journée' },
    { id: 3, title: 'IDE Week-end', establishment: 'SSIAD Domicile+', location: 'Bordeaux', price: '38€/h', urgent: true, date: '21 Jan', duration: 'Week-end' },
    { id: 4, title: 'AES Soin', establishment: 'FAM Les Iris', location: 'Toulouse', price: '21€/h', urgent: false, date: '24 Jan', duration: 'Journée' },
    { id: 5, title: 'Kiné Domicile', establishment: 'HAD Métropole', location: 'Nice', price: '45€/h', urgent: false, date: '25 Jan', duration: 'Tournée' },
    { id: 6, title: 'Infirmier Bloc', establishment: 'CHU Lyon Sud', location: 'Lyon', price: '42€/h', urgent: true, date: '22 Jan', duration: 'Garde' },
    { id: 7, title: 'AS EHPAD', establishment: 'Résidence Soleil', location: 'Marseille', price: '23€/h', urgent: false, date: '26 Jan', duration: '2 jours' },
    { id: 8, title: 'IDE Libéral', establishment: 'Cabinet Santé+', location: 'Nantes', price: '40€/h', urgent: false, date: '27 Jan', duration: 'Matinée' },
    { id: 9, title: 'Auxiliaire de Vie', establishment: 'SAAD Présence', location: 'Lille', price: '18€/h', urgent: true, date: '21 Jan', duration: 'Nuit' },
    { id: 10, title: 'Ergothérapeute', establishment: 'Centre Rééducation', location: 'Strasbourg', price: '35€/h', urgent: false, date: '28 Jan', duration: 'Semaine' },
];

// ========== TALENTS DATA ==========

const SOCIAL_TALENTS: TalentItem[] = [
    { id: 1, name: 'Marie L.', role: 'Éducatrice Spécialisée', available: true, rating: 4.9, avatar: 'https://i.pravatar.cc/80?img=1', experience: '8 ans', verified: true },
    { id: 2, name: 'Thomas D.', role: 'Moniteur-Éducateur', available: true, rating: 4.8, avatar: 'https://i.pravatar.cc/80?img=3', experience: '5 ans', verified: true },
    { id: 3, name: 'Sophie M.', role: 'AES', available: false, rating: 5.0, avatar: 'https://i.pravatar.cc/80?img=5', experience: '3 ans', verified: true },
    { id: 4, name: 'Lucas B.', role: 'Animateur', available: true, rating: 4.7, avatar: 'https://i.pravatar.cc/80?img=8', experience: '4 ans', verified: false },
    { id: 5, name: 'Emma R.', role: 'EJE', available: true, rating: 4.9, avatar: 'https://i.pravatar.cc/80?img=9', experience: '6 ans', verified: true },
    { id: 6, name: 'Hugo P.', role: 'ES MECS', available: false, rating: 4.6, avatar: 'https://i.pravatar.cc/80?img=11', experience: '7 ans', verified: true },
    { id: 7, name: 'Léa C.', role: 'TISF', available: true, rating: 4.8, avatar: 'https://i.pravatar.cc/80?img=16', experience: '2 ans', verified: true },
    { id: 8, name: 'Nathan V.', role: 'CESF', available: true, rating: 4.7, avatar: 'https://i.pravatar.cc/80?img=12', experience: '4 ans', verified: false },
    { id: 9, name: 'Camille G.', role: 'Psychomotricienne', available: true, rating: 5.0, avatar: 'https://i.pravatar.cc/80?img=20', experience: '5 ans', verified: true },
    { id: 10, name: 'Julien F.', role: 'Médiateur', available: false, rating: 4.5, avatar: 'https://i.pravatar.cc/80?img=14', experience: '3 ans', verified: true },
    { id: 11, name: 'Chloé M.', role: 'Assistante Sociale', available: true, rating: 4.9, avatar: 'https://i.pravatar.cc/80?img=23', experience: '9 ans', verified: true },
    { id: 12, name: 'Antoine L.', role: 'Éducateur PJJ', available: true, rating: 4.8, avatar: 'https://i.pravatar.cc/80?img=15', experience: '6 ans', verified: true },
];

const MEDICAL_TALENTS: TalentItem[] = [
    { id: 1, name: 'Claire D.', role: 'Infirmière DE', available: true, rating: 4.9, avatar: 'https://i.pravatar.cc/80?img=1', experience: '10 ans', verified: true },
    { id: 2, name: 'Pierre M.', role: 'Aide-Soignant', available: true, rating: 4.8, avatar: 'https://i.pravatar.cc/80?img=3', experience: '6 ans', verified: true },
    { id: 3, name: 'Isabelle R.', role: 'IDE Bloc', available: false, rating: 5.0, avatar: 'https://i.pravatar.cc/80?img=5', experience: '12 ans', verified: true },
    { id: 4, name: 'Marc T.', role: 'Kinésithérapeute', available: true, rating: 4.7, avatar: 'https://i.pravatar.cc/80?img=8', experience: '8 ans', verified: true },
    { id: 5, name: 'Julie B.', role: 'AS EHPAD', available: true, rating: 4.9, avatar: 'https://i.pravatar.cc/80?img=9', experience: '4 ans', verified: true },
    { id: 6, name: 'François L.', role: 'Infirmier Libéral', available: false, rating: 4.6, avatar: 'https://i.pravatar.cc/80?img=11', experience: '15 ans', verified: true },
    { id: 7, name: 'Nathalie P.', role: 'Ergothérapeute', available: true, rating: 4.8, avatar: 'https://i.pravatar.cc/80?img=16', experience: '7 ans', verified: true },
    { id: 8, name: 'David G.', role: 'AES Soin', available: true, rating: 4.7, avatar: 'https://i.pravatar.cc/80?img=12', experience: '3 ans', verified: false },
    { id: 9, name: 'Amélie V.', role: 'Psychomotricienne', available: true, rating: 5.0, avatar: 'https://i.pravatar.cc/80?img=20', experience: '5 ans', verified: true },
    { id: 10, name: 'Christophe N.', role: 'Ambulancier', available: false, rating: 4.5, avatar: 'https://i.pravatar.cc/80?img=14', experience: '9 ans', verified: true },
    { id: 11, name: 'Marine S.', role: 'Sage-femme', available: true, rating: 4.9, avatar: 'https://i.pravatar.cc/80?img=23', experience: '6 ans', verified: true },
    { id: 12, name: 'Olivier H.', role: 'Orthophoniste', available: true, rating: 4.8, avatar: 'https://i.pravatar.cc/80?img=15', experience: '4 ans', verified: true },
];

// ========== ATELIERS/SOCIOLIVE DATA ==========

const SOCIAL_ATELIERS: AtelierItem[] = [
    { id: 1, title: 'Atelier Sophrologie', host: 'Anne Dubois', date: '22 Jan', time: '14h00', price: '25€', image: 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop', category: 'Bien-être', spots: 8 },
    { id: 2, title: 'Gestion du Stress Pro', host: 'Marc Leroy', date: '23 Jan', time: '10h00', price: '35€', image: 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=400&h=300&fit=crop', category: 'Développement', spots: 12 },
    { id: 3, title: 'Écrits Professionnels', host: 'Claire Martin', date: '24 Jan', time: '18h00', price: '40€', image: 'https://images.unsplash.com/photo-1456324504439-367cee3b3c32?w=400&h=300&fit=crop', category: 'Formation', spots: 15 },
    { id: 4, title: 'Bientraitance & Éthique', host: 'Dr. Rousseau', date: '25 Jan', time: '9h00', price: '45€', image: 'https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?w=400&h=300&fit=crop', category: 'Formation', spots: 20 },
    { id: 5, title: 'Yoga Doux Collectif', host: 'Léa Chen', date: '26 Jan', time: '12h00', price: '15€', image: 'https://images.unsplash.com/photo-1599901860904-17e6ed7083a0?w=400&h=300&fit=crop', category: 'Bien-être', spots: 10 },
    { id: 6, title: 'Communication Non-Violente', host: 'Sophie Bernard', date: '27 Jan', time: '15h00', price: '30€', image: 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=400&h=300&fit=crop', category: 'Développement', spots: 16 },
    { id: 7, title: 'Méditation Guidée', host: 'Paul Moreau', date: '28 Jan', time: '8h00', price: '20€', image: 'https://images.unsplash.com/photo-1508672019048-805c876b67e2?w=400&h=300&fit=crop', category: 'Bien-être', spots: 6 },
    { id: 8, title: 'Prévention des TMS', host: 'Dr. Lambert', date: '29 Jan', time: '11h00', price: '35€', image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop', category: 'Santé', spots: 25 },
];

// ========== PARTNER LOGOS ==========

export const PARTNER_LOGOS: PartnerLogo[] = [
    { id: 1, name: 'FEHAP', logo: '/partners/fehap.svg' },
    { id: 2, name: 'URIOPSS', logo: '/partners/uriopss.svg' },
    { id: 3, name: 'ARS', logo: '/partners/ars.svg' },
    { id: 4, name: 'Croix-Rouge', logo: '/partners/croix-rouge.svg' },
    { id: 5, name: 'CNSA', logo: '/partners/cnsa.svg' },
    { id: 6, name: 'Korian', logo: '/partners/korian.svg' },
    { id: 7, name: 'Orpea', logo: '/partners/orpea.svg' },
    { id: 8, name: 'DomusVi', logo: '/partners/domusvi.svg' },
];

// ========== BLOG/MAG DATA ==========

const SOCIAL_BLOG: BlogArticle[] = [
    {
        id: 1,
        title: 'Comment recruter un éducateur spécialisé en 2026 ?',
        excerpt: 'Les meilleures pratiques pour attirer les talents du médico-social dans un marché tendu.',
        category: 'Recrutement',
        readTime: '5 min',
        image: 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=600&h=400&fit=crop',
        slug: 'recruter-educateur-specialise-2026',
    },
    {
        id: 2,
        title: 'SocioLive : La révolution des ateliers en ligne',
        excerpt: 'Découvrez comment les ateliers virtuels transforment le bien-être des équipes.',
        category: 'Innovation',
        readTime: '4 min',
        image: 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600&h=400&fit=crop',
        slug: 'sociolive-revolution-ateliers-ligne',
    },
    {
        id: 3,
        title: '5 astuces pour fidéliser vos remplaçants',
        excerpt: 'Créez une relation durable avec vos professionnels pour garantir la continuité.',
        category: 'Management',
        readTime: '6 min',
        image: 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=600&h=400&fit=crop',
        slug: 'fideliser-remplacants-conseils',
    },
];

const MEDICAL_BLOG: BlogArticle[] = [
    {
        id: 1,
        title: 'Pénurie d\'infirmiers : Solutions innovantes pour 2026',
        excerpt: 'Stratégies concrètes pour pallier le manque de personnel soignant dans votre établissement.',
        category: 'Actualité',
        readTime: '5 min',
        image: 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=600&h=400&fit=crop',
        slug: 'penurie-infirmiers-solutions-2026',
    },
    {
        id: 2,
        title: 'Le paiement instantané : un atout pour recruter',
        excerpt: 'Comment le paiement sous 48h attire les meilleurs profils soignants.',
        category: 'Finance',
        readTime: '4 min',
        image: 'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=600&h=400&fit=crop',
        slug: 'paiement-instantane-recrutement',
    },
    {
        id: 3,
        title: 'EHPAD : Organiser les remplacements d\'été',
        excerpt: 'Anticipez la période estivale avec notre guide complet de gestion des congés.',
        category: 'Organisation',
        readTime: '7 min',
        image: 'https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?w=600&h=400&fit=crop',
        slug: 'ehpad-remplacements-ete',
    },
];

// ========== IMPACT STATS ==========

export const IMPACT_STATS: ImpactStat[] = [
    { label: 'Heures de mission', value: 450000, suffix: 'h', prefix: '+' },
    { label: 'Satisfaction', value: 98, suffix: '%' },
    { label: 'Missions réussies', value: 2500, suffix: '', prefix: '+' },
    { label: 'Établissements partenaires', value: 850, suffix: '', prefix: '+' },
];

// ========== GETTERS (APP_MODE AWARE) ==========

export function getMissions(): MissionItem[] {
    return isMedical() ? MEDICAL_MISSIONS : SOCIAL_MISSIONS;
}

export function getTalents(): TalentItem[] {
    return isMedical() ? MEDICAL_TALENTS : SOCIAL_TALENTS;
}

export function getAteliers(): AtelierItem[] {
    // Ateliers only shown for SOCIAL mode
    return isMedical() ? [] : SOCIAL_ATELIERS;
}

export function getBlogArticles(): BlogArticle[] {
    return isMedical() ? MEDICAL_BLOG : SOCIAL_BLOG;
}

export function getPartnerLogos(): PartnerLogo[] {
    return PARTNER_LOGOS;
}

export function getImpactStats(): ImpactStat[] {
    return IMPACT_STATS;
}
