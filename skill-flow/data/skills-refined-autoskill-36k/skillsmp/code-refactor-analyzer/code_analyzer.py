#!/usr/bin/env python3
"""
代码分析引擎 - 分析仓库找到可能受需求影响的代码行

功能：
1. 分析用户需求，提取关键词
2. 搜索代码库找到相关代码
3. 识别需要修改的代码位置
4. 生成待办事项建议
"""

import os
import re
import ast
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
import subprocess


class CodeAnalyzer:
    """代码分析器"""

    def __init__(self, repo_path: str = "."):
        """
        初始化代码分析器

        Args:
            repo_path: 仓库路径，默认为当前目录
        """
        self.repo_path = Path(repo_path).resolve()
        self.supported_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.go', '.rs'}

    def extract_keywords(self, requirement: str) -> List[str]:
        """
        从需求中提取关键词

        Args:
            requirement: 用户需求描述

        Returns:
            关键词列表
        """
        # 移除标点符号和常见停用词
        stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}

        # 分割文本
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', requirement.lower())

        # 过滤停用词和短词
        keywords = [word for word in words if word not in stop_words and len(word) > 1]

        # 去重
        return list(set(keywords))

    def search_code_files(self, keywords: List[str], file_extensions: Optional[Set[str]] = None) -> List[Dict]:
        """
        搜索包含关键词的代码文件

        Args:
            keywords: 关键词列表
            file_extensions: 文件扩展名集合，如果为None则使用默认支持的语言

        Returns:
            匹配的文件列表
        """
        if not keywords:
            return []

        extensions = file_extensions or self.supported_extensions
        matched_files = []

        # 遍历仓库目录
        for root, dirs, files in os.walk(self.repo_path):
            # 跳过隐藏目录和特定目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {'node_modules', '__pycache__', 'venv', '.git'}]

            for file in files:
                file_path = Path(root) / file
                file_ext = file_path.suffix.lower()

                if file_ext in extensions:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()

                        # 检查是否包含关键词
                        matches = []
                        for keyword in keywords:
                            if keyword in content:
                                # 计算匹配次数
                                count = content.count(keyword)
                                matches.append({
                                    "keyword": keyword,
                                    "count": count
                                })

                        if matches:
                            # 获取文件相对路径
                            rel_path = file_path.relative_to(self.repo_path)
                            matched_files.append({
                                "file_path": str(rel_path),
                                "absolute_path": str(file_path),
                                "matches": matches,
                                "total_matches": sum(m["count"] for m in matches)
                            })
                    except (IOError, UnicodeDecodeError):
                        continue

        # 按匹配次数排序
        matched_files.sort(key=lambda x: x["total_matches"], reverse=True)
        return matched_files

    def analyze_python_file(self, file_path: Path, keywords: List[str]) -> List[Dict]:
        """
        分析Python文件，找到需要修改的代码位置

        Args:
            file_path: Python文件路径
            keywords: 关键词列表

        Returns:
            需要修改的代码位置列表
        """
        results = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析AST
            tree = ast.parse(content)

            # 遍历AST节点
            for node in ast.walk(tree):
                node_info = self._analyze_ast_node(node, keywords, content)
                if node_info:
                    results.append(node_info)

        except (SyntaxError, IOError, UnicodeDecodeError):
            pass

        return results

    def _analyze_ast_node(self, node: ast.AST, keywords: List[str], file_content: str) -> Optional[Dict]:
        """
        分析AST节点

        Args:
            node: AST节点
            keywords: 关键词列表
            file_content: 文件内容

        Returns:
            节点分析结果，如果不需要修改则返回None
        """
        # 获取节点类型和位置
        node_type = type(node).__name__
        lineno = getattr(node, 'lineno', None)

        if not lineno:
            return None

        # 获取节点对应的代码行
        lines = file_content.split('\n')
        if lineno - 1 < len(lines):
            code_line = lines[lineno - 1].strip()
        else:
            return None

        # 检查代码行是否包含关键词
        line_lower = code_line.lower()
        matched_keywords = [kw for kw in keywords if kw in line_lower]

        if not matched_keywords:
            return None

        # 根据节点类型确定修改建议
        suggestion = self._get_suggestion_for_node(node, node_type, matched_keywords)

        if not suggestion:
            return None

        # 确定优先级
        priority = self._determine_priority(node_type, matched_keywords)

        return {
            "line_number": lineno,
            "code_line": code_line,
            "node_type": node_type,
            "matched_keywords": matched_keywords,
            "priority": priority,
            "suggestion": suggestion
        }

    def _get_suggestion_for_node(self, node: ast.AST, node_type: str, keywords: List[str]) -> Optional[str]:
        """
        根据节点类型获取修改建议

        Args:
            node: AST节点
            node_type: 节点类型名称
            keywords: 匹配的关键词

        Returns:
            修改建议，如果不需要修改则返回None
        """
        suggestions = {
            "FunctionDef": "检查函数是否需要修改以支持新需求",
            "ClassDef": "检查类定义是否需要扩展或修改",
            "Call": "检查函数调用是否需要更新参数或返回值",
            "Assign": "检查变量赋值是否需要更新",
            "Import": "检查导入语句是否需要添加新模块",
            "ImportFrom": "检查从模块导入是否需要更新",
            "Attribute": "检查属性访问是否需要修改",
            "Name": "检查变量名或函数名是否需要更新",
            "Expr": "检查表达式是否需要修改",
            "Return": "检查返回语句是否需要更新",
            "If": "检查条件判断是否需要更新",
            "For": "检查循环是否需要更新",
            "While": "检查循环是否需要更新",
            "Try": "检查异常处理是否需要更新",
            "With": "检查上下文管理器是否需要更新"
        }

        base_suggestion = suggestions.get(node_type, "检查代码是否需要修改以支持新需求")

        # 根据关键词细化建议
        keyword_hints = {
            "auth": "认证相关",
            "user": "用户相关",
            "login": "登录功能",
            "register": "注册功能",
            "password": "密码处理",
            "token": "令牌处理",
            "api": "API接口",
            "database": "数据库操作",
            "query": "查询操作",
            "update": "更新操作",
            "delete": "删除操作",
            "create": "创建操作",
            "validate": "验证逻辑",
            "error": "错误处理",
            "test": "测试相关",
            "config": "配置相关"
        }

        hint = None
        for keyword in keywords:
            if keyword in keyword_hints:
                hint = keyword_hints[keyword]
                break

        if hint:
            return f"{base_suggestion}（{hint}）"
        else:
            return base_suggestion

    def _determine_priority(self, node_type: str, keywords: List[str]) -> str:
        """
        确定修改优先级

        Args:
            node_type: 节点类型
            keywords: 匹配的关键词

        Returns:
            优先级：high, medium, low
        """
        # 高优先级节点类型
        high_priority_types = {"FunctionDef", "ClassDef", "Call", "Import", "ImportFrom"}

        # 高优先级关键词
        high_priority_keywords = {"auth", "user", "login", "password", "token", "security"}

        if node_type in high_priority_types:
            return "high"

        for keyword in keywords:
            if keyword in high_priority_keywords:
                return "high"

        # 中优先级关键词
        medium_priority_keywords = {"api", "database", "query", "update", "validate"}

        for keyword in keywords:
            if keyword in medium_priority_keywords:
                return "medium"

        return "low"

    def analyze_requirement(self, requirement: str, max_files: int = 20) -> List[Dict]:
        """
        分析需求，找到需要修改的代码

        Args:
            requirement: 用户需求描述
            max_files: 最大分析文件数

        Returns:
            分析结果列表
        """
        # 提取关键词
        keywords = self.extract_keywords(requirement)
        if not keywords:
            return []

        # 搜索相关文件
        matched_files = self.search_code_files(keywords)
        if not matched_files:
            return []

        # 限制分析的文件数量
        files_to_analyze = matched_files[:max_files]
        all_results = []

        for file_info in files_to_analyze:
            file_path = Path(file_info["absolute_path"])
            file_ext = file_path.suffix.lower()

            if file_ext == '.py':
                # Python文件使用AST分析
                file_results = self.analyze_python_file(file_path, keywords)
            else:
                # 其他文件使用简单文本分析
                file_results = self.analyze_generic_file(file_path, keywords)

            # 为每个结果添加文件信息
            for result in file_results:
                result.update({
                    "file_path": file_info["file_path"],
                    "matched_keywords_in_file": file_info["matches"]
                })
                all_results.append(result)

        return all_results

    def analyze_generic_file(self, file_path: Path, keywords: List[str]) -> List[Dict]:
        """
        分析通用文本文件

        Args:
            file_path: 文件路径
            keywords: 关键词列表

        Returns:
            分析结果列表
        """
        results = []

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                line_text = line.strip()
                if not line_text:
                    continue

                line_lower = line_text.lower()
                matched_keywords = [kw for kw in keywords if kw in line_lower]

                if matched_keywords:
                    # 简单启发式：包含特定模式的代码行可能需要修改
                    patterns = {
                        r'function\s+\w+': "函数定义可能需要修改",
                        r'class\s+\w+': "类定义可能需要修改",
                        r'def\s+\w+': "函数定义可能需要修改",
                        r'import\s+': "导入语句可能需要更新",
                        r'export\s+': "导出语句可能需要更新",
                        r'const\s+\w+': "常量定义可能需要更新",
                        r'let\s+\w+': "变量定义可能需要更新",
                        r'var\s+\w+': "变量定义可能需要更新"
                    }

                    suggestion = "检查代码是否需要修改以支持新需求"
                    for pattern, pattern_suggestion in patterns.items():
                        if re.search(pattern, line_text, re.IGNORECASE):
                            suggestion = pattern_suggestion
                            break

                    # 确定优先级
                    priority = "medium"
                    high_priority_keywords = {"auth", "user", "login", "password", "token", "security"}
                    for keyword in matched_keywords:
                        if keyword in high_priority_keywords:
                            priority = "high"
                            break

                    results.append({
                        "line_number": line_num,
                        "code_line": line_text,
                        "node_type": "generic",
                        "matched_keywords": matched_keywords,
                        "priority": priority,
                        "suggestion": suggestion
                    })

        except (IOError, UnicodeDecodeError):
            pass

        return results

    def generate_analysis_summary(self, requirement: str, analysis_results: List[Dict]) -> Dict:
        """
        生成分析摘要

        Args:
            requirement: 用户需求描述
            analysis_results: 分析结果列表

        Returns:
            分析摘要字典
        """
        if not analysis_results:
            return {
                "requirement": requirement,
                "total_files": 0,
                "total_lines": 0,
                "priority_distribution": {"high": 0, "medium": 0, "low": 0},
                "file_types": {},
                "summary": "未找到需要修改的代码"
            }

        # 统计信息
        total_files = len(set(result["file_path"] for result in analysis_results))
        total_lines = len(analysis_results)

        # 优先级分布
        priority_distribution = {"high": 0, "medium": 0, "low": 0}
        for result in analysis_results:
            priority = result.get("priority", "medium")
            priority_distribution[priority] += 1

        # 文件类型分布
        file_types = {}
        for result in analysis_results:
            file_path = result["file_path"]
            file_ext = Path(file_path).suffix.lower()
            file_types[file_ext] = file_types.get(file_ext, 0) + 1

        # 生成摘要文本
        if total_lines == 0:
            summary = "未找到需要修改的代码"
        else:
            high_percent = (priority_distribution["high"] / total_lines * 100) if total_lines > 0 else 0
            summary = (
                f"找到 {total_lines} 处可能需要修改的代码，分布在 {total_files} 个文件中。"
                f"其中高优先级修改点占 {high_percent:.1f}%。"
            )

        return {
            "requirement": requirement,
            "total_files": total_files,
            "total_lines": total_lines,
            "priority_distribution": priority_distribution,
            "file_types": file_types,
            "summary": summary
        }


# 测试代码
if __name__ == "__main__":
    # 创建测试分析器
    analyzer = CodeAnalyzer()

    # 测试关键词提取
    test_req = "添加用户认证功能，包括登录和注册"
    keywords = analyzer.extract_keywords(test_req)
    print(f"需求: {test_req}")
    print(f"提取的关键词: {keywords}")

    # 测试代码文件搜索
    matched_files = analyzer.search_code_files(keywords)
    print(f"\n匹配的文件数量: {len(matched_files)}")
    if matched_files:
        print("前3个匹配文件:")
        for file_info in matched_files[:3]:
            print(f"  - {file_info['file_path']} (匹配次数: {file_info['total_matches']})")

    # 测试需求分析
    analysis_results = analyzer.analyze_requirement(test_req, max_files=5)
    print(f"\n分析结果数量: {len(analysis_results)}")
    if analysis_results:
        print("前3个分析结果:")
        for result in analysis_results[:3]:
            print(f"  - {result['file_path']}:{result['line_number']} - {result['code_line'][:50]}...")

    # 测试生成分析摘要
    summary = analyzer.generate_analysis_summary(test_req, analysis_results)
    print(f"\n分析摘要: {summary}")