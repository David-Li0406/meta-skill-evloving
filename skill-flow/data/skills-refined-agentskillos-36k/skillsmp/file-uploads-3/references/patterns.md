# File Uploads & Storage

## Patterns

### **Presigned Upload**
  #### **Description**
Direct upload with presigned URLs
  #### **Example**
    // Server: Generate presigned URL
    import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
    import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
    
    const s3 = new S3Client({
      region: "auto",
      endpoint: process.env.S3_ENDPOINT,
      credentials: {
        accessKeyId: process.env.S3_ACCESS_KEY!,
        secretAccessKey: process.env.S3_SECRET_KEY!,
      },
    });
    
    export async function getUploadUrl(filename: string, contentType: string) {
      const key = "uploads/" + crypto.randomUUID() + "-" + filename;
      
      const command = new PutObjectCommand({
        Bucket: process.env.S3_BUCKET,
        Key: key,
        ContentType: contentType,
      });
    
      const url = await getSignedUrl(s3, command, { expiresIn: 3600 });
      return { url, key };
    }
    
    
    // Client: Upload directly to storage
    async function uploadFile(file: File) {
      // Get presigned URL from your API
      const { url, key } = await fetch("/api/upload", {
        method: "POST",
        body: JSON.stringify({
          filename: file.name,
          contentType: file.type,
        }),
      }).then(r => r.json());
    
      // Upload directly to S3/R2
      await fetch(url, {
        method: "PUT",
        body: file,
        headers: { "Content-Type": file.type },
      });
    
      return key;
    }
    
### **Server Upload**
  #### **Description**
Server-side upload handling
  #### **Example**
    // Next.js API route with formidable
    import formidable from "formidable";
    import { createReadStream } from "fs";
    
    export const config = { api: { bodyParser: false } };
    
    export async function POST(req: Request) {
      const form = formidable({
        maxFileSize: 10 * 1024 * 1024, // 10MB
        filter: ({ mimetype }) => {
          return mimetype?.startsWith("image/") ?? false;
        },
      });
    
      const [fields, files] = await form.parse(req);
      const file = files.file?.[0];
    
      if (!file) {
        return Response.json({ error: "No file" }, { status: 400 });
      }
    
      // Upload to S3
      const stream = createReadStream(file.filepath);
      await s3.send(new PutObjectCommand({
        Bucket: BUCKET,
        Key: "uploads/" + file.newFilename,
        Body: stream,
        ContentType: file.mimetype,
      }));
    
      return Response.json({ key: file.newFilename });
    }
    
### **Image Optimization**
  #### **Description**
Image processing on upload
  #### **Example**
    import sharp from "sharp";
    
    async function processImage(buffer: Buffer) {
      // Resize and convert to WebP
      const optimized = await sharp(buffer)
        .resize(1200, 1200, {
          fit: "inside",
          withoutEnlargement: true,
        })
        .webp({ quality: 80 })
        .toBuffer();
    
      // Generate thumbnail
      const thumbnail = await sharp(buffer)
        .resize(200, 200, { fit: "cover" })
        .webp({ quality: 70 })
        .toBuffer();
    
      return { optimized, thumbnail };
    }
    

## Anti-Patterns

### **Trusting Extension**
  #### **Description**
Trusting file extension for type
  #### **Wrong**
if (file.name.endsWith('.jpg'))
  #### **Right**
Check magic bytes or content-type
### **Buffering Large**
  #### **Description**
Loading large files into memory
  #### **Wrong**
const buffer = await file.arrayBuffer()
  #### **Right**
Stream to storage directly
### **No Size Limit**
  #### **Description**
No file size restrictions
  #### **Wrong**
Accept any file size
  #### **Right**
Set maxFileSize, reject large files