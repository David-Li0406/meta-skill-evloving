# Output Format Reference

## 성공 출력

```markdown
## ✅ Epic 생성 완료

**이슈 번호**: #{issue_number}
**이슈 URL**: https://github.com/semicolon-devteam/docs/issues/{issue_number}
**도메인**: {domain_name}
**프로젝트**: 이슈관리 (연동 완료)

### 다음 단계

1. **Spec 초안 생성** (선택):
   > "Spec 초안도 작성해줘"

2. **개발자에게 전달**:
   - 개발자가 대상 레포에서 브랜치 생성
   - `/speckit.specify` 실행하여 spec.md 보완

3. **진행도 확인**:
   - [GitHub Projects 바로가기](https://github.com/orgs/semicolon-devteam/projects/1)
```

## 에러 처리

### 권한 오류

```markdown
[SEMO] Error: create-epic 실패 → GitHub API 권한 없음

⚠️ docs 레포지토리에 Issue 생성 권한이 필요합니다.
```

### 중복 Epic

```markdown
[SEMO] Warning: 유사한 Epic이 존재합니다

기존 Epic: #{existing_number} - {existing_title}

- 새로 생성하려면: "그래도 생성해줘"
- 기존 Epic 사용: "기존 Epic 사용할게"
```
