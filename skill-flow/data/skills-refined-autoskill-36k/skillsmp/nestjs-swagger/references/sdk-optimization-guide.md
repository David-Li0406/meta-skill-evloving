# SDK 자동 생성 최적화 가이드

OpenAPI 스펙에서 고품질 클라이언트 SDK를 생성하기 위한 가이드입니다.

## 왜 SDK 최적화가 중요한가

| 최적화 전 | 최적화 후 |
|----------|----------|
| `status: string` | `status: OrderStatus` (타입 안전) |
| 주석 없음 | JSDoc 주석 자동 생성 |
| 인라인 enum | 재사용 가능한 enum 타입 |

## 핵심 최적화 항목

### 1. enumName 필수 지정

```typescript
// ❌ SDK에서 string으로 생성됨
@ApiProperty({ enum: ['ACTIVE', 'INACTIVE'] })

// ✅ SDK에서 StatusEnum 타입으로 생성됨
@ApiProperty({
  enum: StatusEnum,
  enumName: 'StatusEnum'
})
```

### 2. 배열 타입 명시

```typescript
// ❌ any[] 로 생성될 수 있음
@ApiProperty()
items: ItemDto[];

// ✅ ItemDto[] 로 정확하게 생성
@ApiProperty({ type: [ItemDto] })
items: ItemDto[];
```

### 3. nullable 명시

```typescript
// ❌ null 허용 여부 불명확
@ApiPropertyOptional()
avatar?: string;

// ✅ string | null 로 명확하게 생성
@ApiPropertyOptional({ nullable: true })
avatar?: string | null;
```

## SDK 생성 도구 추천 (2026)

| 도구 | TypeScript 품질 | React Query | 설정 용이성 |
|------|----------------|-------------|-------------|
| **Orval** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| OpenAPI Generator | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Fern | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**권장:** TypeScript 프로젝트에는 **Orval** 사용

## Orval 기본 설정

```typescript
// orval.config.ts
import { defineConfig } from 'orval';

export default defineConfig({
  api: {
    input: './openapi.yaml',
    output: {
      mode: 'tags-split',
      target: './src/api/endpoints',
      schemas: './src/api/models',
      client: 'react-query',
      mock: true,
    },
  },
});
```

## 검증 체크리스트

- [ ] 모든 enum에 `enumName` 지정
- [ ] 모든 배열에 `type: [Dto]` 명시
- [ ] nullable 필드에 `nullable: true` 명시
- [ ] 모든 description이 마크다운으로 구조화
