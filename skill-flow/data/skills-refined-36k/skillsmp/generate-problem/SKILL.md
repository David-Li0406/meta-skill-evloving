---
name: generate-problem
description: Generate SQL practice problems using Gemini AI. Use when creating new problems, testing problem generation, or when user mentions "문제 생성", "generate problem", "내일 문제 뽑아줘".
---

# Generate Problem

Gemini 2.0 Flash를 사용하여 QueryCraft의 현실적인 SQL 연습 문제를 생성합니다.

## Instructions

1. **태스크 실행**:
   - `scripts/run_task.py`를 사용하여 문제를 생성합니다.
   
   - **PA 문제 생성 (기본)**:
     ```bash
     python scripts/run_task.py gen-pa --date YYYY-MM-DD
     ```
   
   - **Stream 문제 생성**:
     ```bash
     python scripts/run_task.py gen-stream --date YYYY-MM-DD
     ```

2. **파라미터 가이드**:
   - `--date`: 문제를 생성할 대상 날짜 (예: 2026-01-18). 생략 시 오늘 날짜 기준.
   - `--mode`: PA 문제의 경우 산업군을 지정할 수 있습니다 (`commerce`, `saas`, `content`, `community`, `fintech`).

3. **결과 확인**:
   - 생성된 파일: `problems/monthly/` 디렉토리에 JSON 형식으로 누적 저장됩니다.
   - 데이터베이스: PostgreSQL `public.problems` 테이블 및 `grading` 스키마에 자동으로 반영됩니다.

## Key Files

- `scripts/run_task.py`: 통합 실행 스크립트
- `problems/generator.py`: PA 문제 생성 핵심 로직
- `problems/generator_stream.py`: Stream 문제 생성 핵심 로직
- `problems/prompt_pa.py`: PA 문제 생성 프롬프트 템플릿

## Best Practices

- 특정 날짜를 언급하지 않으면 "내일 날짜"를 기본으로 설정하는 것이 좋습니다.
- 문제 생성 후 "생성된 문제를 확인했습니다"와 함께 간단한 문제 요약을 제공하세요.
