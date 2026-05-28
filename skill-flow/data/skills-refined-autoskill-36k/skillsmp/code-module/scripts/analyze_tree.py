#!/usr/bin/env python3
"""
Module tree analyzer for code-module skill.

Generates directory tree structure and identifies leaf directories
for module analysis.
"""

import os
from pathlib import Path
from typing import List, Dict, Tuple, Set


# Common directories to ignore
IGNORED_DIRS = {
    'node_modules',
    '.git',
    '__pycache__',
    '.venv',
    'venv',
    'env',
    'dist',
    'build',
    '.next',
    '.nuxt',
    'target',
    'bin',
    'obj',
    '.pytest_cache',
    'coverage',
    '.mypy_cache',
}

# Code file extensions to consider
CODE_EXTENSIONS = {
    '.py', '.js', '.ts', '.tsx', '.jsx',
    '.java', '.go', '.rs', '.cpp', '.c', '.cs',
    '.rb', '.php', '.swift', '.kt', '.scala',
    '.sh', '.bash', '.zsh',
}


def is_ignored_dir(path: Path) -> bool:
    """Check if directory should be ignored."""
    return any(part in IGNORED_DIRS for part in path.parts)


def find_all_directories(root: Path) -> List[Path]:
    """Find all non-ignored directories recursively."""
    directories = []

    for dirpath, dirnames, filenames in os.walk(root):
        dir_path = Path(dirpath)

        # Skip if any parent directory is ignored
        if is_ignored_dir(dir_path):
            continue

        # Filter out ignored subdirectories
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]

        # Add this directory
        directories.append(dir_path)

    return sorted(directories)


def is_leaf_directory(dir_path: Path, all_dirs: List[Path]) -> bool:
    """Check if a directory has no subdirectories."""
    for other_dir in all_dirs:
        if other_dir.parent == dir_path and other_dir != dir_path:
            return False
    return True


def get_leaf_directories(directories: List[Path]) -> List[Path]:
    """Get all leaf directories (directories with no subdirectories)."""
    return [d for d in directories if is_leaf_directory(d, directories)]


def build_tree_string(directories: List[Path], root: Path) -> str:
    """Build a markdown-formatted tree string."""
    # Build tree structure
    tree = {}
    for dir_path in directories:
        relative = dir_path.relative_to(root)
        current = tree
        for part in relative.parts:
            if part not in current:
                current[part] = {}
            current = current[part]

    # Convert to markdown tree
    lines = []

    def add_to_tree(structure: Dict, prefix: str = "", is_top_level: bool = False):
        items = list(structure.items())
        for i, (name, children) in enumerate(items):
            is_item_last = (i == len(items) - 1)

            if is_top_level:
                # Top-level items: no prefix
                lines.append(name)
            else:
                # Nested items: use connector
                connector = "└── " if is_item_last else "├── "
                lines.append(f"{prefix}{connector}{name}")

            # Update prefix for children
            if children:
                child_prefix = prefix + ("    " if is_item_last else "│   ")
                add_to_tree(children, child_prefix, is_top_level=False)

    add_to_tree(tree, is_top_level=True)

    return "\n".join(lines)


def get_code_files(dir_path: Path) -> List[Path]:
    """Get all code files in a directory."""
    code_files = []
    if not dir_path.exists():
        return code_files

    for file_path in dir_path.iterdir():
        if file_path.is_file() and file_path.suffix in CODE_EXTENSIONS:
            code_files.append(file_path)

    return sorted(code_files)


def print_analysis(root: Path | None = None):
    """Print directory tree analysis."""
    if root is None:
        root = Path.cwd()

    print(f"Analyzing: {root}")
    print()

    # Find all directories
    directories = find_all_directories(root)
    print(f"Found {len(directories)} directories")

    # Find leaf directories
    leaf_dirs = get_leaf_directories(directories)
    print(f"Found {len(leaf_dirs)} leaf directories")
    print()

    # Build and print tree
    print("Directory Tree:")
    print("-" * 50)
    tree_str = build_tree_string(directories, root)
    print(tree_str)
    print()

    # Print leaf directories with code files
    print("Leaf Directories (for bottom-up analysis):")
    print("-" * 50)
    for leaf_dir in leaf_dirs:
        relative = leaf_dir.relative_to(root)
        code_files = get_code_files(leaf_dir)
        code_file_names = [f.name for f in code_files]
        code_str = ", ".join(code_file_names) if code_file_names else "No code files"
        print(f"  {relative}/ - {code_str}")


# ============================================================================
# Incremental Modules Generation Functions
# ============================================================================

def get_full_path(dir_path: Path, root: Path) -> str:
    """
    获取相对于根目录的完整路径字符串。

    Args:
        dir_path: 目录路径
        root: 项目根目录

    Returns:
        完整路径字符串（如：myproject/src/api/auth/）
    """
    relative = dir_path.relative_to(root)
    if relative == Path('.'):
        return f"{root.name}/"
    # 使用 as_posix() 确保使用正斜杠，跨平台兼容
    return f"{root.name}/{relative.as_posix()}/"


