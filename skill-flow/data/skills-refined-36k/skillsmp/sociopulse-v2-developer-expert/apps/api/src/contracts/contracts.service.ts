import {
    Injectable,
    NotFoundException,
    BadRequestException,
    InternalServerErrorException,
    Logger,
} from '@nestjs/common';
import { PrismaService } from '../common/prisma/prisma.service';
import { SignContractDto } from './dto';
import { PDFDocument, rgb, StandardFonts } from 'pdf-lib';
import { MailService } from '../common/mailer';

@Injectable()
export class ContractsService {
    private readonly logger = new Logger(ContractsService.name);

    constructor(
        private readonly prisma: PrismaService,
        private readonly mailService: MailService,
    ) { }

    /**
     * Get all contracts for a user
     */
    async getContracts(userId: string) {
        const contracts = await this.prisma.contract.findMany({
            where: {
                OR: [
                    { talentId: userId },
                    { clientId: userId },
                ],
            },
            include: {
                talent: {
                    select: {
                        id: true,
                        email: true,
                        profile: { select: { firstName: true, lastName: true, avatarUrl: true } },
                    },
                },
                client: {
                    select: {
                        id: true,
                        email: true,
                        establishment: { select: { name: true, address: true, city: true } },
                        profile: { select: { firstName: true, lastName: true } },
                    },
                },
                mission: {
                    select: {
                        id: true,
                        title: true,
                        city: true,
                    },
                },
            },
            orderBy: { createdAt: 'desc' },
        });

        return { contracts };
    }

    /**
     * Get contract by ID
     */
    async getContractById(contractId: string, userId?: string) {
        const contract = await this.prisma.contract.findUnique({
            where: { id: contractId },
            include: {
                talent: {
                    select: {
                        id: true,
                        email: true,
                        profile: { select: { firstName: true, lastName: true, avatarUrl: true } },
                    },
                },
                client: {
                    select: {
                        id: true,
                        email: true,
                        establishment: { select: { name: true, address: true, city: true } },
                        profile: { select: { firstName: true, lastName: true } },
                    },
                },
                mission: {
                    select: {
                        id: true,
                        title: true,
                        description: true,
                        city: true,
                        address: true,
                        hourlyRate: true,
                        startDate: true,
                        endDate: true,
                    },
                },
                quote: {
                    select: {
                        id: true,
                        reference: true,
                    },
                },
            },
        });

        if (!contract) {
            throw new NotFoundException(`Contrat ${contractId} non trouvé`);
        }

        return contract;
    }

    /**
     * Sign contract
     */
    async signContract(talentId: string, dto: SignContractDto) {
        try {
            const mission = await this.prisma.reliefMission.findUnique({
                where: { id: dto.missionId },
                include: { contract: true },
            });

            if (!mission) {
                throw new NotFoundException(`Mission ${dto.missionId} non trouvée`);
            }

            if (mission.status === 'CANCELLED') {
                throw new BadRequestException('Mission annulée');
            }

            const content = dto.content || mission.description || 'Contrat de mission SOS';
            const signatureUrl = dto.signature;
            const now = new Date();

            // Generate contract reference
            const year = now.getFullYear();
            const count = await this.prisma.contract.count({
                where: { createdAt: { gte: new Date(`${year}-01-01`) } },
            });
            const reference = `CTR-${year}-${String(count + 1).padStart(4, '0')}`;

            const contract = await this.prisma.contract.upsert({
                where: { missionId: dto.missionId },
                update: {
                    talentId,
                    content,
                    signatureUrl,
                    status: 'SIGNED',
                    signedAt: now,
                    extraSignedAt: now,
                },
                create: {
                    reference,
                    missionId: dto.missionId,
                    clientId: mission.clientId,
                    talentId,
                    title: mission.title,
                    content,
                    signatureUrl,
                    status: 'SIGNED',
                    signedAt: now,
                    extraSignedAt: now,
                    startDate: mission.startDate,
                    endDate: mission.endDate,
                    totalAmount: mission.totalBudget ? Math.round(mission.totalBudget * 100) : null,
                },
            });

            await this.prisma.reliefMission.update({
                where: { id: dto.missionId },
                data: {
                    assignedTalentId: mission.assignedTalentId || talentId,
                    status: 'ASSIGNED',
                },
            });

            this.logger.log(`Contract signed for mission ${dto.missionId} by ${talentId}`);

            // Generate PDF after signing
            try {
                await this.generatePdf(contract.id);
            } catch (pdfError) {
                const message = pdfError instanceof Error ? pdfError.message : String(pdfError);
                this.logger.error(`PDF generation failed: ${message}`);
                // Don't fail the whole signing process if PDF generation fails
            }

            const participants = await this.prisma.user.findMany({
                where: { id: { in: [mission.clientId, talentId] } },
                select: { id: true, email: true },
            });

            const clientEmail = participants.find((p) => p.id === mission.clientId)?.email;
            const talentEmail = participants.find((p) => p.id === talentId)?.email;

            await this.mailService.sendContractReadyEmail({
                reference: contract.reference,
                clientEmail,
                talentEmail,
                missionTitle: mission.title,
            });

            return contract;
        } catch (error) {
            const message = error instanceof Error ? error.message : String(error);
            this.logger.error(`signContract failed: ${message}`);
            if (error instanceof NotFoundException || error instanceof BadRequestException) {
                throw error;
            }
            throw new InternalServerErrorException('Erreur lors de la signature du contrat');
        }
    }

