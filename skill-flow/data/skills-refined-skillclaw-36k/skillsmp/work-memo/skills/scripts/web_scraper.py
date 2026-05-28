#!/usr/bin/env python3
"""
Web Content Scraper - 抓取并总结网页内容

Usage:
    python web_scraper.py "https://example.com"
    python web_scraper.py "https://example.com" --tags work research
"""

import sys
import argparse
import re
from pathlib import Path
from typing import Optional, List
from urllib.parse import urlparse
import json

# 尝试导入requests和BeautifulSoup
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("错误: 需要安装 requests 和 beautifulsoup4")
    print("运行: pip install requests beautifulsoup4")
    sys.exit(1)

# 添加 scripts 目录到路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from storage import WorkMemoStorage
from schema import WorkRecord, WorkType, Status


def is_valid_url(url: str) -> bool:
    """验证URL格式"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def fetch_webpage(url: str, timeout: int = 10) -> Optional[str]:
    """
    获取网页内容

    Args:
        url: 网页URL
        timeout: 超时时间（秒）

    Returns:
        str: 网页HTML内容
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"❌ 获取网页失败: {e}")
        return None


def extract_content(html: str) -> dict:
    """
    从HTML中提取主要内容

    Args:
        html: HTML内容

    Returns:
        dict: 包含title, content, summary的字典
    """
    soup = BeautifulSoup(html, 'html.parser')

    # 提取标题
    title = ""
    if soup.title:
        title = soup.title.get_text().strip()
    if not title:
        title_tag = soup.find('h1')
        if title_tag:
            title = title_tag.get_text().strip()

    # 移除不需要的标签
    for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe', 'noscript']):
        tag.decompose()

    # 提取主要内容
    content = ""
    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|article|post|entry'))
    
    if main_content:
        # 提取段落
        paragraphs = main_content.find_all('p')
        content = '\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
    else:
        # 回退到所有段落
        paragraphs = soup.find_all('p')
        content = '\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])

    # 清理内容
    content = re.sub(r'\s+', ' ', content)
    content = content.strip()

    # 生成摘要（前500字符）
    summary = content[:500] + "..." if len(content) > 500 else content

    return {
        'title': title,
        'content': content,
        'summary': summary
    }


def summarize_content(content: str, max_length: int = 300) -> str:
    """
    总结内容（简单版本，实际可以使用AI模型）

    Args:
        content: 原始内容
        max_length: 最大长度

    Returns:
        str: 总结内容
    """
    # 简单的摘要生成：提取关键句子
    sentences = re.split(r'[.!?。！？]', content)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # 返回前几个句子
    summary = '. '.join(sentences[:3])
    
    if len(summary) > max_length:
        summary = summary[:max_length] + "..."
    
    return summary


def record_webpage(url: str, tags: Optional[List[str]] = None, urgency: int = 3, importance: int = 3) -> dict:
    """
    抓取网页内容并记录到备忘录

    Args:
        url: 网页URL
        tags: 标签列表
        urgency: 紧急程度 (1-5)
        importance: 重要程度 (1-5)

    Returns:
        dict: 记录信息
    """
    # 验证URL
    if not is_valid_url(url):
        return {
            'status': 'error',
            'message': '无效的URL格式'
        }

    # 获取网页内容
    html = fetch_webpage(url)
    if not html:
        return {
            'status': 'error',
            'message': '无法获取网页内容'
        }

    # 提取内容
    extracted = extract_content(html)
    
    if not extracted['title'] and not extracted['content']:
        return {
            'status': 'error',
            'message': '无法提取网页内容'
        }

    # 生成摘要
    summary = summarize_content(extracted['content'])

    # 创建记录
    storage = WorkMemoStorage()
    storage.initialize()

    # 构建标题
    title = extracted['title'] if extracted['title'] else "网页内容"
    description = f"来源: {url}\n\n摘要: {summary}"

    # 创建记录
    record = WorkRecord(
        title=title,
        description=description,
        type=WorkType.RESEARCH,  # 默认为研究类型
        status=Status.TODO,
        urgency=urgency,
        importance=importance,
        difficulty=5,
    )

    # 添加默认标签
    final_tags = ['web', 'reading']
    if tags:
        final_tags.extend(tags)
    record.tags = list(set(final_tags))

    # 添加URL到上下文
    record.contexts = [url]

    # 保存到数据库
    storage.create(record)

    # 返回记录信息
    result = {
        'status': 'success',
        'id': record.id,
        'title': record.title,
        'url': url,
        'summary': summary,
        'type': record.type.value,
        'urgency': record.urgency,
        'importance': record.importance,
        'tags': record.tags,
        'contexts': record.contexts,
        'eisenhower': record.get_eisenhower_quadrant(),
        'created_at': record.created_at,
    }

    storage.close()
    return result


def print_webpage_record(record: dict):
    """格式化打印网页记录"""
    if record['status'] == 'error':
        print(f"❌ {record['message']}")
        return

    print(f"📝 已记录: {record['id']}")
    print(f"   标题: {record['title']}")
    print(f"   URL: {record['url']}")
    print(f"   摘要: {record['summary']}")
    print(f"   类型: {record['type']}")
    print(f"   优先级: 紧急度 {record['urgency']}/5, 重要度 {record['importance']}/5")
    print(f"   标签: {', '.join(record['tags'])}")
    print(f"   Eisenhower: {record['eisenhower']}")
    print(f"   创建时间: {record['created_at']}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="抓取网页内容并记录到备忘录",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 抓取网页并记录
  python web_scraper.py "https://example.com/article"
  
  # 抓取网页并添加标签
  python web_scraper.py "https://example.com/article" --tags work research
  
  # 设置优先级
  python web_scraper.py "https://example.com/article" --urgency 4 --importance 5
        """
    )

    parser.add_argument(
        'url',
        help='网页URL'
    )
    parser.add_argument(
        '--tags',
        nargs='+',
        help='标签列表'
    )
    parser.add_argument(
        '--urgency',
        type=int,
        choices=range(1, 6),
        default=3,
        help='紧急程度 (1-5, 5=最紧急)'
    )
    parser.add_argument(
        '--importance',
        type=int,
        choices=range(1, 6),
        default=3,
        help='重要程度 (1-5, 5=最重要)'
    )

    args = parser.parse_args()

    # 执行抓取和记录
    result = record_webpage(
        url=args.url,
        tags=args.tags,
        urgency=args.urgency,
        importance=args.importance,
    )
    
    print_webpage_record(result)
    
    if result['status'] == 'success':
        print("\n✅ 网页内容已抓取并记录")


if __name__ == '__main__':
    main()
