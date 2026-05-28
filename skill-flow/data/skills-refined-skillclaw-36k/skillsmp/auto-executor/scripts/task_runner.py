#!/usr/bin/env python3
"""
task_runner.py: Task tool 강제 호출 로직

Claude CLI를 호출할 때 Task tool 사용을 강제합니다.
"""

import subprocess
import shutil
import sys
import json
import re
from pathlib import Path
from typing import Optional, Dict, Any, List


class TaskRunner:
    """Task tool을 강제로 사용하여 서브에이전트 실행"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.claude_path = self._find_claude()

    def _find_claude(self) -> str:
        """Claude CLI 경로 찾기"""
        claude = shutil.which("claude")
        if claude:
            return claude
        # Windows 기본 경로
        default_paths = [
            r"C:\Users\AidenKim\AppData\Local\npm\claude.cmd",
            r"C:\Program Files\nodejs\claude.cmd",
        ]
        for path in default_paths:
            if Path(path).exists():
                return path
        return "claude"  # fallback

    def discover_next_task(self, direction: Optional[str] = None) -> Optional[str]:
        """5계층 우선순위로 다음 작업 발견"""

        # Tier 2: 긴급 (테스트/린트/빌드 실패)
        task = self._check_urgent_tasks()
        if task:
            return task

        # Tier 3: 작업 처리 (변경사항/이슈/PR)
        task = self._check_work_tasks()
        if task:
            return task

        # Tier 1: 명시적 지시 (direction이 있으면)
        if direction:
            return f"사용자 지시: {direction}"

        return None

    def discover_autonomous_task(self) -> Optional[str]:
        """Tier 4: 자율 개선 작업 발견"""

        # 테스트 커버리지 확인
        try:
            result = subprocess.run(
                ["pytest", "--co", "-q"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=30,
            )
            if "no tests" in result.stdout.lower():
                return "테스트가 없는 모듈에 테스트 추가"
        except Exception:
            pass

        # 문서 확인
        readme = self.project_root / "README.md"
        if not readme.exists():
            return "README.md 문서 작성"

        # TODO 주석 확인
        try:
            result = subprocess.run(
                ["git", "grep", "-n", "TODO:", "--", "*.py", "*.ts", "*.js"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=30,
            )
            if result.stdout.strip():
                lines = result.stdout.strip().split("\n")
                return f"TODO 주석 해결 ({len(lines)}개 발견)"
        except Exception:
            pass

        return None

    def _check_urgent_tasks(self) -> Optional[str]:
        """Tier 2: 긴급 작업 확인"""

        # 린트 오류 확인
        try:
            result = subprocess.run(
                ["ruff", "check", ".", "--statistics"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=60,
            )
            if result.returncode != 0:
                # 오류 수 파싱
                match = re.search(r"(\d+)\s+error", result.stdout + result.stderr)
                if match:
                    count = int(match.group(1))
                    if count >= 5:
                        return f"린트 오류 {count}개 수정"
        except Exception:
            pass

        # TypeScript 빌드 오류
        tsconfig = self.project_root / "tsconfig.json"
        if tsconfig.exists():
            try:
                result = subprocess.run(
                    ["npx", "tsc", "--noEmit"],
                    capture_output=True,
                    text=True,
                    cwd=self.project_root,
                    timeout=120,
                )
                if result.returncode != 0:
                    errors = result.stdout.count("error TS")
                    if errors > 0:
                        return f"TypeScript 빌드 오류 {errors}개 수정"
            except Exception:
                pass

        return None

    def _check_work_tasks(self) -> Optional[str]:
        """Tier 3: 작업 처리 확인"""

        # 변경사항 확인
        try:
            result = subprocess.run(
                ["git", "diff", "--stat"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=30,
            )
            if result.stdout.strip():
                # 변경 줄 수 파싱
                match = re.search(r"(\d+)\s+insertion|(\d+)\s+deletion", result.stdout)
                if match:
                    insertions = int(match.group(1) or 0)
                    deletions = int(match.group(2) or 0)
                    total = insertions + deletions
                    if total >= 100:
                        return f"변경사항 {total}줄 커밋"
        except Exception:
            pass

        # GitHub 이슈 확인
        try:
            result = subprocess.run(
                [
                    "gh",
                    "issue",
                    "list",
                    "--state",
                    "open",
                    "--limit",
                    "1",
                    "--json",
                    "number,title",
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=30,
            )
            if result.returncode == 0 and result.stdout.strip():
                issues = json.loads(result.stdout)
                if issues:
                    issue = issues[0]
                    return f"GitHub 이슈 #{issue['number']} 해결: {issue['title']}"
        except Exception:
            pass

        return None

    def execute_with_task_tool(self, task: str, agent: str) -> Dict[str, Any]:
        """
        Task tool을 강제로 사용하여 서브에이전트 실행

        핵심: Claude CLI 호출 시 Task tool 사용을 명시적으로 강제
        """

        # Task tool 강제 프롬프트
        prompt = f'''**중요: 반드시 Task tool을 사용하세요. 직접 처리는 금지입니다.**

다음 작업을 Task tool로 서브에이전트에 위임하세요.

## 작업 정보
- 작업: {task}
- 에이전트: {agent}

## 필수 실행 방식

아래 형식으로 Task tool을 호출하세요:

Task(
    subagent_type="{agent}",
    prompt="""
