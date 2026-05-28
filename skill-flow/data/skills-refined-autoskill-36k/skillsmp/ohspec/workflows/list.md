# /ohspec:list - RFC 列表管理

## 命令说明
列出所有 RFC 项目，展示其状态、进度和最后更新时间，帮助用户快速了解项目全貌。

## 使用方式
```bash
/ohspec:list
/ohspec:list --status=DESIGNING  # 按状态过滤
/ohspec:list --limit=10          # 限制显示数量
```

## 工作流程

### 步骤1：扫描 RFC 目录
扫描 `.ohspec/rfcs/` 目录，获取所有 RFC 项目（兼容：`.claude/ohspec/rfcs/`）：

```python
import os
import re
from datetime import datetime

RFC_BASE_DIR = ".ohspec/rfcs"

def scan_rfcs():
    """扫描所有 RFC 目录"""
    rfcs = []

    if not os.path.exists(RFC_BASE_DIR):
        print(f"RFC 目录不存在：{RFC_BASE_DIR}")
        return rfcs

    # 遍历所有子目录
    for rfc_dir in os.listdir(RFC_BASE_DIR):
        rfc_path = os.path.join(RFC_BASE_DIR, rfc_dir)

        # 检查是否是目录且符合 RFC-YYYYMMDD-HHMMSS 格式
        if os.path.isdir(rfc_path) and rfc_dir.startswith("RFC-"):
            progress_file = os.path.join(rfc_path, "progress.json")

            if os.path.exists(progress_file):
                metadata = extract_metadata(progress_file)
                if metadata:
                    rfcs.append(metadata)

    return rfcs
```

### 步骤2：提取元数据
从每个 RFC 的 `progress.json` 文件中提取元数据：

```python
def extract_metadata(progress_file):
    """从 progress.json 提取元数据"""
    try:
        with open(progress_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取元数据字段（使用正则表达式）
        metadata = {}

        # RFC ID
        match = re.search(r'> RFC ID:\s*(.+)', content)
        if match:
            metadata['rfc_id'] = match.group(1).strip()

        # RFC 标题
        match = re.search(r'> RFC:\s*(.+)', content)
        if match:
            metadata['title'] = match.group(1).strip()

        # 状态
        match = re.search(r'> 状态:\s*(.+)', content)
        if match:
            metadata['status'] = match.group(1).strip()

        # 完成度
        match = re.search(r'> 完成度:\s*(\d+)%', content)
        if match:
            metadata['progress'] = int(match.group(1))

        # 最后更新时间
        match = re.search(r'> 最后更新:\s*(.+)', content)
        if match:
            metadata['last_updated'] = match.group(1).strip()

        # 当前阶段
        match = re.search(r'> 当前阶段:\s*(.+)', content)
        if match:
            metadata['current_phase'] = match.group(1).strip()

        # 用户需求
        match = re.search(r'> 用户需求:\s*(.+)', content)
        if match:
            metadata['user_requirement'] = match.group(1).strip()

        return metadata

    except Exception as e:
        print(f"读取 {progress_file} 失败：{e}")
        return None
```

### 步骤3：排序和过滤
根据参数对 RFC 列表进行排序和过滤：

```python
def filter_and_sort_rfcs(rfcs, status_filter=None, limit=None):
    """过滤和排序 RFC 列表"""
    # 状态过滤
    if status_filter:
        rfcs = [rfc for rfc in rfcs if rfc.get('status') == status_filter]

    # 按最后更新时间倒序排序
    rfcs.sort(key=lambda x: x.get('last_updated', ''), reverse=True)

    # 限制数量
    if limit:
        rfcs = rfcs[:limit]

    return rfcs
```

### 步骤4：格式化输出
将 RFC 列表格式化为易读的表格：

