# Description 작성 베스트 프랙티스

> 클라이언트 개발자를 위한 API 문서화 가이드

## 왜 상세한 Description이 중요한가

### SDK 자동 생성 품질

OpenAPI 스펙의 description은 클라이언트 SDK 생성 시 **코드 주석**으로 변환됩니다:

```typescript
// 자동 생성된 SDK 코드
interface FindPersonaRequest {
  /**
   * 조회 시간 범위
   *
   * **옵션:**
   * | 값 | 설명 |
   * |---|---|
   * | `WEEKLY` | 주간 - 최근 7일간 인기 페르소나 |
   * | `MONTHLY` | 월간 - 최근 30일간 인기 페르소나 |
   * | `RECENTLY` | 최신 - 최근 업데이트된 페르소나 |
   *
   * **기본값:** `RECENTLY`
   */
  timeRange?: TimeRangeEnum;
}
```

### 개발자 경험(DX) 향상

| 측면 | 효과 |
|------|------|
| **온보딩 시간 단축** | 명확한 문서로 학습 곡선 감소 |
| **오류 감소** | 잘못된 값 전달 방지 |
| **지원 부담 감소** | 자주 묻는 질문이 문서에 답변됨 |
| **IDE 지원** | 자동완성 시 설명 표시 |

---

## Description 작성 4원칙

### 1. Why-first: 사용 목적부터 설명

```typescript
// ❌ Bad - What만 설명
@ApiPropertyOptional({ description: '국가 코드' })

// ✅ Good - Why + What
@ApiPropertyOptional({
  description: `사용자 국가 코드 (ISO 3166-1 alpha-2)

**사용 목적:**
사용자의 현재 국가를 지정합니다. 콘텐츠 필터링 및 번역 매칭에 사용됩니다.`
})
```

### 2. 모든 옵션을 마크다운 테이블로 명시

```typescript
@ApiPropertyOptional({
  description: `콘텐츠 국가 노출 설정

**옵션:**
| 값 | 설명 |
|---|---|
| \`ALL_COUNTRIES\` | 모든 국가의 콘텐츠를 표시합니다 |
| \`CURRENT_COUNTRY\` | 현재 국가의 콘텐츠만 표시합니다 |

**기본값:** \`ALL_COUNTRIES\``,
  enum: ContentCountrySettingEnum,
  enumName: 'ContentCountrySettingEnum',
})
```

### 3. 기본값 반드시 명시

```typescript
// ❌ Bad - 기본값 불명확
@ApiPropertyOptional({ description: '시간 범위' })

