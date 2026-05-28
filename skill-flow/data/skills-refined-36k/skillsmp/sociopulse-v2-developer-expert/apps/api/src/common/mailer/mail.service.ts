import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import nodemailer, { Transporter } from 'nodemailer';

interface MailParams {
    to: string | string[];
    subject: string;
    html: string;
    text?: string;
}

@Injectable()
export class MailService {
    private readonly logger = new Logger(MailService.name);
    private readonly transporter?: Transporter;
    private readonly from: string;

    constructor(private readonly configService: ConfigService) {
        const host = this.configService.get<string>('SMTP_HOST');
        const port = parseInt(this.configService.get<string>('SMTP_PORT', '587'), 10);
        const user = this.configService.get<string>('SMTP_USER');
        const pass = this.configService.get<string>('SMTP_PASS');
        const secure = this.configService.get<string>('SMTP_SECURE', 'false') === 'true';

        this.from = this.configService.get<string>('MAIL_FROM') || 'no-reply@sociopulse.fr';

        if (!host) {
            this.logger.log('MODE PROTOTYPE : SMTP absent, envoi des emails en console.');
            return;
        }

        this.transporter = nodemailer.createTransport({
            host,
            port,
            secure,
            auth: user && pass ? { user, pass } : undefined,
        });
    }

    async sendMail(params: MailParams) {
        if (!this.transporter) {
            this.logger.log('[MAIL MOCK]', { to: params.to, subject: params.subject, html: params.html, text: params.text });
            return;
        }

        await this.transporter.sendMail({
            from: this.from,
            ...params,
        });
    }

    async sendCriticalMissionAlert(mission: {
        title: string;
        jobTitle: string;
        city?: string;
        startDate: Date;
        clientEmail?: string | null;
    }) {
        const alertRecipient =
            this.configService.get<string>('ALERT_EMAIL') ||
            mission.clientEmail ||
            this.from;

        const subject = `Mission CRITICAL : ${mission.title || mission.jobTitle}`;
        const readableDate = mission.startDate
            ? new Date(mission.startDate).toLocaleString('fr-FR')
            : '';

        const html = `
            <h2>Nouvelle mission CRITICAL</h2>
            <p><strong>Mission :</strong> ${mission.title || mission.jobTitle}</p>
            <p><strong>Ville :</strong> ${mission.city || 'N/A'}</p>
            <p><strong>Debut :</strong> ${readableDate}</p>
            <p>Merci d'assigner un talent en priorite.</p>
        `;

        await this.sendMail({
            to: alertRecipient,
            subject,
            html,
            text: `Mission CRITICAL ${mission.title || mission.jobTitle} - ${mission.city || ''} - debut ${readableDate}`,
        });
    }

    async sendContractReadyEmail(contract: {
        reference?: string | null;
        clientEmail?: string | null;
        talentEmail?: string | null;
        missionTitle?: string | null;
    }) {
        const recipients = [contract.clientEmail, contract.talentEmail].filter(Boolean) as string[];

        if (recipients.length === 0) {
            this.logger.warn('No recipients found for contract ready email');
            return;
        }

        const subject = `Contrat pret a etre signe ${contract.reference || ''}`.trim();
        const html = `
            <h2>Contrat pret a signature</h2>
            <p>Mission : ${contract.missionTitle || 'Mission SOS'}</p>
            <p>Reference : ${contract.reference || 'N/A'}</p>
            <p>Connectez-vous a votre espace Les Extras pour signer le contrat.</p>
        `;

        await this.sendMail({
            to: recipients,
            subject,
            html,
            text: `Contrat pret a signature - ${contract.reference || ''}`,
        });
    }
}