def update_progress_header(root: Path, processing_dir: str):
    """
    更新 modules.md 中的进度头信息。

    Args:
        root: 项目根目录
        processing_dir: 当前正在处理的目录
    """
    from datetime import datetime

    modules_md_path = root / "modules.md"
    if not modules_md_path.exists():
        return

    # 读取文件
    content = modules_md_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    # 生成新的进度头
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_header = f"<!-- Last Update: {timestamp} | Processing: {processing_dir} -->"

    # 查找并替换进度头
    updated_lines = []
    for line in lines:
        if line.strip().startswith("<!-- Last Update:"):
            updated_lines.append(new_header)
        else:
            updated_lines.append(line)

    # 如果没有找到进度头，在文件末尾添加
    if not any("<!-- Last Update:" in line for line in updated_lines):
        updated_lines.append("")
        updated_lines.append(new_header)

    modules_md_path.write_text('\n'.join(updated_lines), encoding='utf-8')


def remove_progress_header(root: Path):
    """
    移除 modules.md 中的进度头信息。

    Args:
        root: 项目根目录
    """
    modules_md_path = root / "modules.md"
    if not modules_md_path.exists():
        return

    # 读取文件
    content = modules_md_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    # 移除进度头行
    updated_lines = [line for line in lines if not line.strip().startswith("<!-- Last Update:")]

    # 移除末尾多余的空行
    while updated_lines and updated_lines[-1].strip() == "":
        updated_lines.pop()

    modules_md_path.write_text('\n'.join(updated_lines), encoding='utf-8')


def batch_update_descriptions(root: Path, updates: List[Tuple[Path, str]]):
    """
    批量更新 modules.md 中的多个描述。

    Args:
        root: 项目根目录
        updates: [(目录路径, 新描述), ...] 列表
    """
    modules_md_path = root / "modules.md"
    if not modules_md_path.exists():
        raise FileNotFoundError("modules.md not found")

    # 读取文件
    content = modules_md_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    # 构建查找字典：完整路径 -> 新描述
    update_map = {}
    for dir_path, new_desc in updates:
        full_path = get_full_path(dir_path, root)
        update_map[full_path] = new_desc

    # 更新匹配的行
    updated_lines = []
    for line in lines:
        updated = False
        for full_path, new_desc in update_map.items():
            # 匹配格式：完整路径 - 描述
            if line.startswith(full_path + " - "):
                updated_lines.append(f"{full_path} - {new_desc}")
                updated = True
                break

        if not updated:
            updated_lines.append(line)

    # 写回文件
    modules_md_path.write_text('\n'.join(updated_lines), encoding='utf-8')


def get_directories_by_depth(directories: List[Path], root: Path) -> Dict[int, List[Path]]:
    """
    按层级分组目录。

    Args:
        directories: 所有目录路径列表
        root: 项目根目录

    Returns:
        字典 {深度: [目录列表]}
    """
    depth_map: Dict[int, List[Path]] = {}

    for dir_path in directories:
        relative = dir_path.relative_to(root)
        depth = len(relative.parts) if relative != Path('.') else 0
        if depth not in depth_map:
            depth_map[depth] = []
        depth_map[depth].append(dir_path)

    return depth_map


def generate_initial_skeleton(root: Path) -> str:
    """
    生成初始 modules.md 骨架（包含树结构和占位描述）。

    Args:
        root: 项目根目录

    Returns:
        完整的 markdown 内容
    """
    from datetime import datetime

    # 查找所有目录
    directories = find_all_directories(root)

    # 1. 标题
    lines = ["# Modules", ""]

    # 2. 目录树（树形结构）
    lines.append("## Directory Structure")
    lines.append("")
    tree_str = build_tree_string(directories, root)
    lines.append(tree_str)
    lines.append("")

    # 3. 模块描述（完整路径 + 占位符）
    lines.append("## Module Descriptions")
    lines.append("")
    for dir_path in sorted(directories):
        full_path = get_full_path(dir_path, root)
        lines.append(f"{full_path} - [待分析]")
    lines.append("")

    # 4. 进度头（在最后，方便移除）
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"<!-- Last Update: {timestamp} | Processing: Initializing -->")

    return '\n'.join(lines)


def create_skeleton_file(root: Path):
    """
    创建初始 modules.md 文件。

    Args:
        root: 项目根目录
    """
    skeleton = generate_initial_skeleton(root)
    modules_md_path = root / "modules.md"
    modules_md_path.write_text(skeleton, encoding='utf-8')
    print(f"Created: {modules_md_path}")
    print(f"  Found {len(find_all_directories(root))} directories")


