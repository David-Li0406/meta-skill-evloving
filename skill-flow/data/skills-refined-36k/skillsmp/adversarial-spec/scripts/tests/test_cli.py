"""Tests for CLI argument parsing and command routing."""

import json
import sys
import tempfile
from io import StringIO
from pathlib import Path
from unittest.mock import patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestCLIProviders:
    def test_providers_command(self):
        """Test that providers command runs without error."""
        import debate

        with patch("sys.argv", ["debate.py", "providers"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                debate.main()
                output = mock_stdout.getvalue()
                assert "OpenAI" in output
                assert "OPENAI_API_KEY" in output


class TestCLIFocusAreas:
    def test_focus_areas_command(self):
        """Test that focus-areas command lists all areas."""
        import debate

        with patch("sys.argv", ["debate.py", "focus-areas"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                debate.main()
                output = mock_stdout.getvalue()
                assert "security" in output
                assert "scalability" in output
                assert "performance" in output


class TestCLIPersonas:
    def test_personas_command(self):
        """Test that personas command lists all personas."""
        import debate

        with patch("sys.argv", ["debate.py", "personas"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                debate.main()
                output = mock_stdout.getvalue()
                assert "security-engineer" in output
                assert "oncall-engineer" in output


class TestCLISessions:
    def test_sessions_command_empty(self):
        """Test sessions command with no sessions."""
        import debate

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("session.SESSIONS_DIR", Path(tmpdir) / "sessions"):
                with patch("debate.SESSIONS_DIR", Path(tmpdir) / "sessions"):
                    with patch("sys.argv", ["debate.py", "sessions"]):
                        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                            debate.main()
                            output = mock_stdout.getvalue()
                            assert "No sessions found" in output


class TestCLIDiff:
    def test_diff_command(self):
        """Test diff between two files."""
        import debate

        with tempfile.TemporaryDirectory() as tmpdir:
            prev = Path(tmpdir) / "prev.md"
            curr = Path(tmpdir) / "curr.md"
            prev.write_text("line1\nline2\n")
            curr.write_text("line1\nmodified\n")

            with patch(
                "sys.argv",
                ["debate.py", "diff", "--previous", str(prev), "--current", str(curr)],
            ):
                with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                    debate.main()
                    output = mock_stdout.getvalue()
                    assert "-line2" in output
                    assert "+modified" in output


class TestCLISaveProfile:
    def test_save_profile_command(self):
        """Test saving a profile."""
        import debate

        with tempfile.TemporaryDirectory() as tmpdir:
            profiles_dir = Path(tmpdir) / "profiles"

            with patch("providers.PROFILES_DIR", profiles_dir):
                with patch(
                    "sys.argv",
                    [
                        "debate.py",
                        "save-profile",
                        "test-profile",
                        "--models",
                        "gpt-4o,gemini/gemini-2.0-flash",
                        "--focus",
                        "security",
                    ],
                ):
                    with patch("sys.stdout", new_callable=StringIO):
                        debate.main()

                        # Verify profile was saved
                        profile_path = profiles_dir / "test-profile.json"
                        assert profile_path.exists()

                        data = json.loads(profile_path.read_text())
                        assert data["models"] == "gpt-4o,gemini/gemini-2.0-flash"
                        assert data["focus"] == "security"


class TestCLICritique:
    @patch("debate.validate_models_before_run")
    @patch("debate.call_models_parallel")
    def test_critique_with_json_output(self, mock_call, mock_validate):
        """Test critique command with JSON output."""
        import debate
        from models import ModelResponse

        # Mock validation to not check API keys in tests
        mock_validate.return_value = None

        mock_call.return_value = [
            ModelResponse(
                model="gpt-4o",
                response="Critique here.\n[SPEC]\n# Revised\n[/SPEC]",
                agreed=False,
                spec="# Revised",
                input_tokens=100,
                output_tokens=50,
                cost=0.01,
            )
        ]

        with patch("sys.stdin", StringIO("# Test Spec\n\nContent here.")):
            with patch(
                "sys.argv", ["debate.py", "critique", "--models", "gpt-4o", "--json"]
            ):
                with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                    with patch("sys.stderr", new_callable=StringIO):
                        debate.main()
                        output = mock_stdout.getvalue()

                        data = json.loads(output)
                        assert data["round"] == 1
                        assert data["models"] == ["gpt-4o"]
                        assert len(data["results"]) == 1
                        assert data["results"][0]["model"] == "gpt-4o"

    @patch("debate.validate_models_before_run")
    @patch("debate.call_models_parallel")
    def test_critique_with_all_agree(self, mock_call, mock_validate):
        """Test critique when all models agree."""
        import debate
        from models import ModelResponse

        # Mock validation to not check API keys in tests
        mock_validate.return_value = None

        mock_call.return_value = [
            ModelResponse(
                model="gpt-4o",
                response="[AGREE]\n[SPEC]\n# Final\n[/SPEC]",
                agreed=True,
                spec="# Final",
                input_tokens=100,
                output_tokens=50,
                cost=0.01,
            ),
            ModelResponse(
                model="gemini/gemini-2.0-flash",
                response="[AGREE]\n[SPEC]\n# Final\n[/SPEC]",
                agreed=True,
                spec="# Final",
                input_tokens=80,
                output_tokens=40,
                cost=0.005,
            ),
        ]

        with patch("sys.stdin", StringIO("# Test Spec")):
            with patch(
                "sys.argv",
                [
                    "debate.py",
                    "critique",
                    "--models",
                    "gpt-4o,gemini/gemini-2.0-flash",
                    "--json",
                ],
            ):
                with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                    with patch("sys.stderr", new_callable=StringIO):
                        debate.main()
                        output = mock_stdout.getvalue()

                        data = json.loads(output)
                        assert data["all_agreed"] is True

    @patch("debate.validate_models_before_run")
    @patch("debate.call_models_parallel")
    def test_critique_passes_options(self, mock_call, mock_validate):
        """Test that CLI options are passed to model calls."""
        import debate
        from models import ModelResponse

        # Mock validation to not check API keys in tests
        mock_validate.return_value = None

        mock_call.return_value = [
            ModelResponse(
                model="gpt-4o",
                response="[AGREE]\n[SPEC]\n# Spec\n[/SPEC]",
                agreed=True,
                spec="# Spec",
            )
        ]

        with patch("sys.stdin", StringIO("# Spec")):
            with patch(
                "sys.argv",
                [
                    "debate.py",
                    "critique",
                    "--models",
                    "gpt-4o",
                    "--focus",
                    "security",
                    "--persona",
                    "security-engineer",
                    "--preserve-intent",
                    "--json",
                ],
            ):
                with patch("sys.stdout", new_callable=StringIO):
                    with patch("sys.stderr", new_callable=StringIO):
                        debate.main()

                        # Verify options were passed (positional args)
                        # call_models_parallel(models, spec, round_num, doc_type, press,
                        #                      focus, persona, context, preserve_intent, ...)
                        call_args = mock_call.call_args[0]
                        assert call_args[0] == ["gpt-4o"]  # models
                        assert call_args[5] == "security"  # focus
                        assert call_args[6] == "security-engineer"  # persona
                        assert call_args[8] is True  # preserve_intent


class TestCLIBedrock:
    def test_bedrock_status_not_configured(self):
        """Test bedrock status when not configured."""
        import debate

        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.json"

            with patch("providers.GLOBAL_CONFIG_PATH", config_path):
                with patch("sys.argv", ["debate.py", "bedrock", "status"]):
                    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                        debate.main()
                        output = mock_stdout.getvalue()
                        assert "Not configured" in output

    def test_bedrock_enable(self):
        """Test enabling bedrock mode."""
        import debate

        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "adversarial-spec" / "config.json"

            with patch("providers.GLOBAL_CONFIG_PATH", config_path):
                with patch(
                    "sys.argv",
                    ["debate.py", "bedrock", "enable", "--region", "us-east-1"],
                ):
                    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                        debate.main()
                        output = mock_stdout.getvalue()
                        assert "enabled" in output.lower()

                        # Verify config was written
                        assert config_path.exists()
                        data = json.loads(config_path.read_text())
                        assert data["bedrock"]["enabled"] is True
                        assert data["bedrock"]["region"] == "us-east-1"


class TestCreateParser:
    def test_creates_parser_with_all_actions(self):
        """Test that parser includes all expected actions."""
        import debate

        parser = debate.create_parser()
        # Parse with a valid action to verify it works
        args = parser.parse_args(["providers"])
        assert args.action == "providers"

    def test_default_values(self):
        """Test default argument values."""
        import debate

        parser = debate.create_parser()
        args = parser.parse_args(["critique"])
        assert args.models is None  # Now dynamically detected based on API keys
        assert args.doc_type == "tech"
        assert args.round == 1
        assert args.timeout == 600


class TestHandleInfoCommand:
    def test_returns_false_for_non_info_command(self):
        """Test that non-info commands return False."""
        import debate

        parser = debate.create_parser()
        args = parser.parse_args(["critique"])
        result = debate.handle_info_command(args)
        assert result is False

    def test_returns_true_for_providers(self):
        """Test that providers command is handled."""
        import debate

        parser = debate.create_parser()
        args = parser.parse_args(["providers"])
        with patch("sys.stdout", new_callable=StringIO):
            result = debate.handle_info_command(args)
        assert result is True


class TestHandleUtilityCommand:
    def test_returns_false_for_non_utility_command(self):
        """Test that non-utility commands return False."""
        import debate

        parser = debate.create_parser()
        args = parser.parse_args(["critique"])
        result = debate.handle_utility_command(args)
        assert result is False

    def test_diff_without_files_exits(self):
        """Test that diff without --previous/--current exits."""
        import debate
        import pytest

        parser = debate.create_parser()
        args = parser.parse_args(["diff"])
        with pytest.raises(SystemExit) as exc_info:
            with patch("sys.stderr", new_callable=StringIO):
                debate.handle_utility_command(args)
        assert exc_info.value.code == 1


class TestApplyProfile:
    def test_no_profile_does_nothing(self):
        """Test that no profile arg leaves args unchanged."""
        import debate

        parser = debate.create_parser()
        args = parser.parse_args(["critique", "--models", "gpt-4o"])
        original_models = args.models
        debate.apply_profile(args)
        assert args.models == original_models

    def test_profile_overrides_defaults(self):
        """Test that profile values override defaults."""
        import debate

        with tempfile.TemporaryDirectory() as tmpdir:
            profiles_dir = Path(tmpdir)
            profile_path = profiles_dir / "test.json"
            profile_path.write_text(
                json.dumps(
                    {
                        "models": "claude-3-opus",
                        "doc_type": "prd",
                        "focus": "security",
                    }
                )
            )

            with patch("providers.PROFILES_DIR", profiles_dir):
                parser = debate.create_parser()
                args = parser.parse_args(["critique", "--profile", "test"])
                debate.apply_profile(args)
                assert args.models == "claude-3-opus"
                assert args.doc_type == "prd"
                assert args.focus == "security"


class TestParseModels:
    def test_parses_single_model(self):
        """Test parsing single model."""
        import debate

        parser = debate.create_parser()
        args = parser.parse_args(["critique", "--models", "gpt-4o"])
        models = debate.parse_models(args)
        assert models == ["gpt-4o"]

    def test_parses_multiple_models(self):
        """Test parsing comma-separated models."""
        import debate

        parser = debate.create_parser()
        args = parser.parse_args(["critique", "--models", "gpt-4o, claude-3, gemini"])
        models = debate.parse_models(args)
        assert models == ["gpt-4o", "claude-3", "gemini"]

    def test_empty_models_exits(self):
        """Test that empty models list exits."""
        import debate
        import pytest

        parser = debate.create_parser()
        args = parser.parse_args(["critique", "--models", ""])
        with pytest.raises(SystemExit) as exc_info:
            with patch("sys.stderr", new_callable=StringIO):
                debate.parse_models(args)
        assert exc_info.value.code == 1


class TestOutputResults:
    def test_json_output_format(self):
        """Test JSON output format."""
        import debate
        from models import ModelResponse

        parser = debate.create_parser()
        args = parser.parse_args(["critique", "--json"])

        results = [
            ModelResponse(
                model="gpt-4o",
                response="test",
                agreed=True,
                spec="spec",
            )
        ]

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            debate.output_results(args, results, ["gpt-4o"], True, None, None)
            output = json.loads(mock_stdout.getvalue())
            assert output["all_agreed"] is True
            assert output["models"] == ["gpt-4o"]

    def test_text_output_format(self):
        """Test text output format."""
        import debate
        from models import ModelResponse

        parser = debate.create_parser()
        args = parser.parse_args(["critique"])

        results = [
            ModelResponse(
                model="gpt-4o",
                response="Critique text",
                agreed=False,
                spec="spec",
            )
        ]

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            debate.output_results(args, results, ["gpt-4o"], False, None, None)
            output = mock_stdout.getvalue()
            assert "Round 1 Results" in output
            assert "gpt-4o" in output
            assert "Critique text" in output


class TestHandleInfoCommandSessions:
    """Tests for sessions command in handle_info_command.

    Mutation targets:
    - sessions list logic
    - empty sessions check
    """

    def test_sessions_with_data(self):
        import debate

        with tempfile.TemporaryDirectory() as tmpdir:
            sessions_dir = Path(tmpdir) / "sessions"
            sessions_dir.mkdir()
            # Create a session file with correct structure
            session_path = sessions_dir / "test-session.json"
            session_data = {
                "session_id": "test-session",
                "round": 2,
                "doc_type": "tech",
                "updated_at": "2025-01-11T12:00:00",
                "spec": "# Test spec",
                "history": [],
            }
            session_path.write_text(json.dumps(session_data))

            with patch("session.SESSIONS_DIR", sessions_dir):
                with patch("debate.SESSIONS_DIR", sessions_dir):
                    with patch("sys.argv", ["debate.py", "sessions"]):
                        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                            debate.main()
                            output = mock_stdout.getvalue()
                            assert "test-session" in output
                            assert "round: 2" in output


class TestHandleUtilityCommandEdgeCases:
    """Tests for handle_utility_command edge cases.

    Mutation targets:
    - save-profile without name
    - diff file read error
    """

    def test_save_profile_without_name_exits(self):
        import debate
        import pytest

        parser = debate.create_parser()
        args = parser.parse_args(["save-profile"])
        args.profile_name = None

        with pytest.raises(SystemExit) as exc_info:
            debate.handle_utility_command(args)
        assert exc_info.value.code == 1

    def test_diff_with_nonexistent_file(self):
        import debate
        import pytest

        parser = debate.create_parser()
        args = parser.parse_args(
            [
                "diff",
                "--previous",
                "/nonexistent/prev.md",
                "--current",
                "/nonexistent/curr.md",
            ]
        )

        with pytest.raises(SystemExit) as exc_info:
            with patch("sys.stderr", new_callable=StringIO):
                debate.handle_utility_command(args)
        assert exc_info.value.code == 1

    def test_diff_no_differences(self):
        import debate

        with tempfile.TemporaryDirectory() as tmpdir:
            prev = Path(tmpdir) / "prev.md"
            curr = Path(tmpdir) / "curr.md"
            prev.write_text("same content")
            curr.write_text("same content")

            parser = debate.create_parser()
            args = parser.parse_args(
                ["diff", "--previous", str(prev), "--current", str(curr)]
            )

            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = debate.handle_utility_command(args)
                assert result is True
                assert "No differences" in mock_stdout.getvalue()


class TestApplyProfileAllFields:
    """Tests for apply_profile with all fields.

    Mutation targets:
    - context field
    - preserve_intent field
    """

    def test_applies_context_from_profile(self):
        import debate

        with tempfile.TemporaryDirectory() as tmpdir:
            profiles_dir = Path(tmpdir)
            profile_path = profiles_dir / "test.json"
            profile_path.write_text(
                json.dumps(
                    {
                        "models": "gpt-4o",
                        "context": "/some/context.md",
                    }
                )
            )

            with patch("providers.PROFILES_DIR", profiles_dir):
                parser = debate.create_parser()
                args = parser.parse_args(["critique", "--profile", "test"])
                debate.apply_profile(args)
                # Mutation: not setting context would leave it empty
                assert args.context == "/some/context.md"

    def test_applies_preserve_intent_from_profile(self):
        import debate

        with tempfile.TemporaryDirectory() as tmpdir:
            profiles_dir = Path(tmpdir)
            profile_path = profiles_dir / "test.json"
            profile_path.write_text(
                json.dumps(
                    {
                        "models": "gpt-4o",
                        "preserve_intent": True,
                    }
                )
            )

            with patch("providers.PROFILES_DIR", profiles_dir):
                parser = debate.create_parser()
                args = parser.parse_args(["critique", "--profile", "test"])
                debate.apply_profile(args)
                # Mutation: not setting preserve_intent would leave it False
                assert args.preserve_intent is True


class TestSetupBedrock:
    """Tests for setup_bedrock function.

    Mutation targets:
    - bedrock mode detection
    - model validation
    """

    def test_returns_original_models_when_not_bedrock(self):
        import debate

        parser = debate.create_parser()
        args = parser.parse_args(["critique", "--models", "gpt-4o"])
        models = ["gpt-4o"]

        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.json"

            with patch("providers.GLOBAL_CONFIG_PATH", config_path):
                new_models, bedrock_mode, region = debate.setup_bedrock(args, models)
                assert new_models == ["gpt-4o"]
                assert bedrock_mode is False
                assert region is None


class TestSendTelegramNotification:
    """Tests for send_telegram_notification function.

    Mutation targets:
    - telegram config check
    - message formatting
    - poll logic
    """

    @patch("telegram_bot.poll_for_reply")
    @patch("telegram_bot.send_long_message")
    @patch("telegram_bot.get_last_update_id")
    @patch("telegram_bot.get_config")
    def test_sends_notification_and_returns_feedback(
        self, mock_config, mock_last_id, mock_send, mock_poll
    ):
        import debate
        from models import ModelResponse

        mock_config.return_value = ("token", "123")
        mock_last_id.return_value = 0
        mock_send.return_value = True
        mock_poll.return_value = "User feedback"

        results = [
            ModelResponse(
                model="gpt-4o",
                response="Critique here",
                agreed=False,
                spec="# Spec",
            )
        ]

        feedback = debate.send_telegram_notification(["gpt-4o"], 1, results, 60)
        assert feedback == "User feedback"

    @patch("telegram_bot.get_config")
    def test_returns_none_when_not_configured(self, mock_config):
        import debate
        from models import ModelResponse

        mock_config.return_value = ("", "")

        results = [
            ModelResponse(model="gpt-4o", response="test", agreed=True, spec="spec")
        ]

        with patch("sys.stderr", new_callable=StringIO):
            feedback = debate.send_telegram_notification(["gpt-4o"], 1, results, 60)
        assert feedback is None

    @patch("telegram_bot.poll_for_reply")
    @patch("telegram_bot.send_long_message")
    @patch("telegram_bot.get_last_update_id")
    @patch("telegram_bot.get_config")
    def test_handles_all_agree(self, mock_config, mock_last_id, mock_send, mock_poll):
        import debate
        from models import ModelResponse

        mock_config.return_value = ("token", "123")
        mock_last_id.return_value = 0
        mock_send.return_value = True
        mock_poll.return_value = None

        results = [
            ModelResponse(model="gpt-4o", response="[AGREE]", agreed=True, spec="spec"),
            ModelResponse(model="gemini", response="[AGREE]", agreed=True, spec="spec"),
        ]

        feedback = debate.send_telegram_notification(
            ["gpt-4o", "gemini"], 1, results, 60
        )
        assert feedback is None
        # Check message was sent with ALL AGREE status
        call_args = mock_send.call_args
        assert "ALL AGREE" in call_args[0][2]

    @patch("telegram_bot.poll_for_reply")
    @patch("telegram_bot.send_long_message")
    @patch("telegram_bot.get_last_update_id")
    @patch("telegram_bot.get_config")
    def test_handles_error_response(
        self, mock_config, mock_last_id, mock_send, mock_poll
    ):
        import debate
        from models import ModelResponse

        mock_config.return_value = ("token", "123")
        mock_last_id.return_value = 0
        mock_send.return_value = True
        mock_poll.return_value = None

        results = [
            ModelResponse(
                model="gpt-4o",
                response="",
                agreed=False,
                spec="",
                error="API timeout",
            )
        ]

        debate.send_telegram_notification(["gpt-4o"], 1, results, 60)
        call_args = mock_send.call_args
        assert "ERROR" in call_args[0][2]
