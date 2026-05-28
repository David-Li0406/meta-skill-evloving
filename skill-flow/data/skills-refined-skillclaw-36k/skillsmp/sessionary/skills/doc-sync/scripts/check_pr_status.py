#!/usr/bin/env python3
"""
현재 브랜치의 PR 상태 확인 및 변경 파일 분석

Usage:
    python3 check_pr_status.py [pr_number]

Output:
    JSON 형식의 PR 상태 및 관련 문서 정보
"""

import json
import subprocess
import sys
from pathlib import Path

# 코드 경로 → 문서 매핑
CODE_TO_DOC_MAPPING = {
    "backend/app/domain/lecture/": "docs/spec/domain/lecture.md",
    "backend/app/domain/session/": "docs/spec/domain/session.md",
    "backend/app/domain/subscription/": "docs/spec/domain/subscription.md",
    "backend/app/domain/folder/": "docs/spec/domain/folder.md",
    "backend/app/infrastructure/video/": "docs/spec/infrastructure/video-streaming.md",
    "backend/app/infrastructure/streaming/": "docs/spec/infrastructure/video-streaming.md",
    "frontend/src/lib/components/VideoPlayer": "docs/spec/frontend/video-player.md",
    "frontend/src/lib/components/video": "docs/spec/frontend/video-player.md",
    "docker-compose": "docs/spec/infrastructure/video-streaming.md",
}


def get_current_branch() -> str:
    """현재 브랜치 이름 가져오기"""
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()


def get_pr_info(pr_number: str | None = None) -> dict | None:
    """PR 정보 가져오기"""
    cmd = ["gh", "pr", "view"]
    if pr_number:
        cmd.append(pr_number)
    cmd.extend(["--json", "state,mergedAt,headRefName,title,number,url"])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError:
        return None


def get_changed_files(pr_number: str | None = None) -> list[str]:
    """PR에서 변경된 파일 목록 가져오기"""
    cmd = ["gh", "pr", "diff"]
    if pr_number:
        cmd.append(pr_number)
    cmd.append("--name-only")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return [f for f in result.stdout.strip().split("\n") if f]
    except subprocess.CalledProcessError:
        return []


def map_files_to_docs(changed_files: list[str]) -> list[dict]:
    """변경된 파일을 관련 문서에 매핑"""
    related_docs = {}

    for file_path in changed_files:
        for code_pattern, doc_path in CODE_TO_DOC_MAPPING.items():
            if code_pattern in file_path:
                if doc_path not in related_docs:
                    related_docs[doc_path] = {
                        "path": doc_path,
                        "related_files": [],
                        "reason": f"{code_pattern} 코드 변경"
                    }
                related_docs[doc_path]["related_files"].append(file_path)

    return list(related_docs.values())


def categorize_files(files: list[str]) -> dict:
    """파일을 카테고리별로 분류"""
    categories = {
        "backend": [],
        "frontend": [],
        "docs": [],
        "config": [],
        "other": []
    }

    for f in files:
        if f.startswith("backend/"):
            categories["backend"].append(f)
        elif f.startswith("frontend/"):
            categories["frontend"].append(f)
        elif f.startswith("docs/"):
            categories["docs"].append(f)
        elif any(f.endswith(ext) for ext in [".json", ".yaml", ".yml", ".toml"]):
            categories["config"].append(f)
        else:
            categories["other"].append(f)

    return {k: v for k, v in categories.items() if v}


def main():
    pr_number = sys.argv[1] if len(sys.argv) > 1 else None

    # 현재 브랜치 정보
    current_branch = get_current_branch()

    # PR 정보 가져오기
    pr_info = get_pr_info(pr_number)

    if not pr_info:
        result = {
            "error": "No PR found for current branch",
            "branch_name": current_branch,
            "is_merged": False
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    # 변경된 파일 목록
    changed_files = get_changed_files(pr_number or str(pr_info.get("number", "")))

    # 파일 카테고리화
    categorized = categorize_files(changed_files)

    # 관련 문서 매핑
    related_docs = map_files_to_docs(changed_files)

    result = {
        "is_merged": pr_info.get("state") == "MERGED",
        "pr_number": pr_info.get("number"),
        "pr_title": pr_info.get("title"),
        "pr_url": pr_info.get("url"),
        "branch_name": pr_info.get("headRefName", current_branch),
        "merged_at": pr_info.get("mergedAt"),
        "changed_files": changed_files,
        "categorized_files": categorized,
        "related_docs": related_docs
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
