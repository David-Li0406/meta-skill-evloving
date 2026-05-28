---
name: nestjs-swagger
description: Use when documenting NestJS DTOs or Controllers with Swagger decorators. CSO keywords: @ApiProperty, @ApiOperation, DTO 문서화, swagger decorator, API docs, OpenAPI, 스웨거
---

# NestJS Swagger Documentation Skill

이 프로젝트의 Swagger/DTO 문서화 규칙을 제공합니다.

## 핵심 원칙

1. **모든 프로퍼티에 description과 example 필수**
2. **Validator 데코레이터와 Swagger 속성 일치**
3. **description은 한글, example은 실제 값**
4. **커스텀 밸리데이터 적극 활용**
5. **Enum에는 반드시 enumName 지정** (SDK 생성 품질)
6. **옵션/상태는 마크다운 테이블로 표현** (가독성)

## Quick Reference

### Request DTO 템플릿

```typescript
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger'
import { IsIn, IsOptional, IsString } from 'class-validator'

export class ExampleRequestDto {
  @ApiProperty({
    description: '필수 필드 설명',
    example: 'example_value',
  })
  @IsString()
  requiredField!: string

  @ApiPropertyOptional({
    description: '선택 필드 설명',
    example: 'optional_value',
  })
  @IsOptional()
  @IsString()
  optionalField?: string
}
```

### Response DTO 템플릿

```typescript
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger'

export class ExampleResponseDto {
  @ApiProperty({ description: 'ID', example: 1 })
  id!: number

  @ApiProperty({ description: '생성일시' })
  createdAt!: Date

  @ApiPropertyOptional({ description: '선택 응답 필드' })
  optionalField?: string
}
```

### Enum 필드 패턴 (2026 표준)

```typescript
@ApiPropertyOptional({
  description: `상태 필터

**옵션:**
| 값 | 설명 |
|---|---|
| \`ACTIVE\` | 활성 상태 |
| \`INACTIVE\` | 비활성 상태 |

**기본값:** 전체 조회`,
  enum: StatusEnum,
  enumName: 'StatusEnum',  // 필수!
  example: 'ACTIVE',
})
@IsOptional()
@IsEnum(StatusEnum)
status?: StatusEnum
```

### Controller 문서화 패턴

```typescript
@ApiTags('Resource')
@Controller('resource')
export class ExampleController {
  @Post()
  @ApiOperation({
    summary: '리소스 생성',
    description: '새로운 리소스를 생성합니다',
  })
  @ApiResponse({ status: 201, description: '생성 성공', type: ExampleResponseDto })
  @ApiResponse({ status: 400, description: '잘못된 요청' })
  async create(@Body() dto: ExampleRequestDto): Promise<ExampleResponseDto> {}
}
```

## Validator-Swagger 매핑

| Validator | Swagger 속성 | 예시 |
|-----------|-------------|------|
| `@IsIn([...OPTIONS])` | `enum: OPTIONS` | `enum: SUPPORTED_SYMBOLS` |
| `@Min(n)` | `minimum: n` | `minimum: 0` |
| `@Max(n)` | `maximum: n` | `maximum: 100` |
| `@IsOptional()` | `@ApiPropertyOptional()` | 필수 → 선택 |
| `@IsISO8601()` | ISO 8601 example | `example: '2024-01-01T00:00:00Z'` |
| `@IsPositiveInteger()` | 양의 정수 example | `example: 1` |
| `@IsSimilarityRange()` | 0~1 범위 | `minimum: 0, maximum: 1` |

## 클라이언트 친화적 문서화 체크리스트

API 소비자(프론트엔드 개발자)가 쉽게 사용할 수 있도록:

### Description 필수 포함 사항

| 항목 | 체크 | 예시 |
|------|------|------|
| 필드 목적 | ☐ | "계정 인증에 사용되는 이메일" |
| 유효성 규칙 | ☐ | "2~20자", "1 이상 100 이하" |
| 기본값 | ☐ | "미지정 시 10" |
| Enum 값 나열 | ☐ | "pending \| completed" |
| 관계 정보 | ☐ | "GET /categories에서 조회" |

### @ApiQuery/@ApiParam 체크리스트

| 항목 | 체크 |
|------|------|
| 모든 @Query() 파라미터에 @ApiQuery 추가 | ☐ |
| 모든 @Param() 파라미터에 @ApiParam 추가 | ☐ |
| enum 값은 description에도 나열 | ☐ |
| 범위 제한은 minimum/maximum 명시 | ☐ |
| 기본값은 description과 default 모두 명시 | ☐ |

### SDK 생성 최적화

| 항목 | 체크 |
|------|------|
| enum 필드에 `enumName` 지정 | ☐ |
| 배열 타입에 `type: [ItemDto]` 명시 | ☐ |
| nullable 필드에 `nullable: true` 명시 | ☐ |

## 상세 가이드

- **Description 작성법**: [references/description-guide.md](references/description-guide.md)
- **SDK 최적화**: [references/sdk-optimization-guide.md](references/sdk-optimization-guide.md)
- DTO 템플릿: [references/dto-templates.md](references/dto-templates.md)
- Controller 패턴: [references/controller-patterns.md](references/controller-patterns.md)
- 커스텀 밸리데이터: [references/custom-validators.md](references/custom-validators.md)
