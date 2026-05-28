#!/usr/bin/env python3
"""
GitHub 오픈소스 검색 스크립트

Usage:
    python github_search.py "search query" [--min-stars 500] [--license MIT,Apache-2.0]
    python github_search.py --analyze "feature name"
"""

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Repository:
    name: str
    full_name: str
    description: str
    stars: int
    license: str
    language: str
    updated_at: str
    url: str
    open_issues: int


def run_gh_command(args: list) -> dict | list | None:
    """GitHub CLI 명령 실행"""
    try:
        result = subprocess.run(
            ["gh", *args], capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout) if result.stdout else None
    except subprocess.CalledProcessError as e:
        print(f"❌ GitHub CLI 오류: {e.stderr}")
        return None
    except json.JSONDecodeError:
        return None


def search_repositories(
    query: str, min_stars: int = 500, licenses: list = None
) -> list[Repository]:
    """GitHub 저장소 검색"""
    search_query = f"{query} stars:>={min_stars}"

    if licenses:
        license_query = " ".join([f"license:{lic}" for lic in licenses])
        search_query = f"{search_query} {license_query}"

    args = [
        "search",
        "repos",
        search_query,
        "--sort",
        "stars",
        "--order",
        "desc",
        "--limit",
        "20",
        "--json",
        "name,fullName,description,stargazersCount,licenseInfo,primaryLanguage,updatedAt,url,openIssues",
    ]

    results = run_gh_command(args)
    if not results:
        return []

    repos = []
    for r in results:
        license_name = (
            r.get("licenseInfo", {}).get("name", "Unknown")
            if r.get("licenseInfo")
            else "Unknown"
        )
        language = (
            r.get("primaryLanguage", {}).get("name", "Unknown")
            if r.get("primaryLanguage")
            else "Unknown"
        )

        repos.append(
            Repository(
                name=r.get("name", ""),
                full_name=r.get("fullName", ""),
                description=(
                    r.get("description", "")[:100] if r.get("description") else ""
                ),
                stars=r.get("stargazersCount", 0),
                license=license_name,
                language=language,
                updated_at=r.get("updatedAt", ""),
                url=r.get("url", ""),
                open_issues=r.get("openIssues", 0),
            )
        )

    return repos


def evaluate_repository(repo: Repository) -> dict:
    """저장소 평가"""
    score = 0
    notes = []

    # Stars 평가
    if repo.stars >= 10000:
        score += 30
        notes.append("⭐ 매우 인기 (10k+)")
    elif repo.stars >= 5000:
        score += 25
        notes.append("⭐ 인기 (5k+)")
    elif repo.stars >= 1000:
        score += 20
        notes.append("⭐ 활성 (1k+)")
    else:
        score += 10

    # 라이선스 평가
    allowed_licenses = [
        "MIT License",
        "Apache License 2.0",
        "BSD 3-Clause",
        "BSD 2-Clause",
    ]
    if any(lic in repo.license for lic in allowed_licenses):
        score += 25
        notes.append(f"✅ 허용 라이선스 ({repo.license})")
    else:
        score += 5
        notes.append(f"⚠️ 라이선스 확인 필요 ({repo.license})")

    # 최근 업데이트 평가
    try:
        updated = datetime.fromisoformat(repo.updated_at.replace("Z", "+00:00"))
        days_ago = (datetime.now(updated.tzinfo) - updated).days

        if days_ago <= 30:
            score += 25
            notes.append("🔄 최근 업데이트 (30일 이내)")
        elif days_ago <= 180:
            score += 20
            notes.append("🔄 활성 유지보수 (6개월 이내)")
        elif days_ago <= 365:
            score += 10
            notes.append("⚠️ 업데이트 확인 필요 (1년 이내)")
        else:
            notes.append("❌ 비활성 (1년 이상)")
    except Exception:
        notes.append("⚠️ 업데이트 날짜 확인 불가")

    # 이슈 수 평가
    if repo.open_issues < 50:
        score += 10
        notes.append("📋 이슈 관리 양호")
    elif repo.open_issues < 200:
        score += 5
        notes.append("📋 이슈 보통")
    else:
        notes.append("⚠️ 이슈 많음")

    return {
        "score": score,
        "grade": (
            "A" if score >= 80 else "B" if score >= 60 else "C" if score >= 40 else "D"
        ),
        "notes": notes,
    }


