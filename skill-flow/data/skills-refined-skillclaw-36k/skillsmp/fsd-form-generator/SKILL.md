---
name: fsd-form-generator
description: Automatically generate FSD form structures when user mentions creating forms, form validation, or form components. Triggers on phrases like "generate form", "create form schema", "add form for [feature]"
---

# FSD Form Generator Skill

Automatically detects and generates complete FSD (Feature-Sliced Design) form structures following the project's CLAUDE.md guidelines.

## Trigger Phrases

This skill activates when the user says:
- "Generate a form for [domain]"
- "Create form schema for [feature]"
- "Add [domain] form component"
- "I need a form to handle [feature]"
- "Make a validation schema for [domain]"
- "[도메인] 폼 만들어줘"

## Auto-Detection Examples

✅ **User**: "Create a form for payment processing"
→ Generates: `payment-processing` form structure

✅ **User**: "I need a form schema for product filtering"
→ Generates: `product-filter` form structure

✅ **User**: "Add a user settings form with validation"
→ Generates: `user-settings` form structure

## File Structure Output

**⚠️ 중요: Admin vs Service 경로 구분**

### 관리자 전용인 경우:
```
src/
├── entities/[domain]/
│   ├── model/[domain].schema.ts
│   └── index.ts
└── features/admin/ (관리자 전용)
    └── [domain]-form/
        ├── model/[domain]-form.schema.ts
        ├── ui/[Domain]Form.tsx
        └── index.ts
```

### 서비스(일반 사용자)용인 경우:
```
src/
├── entities/[domain]/
│   ├── model/[domain].schema.ts
│   └── index.ts
└── features/service/ (일반 사용자)
    └── [domain]-form/
        ├── model/[domain]-form.schema.ts
        ├── ui/[Domain]Form.tsx
        └── index.ts
```

## What Gets Auto-Generated

### 1. Entity Schema (`src/entities/[domain]/model/[domain].schema.ts`)

**원칙:**
- ❌ 응답 스키마 생성 금지 (orval 타입 사용)
- ✅ 요청 스키마만 생성 (Create/Update)
- ✅ Update는 partial()

```typescript
import { z } from "zod";

/**
 * [Domain] 생성 요청 스키마 (Orval [Domain]CreateRequest 기반)
 */
export const create[Domain]Schema = z.object({
  /** 필드 설명 */
  field1: z.string().min(1, "필드를 입력해주세요"),
  // orval API 스펙의 모든 필드
});

/**
 * [Domain] 수정 요청 스키마
 */
export const update[Domain]Schema = create[Domain]Schema.partial();

export type Create[Domain]Form = z.infer<typeof create[Domain]Schema>;
export type Update[Domain]Form = z.infer<typeof update[Domain]Schema>;
```

**Index Export**: `src/entities/[domain]/index.ts`

### 2. Form Schema

**경로:**
- 관리자: `src/features/admin/[domain]-form/model/[domain]-form.schema.ts`
- 서비스: `src/features/service/[domain]-form/model/[domain]-form.schema.ts`

**핵심 원칙:**
- ❌ **NO transform** - UI 상태 값과 일치
- ✅ **Entity 상속** + 복합 검증만
- ✅ **데이터 변환은 onSubmit에서**

```typescript
import { create[Domain]Schema } from "@/entities/[domain]";
import { z } from "zod";

/**
 * [Domain] 생성 폼 스키마 (Entity 상속 + 복합 검증)
 */
export const create[Domain]FormSchema = create[Domain]Schema.extend({
  // 추가 검증만 (transform 금지)
}).refine(
  (data) => {
    // 복합 검증 로직 (예: 날짜 비교)
    return true;
  },
  { message: "검증 오류", path: ["field"] }
);

/**
 * [Domain] 수정 폼 스키마
 * Edit 전용 필드가 있다면 extend로 추가 후 partial()
 */
export const update[Domain]FormSchema = create[Domain]FormSchema
  .extend({
    // Edit 모드 전용 필드 (예: isActive: z.boolean())
  })
  .partial();

export type Create[Domain]FormInput = z.infer<typeof create[Domain]FormSchema>;
export type Update[Domain]FormInput = z.infer<typeof update[Domain]FormSchema>;

// 호환성 유지
export const [domain]FormSchema = create[Domain]FormSchema;
export type [Domain]FormInput = Create[Domain]FormInput;
```

