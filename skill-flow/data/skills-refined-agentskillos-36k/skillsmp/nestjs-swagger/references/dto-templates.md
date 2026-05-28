# DTO Templates

## 프로젝트 명명 규칙

| 용도 | 파일명 패턴 | 예시 |
|------|------------|------|
| 요청 DTO | `*.request.dto.ts` | `analysis.request.dto.ts` |
| 응답 DTO | `*.response.dto.ts` | `analysis.response.dto.ts` |
| 쿼리 DTO | `*-query.dto.ts` | `news-query.dto.ts` |
| 생성 DTO | `create-*.dto.ts` | `create-news.dto.ts` |
| 수정 DTO | `update-*.dto.ts` | `update-user.dto.ts` |

## Enum 필드 패턴

```typescript
// 1. const 배열로 정의 (타입 추론 + 재사용)
export const SUPPORTED_SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT'] as const

// 2. DTO에서 사용
@ApiProperty({
  description: '거래 심볼',
  example: 'BTCUSDT',
  enum: SUPPORTED_SYMBOLS,  // Swagger enum 표시
})
@IsIn([...SUPPORTED_SYMBOLS], {
  message: `심볼은 ${SUPPORTED_SYMBOLS.join(', ')} 중 하나여야 합니다`,
})
symbol!: string
```

## Enum 필드 - enumName 필수

SDK 자동 생성 시 enum 타입을 재사용 가능하게 하려면 `enumName`이 필수입니다:

```typescript
// ❌ BAD - SDK에서 string으로 생성됨
@ApiProperty({ enum: ['ACTIVE', 'INACTIVE'] })
status: string

// ❌ BAD - enumName 없음
@ApiProperty({ enum: OrderStatus })
status: OrderStatus

// ✅ GOOD - SDK에서 OrderStatus 타입으로 재사용 가능
@ApiProperty({
  enum: OrderStatus,
  enumName: 'OrderStatus',  // 필수!
  description: `주문 상태

**옵션:**
| 값 | 설명 |
|---|---|
| \`PENDING\` | 대기 중 |
| \`COMPLETED\` | 완료됨 |`,
})
status: OrderStatus
```

## 기본값 패턴

```typescript
@ApiProperty({
  description: '페이지당 항목 수',
  example: 20,
  default: 20,  // Swagger에 기본값 표시
})
@IsPositiveInteger()
limit: number = 20  // TypeScript 기본값
```

## 배열 타입 패턴

```typescript
// 단순 배열
@ApiProperty({
  description: '태그 목록',
  type: [String],
  example: ['crypto', 'bitcoin'],
})
tags!: string[]

// 객체 배열
@ApiProperty({
  description: '캔들 데이터',
  type: [CandleDto],
})
candles!: CandleDto[]
```

## 중첩 객체 패턴

```typescript
// 필수 중첩 객체
@ApiProperty({
  description: '페이지네이션 메타 정보',
  type: PagePaginationMetaDto,
})
meta!: PagePaginationMetaDto

// 선택적 중첩 객체
@ApiPropertyOptional({
  description: '뉴스 미리보기',
  type: NewsPreviewDto,
  nullable: true,
})
newsPreview?: NewsPreviewDto | null
```

## 날짜 필드 패턴

```typescript
// ISO 8601 문자열 입력
@ApiPropertyOptional({
  description: '시작 시점 (UTC ISO 8601)',
  example: '2024-01-01T00:00:00Z',
})
@IsOptional()
@IsISO8601({ strict: true })
startTime?: string

// Date 객체 출력
@ApiProperty({ description: '생성일시' })
createdAt!: Date
```

## Union 타입 패턴

```typescript
@ApiPropertyOptional({
  description: '다음 페이지 커서',
  example: 80,
  nullable: true,
  oneOf: [{ type: 'string' }, { type: 'number' }],
})
nextCursor!: string | number | null
```

## Generic/Mixin 패턴 (페이지네이션)

TypeScript의 제네릭은 런타임에 지워지므로 Swagger가 인식할 수 없습니다.
Mixin 함수로 해결합니다:

```typescript
import { Type } from '@nestjs/common'
import { ApiProperty } from '@nestjs/swagger'
import { Type as TransformType } from 'class-transformer'

// 페이지네이션 메타데이터
export class PaginationMetaDto {
  @ApiProperty({ example: 1, description: '현재 페이지' })
  page!: number

  @ApiProperty({ example: 10, description: '페이지당 항목 수' })
  limit!: number

  @ApiProperty({ example: 100, description: '전체 항목 수' })
  totalItems!: number

  @ApiProperty({ example: 10, description: '전체 페이지 수' })
  totalPages!: number
}

// Mixin 함수
export function createPaginatedResponseDto<T>(classRef: Type<T>) {
  abstract class PaginatedResponseDto {
    @ApiProperty({
      type: [classRef],
      description: '데이터 목록'
    })
    @TransformType(() => classRef)
    data!: T[]

    @ApiProperty({
      type: PaginationMetaDto,
      description: '페이지네이션 메타데이터'
    })
    meta!: PaginationMetaDto
  }

  Object.defineProperty(PaginatedResponseDto, 'name', {
    value: `Paginated${classRef.name}ResponseDto`
  })

  return PaginatedResponseDto
}

// 사용
export class PaginatedUserResponseDto extends createPaginatedResponseDto(UserDto) {}
```

## Union 타입 (discriminator)

다형성 타입 처리:

```typescript
import { ApiExtraModels, ApiProperty, getSchemaPath } from '@nestjs/swagger'

export class CatDto {
  @ApiProperty({ example: 'cat' })
  type!: 'cat'

  @ApiProperty({ example: 'meow' })
  sound!: string
}

export class DogDto {
  @ApiProperty({ example: 'dog' })
  type!: 'dog'

  @ApiProperty({ example: 'bark' })
  sound!: string
}

@ApiExtraModels(CatDto, DogDto)
export class PetResponseDto {
  @ApiProperty({
    oneOf: [
      { $ref: getSchemaPath(CatDto) },
      { $ref: getSchemaPath(DogDto) }
    ],
    discriminator: {
      propertyName: 'type',
      mapping: {
        cat: getSchemaPath(CatDto),
        dog: getSchemaPath(DogDto)
      }
    }
  })
  pet!: CatDto | DogDto
}
```
