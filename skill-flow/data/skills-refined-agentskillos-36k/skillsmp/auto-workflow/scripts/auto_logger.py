"""
Auto Logger - /auto 워크플로우 로그 관리

로그 기록 및 청킹을 담당합니다.
- JSON Lines 형식 로깅
- 50KB 초과 시 자동 청킹
- 세션별 로그 디렉토리 관리
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# 상수
CHUNK_SIZE_BYTES = 50 * 1024  # 50KB

# 동적 프로젝트 루트 감지 (환경 변수 > 현재 디렉토리)
def _get_project_root() -> Path:
    """프로젝트 루트 디렉토리를 동적으로 감지"""
    # 1. 환경 변수 우선
    if env_root := os.environ.get("CLAUDE_PROJECT_DIR"):
        return Path(env_root)
    # 2. 스크립트 위치 기반 (skills/auto-workflow/scripts → 프로젝트 루트)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent.parent.parent
    if (project_root / ".claude").exists():
        return project_root
    # 3. 현재 작업 디렉토리 (fallback)
    return Path.cwd()

PROJECT_ROOT = _get_project_root()
LOG_DIR = PROJECT_ROOT / ".claude" / "auto-logs"
ACTIVE_DIR = LOG_DIR / "active"
ARCHIVE_DIR = LOG_DIR / "archive"


class AutoLogger:
    """자동 워크플로우 로그 관리 클래스"""

    def __init__(self, session_id: Optional[str] = None):
        """
        Args:
            session_id: 기존 세션 ID (None이면 새 세션 생성)
        """
        if session_id:
            self.session_id = session_id
        else:
            self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.session_dir = ACTIVE_DIR / self.session_id
        self.session_dir.mkdir(parents=True, exist_ok=True)

        self.current_chunk = 1
        self.sequence = 0
        self._init_chunk()

    def _init_chunk(self):
        """현재 청크 파일 초기화"""
        # 기존 청크 파일 확인
        existing_chunks = list(self.session_dir.glob("log_*.json"))
        if existing_chunks:
            # 마지막 청크 번호 찾기
            chunk_nums = [int(f.stem.split("_")[1]) for f in existing_chunks]
            self.current_chunk = max(chunk_nums)

            # 마지막 청크의 시퀀스 번호 찾기
            last_chunk = self.session_dir / f"log_{self.current_chunk:03d}.json"
            if last_chunk.exists():
                with open(last_chunk, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            try:
                                entry = json.loads(line)
                                self.sequence = entry.get("sequence", 0)
                            except json.JSONDecodeError:
                                pass

        self.current_log_path = self.session_dir / f"log_{self.current_chunk:03d}.json"

    def _check_chunk_size(self) -> bool:
        """청크 크기 확인 및 필요시 새 청크 생성"""
        if self.current_log_path.exists():
            size = self.current_log_path.stat().st_size
            if size >= CHUNK_SIZE_BYTES:
                self.current_chunk += 1
                self.current_log_path = (
                    self.session_dir / f"log_{self.current_chunk:03d}.json"
                )
                return True
        return False

    def log(
        self,
        event_type: str,
        phase: str,
        data: dict[str, Any],
        context_usage: Optional[int] = None,
        todo_state: Optional[list[dict]] = None,
    ) -> dict:
        """
        이벤트 로깅

        Args:
            event_type: action | decision | error | milestone | checkpoint
            phase: init | analysis | implementation | testing | complete
            data: 이벤트 데이터
            context_usage: Context 사용률 (%)
            todo_state: 현재 Todo 상태

        Returns:
            기록된 로그 엔트리
        """
        self._check_chunk_size()
        self.sequence += 1

        entry = {
            "timestamp": datetime.now().isoformat(),
            "sequence": self.sequence,
            "event_type": event_type,
            "phase": phase,
            "data": data,
        }

        if context_usage is not None:
            entry["context_usage"] = context_usage

        if todo_state is not None:
            entry["todo_state"] = todo_state

        # JSON Lines 형식으로 추가
        with open(self.current_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        return entry

    def log_action(
        self,
        action: str,
        target: str,
        result: str,
        details: Optional[dict] = None,
        context_usage: Optional[int] = None,
    ) -> dict:
        """액션 로깅 헬퍼"""
        return self.log(
            event_type="action",
            phase="implementation",
            data={
                "action": action,
                "target": target,
                "result": result,
                "details": details or {},
            },
            context_usage=context_usage,
        )

    def log_decision(
        self,
        decision: str,
        reason: str,
        alternatives: Optional[list[str]] = None,
        context_usage: Optional[int] = None,
    ) -> dict:
        """의사결정 로깅 헬퍼"""
        return self.log(
            event_type="decision",
            phase="analysis",
            data={
                "decision": decision,
                "reason": reason,
                "alternatives": alternatives or [],
            },
            context_usage=context_usage,
        )

    def log_checkpoint(
        self,
        resume_point: dict,
        todo_state: list[dict],
        context_usage: int,
        key_decisions: Optional[list[str]] = None,
    ) -> dict:
        """체크포인트 로깅"""
        return self.log(
            event_type="checkpoint",
            phase="checkpoint",
            data={"resume_point": resume_point, "key_decisions": key_decisions or []},
            context_usage=context_usage,
            todo_state=todo_state,
        )

    def log_error(
        self, error: str, traceback: Optional[str] = None, recoverable: bool = True
    ) -> dict:
        """에러 로깅"""
        return self.log(
            event_type="error",
            phase="error",
            data={"error": error, "traceback": traceback, "recoverable": recoverable},
        )

    def get_recent_logs(self, count: int = 100) -> list[dict]:
        """최근 로그 엔트리 조회"""
        entries = []

        # 모든 청크 파일 역순으로 읽기
        chunk_files = sorted(self.session_dir.glob("log_*.json"), reverse=True)

        for chunk_file in chunk_files:
            with open(chunk_file, "r", encoding="utf-8") as f:
                chunk_entries = []
                for line in f:
                    if line.strip():
                        try:
                            chunk_entries.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass

                # 역순으로 추가
                entries = chunk_entries + entries
                if len(entries) >= count:
                    break

        return entries[-count:]

    def get_stats(self) -> dict:
        """세션 통계 조회"""
        chunk_files = list(self.session_dir.glob("log_*.json"))
        total_size = sum(f.stat().st_size for f in chunk_files)

        entries = self.get_recent_logs(1000)
        event_counts = {}
        for entry in entries:
            event_type = entry.get("event_type", "unknown")
            event_counts[event_type] = event_counts.get(event_type, 0) + 1

        return {
            "session_id": self.session_id,
            "total_chunks": len(chunk_files),
            "total_size_kb": round(total_size / 1024, 2),
            "total_entries": len(entries),
            "event_counts": event_counts,
        }

    def archive(self, summary: Optional[dict] = None):
        """세션 아카이브"""
        # 요약 파일 생성
        summary_data = summary or {}
        summary_data["archived_at"] = datetime.now().isoformat()
        summary_data["stats"] = self.get_stats()

        summary_path = self.session_dir / "summary.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)

        # 아카이브 디렉토리로 이동
        archive_dest = ARCHIVE_DIR / self.session_id
        if archive_dest.exists():
            import shutil

            shutil.rmtree(archive_dest)

        self.session_dir.rename(archive_dest)
        return archive_dest


def get_active_sessions() -> list[str]:
    """활성 세션 목록 조회"""
    if not ACTIVE_DIR.exists():
        return []
    return [d.name for d in ACTIVE_DIR.iterdir() if d.is_dir()]


def get_archived_sessions() -> list[str]:
    """아카이브된 세션 목록 조회"""
    if not ARCHIVE_DIR.exists():
        return []
    return [d.name for d in ARCHIVE_DIR.iterdir() if d.is_dir()]


if __name__ == "__main__":
    # 테스트
    logger = AutoLogger()
    print(f"Session ID: {logger.session_id}")

    # 테스트 로깅
    logger.log_action("file_read", "test.py", "success")
    logger.log_decision("Use JWT", "Better security", ["Session", "Basic Auth"])

    print(f"Stats: {logger.get_stats()}")
