# Frontend Stack & Conventions

> 이코에코 프론트엔드 기술 스택, 코드 컨벤션, Git 규칙, 배포 가이드

## 1. 기술 스택

### Core
| 기술 | 버전 | 설명 |
|------|------|------|
| React | 19.1.1 | UI 라이브러리 |
| TypeScript | 5.9.3 | 타입 시스템 (Strict 모드) |
| Vite | 7.1.7 | 번들러 & 개발 서버 |

### 상태 관리 & 데이터 페칭
| 기술 | 버전 | 설명 |
|------|------|------|
| React Query | 5.90.11 | 서버 상태 관리 |
| Axios | 1.13.2 | HTTP 클라이언트 |

### 스타일링
| 기술 | 버전 | 설명 |
|------|------|------|
| TailwindCSS | 4.1.16 | 유틸리티 CSS |
| Framer Motion | 12.23.24 | 애니메이션 |
| Lucide React | 0.554.0 | 아이콘 |

### 개발 도구
| 기술 | 버전 | 설명 |
|------|------|------|
| ESLint | 9.38.0 | Flat Config |
| Prettier | 3.6.2 | 코드 포매터 |
| Husky | 9.1.7 | Git Hooks |
| Yarn | 4.9.2 | 패키지 매니저 |

---

## 2. 코드 컨벤션

### TypeScript 설정
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "paths": { "@/*": ["./src/*"] }
  }
}
```

### Prettier 설정
```javascript
{
  semi: true,
  singleQuote: true,
  trailingComma: 'all',
  tabWidth: 2,
  printWidth: 80,
  jsxSingleQuote: true,
  plugins: ['prettier-plugin-tailwindcss']
}
```

### 파일 네이밍
| 유형 | 컨벤션 | 예시 |
|------|--------|------|
| 컴포넌트 | PascalCase | `AgentContainer.tsx` |
| 훅 | camelCase + use 접두사 | `useAgentSSE.ts` |
| 타입 | PascalCase | `AgentTypes.ts` |
| 서비스 | kebab-case + .service | `agent.service.ts` |
| 쿼리 | kebab-case + .queries | `agent.queries.ts` |

### Import 순서
```typescript
// 1. React & 외부 라이브러리
import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';

// 2. 내부 컴포넌트
import { AgentSidebar } from '@/components/agent';

// 3. 훅
import { useAgentSSE } from '@/hooks/agent/useAgentSSE';

// 4. 서비스 & 타입
import { AgentService } from '@/api/services/agent/agent.service';
import type { ChatSummary } from '@/api/services/agent/agent.type';

// 5. 상수 & 유틸
import { AGENT_CONFIG } from '@/constants/AgentConfig';
```

---

## 3. Git 규칙

### 브랜치 네이밍
```
{prefix}/{기능설명}/{이름}
```

**허용된 Prefix:**
| Prefix | 용도 |
|--------|------|
| `feat/` | 새로운 기능 |
| `fix/` | 버그 수정 |
| `refactor/` | 리팩토링 |
| `style/` | 스타일/포맷 변경 |
| `chore/` | 기타 변경사항 |

**예시:**
```
feat/agent_sse_streaming/suji_chae
fix/token_recovery_bug/chaehyun_kim
```

### 커밋 메시지
Husky가 브랜치 prefix를 자동으로 커밋 메시지에 추가:

```bash
# 브랜치: feat/agent_sidebar/suji_chae
git commit -m "Add chat list pagination"
# 결과: [feat] Add chat list pagination
```

### Pre-commit Hook
```bash
# .husky/pre-commit
bash check-branch.sh  # 브랜치명 검증
```

---

## 4. 배포

### Vercel (주 배포)
```
main 브랜치 push → Vercel 자동 배포
```

**환경 변수 (Vercel Dashboard):**
```env
VITE_API_URL=https://api.dev.growbin.app
VITE_KAKAO_APP_KEY=your_kakao_app_key
```

### 빌드 스크립트
```bash
yarn build        # tsc -b && vite build
yarn preview      # 빌드 결과 미리보기
```

### PWA 설정
```javascript
// vite.config.ts
VitePWA({
  registerType: 'autoUpdate',
  manifest: {
    name: '이코에코',
    short_name: '이코에코',
    theme_color: '#ffffff',
    display: 'fullscreen',
  },
})
```

---

## 5. React Query 설정

```typescript
// providers/QueryClientProvider.tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 3 * 60 * 1000,  // 3분
      retry: false,
      refetchOnWindowFocus: false,
    },
  },
});
```

---

## 6. Axios 설정

```typescript
// api/axiosInstance.ts
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,  // 쿠키 포함
});

// 401 에러: 토큰 갱신 후 재시도
// 403 에러: 로그아웃 + 로그인 리디렉트
```

---

## 7. 글로벌 스타일

```css
/* style/global.css */
:root {
  --brand-primary: #569f87;
  --brand-secondary: #f0fdf4;
  --text-primary: #1a1a1a;
  --text-secondary: #666666;
  --max-width: 480px;
  --bottom-bar-height: 83px;
  --top-bar-height: 60px;
}
```

---

## 8. 라우팅

```typescript
// App.tsx
<HashRouter>
  <Routes>
    <Route element={<AppLayout />}>
      <Route path="/home" element={<Home />} />
      <Route path="/chat" element={<Chat />} />
      <Route path="/agent" element={<Agent />} />  {/* 새로 추가 */}
      {/* ... */}
    </Route>
  </Routes>
</HashRouter>
```

**HashRouter 사용 이유:** GitHub Pages 호환성