## 작업 지시
{task}

## 프로젝트 경로
{self.project_root}

## 중요 규칙
1. 작업을 완료하고 결과만 반환하세요
2. 중간 질문 없이 최선의 판단으로 진행하세요

## 결과 형식
### 요약
- 한 줄 요약

### 수행 작업
- 작업 목록

### 변경 파일
| 파일 | 변경 |
|------|------|
    """,
    description="{task[:50]}"
)

**경고: Task tool을 사용하지 않고 직접 처리하면 실패로 간주됩니다.**
**반드시 위의 Task() 호출을 실행하세요.**
'''

        try:
            # Claude CLI 실행
            result = subprocess.run(
                [self.claude_path, "-p", prompt, "--dangerously-skip-permissions"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=600,  # 10분 타임아웃
                encoding="utf-8",
                errors="replace",
            )

            output = result.stdout + result.stderr

            # 결과 파싱
            return {
                "success": result.returncode == 0,
                "summary": self._extract_summary(output),
                "output": output[:2000],  # 최대 2000자
                "task": task,
                "agent": agent,
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "summary": "타임아웃 (10분 초과)",
                "output": "",
                "task": task,
                "agent": agent,
            }
        except Exception as e:
            return {
                "success": False,
                "summary": f"실행 오류: {str(e)}",
                "output": "",
                "task": task,
                "agent": agent,
            }

    def execute_verify_parallel(
        self, task: str, target_files: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        GPT + Gemini 병렬 검증 실행

        Args:
            task: 검증 작업 설명
            target_files: 검증할 파일 목록 (없으면 변경된 파일 자동 탐지)

        Returns:
            검증 결과 딕셔너리
        """
        # 1. 검증 대상 파일 결정
        if not target_files:
            target_files = self._get_changed_files()

        if not target_files:
            return {
                "success": False,
                "summary": "검증할 파일이 없습니다",
                "output": "",
                "task": task,
                "agent": "verify",
            }

        # 2. Cross-AI Verifier 스크립트 경로
        verifier_script = (
            self.project_root
            / ".claude"
            / "skills"
            / "cross-ai-verifier"
            / "scripts"
            / "main.py"
        )

        if not verifier_script.exists():
            return {
                "success": False,
                "summary": "Cross-AI Verifier 스크립트를 찾을 수 없습니다",
                "output": f"경로: {verifier_script}",
                "task": task,
                "agent": "verify",
            }

        # 3. 검증 focus 추출 (task에서 키워드 분석)
        focus = self._extract_verify_focus(task)

        # 4. 각 파일에 대해 GPT + Gemini 병렬 검증
        all_results = []
        errors = []

        for file_path in target_files[:5]:  # 최대 5개 파일
            try:
                result = subprocess.run(
                    [
                        sys.executable,
                        str(verifier_script),
                        file_path,
                        "--parallel",  # GPT + Gemini 동시 검증
                        "--focus",
                        focus,
                        "--json",
                    ],
                    capture_output=True,
                    text=True,
                    cwd=self.project_root,
                    timeout=300,  # 5분 타임아웃
                    encoding="utf-8",
                    errors="replace",
                )

                if result.returncode == 0 and result.stdout.strip():
                    try:
                        file_result = json.loads(result.stdout)
                        file_result["file"] = file_path
                        all_results.append(file_result)
                    except json.JSONDecodeError:
                        all_results.append(
                            {"file": file_path, "raw_output": result.stdout[:1000]}
                        )
                else:
                    errors.append(
                        {
                            "file": file_path,
                            "error": (
                                result.stderr[:500]
                                if result.stderr
                                else "Unknown error"
                            ),
                        }
                    )

            except subprocess.TimeoutExpired:
                errors.append({"file": file_path, "error": "검증 타임아웃 (5분 초과)"})
            except Exception as e:
                errors.append({"file": file_path, "error": str(e)})

        # 5. 결과 집계
        total_issues = sum(
            len(r.get("issues", []))
            for r in all_results
            if isinstance(r.get("issues"), list)
        )

        summary = self._format_verify_summary(all_results, errors, focus)

        return {
            "success": len(all_results) > 0,
            "summary": summary,
            "results": all_results,
            "errors": errors,
            "total_issues": total_issues,
            "files_checked": len(all_results),
            "task": task,
            "agent": "verify",
            "providers": ["openai", "gemini"],
        }

    def _get_changed_files(self) -> List[str]:
        """git diff에서 변경된 파일 목록 추출"""
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=ACMR"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=30,
            )

            if result.returncode == 0 and result.stdout.strip():
                files = result.stdout.strip().split("\n")
                # Python/TypeScript 파일만 필터링
                code_files = [
                    f
                    for f in files
                    if f.endswith((".py", ".ts", ".tsx", ".js", ".jsx"))
                ]
                return code_files

            return []
        except Exception:
            return []

    def _extract_verify_focus(self, task: str) -> str:
        """작업 설명에서 검증 focus 추출"""
        task_lower = task.lower()

        if any(
            kw in task_lower for kw in ["보안", "security", "취약점", "vulnerability"]
        ):
            return "security"
        elif any(kw in task_lower for kw in ["버그", "bug", "오류", "error"]):
            return "bugs"
        elif any(
            kw in task_lower for kw in ["성능", "performance", "최적화", "optimization"]
        ):
            return "performance"
        else:
            return "all"

    def _format_verify_summary(
        self, results: List[Dict], errors: List[Dict], focus: str
    ) -> str:
        """검증 결과 요약 포맷팅"""
        if not results and errors:
            return f"검증 실패: {len(errors)}개 파일에서 오류 발생"

        total_issues = sum(
            len(r.get("issues", []))
            for r in results
            if isinstance(r.get("issues"), list)
        )

        high_severity = sum(
            1
            for r in results
            for issue in r.get("issues", [])
            if isinstance(issue, dict) and issue.get("severity") == "high"
        )

        providers_used = "GPT + Gemini"

        summary_parts = [
            f"🔍 Cross-AI 검증 완료 ({providers_used})",
            f"📁 검증 파일: {len(results)}개",
            f"⚠️ 발견 이슈: {total_issues}개",
        ]

        if high_severity > 0:
            summary_parts.append(f"🔴 심각 이슈: {high_severity}개")

        summary_parts.append(f"🎯 검증 초점: {focus}")

        if errors:
            summary_parts.append(f"❌ 오류: {len(errors)}개 파일")

        return " | ".join(summary_parts)

    def should_auto_verify(self, min_changes: int = 100) -> Optional[Dict[str, Any]]:
        """
        코드 변경 시 자동 검증 여부 판단

        Args:
            min_changes: 검증 권장을 위한 최소 변경 줄 수

        Returns:
            검증 필요 시 변경 정보 딕셔너리, 아니면 None
        """
        try:
            # git diff로 변경량 체크
            result = subprocess.run(
                ["git", "diff", "--stat"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=30,
            )

            if result.returncode != 0 or not result.stdout.strip():
                return None

            # 변경 줄 수 파싱 (예: "3 files changed, 150 insertions(+), 20 deletions(-)")
            match = re.search(
                r"(\d+)\s+files?\s+changed(?:,\s+(\d+)\s+insertions?\(\+\))?(?:,\s+(\d+)\s+deletions?\(-\))?",
                result.stdout,
            )

            if not match:
                return None

            files_changed = int(match.group(1))
            insertions = int(match.group(2) or 0)
            deletions = int(match.group(3) or 0)
            total_changes = insertions + deletions

            if total_changes >= min_changes:
                # 변경된 파일 목록 추출
                changed_files = []
                for line in result.stdout.strip().split("\n")[:-1]:
                    # "path/to/file.py | 10 ++"
                    file_match = re.match(r"\s*([^\|]+)\s*\|", line)
                    if file_match:
                        changed_files.append(file_match.group(1).strip())

                return {
                    "should_verify": True,
                    "files_changed": files_changed,
                    "insertions": insertions,
                    "deletions": deletions,
                    "total_changes": total_changes,
                    "changed_files": changed_files[:10],  # 최대 10개
                    "reason": f"대규모 변경 감지: {total_changes}줄 ({insertions}+, {deletions}-)",
                }

            return None

        except Exception:
            return None

    def get_verify_recommendation(self) -> Optional[str]:
        """자동 검증 권장 메시지 생성"""
        verify_info = self.should_auto_verify()

        if not verify_info:
            return None

        files_preview = ", ".join(verify_info["changed_files"][:3])
        if len(verify_info["changed_files"]) > 3:
            files_preview += f" 외 {len(verify_info['changed_files']) - 3}개"

        return f"""💡 **Cross-AI 검증 권장**
{verify_info['reason']}
주요 파일: {files_preview}

검증 실행: `/auto "코드 검증"` 또는 `/verify`"""

    def _extract_summary(self, output: str) -> str:
        """출력에서 요약 추출"""
        # "### 요약" 섹션 찾기
        match = re.search(r"###\s*요약\s*\n([^\n#]+)", output)
        if match:
            return match.group(1).strip()

        # "요약:" 패턴 찾기
        match = re.search(r"요약[:\s]+([^\n]+)", output)
        if match:
            return match.group(1).strip()

        # 첫 번째 의미있는 줄 반환
        for line in output.split("\n"):
            line = line.strip()
            if line and not line.startswith("#") and len(line) > 10:
                return line[:100]

        return "결과 요약 없음"
