# Overview

## 프로젝트 구조

```
bungae/
├── packages/
│   └── bungae/              # 메인 번들러 패키지
│       ├── src/
│       │   ├── index.ts     # API 진입점
│       │   ├── cli.ts       # CLI 진입점
│       │   ├── config/      # 설정 로더
│       │   ├── resolver/    # 모듈 해석
│       │   ├── transformer/ # 코드 변환
│       │   ├── serializer/  # 번들 직렬화
│       │   ├── server/      # 개발 서버
│       │   ├── watcher/     # 파일 감시
│       │   ├── cache/       # 캐싱 시스템
│       │   └── runtime/     # 클라이언트 런타임
│       └── bunup.config.ts
├── reference/               # 참고 프로젝트
│   ├── metro/              # Metro 소스
│   └── rollipop/           # Rollipop 소스
└── .claude/skills/         # Claude 스킬 문서
```

## 핵심 설계 원칙

### 0. Bunup 사용 시 공식 문서 참조

**⚠️ 중요**: bunup 관련 작업(설정 파일 작성, 옵션 사용, 플러그인 개발 등)을 할 때는 **반드시** 공식 웹 스펙 문서를 참조하세요:

- **공식 문서**: https://bunup.dev/docs/guide/options.html
- bunup의 모든 옵션, 설정 방법, 플러그인 시스템은 공식 문서를 기준으로 사용해야 합니다.
- 프로젝트 내부 문서보다 공식 스펙 문서가 최신이고 정확합니다.

### 1. Bun 네이티브 우선

```typescript
// ✅ Good: Bun 내장 트랜스파일러 사용
const transpiler = new Bun.Transpiler({ loader: 'tsx' });
const result = transpiler.transformSync(code);

// ❌ Avoid: 불필요한 Babel 사용
const result = babel.transformSync(code, { presets: ['@babel/preset-typescript'] });
```

### 2. Metro 호환성

- 설정 파일 구조 유사하게 유지
- 번들 출력 형식 호환
- CLI 옵션 호환
- 기존 RN 프로젝트 마이그레이션 용이

### 3. 점진적 채택

Phase 1 → Phase 2 → Phase 3 → Phase 4 순서로 구현.
각 Phase가 독립적으로 동작 가능해야 함.

## CLI 명령어

```bash
bungae serve              # 개발 서버 시작
bungae build              # 프로덕션 빌드
bungae start              # serve 별칭

# 옵션
--platform ios|android    # 타겟 플랫폼
--dev                     # 개발 모드
--minify                  # 코드 압축
--entry <path>            # 진입점
--out-dir <path>          # 출력 디렉토리
--reset-cache             # 캐시 초기화
```

## 성능 목표

| 항목      | 목표                         |
| --------- | ---------------------------- |
| 초기 빌드 | Metro 대비 2-3배 빠름        |
| 증분 빌드 | 캐시 활용으로 단축           |
| 번들 크기 | Tree-shaking으로 10-20% 감소 |
| 메모리    | 대규모 프로젝트에서도 안정적 |
