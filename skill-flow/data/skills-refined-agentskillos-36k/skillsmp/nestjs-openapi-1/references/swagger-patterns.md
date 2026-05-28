# NestJS Swagger/OpenAPI Patterns

## Setup

```typescript
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  const config = new DocumentBuilder()
    .setTitle('API Documentation')
    .setDescription('REST API endpoints')
    .setVersion('1.0')
    .addBearerAuth()
    .addTag('users')
    .addTag('orders')
    .build();

  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs', app, document);

  await app.listen(3000);
}
```

## DTO Documentation

```typescript
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class CreateUserDto {
  @ApiProperty({
    description: 'User email address',
    example: 'user@example.com',
  })
  email: string;

  @ApiProperty({
    description: 'User password',
    minLength: 8,
  })
  password: string;

  @ApiPropertyOptional({
    description: 'User display name',
    example: 'John Doe',
  })
  name?: string;

  @ApiProperty({
    enum: ['admin', 'user', 'guest'],
    default: 'user',
  })
  role: string;
}
```

## Controller Documentation

```typescript
import {
  ApiTags,
  ApiOperation,
  ApiResponse,
  ApiBearerAuth,
  ApiParam,
  ApiQuery,
} from '@nestjs/swagger';

@ApiTags('users')
@Controller('users')
export class UsersController {
  @Get()
  @ApiOperation({ summary: 'Get all users' })
  @ApiQuery({ name: 'page', required: false, type: Number })
  @ApiQuery({ name: 'limit', required: false, type: Number })
  @ApiResponse({ status: 200, description: 'List of users', type: [User] })
  findAll(@Query() query: PaginationDto) {
    return this.usersService.findAll(query);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get user by ID' })
  @ApiParam({ name: 'id', description: 'User ID' })
  @ApiResponse({ status: 200, description: 'User found', type: User })
  @ApiResponse({ status: 404, description: 'User not found' })
  findOne(@Param('id') id: string) {
    return this.usersService.findOne(id);
  }

  @Post()
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Create new user' })
  @ApiResponse({ status: 201, description: 'User created', type: User })
  @ApiResponse({ status: 400, description: 'Validation error' })
  create(@Body() dto: CreateUserDto) {
    return this.usersService.create(dto);
  }
}
```

## Response Schema

```typescript
import { ApiProperty } from '@nestjs/swagger';

export class PaginatedResponse<T> {
  @ApiProperty()
  data: T[];

  @ApiProperty({ example: 100 })
  total: number;

  @ApiProperty({ example: 1 })
  page: number;

  @ApiProperty({ example: 10 })
  limit: number;
}

// Usage in controller
@ApiResponse({
  status: 200,
  schema: {
    allOf: [
      { $ref: getSchemaPath(PaginatedResponse) },
      {
        properties: {
          data: {
            type: 'array',
            items: { $ref: getSchemaPath(User) },
          },
        },
      },
    ],
  },
})
```
