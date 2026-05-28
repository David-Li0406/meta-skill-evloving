"""
Tests for the onboarding module.

Tests interactive init, login, logout, and env file management.
"""
import os
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import directly from the module file to avoid tools/__init__.py issues
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
import onboarding
from onboarding import (
    save_api_key_to_env,
    logout,
    open_signup_in_browser,
    uninstall,
    verify_connection,
    interactive_init,
    prompt_for_api_key,
    display_welcome_message,
)


class TestEnvManagement:
    """Tests for .env file management."""

    def test_save_api_key_creates_env(self, tmp_path):
        """Test that save_api_key_to_env creates .env file if it doesn't exist."""
        env_file = tmp_path / ".env"
        with patch.object(onboarding, "ENV_FILE_NAME", str(env_file)):
            success = save_api_key_to_env("test-key-123")
            assert success is True
            assert env_file.exists()
            assert "ROBYNN_API_KEY=test-key-123" in env_file.read_text()

    def test_save_api_key_updates_existing(self, tmp_path):
        """Test that save_api_key_to_env updates an existing key."""
        env_file = tmp_path / ".env"
        env_file.write_text("OTHER_VAR=value\nROBYNN_API_KEY=old-key\n")
        
        with patch.object(onboarding, "ENV_FILE_NAME", str(env_file)):
            success = save_api_key_to_env("new-key-456")
            assert success is True
            content = env_file.read_text()
            assert "ROBYNN_API_KEY=new-key-456" in content
            assert "ROBYNN_API_KEY=old-key" not in content
            assert "OTHER_VAR=value" in content

    def test_save_preserves_other_keys(self, tmp_path):
        """Test that save_api_key_to_env preserves other environment variables."""
        env_file = tmp_path / ".env"
        env_file.write_text("FOO=bar\nBAZ=qux\n")
        
        with patch.object(onboarding, "ENV_FILE_NAME", str(env_file)):
            success = save_api_key_to_env("new-key-789")
            assert success is True
            content = env_file.read_text()
            assert "ROBYNN_API_KEY=new-key-789" in content
            assert "FOO=bar" in content
            assert "BAZ=qux" in content

    def test_logout_removes_key(self, tmp_path):
        """Test that logout removes the key from .env."""
        env_file = tmp_path / ".env"
        env_file.write_text("OTHER_VAR=value\nROBYNN_API_KEY=some-key\n")
        
        with patch.object(onboarding, "ENV_FILE_NAME", str(env_file)):
            success = logout()
            assert success is True
            content = env_file.read_text()
            assert "ROBYNN_API_KEY" not in content
            assert "OTHER_VAR=value" in content

    def test_logout_not_logged_in(self, tmp_path):
        """Test logout when .env doesn't exist."""
        env_file = tmp_path / "nonexistent_env"
        with patch.object(onboarding, "ENV_FILE_NAME", str(env_file)):
            success = logout()
            assert success is False

    def test_logout_when_no_key_in_env(self, tmp_path):
        """Test logout when .env exists but has no ROBYNN_API_KEY."""
        env_file = tmp_path / ".env"
        env_file.write_text("OTHER_VAR=value\n")
        
        with patch.object(onboarding, "ENV_FILE_NAME", str(env_file)):
            success = logout()
            assert success is False


class TestBrowserOpener:
    """Tests for browser opening functionality."""

    @patch("onboarding.webbrowser.open")
    def test_open_signup_basic(self, mock_open):
        """Test open_signup_in_browser without domain."""
        open_signup_in_browser()
        mock_open.assert_called_once()
        url = mock_open.call_args[0][0]
        assert "robynn.ai/signup" in url
        assert "ref=cli" in url

    @patch("onboarding.webbrowser.open")
    def test_open_signup_with_domain(self, mock_open):
        """Test open_signup_in_browser with domain."""
        open_signup_in_browser("example.com")
        mock_open.assert_called_once()
        url = mock_open.call_args[0][0]
        assert "domain=example.com" in url

    @patch("onboarding.webbrowser.open")
    def test_signup_url_includes_ref_param(self, mock_open):
        """Test signup URL includes ref=cli for attribution."""
        open_signup_in_browser()
        url = mock_open.call_args[0][0]
        assert "ref=cli" in url


class TestConnectionVerification:
    """Tests for API key verification."""

    @patch.object(onboarding, "RobynnClient")
    def test_verify_connection_success(self, mock_client_class):
        """Test verify_connection with valid key."""
        mock_instance = mock_client_class.return_value
        mock_instance.validate_key.return_value = True
        
        result = verify_connection("valid-key")
        assert result is True
        mock_instance.validate_key.assert_called_once_with("valid-key")

    @patch.object(onboarding, "RobynnClient")
    def test_verify_connection_failure(self, mock_client_class):
        """Test verify_connection with invalid key."""
        mock_instance = mock_client_class.return_value
        mock_instance.validate_key.return_value = False
        
        result = verify_connection("invalid-key")
        assert result is False


