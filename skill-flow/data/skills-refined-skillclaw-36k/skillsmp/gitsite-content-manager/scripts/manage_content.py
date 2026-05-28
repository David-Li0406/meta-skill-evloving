#!/usr/bin/env python3
"""
GitSite Content Manager
自动管理 GitSite 项目的 blogs、books 和 pages 内容
"""

import sys
import re
import shutil
from datetime import datetime
from pathlib import Path
import argparse


class GitSiteContentManager:
    def __init__(self, source_dir: str = "source"):
        self.source_dir = Path(source_dir)
        self.blogs_dir = self.source_dir / "blogs" / "tech"
        self.books_dir = self.source_dir / "books"
        self.pages_dir = self.source_dir / "pages"
        self.site_yml_path = self.source_dir / "site.yml"

    def _add_to_site_navigation(self, title: str, uri: str) -> bool:
        """
        在 site.yml 的 navigation 部分添加新条目

        Args:
            title: 导航标题
            uri: URI 路径

        Returns:
            bool: 是否成功添加
        """
        if not self.site_yml_path.exists():
            print(f"⚠️  警告: site.yml 不存在，跳过导航更新")
            return False

        # 读取 site.yml 内容
        content = self.site_yml_path.read_text(encoding="utf-8")

        # 查找 navigation 部分
        nav_pattern = r'(navigation:\s*\n(?:[ \t]+-[ \t]+title:[ \t]+[^\n]+\n(?:[ \t]+uri:[ \t]+[^\n]+\n)*)+)'
        nav_match = re.search(nav_pattern, content)

        if not nav_match:
            print(f"⚠️  警告: 未找到 navigation 部分，跳过导航更新")
            return False

        # 在 Blogs 条目之前插入新书籍
        # 查找 Blogs 的位置
        blogs_pattern = r'([ \t]+-[ \t]+title:[ \t]+Blogs[ \t]*\n[ \t]+uri:[ \t]+/blogs/tech/index\.html[ \t]*\n)'
        new_entry = f"    - title: {title}\n      uri: {uri}\n"

        if re.search(blogs_pattern, content):
            # 在 Blogs 之前插入
            new_content = re.sub(
                blogs_pattern,
                new_entry + r'\1',
                content
            )
        else:
            # 没找到 Blogs，直接在 navigation 末尾添加
            nav_end = content.find("\n  git:")
            if nav_end == -1:
                nav_end = content.find("\nbuild:")
            if nav_end != -1:
                new_content = content[:nav_end] + new_entry + content[nav_end:]
            else:
                new_content = content + new_entry

        # 写回文件
        self.site_yml_path.write_text(new_content, encoding="utf-8")
        print(f"✅ 已更新 site.yml 导航: {title}")
        return True

    def create_blog_post(self, title: str, date: str = None, description: str = "",
                         tags: list = None, author: str = "Orangon") -> dict:
        """
        创建新的博客文章

        Args:
            title: 博客标题
            date: 日期 (YYYY-MM-DD 格式，默认为今天)
            description: 博客描述
            tags: 标签列表
            author: 作者名称

        Returns:
            dict: 包含创建结果的字典
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        if tags is None:
            tags = ["tech", "tutorial"]

        # 创建博客目录名 (支持带 slug 的格式)
        slug = self._slugify(title)
        post_dir_name = f"{date}-{slug}" if title else date
        post_dir = self.blogs_dir / post_dir_name

        if post_dir.exists():
            return {
                "success": False,
                "error": f"博客文章目录已存在: {post_dir}",
                "path": str(post_dir)
            }

        # 创建目录
        post_dir.mkdir(parents=True, exist_ok=True)

        # 生成内容 (注意: GitSite 不支持 frontmatter)
        content = f"""# {title}

<!-- Write your blog post content here -->

## Introduction

<!-- Add your introduction -->

## Main Content

<!-- Add your main content -->

## Conclusion

