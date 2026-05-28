import { Body, Controller, Get, Param, Post, Res, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import { Response } from 'express';
import { ContractsService } from './contracts.service';
import { SignContractDto } from './dto';
import { JwtAuthGuard } from '../common/guards';
import { CurrentUser, CurrentUserPayload } from '../common/decorators';

@ApiTags('contracts')
@Controller('contracts')
export class ContractsController {
    constructor(private readonly contractsService: ContractsService) { }

    @Get()
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Récupérer tous les contrats de l\'utilisateur' })
    async getContracts(@CurrentUser() user: CurrentUserPayload) {
        return this.contractsService.getContracts(user.id);
    }

    @Get(':id')
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Récupérer un contrat par ID' })
    async getContractById(
        @Param('id') id: string,
        @CurrentUser() user: CurrentUserPayload,
    ) {
        return this.contractsService.getContractById(id, user.id);
    }

    @Post('sign')
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Signer un contrat de mission SOS' })
    async sign(
        @CurrentUser() user: CurrentUserPayload,
        @Body() dto: SignContractDto,
    ) {
        return this.contractsService.signContract(user.id, dto);
    }

    @Post(':id/sign')
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Signer un contrat existant' })
    async signById(
        @Param('id') id: string,
        @CurrentUser() user: CurrentUserPayload,
        @Body() dto: { signature: string },
    ) {
        // Get contract to find missionId
        const contract = await this.contractsService.getContractById(id, user.id);
        return this.contractsService.signContract(user.id, {
            missionId: contract.mission?.id || id,
            signature: dto.signature,
            content: contract.content,
        });
    }

    @Get(':id/download')
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Télécharger le PDF du contrat' })
    async downloadPdf(
        @Param('id') id: string,
        @CurrentUser() user: CurrentUserPayload,
        @Res() res: Response,
    ) {
        const { buffer, filename } = await this.contractsService.downloadPdf(id, user.id);

        res.set({
            'Content-Type': 'application/pdf',
            'Content-Disposition': `attachment; filename="${filename}"`,
            'Content-Length': buffer.length,
        });

        res.send(buffer);
    }

    @Post(':id/generate-pdf')
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Régénérer le PDF du contrat' })
    async regeneratePdf(
        @Param('id') id: string,
        @CurrentUser() user: CurrentUserPayload,
    ) {
        // Verify access
        await this.contractsService.getContractById(id, user.id);
        await this.contractsService.generatePdf(id);
        return { success: true, message: 'PDF régénéré avec succès' };
    }
}
