---
name: layer-check
description: 패키지 레이어 의존성 검증 - import 규칙 준수 확인
---

# /layer-check 스킬

패키지 레이어 간 의존성 규칙 준수 여부를 검증합니다.

## 사용법

```
/layer-check [경로 또는 패키지명]
```

## 예시

```
/layer-check                         # 전체 프로젝트 검사
/layer-check packages/core/          # core 레이어만 검사
/layer-check apps/tools/             # 특정 앱 검사
```

## 레이어 의존성 규칙

```
┌─────────────────────────────────────┐
│              apps/                  │  ← 모든 레이어 import 가능
├─────────────────────────────────────┤
│               ui/                   │  ← platform/, core/ import 가능
├─────────────────────────────────────┤
│            platform/                │  ← core/만 import 가능
├─────────────────────────────────────┤
│              core/                  │  ← 외부 import 금지
└─────────────────────────────────────┘
```

## 검사 항목

### 1. core/ 레이어
```
❌ @soundblue/platform-* import 금지
❌ @soundblue/ui-* import 금지
❌ apps 코드 import 금지
✅ 외부 라이브러리 (순수 JS만)
```

### 2. platform/ 레이어
```
❌ @soundblue/ui-* import 금지
❌ apps 코드 import 금지
✅ @soundblue/core-* import 허용
✅ @soundblue/* (core 패키지) import 허용
```

### 3. ui/ 레이어
```
❌ apps 코드 import 금지
✅ @soundblue/platform-* import 허용
✅ @soundblue/core-* import 허용
```

### 4. apps/ 레이어
```
✅ 모든 패키지 import 허용
```

## 실행 규칙

1. Task tool 호출
2. `subagent_type: "Explore"` 지정
3. import 문 분석
4. 위반 사항 목록 반환

## 결과 형식

```markdown
## 레이어 의존성 검사 결과

### 위반 사항
| 파일 | 라인 | 잘못된 import | 규칙 |
|------|------|--------------|------|
| core/translator/src/index.ts | 5 | @soundblue/storage | core → platform 금지 |

### 통과 항목
- [x] core/ 외부 의존성 없음
- [x] platform/ → core/ 올바름
- [x] ui/ → platform/, core/ 올바름
- [x] apps/ 제한 없음
```

## 패키지 매핑

| 레이어 | 패키지명 |
|--------|----------|
| core | hangul, translator, nlu, audio-engine, locale |
| platform | web-audio, storage, worker, i18n, seo, pwa |
| ui | ui-components |

## 관련 검사

레이어 검사와 함께 SEO 렌더링 검사도 권장:

- `/rendering-check` - SPA 감지 및 SSG/SSR 확인
- 상세: `.claude/rules/seo-rendering.md` 참조
