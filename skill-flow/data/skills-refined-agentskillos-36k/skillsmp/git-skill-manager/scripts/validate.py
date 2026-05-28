#!/usr/bin/env python3
"""
Validation Script for install_git_plugin Skill

이 스크립트는 install_git_plugin skill이 Agent Skills 표준을
올바르게 준수하는지 검증합니다.
"""

import os
import json
import sys

def check_file_exists(filepath, description):
    """파일 존재 확인"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {os.path.basename(filepath)}")
    return exists

def check_directory_exists(dirpath, description):
    """디렉토리 존재 확인"""
    exists = os.path.isdir(dirpath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {os.path.basename(dirpath)}/")
    return exists

def check_skill_md_format(filepath):
    """SKILL.md 형식 확인"""
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # YAML frontmatter 확인
    has_frontmatter = content.startswith('---')
    required_fields = ['name:', 'description:', 'allowed-tools:']
    has_required = all(field in content for field in required_fields)
    
    status = "✅" if (has_frontmatter and has_required) else "❌"
    print(f"{status} SKILL.md YAML frontmatter 및 필수 필드")
    return has_frontmatter and has_required

def check_registry_format(filepath):
    """Registry JSON 형식 확인"""
    if not os.path.exists(filepath):
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        has_version = 'version' in data
        has_plugins = 'plugins' in data and isinstance(data['plugins'], list)
        has_updated = 'last_updated' in data
        
        valid = has_version and has_plugins and has_updated
        status = "✅" if valid else "❌"
        print(f"{status} registry.json 형식 (version, plugins, last_updated)")
        return valid
    except Exception as e:
        print(f"❌ registry.json 파싱 실패: {e}")
        return False

def check_script_executable(filepath):
    """스크립트 실행 가능 여부 확인"""
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        first_line = f.readline()
    
    has_shebang = first_line.startswith('#!')
    status = "✅" if has_shebang else "⚠️ "
    print(f"{status} {os.path.basename(filepath)} shebang line")
    return True  # Not critical

def main():
    """메인 검증 함수"""
    print("\n" + "="*60)
    print("🔍 Install Git Plugin Skill - 검증 시작")
    print("="*60 + "\n")
    
    # Skill 디렉토리 경로
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(skill_dir)  # scripts 폴더에서 상위로
    
    score = 0
    total = 0
    
    print("📁 필수 파일 확인:")
    print("-" * 60)
    checks = [
        (check_file_exists, (os.path.join(skill_dir, 'SKILL.md'), '표준 SKILL.md 파일')),
        (check_file_exists, (os.path.join(skill_dir, 'README.md'), 'README 파일')),
        (check_directory_exists, (os.path.join(skill_dir, 'scripts'), 'scripts 디렉토리')),
        (check_directory_exists, (os.path.join(skill_dir, 'assets'), 'assets 디렉토리')),
        (check_file_exists, (os.path.join(skill_dir, 'scripts', 'manage.py'), '메인 스크립트')),
        (check_file_exists, (os.path.join(skill_dir, 'assets', 'registry.json'), 'registry 파일')),
    ]
    
    for check_func, args in checks:
        total += 1
        if check_func(*args):
            score += 1
    
    print("\n📝 형식 검증:")
    print("-" * 60)
    
    total += 1
    if check_skill_md_format(os.path.join(skill_dir, 'SKILL.md')):
        score += 1
    
    total += 1
    if check_registry_format(os.path.join(skill_dir, 'data', 'registry.json')):
        score += 1
    
    total += 1
    if check_script_executable(os.path.join(skill_dir, 'scripts', 'manage.py')):
        score += 1
    
    print("\n🚫 제거된 파일 확인 (없어야 함):")
    print("-" * 60)
    
    old_files = [
        'plugin.json',
        'manifest.json',
        'index.js',
        '.claude-plugin',
        'install_plugin.py',
        'list_plugins.py',
        'remove_plugin.py'
    ]
    
    removed_count = 0
    for old_file in old_files:
        path = os.path.join(skill_dir, old_file)
        exists = os.path.exists(path)
        status = "❌" if exists else "✅"
        print(f"{status} {old_file} {'존재함 (제거 필요)' if exists else '제거 완료'}")
        if not exists:
            removed_count += 1
            score += 1
        total += 1
    
    print("\n" + "="*60)
    print(f"📊 검증 결과: {score}/{total} ({score/total*100:.1f}%)")
    print("="*60 + "\n")
    
    if score == total:
        print("🎉 완벽합니다! Agent Skills 표준을 완전히 준수합니다!")
        return 0
    elif score >= total * 0.8:
        print("✅ 좋습니다! 대부분의 요구사항을 충족합니다.")
        return 0
    elif score >= total * 0.6:
        print("⚠️  일부 개선이 필요합니다.")
        return 1
    else:
        print("❌ 추가 작업이 필요합니다.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
