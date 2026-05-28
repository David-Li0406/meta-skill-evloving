"""
WASDE Release Discovery Script

Discovers WASDE report release dates and URLs from USDA sources.
"""

import re
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from bs4 import BeautifulSoup


# USDA WASDE URLs
WASDE_BASE_URL = "https://www.usda.gov/oce/commodity/wasde"
WASDE_PDF_PATTERN = "https://www.usda.gov/oce/commodity/wasde/wasde{yymm}.pdf"
WASDE_ARCHIVE_URL = "https://esmis.nal.usda.gov/publication/world-agricultural-supply-and-demand-estimates"


def discover_latest_release() -> Dict:
    """
    Discover the latest available WASDE release.

    Returns:
        dict: {
            "release_date": "2025-01-10",
            "pdf_url": "https://...",
            "html_url": "https://..."
        }
    """
    try:
        # Try to get from main WASDE page
        response = requests.get(WASDE_BASE_URL, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for PDF links
        pdf_links = soup.find_all('a', href=re.compile(r'wasde\d{4}\.pdf'))

        if pdf_links:
            # Extract date from latest PDF link
            pdf_url = pdf_links[0]['href']
            if not pdf_url.startswith('http'):
                pdf_url = f"https://www.usda.gov{pdf_url}"

            # Parse date from filename (wasdeMMYY.pdf)
            match = re.search(r'wasde(\d{2})(\d{2})\.pdf', pdf_url)
            if match:
                month, year = match.groups()
                year_full = 2000 + int(year)
                # Estimate release date (around 10th of month)
                release_date = f"{year_full}-{month}-10"

                return {
                    "release_date": release_date,
                    "pdf_url": pdf_url,
                    "html_url": WASDE_BASE_URL
                }

        # Fallback: construct URL for current month
        return _construct_current_month_release()

    except Exception as e:
        print(f"Warning: Could not discover latest release: {e}")
        return _construct_current_month_release()


def discover_by_date(target_date: str) -> Dict:
    """
    Get release info for a specific date.

    Args:
        target_date: Target date in YYYY-MM-DD format

    Returns:
        dict: Release information
    """
    dt = datetime.strptime(target_date, "%Y-%m-%d")
    yymm = dt.strftime("%m%y")

    pdf_url = WASDE_PDF_PATTERN.format(yymm=yymm)

    return {
        "release_date": target_date,
        "pdf_url": pdf_url,
        "html_url": WASDE_BASE_URL
    }


def get_release_calendar(
    start: datetime,
    end: datetime
) -> List[Dict]:
    """
    Get all WASDE releases between start and end dates.

    WASDE is typically released around the 10th-12th of each month.

    Args:
        start: Start date
        end: End date

    Returns:
        list: List of release info dicts
    """
    releases = []
    current = start.replace(day=1)  # Start from first of month

    while current <= end:
        # WASDE typically released around 10th
        release_date = current.replace(day=10)

        if start <= release_date <= end:
            yymm = release_date.strftime("%m%y")
            releases.append({
                "release_date": release_date.strftime("%Y-%m-%d"),
                "pdf_url": WASDE_PDF_PATTERN.format(yymm=yymm),
                "html_url": WASDE_BASE_URL,
                "estimated": True  # Actual date may vary
            })

        # Move to next month
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)

    return releases


def verify_release_exists(release_info: Dict) -> bool:
    """
    Verify that a WASDE release actually exists.

    Args:
        release_info: Release information dict

    Returns:
        bool: True if release exists
    """
    try:
        response = requests.head(release_info['pdf_url'], timeout=10)
        return response.status_code == 200
    except:
        return False


def get_official_release_dates(year: int) -> List[Dict]:
    """
    Get official WASDE release dates for a given year.

    Note: This requires fetching from USDA calendar which may not always
    be available. Falls back to estimated dates.

    Args:
        year: Calendar year

    Returns:
        list: List of release dates
    """
    # USDA publishes release schedule, but for now use estimates
    # Typical release pattern: around 10th-12th of each month
    releases = []

    for month in range(1, 13):
        # Typical release day varies, use 10th as estimate
        release_date = datetime(year, month, 10)
        releases.append({
            "release_date": release_date.strftime("%Y-%m-%d"),
            "estimated": True
        })

    return releases


def _construct_current_month_release() -> Dict:
    """Construct release info for current month."""
    now = datetime.now()
    yymm = now.strftime("%m%y")

    return {
        "release_date": now.strftime("%Y-%m-10"),
        "pdf_url": WASDE_PDF_PATTERN.format(yymm=yymm),
        "html_url": WASDE_BASE_URL,
        "estimated": True
    }


# CLI interface
if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Discover WASDE releases")
    parser.add_argument("--latest", action="store_true", help="Get latest release")
    parser.add_argument("--date", type=str, help="Get release for specific date (YYYY-MM-DD)")
    parser.add_argument("--months", type=int, default=12, help="Get releases for past N months")

    args = parser.parse_args()

    if args.latest:
        result = discover_latest_release()
        print(json.dumps(result, indent=2))

    elif args.date:
        result = discover_by_date(args.date)
        print(json.dumps(result, indent=2))

    else:
        end = datetime.now()
        start = end - timedelta(days=args.months * 31)
        results = get_release_calendar(start, end)
        print(json.dumps(results, indent=2))
