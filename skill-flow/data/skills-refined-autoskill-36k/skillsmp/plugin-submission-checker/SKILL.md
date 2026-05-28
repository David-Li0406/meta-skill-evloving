---
name: plugin-submission-checker
description: Obsidian 커뮤니티 플러그인 코드가 공식 가이드라인을 준수하는지 자동으로 검사하고 개선점을 제안하며, 플러그인 제출 전 코드 품질, 보안, 성능 검토가 필요할 때 사용한다.
---

# Plugin Submission Checker

Obsidian 플러그인 제출 전 필수 요구사항을 자동으로 검사한다.

전체 체크리스트: [references/checklist.md](references/checklist.md)

## 검사 절차

### 1. Manifest 검사

```bash
cat manifest.json
```

**검사 항목**:
- `description`: 250자 이내, 마침표로 끝남, 동작 문장으로 시작
- `minAppVersion`: 호환 가능한 최소 버전 설정 여부
- `fundingUrl`: 유효한 후원 서비스 링크 또는 제거 여부
- `isDesktopOnly`: Node.js/Electron API 사용 시 `true` 설정 여부

### 2. 보안 검사

```bash
grep -rn "innerHTML\s*=" src/
grep -rn "outerHTML\s*=" src/
grep -rn "insertAdjacentHTML" src/
```

**위반 시**: `createEl()`, `createDiv()`, `createSpan()`, `el.empty()` 사용 권장

### 3. 코드 품질 검사

```bash
# 전역 app 사용 금지
grep -rn "window\.app" src/
grep -rn "[^.]app\." src/ | grep -v "this.app"

# 콘솔 로깅 제거
grep -rn "console\.\(log\|debug\|info\|warn\)" src/

# var 대신 const/let
grep -rn "^[[:space:]]*var\s" src/

# Promise 체인 대신 async/await
grep -rn "\.then\s*(" src/
```

### 4. 모바일 호환성 검사

```bash
grep -rn "require.*fs" src/
grep -rn "require.*electron" src/
grep -rn "require.*child_process" src/
grep -rn "require.*path" src/
```

**위반 시**: `manifest.json`에서 `isDesktopOnly: true` 설정 필요

### 5. UI 텍스트 검사

```bash
grep -rn "<h[1-6]>" src/
```

**검사 항목**:
- Sentence case 사용 (Title Case 아님)
- 설정 탭 최상위 헤딩 없음
- `setHeading()` 메서드 사용

### 6. 리소스 관리 검사

```bash
grep -rn "addEventListener" src/
grep -rn "\.on\s*(" src/ | grep -v "registerEvent"
```

**권장**: `registerEvent()`, `addCommand()` 사용하여 자동 정리

### 7. Workspace/Vault API 검사

```bash
# activeLeaf 직접 접근 금지
grep -rn "workspace\.activeLeaf" src/

# vault.adapter 대신 vault API 사용
grep -rn "vault\.adapter" src/

# 비효율적인 파일 검색
grep -rn "getFiles\(\)\.find" src/
grep -rn "getFiles\(\)\.filter" src/

# Vault.modify 대신 Editor API/vault.process
grep -rn "vault\.modify" src/
```

### 8. 스타일링 검사

```bash
grep -rn 'style="' src/
grep -rn "\.style\." src/
grep -rn "color:\s*#" styles.css 2>/dev/null
grep -rn "background.*:\s*#" styles.css 2>/dev/null
```

**권장**: CSS 클래스 및 Obsidian CSS 변수(`var(--text-normal)` 등) 사용

### 9. 명령어 검사

```bash
grep -rn "hotkeys:" src/
```

### 10. 필수 파일 검사

다음 파일 존재 여부 확인:
- `README.md`
- `LICENSE`
- `manifest.json`
- `package.json`

## 결과 보고서 형식

```markdown
# 플러그인 제출 검사 결과

## 1. Manifest 설정
| 항목 | 상태 | 비고 |
|------|------|------|
| description 250자 이내 | ✅/❌ | 현재 N자 |
| description 마침표 종료 | ✅/❌ | |
| minAppVersion 설정 | ✅/❌ | |
| fundingUrl 유효성 | ✅/❌/N/A | |
| isDesktopOnly 설정 | ✅/❌/N/A | |

## 2. 보안
| 항목 | 상태 | 위치 |
|------|------|------|
| DOM 조작 API 사용 | ✅/❌ | |
| XSS 취약점 없음 | ✅/❌ | |

## 3. 코드 품질
| 항목 | 상태 | 위치 |
|------|------|------|
| 전역 app 미사용 | ✅/❌ | |
| 콘솔 로깅 제거 | ✅/❌ | |
| const/let 사용 | ✅/❌ | |
| async/await 사용 | ✅/❌ | |

## 4. 모바일 호환성
| 항목 | 상태 | 비고 |
|------|------|------|
| Node.js API 미사용 | ✅/❌ | |
| Electron API 미사용 | ✅/❌ | |
| isDesktopOnly 설정 | ✅/❌/N/A | |

## 5. UI/스타일링
| 항목 | 상태 | 위치 |
|------|------|------|
| HTML 헤딩 미사용 | ✅/❌ | |
| 인라인 스타일 미사용 | ✅/❌ | |
| CSS 변수 사용 | ✅/❌ | |

## 6. 리소스 관리
| 항목 | 상태 | 비고 |
|------|------|------|
| registerEvent 사용 | ✅/❌ | |
| 적절한 콜백 타입 | ✅/❌ | |

## 7. API 사용
| 항목 | 상태 | 위치 |
|------|------|------|
| getActiveViewOfType 사용 | ✅/❌ | |
| Vault API 우선 사용 | ✅/❌ | |
| normalizePath 사용 | ✅/❌ | |

## 8. 필수 파일
| 파일 | 상태 |
|------|------|
| README.md | ✅/❌ |
| LICENSE | ✅/❌ |
| manifest.json | ✅/❌ |

## 요약
- ✅ 통과: N개
- ❌ 수정 필요: N개
- ⚠️ 확인 필요: N개
```

## 수정 권장사항 예시

**DOM 조작**:
```typescript
// ❌ XSS 취약점
el.setHTML(userInput);

// ✅ 안전한 방법
const div = el.createDiv();
div.setText(userInput);
```

**파일 검색**:
```typescript
// ❌ 비효율적
const file = this.app.vault.getFiles().find(f => f.path === path);

// ✅ 효율적
const file = this.app.vault.getFileByPath(path);
```

**앱 인스턴스**:
```typescript
// ❌ 전역 사용 금지
window.app.vault.read(file);

// ✅ 인스턴스 사용
this.app.vault.read(file);
```