```python
def format_rfc_list(rfcs):
    """格式化 RFC 列表输出"""
    if not rfcs:
        print("未找到任何 RFC 项目")
        return

    print(f"\n📋 RFC 列表（共 {len(rfcs)} 个）\n")
    print("=" * 120)
    print(f"{'RFC ID':<25} | {'标题':<30} | {'状态':<12} | {'阶段':<10} | {'完成度':<8} | {'最后更新':<20}")
    print("=" * 120)

    for rfc in rfcs:
        rfc_id = rfc.get('rfc_id', 'N/A')
        title = rfc.get('title', 'N/A')
        status = rfc.get('status', 'N/A')
        phase = rfc.get('current_phase', 'N/A')
        progress = f"{rfc.get('progress', 0)}%"
        last_updated = rfc.get('last_updated', 'N/A')

        # 截断过长的标题
        if len(title) > 30:
            title = title[:27] + "..."

        print(f"{rfc_id:<25} | {title:<30} | {status:<12} | {phase:<10} | {progress:<8} | {last_updated:<20}")

    print("=" * 120)
```

### 步骤5：按状态分组展示（完整版）
完整版支持按状态分组展示：

```python
def format_rfc_list_grouped(rfcs):
    """按状态分组展示 RFC 列表"""
    if not rfcs:
        print("未找到任何 RFC 项目")
        return

    # 按状态分组
    grouped = {}
    for rfc in rfcs:
        status = rfc.get('status', 'UNKNOWN')
        if status not in grouped:
            grouped[status] = []
        grouped[status].append(rfc)

    # 状态优先级排序
    status_order = ['ANALYZING', 'DESIGNING', 'AUDITING', 'APPROVED', 'REJECTED', 'DRAFT']

    print(f"\n📋 RFC 列表（共 {len(rfcs)} 个）\n")

    for status in status_order:
        if status in grouped:
            rfcs_in_status = grouped[status]
            print(f"\n## {status}（{len(rfcs_in_status)} 个）")
            print("-" * 120)

            for rfc in rfcs_in_status:
                rfc_id = rfc.get('rfc_id', 'N/A')
                title = rfc.get('title', 'N/A')
                phase = rfc.get('current_phase', 'N/A')
                progress = f"{rfc.get('progress', 0)}%"
                last_updated = rfc.get('last_updated', 'N/A')

                print(f"  {rfc_id} | {title}")
                print(f"    阶段: {phase} | 完成度: {progress} | 最后更新: {last_updated}")
                print()
```

### 步骤6：提供快速恢复链接
为每个未完成的 RFC 提供快速恢复命令：

```python
def show_resume_hints(rfcs):
    """显示快速恢复提示"""
    incomplete_rfcs = [
        rfc for rfc in rfcs
        if rfc.get('status') not in ['APPROVED', 'REJECTED']
    ]

    if incomplete_rfcs:
        print("\n💡 快速恢复命令：")
        print("-" * 60)
        for rfc in incomplete_rfcs[:5]:  # 只显示前5个
            rfc_id = rfc.get('rfc_id', 'N/A')
            phase = rfc.get('current_phase', 'N/A')
            print(f"  /ohspec:resume {rfc_id}  # 继续 {phase} 阶段")

        if len(incomplete_rfcs) > 5:
            print(f"  ... 还有 {len(incomplete_rfcs) - 5} 个未完成的 RFC")
        print()
```

## 完整示例

### MVP 简化版
```python
# 主函数
def list_rfcs(status_filter=None, limit=None, grouped=False):
    """列出所有 RFC"""
    # 步骤1：扫描 RFC 目录
    rfcs = scan_rfcs()

    # 步骤2：过滤和排序
    rfcs = filter_and_sort_rfcs(rfcs, status_filter, limit)

    # 步骤3：格式化输出
    if grouped:
        format_rfc_list_grouped(rfcs)
    else:
        format_rfc_list(rfcs)

    # 步骤4：显示快速恢复提示
    show_resume_hints(rfcs)

# 调用示例
list_rfcs()  # 列出所有 RFC
list_rfcs(status_filter='DESIGNING')  # 只显示设计中的 RFC
list_rfcs(limit=10)  # 只显示最近 10 个 RFC
list_rfcs(grouped=True)  # 按状态分组显示
```

## 输出示例

