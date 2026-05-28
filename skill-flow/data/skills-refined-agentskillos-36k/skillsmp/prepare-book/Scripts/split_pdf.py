#!/usr/bin/env python3
"""
PDF Splitter by TOC (Table of Contents)
목차 기반으로 PDF를 챕터별로 분할합니다.
"""

import sys
import re
import argparse
from pathlib import Path
import pymupdf


def sanitize_filename(name: str) -> str:
    """파일명에 사용할 수 없는 문자를 제거/치환합니다."""
    # 파일명에 사용 불가능한 문자들
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', name)
    # 연속된 공백을 하나로
    sanitized = re.sub(r'\s+', ' ', sanitized)
    # 앞뒤 공백 제거
    return sanitized.strip()


def get_split_items(toc: list, max_level: int, total_pages: int) -> list:
    """분할할 항목들을 반환합니다.

    max_level까지 고려하여, 각 섹션에서 가능한 가장 세부적인 레벨로 분할합니다.
    하위 레벨이 있는 항목은 건너뛰고, 하위 항목들을 대신 사용합니다.
    """
    n = len(toc)

    # 각 항목이 max_level 이하의 하위 항목을 가지는지 표시
    has_children = [False] * n
    for i in range(n):
        current_level = toc[i][0]
        if current_level >= max_level:
            continue
        # 다음 항목들 중 하위 레벨이면서 max_level 이하인 항목이 있는지 확인
        for j in range(i + 1, n):
            next_level = toc[j][0]
            if next_level <= current_level:
                break
            if next_level <= max_level:
                has_children[i] = True
                break

    # 분할 항목 선택 및 페이지 범위 계산
    split_items = []
    for i in range(n):
        level, title, start_page = toc[i]
        if level > max_level:
            continue
        if has_children[i]:
            continue

        # 끝 페이지 계산: 같은 레벨 또는 상위 레벨의 다음 항목 찾기
        # (페이지 번호가 현재 항목보다 큰 경우만 유효)
        end_page = total_pages
        for j in range(i + 1, n):
            next_level = toc[j][0]
            next_page = toc[j][2]
            if next_level <= level and next_page > start_page:
                end_page = next_page - 1
                break

        split_items.append({
            'level': level,
            'title': title,
            'start_page': start_page,
            'end_page': end_page
        })

    return split_items


def split_pdf_by_toc(pdf_path: str, max_level: int = 1) -> None:
    """PDF를 목차(TOC) 기준으로 분할합니다."""
    pdf_path = Path(pdf_path).resolve()

    if not pdf_path.exists():
        print(f"오류: 파일을 찾을 수 없습니다: {pdf_path}")
        sys.exit(1)

    if not pdf_path.suffix.lower() == '.pdf':
        print(f"오류: PDF 파일이 아닙니다: {pdf_path}")
        sys.exit(1)

    # PDF 열기
    doc = pymupdf.open(pdf_path)
    total_pages = doc.page_count

    # 목차 추출
    toc = doc.get_toc()

    if not toc:
        print("오류: 이 PDF에는 목차(TOC)가 없습니다.")
        doc.close()
        sys.exit(1)

    # 분할 항목 계산
    split_items_raw = get_split_items(toc, max_level, total_pages)

    if not split_items_raw:
        print(f"오류: Level {max_level} 이하의 목차 항목이 없습니다.")
        doc.close()
        sys.exit(1)

    # 페이지 번호가 순차적으로 증가하는 항목만 필터링
    split_items = []
    last_page = 0
    skipped = []
    for item in split_items_raw:
        if item['start_page'] >= last_page:
            split_items.append(item)
            last_page = item['start_page']
        else:
            skipped.append(item['title'])

    print(f"PDF: {pdf_path.name}")
    print(f"총 페이지: {total_pages}")
    print(f"분할 기준: Level {max_level} 이하")
    print(f"분할 항목: {len(split_items)}개")
    if skipped:
        print(f"제외된 항목 (잘못된 페이지 참조): {', '.join(skipped)}")
    print("-" * 50)

    # 출력 폴더 생성 (PDF 파일명과 동일)
    output_dir = pdf_path.parent / pdf_path.stem
    output_dir.mkdir(exist_ok=True)

    # 각 챕터별로 분할
    for i, item in enumerate(split_items):
        # 페이지 번호는 1-based, PyMuPDF는 0-based
        start_page = item['start_page'] - 1
        end_page = item['end_page'] - 1

        # 유효성 검사
        if start_page < 0:
            start_page = 0
        if end_page >= total_pages:
            end_page = total_pages - 1
        if start_page > end_page:
            print(f"  건너뜀: {item['title']} (잘못된 페이지 범위)")
            continue

        # 파일명 생성
        safe_title = sanitize_filename(item['title'])
        output_filename = f"{i + 1}. {safe_title}.pdf"
        output_path = output_dir / output_filename

        # 새 PDF 생성
        new_doc = pymupdf.open()
        new_doc.insert_pdf(doc, from_page=start_page, to_page=end_page)
        new_doc.save(output_path)
        new_doc.close()

        page_count = end_page - start_page + 1
        print(f"  생성: {output_filename} (페이지 {start_page + 1}-{end_page + 1}, {page_count}페이지)")

    doc.close()

    print("-" * 50)
    print(f"완료! 출력 폴더: {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description='PDF 파일을 목차(TOC) 기준으로 분할합니다.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python split_pdf.py "book.pdf"                 # Level 1 기준 분할 (기본)
  python split_pdf.py --level 2 "book.pdf"       # Level 2 기준 분할
        """
    )
    parser.add_argument('pdf_path', help='PDF 파일 경로')
    parser.add_argument('--level', type=int, default=1,
                        help='분할 기준 레벨 (기본: 1)')

    args = parser.parse_args()
    split_pdf_by_toc(args.pdf_path, args.level)


if __name__ == "__main__":
    main()