def analyze_by_path(dir_path: Path, root: Path) -> str:
    """
    基于完整路径的启发式规则推断目录功能。

    Args:
        dir_path: 目录路径
        root: 项目根目录

    Returns:
        功能描述字符串，如果无法推断则返回 None
    """
    # 确保路径是绝对路径
    dir_path = dir_path.resolve()
    root = root.resolve()

    # 获取相对路径（如 platform/service/manage/hr/）
    try:
        relative = dir_path.relative_to(root)
    except ValueError:
        # dir_path 不是 root 的子路径，使用目录名
        path_parts = [dir_path.name]
    else:
        path_parts = list(relative.parts)

    path_str = '/'.join(path_parts).lower()

    dir_name = dir_path.name.lower()

    # =============== 第一层：顶级目录 ===============
    if len(path_parts) == 1:
        if dir_name in ['api', 'apis']:
            return 'API接口定义层'
        elif dir_name in ['service', 'services']:
            return '业务服务层'
        elif dir_name in ['platform', 'core']:
            return '平台核心模块'
        elif any(k in dir_name for k in ['common', 'shared', 'util']):
            return '公共工具与组件'
        elif dir_name in ['config', 'conf', 'settings']:
            return '系统配置管理'
        elif dir_name in ['test', 'tests']:
            return '测试用例'
        elif dir_name in ['doc', 'docs', 'docs']:
            return '文档目录'
        elif dir_name in ['run', 'dist', 'build', 'bin']:
            return '运行时目录'
        elif dir_name in ['tmp', 'temp', 'cache']:
            return '临时文件目录'
        elif dir_name in ['vendor', 'third_party']:
            return '第三方依赖'
        elif dir_name in ['scripts', 'script']:
            return '脚本与工具'
        elif dir_name in ['modules', 'mod']:
            return '功能模块集'
        elif dir_name in ['assets']:
            return '静态资源目录'
        elif dir_name in ['references', 'ref', 'refs']:
            return '参考资源目录'
        elif dir_name in ['lib', 'libs']:
            return '依赖库目录'
        elif dir_name in ['include', 'includes']:
            return '头文件目录'
        elif dir_name in ['src', 'source']:
            return '源代码目录'

    # =============== 第二层及更深层：路径模式匹配 ===============

    # API 相关
    if any(p in path_parts for p in ['api', 'apis', 'rpc']):
        if 'plat' in path_parts:
            return '平台API接口'
        elif 'agent' in path_parts:
            return 'Agent API接口'
        else:
            return 'RESTful API接口'

    # 服务层
    if 'service' in path_parts:
        if 'manage' in path_parts:
            return '管理服务'
        elif 'dashboard' in path_parts:
            return '仪表盘服务'
        elif 'agent' in path_parts:
            return 'Agent服务'
        elif 'public' in path_parts:
            return '公共服务'
        else:
            return '业务服务'

    # 业务模块
    if 'hr' in path_parts:
        return '人力资源管理模块'
    elif 'enterprise' in path_parts:
        return '企业管理模块'
    elif 'pay' in path_parts:
        return '支付服务模块'
    elif 'mail' in path_parts:
        return '邮件服务模块'
    elif 'sms' in path_parts:
            return '短信服务模块'
    elif 'video' in path_parts:
        return '视频处理模块'
    elif 'file' in path_parts:
        return '文件管理模块'
    elif 'user' in path_parts:
        return '用户管理模块'
    elif 'auth' in path_parts:
        return '认证授权模块'
    elif 'ai' in path_parts:
        return 'AI服务模块'
    elif 'search' in path_parts:
        return '搜索服务模块'
    elif 'recruitment' in path_parts:
        return '招聘管理模块'
    elif 'resume' in path_parts:
        return '简历管理模块'
    elif 'course' in path_parts:
        return '课程管理模块'
    elif 'tex' in path_parts:
        return '考试测评模块'
    elif 'workorder' in path_parts:
        return '工单管理模块'
    elif 'notice' in path_parts:
        return '消息通知模块'
    elif 'invoice' in path_parts:
        return '发票管理模块'
    elif 'contract' in path_parts:
        return '合同管理模块'
    elif 'order' in path_parts:
        return '订单管理模块'
    elif 'product' in path_parts:
        return '产品管理模块'
    elif 'resource' in path_parts:
        return '资源管理模块'
    elif 'cluster' in path_parts:
        return '集群管理模块'
    elif 'container' in path_parts:
        return '容器管理模块'
    elif 'gpu' in path_parts:
        return 'GPU资源模块'
    elif 'hardware' in path_parts:
        return '硬件管理模块'
    elif 'network' in path_parts:
        return '网络管理模块'
    elif 'log' in path_parts or 'logger' in path_parts:
        return '日志管理模块'
    elif 'cache' in path_parts or 'redis' in path_parts:
        return '缓存服务模块'
    elif 'db' in path_parts or 'database' in path_parts:
        return '数据库模块'
    elif 'mq' in path_parts or 'queue' in path_parts:
        return '消息队列模块'
    elif 'event' in path_parts:
        return '事件处理模块'
    elif 'driver' in path_parts:
        return '驱动适配层'
    elif 'adapter' in path_parts:
        return '适配器层'
    elif 'middleware' in path_parts:
        return '中间件层'
    elif 'controller' in path_parts or 'handler' in path_parts:
        return '控制器层'
    elif 'model' in path_parts or 'entity' in path_parts:
        return '数据模型层'
    elif 'common' in path_parts or 'util' in path_parts:
        return '通用工具模块'
    elif 'security' in path_parts:
        return '安全防护模块'
    elif 'test' in path_parts:
        return '测试模块'

    # =============== 目录名本身的关键词匹配 ===============
    if any(k in dir_name for k in ['api', 'service', 'controller', 'model', 'handler', 'adapter', 'driver', 'middleware', 'auth', 'config', 'util', 'common']):
        if 'api' in dir_name:
            return 'API接口'
        elif 'service' in dir_name:
            return '业务服务'
        elif 'controller' in dir_name or 'handler' in dir_name:
            return '控制器'
        elif 'model' in dir_name:
            return '数据模型'
        elif 'adapter' in dir_name:
            return '适配器'
        elif 'driver' in dir_name:
            return '驱动器'
        elif 'middleware' in dir_name:
            return '中间件'
        elif 'auth' in dir_name:
            return '认证授权'
        elif 'config' in dir_name:
            return '配置管理'
        elif 'util' in dir_name or 'common' in dir_name:
            return '工具函数'

    # =============== 第三层：子目录名称模式 ===============
    if dir_name.startswith('api_') or dir_name.endswith('_api'):
        return 'API接口'
    elif dir_name.startswith('service_') or dir_name.endswith('_service'):
        return '业务服务'
    elif dir_name.startswith('controller') or dir_name.endswith('_controller'):
        return '控制器'
    elif dir_name.startswith('model') or dir_name.endswith('_model'):
        return '数据模型'
    elif dir_name.startswith('handler') or dir_name.endswith('_handler'):
        return '请求处理器'
    elif dir_name.startswith('adapter') or dir_name.endswith('_adapter'):
        return '适配器'
    elif dir_name.startswith('driver') or dir_name.endswith('_driver'):
        return '驱动器'

    # =============== 常见目录名 ===============
    if dir_name in ['conf', 'config', 'configs']:
        return '配置文件目录'
    elif dir_name in ['certs', 'certificates']:
        return '证书文件目录'
    elif dir_name in ['example', 'examples', 'demo']:
        return '示例代码'
    elif dir_name in ['test', 'tests', 'spec']:
        return '测试用例'
    elif dir_name in ['doc', 'docs', 'readme']:
        return '文档目录'
    elif dir_name in ['log', 'logs']:
        return '日志目录'

    # 无法推断，返回特殊标记提示需要代码分析
    return "NEED_CODE_ANALYSIS"


