# NestJS File Upload Patterns

## Basic Upload

```typescript
import {
  Controller,
  Post,
  UseInterceptors,
  UploadedFile,
  ParseFilePipe,
  MaxFileSizeValidator,
  FileTypeValidator,
} from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { diskStorage } from 'multer';

@Controller('files')
export class FilesController {
  @Post('upload')
  @UseInterceptors(FileInterceptor('file', {
    storage: diskStorage({
      destination: './uploads',
      filename: (req, file, cb) => {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1e9);
        cb(null, `${uniqueSuffix}-${file.originalname}`);
      },
    }),
  }))
  uploadFile(
    @UploadedFile(
      new ParseFilePipe({
        validators: [
          new MaxFileSizeValidator({ maxSize: 5 * 1024 * 1024 }), // 5MB
          new FileTypeValidator({ fileType: /image\/(jpeg|png|gif)/ }),
        ],
      }),
    )
    file: Express.Multer.File,
  ) {
    return { filename: file.filename, size: file.size };
  }
}
```

## Multiple Files

```typescript
import { FilesInterceptor, FileFieldsInterceptor } from '@nestjs/platform-express';

@Post('multiple')
@UseInterceptors(FilesInterceptor('files', 10))
uploadMultiple(@UploadedFiles() files: Express.Multer.File[]) {
  return files.map(f => ({ name: f.filename, size: f.size }));
}

@Post('fields')
@UseInterceptors(FileFieldsInterceptor([
  { name: 'avatar', maxCount: 1 },
  { name: 'documents', maxCount: 5 },
]))
uploadFields(@UploadedFiles() files: {
  avatar?: Express.Multer.File[],
  documents?: Express.Multer.File[],
}) {
  return { avatar: files.avatar?.[0], documents: files.documents };
}
```

## S3 Upload

```typescript
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

@Injectable()
export class S3Service {
  private s3: S3Client;

  constructor(private config: ConfigService) {
    this.s3 = new S3Client({
      region: config.get('AWS_REGION'),
      credentials: {
        accessKeyId: config.get('AWS_ACCESS_KEY'),
        secretAccessKey: config.get('AWS_SECRET_KEY'),
      },
    });
  }

  async upload(file: Express.Multer.File, key: string): Promise<string> {
    await this.s3.send(new PutObjectCommand({
      Bucket: this.config.get('S3_BUCKET'),
      Key: key,
      Body: file.buffer,
      ContentType: file.mimetype,
    }));

    return `https://${this.config.get('S3_BUCKET')}.s3.amazonaws.com/${key}`;
  }

  async getPresignedUrl(key: string): Promise<string> {
    const command = new PutObjectCommand({
      Bucket: this.config.get('S3_BUCKET'),
      Key: key,
    });
    return getSignedUrl(this.s3, command, { expiresIn: 3600 });
  }
}
```

## Streaming Large Files

```typescript
import { StreamableFile } from '@nestjs/common';
import { createReadStream } from 'fs';

@Get('download/:filename')
downloadFile(@Param('filename') filename: string): StreamableFile {
  const file = createReadStream(`./uploads/${filename}`);
  return new StreamableFile(file, {
    type: 'application/octet-stream',
    disposition: `attachment; filename="${filename}"`,
  });
}
```
