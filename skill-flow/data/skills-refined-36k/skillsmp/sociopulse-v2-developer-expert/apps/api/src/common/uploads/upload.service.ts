import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import { promises as fs } from 'fs';
import { join, dirname } from 'path';
import { v4 as uuidv4 } from 'uuid';

type StorageDriver = 's3' | 'local';

interface UploadParams {
    buffer: Buffer;
    filename: string;
    contentType?: string;
    folder?: string;
}

@Injectable()
export class UploadService {
    private readonly logger = new Logger(UploadService.name);
    private readonly bucket?: string;
    private readonly region: string;
    private readonly endpoint?: string;
    private readonly driver: StorageDriver;
    private readonly localBaseDir: string;
    private readonly publicBaseUrl: string;
    private s3?: S3Client;

    constructor(private readonly configService: ConfigService) {
        this.bucket = this.configService.get<string>('S3_BUCKET');
        this.region = this.configService.get<string>('S3_REGION', 'eu-west-3');
        this.endpoint = this.configService.get<string>('S3_ENDPOINT');
        this.localBaseDir = this.configService.get<string>('LOCAL_UPLOAD_DIR', 'uploads');
        const apiUrl = this.configService.get<string>('API_URL') || 'http://localhost:4000';
        this.publicBaseUrl = this.configService.get<string>('FILES_BASE_URL') || `${apiUrl}/uploads`;
        this.driver = this.bucket ? 's3' : 'local';

        if (this.driver === 's3') {
            const accessKeyId = this.configService.get<string>('S3_ACCESS_KEY_ID');
            const secretAccessKey = this.configService.get<string>('S3_SECRET_ACCESS_KEY');

            this.s3 = new S3Client({
                region: this.region,
                endpoint: this.endpoint || undefined,
                forcePathStyle: !!this.endpoint,
                credentials: accessKeyId && secretAccessKey ? { accessKeyId, secretAccessKey } : undefined,
            });

            this.logger.log(`UploadService configured for S3 bucket ${this.bucket} (region: ${this.region})`);
        } else {
            this.logger.log(`UploadService configured for local storage at ${this.localBaseDir}`);
        }
    }

    async upload(params: UploadParams) {
        const key = this.buildKey(params.filename, params.folder);

        if (this.driver === 's3') {
            await this.uploadToS3(key, params.buffer, params.contentType);
        } else {
            await this.uploadToLocal(key, params.buffer);
        }

        return {
            key,
            url: this.buildPublicUrl(key),
            driver: this.driver,
        };
    }

    private buildKey(filename: string, folder?: string) {
        const safeName = filename.replace(/\s+/g, '-').toLowerCase();
        const finalName = `${uuidv4()}-${safeName}`;
        return folder ? `${folder}/${finalName}` : finalName;
    }

    private async uploadToS3(key: string, body: Buffer, contentType?: string) {
        if (!this.s3 || !this.bucket) {
            throw new Error('S3 client not configured');
        }

        await this.s3.send(
            new PutObjectCommand({
                Bucket: this.bucket,
                Key: key,
                Body: body,
                ContentType: contentType,
                ACL: 'public-read',
            }),
        );
    }

    private async uploadToLocal(key: string, body: Buffer) {
        const absolutePath = join(process.cwd(), this.localBaseDir, key);
        await fs.mkdir(dirname(absolutePath), { recursive: true });
        await fs.writeFile(absolutePath, body);
    }

    private buildPublicUrl(key: string) {
        if (this.driver === 's3') {
            if (this.endpoint) {
                return `${this.endpoint.replace(/\/$/, '')}/${this.bucket}/${key}`;
            }
            return `https://${this.bucket}.s3.${this.region}.amazonaws.com/${key}`;
        }

        return `${this.publicBaseUrl.replace(/\/$/, '')}/${key}`;
    }
}
