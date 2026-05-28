# NestJS Exception Filters

## Built-in Exceptions

```typescript
import {
  BadRequestException,
  UnauthorizedException,
  ForbiddenException,
  NotFoundException,
  ConflictException,
  InternalServerErrorException,
} from '@nestjs/common';

// Usage
throw new NotFoundException('User not found');
throw new BadRequestException('Invalid input');
throw new UnauthorizedException('Invalid credentials');
throw new ConflictException('Email already exists');
```

## Custom Exception

```typescript
export class BusinessException extends HttpException {
  constructor(
    public readonly code: string,
    message: string,
    status: HttpStatus = HttpStatus.BAD_REQUEST,
  ) {
    super({ code, message }, status);
  }
}

// Usage
throw new BusinessException('INSUFFICIENT_FUNDS', 'Not enough balance');
```

## Global Exception Filter

```typescript
import { ExceptionFilter, Catch, ArgumentsHost, HttpException, HttpStatus } from '@nestjs/common';
import { Response } from 'express';

@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  constructor(private readonly logger: Logger) {}

  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest();

    const status = exception instanceof HttpException
      ? exception.getStatus()
      : HttpStatus.INTERNAL_SERVER_ERROR;

    const message = exception instanceof HttpException
      ? exception.getResponse()
      : 'Internal server error';

    const errorResponse = {
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      message: typeof message === 'string' ? message : (message as any).message,
    };

    this.logger.error(
      `${request.method} ${request.url}`,
      exception instanceof Error ? exception.stack : 'Unknown error',
    );

    response.status(status).json(errorResponse);
  }
}

// main.ts
app.useGlobalFilters(new AllExceptionsFilter(new Logger()));
```

## Validation Exception Filter

```typescript
@Catch(ValidationError)
export class ValidationExceptionFilter implements ExceptionFilter {
  catch(exception: ValidationError[], host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();

    const errors = exception.map(err => ({
      field: err.property,
      constraints: Object.values(err.constraints || {}),
    }));

    response.status(HttpStatus.BAD_REQUEST).json({
      statusCode: HttpStatus.BAD_REQUEST,
      message: 'Validation failed',
      errors,
    });
  }
}
```

## HTTP Exception Filter

```typescript
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const status = exception.getStatus();
    const exceptionResponse = exception.getResponse();

    response.status(status).json({
      success: false,
      statusCode: status,
      ...(typeof exceptionResponse === 'object' ? exceptionResponse : { message: exceptionResponse }),
      timestamp: new Date().toISOString(),
    });
  }
}
```

## Using Filters

```typescript
// Controller level
@Controller('users')
@UseFilters(HttpExceptionFilter)
export class UsersController {}

// Method level
@Post()
@UseFilters(ValidationExceptionFilter)
create(@Body() dto: CreateUserDto) {}

// Global (main.ts)
app.useGlobalFilters(new AllExceptionsFilter());

// Global with DI
@Module({
  providers: [
    {
      provide: APP_FILTER,
      useClass: AllExceptionsFilter,
    },
  ],
})
export class AppModule {}
```
