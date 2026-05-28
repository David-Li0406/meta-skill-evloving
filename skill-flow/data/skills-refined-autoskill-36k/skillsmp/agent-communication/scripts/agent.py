#!/usr/bin/env python3
"""
Multi-agent communication agent daemon.

Per-instance background process that manages file-based communication,
queues incoming messages, and exposes local socket for chat.py commands.
"""

import fcntl
import json
import os
import sys
import atexit
import signal
import argparse
import time
import struct
from datetime import datetime, UTC
from pathlib import Path
from collections import deque
import threading
import socket as sock


def get_runtime_dir():
    """Get runtime directory for chat files."""
    return Path(os.environ.get('XDG_RUNTIME_DIR', '/tmp'))


def get_chat_dir():
    """Get chat directory for registry."""
    chat_dir = get_runtime_dir() / "claude-agent-chat"
    chat_dir.mkdir(exist_ok=True)
    return chat_dir


def get_registry_path():
    """Get path to registry file."""
    return get_chat_dir() / "registry.json"


def get_agent_socket_path(agent_name):
    """Get agent's local socket path."""
    chat_dir = get_chat_dir()
    return str(chat_dir / f"{agent_name}.sock")


def read_registry():
    """Read registry with shared lock."""
    registry_path = get_registry_path()

    if not registry_path.exists():
        return {}

    with open(registry_path, 'r') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_SH)
        try:
            data = f.read()
            return json.loads(data) if data else {}
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def write_registry(registry):
    """Write registry with exclusive lock."""
    registry_path = get_registry_path()

    with open(registry_path, 'w') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            json.dump(registry, f, indent=2)
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def check_agent_alive(agent_name):
    """Check if agent is alive by probing its socket."""
    socket_path = get_agent_socket_path(agent_name)

    if not os.path.exists(socket_path):
        return False

    try:
        s = sock.socket(sock.AF_UNIX, sock.SOCK_STREAM)
        s.settimeout(1.0)
        s.connect(socket_path)
        s.close()
        return True
    except:
        return False