### 简单列表模式
```
📋 RFC 列表（共 3 个）

========================================================================================
RFC ID                    | 标题                           | 状态         | 阶段       | 完成度   | 最后更新
========================================================================================
RFC-20240114-120000       | 为音频服务增加3D音效开关        | DESIGNING    | design     | 60%      | 2024-01-14 12:30:00
RFC-20240113-100000       | 添加视频编码器                 | APPROVED     | audit      | 100%     | 2024-01-13 15:00:00
RFC-20240112-090000       | 优化内存管理                   | ANALYZING    | analyze    | 30%      | 2024-01-12 09:30:00
========================================================================================

💡 快速恢复命令：
------------------------------------------------------------
  /ohspec:resume RFC-20240114-120000  # 继续 design 阶段
  /ohspec:resume RFC-20240112-090000  # 继续 analyze 阶段
```

### 分组模式
```
📋 RFC 列表（共 3 个）

## DESIGNING（1 个）
------------------------------------------------------------
  RFC-20240114-120000 | 为音频服务增加3D音效开关
    阶段: design | 完成度: 60% | 最后更新: 2024-01-14 12:30:00

## APPROVED（1 个）
------------------------------------------------------------
  RFC-20240113-100000 | 添加视频编码器
    阶段: audit | 完成度: 100% | 最后更新: 2024-01-13 15:00:00

## ANALYZING（1 个）
------------------------------------------------------------
  RFC-20240112-090000 | 优化内存管理
    阶段: analyze | 完成度: 30% | 最后更新: 2024-01-12 09:30:00
```

## 输出物
- 控制台输出：RFC 列表和快速恢复提示

## 错误处理
- RFC 目录不存在 → 提示用户先创建 RFC
- progress.json 文件损坏 → 跳过该 RFC，记录警告
- 无可用 RFC → 提示"未找到任何 RFC 项目"

## 扩展功能（未来版本）

### 搜索功能
```bash
/ohspec:list --search="音频"  # 搜索标题包含"音频"的 RFC
```

### 导出功能
```bash
/ohspec:list --export=csv  # 导出为 CSV 文件
/ohspec:list --export=json # 导出为 JSON 文件
```

### 统计信息
```bash
/ohspec:list --stats  # 显示统计信息（总数、各状态数量、平均完成度）
```

## 日志滚动窗口（P3-2）

### 滚动规则

日志滚动窗口机制用于管理 progress.json 的生命周期，防止日志无限增长：

| 规则 | 说明 |
|------|------|
| 保留范围 | 最近 3 个 RFC 的完整日志 |
| 旧日志处理 | 压缩归档到 `workflows/archive/` |
| 触发条件 | RFC 数量 > 3 或手动触发或 Token 预警 |
| 归档格式 | tar.gz（包含 progress.json + findings.json） |
| 保留文件 | rfc.md（RFC 文档）、checkpoints/（检查点快照） |

### 滚动触发条件

```python
def should_trigger_log_rotation(rfc_count: int, token_usage_ratio: float = None) -> bool:
    """
    判断是否需要触发日志滚动

    参数：
        rfc_count: 当前 RFC 总数
        token_usage_ratio: Token 使用比例（可选）

    返回：
        True 表示需要滚动，False 表示不需要
    """
    # 条件1：RFC 数量超过 3 个
    if rfc_count > 3:
        return True

    # 条件2：Token 使用达到黄色预警（50%）
    if token_usage_ratio and token_usage_ratio >= 0.50:
        return True

    return False
```

### 步骤1：识别最近 3 个 RFC

按创建时间或更新时间识别最近 3 个 RFC，其余为旧 RFC：

```python
def identify_recent_rfcs(rfcs: list, keep_count: int = 3) -> tuple[list, list]:
    """
    识别最近的 RFC 和旧 RFC

    参数：
        rfcs: RFC 列表（包含元数据）
        keep_count: 保留的 RFC 数量（默认 3）

    返回：
        (recent_rfcs, old_rfcs) - 最近的 RFC 和旧 RFC
    """
    # 按最后更新时间倒序排序
    sorted_rfcs = sorted(
        rfcs,
        key=lambda x: x.get('last_updated', ''),
        reverse=True
    )

    # 分割为最近和旧 RFC
    recent_rfcs = sorted_rfcs[:keep_count]
    old_rfcs = sorted_rfcs[keep_count:]

    return recent_rfcs, old_rfcs
```

### 步骤2：压缩旧日志

将旧 RFC 的日志文件压缩归档：

