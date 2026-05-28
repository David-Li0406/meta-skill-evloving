import json
import os
from datetime import datetime

REGISTRY_PATH = r'.agent/skills/registry.json'
CHANGELOG_PATH = r'.agent/skills/CHANGELOG.md'

def bump_version(version, bump_type='patch'):
    """语义化版本号递增: major.minor.patch"""
    parts = list(map(int, version.split('.')))
    if bump_type == 'major':
        parts[0] += 1
        parts[1] = 0
        parts[2] = 0
    elif bump_type == 'minor':
        parts[1] += 1
        parts[2] = 0
    else:  # patch
        parts[2] += 1
    return '.'.join(map(str, parts))

def update_registry_with_changelog(changes_summary, bump_type='patch'):
    """更新注册表版本并追加 changelog"""
    
    # 1. 读取当前注册表
    with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    old_version = registry.get('version', '1.0.0')
    new_version = bump_version(old_version, bump_type)
    registry['version'] = new_version
    
    # 2. 写回注册表
    with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=4, ensure_ascii=False)
    
    # 3. 追加 changelog
    today = datetime.now().strftime('%Y-%m-%d')
    changelog_entry = f"""
## [{new_version}] - {today}

### 变更 (Changed)
{changes_summary}

---
"""
    
    with open(CHANGELOG_PATH, 'r', encoding='utf-8') as f:
        existing = f.read()
    
    # 在第一个 '## [' 之前插入新条目
    insert_pos = existing.find('## [')
    if insert_pos == -1:
        new_content = existing + changelog_entry
    else:
        new_content = existing[:insert_pos] + changelog_entry + existing[insert_pos:]
    
    with open(CHANGELOG_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Registry updated: {old_version} -> {new_version}")
    print(f"Changelog appended at {CHANGELOG_PATH}")

if __name__ == "__main__":
    # 示例用法
    update_registry_with_changelog("- 初始化版本控制脚本", bump_type='patch')
