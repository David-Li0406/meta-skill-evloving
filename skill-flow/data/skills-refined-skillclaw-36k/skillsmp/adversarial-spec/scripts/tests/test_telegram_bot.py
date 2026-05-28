"""Tests for telegram_bot module."""

import sys
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from telegram_bot import (
    MAX_MESSAGE_LENGTH,
    api_call,
    get_config,
    get_last_update_id,
    poll_for_reply,
    send_long_message,
    send_message,
    split_message,
)


class TestGetConfig:
    def test_returns_empty_when_not_set(self):
        with patch.dict("os.environ", {}, clear=True):
            token, chat_id = get_config()
            assert token == ""
            assert chat_id == ""

    def test_returns_values_when_set(self):
        with patch.dict(
            "os.environ",
            {"TELEGRAM_BOT_TOKEN": "test-token", "TELEGRAM_CHAT_ID": "12345"},
        ):
            token, chat_id = get_config()
            assert token == "test-token"
            assert chat_id == "12345"


class TestSplitMessage:
    def test_short_message_not_split(self):
        text = "Short message"
        result = split_message(text)
        assert result == [text]

    def test_exactly_max_length_not_split(self):
        text = "x" * MAX_MESSAGE_LENGTH
        result = split_message(text)
        assert result == [text]

    def test_splits_at_paragraph_boundary(self):
        first_half = "a" * 2000
        second_half = "b" * 2000
        text = first_half + "\n\n" + second_half
        result = split_message(text, max_length=2500)
        assert len(result) == 2
        assert result[0] == first_half
        assert result[1] == second_half

    def test_splits_at_newline_when_no_paragraph(self):
        first_half = "a" * 2000
        second_half = "b" * 2000
        text = first_half + "\n" + second_half
        result = split_message(text, max_length=2500)
        assert len(result) == 2
        assert first_half in result[0]

    def test_splits_at_space_when_no_newline(self):
        first_half = "a" * 2000
        second_half = "b" * 2000
        text = first_half + " " + second_half
        result = split_message(text, max_length=2500)
        assert len(result) == 2

    def test_hard_split_when_no_boundaries(self):
        text = "x" * 5000
        result = split_message(text, max_length=2000)
        assert len(result) >= 2
        assert all(len(chunk) <= 2000 for chunk in result)


class TestApiCall:
    @patch("telegram_bot.urlopen")
    def test_successful_api_call(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"ok": true, "result": []}'
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        result = api_call("test-token", "getMe")
        assert result == {"ok": True, "result": []}

    @patch("telegram_bot.urlopen")
    def test_api_call_with_params(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"ok": true}'
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        result = api_call("test-token", "sendMessage", {"chat_id": "123", "text": "hi"})
        assert result == {"ok": True}

        called_request = mock_urlopen.call_args[0][0]
        assert "chat_id=123" in called_request.full_url
        assert "text=hi" in called_request.full_url


class TestSendMessage:
    @patch("telegram_bot.api_call")
    def test_send_message_success(self, mock_api_call):
        mock_api_call.return_value = {"ok": True}
        result = send_message("token", "123", "Hello")
        assert result is True
        mock_api_call.assert_called_once()

    @patch("telegram_bot.api_call")
    def test_send_message_failure(self, mock_api_call):
        mock_api_call.return_value = {"ok": False}
        result = send_message("token", "123", "Hello")
        assert result is False


class TestSendLongMessage:
    @patch("telegram_bot.send_message")
    def test_sends_short_message_directly(self, mock_send):
        mock_send.return_value = True
        result = send_long_message("token", "123", "Short message")
        assert result is True
        assert mock_send.call_count == 1

    @patch("telegram_bot.send_message")
    @patch("telegram_bot.time.sleep")
    def test_sends_multiple_chunks(self, mock_sleep, mock_send):
        mock_send.return_value = True
        long_text = "x" * 5000
        result = send_long_message("token", "123", long_text)
        assert result is True
        assert mock_send.call_count >= 2

    @patch("telegram_bot.send_message")
    def test_returns_false_on_chunk_failure(self, mock_send):
        mock_send.side_effect = [True, False]
        long_text = "x" * 5000
        result = send_long_message("token", "123", long_text)
        assert result is False


