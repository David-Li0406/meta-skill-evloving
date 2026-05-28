#!/usr/bin/env python3
"""
docs/spec 문서들과 키워드 매칭하여 관련 문서 필터링

Usage:
    python3 filter_related_docs.py '<keywords_json>'

Output:
    JSON 형식의 관련 문서 목록 (매칭 점수 포함)
"""

import json
import os
import re
import sys
from pathlib import Path

# 프로젝트 루트 자동 탐색 (스크립트 위치 기준)
_REPO_ROOT = Path(__file__).resolve()
while _REPO_ROOT != _REPO_ROOT.parent and not (_REPO_ROOT / "docs/spec").exists():
    _REPO_ROOT = _REPO_ROOT.parent
REPO_ROOT = _REPO_ROOT

# 프로젝트 루트 기준 docs/spec 경로
DOCS_SPEC_PATH = REPO_ROOT / "docs/spec"

# 문서별 키워드 매핑 (사전 정의)
DOC_KEYWORDS = {
    "docs/spec/domain/lecture.md": {
        "keywords": ["lecture", "ticket", "접근권한", "강의", "티켓", "차감", "무제한"],
        "category": "domain"
    },
    "docs/spec/domain/session.md": {
        "keywords": ["session", "type", "세션", "타입", "PLAY", "TALK", "JAM", "BASIC", "SHEET"],
        "category": "domain"
    },
    "docs/spec/domain/subscription.md": {
        "keywords": ["subscription", "plan", "구독", "플랜", "Experimental", "Personal", "Group", "Ticket"],
        "category": "domain"
    },
    "docs/spec/domain/folder.md": {
        "keywords": ["folder", "재생목록", "playlist", "폴더"],
        "category": "domain"
    },
    "docs/spec/infrastructure/video-streaming.md": {
        "keywords": ["cloudflare", "minio", "streaming", "video", "signed url", "hls", "스트리밍", "비디오"],
        "category": "infrastructure"
    },
    "docs/spec/frontend/video-player.md": {
        "keywords": ["player", "플레이어", "video", "hls", "컴포넌트"],
        "category": "frontend"
    },
    "docs/spec/design/design-tokens.md": {
        "keywords": ["color", "token", "theme", "색상", "토큰", "디자인", "primary", "브랜드"],
        "category": "design"
    }
}


def extract_headers(file_path: str) -> list[str]:
    """마크다운 파일에서 헤더 추출"""
    try:
        path = Path(file_path)
        if not path.is_absolute():
            path = REPO_ROOT / path
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        headers = re.findall(r"^#{1,3}\s+(.+)$", content, re.MULTILINE)
        return headers
    except FileNotFoundError:
        return []


def calculate_match_score(issue_keywords: dict, doc_info: dict) -> tuple[float, list[str]]:
    """키워드 매칭 점수 계산"""
    doc_keywords_lower = set(k.lower() for k in doc_info["keywords"])
    matched = []

    # Issue의 모든 카테고리 키워드 확인
    for category, keywords in issue_keywords.items():
        if category == "new_concepts":
            continue
        for keyword in keywords:
            if keyword.lower() in doc_keywords_lower:
                matched.append(keyword)

    # 새로운 개념이 문서 카테고리와 관련 있는지 확인
    if "new_concepts" in issue_keywords:
        for concept in issue_keywords["new_concepts"]:
            concept_lower = concept.lower()
            for doc_keyword in doc_info["keywords"]:
                if doc_keyword.lower() in concept_lower or concept_lower in doc_keyword.lower():
                    matched.append(concept)
                    break

    if not doc_info["keywords"]:
        return 0.0, []

    score = len(matched) / len(doc_info["keywords"])
    return score, list(set(matched))


def filter_docs(keywords: dict, threshold: float = 0.2) -> list[dict]:
    """임계값 이상의 매칭 점수를 가진 문서 필터링"""
    results = []

    for doc_path, doc_info in DOC_KEYWORDS.items():
        score, matched = calculate_match_score(keywords, doc_info)

        if score >= threshold:
            headers = extract_headers(doc_path)
            results.append({
                "path": doc_path,
                "score": round(score, 2),
                "matched_keywords": matched,
                "category": doc_info["category"],
                "headers": headers[:10]  # 상위 10개 헤더만
            })

    # 점수 내림차순 정렬
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 filter_related_docs.py '<keywords_json>'", file=sys.stderr)
        sys.exit(1)

    try:
        keywords = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    # 관련 문서 필터링
    related_docs = filter_docs(keywords)

    # 결과 출력
    print(json.dumps(related_docs, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
