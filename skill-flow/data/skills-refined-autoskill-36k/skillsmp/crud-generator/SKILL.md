---
name: crud-generator
description: Auto-generate CRUD when user mentions "CRUD 추가", "관리 페이지 만들어", "[기능] 리스트/등록/상세/수정"
---

# CRUD Generator Skill

Automatically generates complete Admin CRUD (Create, Read, Update, Delete) system with React Query.

## Trigger Phrases

- "관리자 [기능] CRUD 추가해줘"
- "[기능] 관리 페이지 만들어줘"
- "[기능] 추가하고 AdminSidebar에 메뉴 추가"
- "[기능] 리스트/등록/상세/수정 페이지 만들어"

## ⚠️ CRITICAL: Orval 기반 개발

**반드시 첫 단계로 Orval 확인:**

1. ✅ **Orval 타입/API 확인** (`src/shared/api/orval/types/`, `orval/admin-[domain]/`)
2. ✅ **React Query 사용** (Admin 전용)
3. ✅ **Entity Schema**: Orval CreateRequest → Zod, Update는 partial()
4. ✅ **Entity API**: React Query hooks (queryKeys, useQuery, useMutation)

## Domain Name Extraction

자연어에서 도메인 정보 추출:

| User Input | Domain | Display | Icon |
|------------|--------|---------|------|
| "쿠폰 CRUD" | coupon | 쿠폰 | Ticket |
| "상품 카테고리 관리" | product-category | 상품 카테고리 | Package |

## FSD Structure

**⚠️ 중요: Admin 전용 - admin 경로 사용**

```
src/
├── entities/[domain]/
│   ├── api/[domain].api.ts (React Query hooks)
│   ├── model/[domain].schema.ts (Zod schema)
│   └── index.ts
├── features/admin/ (관리자 전용)
│   ├── [domain]-form/ (Form component)
│   └── [domain]-table/ (DataTable)
├── views/admin/ (관리자 전용)
│   └── [domain]/ (list/detail/create/edit)
└── widgets/admin-sidebar/

app/admin/[domain]s/ (4개 페이지)
```

**서비스(일반 사용자)용이면:**
```
features/service/[domain]-form/
views/service/[domain]/
app/(layout)/[domain]s/
```

## What Gets Generated

### 1. PAGES 상수 + AdminSidebar 메뉴
- `src/shared/constants/routes.ts`: `/admin/[domain]s` 경로
- `src/widgets/admin-sidebar/lib/sidebarData.ts`: 메뉴 항목

### 2. Entity Layer

**Schema** (`entities/[domain]/model/[domain].schema.ts`):
```typescript
// Orval CreateRequest → Zod 변환
export const create[Domain]Schema = z.object({
  // 모든 필드
});

// Update는 partial()
export const update[Domain]Schema = create[Domain]Schema.partial();
```

**API** (`entities/[domain]/api/[domain].api.ts`):
```typescript
export const [domain]QueryKeys = {
  all: ["[domain]s"] as const,
  lists: () => [[domain]QueryKeys.all, "list"] as const,
  details: () => [[domain]QueryKeys.all, "detail"] as const,
  detail: (id: number) => [[domain]QueryKeys.details(), id] as const,
};

// useGetAll[Domain]s, useGet[Domain], useCreate[Domain], useUpdate[Domain], useDelete[Domain]
```

### 3. Form Schema + Component

**Schema** (`features/[domain]-form/model/[domain]-form.schema.ts`):
```typescript
// ❌ NO transform - UI 데이터 구조 유지
// ✅ Entity 상속 + 복합 검증만

export const create[Domain]FormSchema = create[Domain]Schema.extend({
  // 추가 검증만
}).refine(...);

// Edit 전용 필드 추가 후 partial()
export const update[Domain]FormSchema = create[Domain]FormSchema
  .extend({
    // Edit 모드 전용 필드 (예: isActive)
  })
  .partial();
```

**Component** (`features/admin/[domain]-form/ui/[Domain]Form.tsx`) - 관리자 전용:
```typescript
// Discriminated Union Props
type CreateProps = {
  mode: "create";
  initialValues?: never;
  onSubmit: (data: [Domain]CreateRequest) => Promise<void>;
};

type EditProps = {
  mode: "edit";
  initialValues: Partial<Update[Domain]FormInput>;
  onSubmit: (data: Partial<[Domain]CreateRequest>) => Promise<void>;
};

// Mode 기반 스키마 선택
const form = useForm({
  resolver: zodResolver(
    mode === "edit" ? update[Domain]FormSchema : create[Domain]FormSchema
  ),
});

// dirtyFields 기반 제출 (Edit 모드에서 변경된 필드만)
const handleOnSubmit = async (values) => {
  if (mode === "edit") {
    const { dirtyFields } = form.formState;
    const dirtyData = {};
    Object.keys(dirtyFields).forEach((key) => {
      // 필드별 변환 로직 (날짜 등)
    });
    await onSubmit(dirtyData);
  } else {
    // Create 모드: 전체 데이터 변환
  }
};
```

### 4. Views (React Query)

```typescript
// List: useGetAll[Domain]s + DataTable
const { data, isLoading } = useGetAll[Domain]s();

// Detail: useGet[Domain]
const { data } = useGet[Domain](id);

// Create: useCreate[Domain] + toast
const { mutateAsync } = useCreate[Domain]();

// Edit: useGet[Domain] + useUpdate[Domain]
// ISO → YYYY-MM-DD 변환: isoString.split("T")[0]
```

### 5. App Routes

```
app/admin/[domain]s/
  page.tsx (List)
  [id]/page.tsx (Detail)
  create/page.tsx (Create)
  [id]/edit/page.tsx (Edit)
```

## 핵심 패턴

### Schema
- ❌ **NO transform**: UI 데이터와 일치
- ✅ **Update schema**: `partial()` + Edit 전용 필드 `extend()`
- ✅ **Mode 기반 스키마 선택**

### Form
- ✅ **Discriminated Union Props**: `CreateProps | EditProps`
- ✅ **dirtyFields**: Edit 모드에서 변경 필드만 전송
- ✅ **조건부 렌더링**: `mode === "edit" && (...)`

### Data
- ✅ **Orval 타입 직접 사용**: `[Domain]CreateRequest`
- ✅ **React Query**: queryKeys, useQuery, useMutation
- ✅ **Toast**: success/error 메시지

### Code Quality
- ✅ **JSDoc 주석**: 함수, 인터페이스
- ✅ **Public API**: index.ts
- ✅ **Shadcn UI**: @/shared/ui

## Implementation Flow

1. 자연어에서 도메인 정보 추출 (name, display, icon)
2. Orval 타입/API 확인
3. PAGES 상수 + AdminSidebar 메뉴 추가
4. Entity 생성 (schema + React Query API)
5. Form 생성 (schema + component, dirtyFields 패턴)
6. DataTable 생성 (row click)
7. Views 생성 (useQuery + useMutation)
8. App Routes 생성
9. Toast 메시지 추가

## Reference

All rules follow `F:\work\smarter-store-fe\CLAUDE.md`