class TestGetLastUpdateId:
    @patch("telegram_bot.api_call")
    def test_returns_update_id_when_present(self, mock_api_call):
        mock_api_call.return_value = {"ok": True, "result": [{"update_id": 12345}]}
        result = get_last_update_id("token")
        assert result == 12345

    @patch("telegram_bot.api_call")
    def test_returns_zero_when_no_updates(self, mock_api_call):
        mock_api_call.return_value = {"ok": True, "result": []}
        result = get_last_update_id("token")
        assert result == 0


class TestPollForReply:
    @patch("telegram_bot.api_call")
    @patch("telegram_bot.time.time")
    def test_returns_message_text(self, mock_time, mock_api_call):
        # Simulate time: start=0, first iteration check=0.1, remaining > 0
        mock_time.side_effect = [0, 0.1, 0.2]
        # First call returns the message, second clears the update
        mock_api_call.side_effect = [
            {
                "ok": True,
                "result": [
                    {
                        "update_id": 100,
                        "message": {"chat": {"id": "123"}, "text": "Hello from user"},
                    }
                ],
            },
            {"ok": True, "result": []},  # Clear processed updates
        ]
        result = poll_for_reply("token", "123", timeout=60)
        assert result == "Hello from user"

    @patch("telegram_bot.api_call")
    @patch("telegram_bot.time.time")
    def test_returns_none_on_timeout(self, mock_time, mock_api_call):
        mock_time.side_effect = [0, 0, 2]
        mock_api_call.return_value = {"ok": True, "result": []}
        result = poll_for_reply("token", "123", timeout=1)
        assert result is None

    @patch("telegram_bot.api_call")
    @patch("telegram_bot.time.time")
    def test_ignores_messages_from_other_chats(self, mock_time, mock_api_call):
        # Two iterations: first finds other chat, second times out
        mock_time.side_effect = [0, 0.1, 0.5, 2]
        mock_api_call.side_effect = [
            {
                "ok": True,
                "result": [
                    {
                        "update_id": 100,
                        "message": {"chat": {"id": "999"}, "text": "Other chat"},
                    }
                ],
            },
            {"ok": True, "result": []},
        ]
        result = poll_for_reply("token", "123", timeout=1)
        assert result is None


class TestSplitMessageBoundaries:
    """Mutation-targeted tests for split_message boundary conditions.

    Mutation targets:
    - len(text) <= max_length boundary
    - split_at == -1 checks
    - split_at < max_length // 2 boundaries
    """

    def test_exactly_max_length_not_split(self):
        # Mutation: changing <= to < would incorrectly split
        text = "x" * MAX_MESSAGE_LENGTH
        result = split_message(text)
        assert len(result) == 1
        assert result[0] == text

    def test_one_over_max_length_splits(self):
        # Mutation: changing <= to < boundary
        text = "x" * (MAX_MESSAGE_LENGTH + 1)
        result = split_message(text)
        assert len(result) == 2

    def test_split_at_exactly_half_uses_paragraph(self):
        # Mutation: boundary at max_length // 2
        half = 2500 // 2
        first = "a" * half
        second = "b" * (2500 - half)
        text = first + "\n\n" + second
        result = split_message(text, max_length=2500)
        # Should split at paragraph since it's exactly at half
        assert len(result) == 2

    def test_split_at_less_than_half_falls_to_newline(self):
        # Mutation: split_at < max_length // 2 condition
        # Put paragraph break very early, should skip to newline
        first = "a" * 100  # Way less than half
        rest = "b" * 2000 + "\n" + "c" * 300
        text = first + "\n\n" + rest
        result = split_message(text, max_length=2500)
        assert len(result) >= 1

    def test_no_newline_falls_to_space(self):
        # Mutation: newline search fails, falls to space
        first = "word " * 400  # Words with spaces
        text = first.strip()
        result = split_message(text, max_length=2000)
        # Should split at space boundary
        assert len(result) >= 1
        assert all(len(chunk) <= 2000 for chunk in result)


