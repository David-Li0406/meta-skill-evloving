
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

// --- CONFIGURATION ---
// Use /tmp for Docker containers (non-writable /app), otherwise use cwd
const OUTPUT_DIR = process.env.NODE_ENV === 'production' ? os.tmpdir() : process.cwd();
const OUTPUT_FILE = path.join(OUTPUT_DIR, 'sociopulse_seed_2026.json');
const CITIES = [
    'Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice',
    'Nantes', 'Montpellier', 'Strasbourg', 'Bordeaux', 'Lille'
];

// --- DATA MATRICES ---
const ROLES = [
    // PÔLE SOIN
    { title: 'Aide-Soignant (AS)', expertise: 'Nuit & Gériatrie', category: 'SOIN', minPrice: 16, maxPrice: 22, tags: ['Nuit', 'Gériatrie', 'Soins'] },
    { title: 'Aide-Soignant (AS)', expertise: 'Domicile / SSIAD', category: 'SOIN', minPrice: 16, maxPrice: 22, tags: ['Domicile', 'SSIAD', 'Autonomie'] },
    { title: 'Infirmier (IDE)', expertise: 'Coordinateur / EHPAD', category: 'SOIN', minPrice: 30, maxPrice: 45, tags: ['Coordination', 'EHPAD', 'Gériatrie'] },
    { title: 'Infirmier (IDE)', expertise: 'Technique / FAM-MAS', category: 'SOIN', minPrice: 30, maxPrice: 45, tags: ['Technique', 'Handicap', 'FAM', 'MAS'] },
    { title: 'AES / AMP', expertise: 'Vie Sociale', category: 'SOIN', minPrice: 16, maxPrice: 22, tags: ['VieSociale', 'Accompagnement', 'Animation'] },
    // PÔLE ÉDUCATIF
    { title: 'Éducateur Spécialisé (ES)', expertise: 'Protection Enfance (MECS)', category: 'EDUC', minPrice: 20, maxPrice: 28, tags: ['MECS', 'Enfance', 'Protection'] },
    { title: 'Éducateur Spécialisé (ES)', expertise: 'AEMO / Famille', category: 'EDUC', minPrice: 20, maxPrice: 28, tags: ['AEMO', 'Famille', 'Domicile'] },
    { title: 'Moniteur-Éducateur (ME)', expertise: 'Foyer / Quotidien', category: 'EDUC', minPrice: 20, maxPrice: 28, tags: ['Foyer', 'Quotidien', 'Autonomie'] },
    { title: 'Surveillant de Nuit', expertise: 'Sécurité / CHRS', category: 'EDUC', minPrice: 16, maxPrice: 22, tags: ['Nuit', 'Sécurité', 'CHRS'] },
    // PÔLE HANDICAP
    { title: 'Éducateur Spécialisé', expertise: 'Autisme / TSA (ABA)', category: 'HANDICAP', minPrice: 20, maxPrice: 28, tags: ['Autisme', 'TSA', 'ABA'] },
    { title: 'Moniteur d\'Atelier', expertise: 'ESAT / Production', category: 'HANDICAP', minPrice: 20, maxPrice: 28, tags: ['ESAT', 'Production', 'Accompagnement'] },
    { title: 'Psychomotricien', expertise: 'TND / Petite Enfance', category: 'HANDICAP', minPrice: 30, maxPrice: 45, tags: ['TND', 'PetiteEnfance', 'Psychomotricité'] },
    // PÔLE SOCIAL
    { title: 'Assistant Service Social', expertise: 'Droits / Hôpital', category: 'SOCIAL', minPrice: 20, maxPrice: 28, tags: ['Hôpital', 'Droits', 'Social'] },
    { title: 'CESF', expertise: 'Budget / Logement', category: 'SOCIAL', minPrice: 20, maxPrice: 28, tags: ['Budget', 'Logement', 'CESF'] },
    { title: 'Conseiller Insertion (CIP)', expertise: 'Emploi', category: 'SOCIAL', minPrice: 20, maxPrice: 28, tags: ['Insertion', 'Emploi', 'CIP'] },
    // PÔLE PETITE ENFANCE
    { title: 'EJE', expertise: 'Direction Crèche', category: 'PETITE_ENFANCE', minPrice: 20, maxPrice: 28, tags: ['Crèche', 'Direction', 'PetiteEnfance'] },
    { title: 'Auxiliaire de Puériculture', expertise: 'Soins Bébé', category: 'PETITE_ENFANCE', minPrice: 16, maxPrice: 22, tags: ['Crèche', 'Soins', 'Bébé'] },
    // PÔLE SOCIOLIVE (ATELIERS)
    { title: 'Art-thérapeute', expertise: 'Estime de soi', category: 'SOCIOLIVE', minPrice: 50, maxPrice: 80, tags: ['ArtThérapie', 'EstimeDeSoi', 'Atelier'] },
    { title: 'Enseignant APA (Sport)', expertise: 'Prévention Chutes', category: 'SOCIOLIVE', minPrice: 50, maxPrice: 80, tags: ['APA', 'Sport', 'Seniors'] },
    { title: 'Sophrologue', expertise: 'QVT Soignants', category: 'SOCIOLIVE', minPrice: 50, maxPrice: 80, tags: ['Sophrologie', 'QVT', 'Soignants'] },
];

