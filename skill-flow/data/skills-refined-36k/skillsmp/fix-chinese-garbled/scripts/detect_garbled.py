#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文乱码检测工具
用于检测字符串的中文乱码类型
"""

import re
from typing import Optional, Dict, Any


class GarbledDetector:
    """中文乱码类型检测器"""

    # 乱码特征模式
    PATTERNS = {
        "古文码": {
            "regex": r"[\u4e00-\u9fff]+",
            "common_chars": ["鐢", "辨", "湀", "瑕", "佸", "濂", "藉", "涔", "犲", "澶", "悓"],
            "desc": "以 GBK 方式读取 UTF-8 编码的中文",
            "fix": "gbk_to_utf8"
        },
        "口字码": {
            "regex": r"\uFFFD{2,}",
            "common_chars": ["\uFFFD"],
            "desc": "以 UTF-8 的方式读取 GBK 编码的中文",
            "fix": "utf8_to_gbk"
        },
        "符号码": {
            "common_chars": ["Ã", "¤", "§", "©", "®", "°", "±", "²", "³", "µ"],
            "desc": "以 ISO8859-1 方式读取 UTF-8 编码的中文",
            "fix": "latin1_to_utf8"
        },
        "拼音码": {
            "regex": r"[a-z]+[a\x80-\xff]+",
            "common_chars": ["ä", "ö", "ü", "á", "é", "í", "ó", "ú", "à", "è"],
            "desc": "以 ISO8859-1 方式读取 GBK 编码的中文",
            "fix": "latin1_to_gbk"
        },
        "问句码": {
            "common_chars": ["?"],
            "desc": "以 GBK 方式读取 UTF-8 编码的中文，然后又用 UTF-8 的格式再次读取",
            "fix": "double_encode"
        },
        "锟拷码": {
            "regex": r"锟+拷+",
            "common_chars": ["锟", "斤", "拷"],
            "desc": "以 UTF-8 方式读取 GBK 编码的中文，然后又用 GBK 的格式再次读取",
            "fix": "double_decode"
        },
        "烫烫烫": {
            "regex": r"烫+",
            "common_chars": ["烫"],
            "desc": "VC Debug 模式下，栈内存未初始化",
            "fix": "memory_uninitialized"
        },
        "屯屯屯": {
            "regex": r"屯+",
            "common_chars": ["屯"],
            "desc": "VC Debug 模式下，堆内存未初始化 (0xCD)",
            "fix": "memory_uninitialized"
        }
    }

    def __init__(self):
        self.compile_patterns()

    def compile_patterns(self):
        """编译正则表达式模式"""
        for name, info in self.PATTERNS.items():
            if "regex" in info:
                info["compiled"] = re.compile(info["regex"], re.IGNORECASE)

    def detect(self, text: str) -> Optional[Dict[str, Any]]:
        """
        检测文本的乱码类型

        Args:
            text: 待检测的文本

        Returns:
            包含乱码类型信息的字典
        """
        if not text:
            return None

        # 检查是否是烫烫烫或屯屯屯（最高优先级）
        for name in ["烫烫烫", "屯屯屯"]:
            if text.strip() == name[0] * len(text.strip()):
                return {
                    "type": name,
                    "description": self.PATTERNS[name]["desc"],
                    "fix_method": self.PATTERNS[name]["fix"],
                    "confidence": 1.0
                }

        # 检查锟拷码
        if "锟斤拷" in text or ("锟" in text and "拷" in text):
            return {
                "type": "锟拷码",
                "description": self.PATTERNS["锟拷码"]["desc"],
                "fix_method": self.PATTERNS["锟拷码"]["fix"],
                "confidence": 0.9
            }

        # 检查问句码（奇数长度且结尾有问号）
        if text.endswith("?") and len(text) % 2 == 1:
            return {
                "type": "问句码",
                "description": self.PATTERNS["问句码"]["desc"],
                "fix_method": self.PATTERNS["问句码"]["fix"],
                "confidence": 0.7
            }

        # 检查口字码（大量方块）
        replacement_chars = text.count("\uFFFD")
        total_length = len(text)
        if total_length > 0 and replacement_chars / total_length > 0.5:
            return {
                "type": "口字码",
                "description": self.PATTERNS["口字码"]["desc"],
                "fix_method": self.PATTERNS["口字码"]["fix"],
                "confidence": 0.85
            }

        # 检查古文码（包含不认识的古文字符）
        ancient_score = self._check_ancient_code(text)
        if ancient_score > 0.3:
            return {
                "type": "古文码",
                "description": self.PATTERNS["古文码"]["desc"],
                "fix_method": self.PATTERNS["古文码"]["fix"],
                "confidence": min(ancient_score * 1.5, 1.0)
            }

        # 检查符号码（大量拉丁控制字符）
        symbol_score = self._check_symbol_code(text)
        if symbol_score > 0.2:
            return {
                "type": "符号码",
                "description": self.PATTERNS["符号码"]["desc"],
                "fix_method": self.PATTERNS["符号码"]["fix"],
                "confidence": min(symbol_score * 2, 1.0)
            }

        # 检查拼音码（带声调符号的字母）
        pinyin_score = self._check_pinyin_code(text)
        if pinyin_score > 0.2:
            return {
                "type": "拼音码",
                "description": self.PATTERNS["拼音码"]["desc"],
                "fix_method": self.PATTERNS["拼音码"]["fix"],
                "confidence": min(pinyin_score * 2, 1.0)
            }

        return None

    def _check_ancient_code(self, text: str) -> float:
        """检查是否是古文码"""
        if not text:
            return 0.0
        ancient_chars = self.PATTERNS["古文码"]["common_chars"]
        count = sum(1 for char in text if char in ancient_chars)
        return count / len(text)

    def _check_symbol_code(self, text: str) -> float:
        """检查是否是符号码"""
        if not text:
            return 0.0
        symbol_chars = self.PATTERNS["符号码"]["common_chars"]
        count = sum(1 for char in text if char in symbol_chars)
        return count / len(text)

    def _check_pinyin_code(self, text: str) -> float:
        """检查是否是拼音码"""
        if not text:
            return 0.0
        pinyin_chars = self.PATTERNS["拼音码"]["common_chars"]
        count = sum(1 for char in text if char in pinyin_chars)
        return count / len(text)


def main():
    """命令行入口"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python detect_garbled.py <text>")
        print("       python detect_garbled.py --file <filepath>")
        sys.exit(1)

    detector = GarbledDetector()

    if sys.argv[1] == "--file":
        if len(sys.argv) < 3:
            print("Error: --file requires a filepath argument")
            sys.exit(1)
        with open(sys.argv[2], "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    else:
        text = sys.argv[1]

    result = detector.detect(text)

    if result:
        print(f"Type: {result['type']}")
        print(f"Description: {result['description']}")
        print(f"Fix method: {result['fix_method']}")
        print(f"Confidence: {result['confidence']:.2f}")
    else:
        print("No common Chinese garbled type detected")


if __name__ == "__main__":
    main()
