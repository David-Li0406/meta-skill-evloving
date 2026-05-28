
import {
    PrismaClient,
    UserRole,
    UserStatus,
    MissionStatus,
    MissionUrgency,
    ClientType
} from '@prisma/client';
import * as bcrypt from 'bcrypt';
import * as fs from 'fs';
import * as path from 'path';

import * as os from 'os';

const prisma = new PrismaClient();

// Helper to normalize strings
const slugify = (text: string) => {
    return text
        .toString()
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/\s+/g, '.')
        .replace(/[^\w\.]+/g, '')
        .replace(/\.\./g, '.')
        .replace(/^-+/, '')
        .replace(/-+$/, '');
};

async function main() {
    // Use /tmp for Docker containers (non-writable /app), otherwise use cwd
    const jsonDir = process.env.NODE_ENV === 'production' ? os.tmpdir() : process.cwd();
    const jsonPath = path.join(jsonDir, 'sociopulse_seed_2026.json');

    if (!fs.existsSync(jsonPath)) {
        console.error(`❌ File not found: ${jsonPath}`);
        console.log('Run "npm run db:seed:sociopulse" to generate it.');
        process.exit(1);
    }

    const rawData = fs.readFileSync(jsonPath, 'utf-8');
    const seedData = JSON.parse(rawData);

    console.log(`📦 Loaded ${seedData.length} items from JSON.`);
    console.log('🚀 Starting import...');

    const passwordHash = await bcrypt.hash('password123', 10);

    let profilesCreated = 0;
    let missionsCreated = 0;
    let clientsCreated = 0;

    const clientCache: Record<string, string> = {};

    for (const item of seedData) {
        const createdAt = item.createdAt ? new Date(item.createdAt) : new Date();

        if (item.type === 'PROFILE') {
            const data = item.data;
            const email = `${slugify(data.firstName)}.${slugify(data.lastName)}.${slugify(item.city)}@socio-seed.com`.toLowerCase();

            const existingUser = await prisma.user.findUnique({ where: { email } });
            if (existingUser) continue;

            await prisma.user.create({
                data: {
                    email,
                    passwordHash,
                    role: UserRole.TALENT,
                    status: UserStatus.VERIFIED,
                    isSeed: true, // 🎭 Scarcity Feed: Mark as seed for FOMO interception
                    createdAt, // Apply random timestamp
                    profile: {
                        create: {
                            firstName: data.firstName,
                            lastName: data.lastName,
                            headline: data.title,
                            bio: data.description,
                            city: item.city,
                            specialties: data.tags,
                            hourlyRate: data.hourlyRate,
                            isVideoEnabled: false,
                            averageRating: 4.5,
                            createdAt // Apply random timestamp
                        }
                    }
                }
            });
            profilesCreated++;

        } else if (item.type === 'MISSION') {
            const data = item.data;
            const structureName = data.structureName || `Structure ${item.city}`;

            let clientId = clientCache[structureName];

            if (!clientId) {
                // Find or create Client
                const clientEmail = `contact.${slugify(structureName)}@client-seed.com`.toLowerCase();

                let client = await prisma.user.findUnique({ where: { email: clientEmail } });

                if (!client) {
                    const siret = `SEED${Math.floor(Math.random() * 1000000000).toString().padStart(9, '0')}`;

                    client = await prisma.user.create({
                        data: {
                            email: clientEmail,
                            passwordHash,
                            role: UserRole.CLIENT,
                            status: UserStatus.VERIFIED,
                            clientType: ClientType.ESTABLISHMENT,
                            isSeed: true, // 🎭 Scarcity Feed: Mark as seed for FOMO interception
                            createdAt, // Apply random timestamp
                            establishment: {
                                create: {
                                    name: structureName,
                                    type: 'Etablissement',
                                    city: item.city,
                                    address: `${data.address || 'Adresse inconnue'}, ${item.city}`,
                                    postalCode: '00000',
                                    description: 'Structure générée automatiquement',
                                    logoUrl: data.logoUrl, // Use the generated medical image
                                    siret,
                                    createdAt // Apply random timestamp
                                }
                            }
                        }
                    });
                    clientsCreated++;
                }
                clientId = client.id;
                clientCache[structureName] = clientId;
            }

            // Mission Dates
            const startInHours = Math.floor(Math.random() * 72) + 24;
            const durationHours = 7;
            const startDate = new Date(Date.now() + startInHours * 3600 * 1000);
            const endDate = new Date(startDate.getTime() + durationHours * 3600 * 1000);

            await prisma.reliefMission.create({
                data: {
                    clientId,
                    title: data.title,
                    description: data.description,
                    jobTitle: data.title.split('-')[0].trim(),
                    urgencyLevel: MissionUrgency.HIGH,
                    status: MissionStatus.OPEN,
                    startDate,
                    endDate,
                    hourlyRate: data.hourlyRate,
                    address: `${item.city} Centre`,
                    city: item.city,
                    postalCode: '00000',
                    requiredSkills: data.tags,
                    totalBudget: data.hourlyRate * durationHours,
                    isSeed: true, // 🎭 Scarcity Feed: Mark as seed for FOMO interception
                    createdAt // Apply random timestamp to Mission
                }
            });
            missionsCreated++;
        }
    }

    console.log('✅ Import complete!');
    console.log(`📊 Stats: Profiles=${profilesCreated}, Clients=${clientsCreated}, Missions=${missionsCreated}`);
}

main()
    .catch((e) => {
        console.error(e);
        process.exit(1);
    })
    .finally(async () => {
        await prisma.$disconnect();
    });
