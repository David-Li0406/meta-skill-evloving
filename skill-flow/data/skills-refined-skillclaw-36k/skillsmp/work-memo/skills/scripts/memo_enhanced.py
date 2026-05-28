#!/usr/bin/env python3
"""
增强版 Work Memo CLI 工具

支持功能：
- OKR 快速操作
- 工作备注管理
- 数据美化生成幻灯片
"""

import sys
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

# 数据库位置
DB_PATH = Path.home() / ".workmemo" / "db.json"


def load_memos():
    """加载所有备忘录"""
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('records', {})
    except Exception as e:
        print(f"❌ 加载数据失败: {e}")
        return {}


def save_memos(memos):
    """保存所有备忘录"""
    try:
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump({'records': memos}, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"❌ 保存数据失败: {e}")
        return False


def cmd_okr(args):
    """OKR 快速操作 - 回复R2个任务"""
    memos = load_memos()
    count = int(args.count) if args.count else 2

    # 获取最新的未完成任务
    pending = [
        (k, v) for k, v in memos.items()
        if v.get('status') != 'done'
    ]
    pending.sort(key=lambda x: x[1].get('created_at', ''), reverse=True)

    print(f"✅ OKR - 准备回复 {count} 个任务\n")

    for i in range(min(count, len(pending))):
        memo_id, memo = pending[i]
        print(f"{i+1}. {memo.get('title', memo.get('content', ''))}")
        print(f"   ID: {memo_id}")
        print(f"   类型: {memo.get('type', '任务')}")
        if memo.get('urgency'):
            print(f"   紧急度: {memo['urgency']}")
        print(f"   Eisenhower: {memo.get('eisenhower', 'N/A')}")
        print()

    if len(pending) < count:
        print(f"ℹ️  只有 {len(pending)} 个待办任务，少于请求的 {count} 个")


def cmd_note(args):
    """工作备注管理"""
    memos = load_memos()

    if args.add:
        # 添加备注
        memo_id = f"note_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        note = {
            'id': memo_id,
            'content': args.add,
            'type': '备注',
            'status': 'done',
            'created_at': datetime.now().isoformat(),
            'urgency': '3',
            'eisenhower': 'Q4'
        }

        memos[memo_id] = note
        if save_memos(memos):
            print(f"✅ 备注已添加: {args.add}")
            print(f"   ID: {memo_id}")

    elif args.list_notes:
        # 列出所有备注
        notes = [
            (k, v) for k, v in memos.items()
            if v.get('type') == '备注'
        ]
        notes.sort(key=lambda x: x[1].get('created_at', ''), reverse=True)

        print(f"📝 工作备注 ({len(notes)} 条)\n")

        for i, (memo_id, note) in enumerate(notes, 1):
            print(f"{i}. {note.get('content', '')}")
            print(f"   时间: {note['created_at'][:16]}")

    elif args.search:
        # 搜索备注
        search_term = args.search.lower()
        results = [
            (k, v) for k, v in memos.items()
            if v.get('type') == '备注' and search_term in v.get('content', '').lower()
        ]

        print(f"🔍 搜索 '{args.search}' ({len(results)} 条结果)\n")

        for i, (memo_id, note) in enumerate(results, 1):
            print(f"{i}. {note.get('content', '')}")
            print(f"   ID: {memo_id}")

    else:
        print("❌ 请指定操作：--add, --list-notes, 或 --search")


