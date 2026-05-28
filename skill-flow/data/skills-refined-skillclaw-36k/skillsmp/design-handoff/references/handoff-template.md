# Design Handoff Template

## Full Template Structure

```markdown
# Design Handoff: {컴포넌트명}

> 생성일: {YYYY-MM-DD}
> 작성자: {designer}
> 버전: {version}

## 1. 개요

### 목적
{이 컴포넌트가 해결하는 사용자 문제}

### 대상 사용자
{페르소나 또는 사용자 유형}

### 사용 맥락
{어디서, 언제 이 컴포넌트가 사용되는지}

## 2. 시각 스펙

### 레이아웃
\`\`\`
{ASCII 또는 구조 다이어그램}
\`\`\`

### 색상
| 요소 | 색상 | 토큰 |
|------|------|------|
| 배경 | #FFFFFF | --bg-primary |
| 텍스트 | #1F2937 | --text-primary |
| Primary 버튼 | #3B82F6 | --color-primary |
| 오류 | #EF4444 | --color-error |

### 타이포그래피
| 요소 | 폰트 | 크기 | 굵기 |
|------|------|------|------|
| 제목 | Inter | 24px | 600 |
| 레이블 | Inter | 14px | 500 |
| 입력 텍스트 | Inter | 16px | 400 |
| 에러 메시지 | Inter | 12px | 400 |

### 스페이싱
| 요소 | 값 |
|------|-----|
| 컨테이너 패딩 | 24px |
| 필드 간격 | 16px |
| 버튼 패딩 | 12px 24px |

### 테두리/그림자
| 요소 | 스타일 |
|------|--------|
| 입력 필드 | 1px solid #D1D5DB, radius 8px |
| 버튼 | radius 8px, shadow-sm |
| 컨테이너 | radius 12px, shadow-md |

## 3. 인터랙션

### 상태별 스타일
| 상태 | 변화 |
|------|------|
| Default | 기본 스타일 |
| Hover | 버튼 배경 어두워짐 (10%) |
| Focus | 2px ring, primary 색상 |
| Active | 버튼 배경 더 어두워짐 (15%) |
| Disabled | opacity 50%, cursor not-allowed |
| Error | 입력 border red, 에러 메시지 표시 |

### 애니메이션
| 트랜지션 | 속성 | 시간 |
|----------|------|------|
| 버튼 hover | background-color | 150ms ease |
| 포커스 링 | box-shadow | 150ms ease |
| 에러 메시지 | opacity, transform | 200ms ease-out |

### 사용자 흐름
\`\`\`
1. 이메일 입력 → 포커스 스타일
2. 비밀번호 입력 → 포커스 스타일
3. 제출 클릭 → 로딩 상태
4a. 성공 → 대시보드 이동
4b. 실패 → 에러 메시지 표시
\`\`\`

## 4. 반응형

### Desktop (≥1024px)
- 폼 너비: 400px, 중앙 정렬
- 큰 패딩, 여유로운 레이아웃

### Tablet (640px-1023px)
- 폼 너비: 90%, max 400px
- 패딩 유지

### Mobile (<640px)
- 폼 너비: 100%, padding 16px
- 세로 스택 레이아웃
- 터치 타겟 최소 44px

## 5. 접근성

### ARIA 속성
\`\`\`html
<form aria-labelledby="login-title">
  <input aria-describedby="email-error" aria-invalid="true/false">
  <button type="submit" aria-busy="true/false">
</form>
\`\`\`

### 키보드 탐색
- Tab: 순차 포커스 이동
- Enter: 폼 제출
- Escape: 모달 닫기 (해당 시)

### 스크린 리더
- 레이블과 입력 연결 필수
- 에러 메시지 aria-live="polite"
- 로딩 상태 aria-busy 업데이트

### 색상 대비
- 텍스트/배경: 4.5:1 이상
- 버튼 텍스트/배경: 4.5:1 이상

## 6. 에셋

### Figma
- 파일: {Figma 링크}
- 프레임: {프레임 이름}

### 목업 이미지
- Desktop: \`/assets/mockups/{component}-desktop.png\`
- Mobile: \`/assets/mockups/{component}-mobile.png\`

### 아이콘
| 이름 | 용도 | 소스 |
|------|------|------|
| eye | 비밀번호 표시 | lucide-react |
| eye-off | 비밀번호 숨김 | lucide-react |
| loader | 로딩 | lucide-react |

## 7. 구현 노트

### 기술 스택 권장
- React + TypeScript
- Tailwind CSS 또는 CSS Modules
- React Hook Form (폼 관리)
- Zod (유효성 검사)

### 주의사항
- {주의할 점 1}
- {주의할 점 2}

### 참조 컴포넌트
- \`@/components/ui/Button\`
- \`@/components/ui/Input\`
- \`@/components/ui/Label\`
```
