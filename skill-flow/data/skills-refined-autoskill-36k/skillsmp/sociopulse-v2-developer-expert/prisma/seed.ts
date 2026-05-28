import {
  BookingStatus,
  MissionStatus,
  MissionUrgency,
  TagCategory,
  PostCategory,
  PostType,
  PrismaClient,
  ServiceType,
  TransactionStatus,
  TransactionType,
  UserStatus,
  ContractStatus,
  ComplianceStatus,
  MissionMessageType,
} from '@prisma/client';
import * as bcrypt from 'bcrypt';

const prisma = new PrismaClient();

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

const hoursFromNow = (hours: number) => new Date(Date.now() + hours * 60 * 60 * 1000);
const daysFromNow = (days: number) => new Date(Date.now() + days * 24 * 60 * 60 * 1000);
const hoursAgo = (hours: number) => new Date(Date.now() - hours * 60 * 60 * 1000);
const daysAgo = (days: number) => new Date(Date.now() - days * 24 * 60 * 60 * 1000);

const slugify = (value: string) =>
  value
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '')
    .slice(0, 60);

const pic = (seed: string, width = 1200, height = 800) =>
  `https://picsum.photos/seed/${seed}/${width}/${height}`;
const avatar = (img: number) => `https://i.pravatar.cc/150?img=${img}`;

const generateRef = (prefix: string, num: number) =>
  `${prefix}-2026-${String(num).padStart(4, '0')}`;

// =============================================================================
// MAIN SEED FUNCTION
// =============================================================================

