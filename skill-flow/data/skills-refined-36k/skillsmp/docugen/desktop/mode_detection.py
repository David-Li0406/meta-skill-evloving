"""Mode detection for DocuGen workflow documentation.

Determines whether a user request should use web-based (Playwright/Chrome
DevTools) or desktop-based (mss/accessibility) capture pipeline.
"""

import re
from typing import Literal

Mode = Literal["web", "desktop", "ambiguous"]

# Desktop mode indicators
_DESKTOP_KEYWORDS = [
    r"\bdesktop\b",
    r"\bnative\s+app\b",
    r"\binstalled\s+software\b",
    r"\bdesktop\s+software\b",
    r"\bdesktop\s+application\b",
    r"\bsystem\s+preferences?\b",
    r"\bsystem\s+settings?\b",
    r"\bfinder\b",
    r"\bexplorer\b",
    r"\btaskbar\b",
    r"\bstart\s+menu\b",
    r"\bwindows\s+application\b",
    r"\bmacos\s+application\b",
    r"\bphotoshop\b",
    r"\bexcel\b",
    r"\bword\b",
    r"\bvs\s*code\b",
    r"\bterminal\b",
    r"\biterm\b",
    r"\bslack\b",
    r"\bdiscord\b",
    r"\bspotify\b",
    r"\bcapture\s+desktop\b",
    r"\brecord\s+desktop\b",
    r"\bnative\s+ui\b",
]

# Web mode indicators
_WEB_KEYWORDS = [
    r"\bwebsite\b",
    r"\bweb\s+app\b",
    r"\bbrowser\b",
    r"\blogin\s+page\b",
    r"\bdashboard\b",
    r"\bweb\s+portal\b",
    r"\bweb\s+interface\b",
    r"\bonline\b",
    r"\bhttp",
    r"\burl\b",
]

# URL pattern (strong web indicator)
_URL_PATTERN = re.compile(
    r"https?://[^\s]+|www\.[^\s]+", re.IGNORECASE
)

_DESKTOP_PATTERNS = [re.compile(p, re.IGNORECASE) for p in _DESKTOP_KEYWORDS]
_WEB_PATTERNS = [re.compile(p, re.IGNORECASE) for p in _WEB_KEYWORDS]


def detect_mode(user_request: str) -> Mode:
    """Detect whether a request is for web or desktop documentation.

    Priority:
        1. Explicit URL → web (always)
        2. Desktop keywords → desktop
        3. Web keywords → web
        4. Neither → ambiguous

    Args:
        user_request: The user's natural language request.

    Returns:
        "web", "desktop", or "ambiguous".
    """
    # Priority 1: URL presence is a strong web signal
    if _URL_PATTERN.search(user_request):
        return "web"

    desktop_score = sum(1 for p in _DESKTOP_PATTERNS if p.search(user_request))
    web_score = sum(1 for p in _WEB_PATTERNS if p.search(user_request))

    # Priority 2/3: keyword scoring
    if desktop_score > 0 and web_score == 0:
        return "desktop"
    if web_score > 0 and desktop_score == 0:
        return "web"
    if desktop_score > 0 and web_score > 0:
        # Both present - use higher score, bias toward explicit desktop
        return "desktop" if desktop_score >= web_score else "web"

    return "ambiguous"