<!-- Add your conclusion -->
"""

        # 写入 README.md
        readme_path = post_dir / "README.md"
        readme_path.write_text(content, encoding="utf-8")

        return {
            "success": True,
            "path": str(readme_path),
            "url": f"/blogs/tech/{post_dir_name}/index.html",
            "message": f"博客文章已创建: {title}"
        }

    def create_book_chapter(self, book_name: str, chapter_number: str,
                           chapter_title: str, description: str = "") -> dict:
        """
        创建新的书籍章节

        Args:
            book_name: 书籍目录名 (如 AI-Coding)
            chapter_number: 章节编号 (如 01, 02)
            chapter_title: 章节标题
            description: 章节描述

        Returns:
            dict: 包含创建结果的字典
        """
        # 规范化书籍名称
        book_name = self._normalize_book_name(book_name)
        book_dir = self.books_dir / book_name

        if not book_dir.exists():
            return {
                "success": False,
                "error": f"书籍目录不存在: {book_dir}",
                "suggestion": f"请先创建书籍目录或检查书籍名称是否正确"
            }

        # 创建章节目录
        chapter_dir_name = f"{chapter_number}-{self._slugify(chapter_title)}"
        chapter_dir = book_dir / chapter_dir_name

        if chapter_dir.exists():
            return {
                "success": False,
                "error": f"章节目录已存在: {chapter_dir}",
                "path": str(chapter_dir)
            }

        # 创建目录
        chapter_dir.mkdir(parents=True, exist_ok=True)

        # 生成内容 (注意: GitSite 不支持 frontmatter)
        content = f"""# {chapter_title}

<!-- Write your chapter content here -->

## Overview

<!-- Add chapter overview -->

## Main Content

<!-- Add your main content -->

## Summary

<!-- Add chapter summary -->

## References

<!-- Add references if needed -->
"""

        # 写入 README.md
        readme_path = chapter_dir / "README.md"
        readme_path.write_text(content, encoding="utf-8")

        return {
            "success": True,
            "path": str(readme_path),
            "url": f"/books/{book_name}/{chapter_dir_name}/index.html",
            "message": f"章节已创建: {chapter_title}"
        }

    def create_subchapter(self, book_name: str, chapter_number: str,
                         subchapter_number: str, subchapter_title: str) -> dict:
        """
        创建子章节（在现有章节下创建多层级文档，如 1.1、1.2）

        Args:
            book_name: 书籍目录名 (如 test)
            chapter_number: 章节编号 (如 01)
            subchapter_number: 子章节编号 (如 1, 2, 或 1.1)
            subchapter_title: 子章节标题

        Returns:
            dict: 包含创建结果的字典
        """
        # 规范化书籍名称
        book_name = self._normalize_book_name(book_name)
        book_dir = self.books_dir / book_name

        if not book_dir.exists():
            return {
                "success": False,
                "error": f"书籍目录不存在: {book_dir}",
                "suggestion": f"请先创建书籍目录"
            }

        # 查找父章节目录
        chapter_dirs = sorted([d for d in book_dir.iterdir() if d.is_dir() and d.name.startswith(f"{chapter_number}-")])
        if not chapter_dirs:
            return {
                "success": False,
                "error": f"未找到章节 {chapter_number}",
                "suggestion": f"请先使用 'chapter' 命令创建父章节"
            }

        parent_chapter_dir = chapter_dirs[0]

        # 创建子章节目录名 (如 01-1, 01-2)
        # 支持两种格式：1.1 -> 01-1, 或直接用 1 -> 01-1
        if "." in subchapter_number:
            # 格式: "1.1" -> "01-1-1"
            parts = subchapter_number.split(".")
            sub_dir_name = f"{chapter_number}-{parts[0]}-{parts[1]}-{self._slugify(subchapter_title)}"
        else:
            # 格式: "1" -> "01-1"
            sub_dir_name = f"{chapter_number}-{subchapter_number}-{self._slugify(subchapter_title)}"

        subchapter_dir = parent_chapter_dir / sub_dir_name

        if subchapter_dir.exists():
            return {
                "success": False,
                "error": f"子章节目录已存在: {subchapter_dir}",
                "path": str(subchapter_dir)
            }

        # 创建目录
        subchapter_dir.mkdir(parents=True, exist_ok=True)

        # 生成内容 (注意: GitSite 不支持 frontmatter)
        content = f"""# {subchapter_title}

<!-- Write your subchapter content here -->

## Overview

<!-- Add subchapter overview -->

## Main Content

<!-- Add your main content -->

## Summary

<!-- Add subchapter summary -->

## References

