# Security & OWASP

## Patterns

### **Input Validation**
  #### **Description**
Validate and sanitize all input
  #### **Example**
    import { z } from 'zod';
    import DOMPurify from 'dompurify';
    
    // Schema validation with Zod
    const userSchema = z.object({
      email: z.string().email().max(255),
      name: z.string().min(1).max(100).regex(/^[a-zA-Z\s'-]+$/),
      age: z.number().int().min(0).max(150),
    });
    
    // Validate input
    function validateUser(input: unknown) {
      const result = userSchema.safeParse(input);
      if (!result.success) {
        throw new ValidationError(result.error.issues);
      }
      return result.data;
    }
    
    
    // Sanitize HTML (if you must allow some HTML)
    function sanitizeHtml(dirty: string): string {
      return DOMPurify.sanitize(dirty, {
        ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
        ALLOWED_ATTR: ['href'],
      });
    }
    
    
    // Never trust file extensions
    import { fileTypeFromBuffer } from 'file-type';
    
    async function validateUpload(buffer: Buffer) {
      const type = await fileTypeFromBuffer(buffer);
    
      if (!type || !['image/jpeg', 'image/png'].includes(type.mime)) {
        throw new Error('Invalid file type');
      }
    
      // Also check file size
      if (buffer.length > 5 * 1024 * 1024) {
        throw new Error('File too large');
      }
    
      return type;
    }
    
### **Sql Injection Prevention**
  #### **Description**
Use parameterized queries always
  #### **Example**
    // NEVER: String concatenation
    const query = `SELECT * FROM users WHERE email = '${email}'`;
    
    // ALWAYS: Parameterized queries
    
    // Prisma (safe by default)
    const user = await prisma.user.findUnique({
      where: { email },
    });
    
    // Raw SQL with Prisma
    const users = await prisma.$queryRaw`
      SELECT * FROM users WHERE email = ${email}
    `;
    
    // node-postgres
    const { rows } = await pool.query(
      'SELECT * FROM users WHERE email = $1',
      [email]
    );
    
    // Knex
    const users = await knex('users')
      .where('email', email)
      .select('*');
    
    
    // For dynamic column names (rare case)
    const allowedColumns = ['name', 'email', 'created_at'];
    if (!allowedColumns.includes(sortColumn)) {
      throw new Error('Invalid sort column');
    }
    // Only then use in query
    
### **Xss Prevention**
  #### **Description**
Prevent Cross-Site Scripting attacks
  #### **Example**
    // React escapes by default - this is safe
    function UserName({ name }: { name: string }) {
      return <span>{name}</span>;  // Escaped automatically
    }
    
    // DANGEROUS: dangerouslySetInnerHTML
    // Only use with sanitized content
    function RichContent({ html }: { html: string }) {
      const clean = DOMPurify.sanitize(html);
      return <div dangerouslySetInnerHTML={{ __html: clean }} />;
    }
    
    
    // Content Security Policy header
    // next.config.js
    const securityHeaders = [
      {
        key: 'Content-Security-Policy',
        value: [
          "default-src 'self'",
          "script-src 'self' 'unsafe-inline'",  // Avoid if possible
          "style-src 'self' 'unsafe-inline'",
          "img-src 'self' data: https:",
          "font-src 'self'",
          "connect-src 'self' https://api.example.com",
          "frame-ancestors 'none'",
        ].join('; '),
      },
    ];
    
    
    // Set HttpOnly cookies (JS can't access)
    res.cookie('session', token, {
      httpOnly: true,      // Not accessible via JS
      secure: true,        // HTTPS only
      sameSite: 'strict',  // CSRF protection
      maxAge: 3600000,
    });
    
### **Csrf Protection**
  #### **Description**
Prevent Cross-Site Request Forgery
  #### **Example**
    // Method 1: SameSite cookies (modern approach)
    res.cookie('session', token, {
      sameSite: 'strict',  // Or 'lax' for GET requests from links
      secure: true,
      httpOnly: true,
    });
    
    
    // Method 2: CSRF tokens (traditional)
    import csrf from 'csurf';
    
    // Express middleware
    app.use(csrf({ cookie: true }));
    
    // Include token in forms
    app.get('/form', (req, res) => {
      res.render('form', { csrfToken: req.csrfToken() });
    });
    
    // In HTML
    <input type="hidden" name="_csrf" value="{{csrfToken}}" />
    
    
    // Method 3: Double Submit Cookie
    // Set CSRF token in cookie AND require in header
    const csrfToken = crypto.randomUUID();
    res.cookie('csrf', csrfToken, { sameSite: 'strict' });
    
    // Client must read cookie and send as header
    fetch('/api/action', {
      headers: { 'X-CSRF-Token': getCookie('csrf') },
    });
    
    // Server verifies header matches cookie
    if (req.headers['x-csrf-token'] !== req.cookies.csrf) {
      throw new Error('CSRF validation failed');
    }
    
### **Password Security**
  #### **Description**
Secure password handling
  #### **Example**
    import { hash, verify } from '@node-rs/argon2';
    
    // Hash password (Argon2id recommended)
    async function hashPassword(password: string): Promise<string> {
      return hash(password, {
        memoryCost: 65536,    // 64 MB
        timeCost: 3,          // 3 iterations
        parallelism: 4,       // 4 threads
      });
    }
    
    // Verify password
    async function verifyPassword(
      password: string,
      hashedPassword: string
    ): Promise<boolean> {
      return verify(hashedPassword, password);
    }
    
    
    // Password requirements
    const passwordSchema = z.string()
      .min(12, 'Password must be at least 12 characters')
      .regex(/[a-z]/, 'Must contain lowercase letter')
      .regex(/[A-Z]/, 'Must contain uppercase letter')
      .regex(/[0-9]/, 'Must contain number')
      .refine(
        (pwd) => !commonPasswords.includes(pwd.toLowerCase()),
        'Password is too common'
      );
    
    
    // Rate limiting login attempts
    import rateLimit from 'express-rate-limit';
    
    const loginLimiter = rateLimit({
      windowMs: 15 * 60 * 1000,  // 15 minutes
      max: 5,                     // 5 attempts
      message: 'Too many login attempts, try again later',
      keyGenerator: (req) => req.body.email,  // Per email
    });
    
    app.post('/login', loginLimiter, loginHandler);
    
### **Secure Headers**
  #### **Description**
Set security headers
  #### **Example**
    // next.config.js
    const securityHeaders = [
      // Prevent clickjacking
      {
        key: 'X-Frame-Options',
        value: 'DENY',
      },
      // Prevent MIME sniffing
      {
        key: 'X-Content-Type-Options',
        value: 'nosniff',
      },
      // Enable XSS filter
      {
        key: 'X-XSS-Protection',
        value: '1; mode=block',
      },
      // Control referrer
      {
        key: 'Referrer-Policy',
        value: 'strict-origin-when-cross-origin',
      },
      // HTTPS only
      {
        key: 'Strict-Transport-Security',
        value: 'max-age=31536000; includeSubDomains',
      },
      // Permissions policy
      {
        key: 'Permissions-Policy',
        value: 'camera=(), microphone=(), geolocation=()',
      },
    ];
    
    module.exports = {
      async headers() {
        return [
          {
            source: '/:path*',
            headers: securityHeaders,
          },
        ];
      },
    };
    
### **Authorization**
  #### **Description**
Implement proper access control
  #### **Example**
    // Role-based access control
    type Role = 'user' | 'admin' | 'superadmin';
    
    interface User {
      id: string;
      role: Role;
      organizationId: string;
    }
    
    // Permission definitions
    const permissions = {
      user: ['read:own', 'write:own'],
      admin: ['read:own', 'write:own', 'read:org', 'write:org'],
      superadmin: ['read:all', 'write:all', 'admin:all'],
    };
    
    function hasPermission(user: User, permission: string): boolean {
      return permissions[user.role]?.includes(permission) ?? false;
    }
    
    
    // Resource-level authorization
    async function canAccessResource(
      user: User,
      resourceType: string,
      resourceId: string,
      action: 'read' | 'write'
    ): Promise<boolean> {
      const resource = await getResource(resourceType, resourceId);
    
      // Owner can always access own resources
      if (resource.ownerId === user.id) {
        return true;
      }
    
      // Org admins can access org resources
      if (
        resource.organizationId === user.organizationId &&
        hasPermission(user, `${action}:org`)
      ) {
        return true;
      }
    
      // Superadmins can access anything
      if (hasPermission(user, `${action}:all`)) {
        return true;
      }
    
      return false;
    }
    
    
    // Middleware
    function requirePermission(permission: string) {
      return (req, res, next) => {
        if (!hasPermission(req.user, permission)) {
          return res.status(403).json({ error: 'Forbidden' });
        }
        next();
      };
    }
    
    app.delete(
      '/users/:id',
      requirePermission('admin:all'),
      deleteUserHandler
    );
    

## Anti-Patterns

### **Trusting Client**
  #### **Description**
Trusting client-side validation only
  #### **Wrong**
Client validates, server trusts
  #### **Right**
Validate on both client AND server
### **Security Through Obscurity**
  #### **Description**
Hiding instead of securing
  #### **Wrong**
Hide admin panel at /admin-xyz123
  #### **Right**
Proper authentication and authorization
### **Rolling Own Crypto**
  #### **Description**
Implementing custom cryptography
  #### **Wrong**
Custom password hashing algorithm
  #### **Right**
Use proven libraries (Argon2, bcrypt)
### **Secrets In Code**
  #### **Description**
Hardcoding secrets
  #### **Wrong**
const API_KEY = 'sk_live_xxx'
  #### **Right**
Use environment variables, secrets manager