class Agent:
    """Agent daemon."""

    def __init__(self, name, context, presentation, cwd):
        """Initialize agent."""
        self.name = name
        self.context = context
        self.presentation = presentation
        self.cwd = Path(cwd)

        self.local_sock = None
        self.local_socket_path = get_agent_socket_path(self.name)

        self.message_queue = deque(maxlen=100)
        self.members = {}
        self.members_lock = threading.Lock()
        self.running = True
        self.message_event = threading.Event()

    def cleanup(self):
        """Clean up resources."""
        # Unregister from registry
        try:
            registry = read_registry()
            if self.name in registry:
                del registry[self.name]
                write_registry(registry)
        except Exception as e:
            print(f"Error unregistering: {e}", file=sys.stderr)

        # Close local socket
        if self.local_sock:
            self.local_sock.close()

        # Remove local socket file
        if os.path.exists(self.local_socket_path):
            try:
                os.unlink(self.local_socket_path)
                print(f"Cleaned up agent socket: {self.local_socket_path}", file=sys.stderr)
            except OSError as e:
                print(f"Error cleaning up socket: {e}", file=sys.stderr)

    def recv_framed_message(self, conn):
        """Read a length-prefixed JSON message from socket."""
        # Read 4-byte length prefix
        length_data = b''
        while len(length_data) < 4:
            chunk = conn.recv(4 - len(length_data))
            if not chunk:
                return None
            length_data += chunk

        message_length = struct.unpack('>I', length_data)[0]

        # Sanity check on message size (prevent DoS)
        MAX_MESSAGE_SIZE = 1024 * 1024  # 1MB
        if message_length > MAX_MESSAGE_SIZE:
            raise ValueError(f"Message too large: {message_length}")

        # Read message body
        message_data = b''
        while len(message_data) < message_length:
            chunk = conn.recv(min(4096, message_length - len(message_data)))
            if not chunk:
                return None
            message_data += chunk

        return json.loads(message_data.decode('utf-8'))

    def send_framed_message(self, conn, message):
        """Send a length-prefixed JSON message to socket."""
        payload = json.dumps(message).encode('utf-8')
        conn.sendall(struct.pack('>I', len(payload)) + payload)

    def send_to_agent(self, target_name, message):
        """Send message directly to another agent's socket.

        Returns:
            (success: bool, error_message: str | None)
        """
        # Look up socket path from registry
        registry = read_registry()
        target = registry.get(target_name)

        if not target:
            return (False, f"Agent {target_name} not in registry")

        socket_path = target.get('socket_path')
        if not socket_path:
            return (False, f"No socket path for {target_name}")

        # Connect and send
        try:
            s = sock.socket(sock.AF_UNIX, sock.SOCK_STREAM)
            s.settimeout(5.0)  # 5 second timeout for connection
            s.connect(socket_path)

            envelope = {
                "type": "remote_message",
                "message": message
            }

            # Send with length prefix
            self.send_framed_message(s, envelope)

            # Read response
            response = self.recv_framed_message(s)

            s.close()

            return (True, None)

        except (sock.error, ConnectionRefusedError, FileNotFoundError) as e:
            # Remove from members cache if unreachable
            if target_name in self.members:
                del self.members[target_name]
            return (False, str(e))

    def handle_remote_message(self, envelope):
        """Handle message received from another agent."""
        message = envelope.get('message', {})
        msg_type = message.get('type')
        sender = message.get('sender', {})
        sender_name = sender.get('name')

        if msg_type == 'join':
            # Update members cache
            if sender_name and sender_name != self.name:
                with self.members_lock:
                    self.members[sender_name] = sender
            self.message_queue.append(message)

        elif msg_type == 'leave':
            # Remove from members
            if sender_name and sender_name in self.members:
                with self.members_lock:
                    del self.members[sender_name]
            self.message_queue.append(message)

        elif msg_type == 'message':
            if sender.get('name') != self.name:
                self.message_queue.append(message)

        # Signal waiting receivers
        self.message_event.set()

        return {'status': 'ok'}

    def register(self):
        """Register agent in registry."""
        registry = read_registry()

        # Check if name already exists
        if self.name in registry:
            if check_agent_alive(self.name):
                print(f"Error: Agent name '{self.name}' already in use", file=sys.stderr)
                sys.exit(1)
            else:
                # Stale entry, clean it up
                print(f"Cleaning up stale entry for '{self.name}'", file=sys.stderr)
                del registry[self.name]

        # Add self to registry WITH socket path
        registry[self.name] = {
            'name': self.name,
            'context': self.context,
            'presentation': self.presentation,
            'joined_at': datetime.now(UTC).isoformat().replace('+00:00', 'Z'),
            'socket_path': self.local_socket_path,
        }

        write_registry(registry)

        # Update local members cache
        with self.members_lock:
            self.members = {k: v for k, v in registry.items() if k != self.name}

        print(f"Joined chat. {len(registry)} member(s) present.", file=sys.stderr)

        # Broadcast join message via socket (not file)
        with self.members_lock:
            members_to_notify = list(self.members.keys())

        if members_to_notify:
            join_msg = {
                'id': f"{self.name}-{datetime.now(UTC).isoformat().replace('+00:00', 'Z')}",
                'timestamp': datetime.now(UTC).isoformat().replace('+00:00', 'Z'),
                'type': 'join',
                'sender': {
                    'name': self.name,
                    'context': self.context,
                    'presentation': self.presentation,
                },
                'content': self.presentation,
            }

            for agent_name in members_to_notify:
                success, error = self.send_to_agent(agent_name, join_msg)
                if not success:
                    print(f"Could not notify {agent_name} of join: {error}", file=sys.stderr)

    def send_message_to_agents(self, content):
        """Send message to all other agents via direct socket.

        Returns:
            dict with 'delivered_to' and 'failed' keys
        """
        registry = read_registry()

        # Update members cache
        with self.members_lock:
            self.members = {k: v for k, v in registry.items() if k != self.name}
            members_to_send = list(self.members.keys())

        if not members_to_send:
            return {'delivered_to': [], 'failed': {}}

        timestamp = datetime.now(UTC).isoformat().replace('+00:00', 'Z')
        msg = {
            'id': f"{self.name}-{timestamp}",
            'timestamp': timestamp,
            'type': 'message',
            'sender': {
                'name': self.name,
                'context': self.context,
                'presentation': self.presentation,
            },
            'content': content,
        }

        delivered = []
        failed = {}

        # Iterate over copy to avoid dictionary changed size during iteration
        for agent_name in members_to_send:
            success, error = self.send_to_agent(agent_name, msg)
            if success:
                delivered.append(agent_name)
            else:
                failed[agent_name] = error

        return {'delivered_to': delivered, 'failed': failed}

    def start_local_server(self):
        """Start local Unix socket server for chat.py commands."""
        # Remove stale socket
        if os.path.exists(self.local_socket_path):
            os.unlink(self.local_socket_path)

        # Create Unix socket
        self.local_sock = sock.socket(sock.AF_UNIX, sock.SOCK_STREAM)
        self.local_sock.bind(self.local_socket_path)
        self.local_sock.listen(5)
        self.local_sock.settimeout(1.0)

        print(f"Agent listening on {self.local_socket_path}", file=sys.stderr)
        print(f"Agent name: {self.name}", file=sys.stderr)

    def broadcast_leave(self):
        """Broadcast leave message to all agents."""
        with self.members_lock:
            members_to_notify = list(self.members.keys())

        if members_to_notify:
            leave_msg = {
                'id': f"{self.name}-{datetime.now(UTC).isoformat().replace('+00:00', 'Z')}",
                'timestamp': datetime.now(UTC).isoformat().replace('+00:00', 'Z'),
                'type': 'leave',
                'sender': {
                    'name': self.name,
                    'context': self.context,
                    'presentation': self.presentation,
                },
                'content': '',
            }

            for agent_name in members_to_notify:
                try:
                    self.send_to_agent(agent_name, leave_msg)
                except:
                    pass  # Best effort

    def handle_command(self, cmd):
        """Handle command from chat.py."""
        command = cmd.get('command')

        if command == 'send':
            # Block sending if there are unread messages
            if self.message_queue:
                return {
                    'status': 'error',
                    'error': f'Cannot send: {len(self.message_queue)} unread message(s). Use "receive" first.'
                }

            content = cmd.get('args', {}).get('content', '')
            result = self.send_message_to_agents(content)

            # Include delivery report
            return {
                'status': 'ok',
                'data': result
            }

        elif command == 'receive':
            messages = []

            # Clear event first (before draining - prevents race condition)
            self.message_event.clear()

            # Drain existing queue
            while self.message_queue:
                messages.append(self.message_queue.popleft())

            # If no messages yet, wait for event
            if not messages:
                self.message_event.wait()
                while self.message_queue:
                    messages.append(self.message_queue.popleft())

            return {'status': 'ok', 'data': {'messages': messages}}

        elif command == 'notify':
            # Check if there are already messages in queue
            if self.message_queue:
                return {'status': 'ok', 'data': {'count': len(self.message_queue)}}

            # No messages, wait for the event (indefinitely)
            self.message_event.clear()
            self.message_event.wait()

            # Message arrived, return count
            return {'status': 'ok', 'data': {'count': len(self.message_queue)}}

        elif command == 'status':
            return {
                'status': 'ok',
                'data': {
                    'agent': {
                        'name': self.name,
                        'context': self.context,
                    },
                    'members': self.members,
                    'queue_size': len(self.message_queue),
                }
            }

        elif command == 'leave':
            # Broadcast leave message
            self.broadcast_leave()

            # Stop the agent
            self.running = False

            return {'status': 'ok', 'message': 'Left chat successfully'}

        else:
            return {'status': 'error', 'error': f'Unknown command: {command}'}

    def _handle_connection(self, conn):
        """Handle a single connection in its own thread."""
        try:
            # No timeout - wait indefinitely
            conn.settimeout(None)
            envelope = self.recv_framed_message(conn)
            if not envelope:
                return

            msg_type = envelope.get('type')

            if msg_type == 'command':
                response = self.handle_command(envelope)
            elif msg_type == 'remote_message':
                response = self.handle_remote_message(envelope)
            else:
                response = {'status': 'error', 'error': f'Unknown message type: {msg_type}'}

            self.send_framed_message(conn, response)
        except BrokenPipeError:
            pass
        except Exception as e:
            if self.running:
                print(f"Error handling connection: {e}", file=sys.stderr)
        finally:
            try:
                conn.close()
            except:
                pass

    def run_local_server(self):
        """Run server loop spawning handler threads for each connection."""
        while self.running:
            try:
                conn, addr = self.local_sock.accept()
                handler = threading.Thread(
                    target=self._handle_connection,
                    args=(conn,),
                    daemon=True
                )
                handler.start()
            except sock.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Error accepting connection: {e}", file=sys.stderr)

    def run(self):
        """Run the agent."""
        # Register
        self.register()

        # Start local server
        self.start_local_server()

        # Run local server
        self.run_local_server()


