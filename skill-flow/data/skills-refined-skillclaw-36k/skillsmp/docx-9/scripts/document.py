#!/usr/bin/env python3
"""
Word文書の変更履歴とコメント管理ライブラリ。

このモジュールはDocumentクラスを提供し、Word文書の変更履歴（tracked changes）と
コメントの追加・編集を行う。
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

import defusedxml.minidom

from utilities import XMLEditor


class DocxXMLEditor(XMLEditor):
    """Word固有の属性を自動注入するXMLEditor拡張。"""

    def __init__(self, xml_path, author: str, rsid: str):
        """初期化。

        Args:
            xml_path: XMLファイルのパス
            author: 変更の著者名
            rsid: リビジョンセッションID
        """
        super().__init__(xml_path)
        self.author = author
        self.rsid = rsid
        self._change_id = 0

    def get_next_change_id(self) -> int:
        """次の変更IDを取得する。"""
        self._change_id += 1
        return self._change_id

    def create_insertion(self, content: str) -> str:
        """挿入マークアップを作成する。

        Args:
            content: 挿入するXMLコンテンツ

        Returns:
            挿入タグで囲まれたコンテンツ
        """
        change_id = self.get_next_change_id()
        date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        return f'<w:ins w:id="{change_id}" w:author="{self.author}" w:date="{date}">{content}</w:ins>'

    def create_deletion(self, content: str) -> str:
        """削除マークアップを作成する。

        Args:
            content: 削除するXMLコンテンツ（w:t を w:delText に変換済みであること）

        Returns:
            削除タグで囲まれたコンテンツ
        """
        change_id = self.get_next_change_id()
        date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        return f'<w:del w:id="{change_id}" w:author="{self.author}" w:date="{date}">{content}</w:del>'


class Document:
    """Word文書の変更履歴とコメントを管理するクラス。"""

    def __init__(
        self,
        unpacked_dir: str,
        author: str = "Claude",
        author_initials: str = "C",
        rsid: Optional[str] = None,
    ):
        """初期化。

        Args:
            unpacked_dir: 展開されたDOCXディレクトリのパス
            author: 変更の著者名
            author_initials: 著者のイニシャル
            rsid: リビジョンセッションID（省略時は自動生成）
        """
        self.unpacked_dir = Path(unpacked_dir)
        self.author = author
        self.author_initials = author_initials
        self.rsid = rsid or self._generate_rsid()

        # document.xmlエディタを初期化
        document_path = self.unpacked_dir / "word" / "document.xml"
        self.editor = DocxXMLEditor(document_path, author, self.rsid)

        self._comment_id = 0

    def _generate_rsid(self) -> str:
        """ランダムなRSIDを生成する。"""
        import random
        return "".join(random.choices("0123456789ABCDEF", k=8))

    def get_next_comment_id(self) -> int:
        """次のコメントIDを取得する。"""
        self._comment_id += 1
        return self._comment_id

    def suggest_deletion(self, node) -> None:
        """ノードを削除としてマークする。

        Args:
            node: 削除対象のDOMノード
        """
        # w:t を w:delText に変換
        for t_elem in node.getElementsByTagName("w:t"):
            new_elem = self.editor.dom.createElement("w:delText")
            new_elem.setAttribute("xml:space", "preserve")
            while t_elem.firstChild:
                new_elem.appendChild(t_elem.firstChild)
            t_elem.parentNode.replaceChild(new_elem, t_elem)

        # 削除マークアップで囲む
        deletion_xml = self.editor.create_deletion(node.toxml())
        self.editor.replace_node(node, deletion_xml)

    def revert_insertion(self, node) -> None:
        """挿入を削除に変換する（変更を元に戻す）。

        Args:
            node: w:ins 要素ノード
        """
        # 挿入の内容を削除に変換
        for t_elem in node.getElementsByTagName("w:t"):
            new_elem = self.editor.dom.createElement("w:delText")
            new_elem.setAttribute("xml:space", "preserve")
            while t_elem.firstChild:
                new_elem.appendChild(t_elem.firstChild)
            t_elem.parentNode.replaceChild(new_elem, t_elem)

        # w:insタグを取得して内容を削除マークアップに変換
        inner_content = ""
        for child in node.childNodes:
            inner_content += child.toxml()

        deletion_xml = self.editor.create_deletion(inner_content)
        self.editor.replace_node(node, deletion_xml)

    def revert_deletion(self, node) -> None:
        """削除を挿入に変換する（削除を却下）。

        Args:
            node: w:del 要素ノード
        """
        # w:delText を w:t に変換
        for del_text in node.getElementsByTagName("w:delText"):
            new_elem = self.editor.dom.createElement("w:t")
            new_elem.setAttribute("xml:space", "preserve")
            while del_text.firstChild:
                new_elem.appendChild(del_text.firstChild)
            del_text.parentNode.replaceChild(new_elem, del_text)

        # 内容を挿入マークアップで囲む
        inner_content = ""
        for child in node.childNodes:
            inner_content += child.toxml()

        insertion_xml = self.editor.create_insertion(inner_content)
        self.editor.replace_node(node, insertion_xml)

    def save(self) -> None:
        """変更をファイルに保存する。"""
        self.editor.save()
        print(f"Saved changes to {self.editor.xml_path}")
