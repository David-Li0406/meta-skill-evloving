# Bunup 가이드

Bungae 프로젝트에서 사용하는 빌드 도구인 bunup에 대한 가이드.

## ⚠️ 중요: 공식 문서 참조 필수

**bunup 관련 작업을 할 때는 반드시 공식 웹 스펙 문서를 참조하세요:**

- **공식 문서**: https://bunup.dev/docs/guide/options.html
- bunup의 모든 옵션, 설정 방법, 플러그인 시스템은 공식 문서를 기준으로 사용해야 합니다.
- 프로젝트 내부 문서보다 공식 스펙 문서가 최신이고 정확합니다.

## Bunup이란?

Bunup은 Bun의 네이티브 번들러 기능과 oxc 컴파일러를 사용하여 TypeScript/JavaScript 라이브러리를 빌드하는 도구입니다.

### 주요 특징

- **빠른 빌드**: Bun의 네이티브 성능 활용
- **TypeScript 지원**: 타입 선언 파일(.d.ts) 자동 생성
- **다중 포맷**: ESM, CJS, IIFE 지원
- **플러그인 시스템**: 확장 가능한 빌드 파이프라인

## 기본 사용법

### 설정 파일

`bunup.config.ts` 파일을 프로젝트 루트에 생성:

```typescript
import { defineConfig } from 'bunup';

export default defineConfig({
  entry: ['src/index.ts', 'src/cli.ts'],
  outDir: 'dist',
  format: ['esm', 'cjs'],
  dts: true,
  clean: true,
  sourcemap: 'linked',
  target: 'node',
  external: ['react-native'],
});
```

### 주요 옵션

자세한 옵션은 **공식 문서**를 참조하세요: https://bunup.dev/docs/guide/options.html

- `entry`: 진입점 파일 경로
- `outDir`: 출력 디렉토리
- `format`: 출력 포맷 (esm, cjs, iife)
- `dts`: TypeScript 선언 파일 생성 여부
- `target`: 타겟 환경 (node, browser, bun)
- `external`: 번들에서 제외할 패키지

## 참고 자료

- **공식 문서**: https://bunup.dev/docs/guide/options.html
- **프로그래밍 방식 사용**: https://bunup.dev/docs/advanced/programmatic-usage
- **플러그인 개발**: https://bunup.dev/docs/advanced/plugin-development