// --- HELPER DATA ---
const FIRST_NAMES = ['Julien', 'Marie', 'Sophie', 'Thomas', 'Nicolas', 'Camille', 'Léa', 'Lucas', 'Emma', 'Hugo', 'Chloé', 'Alexandre', 'Manon', 'Maxime', 'Inès'];
const LAST_NAMES = ['A.', 'B.', 'C.', 'D.', 'E.', 'F.', 'G.', 'H.', 'I.', 'J.', 'K.', 'L.', 'M.', 'N.', 'O.', 'P.'];

const SOFT_SKILLS = [
    'empathie naturelle', 'gestion du stress', 'travail en équipe', 'écoute active', 'patience',
    'adaptabilité', 'communication bienveillante', 'sens des responsabilités', 'gestion de crise'
];

const HARD_SKILLS_TEMPLATES = {
    'SOIN': ['soins de nursing', 'protocoles d\'hygiène', 'prise de constantes', 'gestes d\'urgence', 'logiciels de soins'],
    'EDUC': ['rédaction de rapports', 'conduite d\'entretien', 'gestion de conflits', 'animation de groupe', 'projets personnalisés'],
    'HANDICAP': ['méthode ABA', 'LSF', 'makaton', 'gestion des troubles du comportement', 'accompagnement au repas'],
    'SOCIAL': ['accès aux droits', 'dossiers administratifs', 'médiation', 'droit du travail', 'dispositifs d\'insertion'],
    'PETITE_ENFANCE': ['développement de l\'enfant', 'activités d\'éveil', 'règles de sécurité', 'alimentation du jeune enfant'],
    'SOCIOLIVE': ['animation de groupe', 'pédagogie active', 'maîtrise des techniques', 'adaptation public', 'évaluation']
};

const MISSION_CONTEXTS = [
    'Remplacement arrêt maladie', 'Renfort période estivale', 'Accroissement d\'activité',
    'Besoin urgent suite désistement', 'Renfort week-end', 'Mission longue durée'
];

const STRUCTURE_NAMES = {
    'SOIN': ['EHPAD Les Mimosas', 'Clinique du Parc', 'SSIAD La Victoire', 'Hôpital St-Jean'],
    'EDUC': ['MECS L\'Envol', 'Foyer du Bonheur', 'Association Espoir', 'Maison de l\'Enfance'],
    'HANDICAP': ['IME Les Tilleuls', 'MAS Horizon', 'ESAT L\'Avenir', 'Foyer de Vie Solaire'],
    'SOCIAL': ['CCAS', 'Mission Locale', 'CHRS Le Refuge', 'Association Solidarité'],
    'PETITE_ENFANCE': ['Crèche Les Petits Pas', 'Halte-Garderie Câlins', 'Micro-crèche Bulles'],
    'SOCIOLIVE': ['Résidence Services Seniors', 'Centre Social', 'Entreprise Santé', 'Association Quartier']
};

const IMAGE_KEYWORDS = {
    'SOIN': 'nurse,hospital,medical',
    'EDUC': 'social work,teaching,meeting',
    'HANDICAP': 'disability support,therapy,care',
    'SOCIAL': 'office,meeting,consultation',
    'PETITE_ENFANCE': 'kindergarten,toys,baby',
    'SOCIOLIVE': 'workshop,group,yoga'
};

// --- HELPERS ---
function getRandom(arr: any[]) {
    return arr[Math.floor(Math.random() * arr.length)];
}

