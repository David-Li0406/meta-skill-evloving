#!/usr/bin/env python3
# 基础功能测试
import os
import sys
import json
import codecs

# 设置控制台编码为UTF-8（Windows兼容）
if sys.platform == 'win32':
    # Windows控制台编码设置
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入技能模块
from interface_analyzer import InterfaceAnalyzer
from chinese_doc_extractor import ChineseDocExtractor
from doc_formatter import DocFormatter
from report_generator import ReportGenerator

def test_interface_analyzer():
    """测试接口分析器"""
    print("=== 测试接口分析器 ===")
    code = """
def 用户登录(username: str, password: str) -> bool:
    \"\"\"用户登录接口
    参数：
    - username: 用户名，必须唯一
    - password: 密码，加密存储
    返回：登录成功返回True，否则False
    示例：用户登录('admin', '123456')
    \"\"\"
    pass

def 获取用户资料(user_id: int) -> dict:
    \"\"\"获取用户详细资料
    参数：
    - user_id: 用户ID
    返回：用户字典
    \"\"\"
    pass
"""
    analyzer = InterfaceAnalyzer(code, 'python')
    interfaces = analyzer.analyze()
    print(f"找到 {len(interfaces)} 个接口:")
    for iface in interfaces:
        print(f"  - {iface['type']}: {iface['name']}({', '.join(iface['args'])}) 行号:{iface.get('line', 'N/A')}")
    return interfaces

def test_chinese_extractor(interfaces):
    """测试中文文档提取器"""
    print("\n=== 测试中文文档提取器 ===")
    code = """
def 用户登录(username: str, password: str) -> bool:
    \"\"\"用户登录接口
    参数：
    - username: 用户名，必须唯一
    - password: 密码，加密存储
    返回：登录成功返回True，否则False
    示例：用户登录('admin', '123456')
    \"\"\"
    # 检查用户名是否存在
    if check_user(username):
        return verify_password(password)
    return False
"""
    extractor = ChineseDocExtractor(code)
    if interfaces:
        result = extractor.extract_for_interface(interfaces[0], 0, 10)
        print(f"提取结果:")
        print(f"  描述: {result.get('description', '无')}")
        print(f"  注释: {result.get('comments', [])}")
        print(f"  参数: {result.get('params', {})}")
    return code

def test_doc_formatter(interfaces):
    """测试文档格式化器"""
    print("\n=== 测试文档格式化器 ===")
    formatter = DocFormatter(interfaces)
    md = formatter.format_markdown()
    print(f"Markdown输出前100字符:")
    print(md[:100] + "...")
    return md

def test_report_generator():
    """测试报告生成器"""
    print("\n=== 测试报告生成器 ===")
    with open('sample_input.json', 'r', encoding='utf-8') as f:
        input_data = json.load(f)

    generator = ReportGenerator(input_data)
    result = generator.generate()
    print(f"生成结果:")
    print(f"  状态: {result['status']}")
    print(f"  接口数: {result['interfaces_count']}")
    print(f"  输出文件: {result['output_file']}")
    print(f"  预览: {result['preview'][:80]}...")
    return result

def main():
    """主测试函数"""
    print("开始测试中文接口文档生成器技能...")

    # 1. 测试接口分析器
    interfaces = test_interface_analyzer()

    # 2. 测试中文提取器
    test_code = test_chinese_extractor(interfaces)

    # 3. 测试文档格式化器
    test_doc_formatter(interfaces)

    # 4. 测试报告生成器
    if os.path.exists('sample_input.json'):
        test_report_generator()
    else:
        print("警告: sample_input.json 不存在，跳过报告生成器测试")

    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    main()