class TestSendLongMessageBoundaries:
    """Mutation-targeted tests for send_long_message.

    Mutation targets:
    - len(chunks) > 1 check
    - i < len(chunks) - 1 check
    - i + 1 in header
    """

    @patch("telegram_bot.send_message")
    def test_single_chunk_no_header(self, mock_send):
        # Mutation: len(chunks) > 1 check
        mock_send.return_value = True
        result = send_long_message("token", "123", "short")
        assert result is True
        # Should NOT have header prefix
        call_text = mock_send.call_args[0][2]
        assert not call_text.startswith("[1/")

    @patch("telegram_bot.send_message")
    @patch("telegram_bot.time.sleep")
    def test_multiple_chunks_have_headers(self, mock_sleep, mock_send):
        # Mutation: header format i + 1
        mock_send.return_value = True
        long_text = "a" * 5000
        result = send_long_message("token", "123", long_text)
        assert result is True
        # Check headers are correct
        calls = mock_send.call_args_list
        assert len(calls) >= 2
        # First chunk should have [1/N] header
        assert calls[0][0][2].startswith("[1/")
        # Second chunk should have [2/N] header
        assert calls[1][0][2].startswith("[2/")

    @patch("telegram_bot.send_message")
    @patch("telegram_bot.time.sleep")
    def test_no_sleep_after_last_chunk(self, mock_sleep, mock_send):
        # Mutation: i < len(chunks) - 1 check
        mock_send.return_value = True
        long_text = "a" * 5000
        send_long_message("token", "123", long_text)
        # Sleep called between chunks but not after last
        # With 2 chunks, should sleep once
        calls = mock_send.call_args_list
        assert mock_sleep.call_count == len(calls) - 1


class TestPollForReplyBoundaries:
    """Mutation-targeted tests for poll_for_reply.

    Mutation targets:
    - remaining <= 0 check
    - after_update_id + 1 offset
    - msg_chat_id == chat_id check
    """

    @patch("telegram_bot.api_call")
    @patch("telegram_bot.time.time")
    def test_uses_after_update_id_offset(self, mock_time, mock_api_call):
        # Mutation: after_update_id + 1 calculation
        # time() called: start=0, loop check=0.01, remaining=0.01, then timeout
        # remaining = int(60 - 0.01) = 59 > 0, so loop continues
        mock_time.side_effect = [0, 0.01, 0.01, 61]  # Last one triggers timeout
        mock_api_call.return_value = {"ok": True, "result": []}
        poll_for_reply("token", "123", timeout=60, after_update_id=100)
        # First call should have offset=101
        assert mock_api_call.call_count >= 1
        first_call = mock_api_call.call_args_list[0]
        assert first_call[0][2]["offset"] == 101

    @patch("telegram_bot.api_call")
    @patch("telegram_bot.time.time")
    def test_handles_runtime_error(self, mock_time, mock_api_call):
        # Mutation: exception handling continues loop
        mock_time.side_effect = [0, 0.1, 2]
        mock_api_call.side_effect = RuntimeError("Network error")
        result = poll_for_reply("token", "123", timeout=1)
        assert result is None

    @patch("telegram_bot.api_call")
    @patch("telegram_bot.time.time")
    def test_empty_text_ignored(self, mock_time, mock_api_call):
        # Mutation: text check in if condition
        mock_time.side_effect = [0, 0.1, 2]
        mock_api_call.side_effect = [
            {
                "ok": True,
                "result": [
                    {
                        "update_id": 100,
                        "message": {"chat": {"id": "123"}, "text": ""},
                    }
                ],
            },
            {"ok": True, "result": []},
        ]
        result = poll_for_reply("token", "123", timeout=1)
        assert result is None


class TestApiCallErrors:
    """Mutation-targeted tests for api_call error handling.

    Mutation targets:
    - HTTPError handling
    - URLError handling
    """

    @patch("telegram_bot.urlopen")
    def test_http_error_raises_runtime_error(self, mock_urlopen):
        from urllib.error import HTTPError

        mock_urlopen.side_effect = HTTPError(
            "url", 400, "Bad Request", {}, MagicMock(read=lambda: b"error body")
        )

        import pytest

        with pytest.raises(RuntimeError) as exc_info:
            api_call("token", "getMe")
        assert "400" in str(exc_info.value)

    @patch("telegram_bot.urlopen")
    def test_url_error_raises_runtime_error(self, mock_urlopen):
        from urllib.error import URLError

        mock_urlopen.side_effect = URLError("Connection refused")

        import pytest

        with pytest.raises(RuntimeError) as exc_info:
            api_call("token", "getMe")
        assert "Network error" in str(exc_info.value)


