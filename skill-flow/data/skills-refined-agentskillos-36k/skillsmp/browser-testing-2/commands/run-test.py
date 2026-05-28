#!/usr/bin/env python3
"""
執行瀏覽器測試腳本

Usage:
    python commands/run-test.py <test_script.py> [--server "npm run dev" --port 3000] [--auto-server]

Examples:
    # 伺服器已運行
    python commands/run-test.py my_test.py

    # 自動啟動伺服器（從 .env.test 讀取 TEST_SERVER_CMD 和 TEST_SERVER_PORT）
    python commands/run-test.py my_test.py --auto-server

    # 手動指定伺服器
    python commands/run-test.py my_test.py --server "npm run dev" --port 3000

    # 多伺服器
    python commands/run-test.py my_test.py --server "npm run api" --port 3001 --server "npm run dev" --port 3000
"""

import subprocess
import sys
import os
import argparse

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WITH_SERVER_SCRIPT = os.path.join(SKILL_DIR, 'scripts', 'with_server.py')

def load_env_file(filepath):
    """Load environment variables from a file."""
    env_vars = {}
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars

def main():
    parser = argparse.ArgumentParser(description='Execute browser test script')
    parser.add_argument('test_script', help='Test script path')
    parser.add_argument('--server', action='append', dest='servers', help='Server command (can be repeated)')
    parser.add_argument('--port', action='append', dest='ports', type=int, help='Server port (can be repeated)')
    parser.add_argument('--auto-server', action='store_true', help='Auto-start server from .env.test settings')
    parser.add_argument('--timeout', type=int, default=60, help='Server startup timeout in seconds (default: 60)')

    args = parser.parse_args()

    # 檢查測試腳本是否存在
    if not os.path.exists(args.test_script):
        print(f'[ERROR] Test script not found: {args.test_script}')
        sys.exit(1)

    # 讀取 .env.test
    env_vars = load_env_file('.env.test')
    if not env_vars:
        print('[WARN] .env.test not found or empty. Create one if login test is needed.')
        print()

    # 處理 --auto-server 選項
    if args.auto_server:
        server_cmd = env_vars.get('TEST_SERVER_CMD')
        server_port = env_vars.get('TEST_SERVER_PORT')
        if server_cmd and server_port:
            args.servers = [server_cmd]
            args.ports = [int(server_port)]
            print(f'[AUTO] Using server from .env.test: {server_cmd} on port {server_port}')
        else:
            print('[ERROR] --auto-server requires TEST_SERVER_CMD and TEST_SERVER_PORT in .env.test')
            sys.exit(1)

    # 設定 PYTHONPATH 讓測試腳本能 import browser_testing
    lib_dir = os.path.join(SKILL_DIR, 'lib')
    env = os.environ.copy()
    pythonpath = env.get('PYTHONPATH', '')
    if pythonpath:
        env['PYTHONPATH'] = f"{lib_dir}{os.pathsep}{pythonpath}"
    else:
        env['PYTHONPATH'] = lib_dir

    # 決定是否需要啟動伺服器
    if args.servers and args.ports:
        if len(args.servers) != len(args.ports):
            print('[ERROR] --server and --port count must match')
            sys.exit(1)

        # 使用 with_server.py 啟動伺服器
        cmd = ['python', WITH_SERVER_SCRIPT]
        cmd.extend(['--timeout', str(args.timeout)])
        for server, port in zip(args.servers, args.ports):
            cmd.extend(['--server', server, '--port', str(port)])
        cmd.extend(['--', 'python', args.test_script])

        print(f'[RUN] Starting server and running test...')
        print(f'   Command: {" ".join(cmd)}\n')
        result = subprocess.run(cmd, env=env)
    else:
        # 直接執行測試
        print(f'[RUN] Running test: {args.test_script}\n')
        result = subprocess.run(['python', args.test_script], env=env)

    sys.exit(result.returncode)

if __name__ == '__main__':
    main()
