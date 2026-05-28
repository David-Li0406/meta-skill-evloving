# File Uploads - Sharp Edges

## Trusting File Type

### **Id**
trusting-file-type
### **Summary**
Trusting client-provided file type
### **Severity**
critical
### **Situation**
  User uploads malware.exe renamed to image.jpg. You check
  extension, looks fine. Store it. Serve it. Another user
  downloads and executes it.
  
### **Why**
  File extensions and Content-Type headers can be faked.
  Attackers rename executables to bypass filters.
  
### **Solution**
  # CHECK MAGIC BYTES
  
  import { fileTypeFromBuffer } from "file-type";
  
  async function validateImage(buffer: Buffer) {
    const type = await fileTypeFromBuffer(buffer);
    
    const allowedTypes = ["image/jpeg", "image/png", "image/webp"];
    
    if (!type || !allowedTypes.includes(type.mime)) {
      throw new Error("Invalid file type");
    }
    
    return type;
  }
  
  // For streams
  import { fileTypeFromStream } from "file-type";
  const type = await fileTypeFromStream(readableStream);
  
### **Symptoms**
  - Malware uploaded as images
  - Wrong content-type served
### **Detection Pattern**


## No Size Limit

### **Id**
no-size-limit
### **Summary**
No upload size restrictions
### **Severity**
high
### **Situation**
  No file size limit. Attacker uploads 10GB file. Server runs
  out of memory or disk. Denial of service. Or massive
  storage bill.
  
### **Why**
  Without limits, attackers can exhaust resources. Even
  legitimate users might accidentally upload huge files.
  
### **Solution**
  # SET SIZE LIMITS
  
  // Formidable
  const form = formidable({
    maxFileSize: 10 * 1024 * 1024, // 10MB
  });
  
  // Multer
  const upload = multer({
    limits: { fileSize: 10 * 1024 * 1024 },
  });
  
  // Client-side early check
  if (file.size > 10 * 1024 * 1024) {
    alert("File too large (max 10MB)");
    return;
  }
  
  // Presigned URL with size limit
  const command = new PutObjectCommand({
    Bucket: BUCKET,
    Key: key,
    ContentLength: expectedSize, // Enforce size
  });
  
### **Symptoms**
  - Server crashes on large uploads
  - Massive storage bills
  - Memory exhaustion
### **Detection Pattern**


## Path Traversal

### **Id**
path-traversal
### **Summary**
User-controlled filename allows path traversal
### **Severity**
critical
### **Situation**
  User uploads file named "../../../etc/passwd". You use
  filename directly. File saved outside upload directory.
  System files overwritten.
  
### **Why**
  User input should never be used directly in file paths.
  Path traversal sequences can escape intended directories.
  
### **Solution**
  # SANITIZE FILENAMES
  
  import path from "path";
  import crypto from "crypto";
  
  function safeFilename(userFilename: string): string {
    // Extract just the base name
    const base = path.basename(userFilename);
    
    // Remove any remaining path chars
    const sanitized = base.replace(/[^a-zA-Z0-9.-]/g, "_");
    
    // Or better: generate new name entirely
    const ext = path.extname(userFilename).toLowerCase();
    const allowed = [".jpg", ".png", ".pdf"];
    
    if (!allowed.includes(ext)) {
      throw new Error("Invalid extension");
    }
    
    return crypto.randomUUID() + ext;
  }
  
  // Never do this
  const path = "uploads/" + req.body.filename; // DANGER!
  
  // Do this
  const path = "uploads/" + safeFilename(req.body.filename);
  
### **Symptoms**
  - Files outside upload directory
  - System file access
### **Detection Pattern**


## Presigned Url Exposure

### **Id**
presigned-url-exposure
### **Summary**
Presigned URL shared or cached incorrectly
### **Severity**
medium
### **Situation**
  Presigned URL for private file returned in API response.
  Response cached by CDN. Anyone with cached URL can access
  private file for hours.
  
### **Why**
  Presigned URLs grant temporary access. If cached or shared,
  access extends beyond intended scope.
  
### **Solution**
  # CONTROL PRESIGNED URL DISTRIBUTION
  
  // Short expiry for sensitive files
  const url = await getSignedUrl(s3, command, {
    expiresIn: 300, // 5 minutes
  });
  
  // No-cache headers for presigned URL responses
  return Response.json({ url }, {
    headers: {
      "Cache-Control": "no-store, max-age=0",
    },
  });
  
  // Or use CloudFront signed URLs for more control
  
### **Symptoms**
  - Private files accessible via cached URLs
  - Access after expiry
### **Detection Pattern**
