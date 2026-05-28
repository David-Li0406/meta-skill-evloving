# NestJS Security Reference

## Authentication

### JWT Setup

```bash
bun add @nestjs/passport passport passport-jwt @nestjs/jwt
bun add -D @types/passport-jwt
```

```typescript
// auth.module.ts
@Module({
  imports: [
    PassportModule.register({ defaultStrategy: 'jwt' }),
    JwtModule.registerAsync({
      imports: [ConfigModule],
      useFactory: (config: ConfigService) => ({
        secret: config.getOrThrow('JWT_SECRET'),
        signOptions: {
          expiresIn: config.get('JWT_EXPIRES_IN', '15m'),
        },
      }),
      inject: [ConfigService],
    }),
    UserModule,
  ],
  providers: [AuthService, JwtStrategy, LocalStrategy],
  controllers: [AuthController],
  exports: [AuthService],
})
export class AuthModule {}
```

### JWT Strategy

```typescript
// jwt.strategy.ts
@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy, 'jwt') {
  constructor(
    private readonly configService: ConfigService,
    private readonly userService: UserService,
  ) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: configService.getOrThrow('JWT_SECRET'),
    });
  }

  async validate(payload: JwtPayload): Promise<AuthUser> {
    // Optional: Check if user still exists and is active
    const user = await this.userService.findById(payload.sub);
    if (!user || !user.isActive) {
      throw new UnauthorizedException('User not found or inactive');
    }

    return {
      id: payload.sub,
      email: payload.email,
      roles: payload.roles,
    };
  }
}
```

### Local Strategy (Username/Password)

```typescript
// local.strategy.ts
@Injectable()
export class LocalStrategy extends PassportStrategy(Strategy, 'local') {
  constructor(private readonly authService: AuthService) {
    super({
      usernameField: 'email',
      passwordField: 'password',
    });
  }

  async validate(email: string, password: string): Promise<AuthUser> {
    const user = await this.authService.validateUser(email, password);
    if (!user) {
      throw new UnauthorizedException('Invalid credentials');
    }
    return user;
  }
}
```

### Auth Service

```typescript
// auth.service.ts
@Injectable()
export class AuthService {
  constructor(
    private readonly userService: UserService,
    private readonly jwtService: JwtService,
    private readonly configService: ConfigService,
  ) {}

  async validateUser(email: string, password: string): Promise<AuthUser | null> {
    const user = await this.userService.findByEmail(email);
    if (!user || !user.isActive) return null;

    const isValid = await bcrypt.compare(password, user.passwordHash);
    if (!isValid) return null;

    return {
      id: user.id,
      email: user.email,
      roles: user.roles,
    };
  }

  async login(user: AuthUser): Promise<TokenResponse> {
    const payload: JwtPayload = {
      sub: user.id,
      email: user.email,
      roles: user.roles,
    };

    const [accessToken, refreshToken] = await Promise.all([
      this.jwtService.signAsync(payload),
      this.jwtService.signAsync(
        { sub: user.id, type: 'refresh' },
        { expiresIn: this.configService.get('JWT_REFRESH_EXPIRES_IN', '7d') },
      ),
    ]);

    return { accessToken, refreshToken };
  }

  async refreshTokens(refreshToken: string): Promise<TokenResponse> {
    try {
      const payload = await this.jwtService.verifyAsync(refreshToken);
      if (payload.type !== 'refresh') {
        throw new UnauthorizedException('Invalid token type');
      }

      const user = await this.userService.findById(payload.sub);
      if (!user || !user.isActive) {
        throw new UnauthorizedException('User not found');
      }

      return this.login({
        id: user.id,
        email: user.email,
        roles: user.roles,
      });
    } catch {
      throw new UnauthorizedException('Invalid refresh token');
    }
  }
}
```

## Guards

### JWT Auth Guard

```typescript
// jwt-auth.guard.ts
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  constructor(private reflector: Reflector) {
    super();
  }

  canActivate(context: ExecutionContext) {
    // Check for @Public() decorator
    const isPublic = this.reflector.getAllAndOverride<boolean>(IS_PUBLIC_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);

    if (isPublic) return true;

    return super.canActivate(context);
  }

  handleRequest(err: any, user: any, info: any) {
    if (err || !user) {
      throw err || new UnauthorizedException(info?.message || 'Unauthorized');
    }
    return user;
  }
}

// Public decorator
export const IS_PUBLIC_KEY = 'isPublic';
export const Public = () => SetMetadata(IS_PUBLIC_KEY, true);
```

### Roles Guard

```typescript
// roles.guard.ts
export enum Role {
  USER = 'user',
  ADMIN = 'admin',
  SUPER_ADMIN = 'super_admin',
}

export const ROLES_KEY = 'roles';
export const Roles = (...roles: Role[]) => SetMetadata(ROLES_KEY, roles);

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<Role[]>(ROLES_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);

    if (!requiredRoles || requiredRoles.length === 0) {
      return true;
    }

    const { user } = context.switchToHttp().getRequest();
    if (!user?.roles) {
      return false;
    }

    return requiredRoles.some((role) => user.roles.includes(role));
  }
}

// Usage
@Controller('admin')
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles(Role.ADMIN)
export class AdminController {}
```

