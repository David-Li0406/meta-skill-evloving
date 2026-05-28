#!/usr/bin/env python3
"""
Event Storming Mermaid Diagram Generator

이벤트 스토밍 구성요소 JSON을 받아 Mermaid flowchart를 생성합니다.

Usage:
    echo '{"title": "...", ...}' | python3 generate_mermaid.py
    python3 generate_mermaid.py < input.json
    python3 generate_mermaid.py --png < input.json
    python3 generate_mermaid.py --output-dir ./diagrams < input.json
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


# 구성요소별 Mermaid 노드 형태 및 스타일
# Note: {{{{ 는 Python format()에서 리터럴 {{ 로 변환됨 (hexagon)
#       {{ 는 Python format()에서 리터럴 { 로 변환됨 (rhombus)
COMPONENT_STYLES = {
    "actor": {
        "node_format": '{{{{"{name}"}}}}',  # hexagon (double braces in mermaid)
        "class": "actor",
        "fill": "#fef9c3",
        "stroke": "#ca8a04",
    },
    "command": {
        "node_format": '["{name}"]',  # rectangle
        "class": "command",
        "fill": "#93c5fd",
        "stroke": "#2563eb",
    },
    "system": {
        "node_format": '(["{name}"])',  # stadium
        "class": "system",
        "fill": "#fbcfe8",
        "stroke": "#db2777",
    },
    "domain_event": {
        "node_format": '(("{name}"))',  # circle
        "class": "event",
        "fill": "#fed7aa",
        "stroke": "#ea580c",
    },
    "policy": {
        "node_format": '{{"{name}"}}',  # rhombus (single braces in mermaid)
        "class": "policy",
        "fill": "#d8b4fe",
        "stroke": "#9333ea",
    },
    "query_model": {
        "node_format": '[/"{name}"/]',  # parallelogram
        "class": "query",
        "fill": "#bbf7d0",
        "stroke": "#16a34a",
    },
    "constraint": {
        "node_format": '[["{name}"]]',  # subroutine
        "class": "constraint",
        "fill": "#fef08a",
        "stroke": "#ca8a04",
    },
    "hotspot": {
        "node_format": '(((("{name}"))))',  # double circle
        "class": "hotspot",
        "fill": "#fecaca",
        "stroke": "#dc2626",
    },
}

# 연결 라벨 기본값
DEFAULT_LABELS = {
    ("actor", "command"): "Decides to",
    ("command", "system"): "Invoked On",
    ("system", "domain_event"): "Produces",
    ("domain_event", "policy"): "Activates",
    ("policy", "command"): "Issues",
    ("domain_event", "query_model"): "Results in",
    ("query_model", "actor"): "observes",
    ("constraint", "command"): "guards",
}


def sanitize_filename(title: str) -> str:
    """파일명으로 사용 가능한 문자열로 변환"""
    sanitized = title.replace(" ", "_")
    sanitized = re.sub(r'[<>:"/\\|?*]', "", sanitized)
    return sanitized


def sanitize_node_name(name: str) -> str:
    """Mermaid 노드 이름에서 특수문자 이스케이프"""
    # 따옴표 이스케이프
    return name.replace('"', '\\"')


def generate_classdefs() -> list[str]:
    """Mermaid classDef 스타일 정의 생성"""
    lines = ["%% 스타일 정의"]
    for comp_type, style in COMPONENT_STYLES.items():
        class_name = style["class"]
        fill = style["fill"]
        stroke = style["stroke"]
        lines.append(f"classDef {class_name} fill:{fill},stroke:{stroke}")
    return lines


def generate_nodes(components: list[dict]) -> list[str]:
    """구성요소별 Mermaid 노드 생성"""
    lines = ["%% 노드 정의"]

    for comp in components:
        comp_id = comp["id"]
        comp_name = sanitize_node_name(comp["name"])
        comp_type = comp["type"]

        style = COMPONENT_STYLES.get(comp_type, COMPONENT_STYLES["command"])
        node_format = style["node_format"].format(name=comp_name)
        class_name = style["class"]

        lines.append(f"{comp_id}{node_format}:::{class_name}")

    return lines


def generate_connections(connections: list[dict], comp_types: dict[str, str]) -> list[str]:
    """연결 화살표 생성"""
    lines = ["%% 연결"]

    for conn in connections:
        from_id = conn["from"]
        to_id = conn["to"]

        # 라벨 결정
        label = conn.get("label")
        if not label:
            from_type = comp_types.get(from_id, "command")
            to_type = comp_types.get(to_id, "command")
            label = DEFAULT_LABELS.get((from_type, to_type), "")

        if label:
            lines.append(f"{from_id} -->|{label}| {to_id}")
        else:
            lines.append(f"{from_id} --> {to_id}")

    return lines


def generate_mermaid(data: dict) -> str:
    """Mermaid flowchart 코드 생성"""
    components = data.get("components", [])
    connections = data.get("connections", [])

    # 구성요소 ID -> 타입 매핑
    comp_types = {c["id"]: c["type"] for c in components}

    lines = ["flowchart LR"]

    # classDef 스타일 추가
    lines.extend(generate_classdefs())
    lines.append("")

    # 노드 정의
    lines.extend(generate_nodes(components))
    lines.append("")

    # 연결 정의
    lines.extend(generate_connections(connections, comp_types))

    return "\n    ".join(lines)


def generate_markdown(title: str, mermaid_code: str) -> str:
    """Markdown 파일 내용 생성 (Mermaid 코드블록 포함)"""
    return f"""# {title}

