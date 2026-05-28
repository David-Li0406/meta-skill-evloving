#!/usr/bin/env python3
import sys
import os
import re
import subprocess
import shutil

_INT_RE = re.compile(r"-?\d+")

# C 语言兼容层 wrapper
C_WRAPPER_HEADER = """
#include <stdio.h>

int getint() {
    int x;
    if (scanf("%d", &x) != 1) return 0; 
    return x;
}

/* SysY code starts here */
#line 1 "testfile.txt"
"""

def find_compiler():
    # 优先找 clang，其次 gcc
    if shutil.which("clang"): return "clang"
    if shutil.which("gcc"): return "gcc"
    return None

def normalize_in_file(in_path: str) -> bool:
    if not os.path.exists(in_path):
        raise FileNotFoundError(in_path)

    with open(in_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    normalized_lines = []
    for idx, line in enumerate(raw_lines, start=1):
        stripped = line.strip()
        if stripped == "":
            continue
        numbers = _INT_RE.findall(stripped)
        if not numbers:
            raise ValueError(f"{in_path}:{idx}: no integer found in line: {stripped!r}")
        for number in numbers:
            normalized_lines.append(number + "\n")

    original = "".join(raw_lines)
    normalized = "".join(normalized_lines)
    if normalized != original:
        with open(in_path, "w", encoding="utf-8") as f:
            f.write(normalized)
        return True
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: run_case.py <target_directory>")
        sys.exit(1)

    target_dir = sys.argv[1]
    src_file = os.path.join(target_dir, "testfile.txt")
    in_file = os.path.join(target_dir, "in.txt")
    ans_file = os.path.join(target_dir, "ans.txt")
    tmp_c_source = os.path.join(target_dir, "__runner.c")
    tmp_binary = os.path.join(target_dir, "__runner.exe")

    if not os.path.exists(src_file):
        print(f"ERROR: {src_file} not found.")
        sys.exit(1)

    # 1. 检查编译器环境
    compiler = find_compiler()
    if not compiler:
        print("ERROR: No gcc or clang found in PATH.")
        sys.exit(1)

    # 2. 合成可编译的 C 代码
    try:
        with open(src_file, "r", encoding="utf-8") as f:
            sysy_code = f.read()
        
        with open(tmp_c_source, "w", encoding="utf-8") as f:
            f.write(C_WRAPPER_HEADER)
            f.write(sysy_code)
    except Exception as e:
        print(f"ERROR: Failed to prepare source: {e}")
        sys.exit(1)

    # 3. 编译
    # 使用 -x c 强制作为 C 语言编译, -std=c99 支持 C99 标准
    # -w 关闭警告，因为 SysY 代码转 C 可能会有很多未使用变量等警告
    cmd_compile = [compiler, "-x", "c", "-std=c99", "-O2", "-w", tmp_c_source, "-o", tmp_binary]
    
    print(f"[*] Compiling with {compiler}...")
    res_compile = subprocess.run(cmd_compile, capture_output=True, text=True)
    
    if res_compile.returncode != 0:
        print("COMPILE ERROR:")
        print(res_compile.stderr)
        sys.exit(1)

    # 3.5 规范化 in.txt：严格每行一个整数（允许从空白/空行/一行多整数自动修正）
    try:
        if normalize_in_file(in_file):
            print(f"[*] Normalized {in_file}")
    except FileNotFoundError:
        print(f"ERROR: {in_file} not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # 4. 运行并生成 ans.txt
    print("[*] Running testcase...")
    try:
        with open(in_file, "r", encoding="utf-8") as fin:
            with open(ans_file, "w", encoding="utf-8") as fout:
                # 这里的输入是从 in.txt 读取
                res_run = subprocess.run([tmp_binary], stdin=fin, stdout=fout, stderr=subprocess.PIPE, text=True, timeout=5)
                
        if res_run.returncode != 0:
            print(f"RUNTIME ERROR (Return Code {res_run.returncode}):")
            print(res_run.stderr)
            sys.exit(1)
            
        print(f"SUCCESS: Generated {ans_file}")
        
    except subprocess.TimeoutExpired:
        print("ERROR: Runtime timed out (infinite loop?).")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Execution failed: {e}")
        sys.exit(1)
    finally:
        # 清理临时文件
        if os.path.exists(tmp_c_source): os.remove(tmp_c_source)
        if os.path.exists(tmp_binary): os.remove(tmp_binary)

if __name__ == "__main__":
    main()