def analyze_directory_code(dir_path: Path) -> str:
    """
    分析目录中的代码并生成功能描述（中文）。

    Args:
        dir_path: 目录路径

    Returns:
        功能描述（10~50 个中文字符）
    """
    # 先基于路径推断
    import os
    root = Path.cwd()
    desc = analyze_by_path(dir_path, root)

    # 如果返回特殊标记，说明需要代码分析
    if desc == "NEED_CODE_ANALYSIS":
        # 需要读取代码文件进行深入分析
        code_files = get_code_files(dir_path)

        if not code_files:
            return "配置文件或资源目录"

        # 读取代码文件
        all_content = ""
        file_names = [f.name for f in code_files]
        for code_file in code_files[:5]:  # 最多读取 5 个文件
            try:
                content = code_file.read_text(encoding='utf-8', errors='ignore')
                all_content += content + "\n"
            except Exception:
                continue

        if not all_content:
            return "无有效代码文件"

        content_lower = all_content.lower()
        dir_name = dir_path.name.lower()

        # 简化的关键词映射
        keywords_map = {
            'auth': '认证授权模块',
            'config': '配置管理',
            'util': '工具函数',
            'api': 'API接口',
            'model': '数据模型',
            'service': '业务服务',
            'test': '测试用例',
            'controller': '控制器',
            'middleware': '中间件',
            'client': '客户端',
            'server': '服务器',
            'cache': '缓存',
            'log': '日志',
            'security': '安全模块',
            'event': '事件处理',
            'task': '任务调度',
            'socket': '通信模块',
            'storage': '存储模块',
            'driver': '驱动器',
            'adapter': '适配器',
        }

        # 1. 基于目录名匹配
        for key, desc_str in keywords_map.items():
            if key in dir_name:
                return desc_str

        # 2. 基于文件名匹配
        for file_name in file_names:
            file_lower = file_name.lower()
            for key, desc_str in keywords_map.items():
                if key in file_lower:
                    return desc_str

        # 3. 基于代码内容匹配
        for key, desc_str in keywords_map.items():
            if key in content_lower:
                return desc_str

        # 4. 默认：使用目录名生成描述
        dir_display = dir_path.name
        if len(dir_display) > 10:
            dir_display = dir_display[:10]
        return f'{dir_display}相关模块'

    # 返回路径推断结果
    return desc

    if not code_files:
        return "配置文件或资源目录"

    # 读取代码文件
    all_content = ""
    file_names = [f.name for f in code_files]
    for code_file in code_files[:5]:  # 最多读取 5 个文件
        try:
            content = code_file.read_text(encoding='utf-8', errors='ignore')
            all_content += content + "\n"
        except Exception:
            continue

    if not all_content:
        return "无有效代码文件"

    content_lower = all_content.lower()
    dir_name = dir_path.name.lower()

    # Fallback：基于目录名和内容的简单匹配
    # 仅当路径无法推断时才使用

    # 简化的关键词映射
    keywords_map = {
        'auth': '认证授权模块',
        'config': '配置管理',
        'util': '工具函数',
        'api': 'API接口',
        'model': '数据模型',
        'service': '业务服务',
        'test': '测试用例',
        'controller': '控制器',
        'middleware': '中间件',
        'client': '客户端',
        'server': '服务器',
        'cache': '缓存',
        'log': '日志',
        'security': '安全模块',
        'event': '事件处理',
        'task': '任务调度',
        'socket': '通信模块',
        'storage': '存储模块',
        'driver': '驱动器',
        'adapter': '适配器',
    }

    # 1. 基于目录名匹配
    for key, desc in keywords_map.items():
        if key in dir_name:
            return desc

    # 2. 基于文件名匹配
    for file_name in file_names:
        file_lower = file_name.lower()
        for key, desc in keywords_map.items():
            if key in file_lower:
                return desc

    # 3. 默认：使用目录名生成描述
    dir_display = dir_path.name
    if len(dir_display) > 10:
        dir_display = dir_display[:10]
    return f'{dir_display}相关模块'