    /**
     * Generate PDF for a signed contract
     */
    async generatePdf(contractId: string): Promise<Buffer> {
        const contract = await this.prisma.contract.findUnique({
            where: { id: contractId },
            include: {
                talent: {
                    select: {
                        email: true,
                        profile: { select: { firstName: true, lastName: true } },
                    },
                },
                client: {
                    select: {
                        email: true,
                        establishment: { select: { name: true, address: true, city: true } },
                        profile: { select: { firstName: true, lastName: true } },
                    },
                },
                mission: {
                    select: {
                        title: true,
                        description: true,
                        city: true,
                        address: true,
                        hourlyRate: true,
                        startDate: true,
                        endDate: true,
                    },
                },
            },
        });

        if (!contract) {
            throw new NotFoundException(`Contrat ${contractId} non trouvé`);
        }

        // Create PDF document
        const pdfDoc = await PDFDocument.create();
        const page = pdfDoc.addPage([595.28, 841.89]); // A4
        const { width, height } = page.getSize();

        // Load fonts
        const helvetica = await pdfDoc.embedFont(StandardFonts.Helvetica);
        const helveticaBold = await pdfDoc.embedFont(StandardFonts.HelveticaBold);

        // Colors
        const coralColor = rgb(1, 0.42, 0.42);
        const darkGray = rgb(0.2, 0.2, 0.2);
        const lightGray = rgb(0.5, 0.5, 0.5);

        let y = height - 50;

        // Header - Logo/Title
        page.drawText('Les Extras', {
            x: 50,
            y,
            size: 24,
            font: helveticaBold,
            color: coralColor,
        });

        page.drawText('CONTRAT DE MISSION', {
            x: width - 200,
            y,
            size: 12,
            font: helveticaBold,
            color: darkGray,
        });

        y -= 20;
        page.drawText(contract.reference || contractId.slice(0, 10).toUpperCase(), {
            x: width - 200,
            y,
            size: 10,
            font: helvetica,
            color: lightGray,
        });

        // Horizontal line
        y -= 30;
        page.drawLine({
            start: { x: 50, y },
            end: { x: width - 50, y },
            thickness: 1,
            color: rgb(0.9, 0.9, 0.9),
        });

        y -= 40;

        // Contract parties section
        page.drawText('PARTIES', {
            x: 50,
            y,
            size: 14,
            font: helveticaBold,
            color: darkGray,
        });

        y -= 25;

        // Talent (Prestataire)
        const talentName = contract.talent?.profile
            ? `${contract.talent.profile.firstName} ${contract.talent.profile.lastName}`
            : contract.talent?.email || 'N/A';

        page.drawText('LE PRESTATAIRE :', {
            x: 50,
            y,
            size: 10,
            font: helveticaBold,
            color: lightGray,
        });

        y -= 15;
        page.drawText(talentName, {
            x: 50,
            y,
            size: 11,
            font: helvetica,
            color: darkGray,
        });

        y -= 30;

        // Client
        const clientName = contract.client?.establishment?.name
            || (contract.client?.profile ? `${contract.client.profile.firstName} ${contract.client.profile.lastName}` : null)
            || contract.client?.email
            || 'N/A';
        const clientAddress = contract.client?.establishment
            ? `${contract.client.establishment.address || ''}, ${contract.client.establishment.city || ''}`
            : '';

        page.drawText('LE CLIENT :', {
            x: 50,
            y,
            size: 10,
            font: helveticaBold,
            color: lightGray,
        });

        y -= 15;
        page.drawText(clientName, {
            x: 50,
            y,
            size: 11,
            font: helvetica,
            color: darkGray,
        });

        if (clientAddress.trim().length > 2) {
            y -= 15;
            page.drawText(clientAddress, {
                x: 50,
                y,
                size: 10,
                font: helvetica,
                color: lightGray,
            });
        }

        y -= 40;

        // Mission details
        if (contract.mission) {
            page.drawText('MISSION', {
                x: 50,
                y,
                size: 14,
                font: helveticaBold,
                color: darkGray,
            });

            y -= 25;
            page.drawText(contract.mission.title || 'Mission SOS', {
                x: 50,
                y,
                size: 12,
                font: helveticaBold,
                color: coralColor,
            });

            y -= 20;
            const location = `${contract.mission.address || ''}, ${contract.mission.city || ''}`.trim();
            if (location.length > 1) {
                page.drawText(`Lieu : ${location}`, {
                    x: 50,
                    y,
                    size: 10,
                    font: helvetica,
                    color: darkGray,
                });
                y -= 15;
            }

            if (contract.mission.hourlyRate) {
                page.drawText(`Taux horaire : ${contract.mission.hourlyRate} €/h`, {
                    x: 50,
                    y,
                    size: 10,
                    font: helvetica,
                    color: darkGray,
                });
                y -= 15;
            }

            const startDate = contract.mission.startDate
                ? new Date(contract.mission.startDate).toLocaleDateString('fr-FR')
                : '';
            const endDate = contract.mission.endDate
                ? new Date(contract.mission.endDate).toLocaleDateString('fr-FR')
                : '';

            if (startDate || endDate) {
                page.drawText(`Période : ${startDate} - ${endDate}`, {
                    x: 50,
                    y,
                    size: 10,
                    font: helvetica,
                    color: darkGray,
                });
                y -= 15;
            }

            y -= 20;

            // Description
            if (contract.mission.description) {
                page.drawText('Description :', {
                    x: 50,
                    y,
                    size: 10,
                    font: helveticaBold,
                    color: lightGray,
                });
                y -= 15;

                // Word wrap description
                const words = contract.mission.description.split(' ');
                let line = '';
                const maxWidth = width - 100;

                for (const word of words) {
                    const testLine = line + (line ? ' ' : '') + word;
                    const textWidth = helvetica.widthOfTextAtSize(testLine, 10);

                    if (textWidth > maxWidth && line) {
                        page.drawText(line, {
                            x: 50,
                            y,
                            size: 10,
                            font: helvetica,
                            color: darkGray,
                        });
                        line = word;
                        y -= 14;

                        if (y < 150) break; // Stop if we're running out of space
                    } else {
                        line = testLine;
                    }
                }

                if (line && y >= 150) {
                    page.drawText(line, {
                        x: 50,
                        y,
                        size: 10,
                        font: helvetica,
                        color: darkGray,
                    });
                    y -= 14;
                }
            }
        }

        y -= 30;

        // Signature section
        page.drawText('SIGNATURES', {
            x: 50,
            y,
            size: 14,
            font: helveticaBold,
            color: darkGray,
        });

        y -= 30;

        // Extra signature
        page.drawText('Signature du Prestataire :', {
            x: 50,
            y,
            size: 10,
            font: helveticaBold,
            color: lightGray,
        });

        y -= 15;

        if (contract.extraSignedAt) {
            const signedDate = new Date(contract.extraSignedAt).toLocaleDateString('fr-FR', {
                day: 'numeric',
                month: 'long',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
            });
            page.drawText(`Signé le ${signedDate}`, {
                x: 50,
                y,
                size: 9,
                font: helvetica,
                color: lightGray,
            });
            y -= 12;
        }

        // Embed signature image if available
        if (contract.signatureUrl && contract.signatureUrl.startsWith('data:image/png')) {
            try {
                const base64Data = contract.signatureUrl.replace(/^data:image\/png;base64,/, '');
                const signatureBytes = Buffer.from(base64Data, 'base64');
                const signatureImage = await pdfDoc.embedPng(signatureBytes);

                const sigWidth = 150;
                const sigHeight = (signatureImage.height / signatureImage.width) * sigWidth;

                page.drawImage(signatureImage, {
                    x: 50,
                    y: y - sigHeight,
                    width: sigWidth,
                    height: sigHeight,
                });

                y -= sigHeight + 10;
            } catch (sigError) {
                const message = sigError instanceof Error ? sigError.message : String(sigError);
                this.logger.warn(`Could not embed signature image: ${message}`);
                page.drawText('[Signature électronique enregistrée]', {
                    x: 50,
                    y,
                    size: 10,
                    font: helvetica,
                    color: darkGray,
                });
                y -= 15;
            }
        }

        // Footer
        const footerY = 50;
        page.drawLine({
            start: { x: 50, y: footerY + 20 },
            end: { x: width - 50, y: footerY + 20 },
            thickness: 0.5,
            color: rgb(0.9, 0.9, 0.9),
        });

        page.drawText('Les Extras - Plateforme de mise en relation médico-social', {
            x: 50,
            y: footerY,
            size: 8,
            font: helvetica,
            color: lightGray,
        });

        page.drawText(`Généré le ${new Date().toLocaleDateString('fr-FR')}`, {
            x: width - 150,
            y: footerY,
            size: 8,
            font: helvetica,
            color: lightGray,
        });

        // Serialize PDF
        const pdfBytes = await pdfDoc.save();
        const pdfBuffer = Buffer.from(pdfBytes);

        // Store PDF as base64 data URL in database
        const pdfBase64 = `data:application/pdf;base64,${pdfBuffer.toString('base64')}`;

        await this.prisma.contract.update({
            where: { id: contractId },
            data: { pdfUrl: pdfBase64 },
        });

        this.logger.log(`PDF generated for contract ${contractId}`);

        return pdfBuffer;
    }

    /**
     * Download PDF for a contract
     */
    async downloadPdf(contractId: string, userId: string): Promise<{ buffer: Buffer; filename: string }> {
        const contract = await this.prisma.contract.findUnique({
            where: { id: contractId },
            select: {
                id: true,
                reference: true,
                pdfUrl: true,
                talentId: true,
                clientId: true,
                status: true,
            },
        });

        if (!contract) {
            throw new NotFoundException(`Contrat ${contractId} non trouvé`);
        }

        // Check access rights
        if (contract.talentId !== userId && contract.clientId !== userId) {
            throw new BadRequestException('Accès non autorisé à ce contrat');
        }

        // Generate PDF if not exists
        let pdfBuffer: Buffer;

        if (contract.pdfUrl && contract.pdfUrl.startsWith('data:application/pdf;base64,')) {
            const base64Data = contract.pdfUrl.replace('data:application/pdf;base64,', '');
            pdfBuffer = Buffer.from(base64Data, 'base64');
        } else {
            pdfBuffer = await this.generatePdf(contractId);
        }

        const filename = `contrat-${contract.reference || contractId.slice(0, 8)}.pdf`;

        return { buffer: pdfBuffer, filename };
    }
}
