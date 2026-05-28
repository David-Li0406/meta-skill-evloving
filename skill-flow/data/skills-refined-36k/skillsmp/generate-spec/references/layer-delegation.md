# Layer Delegation Reference

> Epic에서 Task로 정보를 위임할 때 Layer별 규칙

## Layer별 정보 위임 매트릭스

### Dev Checklist 위임

| Layer | 데이터 흐름 | 시간/계산 | 플랫폼 제약 | 도메인 지식 | 엣지 케이스 |
|-------|------------|----------|-----------|-----------|-----------|
| CONFIG | - | - | - | - | - |
| PROJECT | - | - | - | - | - |
| DATA | ✅ | ✅ | - | - | - |
| TESTS | - | - | - | - | ✅ |
| CODE | - | - | ✅ | ✅ | - |

### Constraints 위임

| Layer | 기술적.의존성 | 기술적.아키텍처 | 기술적.데이터 | 기술적.플랫폼 |
|-------|-------------|---------------|-------------|-------------|
| CONFIG | ✅ | - | - | - |
| PROJECT | - | ✅ | - | - |
| DATA | - | - | ✅ | - |
| TESTS | - | - | - | - |
| CODE | - | - | - | ✅ |

## 위임 예시

### CONFIG Layer (v0.1.x)

```markdown
## ⚠️ Constraints
### 기술적 제약
- Node.js 20.x 이상 필수
- pnpm 워크스페이스 사용
```

### DATA Layer (v0.3.x)

```markdown
## ⚠️ Constraints
### 기술적 제약
- Supabase PostgreSQL 사용
- RLS 정책 필수

### 개발자 체크리스트
#### 데이터 흐름
- [ ] 동시 수정 시 충돌 해결: last-write-wins
- [ ] 멀티플랫폼 동기화: Realtime subscription
- [ ] 삭제 정책: soft delete

#### 시간/계산
- [ ] 집계 기준: UTC 기준 일별
- [ ] 타임존: Asia/Seoul 표시
```

### CODE Layer (v0.5.x)

```markdown
## ⚠️ Constraints
### 기술적 제약
- PWA 오프라인 지원 불가
- iOS Safari 제한사항 적용

### 개발자 체크리스트
#### 플랫폼 제약
- [ ] PWA Push Notification 미지원 → Polling 대안
- [ ] iOS Safari localStorage 제한 → IndexedDB 사용

#### 도메인 지식
- [ ] 업계 표준: ISO 8601 날짜 포맷
- [ ] 엣지 케이스: 윤년, DST 전환
```

## 위임 로직

```javascript
function delegateToTask(epicBody, layer) {
  const delegation = {
    devChecklist: [],
    constraints: []
  };

  switch (layer) {
    case 'CONFIG':
      delegation.constraints = extractConstraints(epicBody, '의존성');
      break;
    case 'PROJECT':
      delegation.constraints = extractConstraints(epicBody, '아키텍처');
      break;
    case 'DATA':
      delegation.devChecklist = extractDevChecklist(epicBody, ['데이터 흐름', '시간/계산']);
      delegation.constraints = extractConstraints(epicBody, '데이터');
      break;
    case 'TESTS':
      delegation.devChecklist = extractDevChecklist(epicBody, ['엣지 케이스']);
      break;
    case 'CODE':
      delegation.devChecklist = extractDevChecklist(epicBody, ['플랫폼 제약', '도메인 지식']);
      delegation.constraints = extractConstraints(epicBody, '플랫폼');
      break;
  }

  return delegation;
}
```
