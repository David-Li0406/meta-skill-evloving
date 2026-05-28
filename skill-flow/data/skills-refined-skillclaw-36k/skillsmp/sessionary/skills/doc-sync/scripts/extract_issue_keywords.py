#!/usr/bin/env python3
"""
Issue body에서 핵심 키워드/개념 추출

Usage:
    python3 extract_issue_keywords.py <issue_number>

Output:
    JSON 형식의 키워드 목록을 stdout으로 출력
"""

import json
import re
import subprocess
import sys
from collections import defaultdict

# 도메인 키워드 사전
DOMAIN_KEYWORDS = {
    "domain": [
        "lecture", "session", "subscription", "folder", "ticket", "plan",
        "접근권한", "구독", "강의", "세션", "재생목록", "티켓", "플랜",
        "PLAY", "TALK", "JAM", "BASIC", "SHEET",
        "Experimental", "Personal", "Group"
    ],
    "infrastructure": [
        "cloudflare", "minio", "streaming", "video", "signed url", "hls",
        "스트리밍", "비디오", "인프라", "CDN", "storage", "docker"
    ],
    "frontend": [
        "player", "component", "ui", "플레이어", "컴포넌트",
        "svelte", "tailwind", "flowbite"
    ],
    "design": [
        "color", "token", "theme", "색상", "토큰", "디자인",
        "primary", "background", "브랜드"
    ]
}

# 템플릿 텍스트 패턴 (제거 대상)
TEMPLATE_PATTERNS = [
    r"^-\s*\[[ x]\].*$",           # 체크박스
    r"^---+$",                      # 구분선
    r"^#+\s*$",                     # 빈 헤더
    r"^\*\*주의\*\*.*$",            # 주의사항 템플릿
    r"^>\s*\[!.*\].*$",            # 콜아웃
    r"^<!--.*-->$",                 # HTML 주석
]


def get_issue_content(issue_number: int) -> dict:
    """gh CLI로 Issue 내용 가져오기"""
    try:
        result = subprocess.run(
            ["gh", "issue", "view", str(issue_number), "--json", "title,body,labels"],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except FileNotFoundError:
        print("gh CLI를 찾을 수 없습니다. GitHub CLI 설치 및 인증 상태를 확인해 주세요.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error fetching issue: {e.stderr}", file=sys.stderr)
        sys.exit(1)


def clean_text(text: str) -> str:
    """템플릿 텍스트 및 불필요한 요소 제거"""
    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        skip = False
        for pattern in TEMPLATE_PATTERNS:
            if re.match(pattern, line.strip()):
                skip = True
                break
        if not skip:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def extract_keywords(text: str) -> dict:
    """텍스트에서 키워드 추출"""
    text_lower = text.lower()
    result = defaultdict(list)

    # 카테고리별 키워드 매칭
    for category, keywords in DOMAIN_KEYWORDS.items():
        for keyword in keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in text_lower:
                if keyword not in result[category]:
                    result[category].append(keyword)

    # 새로운 개념 추출 (백틱으로 감싸진 용어)
    new_concepts = re.findall(r"`([^`]+)`", text)
    # 기존 키워드에 없는 것만 추가
    all_known = set()
    for keywords in DOMAIN_KEYWORDS.values():
        all_known.update(k.lower() for k in keywords)

    result["new_concepts"] = [
        c for c in new_concepts
        if c.lower() not in all_known and len(c) > 2
    ]

    return dict(result)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_issue_keywords.py <issue_number>", file=sys.stderr)
        sys.exit(1)

    try:
        issue_number = int(sys.argv[1])
    except ValueError:
        print("issue_number는 정수여야 합니다.", file=sys.stderr)
        sys.exit(1)

    # Issue 내용 가져오기
    issue_data = get_issue_content(issue_number)

    # 텍스트 정제
    title = issue_data.get("title", "")
    body = issue_data.get("body", "")
    combined_text = f"{title}\n{body}"
    cleaned_text = clean_text(combined_text)

    # 키워드 추출
    keywords = extract_keywords(cleaned_text)

    # 결과 출력
    print(json.dumps(keywords, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