def propagate_summary(dir_path: Path, child_summaries: List[str], root: Path) -> str:
    """
    合并子目录摘要生成父目录摘要（中文）。

    Args:
        dir_path: 父目录路径
        child_summaries: 子目录的摘要列表
        root: 项目根目录

    Returns:
        合并后的摘要（10~50 个中文字符）
    """
    if not child_summaries:
        return analyze_directory_code(dir_path)

    dir_name = dir_path.name

    # 特殊处理常见目录名
    if dir_name in ['src', 'lib', 'core', 'source']:
        return '核心源代码与业务逻辑层'
    elif dir_name in ['test', 'tests', '__tests__', 'spec']:
        return '单元测试与集成测试套件'
    elif dir_name in ['api', 'apis', 'routes']:
        return 'RESTful API 接口与路由层'
    elif dir_name in ['components', 'ui', 'views', 'pages']:
        return '前端组件与视图页面'
    elif dir_name in ['hooks', 'composables']:
        return 'React Hooks 与组合式函数'
    elif dir_name in ['store', 'state', 'redux', 'vuex']:
        return '全局状态管理与数据存储'
    elif dir_name in ['styles', 'css', 'scss', 'less']:
        return '样式表与主题配置文件'
    elif dir_name in ['assets', 'static', 'public']:
        return '静态资源与公共文件目录'
    elif dir_name in ['vendor', 'node_modules', 'third_party']:
        return '第三方库与依赖包文件'
    elif dir_name in ['config', 'settings', 'env']:
        return '系统配置与环境变量管理'
    elif dir_name in ['utils', 'helpers', 'commons']:
        return '通用工具函数与辅助类库'
    elif dir_name in ['services', 'business']:
        return '业务逻辑处理与服务层'
    elif dir_name in ['models', 'entities', 'schemas']:
        return '数据模型与实体定义层'
    elif dir_name in ['controllers', 'handlers']:
        return '控制器与请求处理层'
    elif dir_name in ['middleware', 'interceptors']:
        return '中间件与请求拦截处理'
    elif dir_name in ['client', 'http', 'request']:
        return 'HTTP 客户端与请求封装'
    elif dir_name in ['server', 'app', 'main']:
        return '应用启动与服务器配置'
    elif dir_name in ['database', 'db', 'repositories']:
        return '数据库访问与持久化操作'
    elif dir_name in ['cache', 'redis', 'session']:
        return '缓存与会话管理模块'
    elif dir_name in ['logs', 'logging', 'monitor']:
        return '日志记录与监控追踪系统'
    elif dir_name in ['exceptions', 'errors', 'handlers']:
        return '异常捕获与错误处理模块'
    elif dir_name in ['events', 'listeners', 'observers']:
        return '事件驱动与消息发布订阅'
    elif dir_name in ['tasks', 'jobs', 'queues', 'workers']:
        return '异步任务与定时调度系统'
    elif dir_name in ['socket', 'websocket', 'ws', 'io']:
        return 'WebSocket 与实时通信模块'
    elif dir_name in ['storage', 'files', 'uploads']:
        return '文件存储与上传下载管理'
    elif dir_name in ['security', 'auth', 'permission']:
        return '加密解密与安全防护模块'
    elif dir_name in ['locale', 'i18n', 'translations']:
        return '国际化与多语言支持模块'
    elif dir_name in ['platform', 'core', 'kernel']:
        return '平台核心与基础架构模块'
    elif dir_name in ['cluster', 'distributed']:
        return '集群管理与分布式协调'
    elif dir_name in ['communication', 'comm', 'interfaces']:
        return '平台通信与共享接口定义'
    elif dir_name in ['plugins', 'extensions', 'addons']:
        return '插件扩展与模块化加载'
    elif dir_name in ['documentation', 'docs', 'readme']:
        return '项目文档与使用说明'
    
    # 分析子摘要的共同特征
    unique_summaries = list(set(child_summaries))

    # 特殊处理根目录或顶层目录
    if dir_path == root or dir_path.name == root.name:
        # 根目录或顶层目录，基于子目录描述和目录名生成更准确的描述
        if len(unique_summaries) == 1:
            # 如果子目录描述是通用的"配置文件或资源目录"，基于目录名生成更好的描述
            if unique_summaries[0] == '配置文件或资源目录':
                # 基于目录名生成描述
                dir_display = dir_name
                if len(dir_display) > 10:
                    dir_display = dir_display[:10]
                return f'{dir_display}项目模块'
        return unique_summaries[0] if len(unique_summaries) == 1 else f'{dir_name}相关模块'

    if len(unique_summaries) == 1:
        # 所有子目录相同，但不直接返回，而是基于目录名生成描述
        summary = unique_summaries[0]
        # 确保长度合适
        if len(summary) > 50:
            summary = summary[:50]
        return summary
    
    # 提取关键主题词
    themes = []
    for summary in unique_summaries:
        # 简单提取第一个名词性短语
        words = summary.split()
        if len(words) > 1:
            # 取前两个词作为主题
            theme = ''.join(words[:2])
            if len(theme) >= 4:
                themes.append(theme)
    
    if len(themes) >= 2:
        # 合并两个主要主题
        combined = themes[0] + '与' + themes[1]
        if len(combined) <= 50:
            return combined
    
    # 默认：基于目录名生成描述
    dir_display = dir_name
    if len(dir_display) > 15:
        dir_display = dir_display[:15]
    
    # 尝试从目录名推断功能
    if 'config' in dir_name:
        return f'{dir_display}配置管理模块'
    elif 'test' in dir_name:
        return f'{dir_display}测试套件'
    elif 'api' in dir_name:
        return f'{dir_display}接口模块'
    else:
        return f'{dir_display}功能模块组'