<!-- Add references if needed -->
"""

        # 写入 README.md
        readme_path = subchapter_dir / "README.md"
        readme_path.write_text(content, encoding="utf-8")

        return {
            "success": True,
            "path": str(readme_path),
            "url": f"/books/{book_name}/{parent_chapter_dir.name}/{sub_dir_name}/index.html",
            "message": f"子章节已创建: {subchapter_title}"
        }

    def create_page(self, page_name: str, title: str = None,
                   description: str = "") -> dict:
        """
        创建新的静态页面

        Args:
            page_name: 页面目录名 (如 license, about)
            title: 页面标题 (默认使用 page_name)
            description: 页面描述

        Returns:
            dict: 包含创建结果的字典
        """
        if title is None:
            title = page_name.replace("-", " ").replace("_", " ").title()

        page_dir = self.pages_dir / page_name

        if page_dir.exists():
            return {
                "success": False,
                "error": f"页面目录已存在: {page_dir}",
                "path": str(page_dir)
            }

        # 创建目录
        page_dir.mkdir(parents=True, exist_ok=True)

        # 生成内容 (注意: GitSite 不支持 frontmatter)
        content = f"""# {title}

<!-- Write your page content here -->
"""

        # 写入 README.md
        readme_path = page_dir / "README.md"
        readme_path.write_text(content, encoding="utf-8")

        return {
            "success": True,
            "path": str(readme_path),
            "url": f"/pages/{page_name}/index.html",
            "message": f"页面已创建: {title}"
        }

    def create_book(self, book_name: str, title: str,
                   description: str = "", author: str = "Orangon") -> dict:
        """
        创建新的书籍

        Args:
            book_name: 书籍目录名 (如 AI-Coding)
            title: 书籍标题
            description: 书籍描述
            author: 作者名称

        Returns:
            dict: 包含创建结果的字典
        """
        book_dir = self.books_dir / book_name

        if book_dir.exists():
            return {
                "success": False,
                "error": f"书籍目录已存在: {book_dir}",
                "path": str(book_dir)
            }

        # 创建目录
        book_dir.mkdir(parents=True, exist_ok=True)

        # 创建 book.yml
        book_yml_content = f"""title: {title}
description: {description}
author: {author}
"""

        book_yml_path = book_dir / "book.yml"
        book_yml_path.write_text(book_yml_content, encoding="utf-8")

        # 创建 index.md (注意: GitSite 不支持 frontmatter)
        index_md_content = f"""# {title}

<!-- 书籍索引页面 -->

## 目录

