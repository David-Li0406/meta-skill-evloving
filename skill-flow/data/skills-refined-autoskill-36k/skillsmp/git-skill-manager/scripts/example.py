#!/usr/bin/env python3
"""
간단한 사용 예시 스크립트

이 스크립트는 install_git_plugin skill의 기본 사용법을 보여줍니다.
"""

import subprocess
import sys
import os

def run_command(cmd):
    """명령 실행 및 결과 출력"""
    print(f"\n{'='*60}")
    print(f"실행: {' '.join(cmd)}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"에러: {e}")
        return False

def main():
    """메인 함수"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    manage_script = os.path.join(script_dir, 'manage.py')
    
    print("\n🎯 Install Git Plugin Skill 사용 예시\n")
    
    # 1. 도움말 보기
    print("\n1️⃣  도움말 확인")
    run_command([sys.executable, manage_script, '--help'])
    
    # 2. 현재 설치된 plugin 목록
    print("\n2️⃣  현재 설치된 Plugin 목록")
    run_command([sys.executable, manage_script, 'list'])
    
    # 3. Install 명령 도움말
    print("\n3️⃣  Install 명령 도움말")
    run_command([sys.executable, manage_script, 'install', '--help'])
    
    # 4. Uninstall 명령 도움말
    print("\n4️⃣  Uninstall 명령 도움말")
    run_command([sys.executable, manage_script, 'uninstall', '--help'])
    
    print("\n" + "="*60)
    print("✅ 예시 완료!")
    print("="*60)
    print("\n실제 사용 예시:")
    print("  - 설치: python manage.py install --git-url \"https://github.com/user/repo\"")
    print("  - 목록: python manage.py list")
    print("  - 제거: python manage.py uninstall --skill-name \"skill-name\"")
    print()

if __name__ == '__main__':
    main()
