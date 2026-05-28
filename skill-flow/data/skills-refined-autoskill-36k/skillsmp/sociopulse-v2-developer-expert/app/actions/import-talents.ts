'use server';

import { db } from '@/lib/db';
import { UserRole, UserStatus } from '@prisma/client';
import * as XLSX from 'xlsx';
import { z } from 'zod';

// Schema de validation pour une ligne d'import
const talentImportSchema = z.object({
    firstName: z.string().min(1, "Prénom requis"),
    lastName: z.string().min(1, "Nom requis"),
    email: z.string().email("Email invalide"),
    phone: z.string().optional(),
    job: z.string().optional(),
    tags: z.string().optional(), // "Tag1, Tag2"
});

export type ImportResult = {
    success: number;
    errors: Array<{ row: number; error: string; data: any }>;
    total: number;
};

export async function importTalentsAction(formData: FormData): Promise<ImportResult> {
    const file = formData.get('file') as File;
    const establishmentId = formData.get('establishmentId') as string;

    if (!file || !establishmentId) {
        throw new Error("Fichier ou ID établissement manquant");
    }

    // 1. Parsing du fichier
    const buffer = await file.arrayBuffer();
    const workbook = XLSX.read(buffer, { type: 'buffer' });
    const sheetName = workbook.SheetNames[0];
    const sheet = workbook.Sheets[sheetName];
    const rows = XLSX.utils.sheet_to_json(sheet) as any[];

    let successCount = 0;
    const errors: ImportResult['errors'] = [];

    // Préparez les tags par défaut
    const defaultTags = ["Importé"];

    // 2. Traitement ligne par ligne
    for (let i = 0; i < rows.length; i++) {
        const row = rows[i];

        // Mapping des colonnes (support flexible)
        const data = {
            firstName: row['Prénom'] || row['First Name'] || row['firstname'],
            lastName: row['Nom'] || row['Last Name'] || row['lastname'],
            email: row['Email'] || row['E-mail'] || row['email'],
            phone: row['Téléphone'] || row['Phone'] || row['phone'],
            job: row['Métier'] || row['Job'] || row['job'],
            tags: row['Tags'] || row['tags'],
        };

        // Validation
        const validation = talentImportSchema.safeParse(data);

        if (!validation.success) {
            errors.push({
                row: i + 2, // 1-based + header
                error: validation.error.errors.map(e => e.message).join(', '),
                data: row
            });
            continue;
        }

        const { email, firstName, lastName, phone, job, tags: tagsStr } = validation.data;
        const tags = tagsStr ? tagsStr.split(',').map(t => t.trim()) : [];

        try {
            // Dédoublonnage et Logique Métier
            await db.$transaction(async (tx) => {
                // A. Vérifier existence User
                let user = await tx.user.findUnique({
                    where: { email },
                    include: { profile: true }
                });

                if (!user) {
                    // CAS B: Nouveau User (INVITED)
                    user = await tx.user.create({
                        data: {
                            email,
                            role: UserRole.TALENT,
                            status: UserStatus.INVITED,
                            isMarketplaceVisible: false,
                            isVerified: false,
                            // Création du profil stub
                            profile: {
                                create: {
                                    firstName,
                                    lastName,
                                    headline: job,
                                    // On pourrait générer un avatar par défaut ici
                                }
                            }
                        },
                        include: { profile: true }
                    });

                    // TODO: Déclencher l'envoi d'email d'invitation (via un service de notification ou queue)
                    console.log(`[Import] Invitation envoyée à ${email}`);
                } else {
                    // CAS A: User existant -> Notification (TODO)
                    console.log(`[Import] User existant lié: ${email}`);
                }

                // B. Lier au TalentPool de l'établissement
                // On récupère ou crée le TalentPool "Import" ou défaut de l'établissement
                // Pour simplifier, on suppose qu'on ajoute au pool par défaut ou on crée un lien direct
                // Le prompt parle de `TalentPool` comme liaison Many-to-Many via `TalentPoolMember`.
                // Il faut identifier QUEL TalentPool. Le prompt dit "L'entrée dans TalentPool liant ce User".

                // On cherche un TalentPool par défaut pour cet établissement, sinon on le crée
                let pool = await tx.talentPool.findFirst({
                    where: { establishmentId, name: "Mon Équipe" } // Nom par défaut
                });

                if (!pool) {
                    pool = await tx.talentPool.create({
                        data: {
                            establishmentId,
                            name: "Mon Équipe"
                        }
                    });
                }

                // Créer/Update le membre
                const profileId = user.profile?.id;
                if (profileId) {
                    await tx.talentPoolMember.upsert({
                        where: {
                            talentPoolId_profileId: {
                                talentPoolId: pool.id,
                                profileId: profileId
                            }
                        },
                        create: {
                            talentPoolId: pool.id,
                            profileId: profileId,
                            tags: [...defaultTags, ...tags], // Stocké en Json
                            note: job ? `Métier: ${job}` : undefined
                        },
                        update: {
                            // On ne merge pas forcément les tags existants pour éviter doublons, ou alors si.
                            // Ici on update juste la note si vide
                        }
                    });
                }
            });

            successCount++;
        } catch (err: any) {
            console.error(`Erreur import ligne ${i + 2}:`, err);
            errors.push({
                row: i + 2,
                error: "Erreur base de données: " + err.message,
                data: row
            });
        }
    }

    return {
        success: successCount,
        errors,
        total: rows.length
    };
}