def get_parent_cwd():
    """Get the working directory of the parent process."""
    try:
        parent_pid = os.getppid()
        # Read the cwd from /proc filesystem (Linux)
        cwd_link = f"/proc/{parent_pid}/cwd"
        if os.path.exists(cwd_link):
            return os.readlink(cwd_link)
    except Exception as e:
        print(f"Warning: Could not determine parent cwd: {e}", file=sys.stderr)

    # Fallback to current directory
    return os.getcwd()


def main():
    """Main entry point."""
    # Ignore SIGPIPE - prevents process death when writing to closed sockets
    signal.signal(signal.SIGPIPE, signal.SIG_IGN)

    parser = argparse.ArgumentParser(description='Agent daemon for multi-agent communication')
    parser.add_argument('--name', required=True, help='Agent name')
    parser.add_argument('--context', required=True, help='Agent context (e.g., project/repo)')
    parser.add_argument('--presentation', required=True, help='Agent self-presentation')
    parser.add_argument('--cwd', required=False, help='Working directory for unread notifications (default: auto-detect from parent process)')

    args = parser.parse_args()

    # Use provided cwd or auto-detect from parent process
    cwd = args.cwd if args.cwd else get_parent_cwd()

    agent = Agent(args.name, args.context, args.presentation, cwd)

    # Register cleanup
    atexit.register(agent.cleanup)

    # Handle signals
    def signal_handler(sig, frame):
        print("\nAgent shutting down...", file=sys.stderr)
        agent.running = False

        # Broadcast leave message via socket (not file)
        with agent.members_lock:
            members_to_notify = list(agent.members.keys())

        if members_to_notify:
            leave_msg = {
                'id': f"{agent.name}-{datetime.now(UTC).isoformat().replace('+00:00', 'Z')}",
                'timestamp': datetime.now(UTC).isoformat().replace('+00:00', 'Z'),
                'type': 'leave',
                'sender': {
                    'name': agent.name,
                    'context': agent.context,
                    'presentation': agent.presentation,
                },
                'content': '',
            }

            for agent_name in members_to_notify:
                try:
                    agent.send_to_agent(agent_name, leave_msg)
                except:
                    pass  # Best effort

        agent.cleanup()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        agent.run()
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