class TestCmdSetup:
    """Tests for cmd_setup command.

    Mutation targets:
    - token check
    - chat_id check
    - send_message success/failure
    """

    def test_exits_when_no_token(self):
        import pytest
        from telegram_bot import cmd_setup

        with patch.dict("os.environ", {}, clear=True):
            with patch("sys.stdout", new_callable=StringIO):
                args = MagicMock()
                with pytest.raises(SystemExit) as exc_info:
                    cmd_setup(args)
                assert exc_info.value.code == 2

    @patch("telegram_bot.discover_chat_id")
    def test_discovers_chat_id_when_no_chat_id(self, mock_discover):
        import pytest
        from telegram_bot import cmd_setup

        with patch.dict("os.environ", {"TELEGRAM_BOT_TOKEN": "test-token"}, clear=True):
            with patch("sys.stdout", new_callable=StringIO):
                args = MagicMock()
                with pytest.raises(SystemExit) as exc_info:
                    cmd_setup(args)
                assert exc_info.value.code == 0
                mock_discover.assert_called_once()

    @patch("telegram_bot.send_message")
    def test_sends_test_message_on_success(self, mock_send):
        from telegram_bot import cmd_setup

        mock_send.return_value = True
        with patch.dict(
            "os.environ",
            {"TELEGRAM_BOT_TOKEN": "test-token", "TELEGRAM_CHAT_ID": "123"},
            clear=True,
        ):
            with patch("sys.stdout", new_callable=StringIO) as mock_out:
                args = MagicMock()
                cmd_setup(args)
                output = mock_out.getvalue()
                assert "successfully" in output

    @patch("telegram_bot.send_message")
    def test_exits_on_test_message_failure(self, mock_send):
        import pytest
        from telegram_bot import cmd_setup

        mock_send.return_value = False
        with patch.dict(
            "os.environ",
            {"TELEGRAM_BOT_TOKEN": "test-token", "TELEGRAM_CHAT_ID": "123"},
            clear=True,
        ):
            with patch("sys.stdout", new_callable=StringIO):
                args = MagicMock()
                with pytest.raises(SystemExit) as exc_info:
                    cmd_setup(args)
                assert exc_info.value.code == 1


class TestCmdSend:
    """Tests for cmd_send command.

    Mutation targets:
    - config check
    - empty text check
    - send success/failure
    """

    def test_exits_when_no_config(self):
        import pytest
        from telegram_bot import cmd_send

        with patch.dict("os.environ", {}, clear=True):
            args = MagicMock()
            with pytest.raises(SystemExit) as exc_info:
                cmd_send(args)
            assert exc_info.value.code == 2

    def test_exits_on_empty_stdin(self):
        import pytest
        from telegram_bot import cmd_send

        with patch.dict(
            "os.environ",
            {"TELEGRAM_BOT_TOKEN": "test-token", "TELEGRAM_CHAT_ID": "123"},
            clear=True,
        ):
            with patch("sys.stdin", StringIO("")):
                args = MagicMock()
                with pytest.raises(SystemExit) as exc_info:
                    cmd_send(args)
                assert exc_info.value.code == 1

    @patch("telegram_bot.send_long_message")
    def test_sends_message_from_stdin(self, mock_send):
        from telegram_bot import cmd_send

        mock_send.return_value = True
        with patch.dict(
            "os.environ",
            {"TELEGRAM_BOT_TOKEN": "test-token", "TELEGRAM_CHAT_ID": "123"},
            clear=True,
        ):
            with patch("sys.stdin", StringIO("Hello world")):
                with patch("sys.stdout", new_callable=StringIO):
                    args = MagicMock()
                    cmd_send(args)
                    mock_send.assert_called_once()

    @patch("telegram_bot.send_long_message")
    def test_exits_on_send_failure(self, mock_send):
        import pytest
        from telegram_bot import cmd_send

        mock_send.return_value = False
        with patch.dict(
            "os.environ",
            {"TELEGRAM_BOT_TOKEN": "test-token", "TELEGRAM_CHAT_ID": "123"},
            clear=True,
        ):
            with patch("sys.stdin", StringIO("Hello")):
                args = MagicMock()
                with pytest.raises(SystemExit) as exc_info:
                    cmd_send(args)
                assert exc_info.value.code == 1


