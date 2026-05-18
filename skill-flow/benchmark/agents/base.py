"""
Shared base class and utilities for evaluation agents.
"""

import shlex
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from harbor.agents.installed.base import ExecInput
from harbor.agents.installed.codex import Codex
from harbor.models.trial.paths import EnvironmentPaths

# Separator used in trial directory names: "task-name__hash"
TASK_NAME_SEPARATOR = "__"


@dataclass(frozen=True)
class McpServer:
    """MCP server configuration for Codex agents."""

    name: str
    url: str


def get_project_root() -> Path:
    """Get the project root directory (skill-flow/)."""
    return Path(__file__).parent.parent.parent


class BaseCodexAgent(Codex):
    """
    Shared base class for evaluation Codex agents.

    Provides common utilities for template rendering and AGENTS.md upload.
    """

    def __init__(
        self,
        *args: Any,
        reasoning_effort: str | None = None,
        mcp_servers: list[McpServer] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.reasoning_effort = reasoning_effort
        self._mcp_servers = mcp_servers or []

    def _build_codex_command(self, model: str, escaped_instruction: str) -> str:
        """Build the codex exec command string.

        Forces ``--model gpt-5.4`` because:
        * the harbor agent installs codex@0.79 which defaults to
          ``gpt-5.2-codex`` — that model is rejected by the ChatGPT account
          ("not supported when using Codex with a ChatGPT account") and
          aborts the agent after ~3 seconds with zero useful work;
        * locally-tested ChatGPT-auth-allowed model is ``gpt-5.4``.
        The ``model`` argument from harbor's config (``openai/gpt-5-codex``
        etc.) is intentionally ignored — ChatGPT-auth doesn't honor it.
        """
        del model
        parts = [
            "codex exec",
            "--dangerously-bypass-approvals-and-sandbox",
            "--skip-git-repo-check",
            "--model gpt-5.4",
        ]

        if self.reasoning_effort:
            parts.append(f'--config model_reasoning_effort="{self.reasoning_effort}"')

        parts.extend(
            [
                "--json",
                "--",
                escaped_instruction,
                "2>&1 </dev/null | tee",
                str(EnvironmentPaths.agent_dir / self._OUTPUT_FILENAME),
                "&& rm -rf $CODEX_HOME/auth.json",
            ]
        )

        return " ".join(parts)

    def _build_mcp_registration_commands(self) -> str:
        """Build shell commands to register MCP servers with Codex."""
        lines: list[str] = []
        for server in self._mcp_servers:
            lines.append(f"codex mcp add {server.name} --url {server.url}")
        return "\n".join(lines)

    def create_run_agent_commands(self, instruction: str) -> list[ExecInput]:
        """
        Create commands to run the Codex agent.

        Optionally includes reasoning_effort config if specified.
        """
        escaped_instruction = shlex.quote(instruction)

        if not self.model_name:
            raise ValueError("Model name is required")

        model = self.model_name.split("/")[-1]

        # Use the local ChatGPT subscription auth from ~/.codex/auth.json
        # so the agent runs under the user's ChatGPT plan. OPENAI_API_KEY is
        # intentionally NOT forwarded — it is reserved for the skill retriever.
        codex_auth_json = (Path.home() / ".codex" / "auth.json").read_text(
            encoding="utf-8"
        )

        env = {
            "CODEX_AUTH_JSON": codex_auth_json,
            "CODEX_HOME": (EnvironmentPaths.agent_dir).as_posix(),
        }

        setup_command = (
            'printf %s "$CODEX_AUTH_JSON" >"$CODEX_HOME/auth.json"'
        )

        if self._mcp_servers:
            setup_command += "\n" + self._build_mcp_registration_commands()

        return [
            ExecInput(command=setup_command, env=env),
            ExecInput(
                command=self._build_codex_command(model, escaped_instruction),
                env=env,
            ),
        ]