function getRandomInt(min: number, max: number) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Generate a random date within the last X days
function getRandomDateRecent(days: number = 30): string {
    const end = new Date();
    const start = new Date();
    start.setDate(start.getDate() - days);

    // Random time between start and end
    const randomTime = start.getTime() + Math.random() * (end.getTime() - start.getTime());
    return new Date(randomTime).toISOString();
}

function generateBio(category: string, roleTitle: string) {
    const soft = `${getRandom(SOFT_SKILLS)} et ${getRandom(SOFT_SKILLS)}`;
    const hardList: string[] = (HARD_SKILLS_TEMPLATES as any)[category] || [];
    const hard = hardList.length > 0 ? `${getRandom(hardList)} et ${getRandom(hardList)}` : 'compétences techniques solides';

    return `Professionnel(le) engagé(e) en tant que ${roleTitle}. Je mets à profit mon ${soft} pour accompagner au mieux les publics. Maîtrise des ${hard}. Habitué(e) aux environnements exigeants.`;
}

function generateMissionDescription(roleTitle: string, city: string) {
    const ambiance = ['dynamique', 'bienveillante', 'professionnelle', 'familiale'];
    const publicType = ['personnes âgées', 'enfants', 'adultes en situation de handicap', 'familles en difficulté'];
    return `Nous recherchons un(e) ${roleTitle} pour rejoindre notre équipe ${getRandom(ambiance)} à ${city}. Vous accompagnerez un public de ${getRandom(publicType)}. Cadre de travail agréable et stimulant.`;
}

// Ensure uniqueness of images by appending a random seed param
function generateImageUrl(category: string): string {
    const keywords = (IMAGE_KEYWORDS as any)[category] || 'business';
    const unique = Math.floor(Math.random() * 1000);
    // Using Unsplash Source (deprecated but still works sometimes) or LoremFlickr or similar
    // Let's use LoremFlickr which is reliable for placeholders
    const keyword = keywords.split(',')[0]; // pick first keyword
    return `https://loremflickr.com/320/240/${keyword}?lock=${unique}`;
}

// --- GENERATOR ---
const dataObjects: any[] = [];

console.log('🚀 Starting Seed Generation for SocioPulse 2026...');

CITIES.forEach(city => {
    ROLES.forEach(role => {
        // 1. Generate PROFILE
        const isAvailable = Math.random() > 0.3; // 70% chance true, 30% chance false
        const firstName = getRandom(FIRST_NAMES);
        const lastName = getRandom(LAST_NAMES);

        const profile = {
            type: 'PROFILE',
            category: role.category,
            city: city,
            createdAt: getRandomDateRecent(30),
            data: {
                title: `${role.title} - ${role.expertise} - ${city}`,
                firstName: firstName,
                lastName: lastName,
                structureName: null,
                description: generateBio(role.category, role.title),
                tags: role.tags,
                hourlyRate: getRandomInt(role.minPrice, role.maxPrice),
                isAvailable: isAvailable
            }
        };
        dataObjects.push(profile);

        // 2. Generate MISSION
        const structureList = (STRUCTURE_NAMES as any)[role.category] || ['Structure médico-sociale'];
        const structureName = `${getRandom(structureList)} ${city}`; // Add city
        const missionTitle = `${getRandom(MISSION_CONTEXTS)} - ${role.title}`;

        const mission = {
            type: 'MISSION',
            category: role.category,
            city: city,
            createdAt: getRandomDateRecent(14), // Missions are fresher (last 2 weeks)
            data: {
                title: missionTitle,
                firstName: null,
                lastName: null,
                structureName: structureName,
                logoUrl: generateImageUrl(role.category),
                description: generateMissionDescription(role.title, city),
                tags: [...role.tags, 'Urgence'],
                hourlyRate: getRandomInt(role.minPrice, role.maxPrice),
                isAvailable: true // Missions are generally 'open'
            }
        };
        dataObjects.push(mission);
    });
});

// Sort output by createdAt DESC (Newest first) so user doesn't have to wait for app sort to work perfectly
dataObjects.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());

console.log(`✅ Generated ${dataObjects.length} items.`);

// --- OUTPUT ---
try {
    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(dataObjects, null, 2), 'utf-8');
    console.log(`💾 File saved to: ${OUTPUT_FILE}`);
} catch (error) {
    console.error('Error writing file:', error);
}