```python
import os
import tarfile
import json
from datetime import datetime

ARCHIVE_DIR = ".ohspec/archive"
RFC_BASE_DIR = ".ohspec/rfcs"

def archive_old_logs(old_rfcs: list) -> dict:
    """
    压缩归档旧 RFC 的日志

    参数：
        old_rfcs: 旧 RFC 列表

    返回：
        {
            'archived_count': 归档数量,
            'total_size': 总大小（字节）,
            'archive_files': [归档文件列表],
            'errors': [错误列表]
        }
    """
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    result = {
        'archived_count': 0,
        'total_size': 0,
        'archive_files': [],
        'errors': []
    }

    for rfc in old_rfcs:
        rfc_id = rfc.get('rfc_id')
        rfc_dir = os.path.join(RFC_BASE_DIR, rfc_id)

        if not os.path.exists(rfc_dir):
            result['errors'].append(f"RFC 目录不存在：{rfc_dir}")
            continue

        try:
            # 1. 创建归档文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"{rfc_id}_{timestamp}.tar.gz"
            archive_path = os.path.join(ARCHIVE_DIR, archive_name)

            # 2. 创建 tar.gz 文件
            with tarfile.open(archive_path, "w:gz") as tar:
                # 添加 progress.json
                progress_file = os.path.join(rfc_dir, "progress.json")
                if os.path.exists(progress_file):
                    tar.add(progress_file, arcname=f"{rfc_id}/progress.json")

                # 添加 findings.json
                findings_file = os.path.join(rfc_dir, "findings.json")
                if os.path.exists(findings_file):
                    tar.add(findings_file, arcname=f"{rfc_id}/findings.json")

                # 添加 audit_log（如果存在）
                audit_log_file = os.path.join(rfc_dir, "audit_log.json")
                if os.path.exists(audit_log_file):
                    tar.add(audit_log_file, arcname=f"{rfc_id}/audit_log.json")

            # 3. 记录归档信息
            archive_size = os.path.getsize(archive_path)
            result['archived_count'] += 1
            result['total_size'] += archive_size
            result['archive_files'].append({
                'rfc_id': rfc_id,
                'archive_file': archive_name,
                'archive_path': archive_path,
                'size': archive_size,
                'created_at': datetime.now().isoformat()
            })

            print(f"✅ 已归档 {rfc_id}：{archive_name}（{archive_size / 1024:.1f} KB）")

        except Exception as e:
            result['errors'].append(f"归档 {rfc_id} 失败：{str(e)}")
            print(f"❌ 归档 {rfc_id} 失败：{str(e)}")

    return result
```

### 步骤3：清理原始日志文件

从 RFC 目录中删除已归档的日志文件，保留 RFC 文档和检查点：

```python
def cleanup_archived_logs(old_rfcs: list, archive_result: dict) -> dict:
    """
    清理已归档的日志文件

    参数：
        old_rfcs: 旧 RFC 列表
        archive_result: 归档结果

    返回：
        {
            'cleaned_count': 清理数量,
            'freed_space': 释放空间（字节）,
            'errors': [错误列表]
        }
    """
    result = {
        'cleaned_count': 0,
        'freed_space': 0,
        'errors': []
    }

    # 只清理成功归档的 RFC
    archived_rfc_ids = [
        item['rfc_id'] for item in archive_result.get('archive_files', [])
    ]

    for rfc_id in archived_rfc_ids:
        rfc_dir = os.path.join(RFC_BASE_DIR, rfc_id)

        # 删除的文件列表
        files_to_delete = [
            'progress.json',
            'findings.json',
            'audit_log.json'
        ]

        for filename in files_to_delete:
            file_path = os.path.join(rfc_dir, filename)

            if os.path.exists(file_path):
                try:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    result['cleaned_count'] += 1
                    result['freed_space'] += file_size
                    print(f"✅ 已删除 {rfc_id}/{filename}（{file_size / 1024:.1f} KB）")
                except Exception as e:
                    result['errors'].append(f"删除 {file_path} 失败：{str(e)}")
                    print(f"❌ 删除 {file_path} 失败：{str(e)}")

    return result
```

### 步骤4：记录滚动操作

