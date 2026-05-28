#!/usr/bin/env python3
"""
Task Planner - 작업 계획 자동 생성 및 촘촘함 강제

목적:
- 사용자 요청을 2-3배 더 세분화된 작업 계획으로 분해
- 작업 간 종속성 분석
- 계획의 완전성 검증
- TodoWrite 형식으로 출력

사용:
    python3 task_planner.py "스킬 3개 수정" --detail-level 3
    python3 task_planner.py --from-file plan.md --validate
"""

import argparse
import json
import sys
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Task:
    """작업 단위"""

    id: str
    content: str
    activeForm: str
    status: str = "pending"
    dependencies: List[str] = field(default_factory=list)
    estimated_subtasks: int = 1
    tier: int = 0  # 작업 계층 (0=최상위)
    parent: Optional[str] = None


@dataclass
class TaskPlan:
    """전체 작업 계획"""

    goal: str
    tasks: List[Task] = field(default_factory=list)
    detail_level: int = 2  # 1=낮음, 2=보통, 3=높음 (2-3배 세분화)
    issues: List[str] = field(default_factory=list)


class TaskPlanner:
    """작업 계획 생성기"""

    def __init__(self, detail_level: int = 2):
        """
        Args:
            detail_level: 세분화 수준 (1-3)
                1: 최소 분해
                2: 표준 분해 (2배)
                3: 최대 분해 (3배)
        """
        self.detail_level = detail_level
        self.task_counter = 0

    def generate_task_id(self) -> str:
        """작업 ID 생성"""
        self.task_counter += 1
        return f"T{self.task_counter:03d}"

    def decompose_goal(self, goal: str) -> TaskPlan:
        """
        목표를 세분화된 작업 계획으로 분해

        분해 원칙:
        1. 큰 작업 → 작은 작업들로 분해
        2. 각 작업은 명확한 완료 조건 가짐
        3. 작업 간 종속성 명시
        4. 검증 가능한 단위로 분해

        Args:
            goal: 최종 목표

        Returns:
            작업 계획
        """
        plan = TaskPlan(goal=goal, detail_level=self.detail_level)

        # 목표 분석 및 초기 작업 추출
        initial_tasks = self._extract_initial_tasks(goal)

        # 각 초기 작업을 세분화
        for task_desc in initial_tasks:
            subtasks = self._decompose_task(task_desc, tier=0)
            plan.tasks.extend(subtasks)

        # 종속성 분석
        self._analyze_dependencies(plan)

        # 계획 완전성 검증
        plan.issues = self._validate_plan(plan)

        return plan

    def _extract_initial_tasks(self, goal: str) -> List[str]:
        """
        목표로부터 초기 작업 목록 추출

        휴리스틱:
        - "스킬 N개 수정" → N개 스킬별 작업 생성
        - "구현" → 설계/구현/테스트 단계 생성
        - "수정" → 분석/수정/검증 단계 생성
        """
        tasks = []

        # 숫자 패턴 감지 (예: "스킬 3개 수정")
        import re

        number_match = re.search(r"^(.*?)(\d+)개\\s*(.*)$", goal)
        if number_match:
            count = int(number_match.group(2))
            prefix = number_match.group(1).strip()
            suffix = number_match.group(3).strip()
            base = " ".join([p for p in [prefix, suffix] if p]).strip()
            if not base:
                base = goal.replace(f"{count}개", "").strip()
            for i in range(1, count + 1):
                tasks.append(f"{base} #{i}" if base else f"작업 #{i}")
            return tasks

        # 키워드 기반 단계 생성
        if "구현" in goal or "개발" in goal:
            tasks = [
                f"{goal} - 요구사항 분석",
                f"{goal} - 설계",
                f"{goal} - 구현",
                f"{goal} - 단위 테스트",
                f"{goal} - 통합 테스트",
                f"{goal} - 문서화",
            ]
        elif "수정" in goal or "고침" in goal:
            tasks = [
                f"{goal} - 현황 분석",
                f"{goal} - 수정 실행",
                f"{goal} - 결과 검증",
            ]
        else:
            # 기본: 목표 자체를 작업으로
            tasks = [goal]

        return tasks

    def _decompose_task(self, task_desc: str, tier: int, parent: Optional[str] = None) -> List[Task]:
        """
        작업을 세부 작업으로 분해

        detail_level에 따라 분해 깊이 조정:
        - level 1: 1단계 분해 (Tier 0만)
        - level 2: 2단계 분해 (Tier 0-1)
        - level 3: 3단계 분해 (Tier 0-2)
        """
        task_id = self.generate_task_id()
        task = Task(
            id=task_id,
            content=task_desc,
            activeForm=self._to_active_form(task_desc),
            tier=tier,
            parent=parent,
        )
        tasks = [task]

        # 분해 종료 조건: tier가 detail_level에 도달하면 더 이상 분해하지 않음
        if tier >= self.detail_level:
            return tasks

        # 작업 유형에 따라 하위 작업 목록 생성
        if "분석" in task_desc:
            subtasks = self._decompose_analysis(task_desc, tier)
        elif "설계" in task_desc:
            subtasks = self._decompose_design(task_desc, tier)
        elif "구현" in task_desc or "실행" in task_desc:
            subtasks = self._decompose_implementation(task_desc, tier)
        elif "테스트" in task_desc or "검증" in task_desc:
            subtasks = self._decompose_testing(task_desc, tier)
        else:
            # 일반 작업: 기본 3단계 분해
            subtasks = [
                f"{task_desc} - 준비",
                f"{task_desc} - 실행",
                f"{task_desc} - 완료 확인",
            ]

        # 각 subtask를 재귀적으로 분해
        for st_desc in subtasks:
            tasks.extend(self._decompose_task(st_desc, tier + 1, parent=task_id))

        return tasks

    def _decompose_analysis(self, task_desc: str, tier: int) -> List[str]:
        """분석 작업 세분화"""
        base = task_desc.replace(" - 현황 분석", "").replace(" - 요구사항 분석", "")
        return [
            f"{base} - 파일 목록 확인",
            f"{base} - 현재 구조 파악",
            f"{base} - 문제점 식별",
            f"{base} - 수정 범위 결정",
        ]

    def _decompose_design(self, task_desc: str, tier: int) -> List[str]:
        """설계 작업 세분화"""
        base = task_desc.replace(" - 설계", "")
        return [
            f"{base} - 인터페이스 설계",
            f"{base} - 데이터 구조 설계",
            f"{base} - 알고리즘 설계",
            f"{base} - 설계 검토",
        ]

    def _decompose_implementation(self, task_desc: str, tier: int) -> List[str]:
        """구현 작업 세분화"""
        base = task_desc.replace(" - 구현", "").replace(" - 실행", "").replace(" - 수정 실행", "")
        return [
            f"{base} - 코드 작성",
            f"{base} - 린트 검사",
            f"{base} - 로컬 테스트",
            f"{base} - 커밋 준비",
        ]

    def _decompose_testing(self, task_desc: str, tier: int) -> List[str]:
        """테스트 작업 세분화"""
        base = (
            task_desc.replace(" - 단위 테스트", "")
            .replace(" - 통합 테스트", "")
            .replace(" - 검증", "")
            .replace(" - 결과 검증", "")
        )
        return [
            f"{base} - 테스트 케이스 작성",
            f"{base} - 테스트 실행",
            f"{base} - 결과 분석",
            f"{base} - 수정 사항 반영",
        ]

    def _to_active_form(self, content: str) -> str:
        """명령형 → 진행형 변환"""
        # 간단한 규칙 기반 변환
        if content.endswith("준비"):
            return content.replace("준비", "준비 중")
        elif content.endswith("실행"):
            return content.replace("실행", "실행 중")
        elif content.endswith("확인"):
            return content.replace("확인", "확인 중")
        elif content.endswith("작성"):
            return content.replace("작성", "작성 중")
        elif content.endswith("분석"):
            return content.replace("분석", "분석 중")
        elif content.endswith("설계"):
            return content.replace("설계", "설계 중")
        elif content.endswith("검증"):
            return content.replace("검증", "검증 중")
        else:
            return content + " 중"

    def _analyze_dependencies(self, plan: TaskPlan):
        """작업 간 종속성 분석"""
        # 부모-자식 + 형제 순서 종속성
        groups = {}
        for task in plan.tasks:
            if task.parent and task.parent not in task.dependencies:
                task.dependencies.append(task.parent)

            key = (task.parent, task.tier)
            if key not in groups:
                groups[key] = []
            groups[key].append(task)

        for tasks in groups.values():
            for i in range(1, len(tasks)):
                prev_id = tasks[i - 1].id
                if prev_id not in tasks[i].dependencies:
                    tasks[i].dependencies.append(prev_id)

    def _validate_plan(self, plan: TaskPlan) -> List[str]:
        """계획 완전성 검증"""
        issues = []

        # 1. 최소 작업 수 검증
        min_tasks = 3 * plan.detail_level
        if len(plan.tasks) < min_tasks:
            issues.append(f"작업 수 부족: {len(plan.tasks)}개 (최소 {min_tasks}개 필요)")

        # 2. 순환 종속성 검증
        if self._has_circular_dependency(plan.tasks):
            issues.append("순환 종속성 감지")

        # 3. 작업 계층 구조 검증
        tiers = set(t.tier for t in plan.tasks)
        expected_tiers = plan.detail_level + 1  # tier는 0부터 시작하므로 +1
        if len(tiers) < expected_tiers:
            issues.append(f"계층 구조 부족: {len(tiers)}단계 (최소 {expected_tiers}단계 권장)")

        return issues

    def _has_circular_dependency(self, tasks: List[Task]) -> bool:
        """순환 종속성 검사 (DFS)"""
        visited = set()
        rec_stack = set()

        def dfs(task_id: str) -> bool:
            visited.add(task_id)
            rec_stack.add(task_id)

            task = next((t for t in tasks if t.id == task_id), None)
            if task:
                for dep_id in task.dependencies:
                    if dep_id not in visited:
                        if dfs(dep_id):
                            return True
                    elif dep_id in rec_stack:
                        return True

            rec_stack.remove(task_id)
            return False

        for task in tasks:
            if task.id not in visited:
                if dfs(task.id):
                    return True

        return False

    def export_todowrite_format(self, plan: TaskPlan) -> List[Dict]:
        """TodoWrite 형식으로 출력"""
        todos = []
        for task in plan.tasks:
            todos.append(
                {
                    "content": task.content,
                    "status": task.status,
                    "activeForm": task.activeForm,
                }
            )
        return todos

    def export_yaml(self, plan: TaskPlan) -> str:
        """YAML 형식으로 출력"""
        import yaml

        data = {
            "goal": plan.goal,
            "detail_level": plan.detail_level,
            "task_count": len(plan.tasks),
            "tasks": [
                {
                    "id": t.id,
                    "content": t.content,
                    "activeForm": t.activeForm,
                    "status": t.status,
                    "tier": t.tier,
                    "parent": t.parent,
                    "dependencies": t.dependencies,
                }
                for t in plan.tasks
            ],
        }
        return yaml.dump(data, allow_unicode=True, default_flow_style=False)


