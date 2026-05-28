#!/usr/bin/env python3
"""
Capture TUI output from a Bubble Tea application.

This script runs a TUI application in a pseudo-terminal, optionally sends
key sequences, and captures the rendered output including ANSI escape codes.

Usage:
    python capture_tui.py <app-binary> [options]

Options:
    --keys KEY_SEQUENCE    Keys to send (e.g., "jjk" or "jj<enter><tab>")
    --width WIDTH          Terminal width (default: 80)
    --height HEIGHT        Terminal height (default: 24)
    --output FILE          Output file (default: stdout)
    --timeout SECONDS      Max wait time (default: 5)

Example:
    python capture_tui.py ./chronoflow --keys "jj<tab>" --output /tmp/output.txt
"""

import argparse
import os
import pty
import re
import select
import signal
import subprocess
import sys
import time


def parse_keys(key_string: str) -> list[str]:
    """Parse a key string into individual key events.

    Supports special keys like <enter>, <tab>, <esc>, <up>, <down>, etc.
    """
    keys = []
    i = 0
    while i < len(key_string):
        if key_string[i] == '<':
            # Look for closing >
            end = key_string.find('>', i)
            if end != -1:
                special = key_string[i+1:end].lower()
                keys.append(special)
                i = end + 1
                continue
        keys.append(key_string[i])
        i += 1
    return keys


def key_to_bytes(key: str) -> bytes:
    """Convert a key name to the corresponding byte sequence."""
    special_keys = {
        'enter': b'\r',
        'return': b'\r',
        'tab': b'\t',
        'esc': b'\x1b',
        'escape': b'\x1b',
        'space': b' ',
        'backspace': b'\x7f',
        'delete': b'\x1b[3~',
        'up': b'\x1b[A',
        'down': b'\x1b[B',
        'right': b'\x1b[C',
        'left': b'\x1b[D',
        'home': b'\x1b[H',
        'end': b'\x1b[F',
        'pgup': b'\x1b[5~',
        'pgdown': b'\x1b[6~',
        'f1': b'\x1bOP',
        'f2': b'\x1bOQ',
        'f3': b'\x1bOR',
        'f4': b'\x1bOS',
        'ctrl+c': b'\x03',
        'ctrl+d': b'\x04',
        'ctrl+p': b'\x10',
    }

    if key in special_keys:
        return special_keys[key]
    elif len(key) == 1:
        return key.encode('utf-8')
    else:
        # Unknown special key, return as-is
        return key.encode('utf-8')


def capture_tui(
    app_path: str,
    keys: str = "",
    width: int = 80,
    height: int = 24,
    timeout: float = 5.0
) -> str:
    """Capture TUI output from an application.

    Args:
        app_path: Path to the application binary
        keys: Key sequence to send (e.g., "jjk<enter>")
        width: Terminal width
        height: Terminal height
        timeout: Maximum time to wait for output

    Returns:
        The captured terminal output including ANSI escape codes
    """
    # Create a pseudo-terminal
    master_fd, slave_fd = pty.openpty()

    # Set terminal size
    import fcntl
    import struct
    import termios

    winsize = struct.pack('HHHH', height, width, 0, 0)
    fcntl.ioctl(slave_fd, termios.TIOCSWINSZ, winsize)

    # Set up environment
    env = os.environ.copy()
    env['TERM'] = 'xterm-256color'
    env['COLUMNS'] = str(width)
    env['LINES'] = str(height)

    # Start the process
    process = subprocess.Popen(
        [app_path],
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        env=env,
        preexec_fn=os.setsid
    )

    os.close(slave_fd)

    output = b''
    start_time = time.time()

    try:
        # Wait for initial render
        time.sleep(0.5)

        # Read initial output
        while True:
            ready, _, _ = select.select([master_fd], [], [], 0.1)
            if ready:
                try:
                    data = os.read(master_fd, 4096)
                    if data:
                        output += data
                    else:
                        break
                except OSError:
                    break
            else:
                break

        # Send keys if specified
        if keys:
            parsed_keys = parse_keys(keys)
            for key in parsed_keys:
                key_bytes = key_to_bytes(key)
                os.write(master_fd, key_bytes)
                time.sleep(0.1)

            # Wait for response
            time.sleep(0.5)

            # Read output after keys
            while True:
                ready, _, _ = select.select([master_fd], [], [], 0.1)
                if ready:
                    try:
                        data = os.read(master_fd, 4096)
                        if data:
                            output += data
                        else:
                            break
                    except OSError:
                        break
                else:
                    break

        # Final wait and read
        remaining = timeout - (time.time() - start_time)
        if remaining > 0:
            time.sleep(min(remaining, 0.5))
            while True:
                ready, _, _ = select.select([master_fd], [], [], 0.1)
                if ready:
                    try:
                        data = os.read(master_fd, 4096)
                        if data:
                            output += data
                        else:
                            break
                    except OSError:
                        break
                else:
                    break

    finally:
        # Clean up
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except ProcessLookupError:
            pass
        process.wait()
        os.close(master_fd)

    return output.decode('utf-8', errors='replace')


def main():
    parser = argparse.ArgumentParser(
        description='Capture TUI output from a Bubble Tea application'
    )
    parser.add_argument('app', help='Path to the application binary')
    parser.add_argument('--keys', default='', help='Key sequence to send')
    parser.add_argument('--width', type=int, default=80, help='Terminal width')
    parser.add_argument('--height', type=int, default=24, help='Terminal height')
    parser.add_argument('--output', help='Output file (default: stdout)')
    parser.add_argument('--timeout', type=float, default=5.0, help='Timeout in seconds')

    args = parser.parse_args()

    if not os.path.exists(args.app):
        print(f"Error: Application not found: {args.app}", file=sys.stderr)
        sys.exit(1)

    output = capture_tui(
        args.app,
        keys=args.keys,
        width=args.width,
        height=args.height,
        timeout=args.timeout
    )

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == '__main__':
    main()
