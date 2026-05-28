#!/usr/bin/env python3
"""
Base64 编解码工具
支持编码/解码文本、JSON、二进制文件，自动检测格式
"""

import sys
import json
import base64
import argparse
import os
from typing import Dict, Any, Optional, Tuple

# 文件类型 magic bytes
MAGIC_BYTES = {
    b'\x89PNG\r\n\x1a\n': 'image/png',
    b'\xff\xd8\xff': 'image/jpeg',
    b'GIF87a': 'image/gif',
    b'GIF89a': 'image/gif',
    b'%PDF': 'application/pdf',
    b'PK\x03\x04': 'application/zip',
    b'\x1f\x8b': 'application/gzip',
}


def detect_content_type(data: bytes) -> Tuple[str, str]:
    """
    检测内容类型

    Returns:
        (type, mime_type) - 如 ('image', 'image/png') 或 ('text', 'text/plain')
    """
    # 检查 magic bytes
    for magic, mime in MAGIC_BYTES.items():
        if data.startswith(magic):
            category = mime.split('/')[0]
            return (category, mime)

    # 尝试解析为 UTF-8 文本
    try:
        text = data.decode('utf-8')
        # 尝试解析为 JSON
        try:
            json.loads(text)
            return ('json', 'application/json')
        except json.JSONDecodeError:
            return ('text', 'text/plain')
    except UnicodeDecodeError:
        return ('binary', 'application/octet-stream')


def normalize_base64(b64_string: str) -> str:
    """标准化 Base64 字符串（处理 URL 安全格式和 padding）"""
    # 移除空白字符
    b64_string = ''.join(b64_string.split())

    # URL 安全格式转换
    if '-' in b64_string or '_' in b64_string:
        b64_string = b64_string.replace('-', '+').replace('_', '/')

    # 补齐 padding
    padding = len(b64_string) % 4
    if padding:
        b64_string += '=' * (4 - padding)

    return b64_string


def decode_base64(b64_string: str, output_file: Optional[str] = None,
                  force_binary: bool = False) -> Dict[str, Any]:
    """解码 Base64 字符串"""
    try:
        normalized = normalize_base64(b64_string)
        decoded_bytes = base64.b64decode(normalized)

        content_type, mime_type = detect_content_type(decoded_bytes)

        result = {
            "success": True,
            "operation": "decode",
            "input_length": len(b64_string),
            "type": content_type,
            "mime_type": mime_type,
            "raw_size": len(decoded_bytes),
        }

        # 处理输出
        if output_file:
            with open(output_file, 'wb') as f:
                f.write(decoded_bytes)
            result["output_file"] = output_file
            result["message"] = f"Decoded and saved to {output_file}"
        elif content_type == 'json':
            text = decoded_bytes.decode('utf-8')
            result["content"] = json.loads(text)
            result["raw_string"] = text
            result["message"] = "Successfully decoded as JSON"
        elif content_type == 'text' and not force_binary:
            text = decoded_bytes.decode('utf-8')
            result["content"] = text
            result["message"] = "Successfully decoded as text"
        else:
            # 二进制数据，返回十六进制预览
            result["hex_preview"] = decoded_bytes[:64].hex()
            result["message"] = f"Binary data ({mime_type}), use --output to save"

        return result

    except Exception as e:
        return {
            "success": False,
            "operation": "decode",
            "error": str(e),
            "message": f"Failed to decode: {str(e)}"
        }


def encode_base64(data: str, file_path: Optional[str] = None,
                  url_safe: bool = False) -> Dict[str, Any]:
    """编码为 Base64"""
    try:
        if file_path:
            with open(file_path, 'rb') as f:
                raw_bytes = f.read()
            source = f"file:{file_path}"
        else:
            raw_bytes = data.encode('utf-8')
            source = "text"

        if url_safe:
            encoded = base64.urlsafe_b64encode(raw_bytes).decode('ascii')
        else:
            encoded = base64.b64encode(raw_bytes).decode('ascii')

        return {
            "success": True,
            "operation": "encode",
            "source": source,
            "input_size": len(raw_bytes),
            "output_length": len(encoded),
            "url_safe": url_safe,
            "encoded": encoded,
            "message": "Successfully encoded to Base64"
        }

    except Exception as e:
        return {
            "success": False,
            "operation": "encode",
            "error": str(e),
            "message": f"Failed to encode: {str(e)}"
        }


