#!/usr/bin/env python3
"""
session_manager.py: 세션 YAML 관리

세션 상태를 .claude/auto/session.yaml에 저장하고 관리합니다.
"""

import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class SessionManager:
    """세션 상태 관리"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.auto_dir = project_root / ".claude" / "auto"
        self.session_file = self.auto_dir / "session.yaml"
        self.history_dir = self.auto_dir / "history"

        # 폴더 생성
        self.auto_dir.mkdir(parents=True, exist_ok=True)
        self.history_dir.mkdir(parents=True, exist_ok=True)

        self._session: Optional[Dict[str, Any]] = None

    def ensure_session(self, direction: Optional[str] = None) -> Dict[str, Any]:
        """세션 확인 또는 생성"""
        if self.session_file.exists():
            self._load_session()
            print(f"📂 기존 세션 로드: {self._session['session_id']}")
        else:
            self._create_session(direction)
            print(f"📂 새 세션 생성: {self._session['session_id']}")

        return self._session

    def _load_session(self):
        """세션 파일 로드"""
        with open(self.session_file, "r", encoding="utf-8") as f:
            self._session = yaml.safe_load(f)

    def _save_session(self):
        """세션 파일 저장"""
        with open(self.session_file, "w", encoding="utf-8") as f:
            yaml.dump(self._session, f, allow_unicode=True, default_flow_style=False)

    def _create_session(self, direction: Optional[str] = None):
        """새 세션 생성"""
        now = datetime.now()
        session_id = f"auto_{now.strftime('%Y%m%d')}_{now.strftime('%H%M%S')}"

        self._session = {
            "session_id": session_id,
            "started_at": now.isoformat(),
            "direction": direction or "자동 판단",
            "status": "running",
            "tasks": {"completed": [], "in_progress": [], "pending": []},
            "statistics": {
                "total_tasks": 0,
                "completed": 0,
                "in_progress": 0,
                "pending": 0,
                "total_duration_minutes": 0,
            },
        }
        self._save_session()

    def get_direction(self) -> Optional[str]:
        """현재 작업 방향 반환"""
        if self._session:
            return self._session.get("direction")
        if self.session_file.exists():
            self._load_session()
            return self._session.get("direction")
        return None

    def redirect(self, new_direction: str):
        """작업 방향 수정"""
        if not self._session:
            self._load_session()

        # 기존 pending 작업 정리
        self._session["tasks"]["pending"] = []
        self._session["direction"] = new_direction
        self._session["statistics"]["pending"] = 0

        self._save_session()

    def add_completed_task(self, task: str, agent: str, result: Dict[str, Any]):
        """완료된 작업 추가"""
        if not self._session:
            self._load_session()

        now = datetime.now()

        task_record = {
            "id": f"task_{len(self._session['tasks']['completed']) + 1:03d}",
            "description": task,
            "agent": agent,
            "completed_at": now.isoformat(),
            "result": result.get("summary", ""),
            "success": result.get("success", True),
        }

        self._session["tasks"]["completed"].append(task_record)
        self._session["statistics"]["completed"] = len(
            self._session["tasks"]["completed"]
        )
        self._session["statistics"]["total_tasks"] = (
            self._session["statistics"]["completed"]
            + self._session["statistics"]["in_progress"]
            + self._session["statistics"]["pending"]
        )

        self._save_session()

    def get_statistics(self) -> Dict[str, int]:
        """통계 반환"""
        if not self._session:
            if self.session_file.exists():
                self._load_session()
            else:
                return {"completed": 0, "in_progress": 0, "pending": 0, "total": 0}

        return {
            "completed": self._session["statistics"]["completed"],
            "in_progress": self._session["statistics"]["in_progress"],
            "pending": self._session["statistics"]["pending"],
            "total": self._session["statistics"]["total_tasks"],
        }

    def get_status_report(self) -> str:
        """상태 보고서 생성"""
        if not self.session_file.exists():
            return "❌ 활성 세션 없음. `/auto`로 새 세션을 시작하세요."

        self._load_session()

        # 경과 시간 계산
        started = datetime.fromisoformat(self._session["started_at"])
        elapsed = datetime.now() - started
        elapsed_str = f"{int(elapsed.total_seconds() // 60)}분"

        report = f"""
