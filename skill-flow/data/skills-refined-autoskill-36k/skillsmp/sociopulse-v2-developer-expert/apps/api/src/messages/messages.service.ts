import {
    Injectable,
    NotFoundException,
    InternalServerErrorException,
    Logger,
    ForbiddenException,
} from '@nestjs/common';
import { PrismaService } from '../common/prisma/prisma.service';
import { SendMessageDto } from './dto';

@Injectable()
export class MessagesService {
    private readonly logger = new Logger(MessagesService.name);

    constructor(private readonly prisma: PrismaService) { }

    async send(senderId: string, dto: SendMessageDto) {
        try {
            if (dto.missionId) {
                await this.ensureMissionStillOpen(dto.missionId);
            }

            const recipient = await this.prisma.user.findUnique({
                where: { id: dto.recipientId },
            });

            if (!recipient) {
                throw new NotFoundException(`Destinataire ${dto.recipientId} non trouvé`);
            }

            const message = await this.prisma.message.create({
                data: {
                    senderId,
                    receiverId: dto.recipientId,
                    content: dto.content,
                    attachments: [],
                    referenceType: dto.missionId ? 'MISSION' : undefined,
                    referenceId: dto.missionId,
                },
            });

            return message;
        } catch (error) {
            this.logger.error(`send message failed: ${error.message}`);
            if (error instanceof NotFoundException || error instanceof ForbiddenException) {
                throw error;
            }
            throw new InternalServerErrorException("Erreur lors de l'envoi du message");
        }
    }

    private async ensureMissionStillOpen(missionId: string) {
        const mission = await this.prisma.reliefMission.findUnique({
            where: { id: missionId },
            select: { id: true },
        });

        if (!mission) {
            throw new NotFoundException(`Mission ${missionId} introuvable`);
        }

        const report = await this.prisma.missionReport.findUnique({
            where: { missionId },
            select: { createdAt: true },
        });

        if (!report) {
            return;
        }

        const twentyFourHoursMs = 24 * 60 * 60 * 1000;
        const elapsed = Date.now() - report.createdAt.getTime();

        if (elapsed >= twentyFourHoursMs) {
            throw new ForbiddenException(
                'Messages verrouillés : la mission a un rapport final déposé depuis plus de 24h',
            );
        }
    }
}
