---
name: jikime-migration-ast-grep
description: AST-based code transformation skill using ast-grep. Structural code search and automated migration patterns for legacy code conversion.
version: 1.0.0
tags: ["migration", "ast", "code-transformation", "legacy", "refactoring"]
triggers:
  keywords: ["ast-grep", "sg", "code transformation", "migration pattern", "리팩토링"]
  phases: ["run"]
  agents: ["refactorer"]
  languages: []
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~2000
user-invocable: false
context: fork
agent: migration-orchestrator
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# JikiME AST-grep Migration Skill

ast-grep을 활용한 코드 변환 및 마이그레이션 자동화 스킬입니다.

## Overview

ast-grep(sg)은 구조적 코드 검색 및 변환 도구입니다.
정규식 대신 AST(Abstract Syntax Tree) 패턴을 사용하여 정확한 코드 매칭과 변환을 수행합니다.

## Installation

```bash
# macOS
brew install ast-grep

# npm
npm install -g @ast-grep/cli

# cargo
cargo install ast-grep
```

## Basic Usage

### 검색 (Search)
```bash
# 패턴으로 검색
sg --pattern 'console.log($$$)' --lang typescript

# 특정 디렉토리에서 검색
sg --pattern 'useState($VALUE)' --lang tsx src/

# 검색 결과를 JSON으로
sg --pattern '$FUNC($$$)' --lang javascript --json
```

### 변환 (Rewrite)
```bash
# 패턴 변환
sg --pattern 'var $VAR = $VALUE' --rewrite 'const $VAR = $VALUE' --lang javascript

# 실제 파일 수정
sg --pattern 'var $VAR = $VALUE' --rewrite 'const $VAR = $VALUE' --lang javascript -i
```

## Pattern Syntax

### Meta Variables
| Pattern | Matches |
|---------|---------|
| `$NAME` | 단일 노드 (식별자, 리터럴 등) |
| `$$$ARGS` | 0개 이상의 노드 (가변 인자) |
| `$_` | 와일드카드 (모든 단일 노드) |

### Examples
```yaml
# 함수 호출 매칭
pattern: 'console.log($MSG)'
# matches: console.log("hello"), console.log(variable)

# 여러 인자 매칭
pattern: 'fetch($URL, $$$OPTIONS)'
# matches: fetch(url), fetch(url, options), fetch(url, { method: 'POST' })

# 와일드카드
pattern: 'import $_ from "react"'
# matches: import React from "react", import { useState } from "react"
```

## Migration Rules

### Rule File Structure
```yaml
# rules/migrate-var-to-const.yaml
id: migrate-var-to-const
message: "Use 'const' instead of 'var'"
severity: warning
language: javascript
rule:
  pattern: 'var $VAR = $VALUE'
fix: 'const $VAR = $VALUE'
```

### Complex Rules
```yaml
# rules/migrate-class-to-function.yaml
id: migrate-class-component
message: "Migrate class component to function component"
severity: info
language: tsx
rule:
  pattern: |
    class $NAME extends React.Component {
      render() {
        return $JSX;
      }
    }
fix: |
  function $NAME() {
    return $JSX;
  }
```

## Migration Scenarios

### jQuery → React Patterns

#### Event Handler Migration
```yaml
# rules/jquery-click-to-react.yaml
id: jquery-click-to-onclick
language: javascript
rule:
  pattern: '$($SELECTOR).on("click", $HANDLER)'
fix: '// TODO: Convert to onClick={$HANDLER} in JSX'
note: "Manual review required for selector conversion"
```

#### AJAX to Fetch
```yaml
# rules/jquery-ajax-to-fetch.yaml
id: jquery-ajax-to-fetch
language: javascript
rule:
  pattern: |
    $.ajax({
      url: $URL,
      method: $METHOD,
      success: $SUCCESS,
      error: $ERROR
    })
fix: |
  fetch($URL, { method: $METHOD })
    .then(response => response.json())
    .then($SUCCESS)
    .catch($ERROR)
```

### PHP → TypeScript Patterns

#### Array to Object
```yaml
# rules/php-array-to-ts-object.yaml
id: php-array-syntax
language: php
rule:
  pattern: 'array($$$ITEMS)'
message: "Convert to TypeScript object literal"
# Manual conversion needed - PHP arrays are complex
```

### Vue 2 → Vue 3 Patterns

#### Options to Composition API
```yaml
# rules/vue-data-to-ref.yaml
id: vue-data-to-ref
language: javascript
rule:
  pattern: |
    data() {
      return {
        $NAME: $VALUE
      }
    }
fix: 'const $NAME = ref($VALUE);'
```

