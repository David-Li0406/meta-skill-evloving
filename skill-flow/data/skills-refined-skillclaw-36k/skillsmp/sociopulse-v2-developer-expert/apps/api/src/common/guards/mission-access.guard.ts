import {
    CanActivate,
    ExecutionContext,
    ForbiddenException,
    Injectable,
    Logger,
    NotFoundException,
} from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { Request } from 'express';

@Injectable()
export class MissionAccessGuard implements CanActivate {
    private readonly logger = new Logger(MissionAccessGuard.name);

    constructor(private readonly prisma: PrismaService) { }

    async canActivate(context: ExecutionContext): Promise<boolean> {
        const request = context.switchToHttp().getRequest<Request>();
        const missionId = this.extractMissionId(request);

        if (!missionId) {
            return true;
        }

        const user = request.user as { id?: string; role?: string } | undefined;

        if (!user?.id) {
            throw new ForbiddenException('Authentification requise pour acceder a cette mission');
        }

        const mission = await this.prisma.reliefMission.findUnique({
            where: { id: missionId },
            select: { clientId: true, assignedTalentId: true },
        });

        if (!mission) {
            throw new NotFoundException(`Mission ${missionId} introuvable`);
        }

        if (user.role === 'ADMIN') {
            return true;
        }

        const isParticipant =
            mission.clientId === user.id || mission.assignedTalentId === user.id;

        if (!isParticipant) {
            this.logger.warn(
                `Mission access denied for user ${user.id} on mission ${missionId}`,
            );
            throw new ForbiddenException(
                'Acces refuse : vous devez etre client ou talent assigne de la mission',
            );
        }

        return true;
    }

    private extractMissionId(request: Request): string | undefined {
        const paramsMissionId = request.params?.missionId || request.params?.id;
        if (paramsMissionId) {
            return paramsMissionId;
        }

        if (typeof request.body === 'object' && request.body !== null) {
            const missionId = (request.body as any).missionId || (request.body as any).mission_id;
            if (missionId) {
                return missionId;
            }
        }

        return undefined;
    }
}