class TestInteractiveInit:
    """Tests for the interactive init wizard."""

    @patch.object(onboarding, "save_api_key_to_env", return_value=True)
    @patch.object(onboarding, "verify_connection", return_value=True)
    def test_init_with_api_key_argument(self, mock_verify, mock_save):
        """Test init with API key passed directly."""
        # API key starting with rb_ should be recognized
        result = interactive_init("rb_test_key_12345678901234567890")
        assert result is True
        mock_verify.assert_called_once()
        mock_save.assert_called_once()

    @patch.object(onboarding, "save_api_key_to_env", return_value=True)
    @patch.object(onboarding, "verify_connection", return_value=True)
    @patch.object(onboarding, "prompt_for_api_key", return_value="test-key")
    @patch.object(onboarding, "display_welcome_message")
    @patch("builtins.input", return_value="y")
    @patch("sys.stdin")
    def test_init_with_existing_key_flow(
        self, mock_stdin, mock_input, mock_welcome, mock_prompt, mock_verify, mock_save
    ):
        """Test flow when user already has API key."""
        mock_stdin.isatty.return_value = True
        result = interactive_init()
        assert result is True
        mock_verify.assert_called_once_with("test-key")
        mock_save.assert_called_once_with("test-key")

    @patch.object(onboarding, "save_api_key_to_env", return_value=True)
    @patch.object(onboarding, "verify_connection", return_value=True)
    @patch.object(onboarding, "prompt_for_api_key", return_value="test-key")
    @patch.object(onboarding, "open_signup_in_browser")
    @patch.object(onboarding, "display_welcome_message")
    @patch("builtins.input", return_value="n")
    @patch("sys.stdin")
    def test_init_opens_browser_when_no_key(
        self, mock_stdin, mock_input, mock_welcome, mock_browser, mock_prompt, mock_verify, mock_save
    ):
        """Test browser opens to signup URL when user doesn't have key."""
        mock_stdin.isatty.return_value = True
        result = interactive_init("mycompany.com")
        mock_browser.assert_called_once_with("mycompany.com")

    @patch.object(onboarding, "verify_connection", return_value=False)
    @patch.object(onboarding, "prompt_for_api_key", return_value="invalid-key")
    @patch.object(onboarding, "display_welcome_message")
    @patch("builtins.input", return_value="y")
    @patch("sys.stdin")
    def test_init_handles_invalid_key(
        self, mock_stdin, mock_input, mock_welcome, mock_prompt, mock_verify
    ):
        """Test error message when key validation fails."""
        mock_stdin.isatty.return_value = True
        result = interactive_init()
        assert result is False

    @patch.object(onboarding, "prompt_for_api_key", return_value=None)
    @patch.object(onboarding, "display_welcome_message")
    @patch("builtins.input", return_value="y")
    @patch("sys.stdin")
    def test_init_handles_cancelled_input(
        self, mock_stdin, mock_input, mock_welcome, mock_prompt
    ):
        """Test cancellation when user doesn't provide key."""
        mock_stdin.isatty.return_value = True
        result = interactive_init()
        assert result is False

    @patch.object(onboarding, "display_welcome_message")
    @patch("sys.stdin")
    def test_init_non_interactive_shows_instructions(
        self, mock_stdin, mock_welcome, capsys
    ):
        """Test non-interactive mode shows setup instructions."""
        mock_stdin.isatty.return_value = False
        result = interactive_init()
        assert result is False
        captured = capsys.readouterr()
        assert "Option 1" in captured.out or "Manual Configuration" in captured.out


class TestUninstall:
    """Tests for plugin uninstallation."""

    @patch("builtins.input", return_value="y")
    def test_uninstall_removes_directory(self, mock_input, tmp_path):
        """Test uninstall removes a valid plugin directory when confirmed."""
        plugin_dir = tmp_path / "rory"
        plugin_dir.mkdir()
        (plugin_dir / "tools").mkdir()
        (plugin_dir / "rory.py").write_text("# test file")

        success = uninstall(str(plugin_dir))
        assert success is True
        assert not plugin_dir.exists()

    @patch("builtins.input", return_value="n")
    def test_uninstall_cancelled(self, mock_input, tmp_path):
        """Test uninstall does nothing when cancelled."""
        plugin_dir = tmp_path / "rory"
        plugin_dir.mkdir()
        (plugin_dir / "tools").mkdir()
        (plugin_dir / "rory.py").write_text("# test file")

        success = uninstall(str(plugin_dir))
        assert success is False
        assert plugin_dir.exists()

    def test_uninstall_safety_check(self, tmp_path):
        """Test uninstall fails safety check for non-plugin directory."""
        not_plugin_dir = tmp_path / "not_rory"
        not_plugin_dir.mkdir()

        success = uninstall(str(not_plugin_dir))
        assert success is False

    def test_uninstall_nonexistent_directory(self, tmp_path):
        """Test uninstall handles non-existent directory."""
        nonexistent_dir = tmp_path / "nonexistent"
        success = uninstall(str(nonexistent_dir))
        assert success is False


class TestPromptForApiKey:
    """Tests for API key prompt."""

    @patch("builtins.input", return_value="my-api-key-123")
    def test_prompt_returns_key(self, mock_input):
        """Test prompt returns the entered key."""
        result = prompt_for_api_key()
        assert result == "my-api-key-123"

    @patch("builtins.input", return_value="  spaced-key  ")
    def test_prompt_strips_whitespace(self, mock_input):
        """Test prompt strips whitespace from key."""
        result = prompt_for_api_key()
        assert result == "spaced-key"

    @patch("builtins.input", return_value="")
    def test_prompt_returns_none_for_empty(self, mock_input):
        """Test prompt returns None for empty input."""
        result = prompt_for_api_key()
        assert result is None


class TestDisplayWelcomeMessage:
    """Tests for welcome message display."""

    def test_display_welcome_message_runs(self, capsys):
        """Test welcome message displays without error."""
        display_welcome_message()
        captured = capsys.readouterr()
        assert "Rory" in captured.out
        assert "Brand Hub" in captured.out
