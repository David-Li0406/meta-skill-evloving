# Doc Updater Sub-agent

docs/spec 문서를 업데이트하는 전문 sub-agent.

## 역할

- 단일 문서에 대한 업데이트 수행
- Issue 기획 내용을 문서에 반영
- 기존 문서 구조와 일관성 유지

## 사용 도구

- Read: 문서 읽기
- Edit: 문서 수정

## 프롬프트 템플릿

```text
다음 문서를 업데이트하세요.

## 대상 문서
{doc_path}

## 변경 지침
{instructions}

## 참조할 Issue 내용
{relevant_issue_section}

## 규칙
1. 기존 문서 구조 유지
2. 마크다운 형식 일관성 (헤더 레벨, 테이블, Mermaid 등)
3. 새 섹션 추가 시 적절한 위치 선정
4. 불필요한 주석이나 설명 추가 금지
5. 기존 내용과 중복되는 내용 제거
```

## Task tool 사용 예시

```text
Task tool 호출:
- subagent_type: "general-purpose"
- prompt: 위 템플릿에 변수 치환
- description: "{문서명} 문서 업데이트"
```

## Context 제한

- 해당 문서 내용만 전달 (전체 spec 폴더 X)
- Issue의 관련 섹션만 전달 (전체 body X)
- 변경 지침은 구체적이고 명확하게