### Resource Owner Guard

```typescript
// owner.guard.ts
@Injectable()
export class OwnerGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const user = request.user as AuthUser;
    const resourceId = request.params.id;

    // Admins can access any resource
    if (user.roles?.includes(Role.ADMIN)) {
      return true;
    }

    // Check ownership (implement per resource)
    const ownerField = this.reflector.get<string>('ownerField', context.getHandler()) || 'userId';
    const resource = request[this.reflector.get<string>('resourceKey', context.getHandler())];

    if (resource && resource[ownerField] !== user.id) {
      throw new ForbiddenException('You do not own this resource');
    }

    return true;
  }
}
```

## Validation

### Global Validation Pipe

```typescript
// main.ts
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,              // Strip non-decorated properties
    forbidNonWhitelisted: true,   // Throw on extra properties
    transform: true,              // Auto-transform to DTO types
    transformOptions: {
      enableImplicitConversion: true,
    },
    exceptionFactory: (errors) => {
      const messages = errors.map((error) => ({
        field: error.property,
        constraints: Object.values(error.constraints || {}),
      }));
      return new BadRequestException({ message: 'Validation failed', errors: messages });
    },
  }),
);
```

### DTO Examples

```typescript
// create-user.dto.ts
export class CreateUserDto {
  @IsEmail()
  @Transform(({ value }) => value?.toLowerCase().trim())
  email: string;

  @IsString()
  @MinLength(8)
  @MaxLength(100)
  @Matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/, {
    message: 'Password must contain uppercase, lowercase, number, and special character',
  })
  password: string;

  @IsOptional()
  @IsString()
  @MaxLength(100)
  @Transform(({ value }) => value?.trim())
  name?: string;

  @IsOptional()
  @IsUrl()
  avatarUrl?: string;
}

// Pagination DTO
export class PaginationDto {
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  page?: number = 1;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(100)
  limit?: number = 20;

  @IsOptional()
  @IsString()
  search?: string;
}
```

## Rate Limiting

```bash
bun add @nestjs/throttler
```

```typescript
// app.module.ts
@Module({
  imports: [
    ThrottlerModule.forRoot([
      {
        name: 'short',
        ttl: 1000,      // 1 second
        limit: 3,       // 3 requests
      },
      {
        name: 'medium',
        ttl: 10000,     // 10 seconds
        limit: 20,      // 20 requests
      },
      {
        name: 'long',
        ttl: 60000,     // 1 minute
        limit: 100,     // 100 requests
      },
    ]),
  ],
  providers: [
    {
      provide: APP_GUARD,
      useClass: ThrottlerGuard,
    },
  ],
})
export class AppModule {}

// Custom throttle per endpoint
@Controller('auth')
export class AuthController {
  @Post('login')
  @Throttle({ short: { limit: 5, ttl: 60000 } }) // 5 attempts per minute
  async login(@Body() dto: LoginDto) {}

  @Post('register')
  @Throttle({ short: { limit: 3, ttl: 60000 } }) // 3 per minute
  async register(@Body() dto: CreateUserDto) {}
}

// Skip throttling
@SkipThrottle()
@Get('health')
async health() {}
```

## Security Headers (Helmet)

```bash
bun add helmet
```

```typescript
// main.ts
import helmet from 'helmet';

app.use(helmet());

// Custom CSP
app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", 'data:', 'https:'],
        scriptSrc: ["'self'"],
      },
    },
    crossOriginEmbedderPolicy: false, // For serving images
  }),
);
```

## CORS Configuration

```typescript
// main.ts
app.enableCors({
  origin: (origin, callback) => {
    const allowedOrigins = process.env.ALLOWED_ORIGINS?.split(',') || [];
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
  maxAge: 86400, // 24 hours
});
```

## Password Hashing

```typescript
// auth.service.ts
import * as bcrypt from 'bcrypt';

const SALT_ROUNDS = 12;

async hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, SALT_ROUNDS);
}

async verifyPassword(password: string, hash: string): Promise<boolean> {
  return bcrypt.compare(password, hash);
}
```

## Security Checklist

- [ ] Use HTTPS in production
- [ ] Implement rate limiting on auth endpoints
- [ ] Hash passwords with bcrypt (cost 12+)
- [ ] Use parameterized queries (Drizzle does this automatically)
- [ ] Validate all input with class-validator
- [ ] Use whitelist: true in ValidationPipe
- [ ] Implement proper CORS configuration
- [ ] Add security headers with helmet
- [ ] Use short-lived access tokens (15min)
- [ ] Implement refresh token rotation
- [ ] Log authentication failures
- [ ] Implement account lockout after failed attempts
- [ ] Sanitize error messages (don't expose internals)
- [ ] Use environment variables for secrets
- [ ] Audit sensitive operations