在审计日志中记录滚动操作，便于追踪和恢复：

```python
def record_log_rotation(archive_result: dict, cleanup_result: dict) -> bool:
    """
    记录日志滚动操作到审计日志

    参数：
        archive_result: 归档结果
        cleanup_result: 清理结果

    返回：
        True 表示记录成功，False 表示失败
    """
    try:
        rotation_log = {
            "timestamp": datetime.now().isoformat(),
            "operation": "log_rotation",
            "archive": {
                "archived_count": archive_result.get('archived_count', 0),
                "total_size": archive_result.get('total_size', 0),
                "archive_files": archive_result.get('archive_files', []),
                "errors": archive_result.get('errors', [])
            },
            "cleanup": {
                "cleaned_count": cleanup_result.get('cleaned_count', 0),
                "freed_space": cleanup_result.get('freed_space', 0),
                "errors": cleanup_result.get('errors', [])
            },
            "summary": {
                "total_archived": archive_result.get('archived_count', 0),
                "total_freed_kb": cleanup_result.get('freed_space', 0) / 1024,
                "status": "success" if not archive_result.get('errors') and not cleanup_result.get('errors') else "partial"
            }
        }

        # 写入滚动日志
        rotation_log_file = os.path.join(ARCHIVE_DIR, "rotation-log.json")

        # 读取现有日志（如果存在）
        rotation_logs = []
        if os.path.exists(rotation_log_file):
            with open(rotation_log_file, 'r', encoding='utf-8') as f:
                rotation_logs = json.load(f)

        # 追加新记录
        rotation_logs.append(rotation_log)

        # 保留最近 10 条记录
        rotation_logs = rotation_logs[-10:]

        # 写入文件
        with open(rotation_log_file, 'w', encoding='utf-8') as f:
            json.dump(rotation_logs, f, ensure_ascii=False, indent=2)

        print(f"✅ 滚动操作已记录到 {rotation_log_file}")
        return True

    except Exception as e:
        print(f"❌ 记录滚动操作失败：{str(e)}")
        return False
```

### 步骤5：执行日志滚动

在 list 命令中集成日志滚动逻辑：

```python
def list_rfcs_with_rotation(status_filter=None, limit=None, grouped=False, cleanup=False):
    """
    列出 RFC 并执行日志滚动

    参数：
        status_filter: 状态过滤
        limit: 显示数量限制
        grouped: 是否按状态分组
        cleanup: 是否执行清理（默认自动判断）
    """
    # 步骤1：扫描 RFC 目录
    rfcs = scan_rfcs()

    # 步骤2：检查是否需要滚动
    should_rotate = should_trigger_log_rotation(len(rfcs))

    if should_rotate or cleanup:
        print("\n🔄 执行日志滚动...\n")

        # 识别最近 3 个 RFC 和旧 RFC
        recent_rfcs, old_rfcs = identify_recent_rfcs(rfcs, keep_count=3)

        if old_rfcs:
            print(f"📦 发现 {len(old_rfcs)} 个旧 RFC，开始归档...\n")

            # 归档旧日志
            archive_result = archive_old_logs(old_rfcs)

            # 清理原始文件
            cleanup_result = cleanup_archived_logs(old_rfcs, archive_result)

            # 记录操作
            record_log_rotation(archive_result, cleanup_result)

            # 显示统计信息
            print(f"\n📊 滚动统计：")
            print(f"  - 已归档：{archive_result.get('archived_count', 0)} 个 RFC")
            print(f"  - 已清理：{cleanup_result.get('cleaned_count', 0)} 个文件")
            print(f"  - 释放空间：{cleanup_result.get('freed_space', 0) / 1024 / 1024:.1f} MB")
            print(f"  - 保留 RFC：{len(recent_rfcs)} 个（最近的）\n")
        else:
            print("✅ 无需滚动（RFC 数量 ≤ 3）\n")

    # 步骤3：过滤和排序
    rfcs = filter_and_sort_rfcs(rfcs, status_filter, limit)

    # 步骤4：格式化输出
    if grouped:
        format_rfc_list_grouped(rfcs)
    else:
        format_rfc_list(rfcs)

    # 步骤5：显示快速恢复提示
    show_resume_hints(rfcs)
```

