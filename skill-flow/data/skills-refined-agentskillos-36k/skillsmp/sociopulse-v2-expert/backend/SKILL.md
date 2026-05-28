---
name: Backend Architecture Expert
description: Expert knowledge of NestJS modular architecture, feature modules, guards, decorators, and WebSocket implementation.
---

# Backend Architecture Skill - SocioPulse V2

## Overview

The backend is built with **NestJS 10** following a strict modular architecture with 11+ feature modules.

---

## 1. Module Structure

### Core Modules (Infrastructure)

```
apps/api/src/
├── common/
│   ├── prisma/          # PrismaModule (DB access)
│   ├── mailer/          # MailModule (SMTP/Resend)
│   └── services/        # GeocodingModule
├── app.module.ts        # Root module
└── main.ts              # Bootstrap
```

### Feature Modules (Business Logic)

```
apps/api/src/
├── auth/                # JWT, register, login
├── matching-engine/     # Mission-Talent matching algorithm
├── wall-feed/           # Fil Pro feed logic
├── video-booking/       # LiveKit sessions
├── payments/            # Stripe Connect
├── contracts/           # Devis/Contrats
├── messages/            # Chat (Socket.IO)
├── mission-hub/         # Tracking (Timeline, Reports)
├── growth/              # Gamification (points, referrals)
└── notifications/       # Push notifications
```

---

## 2. Module Pattern

### Example: AuthModule

```typescript
// auth/auth.module.ts
@Module({
  imports: [PrismaModule, JwtModule.register({...})],
  controllers: [AuthController],
  providers: [AuthService, JwtStrategy],
  exports: [AuthService],
})
export class AuthModule {}

// auth/auth.controller.ts
@Controller('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}
  
  @Post('register')
  async register(@Body() dto: RegisterDto) {
    return this.authService.register(dto);
  }
  
  @UseGuards(JwtAuthGuard)
  @Get('me')
  async getProfile(@CurrentUser() user: User) {
    return user;
  }
}
```

---

## 3. Guards & Decorators

### JWT Authentication Guard

```typescript
// common/guards/jwt-auth.guard.ts
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  canActivate(context: ExecutionContext) {
    return super.canActivate(context);
  }
}

// Usage
@UseGuards(JwtAuthGuard)
@Get('profile')
getProfile(@CurrentUser() user: User) {
  return user;
}
```

### Custom  Role Guard

```typescript
// common/guards/roles.guard.ts
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}
  
  canActivate(context: ExecutionContext): boolean {
    const requiredRole = this.reflector.get<UserRole>('role', context.getHandler());
    const { user } = context.switchToHttp().getRequest();
    return user.role === requiredRole;
  }
}

// Usage with decorator
@Roles(UserRole.ADMIN)
@UseGuards(JwtAuthGuard, RolesGuard)
@Delete('users/:id')
deleteUser(@Param('id') id: string) {
  return this.adminService.deleteUser(id);
}
```

---

## 4. DTOs & Validation

### DTO Pattern

```typescript
// auth/dto/register.dto.ts
import { IsEmail, IsString, MinLength, IsEnum } from 'class-validator';

export class RegisterDto {
  @IsEmail()
  email: string;
  
  @IsString()
  @MinLength(8)
  password: string;
  
  @IsEnum(UserRole)
  role: UserRole;
}
```

### Validation Pipe (Global)

```typescript
// main.ts
app.useGlobalPipes(new ValidationPipe({
  whitelist: true,
  forbidNonWhitelisted: true,
  transform: true,
}));
```

---

## 5. Matching Engine Module

### Core Algorithm

```typescript
// matching-engine/matching-engine.service.ts
@Injectable()
export class MatchingEngineService {
  async findMatches(missionId: string): Promise<Profile[]> {
    const mission = await this.prisma.reliefMission.findUnique({
      where: { id: missionId },
    });
    
    // 1. Geo filter (Haversine distance)
    const geoFiltered = await this.geoFilter(mission);
    
    // 2. Job filter (exact jobId match)
    const jobFiltered = geoFiltered.filter(p => p.jobId === mission.jobId);
    
    // 3. Compliance check
    const compliantTalents = jobFiltered.filter(p => 
      mission.requiresDiploma ? p.complianceStatus === 'VALIDATED' : true
    );
    
    // 4. Specialty score (0-100)
    const scored = compliantTalents.map(talent => ({
      talent,
      score: this.calculateSpecialtyScore(talent, mission),
    }));
    
    // 5. Sort and return top 3
    return scored
      .sort((a, b) => b.score - a.score)
      .slice(0, 3)
      .map(s => s.talent);
  }
}
```

---

## 6. WebSocket (Socket.IO)

### Gateway Setup

```typescript
// messages/messages.gateway.ts
@WebSocketGateway({ cors: { origin: '*' } })
export class MessagesGateway {
  @WebSocketServer()
  server: Server;
  
  @SubscribeMessage('chat:send')
  async handleMessage(@MessageBody() data: SendMessageDto, @ConnectedSocket() client: Socket) {
    const message = await this.messagesService.create(data);
    
    // Broadcast to room
    this.server.to(`mission-${data.missionId}`).emit('chat:message', message);
  }
  
  @SubscribeMessage('mission:join')
  joinMissionRoom(@MessageBody() missionId: string, @ConnectedSocket() client: Socket) {
    client.join(`mission-${missionId}`);
  }
}
```

---

## 7. Stripe Integration

### Payments Module

```typescript
// payments/payments.service.ts
@Injectable()
export class PaymentsService {
  private stripe: Stripe;
  
  constructor() {
    this.stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
  }
  
  async createPaymentIntent(amount: number, customerId: string) {
    return this.stripe.paymentIntents.create({
      amount: amount * 100, // cents
      currency: 'eur',
      customer: customerId,
    });
  }
  
  @Post('webhooks')
  async handleWebhook(@Req() req: Request) {
    const sig = req.headers['stripe-signature'];
    const event = this.stripe.webhooks.constructEvent(
      req.body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET,
    );
    
    if (event.type === 'payment_intent.succeeded') {
      await this.processPaymentSuccess(event.data.object);
    }
  }
}
```

---

## 8. Error Handling

### Exception Filters

```typescript
// common/filters/http-exception.filter.ts
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const status = exception.getStatus();
    
    response.status(status).json({
      statusCode: status,
      message: exception.message,
      timestamp: new Date().toISOString(),
    });
  }
}
```

---

## 9. Rate Limiting (Throttler)

### Global Configuration

```typescript
// app.module.ts
ThrottlerModule.forRoot([
  {
    name: 'short',
    ttl: 1000,
    limit: 3,
  },
  {
    name: 'medium',
    ttl: 10000,
    limit: 20,
  },
]),

// Applied globally
providers: [
  {
    provide: APP_GUARD,
    useClass: ThrottlerGuard,
  },
]
```

---

## 10. Best Practices

### DO

✅ Follow modular architecture (one feature = one module)  
✅ Use DTOs for all inputs (validation)  
✅ Implement guards for authentication/authorization  
✅ Use decorators for cleaner code  
✅ Handle errors with exception filters

### DON'T

❌ Put business logic in controllers (use services)  
❌ Skip validation (always use DTOs)  
❌ Hardcode secrets (use ConfigModule)  
❌ Forget to handle WebSocket errors

---

*This backend architecture ensures scalability, maintainability, and security through NestJS best practices.*
