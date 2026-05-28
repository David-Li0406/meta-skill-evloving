---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".
argument-hint: <file-or-pattern>
---

# 웹 인터페이스 디자인 가이드라인 (Web Interface Guidelines)

웹 인터페이스 가이드라인 준수 여부를 확인하기 위해 파일을 리뷰합니다.

## 작동 방식 (How It Works)

1. 로컬에 저장된 가이드라인 파일(`rules.md`)을 읽습니다.
2. 지정된 소스 파일을 읽습니다 (또는 사용자에게 파일/패턴을 묻습니다).
3. 가이드라인의 모든 규칙과 대조하여 검사합니다.
4. 발견된 사항을 간결한 `file:line` 형식으로 출력합니다.

## 가이드라인 원본 (Guidelines Source)

로컬 가이드라인 파일을 참조합니다:

```
.agent/skills/web-design-guidelines/rules.md
```

<!-- 
최신 버전 업데이트 시 아래 URL에서 내용을 다운로드 받아 rules.md에 덮어쓰세요:
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md 
-->

이 파일에는 모든 디자인/접근성 규칙과 출력 형식 지침이 포함되어 있습니다.

## 사용법 (Usage)

사용자가 파일이나 패턴 인수를 제공하는 경우:
1. `rules.md` 파일을 읽어서 숙지합니다.
2. 사용자가 지정한 소스 파일을 읽습니다.
3. 모든 규칙을 적용하여 코드를 분석합니다.
4. 가이드라인에 지정된 형식을 사용하여 발견된 내용을 출력합니다.

파일이 지정되지 않은 경우, 사용자에게 어떤 파일을 리뷰할지 물어보세요.