def generate_modules_incremental(root: Path | None = None, batch_size: int = 5):
    """
    增量式生成 modules.md 文件（两阶段流程）。

    Args:
        root: 项目根目录（默认为当前目录）
        batch_size: 批量更新大小（默认 5 个）
    """
    if root is None:
        root = Path.cwd()

    print(f"Generating modules.md for: {root}")
    print()

    # 阶段 1：生成骨架
    print("=" * 60)
    print("Phase 1: Creating skeleton...")
    print("=" * 60)
    create_skeleton_file(root)
    print()

    # 准备数据结构
    directories = find_all_directories(root)
    leaf_dirs = get_leaf_directories(directories)
    depth_map = get_directories_by_depth(directories, root)
    dir_summaries: Dict[Path, str] = {}

    print(f"Phase 1 completed. Found {len(directories)} directories, {len(leaf_dirs)} leaf dirs.")
    print()

    # 阶段 2：增量填充
    print("=" * 60)
    print("Phase 2: Incremental population...")
    print("=" * 60)
    print()

    # 2.1 分析叶子目录
    print(f"Analyzing {len(leaf_dirs)} leaf directories...")
    updates = []
    processed_count = 0

    for leaf_dir in leaf_dirs:
        # 分析代码
        summary = analyze_directory_code(leaf_dir)
        dir_summaries[leaf_dir] = summary
        updates.append((leaf_dir, summary))
        processed_count += 1

        # 批量更新
        if len(updates) >= batch_size:
            batch_update_descriptions(root, updates)
            update_progress_header(root, get_full_path(leaf_dir, root))
            print(f"  [{processed_count}/{len(leaf_dirs)}] Updated {len(updates)} leaf directories")
            updates.clear()

    # 更新剩余的叶子目录
    if updates:
        batch_update_descriptions(root, updates)
        print(f"  [{processed_count}/{len(leaf_dirs)}] Updated {len(updates)} leaf directories")
        updates.clear()

    print()

    # 2.2 分层向上传播
    print("Propagating summaries upward (by depth)...")
    max_depth = max(depth_map.keys()) if depth_map else 0

    for depth in range(max_depth - 1, -1, -1):
        if depth not in depth_map:
            continue

        print(f"  Depth {depth}: processing {len(depth_map[depth])} directories...")

        for dir_path in depth_map[depth]:
            if dir_path in leaf_dirs:
                continue  # 跳过叶子目录

            # 获取所有子目录的摘要
            child_dirs = [d for d in directories if d.parent == dir_path and d != dir_path]
            child_summaries = [dir_summaries.get(child, "") for child in child_dirs if child in dir_summaries]

            # 合并摘要
            summary = propagate_summary(dir_path, child_summaries, root)
            dir_summaries[dir_path] = summary
            updates.append((dir_path, summary))

            # 批量更新
            if len(updates) >= batch_size:
                batch_update_descriptions(root, updates)
                update_progress_header(root, get_full_path(dir_path, root))
                updates.clear()

        # 更新当前层级的剩余目录
        if updates:
            batch_update_descriptions(root, updates)
            updates.clear()

    print()

    # 完成
    print("=" * 60)
    print("Phase 2 completed!")
    print("=" * 60)
    print()

    # 移除进度头
    remove_progress_header(root)

    # ==================== 验证步骤：确保所有目录都有描述 ====================
    validate_and_fix_missing_descriptions(root)
    # ========================================================================

    print("\n[OK] Generated modules.md successfully!")
    print(f"  Total directories: {len(directories)}")
    print(f"  Leaf directories analyzed: {len(leaf_dirs)}")
    print(f"  Parent directories propagated: {len(directories) - len(leaf_dirs)}")

