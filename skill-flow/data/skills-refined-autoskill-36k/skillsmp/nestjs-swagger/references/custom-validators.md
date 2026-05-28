# Custom Validators

이 프로젝트의 커스텀 밸리데이터와 Swagger 연동 방법입니다.

## 사용 가능한 커스텀 밸리데이터

| 밸리데이터 | 위치 | 용도 |
|-----------|------|------|
| `@IsPositiveInteger()` | `@/common/validators` | 양의 정수 (1 이상) |
| `@IsSimilarityRange()` | `@/common/validators` | 유사도 범위 (0~1) |

## @IsPositiveInteger() 사용법

**기능**: 문자열을 정수로 변환 후 1 이상인지 검증

```typescript
import { IsPositiveInteger } from '@/common/validators'

export class QueryDto {
  @ApiProperty({
    description: '페이지 번호',
    example: 1,
    minimum: 1,  // Swagger에 최소값 표시
  })
  @IsPositiveInteger()
  page: number = 1

  @ApiProperty({
    description: '페이지당 항목 수',
    example: 20,
    minimum: 1,
    default: 20,
  })
  @IsPositiveInteger()
  limit: number = 20
}
```

## @IsSimilarityRange() 사용법

**기능**: 문자열을 실수로 변환 후 0~1 범위인지 검증

```typescript
import { IsSimilarityRange } from '@/common/validators'

export class AnalysisRequestDto {
  @ApiPropertyOptional({
    description: '최소 유사도 필터 (0~1)',
    example: 0.8,
    minimum: 0,
    maximum: 1,
  })
  @IsOptional()
  @IsSimilarityRange()
  minSimilarity?: number
}
```

## 새 커스텀 밸리데이터 생성 패턴

```typescript
// src/common/validators/is-custom.validator.ts
import { applyDecorators } from '@nestjs/common'
import { Transform } from 'class-transformer'
import { IsNumber, Min, Max } from 'class-validator'

/**
 * 커스텀 밸리데이터 예시
 * - 문자열을 숫자로 변환
 * - 특정 범위 검증
 */
export function IsCustomRange(min: number, max: number) {
  return applyDecorators(
    Transform(({ value }) => parseFloat(value)),
    IsNumber({}, { message: '숫자여야 합니다' }),
    Min(min, { message: `${min} 이상이어야 합니다` }),
    Max(max, { message: `${max} 이하여야 합니다` }),
  )
}
```

## index.ts에 export 추가

```typescript
// src/common/validators/index.ts
export * from './is-positive-integer.validator'
export * from './is-similarity-range.validator'
export * from './is-custom.validator'  // 새 밸리데이터 추가
```
