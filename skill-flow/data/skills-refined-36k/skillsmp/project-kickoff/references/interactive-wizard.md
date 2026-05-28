# Interactive Wizard Flow

## Phase 1: Gather Configuration

Ask questions sequentially to collect required information:

### 1️⃣ 프로젝트 기본 정보

```markdown
## 🚀 프로젝트 킥오프 시작

새로운 Semicolon 커뮤니티 서비스를 생성합니다.
몇 가지 정보가 필요해요.

---

### 1️⃣ 프로젝트 기본 정보

**프로젝트 이름**을 알려주세요.

- 형식: kebab-case (예: `my-school-community`)
- 현재 감지된 이름: `{detected_name}` (맞으면 Enter)

> 입력:
```

### 2️⃣ Supabase 설정

```markdown
### 2️⃣ Supabase 설정

**Supabase 프로젝트 ID**를 알려주세요.

- 위치: Supabase Dashboard > Project Settings > General
- 형식: 영문+숫자 조합 (예: `wloqfachtbxceqikzosi`)

> 입력:
```

### 3️⃣ Supabase Keys

```markdown
### 3️⃣ Supabase Keys

**ANON_KEY**를 알려주세요.

- 위치: Supabase Dashboard > Project Settings > API > anon public
- `eyJ`로 시작하는 긴 문자열

> 입력:
```

### 4️⃣ Service Role Key (선택)

```markdown
### 4️⃣ Service Role Key (선택)

**SERVICE_ROLE_KEY**를 알려주세요. (나중에 설정하려면 `skip` 입력)

- 위치: Supabase Dashboard > Project Settings > API > service_role
- ⚠️ 이 키는 절대 공개하면 안 됩니다

> 입력:
```

### 5️⃣ 서비스 설명 (선택)

```markdown
### 5️⃣ 서비스 설명 (선택)

**서비스 한 줄 설명**을 입력해주세요. (기본값 사용하려면 `skip`)

- 예: "교내 정보 공유 및 커뮤니티 플랫폼"

> 입력:
```

## Phase 2: Confirm Configuration

```markdown
## ✅ 설정 확인

다음 설정으로 프로젝트를 생성합니다:

| 항목                  | 값                    |
| --------------------- | --------------------- |
| **프로젝트 이름**     | {project_name}        |
| **서비스 제목**       | {service_title}       |
| **Supabase 프로젝트** | {supabase_project_id} |
| **ANON_KEY**          | {anon_key_masked}     |
| **SERVICE_ROLE_KEY**  | {service_role_masked} |
| **서비스 설명**       | {description}         |

**출력 위치**: `implement-dist/{project_name}/`

---

이대로 진행할까요? (Y/n)
```

## Example Interaction

```
User: cm-school-portal 프로젝트 만들어줘

Agent:
## 🚀 프로젝트 킥오프 시작

새로운 Semicolon 커뮤니티 서비스를 생성합니다.

### 1️⃣ 프로젝트 기본 정보
**프로젝트 이름**: `cm-school-portal` ✓ (감지됨)

### 2️⃣ Supabase 설정
**Supabase 프로젝트 ID**를 알려주세요.

User: abc123xyz456

Agent:
### 3️⃣ Supabase Keys
**ANON_KEY**를 알려주세요.

User: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Agent:
### 4️⃣ Service Role Key
**SERVICE_ROLE_KEY**를 알려주세요. (skip 가능)

User: skip

Agent:
## ✅ 설정 확인
| 항목 | 값 |
|------|-----|
| 프로젝트 이름 | cm-school-portal |
| Supabase 프로젝트 | abc123xyz456 |
| ANON_KEY | eyJhbG...****** |

이대로 진행할까요? (Y/n)

User: Y

Agent:
[프로젝트 생성 실행...]

## 🎉 프로젝트 생성 완료!
**Cm School Portal** 프로젝트가 생성되었습니다.

📁 생성 위치: `implement-dist/cm-school-portal/`
...
```