def detect_type(b64_string: str) -> Dict[str, Any]:
    """检测 Base64 内容类型"""
    try:
        normalized = normalize_base64(b64_string)
        decoded_bytes = base64.b64decode(normalized)

        content_type, mime_type = detect_content_type(decoded_bytes)

        result = {
            "success": True,
            "operation": "detect",
            "type": content_type,
            "mime_type": mime_type,
            "size": len(decoded_bytes),
        }

        # 如果是 JSON 或文本，包含内容预览
        if content_type == 'json':
            text = decoded_bytes.decode('utf-8')
            result["content"] = json.loads(text)
        elif content_type == 'text':
            text = decoded_bytes.decode('utf-8')
            result["preview"] = text[:200] + ('...' if len(text) > 200 else '')
        else:
            result["hex_preview"] = decoded_bytes[:32].hex()

        return result

    except Exception as e:
        return {
            "success": False,
            "operation": "detect",
            "error": str(e),
            "message": f"Failed to detect: {str(e)}"
        }


def batch_decode(input_file: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """批量解码（每行一个 Base64）"""
    results = []

    try:
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        for i, line in enumerate(lines):
            if output_dir:
                # 根据检测的类型决定扩展名
                detect_result = detect_type(line)
                ext = {
                    'json': '.json',
                    'text': '.txt',
                    'image/png': '.png',
                    'image/jpeg': '.jpg',
                    'image/gif': '.gif',
                    'application/pdf': '.pdf',
                }.get(detect_result.get('mime_type', ''), '.bin')

                output_file = os.path.join(output_dir, f"item_{i}{ext}")
                result = decode_base64(line, output_file=output_file)
            else:
                result = decode_base64(line)

            result["index"] = i
            results.append(result)

        success_count = sum(1 for r in results if r["success"])

        return {
            "success": True,
            "operation": "batch",
            "total": len(results),
            "succeeded": success_count,
            "failed": len(results) - success_count,
            "results": results,
            "message": f"Processed {len(results)} items, {success_count} succeeded"
        }

    except Exception as e:
        return {
            "success": False,
            "operation": "batch",
            "error": str(e),
            "message": f"Batch processing failed: {str(e)}"
        }


def format_output(result: Dict[str, Any], pretty: bool = False) -> str:
    """格式化输出结果"""
    if pretty and result.get("success"):
        lines = []
        lines.append(f"✅ {result.get('message', 'Success')}")
        lines.append("")

        op = result.get("operation", "")

        if op == "decode":
            lines.append(f"📊 类型: {result.get('type')} ({result.get('mime_type', 'unknown')})")
            lines.append(f"📏 大小: {result.get('raw_size', 0)} bytes")
            lines.append("")

            content = result.get("content")
            if content is not None:
                lines.append("📄 解码内容:")
                lines.append("-" * 50)
                if result.get("type") == "json":
                    lines.append(json.dumps(content, indent=2, ensure_ascii=False))
                else:
                    lines.append(str(content))
                lines.append("-" * 50)

            if result.get("output_file"):
                lines.append(f"💾 已保存到: {result.get('output_file')}")

            if result.get("hex_preview"):
                lines.append(f"🔢 十六进制预览: {result.get('hex_preview')}")

        elif op == "encode":
            lines.append(f"📥 输入: {result.get('source')} ({result.get('input_size')} bytes)")
            lines.append(f"📤 输出长度: {result.get('output_length')} 字符")
            if result.get("url_safe"):
                lines.append("🔗 URL 安全格式")
            lines.append("")
            lines.append("📄 编码结果:")
            lines.append("-" * 50)
            lines.append(result.get("encoded", ""))
            lines.append("-" * 50)

        elif op == "detect":
            lines.append(f"📊 类型: {result.get('type')} ({result.get('mime_type', 'unknown')})")
            lines.append(f"📏 大小: {result.get('size', 0)} bytes")

            content = result.get("content")
            preview = result.get("preview")

            if content is not None:
                lines.append("")
                lines.append("📄 内容:")
                lines.append("-" * 50)
                if isinstance(content, dict) or isinstance(content, list):
                    lines.append(json.dumps(content, indent=2, ensure_ascii=False))
                else:
                    lines.append(str(content))
                lines.append("-" * 50)
            elif preview:
                lines.append("")
                lines.append(f"📄 预览: {preview}")

            if result.get("hex_preview"):
                lines.append(f"🔢 十六进制: {result.get('hex_preview')}")

        elif op == "batch":
            lines.append(f"📊 处理统计:")
            lines.append(f"   总数: {result.get('total', 0)}")
            lines.append(f"   成功: {result.get('succeeded', 0)}")
            lines.append(f"   失败: {result.get('failed', 0)}")

        return "\n".join(lines)
    else:
        return json.dumps(result, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description='Base64 编解码工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  decode:  python3 base64_tool.py decode "SGVsbG8gV29ybGQ="
  encode:  python3 base64_tool.py encode "Hello World"
  encode file: python3 base64_tool.py encode --file image.png
  detect:  python3 base64_tool.py detect "eyJ0ZXN0IjogMX0="
  batch:   python3 base64_tool.py batch --file input.txt --output-dir ./decoded/

输出格式:
  默认输出 JSON 格式，使用 --pretty/-p 输出人类友好的格式
        """
    )

    parser.add_argument('--pretty', '-p', action='store_true', help='人类友好的输出格式')

    subparsers = parser.add_subparsers(dest='command', help='操作类型')

    # decode 子命令
    decode_parser = subparsers.add_parser('decode', help='解码 Base64')
    decode_parser.add_argument('base64_string', nargs='?', help='Base64 字符串')
    decode_parser.add_argument('--file', '-f', help='从文件读取 Base64')
    decode_parser.add_argument('--output', '-o', help='输出文件路径')
    decode_parser.add_argument('--binary', '-b', action='store_true', help='强制二进制模式')

    # encode 子命令
    encode_parser = subparsers.add_parser('encode', help='编码为 Base64')
    encode_parser.add_argument('text', nargs='?', help='要编码的文本')
    encode_parser.add_argument('--file', '-f', help='要编码的文件')
    encode_parser.add_argument('--url-safe', '-u', action='store_true', help='URL 安全编码')

    # detect 子命令
    detect_parser = subparsers.add_parser('detect', help='检测 Base64 内容类型')
    detect_parser.add_argument('base64_string', help='Base64 字符串')

    # batch 子命令
    batch_parser = subparsers.add_parser('batch', help='批量解码')
    batch_parser.add_argument('--file', '-f', required=True, help='输入文件（每行一个 Base64）')
    batch_parser.add_argument('--output-dir', '-o', help='输出目录')

    args = parser.parse_args()

    if not args.command:
        # 兼容旧版本：无子命令时默认为 decode
        if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
            result = decode_base64(sys.argv[1])
        else:
            parser.print_help()
            sys.exit(1)
    elif args.command == 'decode':
        b64_input = args.base64_string
        if args.file:
            with open(args.file, 'r') as f:
                b64_input = f.read().strip()
        elif not b64_input:
            b64_input = sys.stdin.read().strip()

        result = decode_base64(b64_input, output_file=args.output, force_binary=args.binary)

    elif args.command == 'encode':
        result = encode_base64(args.text or '', file_path=args.file, url_safe=args.url_safe)

    elif args.command == 'detect':
        result = detect_type(args.base64_string)

    elif args.command == 'batch':
        result = batch_decode(args.file, output_dir=args.output_dir)

    print(format_output(result, pretty=args.pretty if hasattr(args, 'pretty') else False))


if __name__ == "__main__":
    main()