**Index Export:**
- 관리자: `src/features/admin/[domain]-form/index.ts`
- 서비스: `src/features/service/[domain]-form/index.ts`

### 3. Form Component

**경로:**
- 관리자: `src/features/admin/[domain]-form/ui/[Domain]Form.tsx`
- 서비스: `src/features/service/[domain]-form/ui/[Domain]Form.tsx`

**핵심 패턴:**

```typescript
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import type { [Domain]CreateRequest } from '@/shared/api/orval/types';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/shared/ui/card';

/**
 * Discriminated Union Props
 */
type CreateProps = {
  mode: "create";
  initialValues?: never;
  onSubmit: (data: [Domain]CreateRequest) => Promise<void>;
  isLoading?: boolean;
};

type EditProps = {
  mode: "edit";
  initialValues: Partial<Update[Domain]FormInput>;
  onSubmit: (data: Partial<[Domain]CreateRequest>) => Promise<void>;
  isLoading?: boolean;
};

type [Domain]FormProps = CreateProps | EditProps;

/**
 * [Domain] 생성/수정 폼 컴포넌트
 */
export function [Domain]Form({ mode, initialValues, onSubmit, isLoading }: [Domain]FormProps) {
  // 1. Mode 기반 스키마 선택
  const form = useForm<Create[Domain]FormInput | Update[Domain]FormInput>({
    resolver: zodResolver(
      mode === "edit" ? update[Domain]FormSchema : create[Domain]FormSchema
    ),
    defaultValues: getDefaultValues(),
  });

  // 2. 데이터 변환 헬퍼 (도메인별로 필요시)
  const formatToApi = (dateString: string): string => {
    return new Date(dateString).toISOString();
  };

  // 3. dirtyFields 기반 제출
  const handleOnSubmit = async (values: [Domain]FormInput | Update[Domain]FormInput) => {
    if (mode === "edit") {
      const data = values as Update[Domain]FormInput;
      const { dirtyFields } = form.formState;
      const dirtyData: Partial<[Domain]CreateRequest> = {};

      Object.keys(dirtyFields).forEach((key) => {
        const k = key as keyof Update[Domain]FormInput;
        const value = data[k];
        if (value === undefined) return;

        // 필드별 변환 (날짜 등)
        (dirtyData as any)[k] = value;
      });

      await onSubmit(dirtyData);
    } else {
      // Create 모드: 전체 데이터 변환
      const data = values as Create[Domain]FormInput;
      const createData: [Domain]CreateRequest = {
        // 필드별 변환
      };
      await onSubmit(createData);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>{mode === "create" ? "[Domain] 등록" : "[Domain] 수정"}</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={form.handleSubmit(handleOnSubmit)} className="space-y-4">
          {/* Shadcn UI 컴포넌트 */}

          {/* Edit 전용 필드는 조건부 렌더링 */}
          {mode === "edit" && (
            <div>
              {/* Edit 모드 전용 필드 */}
            </div>
          )}

          <Button type="submit" disabled={isLoading} className="w-full">
            {isLoading ? '처리 중...' : mode === "create" ? "등록" : "수정"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
```

## FSD Architecture Rules

```
app → views → widgets → features → entities → shared
     (only import from lower layers)
```

- **entities**: Pure domain schemas (request only)
- **features/admin**: Admin business logic + UI
- **features/service**: Service business logic + UI
- **shared**: Reusable UI components (Shadcn)

