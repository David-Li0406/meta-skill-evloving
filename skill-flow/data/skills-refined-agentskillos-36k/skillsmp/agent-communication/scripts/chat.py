#!/usr/bin/env python3
"""
Multi-agent communication CLI.

Foreground tool for Claude to interact with agent daemon.
Commands: send, receive, status
"""

import sys
import json
import argparse
import socket
import struct
import os
from pathlib import Path


def get_runtime_dir():
    """Get runtime directory for socket files."""
    return Path(os.environ.get('XDG_RUNTIME_DIR', '/tmp'))


def get_chat_dir():
    """Get chat directory for registry and sockets."""
    chat_dir = get_runtime_dir() / "claude-agent-chat"
    chat_dir.mkdir(exist_ok=True)
    return chat_dir


def send_command(sock_path, command, args=None):
    """Send command to agent and return response."""
    if args is None:
        args = {}

    try:
        # Connect to agent
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(None)  # Always wait indefinitely
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

    except socket.error as e:
        return {
            'status': 'error',
            'error': f'Cannot connect to agent: {e}'
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }


def cmd_send(args, sock_path):
    """Send a message."""
    response = send_command(sock_path, 'send', {'content': args.message})

    if response['status'] == 'ok':
        data = response.get('data', {})
        delivered = data.get('delivered_to', [])
        failed = data.get('failed', {})

        result = {'status': 'ok', 'message': 'Message sent'}

        if delivered:
            result['delivered_to'] = delivered
        if failed:
            result['warnings'] = {agent: error for agent, error in failed.items()}

        print(json.dumps(result))
        return 0  # Success even with warnings
    else:
        print(json.dumps(response))
        return 1


def cmd_receive(args, sock_path):
    """Receive messages."""
    response = send_command(sock_path, 'receive', {})

    if response['status'] == 'ok':
        messages = response['data']['messages']
        print(json.dumps({'status': 'ok', 'messages': messages}, indent=2))
        return 0 if messages else 2  # Exit code 2 if no messages
    else:
        print(json.dumps(response))
        return 1


def cmd_status(args, sock_path):
    """Show status."""
    response = send_command(sock_path, 'status')

    if response['status'] == 'ok':
        print(json.dumps({'status': 'ok', 'data': response['data']}, indent=2))
        return 0
    else:
        print(json.dumps(response))
        return 1


def cmd_ask(args, sock_path):
    """Send a message and wait for response."""
    # First, send the message
    send_response = send_command(sock_path, 'send', {'content': args.message})

    if send_response['status'] != 'ok':
        print(json.dumps(send_response))
        return 1

    print(json.dumps({'status': 'ok', 'message': 'Message sent, waiting for response...'}), file=sys.stderr)

    # Then wait for responses
    receive_response = send_command(sock_path, 'receive', {})

    if receive_response['status'] == 'ok':
        messages = receive_response['data']['messages']
        print(json.dumps({'status': 'ok', 'messages': messages}, indent=2))
        return 0 if messages else 2  # Exit code 2 if no messages
    else:
        print(json.dumps(receive_response))
        return 1


def cmd_notify(args, sock_path):
    """Wait for a message notification without consuming messages."""
    response = send_command(sock_path, 'notify', {})

    if response['status'] == 'ok':
        count = response['data']['count']
        print(json.dumps({'status': 'ok', 'count': count}))
        return 0
    else:
        print(json.dumps(response))
        return 1


def cmd_leave(args, sock_path):
    """Leave the chat gracefully."""
    response = send_command(sock_path, 'leave')

    if response['status'] == 'ok':
        print(json.dumps({'status': 'ok', 'message': 'Left chat successfully'}))
        return 0
    else:
        print(json.dumps(response))
        return 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Multi-agent communication CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  chat.py --agent plugins-agent send "Hello other agents!"
  chat.py --agent plugins-agent receive
  chat.py --agent plugins-agent ask "What's the API format?"
  chat.py --agent plugins-agent notify
  chat.py --agent plugins-agent status
  chat.py --agent plugins-agent leave
        """
    )

    parser.add_argument('--agent', required=True, help='Agent name')

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # send command
    send_parser = subparsers.add_parser('send', help='Send a message')
    send_parser.add_argument('message', help='Message content')

    # receive command
    receive_parser = subparsers.add_parser('receive', help='Receive messages')

    # ask command (send + receive)
    ask_parser = subparsers.add_parser('ask', help='Send a message and wait for response')
    ask_parser.add_argument('message', help='Message content')

    # notify command
    notify_parser = subparsers.add_parser('notify', help='Wait for message notification without consuming')

    # status command
    status_parser = subparsers.add_parser('status', help='Show agent status and members')

    # leave command
    leave_parser = subparsers.add_parser('leave', help='Leave the chat gracefully')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Get agent socket path
    chat_dir = get_chat_dir()
    sock_path = str(chat_dir / f"{args.agent}.sock")

    if not os.path.exists(sock_path):
        print(json.dumps({
            'status': 'error',
            'error': f'Agent socket not found: {sock_path}'
        }))
        return 1

    # Execute command
    if args.command == 'send':
        return cmd_send(args, sock_path)
    elif args.command == 'receive':
        return cmd_receive(args, sock_path)
    elif args.command == 'ask':
        return cmd_ask(args, sock_path)
    elif args.command == 'notify':
        return cmd_notify(args, sock_path)
    elif args.command == 'status':
        return cmd_status(args, sock_path)
    elif args.command == 'leave':
        return cmd_leave(args, sock_path)
    else:
        print(json.dumps({
            'status': 'error',
            'error': f'Unknown command: {args.command}'
        }))
        return 1


if __name__ == '__main__':
    sys.exit(main())
