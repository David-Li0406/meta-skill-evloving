---
name: Backend Architecture (NestJS)
description: NestJS 10 modular architecture, services, DTOs, guards, and API patterns.
---

# Backend Architecture (NestJS)

## Context

- **Framework**: NestJS 10
- **Location**: `apps/api/`
- **Port**: 3001 (dev), 3001 (prod via Coolify)
- **Architecture**: Modular monolith with strict separation

---

## Directory Structure

```
apps/api/src/
├── modules/
│   ├── auth/           # Authentication & guards
│   ├── users/          # User management
│   ├── missions/       # Mission CRUD
│   ├── wall/           # Feed/Wall feature
│   └── insights/       # AI insights
├── services/
│   └── factory/        # Business logic factories
│       ├── DigitalSoulService.ts
│       └── VertexOracle.ts
├── common/
│   ├── decorators/
│   ├── guards/
│   ├── interceptors/
│   └── pipes/
└── main.ts
```

---

## Core Principles

1. **Dependency Injection**: All services are injectable. No global state.
2. **Factory Pattern**: Complex object creation via Factories (e.g., `PdfFactory`).
3. **Saga Pattern**: Long processes orchestrated in dedicated services.
4. **DTOs Everywhere**: Validate all inputs with `class-validator`.

---

## Module Structure

```typescript
// missions/missions.module.ts
@Module({
  imports: [DatabaseModule],
  controllers: [MissionsController],
  providers: [MissionsService],
  exports: [MissionsService],
})
export class MissionsModule {}
```

---

## Service Pattern

```typescript
@Injectable()
export class MissionsService {
  constructor(private readonly prisma: PrismaService) {}

  async findAll(filters: MissionFiltersDto): Promise<Mission[]> {
    return this.prisma.mission.findMany({
      where: this.buildWhereClause(filters),
      include: { user: true },
    });
  }
}
```

---

## DTO Validation

```typescript
// dto/create-mission.dto.ts
export class CreateMissionDto {
  @IsString()
  @MinLength(10)
  title: string;

  @IsEnum(MissionType)
  type: MissionType;

  @IsOptional()
  @IsDateString()
  startDate?: string;
}
```

---

## Guards

### JWT Authentication

```typescript
@UseGuards(JwtAuthGuard)
@Get('profile')
getProfile(@CurrentUser() user: User) {
  return user;
}
```

### Role-Based Access

```typescript
@Roles(Role.ADMIN, Role.EXPERT)
@UseGuards(JwtAuthGuard, RolesGuard)
@Get('admin/users')
getAllUsers() { ... }
```

---

## Key Services

### DigitalSoulService

Orchestrates AI generation workflow:

```typescript
@Injectable()
export class DigitalSoulService {
  async processOrder(orderId: string): Promise<void> {
    // 1. Fetch order
    // 2. Call VertexOracle for AI analysis
    // 3. Generate PDF via PdfFactory
    // 4. Store results in DB (transaction)
    // 5. Notify user
  }
}
```

### VertexOracle

Encapsulates Vertex AI communication:

```typescript
@Injectable()
export class VertexOracle {
  async generateReading(input: ReadingInput): Promise<ReadingOutput> {
    // Prompt engineering + API call + JSON parsing
  }
}
```

---

## Error Handling

```typescript
// Use standard NestJS exceptions
throw new NotFoundException(`Mission ${id} not found`);
throw new BadRequestException('Invalid date range');
throw new ForbiddenException('Access denied');

// Global exception filter handles formatting
```

---

## Logging

```typescript
import { Logger } from '@nestjs/common';

@Injectable()
export class MissionsService {
  private readonly logger = new Logger(MissionsService.name);

  async create(dto: CreateMissionDto) {
    this.logger.log(`Creating mission: ${dto.title}`);
    // Never use console.log
  }
}
```
