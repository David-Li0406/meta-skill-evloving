# Workflow Patterns

Skill 워크플로우 설계 패턴.

## Sequential Workflows

복잡한 작업은 순차적 단계로 분리:

```markdown
PDF 폼 작성 프로세스:

1. 폼 분석 (run analyze_form.py)
2. 필드 매핑 생성 (edit fields.json)
3. 매핑 검증 (run validate_fields.py)
4. 폼 작성 (run fill_form.py)
5. 출력 확인 (run verify_output.py)
```

## Conditional Workflows

분기 로직이 있는 작업:

```markdown
1. 작업 유형 결정:
   **새 콘텐츠 생성?** → "Creation workflow" 참조
   **기존 콘텐츠 수정?** → "Editing workflow" 참조

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```

## SEMO-Specific Patterns

### Agent-Skill 연동

```markdown
## Workflow

1. Agent가 Skill 호출 조건 감지
2. Skill 실행 및 결과 반환
3. Agent가 결과 기반 후속 작업 수행
```

### Multi-Package 작업

```markdown
## [po | next] 동시 작업

1. 대상 패키지 확인
2. 각 패키지에 동일 작업 수행
3. 결과 통합 및 검증
```