// ✅ Good - 기본값 명시
@ApiPropertyOptional({
  description: `조회 시간 범위

**옵션:**
| 값 | 설명 |
|---|---|
| \`WEEKLY\` | 주간 - 최근 7일간 인기 데이터 |
| \`MONTHLY\` | 월간 - 최근 30일간 인기 데이터 |
| \`RECENTLY\` | 최신 - 최근 업데이트된 데이터 |

**기본값:** \`RECENTLY\``,
  example: 'RECENTLY',
  default: 'RECENTLY',
})
```

### 4. 예시값은 실제 사용 시나리오 반영

```typescript
@ApiPropertyOptional({
  description: `성별 필터 (쉼표로 구분)

**사용 예시:**
- \`남자\` - 남성만
- \`남자,여자\` - 남성과 여성
- \`남자,여자,기타\` - 모든 성별 (기본값)`,
  example: '남자,여자,기타',
})
```

---

## 타입별 Description 템플릿

### Enum 필드 (필수 패턴)

```typescript
@ApiPropertyOptional({
  description: `조회 시간 범위

**옵션:**
| 값 | 설명 |
|---|---|
| \`WEEKLY\` | 주간 - 최근 7일간 인기 데이터 |
| \`MONTHLY\` | 월간 - 최근 30일간 인기 데이터 |
| \`RECENTLY\` | 최신 - 최근 업데이트된 데이터 |

**기본값:** \`RECENTLY\``,
  enum: TimeRangeEnum,
  enumName: 'TimeRangeEnum',  // SDK 생성 시 재사용 가능
  example: 'RECENTLY',
})
```

**중요:** `enumName`을 반드시 지정해야 SDK 생성기가 재사용 가능한 enum 타입을 생성합니다.

### Boolean 필드

```typescript
@ApiPropertyOptional({
  description: `성인 콘텐츠 필터

**옵션:**
| 값 | 설명 |
|---|---|
| \`true\` | 성인 콘텐츠 포함 |
| \`false\` | 성인 콘텐츠 제외 |

**기본값:** 사용자 설정에 따름`,
  type: 'boolean',
  example: false,
})
```

### ID 목록 (쉼표 구분 문자열)

```typescript
@ApiPropertyOptional({
  description: `페르소나 ID 목록 (쉼표로 구분)

**사용 목적:**
특정 페르소나들만 조회할 때 사용합니다.

**형식:** 숫자를 쉼표로 구분 (공백 없이)

**사용 예시:**
- \`12\` - 단일 페르소나
- \`12,15,59\` - 여러 페르소나`,
  example: '12,15,59',
})
```

### 국가/언어 코드

```typescript
@ApiPropertyOptional({
  description: `사용자 국가 코드 (ISO 3166-1 alpha-2)

**사용 목적:**
사용자의 현재 국가를 지정합니다. 콘텐츠 필터링 및 번역 매칭에 사용됩니다.

**지원 국가:**
| 코드 | 국가 |
|---|---|
| \`KR\` | 한국 |
| \`US\` | 미국 |
| \`JP\` | 일본 |
| \`TW\` | 대만 |
| \`TH\` | 태국 |
| \`CN\` | 중국 |`,
  example: 'KR',
  enum: ALLOWED_COUNTRY_CODES,
  enumName: 'AllowedCountryCode',
})
```

### 정렬 필드

```typescript
@ApiPropertyOptional({
  description: `정렬 기준 필드

**사용 목적:**
목록의 정렬 기준을 설정합니다.

**지원 필드:**
| 필드 | 설명 |
|---|---|
| \`numLikes\` | 좋아요 수 |
| \`numReviews\` | 리뷰 수 |
| \`createdAt\` | 생성일 |

**정렬 방향:**
- 오름차순: 필드명만 (예: \`numLikes\`)
- 내림차순: 필드명 앞에 \`-\` (예: \`-numLikes\`)

**사용 예시:**
- \`-numLikes\` - 좋아요 많은 순
- \`numLikes,-numReviews\` - 좋아요 적은 순 → 리뷰 많은 순`,
  example: '-numLikes',
})
```

### 숫자 범위 (Number)

```typescript
@ApiPropertyOptional({
  description: `검색 결과 개수

**사용 목적:**
한 페이지에 표시할 항목 개수를 지정합니다.

**유효 범위:** 1~100

**기본값:** \`10\``,
  minimum: 1,
  maximum: 100,
  default: 10,
  example: 10,
})
```

### 날짜/시간 (ISO 8601)

```typescript
@ApiPropertyOptional({
  description: `조회 기준 시점 (UTC ISO 8601 형식)

**사용 목적:**
특정 시점의 데이터를 조회할 때 사용합니다.

**형식:** \`YYYY-MM-DDTHH:mm:ssZ\`

**기본값:** 현재 시점`,
  format: 'date-time',
  example: '2025-01-21T00:00:00Z',
})
```

### 참조 ID (Reference)

```typescript
@ApiPropertyOptional({
  description: `카테고리 ID

**사용 목적:**
특정 카테고리로 필터링할 때 사용합니다.

**조회 방법:** GET /categories 엔드포인트에서 카테고리 목록 조회 가능`,
  example: 'cat_tech_001',
})
```

---

## 좋은 예시 vs 나쁜 예시

### ❌ Bad Example

```typescript
@ApiPropertyOptional({ description: '공개 여부', example: true })
isVisible?: boolean

@ApiPropertyOptional({ example: '1', description: '유저 ID' })
userId?: string