def print_results(repos: list[Repository]):
    """검색 결과 출력"""
    if not repos:
        print("❌ 검색 결과가 없습니다.")
        return

    print("\n" + "=" * 80)
    print("📦 오픈소스 검색 결과")
    print("=" * 80)

    for i, repo in enumerate(repos[:10], 1):
        eval_result = evaluate_repository(repo)

        print(f"\n### {i}. {repo.full_name}")
        print(
            f"   ⭐ Stars: {repo.stars:,} | 📜 License: {repo.license} | 💻 {repo.language}"
        )
        print(f"   📝 {repo.description}")
        print(f"   🔗 {repo.url}")
        print(f"   📊 평가: {eval_result['grade']} ({eval_result['score']}점)")
        for note in eval_result["notes"]:
            print(f"      {note}")

    print("\n" + "=" * 80)

    # 권장사항
    top_repos = sorted(
        repos[:10], key=lambda r: evaluate_repository(r)["score"], reverse=True
    )
    if top_repos:
        best = top_repos[0]
        eval_best = evaluate_repository(best)
        print(f"\n💡 권장: {best.full_name} (평가: {eval_best['grade']})")
        print(f"   이유: Stars {best.stars:,}, {best.license}, 활성 유지보수")


def generate_analysis_template(feature_name: str):
    """Make vs Buy 분석 템플릿 생성"""
    template = f"""
## Make vs Buy 분석: {feature_name}

### Option A: 직접 개발 (Make)
- **예상 시간**: [X]일
- **복잡도**: [높음/중간/낮음]
- **장점**:
  - 커스터마이징 자유
  - 외부 의존성 없음
  - 보안 완전 통제
- **단점**:
  - 개발 시간 소요
  - 유지보수 부담
  - 버그 위험

### Option B: 오픈소스 활용 (Buy)
- **후보**: [라이브러리명] (Stars: X, License: MIT)
- **통합 시간**: [X]일
- **장점**:
  - 검증된 솔루션
  - 커뮤니티 지원
  - 빠른 도입
- **단점**:
  - 의존성 추가
  - 커스터마이징 제한
  - 버전 호환성 관리

### 평가 기준

| 기준 | Make | Buy |
|------|------|-----|
| 개발 시간 | [ ]일 | [ ]일 |
| 유지보수 비용 | 높음/낮음 | 높음/낮음 |
| 커스터마이징 | 완전 | 제한적 |
| 리스크 | 높음/낮음 | 높음/낮음 |

### 권장사항

**[Make / Buy]** 권장

**이유**:
1. [구체적 근거 1]
2. [구체적 근거 2]
3. [구체적 근거 3]

---

**승인 필요**: 위 분석 결과를 검토하고 진행 방향을 결정해 주세요.
"""
    print(template)


def main():
    parser = argparse.ArgumentParser(description="GitHub 오픈소스 검색")
    parser.add_argument("query", nargs="?", help="검색 쿼리")
    parser.add_argument(
        "--min-stars", type=int, default=500, help="최소 Stars 수 (기본: 500)"
    )
    parser.add_argument("--license", type=str, help="라이선스 필터 (콤마 구분)")
    parser.add_argument("--analyze", type=str, help="Make vs Buy 분석 템플릿 생성")

    args = parser.parse_args()

    if args.analyze:
        generate_analysis_template(args.analyze)
        return

    if not args.query:
        parser.print_help()
        return

    licenses = args.license.split(",") if args.license else None

    print(f"🔍 검색 중: {args.query}")
    print(f"   최소 Stars: {args.min_stars}")
    if licenses:
        print(f"   라이선스: {', '.join(licenses)}")

    repos = search_repositories(args.query, args.min_stars, licenses)
    print_results(repos)


if __name__ == "__main__":
    main()
