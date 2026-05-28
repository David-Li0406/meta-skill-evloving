---
name: backend-controller-pattern-integration
description: Provides NestJS Controller patterns for Integration endpoints. This skill should be used when building endpoints for external integrations like Google Sheets or Webhooks.
---

# Integration Controller Pattern (NestJS)

This skill outlines the patterns for **Integration** controllers in `erify_api`, specifically for external integrations like Google Sheets extensions.

## Core Principles

1.  **Inheritance**: Integration controllers should extend their specific base class (e.g., `BaseGoogleSheetsController`).
2.  **Authentication**: Use specific decorators for the integration type (e.g., `@GoogleSheets()`).
3.  **Response Format**: often requires specific serialization compatibility (e.g., snake_case for external tools).

## Google Sheets Pattern

**Base Controller**: `BaseGoogleSheetsController` provides:
*   `@GoogleSheets()` authentication decorator.
*   `createPaginatedResponse()` for standard pagination.

**Implementation**:

```typescript
import { Controller, Get, Query } from '@nestjs/common';
import { BaseGoogleSheetsController } from '../base-google-sheets.controller';
import { ApiZodResponse } from '@/lib/openapi/decorators';
import { ZodSerializerDto } from 'nestjs-zod';

@Controller('google-sheets/schedules')
export class GoogleSheetsScheduleController extends BaseGoogleSheetsController {
  
  // Note: Google Sheets often uses explicit @ApiZodResponse + @ZodSerializerDto 
  // instead of a wrapper if specific description tuning is needed.
  @Get()
  @ApiZodResponse(createPaginatedResponseSchema(scheduleDto))
  @ZodSerializerDto(createPaginatedResponseSchema(scheduleDto))
  async getSchedules(@Query() query: ListSchedulesQueryDto) {
    const { schedules, total } = await this.scheduleService.getPaginatedSchedules(query);
    return this.createPaginatedResponse(schedules, total, query);
  }
}
```

## Checklist

- [ ] Controller extends appropriate base (e.g., `BaseGoogleSheetsController`).
- [ ] Uses specific auth decorator (e.g., `@GoogleSheets`).
- [ ] Uses `@ZodSerializerDto` for strict output serialization.
