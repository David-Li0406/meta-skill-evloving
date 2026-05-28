#!/usr/bin/env python3
"""
Debug State Manager for Hypothesis-Verification Debugging Process

Phase Gate Model:
D0 (Issue) -> D1 (Analyze) -> D2 (Plan) -> D3 (Verify) -> D4 (Fix)

Each phase has gate conditions that must be satisfied to advance.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Literal, TypedDict


class DebugHistory(TypedDict):
    phase: str
    timestamp: str
    data: dict


class DebugStateData(TypedDict):
    issue_id: str
    issue_description: str
    created_at: str
    current_phase: Literal["D0_ISSUE", "D1_ANALYZE", "D2_PLAN", "D3_VERIFY", "D4_FIX"]
    hypothesis: str | None
    hypothesis_count: int
    verification_plan: str | None
    verification_result: Literal["confirmed", "rejected"] | None
    hypothesis_confirmed: bool
    history: list[DebugHistory]


class DebugState:
    """Manages debug session state with phase gate enforcement."""

    PHASES = ["D0_ISSUE", "D1_ANALYZE", "D2_PLAN", "D3_VERIFY", "D4_FIX"]
    MIN_HYPOTHESIS_LENGTH = 20

    def __init__(self, project_root: Path | str):
        self.project_root = Path(project_root)
        self.debug_dir = self.project_root / ".debug"
        self.state_file = self.debug_dir / "state.json"
        self.hypotheses_dir = self.debug_dir / "hypotheses"
        self.evidence_dir = self.debug_dir / "evidence"
        self._state: DebugStateData | None = None

    def _ensure_dirs(self) -> None:
        """Create debug directories if they don't exist."""
        self.debug_dir.mkdir(parents=True, exist_ok=True)
        self.hypotheses_dir.mkdir(exist_ok=True)
        self.evidence_dir.mkdir(exist_ok=True)

    def _now(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()

    @property
    def state(self) -> DebugStateData | None:
        """Get current state, loading from file if needed."""
        if self._state is None and self.state_file.exists():
            self._state = json.loads(self.state_file.read_text(encoding="utf-8"))
        return self._state

    def save(self) -> None:
        """Save current state to file."""
        if self._state:
            self._ensure_dirs()
            self.state_file.write_text(
                json.dumps(self._state, indent=2, ensure_ascii=False), encoding="utf-8"
            )

    def has_active_session(self) -> bool:
        """Check if there's an active debug session."""
        return self.state is not None and self.state["current_phase"] != "D4_FIX"

    def start(self, issue_description: str, issue_id: str | None = None) -> dict:
        """
        Start a new debug session (D0).

        Returns:
            dict with 'success', 'phase', 'message'
        """
        if self.has_active_session():
            return {
                "success": False,
                "phase": self.state["current_phase"],
                "message": f"Active session exists. Use 'abort' first or continue from {self.state['current_phase']}",
            }

        self._ensure_dirs()

        if not issue_id:
            issue_id = f"DEBUG-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        self._state = {
            "issue_id": issue_id,
            "issue_description": issue_description,
            "created_at": self._now(),
            "current_phase": "D0_ISSUE",
            "hypothesis": None,
            "hypothesis_count": 0,
            "verification_plan": None,
            "verification_result": None,
            "hypothesis_confirmed": False,
            "history": [
                {
                    "phase": "D0_ISSUE",
                    "timestamp": self._now(),
                    "data": {"description": issue_description},
                }
            ],
        }
        self.save()

        return {
            "success": True,
            "phase": "D0_ISSUE",
            "message": f"Debug session started: {issue_id}",
            "next_action": "analyze - Write your hypothesis about the root cause",
        }

    def can_advance_to(self, target_phase: str) -> tuple[bool, str]:
        """
        Check if we can advance to the target phase.

        Returns:
            (can_advance, reason)
        """
        if not self.state:
            return False, "No active session. Start with 'debug start'"

        current = self.state["current_phase"]
        current_idx = self.PHASES.index(current)
        target_idx = self.PHASES.index(target_phase)

        # Can only advance one step at a time (except reject going back)
        if target_idx > current_idx + 1:
            return (
                False,
                f"Cannot skip phases. Current: {current}, Next: {self.PHASES[current_idx + 1]}",
            )

        # Gate conditions for each phase
        if target_phase == "D1_ANALYZE":
            if current != "D0_ISSUE":
                return False, "Must complete D0 (issue description) first"
            if not self.state["issue_description"]:
                return False, "Issue description required"
            return True, "Ready for analysis"

        elif target_phase == "D2_PLAN":
            if current != "D1_ANALYZE":
                return False, "Must complete D1 (hypothesis) first"
            hypothesis = self.state.get("hypothesis", "")
            if not hypothesis or len(hypothesis) < self.MIN_HYPOTHESIS_LENGTH:
                return (
                    False,
                    f"Hypothesis required (min {self.MIN_HYPOTHESIS_LENGTH} chars). Current: {len(hypothesis or '')} chars",
                )
            return True, "Ready for verification plan"

        elif target_phase == "D3_VERIFY":
            if current != "D2_PLAN":
                return False, "Must complete D2 (verification plan) first"
            if not self.state.get("verification_plan"):
                return False, "Verification plan required"
            return True, "Ready to verify"

        elif target_phase == "D4_FIX":
            if current != "D3_VERIFY":
                return False, "Must complete D3 (verification) first"
            if not self.state.get("hypothesis_confirmed"):
                return (
                    False,
                    "Hypothesis not confirmed. Verify first or reject and re-analyze",
                )
            return True, "Hypothesis confirmed. Ready to fix"

        return False, f"Unknown phase: {target_phase}"

    def set_hypothesis(self, hypothesis: str) -> dict:
        """
        Set hypothesis and advance to D1.

        Returns:
            dict with 'success', 'phase', 'message'
        """
        if not self.state:
            return {"success": False, "phase": None, "message": "No active session"}

        if len(hypothesis) < self.MIN_HYPOTHESIS_LENGTH:
            return {
                "success": False,
                "phase": self.state["current_phase"],
                "message": f"Hypothesis too short. Minimum {self.MIN_HYPOTHESIS_LENGTH} chars, got {len(hypothesis)}",
            }

        self._state["hypothesis"] = hypothesis
        self._state["hypothesis_count"] += 1
        self._state["current_phase"] = "D1_ANALYZE"
        self._state["history"].append(
            {
                "phase": "D1_ANALYZE",
                "timestamp": self._now(),
                "data": {
                    "hypothesis": hypothesis,
                    "count": self._state["hypothesis_count"],
                },
            }
        )
        self.save()

        # Save hypothesis to file
        hyp_file = (
            self.hypotheses_dir / f"{self._state['hypothesis_count']:03d}-hypothesis.md"
        )
        hyp_file.write_text(
            f"# Hypothesis #{self._state['hypothesis_count']}\n\n"
            f"**Created**: {self._now()}\n\n"
            f"## Hypothesis\n\n{hypothesis}\n\n"
            f"## Verification Result\n\n(pending)\n",
            encoding="utf-8",
        )

        return {
            "success": True,
            "phase": "D1_ANALYZE",
            "message": f"Hypothesis #{self._state['hypothesis_count']} recorded",
            "next_action": "plan - Design verification method",
        }

    def set_verification_plan(self, plan: str) -> dict:
        """
        Set verification plan and advance to D2.

        Returns:
            dict with 'success', 'phase', 'message'
        """
        can_advance, reason = self.can_advance_to("D2_PLAN")
        if not can_advance:
            return {
                "success": False,
                "phase": self.state["current_phase"],
                "message": reason,
            }

        self._state["verification_plan"] = plan
        self._state["current_phase"] = "D2_PLAN"
        self._state["history"].append(
            {
                "phase": "D2_PLAN",
                "timestamp": self._now(),
                "data": {"plan": plan},
            }
        )
        self.save()

        return {
            "success": True,
            "phase": "D2_PLAN",
            "message": "Verification plan recorded",
            "next_action": "verify - Execute plan and record result",
        }

    def set_verification_result(
        self, result: Literal["confirmed", "rejected"], evidence: str = ""
    ) -> dict:
        """
        Set verification result and advance to D3 or reject.

        Returns:
            dict with 'success', 'phase', 'message'
        """
        can_advance, reason = self.can_advance_to("D3_VERIFY")
        if not can_advance:
            return {
                "success": False,
                "phase": self.state["current_phase"],
                "message": reason,
            }

        self._state["verification_result"] = result
        self._state["current_phase"] = "D3_VERIFY"
        self._state["history"].append(
            {
                "phase": "D3_VERIFY",
                "timestamp": self._now(),
                "data": {"result": result, "evidence": evidence},
            }
        )

        # Save evidence
        if evidence:
            ev_file = (
                self.evidence_dir
                / f"{self._state['hypothesis_count']:03d}-evidence.txt"
            )
            ev_file.write_text(
                f"Hypothesis #{self._state['hypothesis_count']} Verification\n"
                f"Result: {result}\n"
                f"Timestamp: {self._now()}\n\n"
                f"Evidence:\n{evidence}\n",
                encoding="utf-8",
            )

        if result == "confirmed":
            self._state["hypothesis_confirmed"] = True
            self.save()
            return {
                "success": True,
                "phase": "D3_VERIFY",
                "message": "Hypothesis CONFIRMED",
                "next_action": "fix - Proceed to implement the fix",
            }
        else:
            # Check 3-strike rule
            if self._state["hypothesis_count"] >= 3:
                self.save()
                return {
                    "success": False,
                    "phase": "D3_VERIFY",
                    "message": "3 hypotheses rejected. Escalate to /issue failed",
                    "escalate": True,
                }

            # Reset for new hypothesis
            self._state["hypothesis"] = None
            self._state["verification_plan"] = None
            self._state["verification_result"] = None
            self._state["current_phase"] = "D0_ISSUE"  # Back to start of cycle
            self.save()

            return {
                "success": True,
                "phase": "D0_ISSUE",
                "message": f"Hypothesis REJECTED ({self._state['hypothesis_count']}/3). Back to analysis",
                "next_action": "analyze - Write a new hypothesis",
            }

    def advance_to_fix(self) -> dict:
        """
        Advance to D4 (fix allowed).

        Returns:
            dict with 'success', 'phase', 'message'
        """
        can_advance, reason = self.can_advance_to("D4_FIX")
        if not can_advance:
            return {
                "success": False,
                "phase": self.state["current_phase"],
                "message": reason,
            }

        self._state["current_phase"] = "D4_FIX"
        self._state["history"].append(
            {
                "phase": "D4_FIX",
                "timestamp": self._now(),
                "data": {},
            }
        )
        self.save()

        return {
            "success": True,
            "phase": "D4_FIX",
            "message": "Fix phase reached. You may now implement the fix.",
        }

    def get_status(self) -> dict:
        """Get current debug session status."""
        if not self.state:
            return {"active": False, "message": "No active debug session"}

        return {
            "active": True,
            "issue_id": self.state["issue_id"],
            "issue_description": self.state["issue_description"],
            "current_phase": self.state["current_phase"],
            "hypothesis": self.state.get("hypothesis"),
            "hypothesis_count": self.state["hypothesis_count"],
            "verification_plan": self.state.get("verification_plan"),
            "verification_result": self.state.get("verification_result"),
            "hypothesis_confirmed": self.state["hypothesis_confirmed"],
            "history_count": len(self.state["history"]),
        }

    def abort(self) -> dict:
        """Abort current debug session."""
        if not self.state:
            return {"success": False, "message": "No active session to abort"}

        issue_id = self.state["issue_id"]

        # Archive the state
        archive_file = self.debug_dir / f"archived-{issue_id}.json"
        archive_file.write_text(
            json.dumps(self._state, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # Remove active state
        self.state_file.unlink()
        self._state = None

        return {
            "success": True,
            "message": f"Session {issue_id} aborted and archived",
        }


def main():
    """CLI entry point for testing."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: debug_state.py <project_root> <command> [args]")
        print("Commands: start, analyze, plan, verify, fix, status, abort")
        sys.exit(1)

    project_root = Path(sys.argv[1])
    command = sys.argv[2] if len(sys.argv) > 2 else "status"

    state = DebugState(project_root)

    if command == "status":
        print(json.dumps(state.get_status(), indent=2, ensure_ascii=False))
    elif command == "start":
        desc = sys.argv[3] if len(sys.argv) > 3 else "No description"
        print(json.dumps(state.start(desc), indent=2, ensure_ascii=False))
    elif command == "abort":
        print(json.dumps(state.abort(), indent=2, ensure_ascii=False))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