<!-- GitSite 会自动根据章节目录生成目录 -->
"""

        index_path = book_dir / "index.md"
        index_path.write_text(index_md_content, encoding="utf-8")

        # 更新 site.yml 导航
        uri = f"/books/{book_name}/index.html"
        self._add_to_site_navigation(title, uri)

        return {
            "success": True,
            "path": str(book_dir),
            "url": uri,
            "message": f"书籍已创建: {title}"
        }

    def _slugify(self, text: str) -> str:
        """将文本转换为 URL 友好的 slug"""
        # 转换为小写，替换空格和特殊字符为连字符
        slug = re.sub(r'[^\w\s-]', '', text.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')

    def _normalize_book_name(self, book_name: str) -> str:
        """规范化书籍名称"""
        # 移除可能的 books/ 前缀
        book_name = book_name.replace("books/", "").replace("books\\", "")
        # 移除尾部斜杠
        book_name = book_name.rstrip("/").rstrip("\\")
        return book_name

    # ========== 列表功能 ==========

    def list_books(self) -> dict:
        """
        列出所有书籍

        Returns:
            dict: 包含书籍列表的字典
        """
        if not self.books_dir.exists():
            return {
                "success": False,
                "error": f"书籍目录不存在: {self.books_dir}"
            }

        books = []
        for book_dir in sorted(self.books_dir.iterdir()):
            if book_dir.is_dir():
                book_yml = book_dir / "book.yml"
                title = book_dir.name
                if book_yml.exists():
                    # 读取 book.yml 获取标题
                    content = book_yml.read_text(encoding="utf-8")
                    for line in content.split("\n"):
                        if line.startswith("title:"):
                            title = line.split(":", 1)[1].strip()
                            break

                # 统计章节数
                chapters = [d for d in book_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
                books.append({
                    "name": book_dir.name,
                    "title": title,
                    "chapters_count": len(chapters)
                })

        return {
            "success": True,
            "books": books
        }

    def list_book_structure(self, book_name: str) -> dict:
        """
        列出书籍的章节结构（树形显示）

        Args:
            book_name: 书籍目录名

        Returns:
            dict: 包含章节结构的字典
        """
        book_name = self._normalize_book_name(book_name)
        book_dir = self.books_dir / book_name

        if not book_dir.exists():
            return {
                "success": False,
                "error": f"书籍目录不存在: {book_dir}"
            }

        def build_tree(directory: Path, prefix: str = "", is_last: bool = True) -> list:
            """递归构建目录树"""
            items = []
            dirs = sorted([d for d in directory.iterdir() if d.is_dir() and not d.name.startswith(".")])

            for i, dir_path in enumerate(dirs):
                is_last_item = (i == len(dirs) - 1)
                # 使用目录名作为显示名称
                display_name = dir_path.name

                # 检查是否有 README.md
                has_readme = (dir_path / "README.md").exists()
                status = "✓" if has_readme else "✗"

                items.append({
                    "prefix": prefix,
                    "name": display_name,
                    "status": status,
                    "path": str(dir_path.relative_to(book_dir))
                })

                # 递归处理子目录
                if prefix == "":
                    new_prefix = "    " if is_last_item else "│   "
                else:
                    new_prefix = prefix + ("    " if is_last_item else "│   ")

                items.extend(build_tree(dir_path, new_prefix, is_last_item))

            return items

        tree_items = build_tree(book_dir)

        return {
            "success": True,
            "book": book_name,
            "tree": tree_items
        }

    # ========== 删除功能 ==========

    def delete_subchapter(self, book_name: str, chapter_number: str,
                         subchapter_number: str, force: bool = False) -> dict:
        """
        删除子章节

        Args:
            book_name: 书籍目录名
            chapter_number: 父章节编号
            subchapter_number: 子章节编号
            force: 是否强制删除（不确认）

        Returns:
            dict: 包含删除结果的字典
        """
        book_name = self._normalize_book_name(book_name)
        book_dir = self.books_dir / book_name

        if not book_dir.exists():
            return {
                "success": False,
                "error": f"书籍目录不存在: {book_dir}"
            }

        # 查找父章节目录
        chapter_dirs = sorted([d for d in book_dir.iterdir() if d.is_dir() and d.name.startswith(f"{chapter_number}-")])
        if not chapter_dirs:
            return {
                "success": False,
                "error": f"未找到章节 {chapter_number}"
            }

        parent_chapter_dir = chapter_dirs[0]

        # 构建子章节目录名
        if "." in subchapter_number:
            parts = subchapter_number.split(".")
            sub_dir_name = f"{chapter_number}-{parts[0]}-{parts[1]}"
        else:
            sub_dir_name = f"{chapter_number}-{subchapter_number}"

        # 查找匹配的子章节目录
        subchapter_dirs = sorted([d for d in parent_chapter_dir.iterdir()
                                 if d.is_dir() and d.name.startswith(sub_dir_name)])

        if not subchapter_dirs:
            return {
                "success": False,
                "error": f"未找到子章节 {subchapter_number}"
            }

        subchapter_dir = subchapter_dirs[0]

        # 确认删除
        if not force:
            print(f"⚠️  即将删除子章节: {subchapter_dir.name}")
            print(f"   路径: {subchapter_dir}")
            confirm = input("确认删除? (yes/no): ")
            if confirm.lower() not in ["yes", "y"]:
                return {
                    "success": False,
                    "error": "取消删除"
                }

        # 删除目录
        shutil.rmtree(subchapter_dir)

        return {
            "success": True,
            "message": f"子章节已删除: {subchapter_dir.name}",
            "path": str(subchapter_dir)
        }

    def delete_chapter(self, book_name: str, chapter_number: str,
                      force: bool = False) -> dict:
        """
        删除章节（包括其所有子章节）

        Args:
            book_name: 书籍目录名
            chapter_number: 章节编号
            force: 是否强制删除（不确认）

        Returns:
            dict: 包含删除结果的字典
        """
        book_name = self._normalize_book_name(book_name)
        book_dir = self.books_dir / book_name

        if not book_dir.exists():
            return {
                "success": False,
                "error": f"书籍目录不存在: {book_dir}"
            }

        # 查找章节目录
        chapter_dirs = sorted([d for d in book_dir.iterdir() if d.is_dir() and d.name.startswith(f"{chapter_number}-")])
        if not chapter_dirs:
            return {
                "success": False,
                "error": f"未找到章节 {chapter_number}"
            }

        chapter_dir = chapter_dirs[0]

        # 统计子章节
        subchapters = [d for d in chapter_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]

        # 确认删除
        if not force:
            print(f"⚠️  即将删除章节: {chapter_dir.name}")
            print(f"   路径: {chapter_dir}")
            if subchapters:
                print(f"   包含 {len(subchapters)} 个子章节")
            confirm = input("确认删除? (yes/no): ")
            if confirm.lower() not in ["yes", "y"]:
                return {
                    "success": False,
                    "error": "取消删除"
                }

        # 删除目录
        shutil.rmtree(chapter_dir)

        return {
            "success": True,
            "message": f"章节已删除: {chapter_dir.name}",
            "path": str(chapter_dir)
        }

    def delete_book(self, book_name: str, force: bool = False) -> dict:
        """
        删除整个书籍（包括所有章节和子章节）

        Args:
            book_name: 书籍目录名
            force: 是否强制删除（不确认）

        Returns:
            dict: 包含删除结果的字典
        """
        book_name = self._normalize_book_name(book_name)
        book_dir = self.books_dir / book_name

        if not book_dir.exists():
            return {
                "success": False,
                "error": f"书籍目录不存在: {book_dir}"
            }

        # 统计章节数
        chapters = [d for d in book_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]

        # 确认删除
        if not force:
            print(f"⚠️  即将删除书籍: {book_name}")
            print(f"   路径: {book_dir}")
            print(f"   包含 {len(chapters)} 个章节")
            confirm = input("确认删除? (yes/no): ")
            if confirm.lower() not in ["yes", "y"]:
                return {
                    "success": False,
                    "error": "取消删除"
                }

        # 删除目录
        shutil.rmtree(book_dir)

        # 从 site.yml 移除导航条目
        if self.site_yml_path.exists():
            content = self.site_yml_path.read_text(encoding="utf-8")
            # 移除匹配的导航条目
            pattern = rf'[ \t]+-[ \t]+title:[ \t]+{re.escape(book_name)}[ \t]*\n[ \t]+uri:[ \t]+/books/{re.escape(book_name)}/index\.html[ \t]*\n?'
            new_content = re.sub(pattern, '', content)
            if new_content != content:
                self.site_yml_path.write_text(new_content, encoding="utf-8")
                print(f"✅ 已从 site.yml 移除导航: {book_name}")

        return {
            "success": True,
            "message": f"书籍已删除: {book_name}",
            "path": str(book_dir)
        }


def main():
    parser = argparse.ArgumentParser(
        description="GitSite Content Manager - 管理博客、书籍和页面内容"
    )

    parser.add_argument(
        "--source-dir",
        default="source",
        help="源代码目录 (默认: source)"
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 博客文章命令
    blog_parser = subparsers.add_parser("blog", help="创建博客文章")
    blog_parser.add_argument("--title", required=True, help="博客标题")
    blog_parser.add_argument("--date", help="日期 (YYYY-MM-DD)")
    blog_parser.add_argument("--description", default="", help="博客描述")
    blog_parser.add_argument("--tags", nargs="+", default=["tech"], help="标签列表")
    blog_parser.add_argument("--author", default="Orangon", help="作者名称")

    # 书籍命令
    book_parser = subparsers.add_parser("book", help="创建书籍")
    book_parser.add_argument("--name", required=True, help="书籍目录名")
    book_parser.add_argument("--title", required=True, help="书籍标题")
    book_parser.add_argument("--description", default="", help="书籍描述")
    book_parser.add_argument("--author", default="Orangon", help="作者名称")

    # 章节命令
    chapter_parser = subparsers.add_parser("chapter", help="创建书籍章节")
    chapter_parser.add_argument("--book", required=True, help="书籍目录名")
    chapter_parser.add_argument("--number", required=True, help="章节编号")
    chapter_parser.add_argument("--title", required=True, help="章节标题")
    chapter_parser.add_argument("--description", default="", help="章节描述")

    # 子章节命令
    subchapter_parser = subparsers.add_parser("subchapter", help="创建子章节（多层级文档）")
    subchapter_parser.add_argument("--book", required=True, help="书籍目录名")
    subchapter_parser.add_argument("--chapter", required=True, help="父章节编号 (如 01)")
    subchapter_parser.add_argument("--number", required=True, help="子章节编号 (如 1 或 1.1)")
    subchapter_parser.add_argument("--title", required=True, help="子章节标题")

    # 页面命令
    page_parser = subparsers.add_parser("page", help="创建静态页面")
    page_parser.add_argument("--name", required=True, help="页面目录名")
    page_parser.add_argument("--title", help="页面标题")
    page_parser.add_argument("--description", default="", help="页面描述")

    # 列表命令
    list_parser = subparsers.add_parser("list", help="列出内容")
    list_parser.add_argument("--type", choices=["books", "blogs", "pages"], default="books", help="内容类型")
    list_parser.add_argument("--book", help="书籍名称（用于显示章节结构）")

    # 删除命令
    delete_parser = subparsers.add_parser("delete", help="删除内容")
    delete_parser.add_argument("--type", choices=["book", "chapter", "subchapter"], required=True, help="删除类型")
    delete_parser.add_argument("--book", help="书籍目录名")
    delete_parser.add_argument("--chapter", help="章节编号")
    delete_parser.add_argument("--subchapter", help="子章节编号")
    delete_parser.add_argument("--force", action="store_true", help="强制删除，不确认")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    manager = GitSiteContentManager(args.source_dir)

    if args.command == "blog":
        result = manager.create_blog_post(
            title=args.title,
            date=args.date,
            description=args.description,
            tags=args.tags,
            author=args.author
        )
    elif args.command == "book":
        result = manager.create_book(
            book_name=args.name,
            title=args.title,
            description=args.description,
            author=args.author
        )
    elif args.command == "chapter":
        result = manager.create_book_chapter(
            book_name=args.book,
            chapter_number=args.number,
            chapter_title=args.title,
            description=args.description
        )
    elif args.command == "page":
        result = manager.create_page(
            page_name=args.name,
            title=args.title,
            description=args.description
        )
    elif args.command == "subchapter":
        result = manager.create_subchapter(
            book_name=args.book,
            chapter_number=args.chapter,
            subchapter_number=args.number,
            subchapter_title=args.title
        )
    elif args.command == "list":
        if args.book:
            result = manager.list_book_structure(args.book)
        else:
            result = manager.list_books()
    elif args.command == "delete":
        if args.type == "book":
            result = manager.delete_book(args.book, args.force)
        elif args.type == "chapter":
            result = manager.delete_chapter(args.book, args.chapter, args.force)
        elif args.type == "subchapter":
            result = manager.delete_subchapter(args.book, args.chapter, args.subchapter, args.force)
    else:
        parser.print_help()
        return 1

    # 输出结果
    if result.get("success"):
        # 列表命令的特殊输出
        if args.command == "list":
            if "books" in result:
                print(f"\n📚 书籍列表 ({len(result['books'])} 个):\n")
                for book in result["books"]:
                    print(f"  📖 {book['name']}")
                    print(f"     标题: {book['title']}")
                    print(f"     章节数: {book['chapters_count']}")
                    print()
            elif "tree" in result:
                print(f"\n📖 书籍结构: {result['book']}\n")
                print(f"{result['book']}/")
                for item in result["tree"]:
                    connector = "└── " if "    " in item["prefix"] else "├── "
                    status_icon = "✓" if item["status"] == "✓" else "✗"
                    print(f"{item['prefix']}{connector}{item['name']} [{status_icon}]")
                print()
            return 0

        # 删除命令的成功输出
        if args.command == "delete":
            print(f"✅ {result['message']}")
            return 0

        # 创建命令的标准输出
        print(f"✅ {result['message']}")
        print(f"📄 路径: {result['path']}")
        if "url" in result:
            print(f"🔗 URL: {result['url']}")
        return 0
    else:
        print(f"❌ 错误: {result['error']}")
        if "suggestion" in result:
            print(f"💡 建议: {result['suggestion']}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