# ============================================================================
# Validation and Fix Functions
# ============================================================================

def validate_and_fix_missing_descriptions(root: Path):
    """
    验证并修复缺失的目录描述。

    Args:
        root: 项目根目录
    """
    modules_md_path = root / "modules.md"
    if not modules_md_path.exists():
        print("[ERROR] modules.md not found!")
        return

    print("=" * 60)
    print("Validating module descriptions...")
    print("=" * 60)

    # 1. 读取所有目录
    directories = find_all_directories(root)
    print(f"Found {len(directories)} directories in filesystem.")

    # 2. 解析现有的描述
    existing_descriptions = parse_existing_descriptions(root)
    print(f"Found {len(existing_descriptions)} descriptions in modules.md.")

    # 3. 找出缺失或无效的描述
    missing_or_invalid = []
    for dir_path in directories:
        full_path = get_full_path(dir_path, root)
        desc = existing_descriptions.get(full_path, '')

        # 检查：不存在、为空、或仍为占位符
        if not desc or desc == '[待分析]':
            missing_or_invalid.append(dir_path)

    if not missing_or_invalid:
        print("[OK] All directories have valid descriptions!")
        return

    # 4. 修复缺失的描述
    print(f"\nFound {len(missing_or_invalid)} directories without valid descriptions.")
    print("Fixing missing descriptions...\n")

    updates = []
    batch_size = 5

    for dir_path in missing_or_invalid:
        try:
            # 分析目录代码
            summary = analyze_directory_code(dir_path)
            updates.append((dir_path, summary))

            # 批量更新
            if len(updates) >= batch_size:
                batch_update_descriptions(root, updates)
                print(f"  Fixed {len(updates)} missing descriptions")
                updates.clear()

        except Exception as e:
            print(f"  [WARNING] Failed to analyze {dir_path}: {e}")
            # 添加默认描述
            dir_display = dir_path.name
            if len(dir_display) > 10:
                dir_display = dir_display[:10]
            updates.append((dir_path, f"{dir_display}相关功能模块"))

    # 更新剩余的
    if updates:
        batch_update_descriptions(root, updates)
        print(f"  Fixed {len(updates)} missing descriptions")

    print("\n[OK] Validation and fix completed!")


# ============================================================================
# Interactive Mode Functions
# ============================================================================

def backup_existing_modules(root: Path) -> Path | None:
    """
    备份现有的 modules.md 文件。
    """
    from datetime import datetime
    import shutil

    modules_md_path = root / 'modules.md'
    if not modules_md_path.exists():
        return None

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_path = root / f'modules_{timestamp}.md'
    shutil.copy2(modules_md_path, backup_path)
    print(f'Backed up: modules.md -> {backup_path.name}')
    return backup_path


