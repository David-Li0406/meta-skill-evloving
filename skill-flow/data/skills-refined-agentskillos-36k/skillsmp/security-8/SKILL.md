---
name: Security
description: Authentication, JWT tokens, CORS, security headers, and secrets management.
---

# Security

## Context

Lumira V2 implements security at multiple layers:

| Layer | Implementation |
|-------|----------------|
| Authentication | NextAuth.js (Frontend), JWT (API) |
| Authorization | Role-based guards |
| Transport | HTTPS (via Coolify/Traefik) |
| Headers | Helmet.js |

---

## Authentication Flow

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Client  │───▶│ NextAuth │───▶│   API    │───▶│   DB     │
│          │    │  (OAuth) │    │  (JWT)   │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │
     │  1. Login     │               │
     │──────────────▶│               │
     │               │  2. Verify    │
     │               │──────────────▶│
     │               │               │  3. Check user
     │               │               │──────────────▶│
     │               │◀──────────────│◀──────────────│
     │  4. JWT Token │               │
     │◀──────────────│               │
```

---

## NextAuth.js Configuration

### Location: `apps/web/lib/auth.ts`

```typescript
import NextAuth from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';

export const authOptions = {
  providers: [
    CredentialsProvider({
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        const res = await fetch(`${API_URL}/auth/login`, {
          method: 'POST',
          body: JSON.stringify(credentials),
          headers: { 'Content-Type': 'application/json' },
        });
        const user = await res.json();
        if (res.ok && user) return user;
        return null;
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) token.accessToken = user.accessToken;
      return token;
    },
    async session({ session, token }) {
      session.accessToken = token.accessToken;
      return session;
    },
  },
  pages: {
    signIn: '/login',
    error: '/login',
  },
  secret: process.env.NEXTAUTH_SECRET,
};
```

---

## JWT Token Strategy

### API Implementation

```typescript
// apps/api/src/auth/auth.service.ts
@Injectable()
export class AuthService {
  constructor(private jwtService: JwtService) {}

  async login(user: User) {
    const payload = { sub: user.id, email: user.email, role: user.role };
    return {
      accessToken: this.jwtService.sign(payload, { expiresIn: '1h' }),
      refreshToken: this.jwtService.sign(payload, { expiresIn: '7d' }),
    };
  }

  async refreshToken(refreshToken: string) {
    const payload = this.jwtService.verify(refreshToken);
    return this.login({ id: payload.sub, email: payload.email, role: payload.role });
  }
}
```

### JWT Guard

```typescript
// apps/api/src/auth/jwt.guard.ts
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  canActivate(context: ExecutionContext) {
    return super.canActivate(context);
  }
}
```

---

## Role-Based Authorization

```typescript
// Decorator
export const Roles = (...roles: Role[]) => SetMetadata('roles', roles);

// Guard
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<Role[]>('roles', [
      context.getHandler(),
      context.getClass(),
    ]);
    if (!requiredRoles) return true;
    
    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.includes(user.role);
  }
}

// Usage
@Roles(Role.ADMIN)
@UseGuards(JwtAuthGuard, RolesGuard)
@Get('admin/users')
getUsers() { ... }
```

---

## CORS Configuration

```typescript
// apps/api/src/main.ts
app.enableCors({
  origin: process.env.CORS_ORIGINS?.split(',') || [
    'https://sociopulse.fr',
    'https://medicopulse.fr',
  ],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
});
```

---

## Security Headers (Helmet)

```typescript
// apps/api/src/main.ts
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:'],
    },
  },
  hsts: { maxAge: 31536000, includeSubDomains: true },
}));
```

---

## Rate Limiting

```typescript
// apps/api/src/app.module.ts
import { ThrottlerModule } from '@nestjs/throttler';

@Module({
  imports: [
    ThrottlerModule.forRoot({
      ttl: 60,      // 60 seconds window
      limit: 100,   // 100 requests per window
    }),
  ],
})
export class AppModule {}

// Usage on sensitive endpoints
@UseGuards(ThrottlerGuard)
@Throttle(5, 60) // 5 requests per 60 seconds
@Post('login')
login() { ... }
```

---

## Input Validation

```typescript
// Always use DTOs with class-validator
export class LoginDto {
  @IsEmail()
  email: string;

  @IsString()
  @MinLength(8)
  password: string;
}

// Enable validation pipe globally
app.useGlobalPipes(new ValidationPipe({
  whitelist: true,       // Strip unknown properties
  forbidNonWhitelisted: true,
  transform: true,       // Auto-transform types
}));
```

---

## Secrets Management

### Local Development

```bash
# .env (gitignored)
DATABASE_URL=postgresql://...
JWT_SECRET=dev-secret-key
NEXTAUTH_SECRET=dev-nextauth-secret
```

### Production (Coolify)

1. Use Coolify Secrets management
2. Reference via `${SECRET_NAME}`
3. Never commit secrets to Git

### Environment Variables Checklist

| Variable | Where | Sensitive |
|----------|-------|-----------|
| `DATABASE_URL` | API | Yes |
| `JWT_SECRET` | API | Yes |
| `NEXTAUTH_SECRET` | Web | Yes |
| `CORS_ORIGINS` | API | No |
| `VERTEX_AI_CREDENTIALS` | API | Yes |

---

## Best Practices

| ✅ DO | ❌ DON'T |
|-------|----------|
| Validate all inputs | Trust client data |
| Use HTTPS everywhere | Expose HTTP endpoints |
| Rotate secrets regularly | Use same secret forever |
| Log auth failures | Log passwords/tokens |
| Hash passwords (bcrypt) | Store plain text |
| Use short-lived tokens | Use long-lived tokens |