#### $emit to defineEmits
```yaml
# rules/vue-emit-to-define.yaml
id: vue-emit-migration
language: javascript
rule:
  pattern: 'this.$emit($EVENT, $$$ARGS)'
fix: 'emit($EVENT, $$$ARGS)'
note: "Add defineEmits at component top"
```

### React Patterns

#### Class to Function Component
```yaml
# rules/react-class-to-function.yaml
id: react-class-to-function
language: tsx
rule:
  pattern: |
    class $NAME extends Component {
      state = { $STATE_KEY: $STATE_VALUE };
      render() {
        return $JSX;
      }
    }
fix: |
  function $NAME() {
    const [$STATE_KEY, set$STATE_KEY] = useState($STATE_VALUE);
    return $JSX;
  }
```

#### useState Destructuring
```yaml
# rules/react-usestate-naming.yaml
id: usestate-naming
language: tsx
rule:
  pattern: 'const [$STATE, $SETTER] = useState($INITIAL)'
constraints:
  $SETTER:
    regex: '^set[A-Z]'
message: "useState setter should follow setXxx naming convention"
```

## Workflow Integration

### Pre-Migration Analysis
```bash
# 1. 변환 대상 코드 검색
sg scan --rule rules/migration/ --json > migration-targets.json

# 2. 변환 예상 결과 미리보기
sg --pattern 'var $VAR = $VALUE' --rewrite 'const $VAR = $VALUE' --lang js

# 3. 실제 변환 적용
sg --pattern 'var $VAR = $VALUE' --rewrite 'const $VAR = $VALUE' --lang js -i
```

### Batch Migration
```yaml
# sgconfig.yaml
ruleDirs:
  - rules/migration/

rules:
  - id: phase1-syntax
    include:
      - rules/migration/syntax/*.yaml
  - id: phase2-patterns
    include:
      - rules/migration/patterns/*.yaml
```

```bash
# 단계별 마이그레이션 실행
sg scan --rule phase1-syntax --fix
sg scan --rule phase2-patterns --fix
```

## Custom Rule Development

### Rule Structure
```yaml
id: unique-rule-id           # 규칙 고유 ID
message: "Description"        # 사용자에게 표시할 메시지
severity: error|warning|info  # 심각도
language: typescript          # 대상 언어
rule:
  pattern: 'code pattern'     # 매칭 패턴
  kind: identifier            # (선택) AST 노드 종류
  inside:                     # (선택) 부모 노드 조건
    kind: function_declaration
  has:                        # (선택) 자식 노드 조건
    pattern: 'specific child'
fix: 'replacement code'       # 자동 수정 코드
constraints:                  # (선택) 추가 조건
  $VAR:
    regex: '^_'               # 정규식 조건
```

### Multi-Pattern Rules
```yaml
id: complex-migration
rule:
  any:
    - pattern: 'pattern1($A)'
    - pattern: 'pattern2($B)'
  not:
    pattern: 'exception($C)'
```

## Integration with Commands

| Command | ast-grep Usage |
|---------|----------------|
| `/jikime:migrate-0-discover` | 코드 패턴 분석 및 변환 대상 식별 |
| `/jikime:migrate-3-execute` | 자동 코드 변환 실행 |
| `/jikime:refactor` | 리팩토링 패턴 적용 |

### Discover Phase
```bash
# 레거시 패턴 검색
sg --pattern 'var $VAR = $VALUE' --lang js --json | jq '.matches | length'
sg --pattern '$.ajax($$$)' --lang js --json | jq '.matches | length'
sg --pattern 'this.$emit($$$)' --lang vue --json | jq '.matches | length'
```

### Migrate Phase
```bash
# 순차적 변환
sg scan --rule rules/phase1-syntax.yaml --fix
sg scan --rule rules/phase2-patterns.yaml --fix
sg scan --rule rules/phase3-modern.yaml --fix
```

## Best Practices

1. **점진적 적용**: 한 번에 하나의 규칙만 적용
2. **미리보기**: `-i` 없이 먼저 결과 확인
3. **백업**: 변환 전 git commit
4. **테스트**: 변환 후 테스트 실행
5. **수동 검토**: 복잡한 변환은 수동 확인

## Limitations

- 주석은 AST에서 제외될 수 있음
- 포맷팅이 변경될 수 있음 (Prettier로 후처리)
- 복잡한 제어 흐름 변환은 수동 필요
- 런타임 동작 변경은 감지 불가
