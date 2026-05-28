#!/usr/bin/env python3
"""
PDF TOC Checker
PDF의 목차(TOC) 구조를 분석하고 JSON으로 저장합니다.
"""

import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
import pymupdf


def calculate_characters(doc, start_page: int, end_page: int) -> int:
    """주어진 페이지 범위의 텍스트 문자 수를 계산합니다.

    Args:
        doc: pymupdf Document 객체
        start_page: 시작 페이지 (1-based)
        end_page: 끝 페이지 (1-based)

    Returns:
        해당 페이지 범위의 총 문자 수
    """
    total_chars = 0
    # pymupdf는 0-based 인덱스 사용
    for page_num in range(start_page - 1, end_page):
        if 0 <= page_num < doc.page_count:
            page = doc[page_num]
            text = page.get_text()
            total_chars += len(text)
    return total_chars


def calculate_page_ranges(toc: list, total_pages: int, doc=None) -> list:
    """각 TOC 항목의 페이지 범위를 계산합니다.

    Args:
        toc: pymupdf에서 추출한 TOC 리스트
        total_pages: 전체 페이지 수
        doc: pymupdf Document 객체 (문자 수 계산용, optional)
    """
    result = []
    n = len(toc)

    for i, (level, title, start_page) in enumerate(toc):
        # 끝 페이지 계산: 같은 레벨 또는 상위 레벨의 다음 항목 찾기
        # (페이지 번호가 현재 항목보다 큰 경우만 유효)
        end_page = total_pages
        for j in range(i + 1, n):
            next_level = toc[j][0]
            next_page = toc[j][2]
            if next_level <= level and next_page > start_page:
                end_page = next_page - 1
                break

        # 하위 항목 존재 여부 확인
        has_children = False
        if i + 1 < n and toc[i + 1][0] > level:
            has_children = True

        page_count = end_page - start_page + 1

        # 문자 수 계산 (doc이 제공된 경우)
        characters = 0
        if doc is not None:
            characters = calculate_characters(doc, start_page, end_page)

        result.append({
            'level': level,
            'title': title,
            'start_page': start_page,
            'end_page': end_page,
            'page_count': page_count,
            'characters': characters,
            'has_children': has_children
        })

    return result


def validate_toc(toc_with_ranges: list) -> tuple[list, list]:
    """TOC 항목의 유효성을 검사합니다.

    페이지 번호가 순차적으로 증가하지 않거나,
    시작 페이지가 끝 페이지보다 큰 경우 무효로 처리합니다.
    """
    valid = []
    invalid = []
    last_page = 0

    for item in toc_with_ranges:
        is_valid = (
            item['start_page'] >= last_page and
            item['start_page'] <= item['end_page'] and
            item['page_count'] > 0
        )

        if is_valid:
            valid.append(item)
            last_page = item['start_page']
        else:
            invalid.append({
                'level': item['level'],
                'title': item['title'],
                'start_page': item['start_page'],
                'end_page': item['end_page'],
                'reason': 'invalid_page_sequence'
            })

    return valid, invalid


def calculate_summary(toc: list, total_pages: int) -> dict:
    """레벨별 통계를 계산합니다."""
    level_stats = defaultdict(lambda: {
        'count': 0,
        'total_pages': 0,
        'total_characters': 0,
        'page_items': [],
        'char_items': []
    })
    max_level = 0

    for item in toc:
        level = item['level']
        level_stats[level]['count'] += 1
        level_stats[level]['total_pages'] += item['page_count']
        level_stats[level]['total_characters'] += item.get('characters', 0)
        level_stats[level]['page_items'].append(item['page_count'])
        level_stats[level]['char_items'].append(item.get('characters', 0))
        max_level = max(max_level, level)

    summary = {
        'total_pages': total_pages,
        'max_level': max_level,
        'levels': {}
    }

    for level in sorted(level_stats.keys()):
        stats = level_stats[level]
        page_items = stats['page_items']
        char_items = stats['char_items']
        avg_pages = stats['total_pages'] / stats['count'] if stats['count'] > 0 else 0
        avg_chars = stats['total_characters'] / stats['count'] if stats['count'] > 0 else 0

        summary['levels'][f'level_{level}'] = {
            'count': stats['count'],
            'total_pages': stats['total_pages'],
            'avg_pages': round(avg_pages, 1),
            'min_pages': min(page_items) if page_items else 0,
            'max_pages': max(page_items) if page_items else 0,
            'total_characters': stats['total_characters'],
            'avg_characters': round(avg_chars, 1),
            'min_characters': min(char_items) if char_items else 0,
            'max_characters': max(char_items) if char_items else 0
        }

    return summary


def check_toc(pdf_path: str) -> dict:
    """PDF의 TOC를 분석합니다."""
    pdf_path = Path(pdf_path).resolve()

    if not pdf_path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {pdf_path}")

    doc = pymupdf.open(pdf_path)
    total_pages = doc.page_count
    toc = doc.get_toc()

    if not toc:
        doc.close()
        return {
            'pdf_name': pdf_path.name,
            'pdf_path': str(pdf_path),
            'total_pages': total_pages,
            'error': 'No TOC found'
        }

    # 페이지 범위 및 문자 수 계산 (doc 전달)
    toc_with_ranges = calculate_page_ranges(toc, total_pages, doc)
    doc.close()

    # 유효성 검사
    valid_toc, invalid_entries = validate_toc(toc_with_ranges)

    # 통계 계산
    summary = calculate_summary(valid_toc, total_pages)

    return {
        'pdf_name': pdf_path.name,
        'pdf_path': str(pdf_path),
        'total_pages': total_pages,
        'summary': summary,
        'toc': valid_toc
    }


def main():
    parser = argparse.ArgumentParser(
        description='PDF의 목차(TOC) 구조를 분석하고 JSON으로 저장합니다.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python check_toc.py "Examples/Value.pdf"          # JSON 파일 저장
  python check_toc.py --stdout "Examples/Value.pdf" # 표준 출력
        """
    )
    parser.add_argument('pdf_path', help='PDF 파일 경로')
    parser.add_argument('--stdout', action='store_true',
                        help='파일 저장 대신 표준 출력으로 출력')

    args = parser.parse_args()

    try:
        result = check_toc(args.pdf_path)

        if args.stdout:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # JSON 파일로 저장 (PDF 이름과 동일한 폴더에)
            pdf_path = Path(args.pdf_path).resolve()
            output_dir = pdf_path.parent / pdf_path.stem
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / "toc.json"

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            print(f"저장됨: {output_path}")

    except FileNotFoundError as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