def cmd_slide(args):
    """数据美化生成幻灯片"""
    memos = load_memos()

    if args.content:
        # 生成幻灯片内容
        content = args.content

        # 幻灯片标题
        title = content if len(content) < 50 else content[:47] + "..."

        # 提取相关备忘录
        related_memos = []
        if args.include_memos:
            related_memos = [
                (k, v) for k, v in memos.items()
                if v.get('status') != 'done' and content.lower() in v.get('content', '').lower()
            ]

        # 生成幻灯片 HTML
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }}

        .slide {{
            background: white;
            border-radius: 20px;
            padding: 60px 80px;
            margin-bottom: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }}

        .header {{
            text-align: center;
            margin-bottom: 40px;
        }}

        .header h1 {{
            font-size: 2.5em;
            color: #667eea;
            margin: 0 0 20px 0;
            font-weight: 700;
        }}

        .header .date {{
            font-size: 1.1em;
            color: #666;
            margin: 0 0 20px;
        }}

        .content {{
            font-size: 1.3em;
            line-height: 1.8;
            color: #444;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}

        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #666;
            font-size: 0.9em;
        }}

        .memos-list {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-top: 30px;
        }}

        .memos-list h3 {{
            margin: 0 0 20px 0;
            color: #667eea;
        }}

        .memo-item {{
            background: white;
            border-left: 4px solid #667eea;
            padding: 12px 16px;
            margin-bottom: 10px;
            border-radius: 4px;
        }}

        .memo-item strong {{
            color: #667eea;
        }}

        .tag {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-left: 10px;
        }}

        .controls {{
            text-align: center;
            margin-top: 40px;
        }}

        .controls p {{
            color: #666;
            font-size: 0.9em;
            margin: 5px 0;
        }}

        .controls code {{
            background: #667eea;
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
            font-family: monospace;
            margin: 0 5px;
        }}

        @media print {{
            .slide {{
                box-shadow: none;
                border: 1px solid #ddd;
            }}
            body {{
                background: white;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="slide">
            <div class="header">
                <h1>{title}</h1>
                <p class="date">📅 {datetime.now().strftime('%Y年%m月%d日')}</p>
            </div>

            <div class="content">{content}</div>
"""

        # 如果有相关备忘录
        if related_memos:
            html_content += f"""
            <div class="memos-list">
                <h3>📋 相关工作记录 ({len(related_memos)} 条)</h3>
"""
            for memo_id, memo in related_memos[:10]:
                html_content += f"""
                <div class="memo-item">
                    <strong>{memo.get('content', '')}</strong>
                    <span class="tag">{memo.get('type', '备忘')}</span>
                </div>
"""
            html_content += """
            </div>
"""

        html_content += f"""
            <div class="footer">
                <p>📊 Work Memo</p>
            </div>
        </div>

        <div class="controls">
            <p>📌 提示：</p>
            <p>使用浏览器打开 HTML 文件</p>
            <p>按 <code>Command + P</code> 进入演示模式</p>
            <p>按 <code>ESC</code> 退出演示模式</p>
        </div>
    </div>
</body>
</html>
"""

        # 保存文件
        output_dir = Path.home() / "workmemo-slides"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"slide_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        output_file.write_text(html_content, encoding='utf-8')

        print(f"✅ 幻灯片已生成: {output_file}")
        print(f"   标题: {title}")
        print(f"   保存位置: {output_file}")
        print(f"   备注数量: {len(related_memos)}")

    else:
        print("❌ 请提供幻灯片内容")


def main():
    parser = argparse.ArgumentParser(
        description="Work Memo 增强命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # OKR 命令
    parser.add_argument(
        '--okr',
        action='store_true',
        help='OKR 快速操作 - 回复任务列表'
    )
    parser.add_argument(
        '--count',
        type=int,
        default=2,
        help='回复的任务数量 (默认: 2)'
    )

    # 工作备注命令
    parser.add_argument(
        'note',
        action='store_true',
        help='工作备注管理'
    )
    parser.add_argument(
        '--add',
        type=str,
        metavar='内容',
        help='添加工作备注'
    )
    parser.add_argument(
        '--list-notes',
        action='store_true',
        help='列出所有工作备注'
    )
    parser.add_argument(
        '--search',
        type=str,
        metavar='关键词',
        help='搜索工作备注'
    )

    # 幻灯片生成命令
    parser.add_argument(
        'slide',
        action='store_true',
        help='数据美化生成幻灯片'
    )
    parser.add_argument(
        '--content',
        type=str,
        help='幻灯片内容'
    )
    parser.add_argument(
        '--include-memos',
        action='store_true',
        help='包含相关的备忘录'
    )

    args = parser.parse_args()

    # 执行相应命令
    if args.okr:
        cmd_okr(args)
    elif args.add:
        cmd_note(args)
    elif args.list_notes:
        cmd_note(args)
    elif args.search:
        cmd_note(args)
    elif args.slide:
        cmd_slide(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
