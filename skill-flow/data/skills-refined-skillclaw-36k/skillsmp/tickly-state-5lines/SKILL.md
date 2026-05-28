---
name: tickly-state-5lines
description: Tickly 작업 시작/재개할 때 현재 상태를 5줄로 고정 요약한다. "Tickly 상태 요약", "오늘 뭐부터?", "진행상황 정리" 같은 요청에 사용한다.
---

# Tickly 상태 스냅샷 (5줄)

## 출력(반드시 5줄, 줄 수 엄수)
1) Goal:
2) Now:
3) Constraints:
4) Today (1 task):
5) Next:

## 규칙
- 각 줄 120자 이내.
- Today는 반드시 1개 작업만(목록 금지).
- 정보가 부족하면 질문은 최대 2개만 하고, 그래도 5줄 출력은 한다(빈칸은 TBD).
