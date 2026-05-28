# tools-mcp: MCP 도구 사용 패턴

## 핵심 규칙

**⚠️ 일반 Read/Write/Glob이 아닌 CAD 전용 MCP 도구를 사용해야 합니다!**

| MCP 도구 | 설명 | 일반 도구 (사용 금지) |
|----------|------|--------------------|
| `mcp__ai-native-cad__glob` | CAD 파일 목록 | ❌ Glob |
| `mcp__ai-native-cad__read` | CAD 코드 읽기 | ❌ Read |
| `mcp__ai-native-cad__edit` | 부분 수정 → 자동 실행 | ❌ Edit |
| `mcp__ai-native-cad__write` | 전체 작성 → 자동 실행 | ❌ Write |
| `mcp__ai-native-cad__lsp` | 함수 스키마 탐색 | - |
| `mcp__ai-native-cad__bash` | 씬 조회/내보내기 | ❌ Bash |

## glob - 파일 목록 조회

```javascript
// 전체 파일 목록
glob()
// → main, chicken, crossy_bg, ...

// 패턴 매칭
glob({ pattern: 'house_*' })
// → house_lib, house_advanced
```

**패턴 문법:**
- `*` - 0개 이상의 문자 매칭 (예: `house_*` → house_lib, house_advanced)
- `?` - 정확히 1개의 문자 매칭 (예: `car_?` → car_0, car_1)
- 정규식이나 character class는 지원하지 않음
- 파일명에는 영문, 숫자, 밑줄, 하이픈만 허용

## read - 파일 읽기

```javascript
// main 코드 읽기
read({ file: 'main' })

// 모듈 읽기
read({ file: 'chicken' })
```

## edit - 부분 수정 (자동 실행)

```javascript
// old_code를 new_code로 교체
edit({
  file: 'main',
  old_code: 'radius: 50',
  new_code: 'radius: 100'
})
// → 파일 수정 + 코드 실행 + 결과 반환

// 실패 시 자동 롤백 (파일 변경 없음)

// 멀티라인 수정 예시 (들여쓰기/줄바꿈 정확히 일치 필요)
edit({
  file: 'main',
  old_code: `function draw() {
  drawRect('a', 0, 0, 10, 10);
}`,
  new_code: `function draw() {
  drawRect('a', 0, 0, 20, 20);
  drawCircle('b', 30, 0, 5);
}`
})
```

**주의**:
- `old_code`는 공백/들여쓰기/줄바꿈까지 정확히 일치해야 함
- 모든 일치 항목이 교체됨 (replaceAll 동작)

## write - 전체 작성 (자동 실행)

```javascript
// 새 모듈 작성
write({
  file: 'house_lib',
  code: `
function buildHouse(name, x, y) {
  drawRect(name + '_wall', 0, 15, 40, 30);
  createGroup(name, [name + '_wall']);
  translate(name, x, y);
}
`
})

// main 작성
write({
  file: 'main',
  code: `
import 'house_lib'
buildHouse('h1', 0, 0);
`
})
```

**동작 특성:**
- 파일명에 확장자 없이 지정 (자동으로 `.js` 추가)
- 저장 즉시 실행됨 (MCP 서버가 코드 실행)
- 모듈 파일(`house_lib`) 작성 후 `main`에서 `import 'house_lib'`로 사용
- 실행 순서: 모듈 등록 → main 실행 (import가 모듈 코드로 치환됨)
- 실패 시 파일과 씬 모두 롤백됨

## lsp - 코드 탐색

```javascript
// 1. 도메인 목록
lsp({ operation: 'domains' })
// → primitives, text, transforms, boolean, geometry, style, groups, query, utility

// 2. 도메인 내 함수 시그니처
lsp({ operation: 'describe', domain: 'primitives' })
// → drawCircle(name, x, y, radius), drawRect(name, x, y, w, h), ...

// 3. 특정 함수 상세 스키마
lsp({ operation: 'schema', name: 'drawBezier' })
// → 파라미터, 타입, 설명, 예시 코드

// 4. 파일 내 심볼 (클래스, 함수)
lsp({ operation: 'symbols', file: 'chicken' })
// → 모듈에 정의된 함수/클래스 목록
```

## bash - 씬 조회/내보내기

```javascript
// 씬 정보
bash({ command: 'info' })       // 엔티티 수, bounds
bash({ command: 'tree' })       // 계층 구조
bash({ command: 'groups' })     // 그룹 목록
bash({ command: 'draw_order' }) // z-order (root)
bash({ command: 'draw_order', group: 'robot' }) // 그룹 내부

// 엔티티 좌표 조회 (로컬 + 월드)
bash({ command: 'entity', name: 'chicken_body' })
// → { local: { geometry, transform, bounds }, world: { bounds, center } }
// 💡 스케치 좌표와 비교하여 translate()로 위치 조정

// 내보내기
bash({ command: 'capture' })    // PNG 스크린샷
bash({ command: 'svg' })        // SVG 벡터
bash({ command: 'json' })       // JSON

// 초기화 (주의!)
bash({ command: 'reset' })

// 스냅샷/undo/redo (세션 내 상태 관리)
bash({ command: 'snapshot' })  // 현재 씬 스냅샷 저장
bash({ command: 'undo' })      // 이전 스냅샷으로 복원
bash({ command: 'redo' })      // 다음 스냅샷으로 이동
bash({ command: 'snapshots' }) // 스냅샷 히스토리 조회
// 💡 undo/redo 실패 시 현재 씬 상태 자동 복원
```

## 워크플로우 예시

### 기본 워크플로우

```
1. glob() → 기존 모듈 확인
2. read({ file: 'main' }) → 현재 코드 확인
3. lsp({ operation: 'schema', name: 'drawCircle' }) → 함수 스키마 확인
4. write({ file: 'main', code: '...' }) → 코드 작성 + 실행
5. bash({ command: 'capture' }) → 결과 확인
6. bash({ command: 'entity', name: '...' }) → 좌표 확인
7. edit({ file: 'main', ... }) → 수정 + 실행
```

### 에러 복구가 필요한 경우

```
1. bash({ command: 'snapshot' }) → 수정 전 상태 저장
2. write/edit 실행
   - 성공 → 계속 진행
   - 실패 → 자동 롤백 (파일 + 씬 복원)
3. 수동 복구 필요 시:
   - bash({ command: 'undo' }) → 스냅샷으로 복원
   - bash({ command: 'snapshots' }) → 히스토리 확인
```

## 트랜잭션 동작

- `edit`/`write` 실행 시 코드가 실패하면:
  1. **파일 자동 롤백**: 수정 전 원본 파일 복원
  2. **씬 자동 복원**: main.js 재실행으로 이전 씬 상태 복구
- 안전하게 실험 가능
- 실패 메시지에서 에러 원인 확인 후 수정
- 수동 복구: `bash({ command: 'undo' })`로 스냅샷 기반 복원
