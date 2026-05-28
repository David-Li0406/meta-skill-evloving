#!/usr/bin/env python3

"""
Install/Uninstall Git Plugin Skill

설명: Git repository에서 Claude plugin을 설치/제거합니다.
설치된 plugins은 registry.json으로 관리됩니다.

사용 예시:
설치:
python manage.py install --git-url "https://github.com/gabrielwithappy/obsidian-skills"

제거:
python manage.py uninstall --skill-name "json-canvas"

목록 조회:
python manage.py list
"""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
import shutil
import argparse


def get_registry_path(target_path: str) -> str:
    """registry.json 파일 경로 반환"""
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    registry_file = os.path.join(script_dir, 'assets', 'registry.json')
    return registry_file


def load_registry(target_path: str) -> Dict[str, Any]:
    """설치된 plugins 레지스트리 로드"""
    registry_path = get_registry_path(target_path)
    
    if os.path.exists(registry_path):
        try:
            with open(registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    
    return {
        'version': '1.0.0',
        'plugins': [],
        'last_updated': datetime.now().isoformat()
    }


def save_registry(target_path: str, registry: Dict[str, Any]) -> None:
    """레지스트리 저장"""
    registry_path = get_registry_path(target_path)
    registry['last_updated'] = datetime.now().isoformat()
    
    os.makedirs(os.path.dirname(registry_path), exist_ok=True)
    with open(registry_path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)


def add_to_registry(target_path: str, plugin_info: Dict[str, Any]) -> None:
    """레지스트리에 plugin 추가"""
    registry = load_registry(target_path)
    
    # 중복 확인
    for plugin in registry['plugins']:
        if plugin['name'] == plugin_info['name']:
            plugin.update(plugin_info)
            save_registry(target_path, registry)
            return
    
    registry['plugins'].append(plugin_info)
    save_registry(target_path, registry)


def remove_from_registry(target_path: str, skill_name: str) -> bool:
    """레지스트리에서 plugin 제거"""
    registry = load_registry(target_path)
    original_count = len(registry['plugins'])
    registry['plugins'] = [p for p in registry['plugins'] if p['name'] != skill_name]
    
    if len(registry['plugins']) < original_count:
        save_registry(target_path, registry)
        return True
    return False


def extract_repo_name(git_url: str) -> str:
    """Git URL에서 repository 이름 추출"""
    return git_url.rstrip('/').split('/')[-1].replace('.git', '')


def ensure_directory_exists(dir_path: str) -> None:
    """디렉토리 생성"""
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def fetch_github_file(owner: str, repo: str, file_path: str) -> Optional[str]:
    """GitHub에서 파일 다운로드"""
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{file_path}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Claude-Plugin-Installer'})
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise Exception(f"HTTP {e.code}: {e.reason}")
    except Exception as e:
        return None


def fetch_github_directory_structure(owner: str, repo: str, path: str = '') -> list:
    """GitHub API를 사용하여 디렉토리 구조 조회"""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Claude-Plugin-Installer'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            if isinstance(data, list):
                return data
            return []
    except Exception as e:
        return []


def download_directory_recursively(owner: str, repo: str, path: str, files: Dict, max_depth: int = 3, current_depth: int = 0) -> None:
    """GitHub 디렉토리를 재귀적으로 다운로드"""
    if current_depth >= max_depth:
        return
    
    try:
        contents = fetch_github_directory_structure(owner, repo, path)
        for item in contents:
            if item['type'] == 'file':
                file_path = item['path']
                try:
                    content = fetch_github_file(owner, repo, file_path)
                    if content:
                        files[file_path] = content
                except Exception:
                    pass
            elif item['type'] == 'dir':
                download_directory_recursively(owner, repo, item['path'], files, max_depth, current_depth + 1)
    except Exception as e:
        pass


def fetch_plugin_config(owner: str, repo: str) -> Optional[Dict]:
    """GitHub 저장소의 .claude-plugin/plugin.json 설정 읽기"""
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/.claude-plugin/plugin.json"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Claude-Plugin-Installer'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            return json.loads(content)
    except Exception:
        return None


def download_plugin_files(git_url: str, plugin_name: str) -> Dict[str, Optional[str]]:
    """Git repository에서 플러그인 파일들 다운로드"""
    api_url = git_url.replace('https://github.com/', '').replace('http://github.com/', '').replace('.git', '')
    
    parts = api_url.split('/')
    if len(parts) < 2:
        raise Exception(f"Invalid Git URL: {git_url}")
    
    owner, repo = parts[0], parts[1]
    files = {}
    
    # 주요 파일들
    main_files = ['README.md', 'LICENSE']
    
    for file_name in main_files:
        try:
            content = fetch_github_file(owner, repo, file_name)
            if content:
                files[file_name] = content
        except Exception as e:
            pass
    
    # .claude-plugin/plugin.json
    try:
        plugin_config = fetch_plugin_config(owner, repo)
        if plugin_config:
            files['.claude-plugin/plugin.json'] = json.dumps(plugin_config, indent=2, ensure_ascii=False)
    except Exception as e:
        pass
    
    # .claude/skills 디렉토리
    try:
        download_directory_recursively(owner, repo, '.claude/skills', files)
    except Exception as e:
        pass
    
    return files


def save_plugin_files(plugin_path: str, files: Dict[str, Optional[str]]) -> None:
    """플러그인 파일들 저장"""
    for file_name, content in files.items():
        if content:
            file_path = os.path.join(plugin_path, file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)


def read_plugin_info(git_url: str) -> Dict[str, Any]:
    """플러그인 정보 생성"""
    api_url = git_url.replace('https://github.com/', '').replace('http://github.com/', '').replace('.git', '')
    parts = api_url.split('/')
    
    owner = parts[0] if len(parts) > 0 else 'unknown'
    repo = parts[1] if len(parts) > 1 else 'unknown-plugin'
    
    return {
        'name': repo,
        'repository': git_url,
        'owner': owner,
        'installed_at': datetime.now().isoformat(),
        'status': 'active'
    }


def install_plugin(git_url: str, plugin_name: Optional[str] = None, target_path: str = '.claude') -> Dict[str, Any]:
    """Claude plugin/skills 설치"""
    try:
        if not git_url:
            raise Exception("git_url 파라미터가 필요합니다")
        
        plugin_name = plugin_name or extract_repo_name(git_url)
        
        # 파일 다운로드
        api_url = git_url.replace('https://github.com/', '').replace('http://github.com/', '').replace('.git', '')
        parts = api_url.split('/')
        owner, repo = parts[0], parts[1]
        
        print(f"📦 '{plugin_name}' 다운로드 중...")
        plugin_config = fetch_plugin_config(owner, repo)
        files = download_plugin_files(git_url, plugin_name)
        plugin_info = read_plugin_info(git_url)
        
        # 설치
        skills_path = os.path.join(target_path, 'skills')
        ensure_directory_exists(skills_path)
        
        skill_paths = []
        for file_path, content in files.items():
            if file_path.startswith('.claude/skills/') and content:
                parts = file_path.split('/')
                if len(parts) >= 4:
                    skill_name = parts[2]
                    skill_file = '/'.join(parts[3:])
                    skill_dir = os.path.join(skills_path, skill_name)
                    ensure_directory_exists(skill_dir)
                    
                    file_full_path = os.path.join(skill_dir, skill_file)
                    ensure_directory_exists(os.path.dirname(file_full_path))
                    with open(file_full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    if skill_dir not in skill_paths:
                        skill_paths.append(skill_dir)
        

        # 레지스트리 기록
        registry_info = {
            'name': plugin_name,
            'git_url': git_url,
            'owner': owner,
            'repo': repo,
            'target_path': target_path,
            'installed_at': datetime.now().isoformat(),
            'skills': [os.path.basename(p) for p in skill_paths],
            'status': 'installed'
        }
        add_to_registry(target_path, registry_info)
        
        print(f"✓ 플러그인 '{plugin_name}'이(가) 성공적으로 설치되었습니다.")
        print(f"✓ {len(set(skill_paths))}개의 skill이 설치되었습니다:")
        for skill_path in sorted(set(skill_paths)):
            print(f"  - {skill_path}")
        
        return {
            'status': 'success',
            'action': 'install',
            'message': f"플러그인 '{plugin_name}'이(가) 성공적으로 설치되었습니다.",
            'install_path': os.path.join(target_path, 'skills'),
            'skills_count': len(set(skill_paths)),
            'skill_paths': list(set(skill_paths))
        }
    except Exception as error:
        print(f"✗ 플러그인 설치 실패: {str(error)}")
        return {
            'status': 'error',
            'action': 'install',
            'message': f"플러그인 설치 실패: {str(error)}"
        }


def uninstall_plugin(skill_name: str, target_path: str = '.claude') -> Dict[str, Any]:
    """설치된 skill 제거"""
    try:
        if not skill_name:
            raise Exception("skill_name 파라미터가 필요합니다")
        
        skill_path = os.path.join(target_path, 'skills', skill_name)
        
        if not os.path.exists(skill_path):
            raise Exception(f"스킬 '{skill_name}'을(를) 찾을 수 없습니다")
        
        # 삭제
        deleted_files = []
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                deleted_files.append(os.path.join(root, file))
        
        print(f"🗑️  '{skill_name}' 제거 중...")
        shutil.rmtree(skill_path)
        
        # 레지스트리 업데이트
        removed = remove_from_registry(target_path, skill_name)
        
        print(f"✓ 스킬 '{skill_name}'이(가) 성공적으로 제거되었습니다.")
        print(f"✓ {len(deleted_files)}개의 파일이 삭제되었습니다.")
        
        return {
            'status': 'success',
            'action': 'uninstall',
            'message': f"스킬 '{skill_name}'이(가) 성공적으로 제거되었습니다.",
            'removed_path': skill_path,
            'deleted_file_count': len(deleted_files),
            'registry_updated': removed
        }
    except Exception as error:
        print(f"✗ 스킬 제거 실패: {str(error)}")
        return {
            'status': 'error',
            'action': 'uninstall',
            'message': f"스킬 제거 실패: {str(error)}"
        }


def list_plugins(target_path: str = '.claude') -> Dict[str, Any]:
    """설치된 plugins 목록 조회"""
    try:
        registry = load_registry(target_path)
        
        print(f"\n📋 설치된 Plugin 목록 ({len(registry['plugins'])}개):")
        print("=" * 60)
        
        if not registry['plugins']:
            print("설치된 플러그인이 없습니다.")
        else:
            for idx, plugin in enumerate(registry['plugins'], 1):
                print(f"\n{idx}. {plugin['name']}")
                print(f"   Repository: {plugin.get('git_url', 'N/A')}")
                print(f"   Owner: {plugin.get('owner', 'N/A')}")
                print(f"   Installed: {plugin.get('installed_at', 'N/A')}")
                if plugin.get('skills'):
                    print(f"   Skills: {', '.join(plugin['skills'])}")
        
        print("\n" + "=" * 60)
        print(f"Last Updated: {registry.get('last_updated', 'N/A')}\n")
        
        return {
            'status': 'success',
            'action': 'list',
            'message': f"{len(registry['plugins'])}개의 플러그인이 설치되어 있습니다.",
            'plugins': registry['plugins'],
            'last_updated': registry.get('last_updated'),
            'target_path': target_path
        }
    except Exception as error:
        print(f"✗ 플러그인 목록 조회 실패: {str(error)}")
        return {
            'status': 'error',
            'action': 'list',
            'message': f"플러그인 목록 조회 실패: {str(error)}"
        }


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description='Git repository에서 Claude skill plugin을 설치/제거/관리합니다.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  # Plugin 설치
  %(prog)s install --git-url "https://github.com/user/repo"
  
  # Plugin 목록 조회
  %(prog)s list
  
  # Plugin 제거
  %(prog)s uninstall --skill-name "skill-name"
        """
    )
    
    subparsers = parser.add_subparsers(dest='action', help='수행할 작업')
    
    # Install subcommand
    install_parser = subparsers.add_parser('install', help='Plugin 설치')
    install_parser.add_argument('--git-url', required=True, help='Git repository URL')
    install_parser.add_argument('--plugin-name', help='설치할 플러그인 이름 (선택사항)')
    install_parser.add_argument('--target-path', default='.claude', help='설치 대상 경로 (기본값: .claude)')
    
    # Uninstall subcommand
    uninstall_parser = subparsers.add_parser('uninstall', help='Plugin 제거')
    uninstall_parser.add_argument('--skill-name', required=True, help='제거할 스킬 이름')
    uninstall_parser.add_argument('--target-path', default='.claude', help='대상 경로 (기본값: .claude)')
    
    # List subcommand
    list_parser = subparsers.add_parser('list', help='설치된 Plugin 목록')
    list_parser.add_argument('--target-path', default='.claude', help='대상 경로 (기본값: .claude)')
    
    args = parser.parse_args()
    
    if not args.action:
        parser.print_help()
        sys.exit(1)
    
    if args.action == 'install':
        result = install_plugin(args.git_url, args.plugin_name, args.target_path)
    elif args.action == 'uninstall':
        result = uninstall_plugin(args.skill_name, args.target_path)
    elif args.action == 'list':
        result = list_plugins(args.target_path)
    else:
        print(f"알 수 없는 action: {args.action}")
        sys.exit(1)
    
    sys.exit(0 if result['status'] == 'success' else 1)


if __name__ == '__main__':
    main()
