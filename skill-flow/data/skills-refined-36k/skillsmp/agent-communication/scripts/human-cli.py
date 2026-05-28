#!/usr/bin/env python3
"""
Human CLI for multi-agent communication.

Interactive REPL that allows humans to join the agent chat as full participants.
"""

import sys
import os
import json
import argparse
import subprocess
import signal
import time
import struct
import threading
import socket as sock
import readline
from pathlib import Path
from datetime import datetime


def get_runtime_dir():
    """Get runtime directory for socket files."""
    return Path(os.environ.get('XDG_RUNTIME_DIR', '/tmp'))


def get_chat_dir():
    """Get chat directory for registry and sockets."""
    chat_dir = get_runtime_dir() / "claude-agent-chat"
    chat_dir.mkdir(exist_ok=True)
    return chat_dir


def get_agent_socket_path(agent_name):
    """Get agent's local socket path."""
    chat_dir = get_chat_dir()
    return str(chat_dir / f"{agent_name}.sock")


def send_command(sock_path, command, args=None):
    """Send command to agent and return response."""
    if args is None:
        args = {}

    try:
        s = sock.socket(sock.AF_UNIX, sock.SOCK_STREAM)
        s.settimeout(5.0)
        s.connect(sock_path)

        # Wrap in envelope
        envelope = {
            'type': 'command',
            'command': command,
            'args': args,
        }

        # Send with length prefix
        payload = json.dumps(envelope).encode('utf-8')
        s.sendall(struct.pack('>I', len(payload)) + payload)

        # Receive response with length prefix
        length_data = b''
        while len(length_data) < 4:
            chunk = s.recv(4 - len(length_data))
            if not chunk:
                raise Exception("Connection closed by server")
            length_data += chunk

        response_length = struct.unpack('>I', length_data)[0]

        response_data = b''
        while len(response_data) < response_length:
            chunk = s.recv(min(4096, response_length - len(response_data)))
            if not chunk:
                break
            response_data += chunk

        response = json.loads(response_data.decode('utf-8'))
        s.close()

        return response

    except sock.error as e:
        return {
            'status': 'error',
            'error': f'Cannot connect to agent: {e}'
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }


class HumanCLI:
    """Human CLI for agent communication."""

    def __init__(self, name, context, presentation, agent_script_path):
        """Initialize CLI."""
        self.name = name
        self.context = context
        self.presentation = presentation
        self.agent_script_path = agent_script_path
        self.sock_path = get_agent_socket_path(name)

        self.agent_process = None
        self.running = True
        self.message_thread = None
        self.display_lock = threading.Lock()

        # ANSI color codes
        self.COLOR_RESET = '\033[0m'
        self.COLOR_GRAY = '\033[90m'
        self.COLOR_GREEN = '\033[92m'
        self.COLOR_YELLOW = '\033[93m'
        self.COLOR_BLUE = '\033[94m'
        self.COLOR_MAGENTA = '\033[95m'

    def print_colored(self, text, color=''):
        """Print text with color if terminal supports it."""
        if sys.stdout.isatty():
            print(f"{color}{text}{self.COLOR_RESET}")
        else:
            print(text)

    def format_timestamp(self, iso_timestamp):
        """Format ISO timestamp to HH:MM:SS."""
        try:
            dt = datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))
            return dt.strftime('%H:%M:%S')
        except:
            return iso_timestamp

    def unescape_content(self, content):
        """Unescape common shell escape sequences in message content."""
        # Remove backslashes before characters that don't need escaping in display
        # This fixes messages that were sent via shell with escaped special chars
        return content.replace('\\!', '!').replace('\\?', '?').replace('\\$', '$')

    def display_message(self, msg):
        """Display a message with formatting."""
        with self.display_lock:
            msg_type = msg.get('type', 'message')
            sender = msg.get('sender', {})
            sender_name = sender.get('name', 'unknown')
            timestamp = self.format_timestamp(msg.get('timestamp', ''))
            content = self.unescape_content(msg.get('content', ''))

            # Save the current line buffer and cursor position
            saved_line = readline.get_line_buffer()
            saved_point = readline.get_begidx()

            # Move to beginning of line and clear it
            sys.stdout.write('\r\033[K')
            sys.stdout.flush()

            if msg_type == 'join':
                self.print_colored(
                    f"[{timestamp}] → {sender_name} joined the chat",
                    self.COLOR_GREEN
                )
                context = sender.get('context', '')
                if context:
                    self.print_colored(f"  Context: {context}", self.COLOR_GRAY)
            elif msg_type == 'leave':
                self.print_colored(
                    f"[{timestamp}] ← {sender_name} left the chat",
                    self.COLOR_YELLOW
                )
            else:
                self.print_colored(
                    f"[{timestamp}] {sender_name}: {content}",
                    self.COLOR_BLUE
                )

            # Restore the prompt and the user's input
            sys.stdout.write('> ' + saved_line)
            sys.stdout.flush()

            # Force readline to redraw (if terminal supports it)
            readline.redisplay()

    def start_agent(self):
        """Start agent daemon as subprocess."""
        self.print_colored("Starting agent daemon...", self.COLOR_GRAY)

        cmd = [
            self.agent_script_path,
            '--name', self.name,
            '--context', self.context,
            '--presentation', self.presentation,
        ]

        self.agent_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Wait for socket to be ready
        max_wait = 5
        for _ in range(max_wait * 10):
            if os.path.exists(self.sock_path):
                time.sleep(0.2)  # Extra time for socket to be ready
                break
            time.sleep(0.1)
        else:
            self.print_colored("Error: Agent daemon did not start in time", self.COLOR_YELLOW)
            sys.exit(1)

        self.print_colored(f"Connected as: {self.name}", self.COLOR_GREEN)
        self.print_colored(f"Context: {self.context}", self.COLOR_GRAY)
        self.print_colored("Type /help for commands\n", self.COLOR_GRAY)

    def stop_agent(self):
        """Stop agent daemon gracefully."""
        if self.agent_process:
            # Send leave command to agent
            try:
                response = send_command(self.sock_path, 'leave')
                if response['status'] == 'ok':
                    # Wait for agent to exit
                    try:
                        self.agent_process.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        self.agent_process.kill()
                else:
                    # Fallback to SIGTERM if leave command failed
                    self.agent_process.send_signal(signal.SIGTERM)
                    try:
                        self.agent_process.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        self.agent_process.kill()
            except Exception:
                # Fallback to SIGTERM if we can't connect
                self.agent_process.send_signal(signal.SIGTERM)
                try:
                    self.agent_process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    self.agent_process.kill()

    def message_receiver_loop(self):
        """Background thread to wait for and display messages."""
        while self.running:
            try:
                # Use notify to wait for messages (will wait indefinitely)
                # The socket timeout in send_command (5s) will cause this to retry periodically
                notify_response = send_command(self.sock_path, 'notify', {})

                if notify_response['status'] == 'ok' and self.running:
                    # Messages available, receive them
                    receive_response = send_command(self.sock_path, 'receive', {})

                    if receive_response['status'] == 'ok':
                        messages = receive_response.get('data', {}).get('messages', [])
                        for msg in messages:
                            self.display_message(msg)

            except Exception as e:
                if self.running:
                    time.sleep(1)

    def cmd_help(self):
        """Show help."""
        print("\nAvailable commands:")
        print("  /help       - Show this help")
        print("  /status     - Show agent status")
        print("  /members    - List connected agents")
        print("  /quit, /exit - Exit the chat")
        print("\nAnything else will be sent as a message to all agents.\n")

    def cmd_status(self):
        """Show status."""
        response = send_command(self.sock_path, 'status')

        if response['status'] == 'ok':
            data = response['data']
            agent = data['agent']
            members = data['members']
            queue_size = data['queue_size']

            print(f"\nAgent: {agent['name']}")
            print(f"Context: {agent['context']}")
            print(f"Connected agents: {len(members)}")
            print(f"Unread messages: {queue_size}\n")
        else:
            self.print_colored(f"Error: {response.get('error', 'Unknown error')}", self.COLOR_YELLOW)

    def cmd_members(self):
        """List members."""
        response = send_command(self.sock_path, 'status')

        if response['status'] == 'ok':
            members = response['data']['members']

            if not members:
                print("\nNo other agents connected.\n")
                return

            print(f"\nConnected agents ({len(members)}):")
            for name, info in members.items():
                context = info.get('context', 'N/A')
                presentation = info.get('presentation', '')
                print(f"  • {name}")
                print(f"    Context: {context}")
                if presentation:
                    print(f"    {presentation}")
            print()
        else:
            self.print_colored(f"Error: {response.get('error', 'Unknown error')}", self.COLOR_YELLOW)

    def cmd_send(self, message):
        """Send a message."""
        response = send_command(self.sock_path, 'send', {'content': message})

        if response['status'] != 'ok':
            self.print_colored(f"Error: {response.get('error', 'Unknown error')}", self.COLOR_YELLOW)

    def run_repl(self):
        """Run the REPL loop."""
        try:
            while self.running:
                try:
                    # Use input() for proper readline integration
                    # Don't use lock here - let messages interrupt
                    line = input('> ')
                except EOFError:
                    # Ctrl+D pressed
                    print("\nGoodbye!")
                    self.running = False
                    break
                except KeyboardInterrupt:
                    # Ctrl+C pressed
                    print("\nGoodbye!")
                    self.running = False
                    break

                line = line.strip()

                if not line:
                    continue

                # Handle commands
                if line.startswith('/'):
                    cmd = line[1:].lower()

                    if cmd in ('quit', 'exit'):
                        print("Goodbye!")
                        self.running = False
                        break
                    elif cmd == 'help':
                        self.cmd_help()
                    elif cmd == 'status':
                        self.cmd_status()
                    elif cmd == 'members':
                        self.cmd_members()
                    else:
                        self.print_colored(f"Unknown command: /{cmd}", self.COLOR_YELLOW)
                        self.print_colored("Type /help for available commands", self.COLOR_GRAY)
                else:
                    # Send as message
                    self.cmd_send(line)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            self.running = False

    def run(self):
        """Run the CLI."""
        try:
            # Start agent
            self.start_agent()

            # Start message receiver thread
            self.message_thread = threading.Thread(
                target=self.message_receiver_loop,
                daemon=True
            )
            self.message_thread.start()

            # Run REPL
            self.run_repl()

        finally:
            # Cleanup
            self.running = False
            self.stop_agent()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Human CLI for multi-agent communication',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  human-cli.py
  human-cli.py --name human-alice
  human-cli.py --name alice --context "myproject/docs" --presentation "Documentation maintainer"
        """
    )

    # Determine default name
    try:
        default_name = f"human-{os.getlogin()}"
    except:
        default_name = "human-user"

    parser.add_argument(
        '--name',
        default=default_name,
        help=f'Agent name (default: {default_name})'
    )
    parser.add_argument(
        '--context',
        default='human-terminal',
        help='Agent context (default: human-terminal)'
    )
    parser.add_argument(
        '--presentation',
        default='Human operator joining the chat',
        help='Agent presentation (default: "Human operator joining the chat")'
    )

    args = parser.parse_args()

    # Get path to agent.py (resolve symlinks to find the real script location)
    script_path = Path(__file__).resolve()
    script_dir = script_path.parent
    agent_script = str(script_dir / 'agent.py')

    if not os.path.exists(agent_script):
        print(f"Error: agent.py not found at {agent_script}", file=sys.stderr)
        sys.exit(1)

    # Run CLI
    cli = HumanCLI(args.name, args.context, args.presentation, agent_script)
    cli.run()


if __name__ == '__main__':
    main()