## /auto 진행 현황

### 세션 정보
| 항목 | 값 |
|------|-----|
| 세션 ID | {self._session['session_id']} |
| 시작 | {self._session['started_at'][:16].replace('T', ' ')} |
| 경과 | {elapsed_str} |
| 방향 | {self._session['direction']} |
| 상태 | {self._session['status']} |

### 완료된 작업 ({len(self._session['tasks']['completed'])}개)
"""
        for i, task in enumerate(self._session["tasks"]["completed"], 1):
            status = "✅" if task.get("success", True) else "❌"
            report += f"{i}. {status} {task['description']} ({task['agent']})\n"

        if self._session["tasks"]["in_progress"]:
            report += f"\n### 진행중 ({len(self._session['tasks']['in_progress'])}개)\n"
            for task in self._session["tasks"]["in_progress"]:
                report += f"🔄 {task['description']} ({task['agent']})\n"

        if self._session["tasks"]["pending"]:
            report += f"\n### 대기중 ({len(self._session['tasks']['pending'])}개)\n"
            for task in self._session["tasks"]["pending"]:
                report += f"⏳ {task['description']}\n"

        report += f"""
### 통계
| 항목 | 값 |
|------|-----|
| 총 작업 | {self._session['statistics']['total_tasks']} |
| 완료 | {self._session['statistics']['completed']} |
| 경과 시간 | {elapsed_str} |

---

**명령어**
- 계속 진행: `python auto_executor.py`
- 방향 수정: `python auto_executor.py --redirect "새 방향"`
- 종료: `python auto_executor.py --stop`
"""
        return report

    def stop_session(self) -> str:
        """세션 종료 및 최종 보고서"""
        if not self.session_file.exists():
            return "❌ 활성 세션 없음."

        self._load_session()

        # 최종 보고서 생성
        started = datetime.fromisoformat(self._session["started_at"])
        ended = datetime.now()
        duration = ended - started
        duration_str = f"{int(duration.total_seconds() // 60)}분"

        # 에이전트별 통계
        agent_stats: Dict[str, int] = {}
        for task in self._session["tasks"]["completed"]:
            agent = task.get("agent", "unknown")
            agent_stats[agent] = agent_stats.get(agent, 0) + 1

        report = f"""
## /auto 최종 보고서

### 세션 요약
| 항목 | 값 |
|------|-----|
| 세션 ID | {self._session['session_id']} |
| 기간 | {self._session['started_at'][:16]} ~ {ended.strftime('%Y-%m-%d %H:%M')} |
| 총 시간 | {duration_str} |
| 방향 | {self._session['direction']} |

### 작업 통계
| 상태 | 개수 |
|------|------|
| 완료 | {self._session['statistics']['completed']} |
| 미완료 | {self._session['statistics']['in_progress'] + self._session['statistics']['pending']} |
| 총계 | {self._session['statistics']['total_tasks']} |

### 사용된 에이전트
| 에이전트 | 작업 수 |
|----------|---------|
"""
        for agent, count in sorted(agent_stats.items(), key=lambda x: -x[1]):
            report += f"| {agent} | {count} |\n"

        report += "\n### 완료된 작업 목록\n"
        for i, task in enumerate(self._session["tasks"]["completed"], 1):
            status = "✅" if task.get("success", True) else "❌"
            report += f"{i}. {status} {task['description']}\n"
            if task.get("result"):
                report += f"   → {task['result']}\n"

        report += """
---

세션이 종료되었습니다.
새 세션을 시작하려면 `python auto_executor.py` 실행
"""

        # 세션 파일 아카이브
        archive_name = f"session_{self._session['session_id']}.yaml"
        archive_path = self.history_dir / archive_name

        self._session["status"] = "completed"
        self._session["ended_at"] = ended.isoformat()

        with open(archive_path, "w", encoding="utf-8") as f:
            yaml.dump(self._session, f, allow_unicode=True, default_flow_style=False)

        # 현재 세션 파일 삭제
        self.session_file.unlink()
        self._session = None

        return report