@ApiPropertyOptional({ example: '1, 2', description: '태그 ID 목록' })
tagIds?: string
```

**문제점:**
- 왜 이 필드를 사용하는지 불명확
- 어떤 값이 유효한지 불명확
- 기본값 불명확
- 형식 요구사항 불명확

### ✅ Good Example

```typescript
@ApiPropertyOptional({
  description: `공개 여부 필터

**사용 목적:**
콘텐츠의 공개 상태로 필터링합니다.

**옵션:**
| 값 | 설명 |
|---|---|
| \`true\` | 공개된 콘텐츠만 조회 |
| \`false\` | 비공개 콘텐츠만 조회 |
| 미입력 | 전체 조회 (기본값) |

**참고:** 일반 사용자는 공개 콘텐츠만 조회 가능합니다.`,
  type: 'boolean',
  example: true,
})
isVisible?: boolean

@ApiPropertyOptional({
  description: `사용자 ID

**사용 목적:**
특정 사용자의 콘텐츠만 조회할 때 사용합니다.

**형식:** 숫자 문자열`,
  example: '123',
})
userId?: string

@ApiPropertyOptional({
  description: `태그 ID 목록 (쉼표로 구분)

**사용 목적:**
특정 태그들로 필터링할 때 사용합니다.

**형식:** 숫자를 쉼표로 구분 (공백 없이)

**사용 예시:**
- \`1\` - 단일 태그
- \`1,2,5\` - 여러 태그 (OR 조건)`,
  example: '1,2,5',
})
tagIds?: string
```

---

## 마크다운 활용

Swagger UI와 대부분의 SDK 생성기는 마크다운을 지원합니다.

### 지원되는 마크다운 문법

| 문법 | 용도 |
|------|------|
| `**bold**` | 섹션 제목 강조 |
| `` `code` `` | 값, 필드명 강조 |
| `\|테이블\|` | 옵션 나열 |
| `- 항목` | 사용 예시 나열 |

### 표준 Description 템플릿

```typescript
description: `[필드 한 줄 요약]

**사용 목적:**
[왜 이 필드가 필요한지 1-2문장]

**옵션:**
| 값 | 설명 |
|---|---|
| \`VALUE1\` | 설명1 |
| \`VALUE2\` | 설명2 |

**기본값:** \`DEFAULT_VALUE\`

**사용 예시:**
- \`value1\` - 상황1
- \`value2\` - 상황2`
```

**섹션별 사용 가이드:**

| 섹션 | 필수 여부 | 언제 사용 |
|------|----------|----------|
| **사용 목적:** | 권장 | 필드의 역할이 명확하지 않을 때 |
| **옵션:** | 필수 | enum, boolean 등 제한된 값 목록이 있을 때 |
| **기본값:** | 필수 | Optional 필드일 때 |
| **사용 예시:** | 권장 | 복합 값 (쉼표 구분, 정렬 등) |
| **형식:** | 권장 | 문자열 패턴이 있을 때 (ISO 코드, 날짜 등) |
| **유효 범위:** | 필수 | 숫자 제약이 있을 때 |
| **조회 방법:** | 권장 | 참조 ID일 때 |

---

## 체크리스트

DTO 작성 시 각 필드에 대해 확인:

- [ ] **사용 목적**이 설명되어 있는가?
- [ ] **모든 유효한 값**이 마크다운 테이블로 나열되어 있는가?
- [ ] **기본값**이 명시되어 있는가?
- [ ] **예시값**이 실제 사용 시나리오를 반영하는가?
- [ ] **형식 요구사항**이 설명되어 있는가? (쉼표 구분, ISO 코드 등)
- [ ] **제약사항**이 설명되어 있는가? (권한, 최대값 등)
- [ ] `enum`, `enumName`이 모두 설정되어 있는가? (enum 타입의 경우)
- [ ] Validator 데코레이터와 일치하는가? (`@Min/@Max`, `@IsIn` 등)

---

## 안티패턴 (피해야 할 것)

### ❌ 타입/필드명만 반복

```typescript
@ApiProperty({ description: '이메일' })
email: string
```

**왜 나쁜가:** 필드명과 동일한 정보만 반복. 아무런 가치도 제공하지 않음.

### ❌ 옵션을 인라인 텍스트로 나열

```typescript
// BAD - 가독성 떨어짐
@ApiProperty({ description: '상태. pending, completed, cancelled 중 하나' })
```

**왜 나쁜가:** 각 옵션의 의미를 파악하기 어려움. SDK 생성기가 파싱하기 어려움.

### ❌ enum 값을 description에서 누락

```typescript
// BAD - enum 값이 뭔지 알 수 없음
@ApiProperty({ description: '상태', enum: Status })
```

**왜 나쁜가:** SDK 주석에 enum 값이 나타나지 않아 개발자가 별도로 코드를 확인해야 함.

### ❌ 기본값 미설명

```typescript
// BAD - 기본값이 있지만 description에 없음
@ApiPropertyOptional({ description: '페이지 크기' })
limit?: number = 10
```

**왜 나쁜가:** 클라이언트 개발자가 이 값을 생략했을 때 무슨 일이 일어나는지 알 수 없음.

### ❌ enumName 누락

```typescript
// BAD - SDK에서 string 타입으로 생성됨
@ApiProperty({ enum: ['ACTIVE', 'INACTIVE'] })
status: string
```

**왜 나쁜가:** SDK 생성 시 타입 안전성이 떨어짐. 재사용 가능한 enum 타입이 생성되지 않음.

### ❌ 형식 요구사항 미설명

```typescript
// BAD - 쉼표 구분인지, 배열인지 불명확
@ApiProperty({ description: 'ID 목록' })
ids: string
```

**왜 나쁜가:** 클라이언트 개발자가 `"1,2,3"` vs `["1","2","3"]` 중 어떤 형식으로 보내야 할지 모름.

---

## 고급 패턴

### 동적 설명 (환경별 차이)

```typescript
@ApiPropertyOptional({
  description: `API 키

**사용 목적:**
외부 서비스 연동 시 인증에 사용됩니다.

**환경별 키 발급:**
| 환경 | 발급 방법 |
|------|----------|
| 개발 | 개발자 콘솔에서 자동 발급 |
| 프로덕션 | 관리자 승인 필요 |

**보안 주의:** 클라이언트에 노출되지 않도록 서버에서만 사용하세요.`,
  example: 'sk_test_...',
})
```

### 복합 제약 조건

```typescript
@ApiPropertyOptional({
  description: `검색 키워드

**사용 목적:**
콘텐츠를 키워드로 검색할 때 사용합니다.

**제약 조건:**
- 최소 2자 이상
- 최대 50자 이하
- 특수문자 허용 안 함 (공백, 하이픈은 허용)

**검색 방식:** 부분 일치 (LIKE '%keyword%')`,
  minLength: 2,
  maxLength: 50,
  pattern: '^[a-zA-Z0-9가-힣\\s-]+$',
  example: '아이언맨',
})
```

### 버전별 차이점 명시

```typescript
@ApiPropertyOptional({
  description: `콘텐츠 필터 설정

**V3 변경사항:**
이 필드는 V2의 \`contentLanguageCodes\`를 대체합니다.

**V2와의 차이:**
| 버전 | 필드 | 동작 |
|------|------|------|
| V2 | \`contentLanguageCodes\` | 언어 코드 직접 지정 |
| V3 | \`contentCountrySetting\` | 사용자 설정 자동 적용 |

**마이그레이션:**
- V2 \`contentLanguageCodes: ['ko', 'en']\` → V3 생략 (자동 적용)`,
  enum: ContentCountrySettingEnum,
  enumName: 'ContentCountrySettingEnum',
})
```

---

## 추가 자료

- [SDK 자동 생성 최적화 가이드](./sdk-optimization-guide.md)
- [DTO 템플릿 모음](./dto-templates.md)
- [Controller 패턴 가이드](./controller-patterns.md)
