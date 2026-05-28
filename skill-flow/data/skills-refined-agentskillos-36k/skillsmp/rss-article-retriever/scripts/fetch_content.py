#!/usr/bin/env python3
"""
微信公众号文章内容抓取脚本
使用 Python Playwright 进行抓取，支持：
- 反检测机制（User-Agent、webdriver 隐藏）
- 智能重试（最多 3 次）
- 完善的错误检测
- JSON 格式输出

用法: python fetch_content.py <URL>
输出: JSON 格式的文章内容或错误信息
"""

import asyncio
import argparse
import json
import sys
from typing import Optional, Dict, Any


def parse_args():
    parser = argparse.ArgumentParser(description='Fetch WeChat Article Content via Playwright')
    parser.add_argument('url', type=str, help='Article URL')
    parser.add_argument('--retries', type=int, default=3, help='Number of retries (default: 3)')
    return parser.parse_args()


async def attempt_fetch(url: str, headless: bool = True) -> Dict[str, Any]:
    """
    尝试抓取微信文章内容
    
    Args:
        url: 文章 URL
        headless: 是否使用无头模式
        
    Returns:
        dict: 包含 title, content, url 的字典
        
    Raises:
        Exception: 抓取失败时抛出异常
    """
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=headless,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )
        
        try:
            # 创建浏览器上下文，设置 User-Agent
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1366, 'height': 768}
            )
            
            page = await context.new_page()
            
            # 反检测设置
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en'] });
                window.chrome = { runtime: {} };
            """)
            
            print(f"正在访问: {url}", file=sys.stderr)
            await page.goto(url, wait_until='networkidle', timeout=30000)
            
            # 等待页面加载
            await asyncio.sleep(3)
            
            # 滚动页面触发懒加载
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(2)
            
            # 提取文章内容
            content = await page.evaluate("""
                () => {
                    // 获取微信公众号文章主体
                    const article = document.querySelector('#js_content') ||
                                   document.querySelector('.rich_media_content') ||
                                   document.body;
                    
                    const rawHtml = article.innerHTML;
                    
                    // 检测错误页面
                    const isErrorPage = rawHtml.includes('参数错误') ||
                                       rawHtml.includes('访问异常') ||
                                       rawHtml.includes('此内容无法查看') ||
                                       document.title === '微信公众平台';
                    
                    if (isErrorPage) {
                        return { error: '检测到错误页面,可能URL无效或需要登录' };
                    }
                    
                    // 清理HTML,保留段落结构
                    let cleanText = rawHtml
                        // 段落标签替换为双换行
                        .replace(/<p[^>]*>/gi, '\\n\\n')
                        .replace(/<\\/p>/gi, '')
                        // br标签替换为换行
                        .replace(/<br\\s*\\/?>/gi, '\\n')
                        // 移除所有HTML标签
                        .replace(/<[^>]+>/g, '')
                        // 处理HTML实体
                        .replace(/&nbsp;/g, ' ')
                        .replace(/&lt;/g, '<')
                        .replace(/&gt;/g, '>')
                        .replace(/&amp;/g, '&')
                        .replace(/&quot;/g, '"')
                        .replace(/&#39;/g, "'")
                        // 清理多余空行(最多保留两个连续换行)
                        .replace(/\\n{3,}/g, '\\n\\n')
                        .replace(/^\\n+/, '')
                        .replace(/\\n+$/, '')
                        .trim();
                    
                    return {
                        title: document.title.replace('微信公众平台', '').trim(),
                        content: cleanText,
                        url: window.location.href
                    };
                }
            """)
            
            if content.get('error'):
                raise Exception(content['error'])
            
            print(f"抓取成功！标题: {content['title']}", file=sys.stderr)
            print(f"内容长度: {len(content['content'])} 字符", file=sys.stderr)
            
            return content
            
        finally:
            await browser.close()


async def fetch_wechat_article(url: str, retries: int = 3) -> Dict[str, Any]:
    """
    抓取微信文章，支持重试和回退到有头模式
    
    Args:
        url: 文章 URL
        retries: 重试次数
        
    Returns:
        dict: JSON 格式的结果
    """
    last_error = None
    
    # 首先尝试无头模式
    for attempt in range(1, retries + 1):
        try:
            print(f"尝试 {attempt}/{retries}: 抓取 {url}", file=sys.stderr)
            result = await attempt_fetch(url, headless=True)
            
            # 验证内容不为空
            if not result.get('content') or len(result['content'].strip()) < 50:
                raise Exception(f"内容为空或太短 ({len(result.get('content', '').strip())} 字符)")
            
            print("✅ 抓取成功！", file=sys.stderr)
            return {
                "version": "1.0.0",
                "operation": "get",
                "result": {
                    "type": "full",
                    "article": {
                        "url": result['url'],
                        "title": result['title'],
                        "content": {
                            "plain_text": result['content'],
                            "source": "playwright-python"
                        },
                        "word_count": len(result['content'])
                    }
                }
            }
        except Exception as e:
            last_error = str(e)
            print(f"❌ 尝试 {attempt} 失败: {last_error}", file=sys.stderr)
            if attempt < retries:
                print(f"⏳ 等待 3 秒后重试...", file=sys.stderr)
                await asyncio.sleep(3)
    
    # 无头模式失败，尝试有头模式（在容器中可能不可用）
    print("⚠️ 无头模式失败，尝试使用有头模式...", file=sys.stderr)
    try:
        result = await attempt_fetch(url, headless=False)
        
        if not result.get('content') or len(result['content'].strip()) < 50:
            raise Exception(f"内容为空或太短 ({len(result.get('content', '').strip())} 字符)")
        
        print("✅ 有头模式抓取成功！", file=sys.stderr)
        return {
            "version": "1.0.0",
            "operation": "get",
            "result": {
                "type": "full",
                "article": {
                    "url": result['url'],
                    "title": result['title'],
                    "content": {
                        "plain_text": result['content'],
                        "source": "playwright-python-headed"
                    },
                    "word_count": len(result['content'])
                }
            }
        }
    except Exception as e:
        print(f"❌ 有头模式也失败了: {e}", file=sys.stderr)
        
        # 返回错误
        return {
            "version": "1.0.0",
            "operation": "get",
            "error": {
                "code": "FETCH_ERROR",
                "message": f"所有尝试均失败。最后错误: {last_error}",
                "suggestion": "页面可能需要登录，或 URL 无效。请尝试其他文章 URL 或直接提供文章内容。"
            }
        }


def main():
    args = parse_args()
    
    try:
        result = asyncio.run(fetch_wechat_article(args.url, args.retries))
    except Exception as e:
        result = {
            "version": "1.0.0",
            "operation": "get",
            "error": {
                "code": "EXECUTION_ERROR",
                "message": str(e),
                "suggestion": "请检查 Playwright 是否已正确安装"
            }
        }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