async function main() {
  console.log('');
  console.log('═══════════════════════════════════════════════════════════════');
  console.log('🌱 SOCIOPULSE V2 - ADVANCED SCENARIO SEEDING');
  console.log('═══════════════════════════════════════════════════════════════');
  console.log('');

  // =========================================================================
  // CLEANUP DATABASE
  // =========================================================================
  console.log('🧹 Cleaning database...');
  await prisma.missionTimelineEvent.deleteMany();
  await prisma.missionReport.deleteMany();
  await prisma.missionInstruction.deleteMany();
  await prisma.missionMessage.deleteMany();
  await prisma.externalNews.deleteMany();
  await prisma.transaction.deleteMany();
  await prisma.message.deleteMany();
  await prisma.review.deleteMany();
  await prisma.booking.deleteMany();
  await prisma.missionApplication.deleteMany();
  await prisma.contract.deleteMany();
  await prisma.quote.deleteMany();
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
  await prisma.user.deleteMany();

  const passwordHash = await bcrypt.hash('password123', 10);

  // =========================================================================
  // SETUP: TAGS
  // =========================================================================
  console.log('🏷️  Creating tags (Growth Engine)...');
  await prisma.tag.createMany({
    data: [
      // JOB Tags
      { name: 'Éducateur Spé', category: TagCategory.JOB },
      { name: 'Moniteur-Éducateur', category: TagCategory.JOB },
      { name: 'AES', category: TagCategory.JOB },
      { name: 'Aide-Soignant', category: TagCategory.JOB },
      { name: 'Infirmier', category: TagCategory.JOB },
      { name: 'Psychologue', category: TagCategory.JOB },
      { name: 'Ergothérapeute', category: TagCategory.JOB },
      { name: 'Psychomotricien', category: TagCategory.JOB },
      { name: 'Orthophoniste', category: TagCategory.JOB },
      { name: 'Animateur', category: TagCategory.JOB },
      { name: 'EJE', category: TagCategory.JOB },

      // STRUCTURE Tags
      { name: 'EHPAD', category: TagCategory.STRUCTURE },
      { name: 'MECS', category: TagCategory.STRUCTURE },
      { name: 'IME', category: TagCategory.STRUCTURE },
      { name: 'ITEP', category: TagCategory.STRUCTURE },
      { name: 'FAM', category: TagCategory.STRUCTURE },
      { name: 'MAS', category: TagCategory.STRUCTURE },
      { name: 'Crèche', category: TagCategory.STRUCTURE },
      { name: 'Hôpital', category: TagCategory.STRUCTURE },
      { name: 'Centre d\'hébergement', category: TagCategory.STRUCTURE },

      // SKILL Tags
      { name: 'TSA', category: TagCategory.SKILL },
      { name: 'Autisme', category: TagCategory.SKILL },
      { name: 'Gériatrie', category: TagCategory.SKILL },
      { name: 'Petite enfance', category: TagCategory.SKILL },
      { name: 'Gestion de crise', category: TagCategory.SKILL },
      { name: 'Troubles du comportement', category: TagCategory.SKILL },
      { name: 'Soins infirmiers', category: TagCategory.SKILL },
      { name: 'Animation atelier', category: TagCategory.SKILL },
      { name: 'Nuit', category: TagCategory.SKILL },
      { name: 'Permis B', category: TagCategory.SKILL },
      { name: 'SocioLive', category: TagCategory.SKILL },
    ],
    skipDuplicates: true,
  });

  // =========================================================================
  // SETUP: ADMIN USER
  // =========================================================================
  console.log('👤 Creating admin...');
  const admin = await prisma.user.create({
    data: {
      email: 'admin@sociopulse.fr',
      passwordHash,
      role: 'ADMIN',
      status: UserStatus.VERIFIED,
      walletBalance: 1000000,
      referralCode: 'ADMIN001',
      profile: {
        create: {
          firstName: 'Admin',
          lastName: 'System',
          bio: 'Super Admin SocioPulse',
          specialties: [],
          diplomas: [],
          complianceStatus: ComplianceStatus.VALIDATED,
        },
      },
    },
  });

  // =========================================================================
  // SETUP: ESTABLISHMENT CLIENTS
  // =========================================================================
  console.log('🏢 Creating establishments (clients)...');

  const establishmentsData = [
    {
      email: 'ehpad.jardins@exemple.fr',
      name: 'EHPAD Les Jardins',
      type: 'EHPAD',
      city: 'Paris',
      postalCode: '75004',
      address: '12 Rue de Rivoli',
      latitude: 48.8566,
      longitude: 2.3522,
      description: 'EHPAD familial, besoins réguliers en renforts IDE et AS.',
    },
    {
      email: 'ime.espoir@exemple.fr',
      name: 'IME L\'Espoir',
      type: 'IME',
      city: 'Paris',
      postalCode: '75001',
      address: '150 Rue Saint-Honoré',
      latitude: 48.8606,
      longitude: 2.3376,
      description: 'IME spécialisé TSA, accompagnements éducatifs et ateliers.',
    },
    {
      email: 'creche.petitspas@exemple.fr',
      name: 'Crèche Les Petits Pas',
      type: 'Crèche',
      city: 'Lyon',
      postalCode: '69002',
      address: '5 Place Bellecour',
      latitude: 45.764,
      longitude: 4.8357,
      description: 'Crèche associative, renforts réguliers sur les pics d\'activité.',
    },
    {
      email: 'mecs.horizon@exemple.fr',
      name: 'MECS Horizon',
      type: 'MECS',
      city: 'Lille',
      postalCode: '59000',
      address: '8 Rue Nationale',
      latitude: 50.62925,
      longitude: 3.057256,
      description: 'Maison d\'enfants, besoins en éducateurs et veilles de nuit.',
    },
    {
      email: 'foyer.amandiers@exemple.fr',
      name: 'Foyer Les Amandiers',
      type: 'Foyer de vie',
      city: 'Bordeaux',
      postalCode: '33000',
      address: '20 Cours de l\'Intendance',
      latitude: 44.841225,
      longitude: -0.574,
      description: 'Foyer de vie pour adultes, missions de jour et week-end.',
    },
  ];

  const establishments: Record<string, any> = {};

  for (let i = 0; i < establishmentsData.length; i++) {
    const data = establishmentsData[i];
    const client = await prisma.user.create({
      data: {
        email: data.email,
        passwordHash,
        role: 'CLIENT',
        clientType: 'ESTABLISHMENT',
        status: UserStatus.VERIFIED,
        walletBalance: 500000,
        isSeed: true, // 🎭 Scarcity Feed: Mark as seed for FOMO interception
        establishment: {
          create: {
            name: data.name,
            type: data.type,
            city: data.city,
            address: data.address,
            postalCode: data.postalCode,
            latitude: data.latitude,
            longitude: data.longitude,
            description: data.description,
            contactName: 'Direction',
            contactRole: 'Directeur(trice)',
            siret: `SEED${String(i + 1).padStart(12, '0')}`,
            logoUrl: pic(`est-${slugify(data.name)}`, 128, 128),
          },
        },
      },
      include: { establishment: true },
    });
    establishments[slugify(data.name)] = client;
  }

  // =========================================================================
  // SETUP: TALENTS WITH SPECIFIC JOB TYPES & TAGS
  // =========================================================================
  console.log('🧑‍⚕️ Creating talents with job assignments...');

  const talentsData = [
    // CRITICAL: Lucas Moreau - EDUCATEUR with MECS, NUIT, PERMIS_B
    {
      email: 'lucas.moreau@exemple.fr',
      firstName: 'Lucas',
      lastName: 'Moreau',
      headline: 'Éducateur spécialisé - MECS & veilles',
      city: 'Lille',
      postalCode: '59800',
      latitude: 50.636,
      longitude: 3.063,
      hourlyRate: 34,
      isVideoEnabled: false,
      avatarImg: 15,
      // MATCHING FIELDS
      jobId: 'ES', // Éducateur Spécialisé
      specialties: ['MECS', 'NUIT', 'PERMIS_B', 'veilles', 'groupe'],
      complianceStatus: ComplianceStatus.VALIDATED,
      hasDriverLicense: true,
      canDoNightShift: true,
    },
    // CRITICAL: Jean Dupont - INFIRMIER with EHPAD, GERIATRIE
    {
      email: 'jean.dupont@exemple.fr',
      firstName: 'Jean',
      lastName: 'Dupont',
      headline: 'Infirmier DE - Renfort de nuit',
      city: 'Paris',
      postalCode: '75011',
      latitude: 48.857,
      longitude: 2.38,
      hourlyRate: 38,
      isVideoEnabled: false,
      avatarImg: 12,
      // MATCHING FIELDS
      jobId: 'IDE', // Infirmier
      specialties: ['EHPAD', 'GERIATRIE', 'soins', 'nuit'],
      complianceStatus: ComplianceStatus.VALIDATED,
      adeliNumber: 'ADELI-75-123456',
      hasDriverLicense: false,
      canDoNightShift: true,
    },
    // CRITICAL: Sarah Lopez - EJE with CRECHE, SOCIOLIVE
    {
      email: 'sarah.lopez@exemple.fr',
      firstName: 'Sarah',
      lastName: 'Lopez',
      headline: 'Éducatrice jeunes enfants - Crèche',
      city: 'Lyon',
      postalCode: '69007',
      latitude: 45.7485,
      longitude: 4.8467,
      hourlyRate: 30,
      isVideoEnabled: true,
      avatarImg: 41,
      // MATCHING FIELDS
      jobId: 'EJE', // Éducateur Jeunes Enfants
      specialties: ['CRECHE', 'SOCIOLIVE', 'petite_enfance', 'animation'],
      complianceStatus: ComplianceStatus.VALIDATED,
      hasDriverLicense: false,
      canDoNightShift: false,
    },
    // CRITICAL: Paul Verlaine - EDUCATEUR but PENDING compliance (to test blocking)
    {
      email: 'paul.verlaine@exemple.fr',
      firstName: 'Paul',
      lastName: 'Verlaine',
      headline: 'Éducateur spécialisé - TSA',
      city: 'Lyon',
      postalCode: '69002',
      latitude: 45.764,
      longitude: 4.8357,
      hourlyRate: 32,
      isVideoEnabled: true,
      avatarImg: 5,
      // MATCHING FIELDS - PENDING COMPLIANCE
      jobId: 'ES',
      specialties: ['autisme', 'adolescents', 'TSA'],
      complianceStatus: ComplianceStatus.PENDING, // ⚠️ NOT VALIDATED
      hasDriverLicense: true,
      canDoNightShift: true,
    },
    // Emma Roux - Art-thérapeute (for Wall posts)
    {
      email: 'emma.roux@exemple.fr',
      firstName: 'Emma',
      lastName: 'Roux',
      headline: 'Art-thérapeute - Ateliers créatifs',
      city: 'Paris',
      postalCode: '75020',
      latitude: 48.863,
      longitude: 2.401,
      hourlyRate: 48,
      isVideoEnabled: true,
      avatarImg: 27,
      jobId: 'ME', // Moniteur-Éducateur (close enough)
      specialties: ['art_therapie', 'émotions', 'visio', 'créatif'],
      complianceStatus: ComplianceStatus.VALIDATED,
      hasDriverLicense: false,
      canDoNightShift: false,
    },
    // Adam Cherif - Médiateur (for Wall posts)
    {
      email: 'adam.cherif@exemple.fr',
      firstName: 'Adam',
      lastName: 'Chérif',
      headline: 'Médiateur - Gestion de conflits',
      city: 'Marseille',
      postalCode: '13008',
      latitude: 43.2677,
      longitude: 5.382,
      hourlyRate: 42,
      isVideoEnabled: true,
      avatarImg: 8,
      jobId: 'ES',
      specialties: ['médiation', 'conflits', 'visio', 'cadre'],
      complianceStatus: ComplianceStatus.VALIDATED,
      hasDriverLicense: true,
      canDoNightShift: false,
    },
    // Marie Curie - Aide-soignante
    {
      email: 'marie.curie@exemple.fr',
      firstName: 'Marie',
      lastName: 'Curie',
      headline: 'Aide-soignante - EHPAD & domicile',
      city: 'Paris',
      postalCode: '75004',
      latitude: 48.8566,
      longitude: 2.3522,
      hourlyRate: 28,
      isVideoEnabled: false,
      avatarImg: 32,
      jobId: 'AS',
      specialties: ['toilette', 'repas', 'EHPAD', 'domicile'],
      complianceStatus: ComplianceStatus.VALIDATED,
      hasDriverLicense: false,
      canDoNightShift: true,
    },
    // Clara Durand - Orthophoniste
    {
      email: 'clara.durand@exemple.fr',
      firstName: 'Clara',
      lastName: 'Durand',
      headline: 'Orthophoniste - Troubles DYS',
      city: 'Lille',
      postalCode: '59000',
      latitude: 50.62925,
      longitude: 3.057256,
      hourlyRate: 60,
      isVideoEnabled: true,
      avatarImg: 23,
      jobId: 'ORTHOPHONISTE',
      specialties: ['dyslexie', 'langage', 'visio', 'bilan'],
      complianceStatus: ComplianceStatus.VALIDATED,
      adeliNumber: 'ADELI-59-789012',
      hasDriverLicense: true,
      canDoNightShift: false,
    },
  ];

  const talents: Record<string, any> = {};

  for (let i = 0; i < talentsData.length; i++) {
    const data = talentsData[i];
    const talent = await prisma.user.create({
      data: {
        email: data.email,
        passwordHash,
        role: 'TALENT',
        status: UserStatus.VERIFIED,
        stripeAccountId: `acct_seed_${i + 1}`,
        stripeOnboarded: true,
        referralCode: `TALENT${String(i + 1).padStart(4, '0')}`,
        isSeed: true, // 🎭 Scarcity Feed: Mark as seed for FOMO interception
        profile: {
          create: {
            firstName: data.firstName,
            lastName: data.lastName,
            avatarUrl: avatar(data.avatarImg),
            headline: data.headline,
            bio: `Disponible pour des missions de renfort. ${data.headline}.`,
            city: data.city,
            postalCode: data.postalCode,
            latitude: data.latitude,
            longitude: data.longitude,
            // CRITICAL: Job & Matching fields
            jobId: data.jobId,
            specialties: data.specialties,
            complianceStatus: data.complianceStatus,
            adeliNumber: data.adeliNumber || null,
            hasDriverLicense: data.hasDriverLicense,
            canDoNightShift: data.canDoNightShift,
            // Other fields
            diplomas: [{ name: 'Diplôme d\'État', year: 2018 }],
            hourlyRate: data.hourlyRate,
            isVideoEnabled: data.isVideoEnabled,
            averageRating: 4.5 + Math.random() * 0.5,
            totalReviews: Math.floor(10 + Math.random() * 30),
            totalMissions: Math.floor(5 + Math.random() * 20),
          },
        },
      },
      include: { profile: true },
    });
    talents[slugify(`${data.firstName}-${data.lastName}`)] = talent;
  }

  console.log('');
  console.log('═══════════════════════════════════════════════════════════════');
  console.log('📊 SCENARIO SEEDING');
  console.log('═══════════════════════════════════════════════════════════════');

  // =========================================================================
  // SCENARIO 1: THE PERFECT MATCH (SOS BROADCAST)
  // Mission from MECS Horizon for EDUCATEUR with NUIT context
  // Should appear in Lucas Moreau's feed
  // =========================================================================
  console.log('');
  console.log('📌 SCENARIO 1: THE PERFECT MATCH (SOS BROADCAST)');

  const mecsHorizon = establishments['mecs-horizon'];
  const lucasMoreau = talents['lucas-moreau'];

  const perfectMatchMission = await prisma.reliefMission.create({
    data: {
      clientId: mecsHorizon.id,
      title: '🆘 Veilleur de nuit URGENT - MECS',
      description: `Besoin urgent d'un éducateur pour une veille de nuit ce week-end.
      
Contexte : Effectif réduit suite à un arrêt maladie.
Public : Adolescents 12-18 ans
Expérience MECS requise.

Permis B apprécié pour interventions extérieures possibles.`,
      jobTitle: 'Éducateur Spécialisé',
      // SOS RENFORT FIELDS
      jobId: 'ES',
      specialtiesTags: ['MECS', 'NUIT', 'veilles', 'adolescents'],
      requiresCar: false, // Apprécié mais pas obligatoire
      requiresNight: true,
      requiresDiploma: true,
      targetPublic: 'Adolescents 12-18 ans',
      // Timing
      urgencyLevel: MissionUrgency.CRITICAL,
      startDate: hoursFromNow(8),
      endDate: hoursFromNow(18),
      isNightShift: true,
      // Location
      address: mecsHorizon.establishment.address,
      city: mecsHorizon.establishment.city,
      postalCode: mecsHorizon.establishment.postalCode,
      latitude: mecsHorizon.establishment.latitude,
      longitude: mecsHorizon.establishment.longitude,
      radiusKm: 30,
      // Pricing
      hourlyRate: 35,
      estimatedHours: 10,
      // Status: Broadcasting
      status: MissionStatus.OPEN,
      requiredSkills: ['veilles', 'MECS', 'gestion_crise'],
      // 🎭 Scarcity Feed: Mark as seed for FOMO interception
      isSeed: true,
    },
  });

  // Create a POST of type NEED to inject into the Feed
  await prisma.post.create({
    data: {
      authorId: mecsHorizon.id,
      type: PostType.NEED,
      title: '🆘 Veilleur de nuit URGENT - Ce week-end',
      content: `MECS Horizon recherche en urgence un éducateur pour veille de nuit ce week-end.

✅ Profil recherché : Éducateur spécialisé avec expérience MECS
🌙 Horaires : Nuit (22h-8h)
📍 Lille
💰 35€/h

Contact via la plateforme.`,
      city: 'Lille',
      postalCode: '59000',
      latitude: 50.62925,
      longitude: 3.057256,
      tags: ['SOS', 'MECS', 'NUIT', 'veille', 'éducateur'],
      validUntil: hoursFromNow(48),
      isActive: true,
    },
  });

  console.log('   ✅ Created OPEN mission from MECS Horizon (jobId=ES, requiresNight=true)');
  console.log('   ✅ Created NEED post for Feed injection');
  console.log(`   📧 Test: Login as lucas.moreau@exemple.fr to see matching mission`);

  // =========================================================================
  // SCENARIO 2: THE ADMIN BLOCK (CONTRACTS)
  // Mission ASSIGNED but contract NOT signed (Paul Verlaine has PENDING compliance)
  // =========================================================================
  console.log('');
  console.log('📌 SCENARIO 2: THE ADMIN BLOCK (CONTRACTS)');

  const imeEspoir = establishments['ime-lespoir'];
  const paulVerlaine = talents['paul-verlaine'];

  const adminBlockMission = await prisma.reliefMission.create({
    data: {
      clientId: imeEspoir.id,
      assignedTalentId: paulVerlaine.id,
      title: 'Accompagnement éducatif TSA',
      description: `Mission d'accompagnement pour un jeune autiste.
      
Contexte : Atelier individuel + temps collectif
Profil TSA expérimenté requis.`,
      jobTitle: 'Éducateur spécialisé',
      jobId: 'ES',
      specialtiesTags: ['TSA', 'autisme', 'IME'],
      requiresCar: false,
      requiresNight: false,
      requiresDiploma: true,
      targetPublic: 'Jeune adulte TSA',
      urgencyLevel: MissionUrgency.HIGH,
      startDate: daysFromNow(3),
      endDate: daysFromNow(3),
      isNightShift: false,
      address: imeEspoir.establishment.address,
      city: imeEspoir.establishment.city,
      postalCode: imeEspoir.establishment.postalCode,
      latitude: imeEspoir.establishment.latitude,
      longitude: imeEspoir.establishment.longitude,
      radiusKm: 20,
      hourlyRate: 32,
      estimatedHours: 7,
      status: MissionStatus.ASSIGNED,
      assignedAt: new Date(),
      // 🎭 Scarcity Feed: Mark as seed for FOMO interception
      isSeed: true,
    },
  });

  // Create contract with signedAt = NULL (blocking action required)
  const adminBlockContract = await prisma.contract.create({
    data: {
      reference: generateRef('CTR', 1),
      type: 'MISSION_SOS',
      talentId: paulVerlaine.id,
      clientId: imeEspoir.id,
      missionId: adminBlockMission.id,
      title: `Contrat - ${adminBlockMission.title}`,
      content: `Contrat de mission SOS Renfort.

Mission : ${adminBlockMission.title}
Établissement : ${imeEspoir.establishment.name}
Date : ${adminBlockMission.startDate.toLocaleDateString('fr-FR')}

Conditions générales...`,
      totalAmount: adminBlockMission.hourlyRate * 7 * 100,
      platformFee: Math.round(adminBlockMission.hourlyRate * 7 * 100 * 0.15),
      startDate: adminBlockMission.startDate,
      endDate: adminBlockMission.endDate,
      status: ContractStatus.PENDING,
      signedAt: null, // ⚠️ NOT SIGNED
    },
  });

  console.log('   ✅ Created ASSIGNED mission between IME L\'Espoir and Paul Verlaine');
  console.log('   ✅ Created CONTRACT with signedAt=NULL (action required)');
  console.log('   ⚠️  Paul Verlaine has complianceStatus=PENDING (blocking)');
  console.log(`   📧 Test: Login as paul.verlaine@exemple.fr to see "Action Required"`);

  // =========================================================================
  // SCENARIO 3: THE LIVE OPS (TRACKING)
  // Mission IN_PROGRESS with chat messages
  // =========================================================================
  console.log('');
  console.log('📌 SCENARIO 3: THE LIVE OPS (TRACKING)');

  const ehpadJardins = establishments['ehpad-les-jardins'];
  const jeanDupont = talents['jean-dupont'];

  const liveOpsMission = await prisma.reliefMission.create({
    data: {
      clientId: ehpadJardins.id,
      assignedTalentId: jeanDupont.id,
      title: 'Renfort IDE Nuit - Gériatrie',
      description: `Mission de nuit en cours au service gériatrie.
      
Effectif : 45 résidents
Équipe : 1 IDE + 2 AS`,
      jobTitle: 'Infirmier',
      jobId: 'IDE',
      specialtiesTags: ['EHPAD', 'GERIATRIE', 'nuit', 'soins'],
      requiresCar: false,
      requiresNight: true,
      requiresDiploma: true,
      serviceName: 'Service Gériatrie - Étage 2',
      urgencyLevel: MissionUrgency.HIGH,
      startDate: hoursAgo(2), // Started 2 hours ago
      endDate: hoursFromNow(6),
      isNightShift: true,
      address: ehpadJardins.establishment.address,
      city: ehpadJardins.establishment.city,
      postalCode: ehpadJardins.establishment.postalCode,
      latitude: ehpadJardins.establishment.latitude,
      longitude: ehpadJardins.establishment.longitude,
      radiusKm: 20,
      hourlyRate: 38,
      estimatedHours: 8,
      status: MissionStatus.IN_PROGRESS, // ⚡ LIVE
      assignedAt: hoursAgo(4),
      // 🎭 Scarcity Feed: Mark as seed for FOMO interception
      isSeed: true,
    },
  });

  // Create mission instructions
  await prisma.missionInstruction.create({
    data: {
      missionId: liveOpsMission.id,
      content: `Bienvenue à l'EHPAD Les Jardins !

📋 CONSIGNES IMPORTANTES :
- Badge d'accès : Retirer à l'accueil
- Vestiaire : Salle 103, code 4521
- Tour de garde : 22h00, 02h00, 06h00
- Téléphone de garde : 06 12 34 56 78

⚠️ Résidents prioritaires :
- Mme Martin (ch. 12) - Surveillance tension
- M. Bernard (ch. 18) - Risque de chute`,
      checklist: [
        { id: '1', text: 'Récupérer le badge d\'accès', completed: true },
        { id: '2', text: 'Lecture du dossier de transmissions', completed: true },
        { id: '3', text: 'Premier tour de garde effectué', completed: false },
      ],
      isAcknowledged: true,
      acknowledgedAt: hoursAgo(2),
    },
  });

  // Create chat messages
  const chatMessages = [
    {
      senderId: ehpadJardins.id,
      content: 'Bienvenue Jean ! Badge récupéré à l\'accueil ?',
      createdAt: hoursAgo(2),
    },
    {
      senderId: jeanDupont.id,
      content: 'Oui c\'est bon, je suis en place. Transmissions lues.',
      createdAt: hoursAgo(1.9),
    },
    {
      senderId: jeanDupont.id,
      content: 'RAS pour le moment, premier tour effectué.',
      createdAt: hoursAgo(0.5),
    },
  ];

  for (const msg of chatMessages) {
    await prisma.missionMessage.create({
      data: {
        missionId: liveOpsMission.id,
        senderId: msg.senderId,
        content: msg.content,
        type: MissionMessageType.TEXT,
        createdAt: msg.createdAt,
      },
    });
  }

  // Create timeline events
  await prisma.missionTimelineEvent.create({
    data: {
      missionId: liveOpsMission.id,
      type: 'BRIEFING_READ',
      userId: jeanDupont.id,
      createdAt: hoursAgo(2),
    },
  });

  await prisma.missionTimelineEvent.create({
    data: {
      missionId: liveOpsMission.id,
      type: 'MISSION_STARTED',
      userId: jeanDupont.id,
      createdAt: hoursAgo(2),
    },
  });

  console.log('   ✅ Created IN_PROGRESS mission (started 2h ago)');
  console.log('   ✅ Created mission instructions (acknowledged)');
  console.log('   ✅ Created 3 chat messages');
  console.log('   ✅ Created timeline events');
  console.log(`   📧 Test: Login as jean.dupont@exemple.fr to see Live Tracking`);

  // =========================================================================
  // SCENARIO 4: THE COMPLETED BILLING (SOCIOLIVE)
  // Completed booking with paid invoice/transaction
  // =========================================================================
  console.log('');
  console.log('📌 SCENARIO 4: THE COMPLETED BILLING (SOCIOLIVE)');

  const crechePetitsPas = establishments['creche-les-petits-pas'];
  const sarahLopez = talents['sarah-lopez'];

  // Create a service for Sarah
  const sarahService = await prisma.service.create({
    data: {
      profileId: sarahLopez.profile.id,
      name: 'Atelier Éveil Musical - Crèche',
      slug: `atelier-eveil-musical-sarah-lopez`,
      description: `Un atelier d'éveil musical adapté aux tout-petits.
      
Objectifs :
- Découverte des sons et rythmes
- Motricité fine
- Socialisation

Matériel fourni.`,
      shortDescription: 'Éveil musical pour les 0-3 ans',
      type: ServiceType.WORKSHOP,
      category: 'Petite enfance',
      basePrice: 450,
      duration: 120,
      minParticipants: 6,
      maxParticipants: 15,
      ageGroups: ['0-3 ans'],
      tags: ['éveil', 'musique', 'crèche', 'petite_enfance'],
      imageUrl: pic('workshop-music', 800, 600),
      isActive: true,
    },
  });

  // Create completed booking
  const completedBooking = await prisma.booking.create({
    data: {
      clientId: crechePetitsPas.id,
      providerId: sarahLopez.id,
      serviceId: sarahService.id,
      sessionDate: daysAgo(5),
      sessionTime: '14:00',
      totalPrice: 450, // 450€
      platformFee: 67.5, // 15%
      providerPayout: 382.5,
      status: BookingStatus.COMPLETED,
      clientNotes: 'Atelier très apprécié par les enfants et l\'équipe !',
      confirmedAt: daysAgo(10),
      completedAt: daysAgo(5),
      paidAt: daysAgo(5),
    },
  });

  // Create transaction (payment)
  await prisma.transaction.create({
    data: {
      userId: sarahLopez.id,
      type: TransactionType.BOOKING_PAYMENT,
      amount: 45000, // centimes
      status: TransactionStatus.COMPLETED,
      description: `Paiement atelier - ${sarahService.name}`,
      bookingId: completedBooking.id,
      stripePaymentId: `pi_seed_${Date.now()}`,
      completedAt: daysAgo(5),
    },
  });

  // Create review
  await prisma.review.create({
    data: {
      bookingId: completedBooking.id,
      profileId: sarahLopez.profile.id,
      serviceId: sarahService.id,
      rating: 5,
      title: 'Excellent atelier !',
      comment: 'Sarah a su captiver les enfants avec beaucoup de douceur. Les parents ont eu des retours très positifs. Nous referons appel à elle !',
    },
  });

  console.log('   ✅ Created COMPLETED booking (Atelier 450€)');
  console.log('   ✅ Created PAID transaction');
  console.log('   ✅ Created 5-star review');
  console.log(`   📧 Test: Login as sarah.lopez@exemple.fr to see billing history`);

  // =========================================================================
  // SCENARIO 5: SOCIAL ACTIVITY (WALL)
  // Multiple posts from talents with engagement
  // =========================================================================
  console.log('');
  console.log('📌 SCENARIO 5: SOCIAL ACTIVITY (WALL)');

  const emmaRoux = talents['emma-roux'];
  const adamCherif = talents['adam-cherif'];

  const wallPosts = [
    {
      authorId: emmaRoux.id,
      type: PostType.SOCIAL,
      title: 'Super atelier aujourd\'hui !',
      content: `🎨 Journée magique à l'IME !

Les participants ont créé des œuvres incroyables autour du thème "Mes émotions en couleurs".

Un moment de partage intense, des sourires, des découvertes... C'est ça la beauté de l'art-thérapie. 💜

#ArtTherapie #IME #Émotions #Atelier`,
      city: 'Paris',
      tags: ['art-thérapie', 'IME', 'atelier', 'émotions'],
      category: PostCategory.EXPERIENCE,
      mediaUrls: [pic('atelier-art-1'), pic('atelier-art-2')],
    },
    {
      authorId: adamCherif.id,
      type: PostType.SOCIAL,
      title: 'Dispo sur Marseille semaine prochaine',
      content: `📍 Je serai disponible sur Marseille du 27 au 31 janvier.

Si vous avez besoin d'un médiateur pour :
- Gestion de conflits d'équipe
- Ateliers communication non-violente
- Accompagnement de situations tendues

N'hésitez pas à me contacter ! 🙌

#Médiation #Marseille #Disponible`,
      city: 'Marseille',
      tags: ['médiation', 'Marseille', 'disponibilité', 'CNV'],
      category: PostCategory.NEWS,
      mediaUrls: [],
    },
    {
      authorId: lucasMoreau.id,
      type: PostType.SOCIAL,
      title: 'Formation gestion de crise terminée ✅',
      content: `Très content d'avoir validé ma formation "Gestion de crise en MECS" !

3 jours intenses mais riches en apprentissages :
- Techniques de désescalade
- Posture contenante
- Analyse post-incident

Merci à toute l'équipe de formateurs. 💪

#Formation #MECS #GestionDeCrise`,
      city: 'Lille',
      tags: ['formation', 'MECS', 'gestion-crise', 'éducateur'],
      category: PostCategory.EXPERIENCE,
      mediaUrls: [pic('formation-crise')],
    },
    {
      authorId: emmaRoux.id,
      type: PostType.OFFER,
      title: 'Nouvel atelier : Art & Émotions seniors',
      content: `🆕 Je lance un nouvel atelier spécial EHPAD !

"Art & Émotions" - Un voyage créatif adapté aux seniors.

✨ Objectifs :
- Stimulation cognitive douce
- Expression des émotions
- Moments de partage

📅 Disponible pour interventions régulières ou ponctuelles.
📍 Île-de-France

Contactez-moi pour plus d'infos !`,
      city: 'Paris',
      tags: ['art-thérapie', 'seniors', 'EHPAD', 'atelier'],
      category: null,
      mediaUrls: [pic('atelier-seniors')],
    },
    {
      authorId: adamCherif.id,
      type: PostType.SOCIAL,
      title: 'Retour sur une belle intervention',
      content: `🙏 Merci à l'équipe du CMS Prado pour leur accueil !

Une situation complexe qui nécessitait de la patience et de l'écoute. 3 séances de médiation plus tard, l'équipe a retrouvé une dynamique positive.

C'est gratifiant de voir les relations se reconstruire. 🤝

#Médiation #CMS #Équipe #Conflits`,
      city: 'Marseille',
      tags: ['médiation', 'équipe', 'CMS', 'accompagnement'],
      category: PostCategory.EXPERIENCE,
      mediaUrls: [],
    },
  ];

  for (const postData of wallPosts) {
    await prisma.post.create({
      data: {
        authorId: postData.authorId,
        type: postData.type,
        title: postData.title,
        content: postData.content,
        city: postData.city,
        tags: postData.tags,
        category: postData.category,
        mediaUrls: postData.mediaUrls,
        isActive: true,
        viewCount: Math.floor(50 + Math.random() * 200),
        createdAt: daysAgo(Math.floor(Math.random() * 7)),
      },
    });
  }

  console.log('   ✅ Created 5 Wall posts (SOCIAL, OFFER types)');
  console.log('   ✅ Posts from Emma Roux and Adam Chérif');
  console.log('   📧 Test: Visit /wall to see social feed');

  // =========================================================================
  // BONUS: CREATE ADDITIONAL OPEN MISSIONS FOR FEED
  // =========================================================================
  console.log('');
  console.log('📌 BONUS: Additional open missions for feed...');

  const additionalMissions = [
    {
      client: ehpadJardins,
      title: 'Renfort AS Week-end',
      jobId: 'AS',
      jobTitle: 'Aide-Soignant',
      tags: ['EHPAD', 'week-end', 'soins'],
      urgency: MissionUrgency.MEDIUM,
      hourlyRate: 28,
      requiresNight: false,
    },
    {
      client: imeEspoir,
      title: 'Animateur Atelier TSA',
      jobId: 'ME',
      jobTitle: 'Moniteur-Éducateur',
      tags: ['IME', 'TSA', 'animation'],
      urgency: MissionUrgency.LOW,
      hourlyRate: 30,
      requiresNight: false,
    },
    {
      client: crechePetitsPas,
      title: 'EJE Renfort Matin',
      jobId: 'EJE',
      jobTitle: 'Éducateur Jeunes Enfants',
      tags: ['CRECHE', 'matin', 'accueil'],
      urgency: MissionUrgency.HIGH,
      hourlyRate: 32,
      requiresNight: false,
    },
  ];

  for (const m of additionalMissions) {
    await prisma.reliefMission.create({
      data: {
        clientId: m.client.id,
        title: m.title,
        description: `Mission de renfort - ${m.title}`,
        jobTitle: m.jobTitle,
        jobId: m.jobId,
        specialtiesTags: m.tags,
        requiresCar: false,
        requiresNight: m.requiresNight,
        requiresDiploma: true,
        urgencyLevel: m.urgency,
        startDate: hoursFromNow(24 + Math.random() * 72),
        endDate: hoursFromNow(32 + Math.random() * 72),
        isNightShift: false,
        address: m.client.establishment.address,
        city: m.client.establishment.city,
        postalCode: m.client.establishment.postalCode,
        latitude: m.client.establishment.latitude,
        longitude: m.client.establishment.longitude,
        radiusKm: 25,
        hourlyRate: m.hourlyRate,
        estimatedHours: 7,
        status: MissionStatus.OPEN,
        // 🎭 Scarcity Feed: Mark as seed for FOMO interception
        isSeed: true,
      },
    });
  }

  console.log('   ✅ Created 3 additional OPEN missions');

  // =========================================================================
  // SUMMARY
  // =========================================================================
  console.log('');
  console.log('═══════════════════════════════════════════════════════════════');
  console.log('✅ SEEDING COMPLETE - TEST SCENARIOS READY');
  console.log('═══════════════════════════════════════════════════════════════');
  console.log('');
  console.log('🔐 All accounts use password: password123');
  console.log('');
  console.log('📋 TEST ACCOUNTS:');
  console.log('   ┌──────────────────────────────────────────────────────────┐');
  console.log('   │ ADMIN                                                    │');
  console.log('   │   admin@sociopulse.fr                                    │');
  console.log('   ├──────────────────────────────────────────────────────────┤');
  console.log('   │ ESTABLISHMENTS (Clients)                                 │');
  console.log('   │   ehpad.jardins@exemple.fr     → EHPAD Les Jardins       │');
  console.log('   │   ime.espoir@exemple.fr        → IME L\'Espoir           │');
  console.log('   │   creche.petitspas@exemple.fr  → Crèche Les Petits Pas   │');
  console.log('   │   mecs.horizon@exemple.fr      → MECS Horizon            │');
  console.log('   ├──────────────────────────────────────────────────────────┤');
  console.log('   │ TALENTS                                                  │');
  console.log('   │   lucas.moreau@exemple.fr      → ES, MECS+NUIT ✅        │');
  console.log('   │   jean.dupont@exemple.fr       → IDE, EHPAD+GERIATRIE ✅ │');
  console.log('   │   sarah.lopez@exemple.fr       → EJE, CRECHE ✅          │');
  console.log('   │   paul.verlaine@exemple.fr     → ES, TSA ⚠️ PENDING     │');
  console.log('   │   emma.roux@exemple.fr         → Art-thérapeute ✅       │');
  console.log('   │   adam.cherif@exemple.fr       → Médiateur ✅            │');
  console.log('   └──────────────────────────────────────────────────────────┘');
  console.log('');
  console.log('🧪 SCENARIO TESTS:');
  console.log('');
  console.log('   ▶ SCENARIO 1 - PERFECT MATCH:');
  console.log('     Login as lucas.moreau@exemple.fr');
  console.log('     → Should see MECS Horizon\'s night mission in feed (matching!)');
  console.log('');
  console.log('   ▶ SCENARIO 2 - ADMIN BLOCK:');
  console.log('     Login as paul.verlaine@exemple.fr');
  console.log('     → Has ASSIGNED mission but PENDING compliance');
  console.log('     → Contract signedAt=NULL → "Action Required"');
  console.log('');
  console.log('   ▶ SCENARIO 3 - LIVE OPS:');
  console.log('     Login as jean.dupont@exemple.fr');
  console.log('     → Mission IN_PROGRESS (started 2h ago)');
  console.log('     → Has chat messages and timeline events');
  console.log('     → Go to /dashboard/tracking to see live mission');
  console.log('');
  console.log('   ▶ SCENARIO 4 - COMPLETED BILLING:');
  console.log('     Login as sarah.lopez@exemple.fr');
  console.log('     → Has COMPLETED booking (450€ workshop)');
  console.log('     → Transaction PAID, 5-star review');
  console.log('');
  console.log('   ▶ SCENARIO 5 - SOCIAL WALL:');
  console.log('     Visit /wall');
  console.log('     → 5 posts from Emma Roux, Adam Chérif, Lucas Moreau');
  console.log('');
  console.log('═══════════════════════════════════════════════════════════════');
  console.log('');
}

main()
  .catch((e) => {
    console.error('❌ Seeding failed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