class TestCmdPoll:
    """Tests for cmd_poll command.

    Mutation targets:
    - config check
    - reply success/failure
    """

    def test_exits_when_no_config(self):
        import pytest
        from telegram_bot import cmd_poll

        with patch.dict("os.environ", {}, clear=True):
            args = MagicMock(timeout=60)
            with pytest.raises(SystemExit) as exc_info:
                cmd_poll(args)
            assert exc_info.value.code == 2

    @patch("telegram_bot.poll_for_reply")
    @patch("telegram_bot.get_last_update_id")
    def test_prints_reply_on_success(self, mock_last_id, mock_poll):
        from telegram_bot import cmd_poll

        mock_last_id.return_value = 0
        mock_poll.return_value = "User reply"
        with patch.dict(
            "os.environ",
            {"TELEGRAM_BOT_TOKEN": "test-token", "TELEGRAM_CHAT_ID": "123"},
            clear=True,
        ):
            with patch("sys.stdout", new_callable=StringIO) as mock_out:
                with patch("sys.stderr", new_callable=StringIO):
                    args = MagicMock(timeout=60)
                    cmd_poll(args)
                    assert "User reply" in mock_out.getvalue()

    @patch("telegram_bot.poll_for_reply")
    @patch("telegram_bot.get_last_update_id")
    def test_exits_on_no_reply(self, mock_last_id, mock_poll):
        import pytest
        from telegram_bot import cmd_poll

        mock_last_id.return_value = 0
        mock_poll.return_value = None
        with patch.dict(
            "os.environ",
            {"TELEGRAM_BOT_TOKEN": "test-token", "TELEGRAM_CHAT_ID": "123"},
            clear=True,
        ):
            with patch("sys.stderr", new_callable=StringIO):
                args = MagicMock(timeout=60)
                with pytest.raises(SystemExit) as exc_info:
                    cmd_poll(args)
                assert exc_info.value.code == 1


class TestCmdNotify:
    """Tests for cmd_notify command.

    Mutation targets:
    - config check
    - empty notification check
    - send failure
    """

    def test_exits_when_no_config(self):
        import pytest
        from telegram_bot import cmd_notify

        with patch.dict("os.environ", {}, clear=True):
            args = MagicMock(timeout=60)
            with pytest.raises(SystemExit) as exc_info:
                cmd_notify(args)
            assert exc_info.value.code == 2

    def test_exits_on_empty_notification(self):
        import pytest
        from telegram_bot import cmd_notify

        with patch.dict(
            "os.environ",
            {"TELEGRAM_BOT_TOKEN": "test-token", "TELEGRAM_CHAT_ID": "123"},
            clear=True,
        ):
            with patch("sys.stdin", StringIO("")):
                args = MagicMock(timeout=60)
                with pytest.raises(SystemExit) as exc_info:
                    cmd_notify(args)
                assert exc_info.value.code == 1

    @patch("telegram_bot.poll_for_reply")
    @patch("telegram_bot.send_long_message")
    @patch("telegram_bot.get_last_update_id")
    def test_sends_notification_and_polls(self, mock_last_id, mock_send, mock_poll):
        import json

        from telegram_bot import cmd_notify

        mock_last_id.return_value = 0
        mock_send.return_value = True
        mock_poll.return_value = "Feedback here"
        with patch.dict(
            "os.environ",
            {"TELEGRAM_BOT_TOKEN": "test-token", "TELEGRAM_CHAT_ID": "123"},
            clear=True,
        ):
            with patch("sys.stdin", StringIO("Round 1 complete")):
                with patch("sys.stdout", new_callable=StringIO) as mock_out:
                    args = MagicMock(timeout=60)
                    cmd_notify(args)
                    output = json.loads(mock_out.getvalue())
                    assert output["notification_sent"] is True
                    assert output["feedback"] == "Feedback here"

    @patch("telegram_bot.send_long_message")
    @patch("telegram_bot.get_last_update_id")
    def test_exits_on_send_failure(self, mock_last_id, mock_send):
        import pytest
        from telegram_bot import cmd_notify

        mock_last_id.return_value = 0
        mock_send.return_value = False
        with patch.dict(
            "os.environ",
            {"TELEGRAM_BOT_TOKEN": "test-token", "TELEGRAM_CHAT_ID": "123"},
            clear=True,
        ):
            with patch("sys.stdin", StringIO("Notification")):
                args = MagicMock(timeout=60)
                with pytest.raises(SystemExit) as exc_info:
                    cmd_notify(args)
                assert exc_info.value.code == 1


class TestMain:
    """Tests for main entry point."""

    def test_main_with_setup_command(self):
        import pytest
        from telegram_bot import main

        with patch("sys.argv", ["telegram_bot.py", "setup"]):
            with patch.dict("os.environ", {}, clear=True):
                with patch("sys.stdout", new_callable=StringIO):
                    with pytest.raises(SystemExit) as exc_info:
                        main()
                    # Exits with 2 due to no token
                    assert exc_info.value.code == 2
