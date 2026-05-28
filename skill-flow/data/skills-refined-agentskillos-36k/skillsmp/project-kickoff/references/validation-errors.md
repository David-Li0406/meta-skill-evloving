# Validation & Error Handling

## Configuration Schema

```yaml
required:
  project_name:
    type: string
    format: kebab-case
    example: "my-school-community"

  supabase_project_id:
    type: string
    format: alphanumeric
    example: "wloqfachtbxceqikzosi"

  anon_key:
    type: string
    format: jwt
    starts_with: "eyJ"

optional:
  service_role_key:
    type: string
    format: jwt
    default: "your-service-role-key-here"

  description:
    type: string
    default: "Semicolon 커뮤니티 기반 서비스"
```

## Validation Rules

### Project Name Validation

```javascript
function validateProjectName(name) {
  // kebab-case: lowercase letters, numbers, hyphens
  const pattern = /^[a-z][a-z0-9-]*[a-z0-9]$/;

  if (!pattern.test(name)) {
    return { valid: false, reason: "kebab-case 형식이 아닙니다" };
  }

  if (name.includes("--")) {
    return { valid: false, reason: "연속된 하이픈은 사용할 수 없습니다" };
  }

  if (name.length < 3) {
    return { valid: false, reason: "최소 3자 이상이어야 합니다" };
  }

  return { valid: true };
}
```

### Supabase Project ID Validation

```javascript
function validateSupabaseProjectId(id) {
  // Supabase project IDs are alphanumeric, ~20 chars
  const pattern = /^[a-z0-9]{15,25}$/;
  return pattern.test(id);
}
```

### ANON_KEY Validation

```javascript
function validateAnonKey(key) {
  // JWT format starting with eyJ
  return key.startsWith("eyJ") && key.length > 100;
}
```

## Error Messages

### Invalid Project Name

```markdown
⚠️ 프로젝트 이름이 올바르지 않습니다.

**요구사항**:

- kebab-case 형식 (소문자, 하이픈만 사용)
- 예: `my-school-community`, `company-portal`

**입력값**: `{invalid_input}`
**문제**: {reason}

다시 입력해주세요:
```

### Invalid Supabase Project ID

```markdown
⚠️ Supabase 프로젝트 ID가 올바르지 않습니다.

**요구사항**:

- 영문 소문자 + 숫자 조합
- Supabase Dashboard에서 확인 가능

다시 입력해주세요:
```

### Invalid ANON_KEY

```markdown
⚠️ ANON_KEY 형식이 올바르지 않습니다.

**요구사항**:

- `eyJ`로 시작하는 JWT 토큰
- Supabase Dashboard > Project Settings > API에서 복사

다시 입력해주세요:
```

### Script Execution Failure

```markdown
❌ 프로젝트 생성 중 오류가 발생했습니다.

**오류 내용**:
{error_message}

**해결 방법**:
1. 입력값 확인
2. 템플릿 디렉토리 확인: `ls -la scripts/`
3. 권한 확인: `chmod +x scripts/create-service.sh`

다시 시도하시겠습니까? (Y/n)
```