### 步骤6：提供滚动管理命令

```python
def manage_log_rotation(action: str, rfc_id: str = None) -> bool:
    """
    管理日志滚动

    参数：
        action: 操作类型（cleanup | restore | list）
        rfc_id: RFC ID（可选）

    返回：
        True 表示操作成功，False 表示失败
    """
    if action == "cleanup":
        # 手动触发清理
        print("🔄 执行日志滚动清理...\n")
        rfcs = scan_rfcs()
        recent_rfcs, old_rfcs = identify_recent_rfcs(rfcs, keep_count=3)

        if old_rfcs:
            archive_result = archive_old_logs(old_rfcs)
            cleanup_result = cleanup_archived_logs(old_rfcs, archive_result)
            record_log_rotation(archive_result, cleanup_result)
            return True
        else:
            print("✅ 无需清理（RFC 数量 ≤ 3）")
            return True

    elif action == "restore":
        # 从归档恢复
        if not rfc_id:
            print("❌ 需要指定 RFC ID")
            return False

        print(f"🔄 从归档恢复 {rfc_id}...\n")

        # 查找最新的归档文件
        archive_files = sorted([
            f for f in os.listdir(ARCHIVE_DIR)
            if f.startswith(rfc_id) and f.endswith('.tar.gz')
        ], reverse=True)

        if not archive_files:
            print(f"❌ 未找到 {rfc_id} 的归档文件")
            return False

        archive_file = archive_files[0]
        archive_path = os.path.join(ARCHIVE_DIR, archive_file)
        rfc_dir = os.path.join(RFC_BASE_DIR, rfc_id)

        try:
            # 解压归档
            with tarfile.open(archive_path, "r:gz") as tar:
                tar.extractall(path=RFC_BASE_DIR)

            print(f"✅ 已从 {archive_file} 恢复 {rfc_id}")
            return True
        except Exception as e:
            print(f"❌ 恢复失败：{str(e)}")
            return False

    elif action == "list":
        # 列出所有归档
        print("\n📋 日志归档列表\n")
        print("=" * 100)

        archive_files = sorted([
            f for f in os.listdir(ARCHIVE_DIR)
            if f.endswith('.tar.gz')
        ], reverse=True)

        if not archive_files:
            print("未找到任何归档文件")
            return True

        for archive_file in archive_files:
            archive_path = os.path.join(ARCHIVE_DIR, archive_file)
            file_size = os.path.getsize(archive_path)
            mod_time = datetime.fromtimestamp(os.path.getmtime(archive_path))

            print(f"{archive_file}")
            print(f"  大小：{file_size / 1024:.1f} KB")
            print(f"  修改时间：{mod_time.isoformat()}")
            print()

        print("=" * 100)
        return True

    return False
```

### 使用示例

```bash
# 自动检测并执行滚动
/ohspec:list

# 手动触发清理
/ohspec:list --cleanup

# 列出所有归档
/ohspec:list --archive-list

# 从归档恢复指定 RFC
/ohspec:list --restore RFC-20240101-100000
```

### 与检查点机制的集成（P2-7）

日志滚动窗口与检查点机制的关系：

| 机制 | 触发条件 | 保留内容 | 用途 |
|------|---------|---------|------|
| 检查点 | 阶段完成/Token 70%/用户请求 | L0+L1 上下文快照 | 断点恢复 |
| 日志滚动 | RFC 数量 > 3/Token 50%/手动触发 | progress.json + findings.json | 日志管理 |

**关键区别**：
- 检查点保留在 `checkpoints/` 目录，用于恢复上下文
- 日志滚动归档到 `workflows/archive/`，用于释放存储空间
- 检查点 TTL 为 24 小时，归档文件永久保留

**集成策略**：
1. 当 Token 使用达到 50% 时，自动触发日志滚动
2. 当 Token 使用达到 70% 时，创建检查点并触发日志滚动
3. 日志滚动不影响检查点的创建和恢复

## 下一步
- 使用 `/ohspec:resume RFC-ID` 恢复未完成的 RFC
- 使用 `/ohspec:start` 创建新的 RFC
- 使用 `/ohspec:list --cleanup` 手动触发日志滚动