def main():
    parser = argparse.ArgumentParser(description="Task Planner - 촘촘한 작업 계획 자동 생성")
    parser.add_argument("goal", nargs="?", help='최종 목표 (예: "스킬 3개 수정")')
    parser.add_argument(
        "--detail-level",
        type=int,
        default=2,
        choices=[1, 2, 3],
        help="세분화 수준 (1=낮음, 2=보통, 3=높음)",
    )
    parser.add_argument(
        "--format",
        choices=["todowrite", "yaml", "json"],
        default="todowrite",
        help="출력 형식",
    )
    parser.add_argument("--from-file", type=str, help="계획 파일에서 목표 읽기")
    parser.add_argument("--validate", action="store_true", help="계획 검증만 수행")
    parser.add_argument("--dry-run", action="store_true", help="시뮬레이션 모드")

    args = parser.parse_args()

    if args.from_file:
        # 파일에서 목표 읽기
        goal = Path(args.from_file).read_text(encoding="utf-8").splitlines()[0]
    elif args.goal:
        goal = args.goal
    else:
        parser.print_help()
        sys.exit(1)

    # 계획 생성
    planner = TaskPlanner(detail_level=args.detail_level)
    plan = planner.decompose_goal(goal)

    if args.dry_run:
        print(f"[DRY-RUN] 목표: {goal}")
        print(f"[DRY-RUN] 세분화 수준: {args.detail_level}")
        print(f"[DRY-RUN] 생성된 작업 수: {len(plan.tasks)}")

    if args.validate:
        if plan.issues:
            print("⚠️  계획 검증 경고:", file=sys.stderr)
            for issue in plan.issues:
                print(f"  - {issue}", file=sys.stderr)
        else:
            print("✓ 계획 검증 통과")
        return

    if plan.issues:
        print("⚠️  계획 검증 경고:", file=sys.stderr)
        for issue in plan.issues:
            print(f"  - {issue}", file=sys.stderr)

    # 출력
    if args.format == "todowrite":
        todos = planner.export_todowrite_format(plan)
        print(json.dumps(todos, ensure_ascii=False, indent=2))
    elif args.format == "yaml":
        print(planner.export_yaml(plan))
    elif args.format == "json":
        data = {
            "goal": plan.goal,
            "detail_level": plan.detail_level,
            "tasks": [
                {
                    "id": t.id,
                    "content": t.content,
                    "activeForm": t.activeForm,
                    "status": t.status,
                    "tier": t.tier,
                    "dependencies": t.dependencies,
                }
                for t in plan.tasks
            ],
        }
        print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
