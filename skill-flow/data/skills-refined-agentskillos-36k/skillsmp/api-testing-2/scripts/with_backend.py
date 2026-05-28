#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
后端服务器生命周期管理

启动后端服务器，等待其就绪，然后执行测试命令。
测试完成后自动关闭服务器。

使用方法：
    python with_backend.py --help

示例：
    # 启动后端并运行测试
    python with_backend.py --server "python run.py" --port 5000 -- pytest tests/api/ -v
    
    # 指定工作目录
    python with_backend.py --server "python run.py" --port 5000 --cwd platform-fastapi-server -- pytest tests/ -v
    
    # 自定义超时时间
    python with_backend.py --server "python run.py" --port 5000 --timeout 60 -- pytest tests/ -v
"""

import argparse
import os
import signal
import socket
import subprocess
import sys
import time
from typing import List, Optional


def is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    """检查端口是否开放"""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def wait_for_port(
    host: str,
    port: int,
    timeout: int = 30,
    interval: float = 0.5
) -> bool:
    """
    等待端口就绪
    
    Args:
        host: 主机地址
        port: 端口号
        timeout: 超时时间（秒）
        interval: 检查间隔（秒）
        
    Returns:
        端口是否就绪
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_port_open(host, port):
            return True
        time.sleep(interval)
    return False


def start_server(
    command: str,
    cwd: Optional[str] = None,
    env: Optional[dict] = None
) -> subprocess.Popen:
    """
    启动服务器进程
    
    Args:
        command: 启动命令
        cwd: 工作目录
        env: 环境变量
        
    Returns:
        服务器进程对象
    """
    # 合并环境变量
    process_env = os.environ.copy()
    if env:
        process_env.update(env)
    
    # 根据操作系统选择 shell
    if sys.platform == "win32":
        # Windows 使用 cmd
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            env=process_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:
        # Unix 使用 bash
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            env=process_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            preexec_fn=os.setsid
        )
    
    return process


def stop_server(process: subprocess.Popen) -> None:
    """
    停止服务器进程
    
    Args:
        process: 服务器进程对象
    """
    if process.poll() is None:  # 进程仍在运行
        try:
            if sys.platform == "win32":
                # Windows: 发送 CTRL_BREAK_EVENT
                process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                # Unix: 发送 SIGTERM 到进程组
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            
            # 等待进程退出
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # 强制终止
            if sys.platform == "win32":
                process.kill()
            else:
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            process.wait()
        except Exception as e:
            print(f"停止服务器时出错: {e}")
            process.kill()


def run_command(command: List[str], cwd: Optional[str] = None) -> int:
    """
    运行测试命令
    
    Args:
        command: 命令列表
        cwd: 工作目录
        
    Returns:
        命令退出码
    """
    process = subprocess.run(command, cwd=cwd)
    return process.returncode


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="后端服务器生命周期管理",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 启动后端并运行 pytest
  python with_backend.py --server "python run.py" --port 5000 -- pytest tests/api/ -v
  
  # 指定工作目录
  python with_backend.py --server "python run.py" --port 5000 --cwd platform-fastapi-server -- pytest tests/ -v
  
  # 自定义超时和主机
  python with_backend.py --server "python run.py" --port 5000 --host 127.0.0.1 --timeout 60 -- pytest tests/ -v
  
  # 设置环境变量
  python with_backend.py --server "python run.py" --port 5000 --env DB_TYPE=sqlite -- pytest tests/ -v
"""
    )
    
    parser.add_argument(
        "--server",
        required=True,
        help="服务器启动命令"
    )
    parser.add_argument(
        "--port",
        type=int,
        required=True,
        help="服务器端口"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="服务器主机地址（默认: 127.0.0.1）"
    )
    parser.add_argument(
        "--cwd",
        help="服务器工作目录"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="等待服务器就绪的超时时间（秒，默认: 30）"
    )
    parser.add_argument(
        "--env",
        action="append",
        help="环境变量（格式: KEY=VALUE，可多次指定）"
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="要执行的测试命令（在 -- 之后）"
    )
    
    args = parser.parse_args()
    
    # 解析测试命令
    test_command = args.command
    if test_command and test_command[0] == "--":
        test_command = test_command[1:]
    
    if not test_command:
        print("错误: 请在 -- 之后指定要执行的命令")
        parser.print_help()
        sys.exit(1)
    
    # 解析环境变量
    env = {}
    if args.env:
        for item in args.env:
            if "=" in item:
                key, value = item.split("=", 1)
                env[key] = value
    
    # 检查端口是否已被占用
    if is_port_open(args.host, args.port):
        print(f"⚠️  端口 {args.port} 已被占用，假设服务器已在运行")
        print(f"🚀 执行命令: {' '.join(test_command)}")
        exit_code = run_command(test_command)
        sys.exit(exit_code)
    
    # 启动服务器
    print(f"🔧 启动服务器: {args.server}")
    if args.cwd:
        print(f"📁 工作目录: {args.cwd}")
    
    server_process = start_server(args.server, cwd=args.cwd, env=env or None)
    
    try:
        # 等待服务器就绪
        print(f"⏳ 等待服务器就绪 (端口 {args.port})...")
        if not wait_for_port(args.host, args.port, timeout=args.timeout):
            print(f"❌ 服务器启动超时（{args.timeout}秒）")
            
            # 输出服务器日志
            if server_process.stdout:
                output = server_process.stdout.read()
                if output:
                    print(f"\n服务器输出:\n{output.decode('utf-8', errors='ignore')}")
            
            stop_server(server_process)
            sys.exit(1)
        
        print(f"✅ 服务器已就绪: http://{args.host}:{args.port}")
        
        # 执行测试命令
        print(f"🚀 执行命令: {' '.join(test_command)}")
        print("-" * 60)
        
        exit_code = run_command(test_command)
        
        print("-" * 60)
        if exit_code == 0:
            print("✅ 命令执行成功")
        else:
            print(f"❌ 命令执行失败 (退出码: {exit_code})")
        
    finally:
        # 停止服务器
        print("🛑 停止服务器...")
        stop_server(server_process)
        print("✅ 服务器已停止")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
