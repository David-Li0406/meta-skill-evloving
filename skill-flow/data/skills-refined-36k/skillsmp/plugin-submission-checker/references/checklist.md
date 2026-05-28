# Obsidian 플러그인 제출 체크리스트

이 문서는 Obsidian 커뮤니티 플러그인 제출 시 필요한 요구사항과 가이드라인을 체크리스트로 정리한 것입니다.

> **참고 문서:**
> - [Submission requirements for plugins](https://docs.obsidian.md/Plugins/Releasing/Submission+requirements+for+plugins)
> - [Plugin guidelines](https://docs.obsidian.md/Plugins/Releasing/Plugin+guidelines)

---

## 1. 필수 요구사항 (Submission Requirements)

### 1.1 Manifest 설정

- [ ] `fundingUrl`은 Buy Me A Coffee, GitHub Sponsors 등 금전적 후원 서비스 링크만 사용
- [ ] 후원을 받지 않는 경우 `fundingUrl` 제거
- [ ] `minAppVersion`을 플러그인이 호환되는 최소 Obsidian 버전으로 설정
- [ ] 적절한 버전을 모르는 경우 최신 안정 빌드 번호 사용

### 1.2 플러그인 설명

- [ ] 설명은 최대 250자 이내
- [ ] 설명은 마침표(`.`)로 끝남
- [ ] "Translate selected text into...", "Generate notes automatically from..." 등 동작 문장으로 시작
- [ ] "This is a plugin"으로 시작하지 않음
- [ ] 이모지나 특수문자 사용 금지
- [ ] 약어, 고유명사, 상표 올바르게 대문자 사용 (예: "Obsidian", "Markdown", "PDF")
- [ ] [Obsidian 스타일 가이드](https://help.obsidian.md/Contributing+to+Obsidian/Style+guide) 준수

### 1.3 데스크톱 전용 API

- [ ] Node.js 또는 Electron API 사용 시 `manifest.json`에서 `isDesktopOnly`를 `true`로 설정
- [ ] 가능하면 Web API 대안 사용:
  - `SubtleCrypto` (crypto 대신)
  - `navigator.clipboard.readText()`/`writeText()` (클립보드 접근)

### 1.4 명령어 ID

- [ ] 명령어 ID에 플러그인 ID를 수동으로 포함하지 않음 (Obsidian이 자동으로 접두사 추가)

### 1.5 샘플 코드

- [ ] 샘플 플러그인의 모든 예제 코드 제거

---

## 2. 일반 가이드라인 (General)

### 2.1 앱 인스턴스

- [ ] 전역 `app` 또는 `window.app` 객체 사용 금지
- [ ] 대신 `this.app` 사용

### 2.2 콘솔 로깅

- [ ] 불필요한 콘솔 로깅 제거
- [ ] 기본 설정에서 개발자 콘솔에 에러 메시지만 표시

### 2.3 코드 구조

- [ ] 여러 `.ts` 파일 사용 시 폴더로 정리
- [ ] 플레이스홀더 클래스명(`MyPlugin`, `MyPluginSettings`, `SampleSettingTab`) 변경

---

## 3. 모바일 호환성 (Mobile)

- [ ] Node.js 및 Electron API 모바일 미지원 확인
- [ ] 정규식에서 lookbehind 패턴 사용 시 모바일 호환성 주의

---

## 4. UI 텍스트 (UI Text)

### 4.1 대소문자

- [ ] UI 텍스트에 Sentence case 사용 (Title Case 아님)
  - ✅ "Template folder location"
  - ❌ "Template Folder Location"
  - ✅ "Create new note"
  - ❌ "Create New Note"

### 4.2 설정 헤딩

- [ ] 설정 탭에 최상위 헤딩("General", "Settings", 플러그인 이름) 추가 금지
- [ ] 여러 섹션이 있는 경우에만 헤딩 사용
- [ ] 일반 설정은 헤딩 없이 상단에 배치
- [ ] 헤딩에 "settings" 단어 포함 금지
  - ✅ "Advanced"
  - ❌ "Advanced settings"
  - ✅ "Templates"
  - ❌ "Settings for templates"

### 4.3 헤딩 요소

- [ ] HTML 헤딩 요소(`<h1>`, `<h2>`) 대신 `setHeading()` 사용
```ts
new Setting(containerEl).setName('your heading title').setHeading();
```

---

## 5. 보안 (Security)

- [ ] `innerHTML` 사용 금지
- [ ] `outerHTML` 사용 금지
- [ ] `insertAdjacentHTML` 사용 금지
- [ ] DOM API 또는 Obsidian 헬퍼 함수 사용:
  - `createEl()`
  - `createDiv()`
  - `createSpan()`
- [ ] HTML 요소 내용 정리 시 `el.empty()` 사용

---

## 6. 리소스 관리 (Resource Management)

### 6.1 리소스 정리

- [ ] 플러그인 언로드 시 모든 리소스(이벤트 리스너 등) 정리
- [ ] 자동 정리를 위해 `registerEvent()` 또는 `addCommand()` 사용
```ts
export default class MyPlugin extends Plugin {
  onload() {
    this.registerEvent(this.app.vault.on('create', this.onCreate));
  }
}
```

### 6.2 Leaf 관리

- [ ] `onunload`에서 leaf를 detach하지 않음 (업데이트 시 위치 유지를 위해)

---

## 7. 명령어 (Commands)

- [ ] 명령어에 기본 단축키 설정하지 않음 (충돌 방지)
- [ ] 적절한 콜백 타입 사용:
  - `callback`: 무조건 실행되는 명령어
  - `checkCallback`: 특정 조건에서만 실행되는 명령어
  - `editorCallback`/`editorCheckCallback`: 활성 마크다운 에디터 필요 시

---

## 8. 워크스페이스 (Workspace)

### 8.1 활성 뷰 접근

- [ ] `workspace.activeLeaf` 직접 접근 금지
- [ ] 대신 `getActiveViewOfType()` 사용
```ts
const view = this.app.workspace.getActiveViewOfType(MarkdownView);
if (view) {
  // ...
}
```

### 8.2 에디터 접근

- [ ] 활성 노트의 에디터는 `activeEditor` 사용
```ts
const editor = this.app.workspace.activeEditor?.editor;
```

### 8.3 커스텀 뷰 참조

- [ ] 커스텀 뷰 참조 저장 금지 (메모리 누수 방지)
```ts
// ❌ 하지 마세요
this.registerView(MY_VIEW_TYPE, () => this.view = new MyCustomView());

// ✅ 이렇게 하세요
this.registerView(MY_VIEW_TYPE, () => new MyCustomView());
```
- [ ] 뷰 접근 시 `Workspace.getActiveLeavesOfType()` 사용

---

## 9. Vault (파일 시스템)

### 9.1 파일 수정

- [ ] 활성 파일 편집 시 `Vault.modify()` 대신 Editor API 사용
- [ ] 백그라운드 파일 수정 시 `Vault.process()` 사용 (원자적 수정)
- [ ] 프론트매터 수정 시 `FileManager.processFrontMatter()` 사용

### 9.2 API 선택

- [ ] Adapter API(`app.vault.adapter`) 대신 Vault API(`app.vault`) 선호
  - 캐싱 레이어로 성능 향상
  - 직렬 파일 작업으로 경쟁 조건 방지

### 9.3 파일 검색

- [ ] 경로로 파일 찾을 때 모든 파일 반복 금지
```ts
// ❌ 하지 마세요
this.app.vault.getFiles().find(file => file.path === filePath);

// ✅ 이렇게 하세요
const file = this.app.vault.getFileByPath(filePath);
const folder = this.app.vault.getFolderByPath(folderPath);
const abstractFile = this.app.vault.getAbstractFileByPath(filePath);
```

### 9.4 경로 정규화

- [ ] 사용자 정의 경로에 `normalizePath()` 사용
```ts
import { normalizePath } from 'obsidian';
const pathToPlugin = normalizePath('//my-folder\file');
// 결과: "my-folder/file"
```

---

## 10. 에디터 (Editor)

- [ ] 에디터 확장 재구성 시 `updateOptions()` 사용
```ts
this.app.workspace.updateOptions();
```

---

## 11. 스타일링 (Styling)

- [ ] 하드코딩된 인라인 스타일 금지
```ts
// ❌ 하지 마세요
el.style.color = 'white';
el.style.backgroundColor = 'red';

// ✅ 이렇게 하세요
const el = containerEl.createDiv({cls: 'warning-container'});
```
- [ ] CSS 클래스 사용
- [ ] Obsidian CSS 변수 사용
```css
.warning-container {
  color: var(--text-normal);
  background-color: var(--background-modifier-error);
}
```

---

## 12. TypeScript 코드 스타일

- [ ] `var` 대신 `const`와 `let` 사용
- [ ] Promise 체인 대신 `async`/`await` 사용
```ts
// ❌ 하지 마세요
function test(): Promise<string | null> {
  return requestUrl('https://example.com')
    .then(res => res.text)
    .catch(e => {
      console.log(e);
      return null;
    });
}

// ✅ 이렇게 하세요
async function asyncTest(): Promise<string | null> {
  try {
    let res = await requestUrl('https://example.com');
    let text = await res.text;
    return text;
  } catch (e) {
    console.log(e);
    return null;
  }
}
```

---

## 제출 전 최종 체크

- [ ] 모든 필수 요구사항 충족
- [ ] [Developer policies](https://docs.obsidian.md/Developer+policies) 검토
- [ ] 플러그인 테스트 완료 (데스크톱 및 모바일)
- [ ] README.md 작성
- [ ] CHANGELOG.md 또는 릴리스 노트 작성
- [ ] 라이선스 파일 포함
