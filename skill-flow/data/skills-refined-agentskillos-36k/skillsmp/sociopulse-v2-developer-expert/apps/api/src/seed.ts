import { PrismaClient } from '@prisma/client';
import * as bcrypt from 'bcrypt';

/**
 * Production-ready seed runner
 * Compiled to dist/seed.js by nest build
 * Run with: node dist/seed.js
 */

const prisma = new PrismaClient();

const hoursFromNow = (hours: number) => new Date(Date.now() + hours * 60 * 60 * 1000);
const pic = (seed: string, width = 1200, height = 800) => `https://picsum.photos/seed/${seed}/${width}/${height}`;
const avatar = (img: number) => `https://i.pravatar.cc/150?img=${img}`;

async function main() {
    console.log('🌱 Starting database seed...');

    const passwordHash = await bcrypt.hash('password123', 10);

    // Clean database
    console.log('🧹 Cleaning existing data...');
    await prisma.externalNews.deleteMany();
    await prisma.transaction.deleteMany();
    await prisma.message.deleteMany();
    await prisma.review.deleteMany();
    await prisma.booking.deleteMany();
    await prisma.missionApplication.deleteMany();
    await prisma.contract.deleteMany();
    await prisma.reliefMission.deleteMany();
    await prisma.service.deleteMany();
    await prisma.availabilitySlot.deleteMany();
    await prisma.talentPoolMember.deleteMany();
    await prisma.talentPool.deleteMany();
    await prisma.profile.deleteMany();
    await prisma.establishment.deleteMany();
    await prisma.notification.deleteMany();
    await prisma.post.deleteMany();
    await prisma.pointLog.deleteMany();
    await prisma.tag.deleteMany();
    await prisma.adminNote.deleteMany();
    await prisma.auditLog.deleteMany();
    await prisma.user.deleteMany();

    // Create Admin
    console.log('👤 Creating admin...');
    await prisma.user.create({
        data: {
            email: 'admin@sociopulse.fr',
            passwordHash,
            role: 'ADMIN',
            status: 'VERIFIED',
            walletBalance: 500000,
            referralCode: 'admin0001',
            profile: {
                create: {
                    firstName: 'Admin',
                    lastName: 'System',
                    bio: 'Super Admin',
                    specialties: [],
                    diplomas: [],
                },
            },
        },
    });

    // Create Clients
    console.log('🏢 Creating clients...');
    const clientsData = [
        { email: 'ehpad.paris@exemple.fr', name: 'EHPAD Les Jardins', type: 'EHPAD', city: 'Paris', postalCode: '75004', address: '12 Rue de Rivoli' },
        { email: 'ime.paris@exemple.fr', name: "IME L'Espoir", type: 'IME', city: 'Paris', postalCode: '75001', address: '150 Rue Saint-Honoré' },
        { email: 'creche.lyon@exemple.fr', name: 'Crèche Les Petits Pas', type: 'Crèche', city: 'Lyon', postalCode: '69002', address: '5 Place Bellecour' },
        { email: 'mecs.lille@exemple.fr', name: 'MECS Horizon', type: 'MECS', city: 'Lille', postalCode: '59000', address: '8 Rue Nationale' },
    ];

    const clients: any[] = [];
    for (let i = 0; i < clientsData.length; i++) {
        const d = clientsData[i];
        const client = await prisma.user.create({
            data: {
                email: d.email,
                passwordHash,
                role: 'CLIENT',
                status: 'VERIFIED',
                walletBalance: 200000,
                establishment: {
                    create: {
                        name: d.name,
                        type: d.type,
                        city: d.city,
                        address: d.address,
                        postalCode: d.postalCode,
                        contactName: 'Direction',
                        contactRole: 'Direction',
                        siret: `SEED${String(i + 1).padStart(12, '0')}`,
                        logoUrl: pic(`est-${d.name.toLowerCase().replace(/\s/g, '-')}`, 128, 128),
                    },
                },
            },
            include: { establishment: true },
        });
        clients.push(client);
    }

    // Create Talents
    console.log('🧑‍⚕️ Creating talents...');
    const talentsData = [
        { email: 'jean.dupont@exemple.fr', firstName: 'Jean', lastName: 'Dupont', headline: 'Infirmier - Renfort de nuit', city: 'Paris', postalCode: '75011', hourlyRate: 35, isVideoEnabled: false, avatarImg: 12, specialties: ['soins', 'nuit', 'gériatrie'] },
        { email: 'marie.curie@exemple.fr', firstName: 'Marie', lastName: 'Curie', headline: 'Aide-soignante - EHPAD', city: 'Paris', postalCode: '75004', hourlyRate: 28, isVideoEnabled: false, avatarImg: 32, specialties: ['toilette', 'repas', 'EHPAD'] },
        { email: 'paul.verlaine@exemple.fr', firstName: 'Paul', lastName: 'Verlaine', headline: 'Éducateur spécialisé - TSA', city: 'Lyon', postalCode: '69002', hourlyRate: 32, isVideoEnabled: true, avatarImg: 5, specialties: ['autisme', 'adolescents', 'TSA'] },
        { email: 'ines.martin@exemple.fr', firstName: 'Inès', lastName: 'Martin', headline: 'Coach parental - Visio', city: 'Nantes', postalCode: '44000', hourlyRate: 55, isVideoEnabled: true, avatarImg: 47, specialties: ['parentalité', 'routines', 'visio'] },
        { email: 'yassine.ben@exemple.fr', firstName: 'Yassine', lastName: 'Benali', headline: 'Psychomotricien - Ateliers seniors', city: 'Bordeaux', postalCode: '33000', hourlyRate: 45, isVideoEnabled: false, avatarImg: 19, specialties: ['motricité', 'seniors', 'stimulation'] },
        { email: 'clara.durand@exemple.fr', firstName: 'Clara', lastName: 'Durand', headline: 'Orthophoniste - Troubles DYS', city: 'Lille', postalCode: '59000', hourlyRate: 60, isVideoEnabled: true, avatarImg: 23, specialties: ['dyslexie', 'langage', 'visio'] },
    ];

    const talents: any[] = [];
    for (let i = 0; i < talentsData.length; i++) {
        const t = talentsData[i];
        const talent = await prisma.user.create({
            data: {
                email: t.email,
                passwordHash,
                role: 'TALENT',
                status: 'VERIFIED',
                stripeAccountId: `acct_seed_${i + 1}`,
                stripeOnboarded: true,
                profile: {
                    create: {
                        firstName: t.firstName,
                        lastName: t.lastName,
                        avatarUrl: avatar(t.avatarImg),
                        headline: t.headline,
                        bio: `Disponible pour des missions de renfort. ${t.headline}.`,
                        city: t.city,
                        postalCode: t.postalCode,
                        specialties: t.specialties,
                        diplomas: [{ name: "Diplôme d'État", year: 2018 }],
                        hourlyRate: t.hourlyRate,
                        isVideoEnabled: t.isVideoEnabled,
                        averageRating: 4.6,
                        totalReviews: 18,
                    },
                },
            },
            include: { profile: true },
        });
        talents.push(talent);
    }

    // Create Services
    console.log('🛍️ Creating services...');
    const serviceTemplates = [
        { name: 'Atelier Boxe éducative', category: 'Sport adapté', basePrice: 70, shortDescription: 'Un atelier structuré pour canaliser l\'énergie et renforcer la confiance.', type: 'WORKSHOP' },
        { name: 'Atelier Mémoire', category: 'Seniors', basePrice: 55, shortDescription: 'Stimulation cognitive douce, ludique et progressive.', type: 'WORKSHOP' },
        { name: 'Coaching parental (Visio)', category: 'Educat\'heure', basePrice: 60, shortDescription: 'Un rendez-vous clair pour débloquer une situation du quotidien.', type: 'COACHING_VIDEO' },
        { name: 'Atelier Arts & émotions', category: 'Art-thérapie', basePrice: 65, shortDescription: 'Créer pour apaiser : une bulle créative guidée.', type: 'WORKSHOP' },
        { name: 'Suivi éducatif (Visio)', category: 'Accompagnement', basePrice: 55, shortDescription: 'Un accompagnement régulier, simple et actionnable.', type: 'COACHING_VIDEO' },
        { name: 'Atelier Motricité', category: 'Psychomotricité', basePrice: 60, shortDescription: 'Parcours et jeux moteurs adaptés à tous les niveaux.', type: 'WORKSHOP' },
    ];

    for (let i = 0; i < talents.length; i++) {
        const talent = talents[i];
        if (!talent.profile) continue;
        const template = serviceTemplates[i % serviceTemplates.length];
        const slug = `${template.name.toLowerCase().replace(/[^a-z0-9]+/g, '-')}-${talent.profile.firstName.toLowerCase()}-${i}`;

        await prisma.service.create({
            data: {
                profileId: talent.profile.id,
                name: template.name,
                slug,
                description: `${template.shortDescription}\n\n${talent.profile.headline || ''}`,
                shortDescription: template.shortDescription,
                type: template.type as any,
                category: template.category,
                basePrice: template.basePrice,
                tags: ['wall', 'featured', template.category.toLowerCase()],
                imageUrl: pic(`svc-${slug}`),
                galleryUrls: [pic(`svc-${slug}-2`), pic(`svc-${slug}-3`)],
                isActive: true,
            },
        });
    }

    // Create Missions
    console.log('🆘 Creating relief missions...');
    const missionTemplates = [
        { title: 'Renfort IDE Nuit - urgence', jobTitle: 'Infirmier', urgencyLevel: 'CRITICAL', hourlyRate: 38, skills: ['nuit', 'soins', 'EHPAD'], description: 'Remplacement arrêt maladie. Besoin cette nuit.' },
        { title: 'Renfort éducateur TSA (week-end)', jobTitle: 'Éducateur spécialisé', urgencyLevel: 'HIGH', hourlyRate: 32, skills: ['TSA', 'groupe', 'communication'], description: 'Accompagnement atelier et temps collectif.' },
        { title: 'Renfort crèche - ouverture', jobTitle: 'EJE', urgencyLevel: 'HIGH', hourlyRate: 28, skills: ['petite_enfance', 'animation', 'sécurité'], description: 'Besoin sur l\'accueil du matin + activités.' },
        { title: 'Veille éducative - nuit', jobTitle: 'Éducateur', urgencyLevel: 'MEDIUM', hourlyRate: 30, skills: ['veilles', 'mecs', 'gestion_crise'], description: 'Veille en MECS, présence sécurisante.' },
        { title: 'Atelier motricité - adultes', jobTitle: 'Psychomotricien', urgencyLevel: 'MEDIUM', hourlyRate: 42, skills: ['motricité', 'équilibre', 'adapté'], description: 'Animation + accompagnement, profil psychomotricien apprécié.' },
        { title: 'Renfort AS Journée', jobTitle: 'Aide-Soignant', urgencyLevel: 'HIGH', hourlyRate: 28, skills: ['toilette', 'repas', 'EHPAD'], description: 'Besoin de renfort pour la journée.' },
    ];

    for (let i = 0; i < missionTemplates.length; i++) {
        const m = missionTemplates[i];
        const client = clients[i % clients.length];
        const est = client?.establishment;
        if (!client || !est) continue;

        await prisma.reliefMission.create({
            data: {
                clientId: client.id,
                title: m.title,
                description: m.description,
                jobTitle: m.jobTitle,
                urgencyLevel: m.urgencyLevel as any,
                status: 'OPEN',
                startDate: hoursFromNow(6 + i * 12),
                endDate: hoursFromNow(14 + i * 12),
                hourlyRate: m.hourlyRate,
                estimatedHours: 8,
                totalBudget: m.hourlyRate * 8,
                address: est.address || 'Adresse à préciser',
                city: est.city,
                postalCode: est.postalCode || '',
                requiredSkills: m.skills,
                requiredDiplomas: ["Diplôme d'État"],
                isNightShift: m.title.toLowerCase().includes('nuit'),
            },
        });
    }

    // Create External News
    console.log('📰 Creating external news...');
    const newsData = [
        { title: 'Réforme Grand Âge : ce qui change en 2025', source: 'Le Monde', url: 'https://lemonde.fr', excerpt: 'Nouvelles mesures pour les EHPAD et le maintien à domicile.' },
        { title: 'Ségur de la santé : revalorisation des salaires', source: 'Ministère', url: 'https://sante.gouv.fr', excerpt: 'Point sur les augmentations prévues pour le médico-social.' },
        { title: 'Pénurie de soignants : les solutions innovantes', source: 'Hospimedia', url: 'https://hospimedia.fr', excerpt: 'Les établissements se réinventent face aux difficultés de recrutement.' },
    ];

    for (const news of newsData) {
        await prisma.externalNews.create({
            data: {
                title: news.title,
                source: news.source,
                url: news.url,
                excerpt: news.excerpt,
                publishedAt: new Date(),
                isActive: true,
            },
        });
    }

    console.log('');
    console.log('✅ Database seeding completed!');
    console.log('');
    console.log('📊 Summary:');
    console.log(`   - 1 Admin`);
    console.log(`   - ${clients.length} Clients (Establishments)`);
    console.log(`   - ${talents.length} Talents`);
    console.log(`   - ${talents.length} Services`);
    console.log(`   - ${missionTemplates.length} Missions`);
    console.log(`   - ${newsData.length} News articles`);
    console.log('');
    console.log('🔐 Login credentials:');
    console.log('   Admin: admin@sociopulse.fr / password123');
    console.log('   Talent: jean.dupont@exemple.fr / password123');
    console.log('   Client: ehpad.paris@exemple.fr / password123');
}

main()
    .catch((e) => {
        console.error('❌ Seed failed:', e);
        process.exit(1);
    })
    .finally(async () => {
        await prisma.$disconnect();
    });