## 핵심 패턴 정리

### 1. Schema 설계
- **NO transform**: UI 데이터 구조와 일치
- **Update Schema**: `.partial()` + Edit 전용 필드 `.extend()`
- **타입**: `z.infer`만 사용 (input/output 분리 없음)

### 2. Props 설계
- **Discriminated Union**: `CreateProps | EditProps`
- **Mode 기반 스키마**: `mode === "edit" ? update : create`

### 3. Submit 처리
- **dirtyFields**: Edit 모드에서 변경된 필드만 전송
- **forEach + undefined 체크**: Type-Safe 처리
- **데이터 변환**: onSubmit에서 처리 (날짜, 숫자 등)

### 4. 조건부 렌더링
- Edit 전용 필드: `mode === "edit" && (...)`

## 변환 패턴 예시

**날짜 필드:**
```typescript
// UI → API
if (k === "startDate") {
  dirtyData[k] = new Date(value as string).toISOString();
}

// API → UI (Edit View에서)
initialValues={{ startDate: data.startDate.split("T")[0] }}
```

**Edit 전용 필드:**
```typescript
// Schema
export const update[Domain]FormSchema = create[Domain]FormSchema
  .extend({ isActive: z.boolean() })
  .partial();

// Component
{mode === "edit" && (
  <Checkbox
    checked={form.watch("isActive") ?? true}
    onCheckedChange={(checked) => form.setValue("isActive", checked as boolean)}
  />
)}
```

**숫자 필드:**
```typescript
<Input type="number" {...form.register("price", { valueAsNumber: true })} />
```

## Mandatory Requirements

### Documentation
- ✅ **함수 JSDoc**: 목적, @param, @returns 필수
- ✅ **인터페이스 주석**: 모든 프로퍼티에 `/** 설명 */`
- ✅ **분기문 주석**: 5줄 이상 분기문에 설명 필수

### Code Standards
- ✅ **Server Component 우선**: 상호작용 필요시만 'use client'
- ✅ **FSD Public API**: index.ts를 통한 export만 허용
- ✅ **pnpm 사용**: npm, yarn 금지
- ✅ **Shadcn UI**: @/shared/ui에서 import

### Schema Rules
- ❌ **응답 스키마 생성 금지**: orval 타입 사용
- ✅ **요청 스키마만**: create, update용만
- ✅ **FSD 의존성**: features가 entities 상속
- ✅ **폼 로직 분리**: entities(순수) vs features(폼 특화)
- ❌ **NO transform**: 스키마에서 변환 금지
- ✅ **검증 로직**: `.refine()` 사용

## Implementation Flow

1. **Detect Domain Name & Context**
   - Extract from user's natural language
   - Convert to kebab-case
   - **Determine if admin or service**

2. **Check Orval Types**
   - Look for `src/shared/api/orval/types/`
   - Identify `[Domain]CreateRequest` fields

3. **Generate Entity Schema**
   - Pure request validation
   - Update는 partial()

4. **Generate Form Schema**
   - **Path: features/admin/ or features/service/**
   - Extend entity schema
   - NO transform, only refine
   - Edit 전용 필드 extend

5. **Generate Form Component**
   - **Path: features/admin/ or features/service/**
   - Discriminated Union Props
   - Mode 기반 스키마 선택
   - dirtyFields 처리
   - 조건부 렌더링

6. **Create Index Exports**
   - Entity public API
   - Feature public API

7. **Verify**
   - Correct path (admin/service)
   - FSD dependencies
   - JSDoc present
   - Shadcn imports

## Integration with Orval

When orval types exist:
1. Read `src/shared/api/orval/types/`
2. Match `[Domain]CreateRequest` payload
3. Generate zod schema based on API fields
4. Use orval response types (don't recreate)

## Reference

All rules follow `F:\work\smarter-store-fe\CLAUDE.md`