def parse_existing_descriptions(root: Path) -> Dict[str, str]:
    """
    解析现有的 modules.md，提取已分析的目录描述。
    """
    modules_md_path = root / 'modules.md'
    if not modules_md_path.exists():
        return {}

    descriptions = {}
    in_descriptions_section = False

    with open(modules_md_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line == '## Module Descriptions':
                in_descriptions_section = True
                continue
            if in_descriptions_section and line.startswith('##'):
                break
            if in_descriptions_section and ' - ' in line and not line.startswith('<!--'):
                path, desc = line.split(' - ', 1)
                descriptions[path] = desc

    return descriptions


def get_unanalyzed_directories(directories, existing_descriptions, root):
    """
    获取未分析的目录（描述为 [待分析] 或不存在）。
    """
    unanalyzed = []
    for dir_path in directories:
        full_path = get_full_path(dir_path, root)
        desc = existing_descriptions.get(full_path, '')
        if not desc or desc == '[待分析]':
            unanalyzed.append(dir_path)
    return unanalyzed


def get_new_directories(directories, existing_descriptions, root):
    """
    获取新增的目录。
    """
    new_dirs = []
    for dir_path in directories:
        full_path = get_full_path(dir_path, root)
        if full_path not in existing_descriptions:
            new_dirs.append(dir_path)
    return new_dirs


def interactive_mode(root):
    """
    交互式模式：检测重复执行并询问用户选择。
    """
    modules_md_path = root / 'modules.md'

    if not modules_md_path.exists():
        generate_modules_incremental(root)
        return

    print('=' * 60)
    print('Existing modules.md detected!')
    print('=' * 60)
    print()
    print('Please choose an option:')
    print('  1. Full overwrite (backup existing, regenerate from scratch)')
    print('  2. Continue unanalyzed directories (skip [待分析] only)')
    print('  3. Check new directories only (not in existing list)')
    print()
    
    while True:
        try:
            choice = input('Your choice (1/2/3): ').strip()

            if choice == '1':
                print()
                print('Option 1: Full overwrite...')
                backup_existing_modules(root)
                modules_md_path.unlink()
                generate_modules_incremental(root)
                break

            elif choice == '2':
                print()
                print('Option 2: Continuing unanalyzed directories...')
                existing_descriptions = parse_existing_descriptions(root)
                directories = find_all_directories(root)
                unanalyzed = get_unanalyzed_directories(directories, existing_descriptions, root)
                
                if not unanalyzed:
                    print('No unanalyzed directories found. All directories are already analyzed!')
                    return

                print(f'Found {len(unanalyzed)} unanalyzed directories to process.')
                print()
                update_progress_header(root, 'Processing unanalyzed directories')
                process_incremental_update(root, unanalyzed, existing_descriptions)
                break

            elif choice == '3':
                print()
                print('Option 3: Checking new directories...')
                existing_descriptions = parse_existing_descriptions(root)
                directories = find_all_directories(root)
                new_dirs = get_new_directories(directories, existing_descriptions, root)
                
                if not new_dirs:
                    print('No new directories found. All directories are already in the list!')
                    return

                print(f'Found {len(new_dirs)} new directories to process.')
                print()
                update_progress_header(root, 'Processing new directories')
                process_incremental_update(root, new_dirs, existing_descriptions)
                break

            else:
                print('Invalid choice. Please enter 1, 2, or 3.')
        except KeyboardInterrupt:
            print()
            print('Operation cancelled.')
            return
        except EOFError:
            print()
            print('Non-interactive mode detected. Using option 1 (full overwrite)...')
            backup_existing_modules(root)
            modules_md_path.unlink()
            generate_modules_incremental(root)
            break


def process_incremental_update(root, target_dirs, existing_descriptions):
    """
    处理增量更新（用于选项 2 和 3）。
    """
    directories = find_all_directories(root)
    dir_summaries = {}
    batch_size = 5
    depth_map = get_directories_by_depth(directories, root)
    max_depth = max(depth_map.keys()) if depth_map else 0
    updates = []

    for depth in range(max_depth, -1, -1):
        if depth not in depth_map:
            continue
        for dir_path in depth_map[depth]:
            if dir_path not in target_dirs:
                continue
            leaf_dirs = get_leaf_directories(directories)
            if dir_path in leaf_dirs:
                summary = analyze_directory_code(dir_path)
            else:
                child_dirs = [d for d in directories if d.parent == dir_path and d != dir_path]
                child_summaries = []
                for child in child_dirs:
                    full_path = get_full_path(child, root)
                    if child in dir_summaries:
                        child_summaries.append(dir_summaries[child])
                    elif full_path in existing_descriptions:
                        child_summaries.append(existing_descriptions[full_path])
                summary = propagate_summary(dir_path, child_summaries, root)
            dir_summaries[dir_path] = summary
            updates.append((dir_path, summary))
            if len(updates) >= batch_size:
                batch_update_descriptions(root, updates)
                update_progress_header(root, get_full_path(dir_path, root))
                print(f'  Updated {len(updates)} directories')
                updates.clear()

    if updates:
        batch_update_descriptions(root, updates)
        print(f'  Updated {len(updates)} directories')

    remove_progress_header(root)
    print()
    print('[OK] Incremental update completed!')
    print(f'  Directories processed: {len(target_dirs)}')



def main():
    """Main entry point."""
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--generate":
            # 执行两阶段增量生成
            root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()
            interactive_mode(root)

        elif sys.argv[1] == "--validate":
            # 验证并修复缺失的描述
            root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()
            validate_and_fix_missing_descriptions(root)

        else:
            # 仅分析并打印（原有行为）
            root = Path(sys.argv[1])
            print_analysis(root)
    else:
        # 默认：仅分析
        root = Path.cwd()
        print_analysis(root)


if __name__ == "__main__":
    main()
