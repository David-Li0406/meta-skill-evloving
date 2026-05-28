"""
Auto State - /auto 워크플로우 상태 관리

세션 상태 및 체크포인트를 관리합니다.
- 세션 상태 저장/로드
- 체크포인트 생성/복원
- Context 사용량 모니터링
"""

import json
from datetime import datetime
from typing import Optional

from auto_logger import AutoLogger, ACTIVE_DIR, ARCHIVE_DIR
from context_predictor import ContextPredictor, predict_and_decide, TaskEstimate

# Context 임계값
CONTEXT_THRESHOLDS = {
    "safe": 40,
    "monitor": 60,
    "prepare": 80,
    "warning": 85,
    "critical": 90,
}

# 80% 예측 임계값 (다음 작업이 이 %를 초과하면 정리)
PREDICTION_THRESHOLD = 20


class AutoState:
    """자동 워크플로우 상태 관리 클래스"""

    def __init__(self, session_id: Optional[str] = None, original_request: str = ""):
        """
        Args:
            session_id: 기존 세션 ID (None이면 새 세션 생성)
            original_request: 원본 작업 요청
        """
        self.logger = AutoLogger(session_id)
        self.session_id = self.logger.session_id
        self.session_dir = self.logger.session_dir

        self.state_path = self.session_dir / "state.json"
        self.checkpoint_path = self.session_dir / "checkpoint.json"

        if self.state_path.exists():
            self._load_state()
        else:
            self._init_state(original_request)

    def _init_state(self, original_request: str):
        """새 세션 상태 초기화"""
        self.state = {
            "session_id": self.session_id,
            "status": "running",
            "started_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "original_request": original_request,
            "current_phase": "init",
            "context_stats": {"peak_usage": 0, "current_usage": 0, "clear_count": 0},
            "progress": {
                "total_tasks": 0,
                "completed": 0,
                "in_progress": 0,
                "pending": 0,
            },
            "prd": {
                "path": None,
                "status": "none",  # none | searching | writing | reviewing | approved
                "review_result": None,
                "approved_at": None,
            },
            "files_touched": [],
            "key_decisions": [],
            "resume_point": None,
            "last_commit": None,
        }
        self._save_state()

    def _load_state(self):
        """세션 상태 로드"""
        with open(self.state_path, "r", encoding="utf-8") as f:
            self.state = json.load(f)

    def _save_state(self):
        """세션 상태 저장"""
        self.state["last_activity"] = datetime.now().isoformat()
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    # === 상태 업데이트 ===

    def update_phase(self, phase: str):
        """현재 Phase 업데이트"""
        self.state["current_phase"] = phase
        self._save_state()

    def update_context_usage(self, percent: int) -> str:
        """
        Context 사용량 업데이트

        Returns:
            상태 레벨: safe | monitor | prepare | warning | critical
        """
        self.state["context_stats"]["current_usage"] = percent
        if percent > self.state["context_stats"]["peak_usage"]:
            self.state["context_stats"]["peak_usage"] = percent
        self._save_state()

        # 임계값 확인
        if percent >= CONTEXT_THRESHOLDS["critical"]:
            return "critical"
        elif percent >= CONTEXT_THRESHOLDS["warning"]:
            return "warning"
        elif percent >= CONTEXT_THRESHOLDS["prepare"]:
            return "prepare"
        elif percent >= CONTEXT_THRESHOLDS["monitor"]:
            return "monitor"
        return "safe"

    # === Context 예측 (80% 판단) ===

    def analyze_next_task(self, task: dict) -> dict:
        """
        다음 작업의 예상 Context 사용량 분석

        Args:
            task: {
                "type": str,           # 작업 유형
                "affected_files": int, # 영향받는 파일 수
                "complexity": str,     # low | medium | high
                "description": str     # 작업 설명
            }

        Returns:
            {
                "action": "continue" | "cleanup",
                "estimate": TaskEstimate,
                "message": str
            }
        """
        current = self.state["context_stats"]["current_usage"]
        return predict_and_decide(current, task, PREDICTION_THRESHOLD)

    def should_cleanup_before_task(
        self, task: dict
    ) -> tuple[bool, Optional[TaskEstimate]]:
        """
        작업 전 정리 필요 여부 판단 (80% 이상일 때 사용)

        Returns:
            (정리 필요 여부, TaskEstimate 또는 None)
        """
        current = self.state["context_stats"]["current_usage"]

        # 80% 미만이면 정리 불필요
        if current < CONTEXT_THRESHOLDS["prepare"]:
            return False, None

        predictor = ContextPredictor(current)
        should_clean, estimate = predictor.should_cleanup(task, PREDICTION_THRESHOLD)

        return should_clean, estimate

    def handle_prepare(self, next_task: Optional[dict] = None) -> dict:
        """
        80% 도달 시 처리 로직

        Args:
            next_task: 다음 작업 정보 (없으면 기본 작업 가정)

        Returns:
            {
                "action": "continue" | "cleanup",
                "reason": str,
                "estimate": TaskEstimate | None,
                "instructions": list[str]  # 실행할 명령어 목록
            }
        """
        current = self.state["context_stats"]["current_usage"]

        # 기본 작업 (정보 없을 때)
        if next_task is None:
            next_task = {"type": "default", "affected_files": 1, "complexity": "medium"}

        predictor = ContextPredictor(current)
        should_clean, estimate = predictor.should_cleanup(
            next_task, PREDICTION_THRESHOLD
        )

        if should_clean:
            # 정리 필요
            return {
                "action": "cleanup",
                "reason": f"예상 {estimate.adjusted_estimate}% > 임계값 {PREDICTION_THRESHOLD}%",
                "estimate": estimate,
                "instructions": [
                    "1. 현재 작업 완료",
                    "2. 세션 문서 업데이트",
                    "3. /commit 실행",
                    "4. /clear 실행",
                    "5. /auto 재시작",
                ],
            }
        else:
            # 계속 진행
            return {
                "action": "continue",
                "reason": f"예상 {estimate.adjusted_estimate}% <= 임계값 {PREDICTION_THRESHOLD}%",
                "estimate": estimate,
                "instructions": [f"다음 작업 진행: {next_task.get('type', 'default')}"],
            }

    def handle_critical(self) -> dict:
        """
        90% 도달 시 즉시 정리 처리

        Returns:
            {
                "action": "immediate_cleanup",
                "reason": str,
                "instructions": list[str]
            }
        """
        current = self.state["context_stats"]["current_usage"]

        return {
            "action": "immediate_cleanup",
            "reason": f"Context {current}% >= 90% (임계값)",
            "instructions": [
                "1. 추가 작업 없이 현재 작업만 완료",
                "2. 세션 문서 업데이트",
                "3. /commit 실행",
                "4. /clear 실행",
                "5. /auto 재시작 (체크포인트에서 재개)",
            ],
        }

    def get_context_action(self, next_task: Optional[dict] = None) -> dict:
        """
        현재 Context 상태에 따른 액션 결정

        Returns:
            {
                "level": str,          # safe | monitor | prepare | warning | critical
                "action": str,         # continue | cleanup | immediate_cleanup
                "details": dict        # 상세 정보
            }
        """
        current = self.state["context_stats"]["current_usage"]
        level = self.update_context_usage(current)

        if level == "critical":
            return {
                "level": level,
                "action": "immediate_cleanup",
                "details": self.handle_critical(),
            }
        elif level in ["prepare", "warning"]:
            prepare_result = self.handle_prepare(next_task)
            return {
                "level": level,
                "action": prepare_result["action"],
                "details": prepare_result,
            }
        else:
            return {
                "level": level,
                "action": "continue",
                "details": {
                    "reason": f"Context {current}% - 안전 구간",
                    "instructions": ["정상 작업 계속"],
                },
            }

    def update_progress(
        self,
        total: Optional[int] = None,
        completed: Optional[int] = None,
        in_progress: Optional[int] = None,
        pending: Optional[int] = None,
    ):
        """진행 상황 업데이트"""
        if total is not None:
            self.state["progress"]["total_tasks"] = total
        if completed is not None:
            self.state["progress"]["completed"] = completed
        if in_progress is not None:
            self.state["progress"]["in_progress"] = in_progress
        if pending is not None:
            self.state["progress"]["pending"] = pending
        self._save_state()

    def add_file_touched(self, file_path: str):
        """변경된 파일 추가"""
        if file_path not in self.state["files_touched"]:
            self.state["files_touched"].append(file_path)
            self._save_state()

    def add_decision(self, decision: str):
        """핵심 결정 추가"""
        if decision not in self.state["key_decisions"]:
            self.state["key_decisions"].append(decision)
            self._save_state()

    def set_last_commit(self, commit_message: str):
        """마지막 커밋 정보 저장"""
        self.state["last_commit"] = {
            "message": commit_message,
            "timestamp": datetime.now().isoformat(),
        }
        self._save_state()

    # === PRD 관리 ===

    def update_prd_status(self, status: str, path: Optional[str] = None):
        """
        PRD 상태 업데이트

        Args:
            status: none | searching | writing | reviewing | approved
            path: PRD 파일 경로
        """
        self.state["prd"]["status"] = status
        if path:
            self.state["prd"]["path"] = path
        self._save_state()

    def set_prd_review_result(self, result: dict):
        """
        PRD 검토 결과 저장

        Args:
            result: {
                "requirements": int,  # 요구사항 개수
                "tech_spec": str,     # 기술 스펙 상태 (clear/unclear)
                "test_scenarios": int, # 테스트 시나리오 개수
                "checklist_items": int # 체크리스트 항목 개수
            }
        """
        self.state["prd"]["review_result"] = result
        self._save_state()

    def approve_prd(self):
        """PRD 승인"""
        self.state["prd"]["status"] = "approved"
        self.state["prd"]["approved_at"] = datetime.now().isoformat()
        self._save_state()

    def get_prd_status(self) -> dict:
        """PRD 상태 조회"""
        return self.state.get(
            "prd",
            {
                "path": None,
                "status": "none",
                "review_result": None,
                "approved_at": None,
            },
        )

    # === 체크포인트 ===

    def create_checkpoint(
        self, task_id: int, task_content: str, context_hint: str, todo_state: list[dict]
    ):
        """체크포인트 생성"""
        checkpoint = {
            "created_at": datetime.now().isoformat(),
            "session_id": self.session_id,
            "resume_point": {
                "task_id": task_id,
                "task_content": task_content,
                "context_hint": context_hint,
            },
            "todo_state": todo_state,
            "state_snapshot": {
                "current_phase": self.state["current_phase"],
                "progress": self.state["progress"].copy(),
                "key_decisions": self.state["key_decisions"].copy(),
                "files_touched": self.state["files_touched"].copy(),
            },
        }

        with open(self.checkpoint_path, "w", encoding="utf-8") as f:
            json.dump(checkpoint, f, ensure_ascii=False, indent=2)

        # 상태에도 resume_point 저장
        self.state["resume_point"] = checkpoint["resume_point"]
        self._save_state()

        # 로그에도 기록
        self.logger.log_checkpoint(
            resume_point=checkpoint["resume_point"],
            todo_state=todo_state,
            context_usage=self.state["context_stats"]["current_usage"],
            key_decisions=self.state["key_decisions"],
        )

        return checkpoint

    def load_checkpoint(self) -> Optional[dict]:
        """체크포인트 로드"""
        if not self.checkpoint_path.exists():
            return None

        with open(self.checkpoint_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # === 상태 관리 ===

    def set_status(self, status: str):
        """세션 상태 설정: running | paused | completed | failed"""
        self.state["status"] = status
        self._save_state()

    def increment_clear_count(self):
        """Context clear 횟수 증가"""
        self.state["context_stats"]["clear_count"] += 1
        self._save_state()

    def get_status(self) -> dict:
        """현재 상태 조회"""
        return {
            "session_id": self.session_id,
            "status": self.state["status"],
            "phase": self.state["current_phase"],
            "progress": self.state["progress"],
            "context": self.state["context_stats"],
            "clear_count": self.state["context_stats"]["clear_count"],
        }

    def get_resume_summary(self) -> str:
        """재개용 요약 생성"""
        checkpoint = self.load_checkpoint()
        if not checkpoint:
            return "체크포인트가 없습니다."

        progress = self.state["progress"]
        decisions = self.state["key_decisions"]
        prd = self.state.get("prd", {})
        last_commit = self.state.get("last_commit")

        # PRD 상태 문자열
        prd_status_str = ""
        if prd.get("path"):
            prd_status_str = f"- PRD: {prd['path']} ({prd.get('status', 'unknown')})"
        else:
            prd_status_str = "- PRD: (없음)"

        # 마지막 커밋 문자열
        commit_str = ""
        if last_commit:
            commit_str = f"\n### 마지막 커밋\n{last_commit['message']}"

        summary = f"""
## 세션 재개: {self.session_id}

### 원본 요청
{self.state['original_request']}

### 진행 상황
- 완료: {progress['completed']}/{progress['total_tasks']}
- 현재 Phase: {self.state['current_phase']}
- Context Clear 횟수: {self.state['context_stats']['clear_count']}
{prd_status_str}
{commit_str}

### 핵심 결정
{chr(10).join('- ' + d for d in decisions) if decisions else '- (없음)'}

### 다음 작업
{checkpoint['resume_point']['task_content']}

### 힌트
{checkpoint['resume_point']['context_hint']}

### 변경된 파일
{chr(10).join('- ' + f for f in self.state['files_touched'][:10]) if self.state['files_touched'] else '- (없음)'}
"""
        return summary.strip()

    # === 정리 ===

    def complete(self, summary: Optional[dict] = None):
        """세션 완료 및 아카이브"""
        self.set_status("completed")
        return self.logger.archive(summary)

    def abort(self):
        """세션 취소"""
        self.set_status("failed")
        # 아카이브하지 않고 상태만 변경


def restore_session(session_id: str) -> tuple[AutoState, str]:
    """
    세션 복원

    Returns:
        (AutoState 인스턴스, 재개 요약)
    """
    # active에서 찾기
    session_dir = ACTIVE_DIR / session_id
    if not session_dir.exists():
        # archive에서 찾기
        session_dir = ARCHIVE_DIR / session_id
        if session_dir.exists():
            # archive에서 active로 이동
            import shutil

            active_dest = ACTIVE_DIR / session_id
            shutil.move(str(session_dir), str(active_dest))

    if not (ACTIVE_DIR / session_id).exists():
        raise ValueError(f"Session not found: {session_id}")

    state = AutoState(session_id)
    state.increment_clear_count()
    summary = state.get_resume_summary()

    return state, summary


def get_latest_active_session() -> Optional[str]:
    """가장 최근 활성 세션 ID 조회"""
    if not ACTIVE_DIR.exists():
        return None

    sessions = []
    for d in ACTIVE_DIR.iterdir():
        if d.is_dir():
            state_file = d / "state.json"
            if state_file.exists():
                with open(state_file, "r", encoding="utf-8") as f:
                    state = json.load(f)
                    if state.get("status") == "running":
                        sessions.append((d.name, state.get("last_activity", "")))

    if not sessions:
        return None

    # 최신순 정렬
    sessions.sort(key=lambda x: x[1], reverse=True)
    return sessions[0][0]


if __name__ == "__main__":
    # 테스트
    state = AutoState(original_request="API 인증 기능 구현")
    print(f"Session ID: {state.session_id}")

    state.update_phase("analysis")
    state.update_progress(total=5, completed=0, pending=5)
    state.add_decision("JWT 토큰 방식 선택")

    level = state.update_context_usage(45)
    print(f"Context Level: {level}")

    # 체크포인트 테스트
    state.create_checkpoint(
        task_id=1,
        task_content="핸들러 구현",
        context_hint="src/auth/handler.py",
        todo_state=[{"id": 1, "content": "핸들러 구현", "status": "in_progress"}],
    )

    print(state.get_resume_summary())