```mermaid
{mermaid_code}
```
"""


def convert_to_png(mmd_path: Path, png_path: Path) -> bool:
    """mermaid-cli를 사용하여 PNG로 변환"""
    try:
        result = subprocess.run(
            ["npx", "-p", "@mermaid-js/mermaid-cli", "mmdc", "-i", str(mmd_path), "-o", str(png_path)],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return True
        else:
            print(f"PNG conversion failed: {result.stderr}", file=sys.stderr)
            return False
    except FileNotFoundError:
        print("Error: npx not found. Install Node.js to enable PNG conversion.", file=sys.stderr)
        return False
    except subprocess.TimeoutExpired:
        print("Error: PNG conversion timed out.", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Event Storming Mermaid Diagram Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  echo '{"title": "주문 처리", ...}' | python3 generate_mermaid.py

  python3 generate_mermaid.py --png < input.json

  python3 generate_mermaid.py --output-dir ./diagrams < input.json
        """
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default=".",
        help="출력 디렉토리 (기본값: 현재 디렉토리)"
    )
    parser.add_argument(
        "--png",
        action="store_true",
        help="PNG 이미지도 생성 (mermaid-cli 필요)"
    )

    args = parser.parse_args()

    # stdin에서 JSON 읽기
    try:
        input_data = sys.stdin.read()
        if not input_data.strip():
            print("Error: No input provided. Pipe JSON data to stdin.", file=sys.stderr)
            sys.exit(1)

        data = json.loads(input_data)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input - {e}", file=sys.stderr)
        sys.exit(1)

    # 필수 필드 검증
    required = ["title", "components"]
    for field in required:
        if field not in data:
            print(f"Error: Missing required field '{field}'", file=sys.stderr)
            sys.exit(1)

    # Mermaid 코드 생성
    title = data["title"]
    mermaid_code = generate_mermaid(data)
    markdown_content = generate_markdown(title, mermaid_code)

    # 출력 디렉토리 생성
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 파일명 생성
    safe_title = sanitize_filename(title)
    md_path = output_dir / f"{safe_title}.md"

    # Markdown 파일 저장
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"Generated: {md_path}")

    # PNG 변환 (옵션)
    if args.png:
        # 임시 .mmd 파일 생성
        mmd_path = output_dir / f"{safe_title}.mmd"
        with open(mmd_path, "w", encoding="utf-8") as f:
            f.write(mermaid_code)

        png_path = output_dir / f"{safe_title}.png"
        if convert_to_png(mmd_path, png_path):
            print(f"Generated: {png_path}")
            # 임시 .mmd 파일 삭제
            mmd_path.unlink()
        else:
            print(f"Note: .mmd file kept at {mmd_path} for manual conversion")


if __name__ == "__main__":
    main()
