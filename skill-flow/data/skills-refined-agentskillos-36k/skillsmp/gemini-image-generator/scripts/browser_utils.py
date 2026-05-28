"""
Browser utilities for Gemini Image Generator
Handles browser launching with persistent context and anti-detection features
Based on NotebookLM skill patterns
"""

import json
import time
import random
from typing import Optional
from pathlib import Path

from patchright.sync_api import Playwright, BrowserContext, Page

from config import (
    BROWSER_PROFILE_DIR,
    STATE_FILE,
    BROWSER_ARGS,
    USER_AGENT,
    TYPING_WPM_MIN,
    TYPING_WPM_MAX
)


class BrowserFactory:
    """Factory for creating configured browser contexts with persistent profiles"""

    @staticmethod
    def launch_persistent_context(
        playwright: Playwright,
        headless: bool = True,
        user_data_dir: Optional[str] = None
    ) -> BrowserContext:
        """
        Launch a persistent browser context with anti-detection features.

        This uses launch_persistent_context which:
        - Maintains browser profile between sessions
        - Automatically saves/restores cookies and localStorage
        - Prevents automation detection

        Args:
            playwright: Playwright instance
            headless: Whether to run in headless mode
            user_data_dir: Directory for browser profile (default: BROWSER_PROFILE_DIR)

        Returns:
            BrowserContext: Configured browser context
        """
        if user_data_dir is None:
            user_data_dir = str(BROWSER_PROFILE_DIR)

        # Ensure profile directory exists
        Path(user_data_dir).mkdir(parents=True, exist_ok=True)

        print(f"   → Using browser profile: {user_data_dir}")

        # Launch persistent context (key difference from regular launch!)
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            channel="chrome",  # Use real Chrome for better compatibility
            headless=headless,
            no_viewport=True,  # Allow dynamic viewport
            ignore_default_args=["--enable-automation"],
            user_agent=USER_AGENT,
            args=BROWSER_ARGS
        )

        # Inject cookies from state.json if available (Playwright bug workaround)
        # See: https://github.com/microsoft/playwright/issues/36139
        BrowserFactory._inject_cookies(context)

        return context

    @staticmethod
    def _inject_cookies(context: BrowserContext):
        """
        Inject cookies from state.json if available.

        This is a workaround for Playwright bug where session cookies
        (expires=-1) don't persist automatically in user_data_dir.
        """
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r') as f:
                    state = json.load(f)
                    if 'cookies' in state and len(state['cookies']) > 0:
                        context.add_cookies(state['cookies'])
                        print(f"   → Restored {len(state['cookies'])} cookies")
            except Exception as e:
                # Not critical, just means fresh login needed
                pass


class StealthUtils:
    """Utilities for human-like browser interactions"""

    @staticmethod
    def random_delay(min_ms: int = 100, max_ms: int = 500):
        """Add random delay to mimic human behavior"""
        time.sleep(random.uniform(min_ms / 1000, max_ms / 1000))

    @staticmethod
    def human_type(page: Page, selector: str, text: str,
                   wpm_min: int = TYPING_WPM_MIN,
                   wpm_max: int = TYPING_WPM_MAX):
        """
        Type text with human-like speed variations.

        Args:
            page: Playwright page
            selector: CSS selector for input element
            text: Text to type
            wpm_min: Minimum words per minute
            wpm_max: Maximum words per minute
        """
        element = page.query_selector(selector)
        if not element:
            try:
                element = page.wait_for_selector(selector, timeout=5000)
            except:
                print(f"   ⚠️  Element not found: {selector}")
                return

        # Calculate delay per character
        wpm = random.randint(wpm_min, wpm_max)
        chars_per_second = (wpm * 5) / 60  # Average word = 5 chars
        base_delay = 1000 / chars_per_second  # ms per char

        # Type with variation
        for char in text:
            element.type(char)
            # Add random variation (±30%)
            delay = base_delay * random.uniform(0.7, 1.3)
            time.sleep(delay / 1000)

    @staticmethod
    def scroll_slowly(page: Page, amount: int = 300):
        """Scroll page slowly like a human"""
        page.evaluate(f"""
            window.scrollBy({{
                top: {amount},
                behavior: 'smooth'
            }});
        """)
        StealthUtils.random_delay(500, 1000)
