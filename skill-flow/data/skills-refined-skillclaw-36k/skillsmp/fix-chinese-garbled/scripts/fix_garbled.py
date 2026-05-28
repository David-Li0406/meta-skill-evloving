#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文乱码修复工具
智能检测并修复各种类型的中文乱码
"""

from typing import Optional, Tuple, List


class GarbledFixer:
    """中文乱码修复器"""

    # 中文常用字（用于判断修复是否成功）
    COMMON_CHINESE_CHARS = "的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战先回则任取完举科触广"

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def fix(self, text: str, encoding_hint: Optional[str] = None) -> Tuple[Optional[str], str]:
        """
        智能修复乱码文本

        Args:
            text: 乱码文本
            encoding_hint: 可选的编码提示 (gbk/utf-8/iso8859-1)

        Returns:
            (修复后的文本, 使用的修复方法)
        """
        if not text:
            return None, "empty_input"

        # 如果已经是正常中文，直接返回
        if self._is_normal_chinese(text):
            return text, "already_normal"

        best_result = None
        best_score = 0
        best_method = "unknown"

        # 根据编码提示优先尝试特定编码组合
        if encoding_hint:
            hint_methods = self._get_hint_methods(encoding_hint)
            for from_enc, to_enc, desc in hint_methods:
                result = self._try_convert(text, from_enc, to_enc)
                if result:
                    score = self._chinese_score(result)
                    if self.verbose:
                        print(f"[提示优先] {desc}: 得分 {score:.2f}")
                    if score > best_score:
                        best_result = result
                        best_score = score
                        best_method = desc

        # 尝试所有编码组合
        methods = [
            ("latin-1", "utf-8", "Latin-1 -> UTF-8"),
            ("latin-1", "gbk", "Latin-1 -> GBK"),
            ("latin-1", "gb18030", "Latin-1 -> GB18030"),
        ]

        for from_enc, to_enc, desc in methods:
            result = self._try_convert(text, from_enc, to_enc)
            if result:
                score = self._chinese_score(result)
                if self.verbose:
                    print(f"[通用尝试] {desc}: 得分 {score:.2f}")
                if score > best_score:
                    best_result = result
                    best_score = score
                    best_method = desc

        # 尝试特殊修复
        special_results = self._try_special_fixes(text)
        for result, method in special_results:
            score = self._chinese_score(result)
            if self.verbose:
                print(f"[特殊修复] {method}: 得分 {score:.2f}")
            if score > best_score:
                best_result = result
                best_score = score
                best_method = method

        # 设置阈值
        if best_score > 0.6:
            return best_result, best_method
        elif best_score > 0.3:
            return best_result, f"{best_method} (low confidence)"
        else:
            return None, "no_match_found"

    def _get_hint_methods(self, encoding_hint: str) -> List[Tuple[str, str, str]]:
        """根据编码提示返回优先尝试的编码组合"""
        hint = encoding_hint.lower()
        if hint in ("gbk", "gb2312", "gb18030"):
            return [
                ("latin-1", "gbk", "Latin-1 -> GBK (hint)"),
                ("utf-8", "gbk", "UTF-8 -> GBK (hint)"),
                ("gbk", "utf-8", "GBK -> UTF-8 (hint)"),
            ]
        elif hint in ("utf-8", "utf8"):
            return [
                ("latin-1", "utf-8", "Latin-1 -> UTF-8 (hint)"),
                ("gbk", "utf-8", "GBK -> UTF-8 (hint)"),
            ]
        elif hint in ("iso8859-1", "latin-1", "latin1"):
            return [
                ("latin-1", "utf-8", "Latin-1 -> UTF-8 (hint)"),
                ("latin-1", "gbk", "Latin-1 -> GBK (hint)"),
            ]
        return []

    def _try_convert(self, text: str, from_enc: str, to_enc: str) -> Optional[str]:
        """尝试转换编码"""
        try:
            bytes_data = text.encode(from_enc, errors="ignore")
            return bytes_data.decode(to_enc, errors="ignore")
        except (UnicodeDecodeError, UnicodeEncodeError):
            return None

    def _try_special_fixes(self, text: str) -> List[Tuple[str, str]]:
        """尝试特殊修复方法"""
        results = []

        # 锟拷码修复
        try:
            bytes_data = text.encode("gbk", errors="ignore")
            fixed = bytes_data.decode("utf-8", errors="ignore")
            if fixed != text:
                results.append((fixed, "GBK -> UTF-8 (锟拷码)"))
        except Exception:
            pass

        # 反向尝试
        try:
            bytes_data = text.encode("utf-8", errors="ignore")
            fixed = bytes_data.decode("gbk", errors="ignore")
            if fixed != text:
                results.append((fixed, "UTF-8 -> GBK"))
        except Exception:
            pass

        # 尝试 GB18030
        for target in ["utf-8", "gb18030"]:
            try:
                bytes_data = text.encode("latin-1", errors="ignore")
                fixed = bytes_data.decode(target, errors="ignore")
                if fixed != text:
                    results.append((fixed, f"Latin-1 -> {target}"))
            except Exception:
                pass

        return results

    def _chinese_score(self, text: str) -> float:
        """计算文本的中文化得分 (0-1)"""
        if not text:
            return 0

        total = len(text)
        if total == 0:
            return 0

        chinese_count = sum(1 for char in text if self._is_chinese_char(char))
        ratio = chinese_count / total

        if ratio > 0.5:
            common_count = sum(1 for char in text if char in self.COMMON_CHINESE_CHARS)
            common_ratio = common_count / max(total, 1)
            ratio += common_ratio * 0.5

        bad_chars = set(text) & {"?", "\ufffd", "\x00"}
        if bad_chars:
            bad_count = sum(1 for char in text if char in bad_chars)
            bad_ratio = bad_count / total
            ratio -= bad_ratio * 0.5

        return max(0, min(1, ratio))

    def _is_normal_chinese(self, text: str) -> bool:
        """判断是否已经是正常中文"""
        return self._chinese_score(text) > 0.8

    def _is_chinese_char(self, char: str) -> bool:
        """判断是否是中文字符"""
        if len(char) != 1:
            return False
        return 0x4E00 <= ord(char) <= 0x9FFF


def fix_file(input_path: str, output_path: str = None, encoding_hint: str = None, verbose: bool = False):
    """修复文件中的乱码"""
    text = None
    for enc in ["utf-8", "gbk", "gb18030", "latin-1"]:
        try:
            with open(input_path, "r", encoding=enc, errors="ignore") as f:
                text = f.read()
            if verbose:
                print(f"Read file with {enc} encoding")
            break
        except Exception:
            continue

    if text is None:
        print(f"Cannot read file: {input_path}")
        return

    fixer = GarbledFixer(verbose=verbose)
    fixed_text, method = fixer.fix(text, encoding_hint)

    if fixed_text:
        print(f"Fix method: {method}")
        print(f"Before: {text[:50]}...")
        print(f"After: {fixed_text[:50]}...")

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(fixed_text)
            print(f"Saved to: {output_path}")
    else:
        print("Cannot fix this text")


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Chinese garbled text fixer")
    parser.add_argument("input", help="Input text or file path")
    parser.add_argument("--file", action="store_true", help="Input is a file path")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--encoding", "-e", help="Encoding hint (gbk/utf-8/iso8859-1)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed process")

    args = parser.parse_args()

    if args.file:
        fix_file(args.input, args.output, args.encoding, args.verbose)
    else:
        fixer = GarbledFixer(verbose=args.verbose)
        fixed_text, method = fixer.fix(args.input, args.encoding)
        if fixed_text:
            print(f"Fix method: {method}")
            print(f"Fixed: {fixed_text}")
        else:
            print("Cannot fix this text")


if __name__ == "__main__":
    main()
