#!/usr/bin/env python3
"""
Website-to-Vite Scraper V2.0
Enhanced with Smart Router and API Integrations

Features:
- Auto-detect SSR vs CSR sites
- Tiered scraping: FREE → Playwright → Firecrawl
- MCP server integration ready
- LLM-optimized markdown output option
"""

import os
import re
import sys
import json
import time
import asyncio
import hashlib
import subprocess
from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum

try:
    import httpx
except ImportError:
    httpx = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

try:
    from playwright.async_api import async_playwright
except ImportError:
    async_playwright = None


class SiteType(Enum):
    STATIC = "static"           # Pure HTML, no JS rendering needed
    CSR = "csr"                 # Client-side rendered (React, Vue, etc)
    PROTECTED = "protected"     # Anti-bot protection (Cloudflare, etc)
    UNKNOWN = "unknown"


class ScraperTier(Enum):
    FREE_STATIC = "free_static"       # BeautifulSoup + requests
    FREE_PLAYWRIGHT = "free_playwright"  # Playwright via GitHub Actions
    PAID_BROWSERLESS = "paid_browserless"  # Browserless.io
    PAID_FIRECRAWL = "paid_firecrawl"    # Firecrawl for anti-bot


@dataclass
class ScrapeResult:
    html: str
    site_type: SiteType
    tier_used: ScraperTier
    assets: Dict[str, list]
    metadata: Dict[str, Any]
    success: bool
    error: Optional[str] = None


class SmartRouter:
    """Intelligently route scraping requests to the appropriate tier."""
    
    # Indicators of CSR frameworks
    CSR_INDICATORS = [
        '__NEXT_DATA__',
        '__NUXT__',
        'window.__INITIAL_STATE__',
        'window.__REDUX_STATE__',
        'id="__next"',
        'id="app"',
        'id="root"',
        'ng-app',
        'data-reactroot',
    ]
    
    # Indicators of anti-bot protection
    PROTECTION_INDICATORS = [
        'cf-browser-verification',
        'challenge-platform',
        'cf-chl-bypass',
        '_cf_chl',
        'Just a moment...',
        'Checking your browser',
        'DDoS protection by',
    ]
    
    @classmethod
    def detect_site_type(cls, html: str, response_headers: dict = None) -> SiteType:
        """Analyze HTML to determine site type."""
        # Check for protection first
        for indicator in cls.PROTECTION_INDICATORS:
            if indicator in html:
                return SiteType.PROTECTED
        
        # Check for CSR frameworks
        for indicator in cls.CSR_INDICATORS:
            if indicator in html:
                # If __NEXT_DATA__ exists but body has content, it's SSR
                if indicator == '__NEXT_DATA__':
                    soup = BeautifulSoup(html, 'html.parser') if BeautifulSoup else None
                    if soup:
                        body = soup.find('body')
                        # If body has minimal content, it's CSR
                        if body and len(body.get_text(strip=True)) < 100:
                            return SiteType.CSR
                else:
                    return SiteType.CSR
        
        return SiteType.STATIC
    
    @classmethod
    def select_tier(cls, site_type: SiteType, force_tier: ScraperTier = None) -> ScraperTier:
        """Select the appropriate scraper tier based on site type."""
        if force_tier:
            return force_tier
        
        tier_map = {
            SiteType.STATIC: ScraperTier.FREE_STATIC,
            SiteType.CSR: ScraperTier.FREE_PLAYWRIGHT,
            SiteType.PROTECTED: ScraperTier.PAID_FIRECRAWL,
            SiteType.UNKNOWN: ScraperTier.FREE_PLAYWRIGHT,
        }
        return tier_map.get(site_type, ScraperTier.FREE_PLAYWRIGHT)


class WebsiteToViteScraperV2:
    """Enhanced scraper with smart routing and API integrations."""
    
    def __init__(
        self,
        base_url: str,
        output_dir: str = "scraped-site",
        firecrawl_key: str = None,
        browserless_key: str = None,
        apify_key: str = None,
    ):
        self.base_url = base_url.rstrip('/')
        self.output_dir = output_dir
        self.firecrawl_key = firecrawl_key or os.getenv('FIRECRAWL_API_KEY')
        self.browserless_key = browserless_key or os.getenv('BROWSERLESS_API_KEY')
        self.apify_key = apify_key or os.getenv('APIFY_API_TOKEN')
        
        self.router = SmartRouter()
        self.assets = {'images': [], 'css': [], 'js': [], 'fonts': []}
        self.scraped_pages = set()
        
    async def scrape(self, force_tier: ScraperTier = None) -> ScrapeResult:
        """Main scraping entry point with smart routing."""
        print(f"🕷️ Scraper V2.0 - Analyzing {self.base_url}")
        
        # Step 1: Quick probe to detect site type
        site_type, initial_html = await self._probe_site()
        print(f"📊 Detected site type: {site_type.value}")
        
        # Step 2: Select tier
        tier = self.router.select_tier(site_type, force_tier)
        print(f"🎯 Selected tier: {tier.value}")
        
        # Step 3: Execute scrape with selected tier
        result = await self._execute_scrape(tier, initial_html)
        
        if result.success:
            # Step 4: Generate Vite project
            self._create_vite_structure()
            self._process_and_save(result.html)
            self._create_project_files()
            
            print(f"\n✅ Scraping complete!")
            print(f"📁 Output: {self.output_dir}/")
            print(f"🎯 Tier used: {tier.value}")
        else:
            print(f"\n❌ Scraping failed: {result.error}")
        
        return result
    
    async def _probe_site(self) -> Tuple[SiteType, str]:
        """Quick probe to detect site type."""
        if httpx:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(
                        self.base_url,
                        headers={'User-Agent': 'Mozilla/5.0'},
                        timeout=10,
                        follow_redirects=True
                    )
                    html = response.text
                    site_type = self.router.detect_site_type(html)
                    return site_type, html
                except Exception as e:
                    print(f"⚠️ Probe failed: {e}")
                    return SiteType.UNKNOWN, ""
        else:
            # Fallback to requests
            import requests
            try:
                response = requests.get(
                    self.base_url,
                    headers={'User-Agent': 'Mozilla/5.0'},
                    timeout=10
                )
                html = response.text
                site_type = self.router.detect_site_type(html)
                return site_type, html
            except Exception as e:
                print(f"⚠️ Probe failed: {e}")
                return SiteType.UNKNOWN, ""
    
    async def _execute_scrape(self, tier: ScraperTier, initial_html: str) -> ScrapeResult:
        """Execute scraping with the selected tier."""
        try:
            if tier == ScraperTier.FREE_STATIC:
                return await self._scrape_static(initial_html)
            elif tier == ScraperTier.FREE_PLAYWRIGHT:
                return await self._scrape_playwright()
            elif tier == ScraperTier.PAID_BROWSERLESS:
                return await self._scrape_browserless()
            elif tier == ScraperTier.PAID_FIRECRAWL:
                return await self._scrape_firecrawl()
            else:
                return ScrapeResult(
                    html="", site_type=SiteType.UNKNOWN, tier_used=tier,
                    assets={}, metadata={}, success=False,
                    error=f"Unknown tier: {tier}"
                )
        except Exception as e:
            # Fallback to next tier on failure
            return await self._fallback_scrape(tier, str(e))
    
    async def _scrape_static(self, html: str) -> ScrapeResult:
        """Tier 1: Static scraping with BeautifulSoup."""
        print("📄 Using FREE_STATIC tier (BeautifulSoup)")
        
        if not html:
            import requests
            response = requests.get(self.base_url, timeout=15)
            html = response.text
        
        return ScrapeResult(
            html=html,
            site_type=SiteType.STATIC,
            tier_used=ScraperTier.FREE_STATIC,
            assets=self.assets,
            metadata={'method': 'beautifulsoup'},
            success=True
        )
    
    async def _scrape_playwright(self) -> ScrapeResult:
        """Tier 2: Playwright for CSR sites."""
        print("🎭 Using FREE_PLAYWRIGHT tier")
        
        if not async_playwright:
            # Fallback: try to run playwright via subprocess
            return await self._playwright_subprocess()
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            await page.goto(self.base_url, wait_until='networkidle', timeout=60000)
            await page.wait_for_timeout(3000)  # Extra wait for JS
            
            html = await page.content()
            
            # Take screenshot for reference
            await page.screenshot(path=f"{self.output_dir}/screenshot.png", full_page=True)
            
            await browser.close()
        
        return ScrapeResult(
            html=html,
            site_type=SiteType.CSR,
            tier_used=ScraperTier.FREE_PLAYWRIGHT,
            assets=self.assets,
            metadata={'method': 'playwright', 'screenshot': 'screenshot.png'},
            success=True
        )
    
    async def _playwright_subprocess(self) -> ScrapeResult:
        """Run Playwright via subprocess (for environments without async)."""
        script = f'''
const {{ chromium }} = require('playwright');
(async () => {{
    const browser = await chromium.launch();
    const page = await browser.newPage();
    await page.goto('{self.base_url}', {{ waitUntil: 'networkidle', timeout: 60000 }});
    await page.waitForTimeout(3000);
    const html = await page.content();
    console.log(html);
    await browser.close();
}})();
'''
        result = subprocess.run(
            ['node', '-e', script],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            return ScrapeResult(
                html=result.stdout,
                site_type=SiteType.CSR,
                tier_used=ScraperTier.FREE_PLAYWRIGHT,
                assets=self.assets,
                metadata={'method': 'playwright-subprocess'},
                success=True
            )
        else:
            raise Exception(f"Playwright subprocess failed: {result.stderr}")
    
    async def _scrape_browserless(self) -> ScrapeResult:
        """Tier 3: Browserless.io for complex JS."""
        print("☁️ Using PAID_BROWSERLESS tier")
        
        if not self.browserless_key:
            raise Exception("BROWSERLESS_API_KEY not set")
        
        if httpx:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://chrome.browserless.io/content?token={self.browserless_key}",
                    json={
                        "url": self.base_url,
                        "waitFor": 5000,
                        "gotoOptions": {"waitUntil": "networkidle0"}
                    },
                    timeout=60
                )
                html = response.text
        else:
            import requests
            response = requests.post(
                f"https://chrome.browserless.io/content?token={self.browserless_key}",
                json={
                    "url": self.base_url,
                    "waitFor": 5000,
                    "gotoOptions": {"waitUntil": "networkidle0"}
                },
                timeout=60
            )
            html = response.text
        
        return ScrapeResult(
            html=html,
            site_type=SiteType.CSR,
            tier_used=ScraperTier.PAID_BROWSERLESS,
            assets=self.assets,
            metadata={'method': 'browserless'},
            success=True
        )
    
    async def _scrape_firecrawl(self) -> ScrapeResult:
        """Tier 4: Firecrawl for anti-bot protected sites."""
        print("🔥 Using PAID_FIRECRAWL tier")
        
        if not self.firecrawl_key:
            raise Exception("FIRECRAWL_API_KEY not set")
        
        if httpx:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.firecrawl.dev/v1/scrape",
                    headers={"Authorization": f"Bearer {self.firecrawl_key}"},
                    json={
                        "url": self.base_url,
                        "formats": ["html", "markdown"],
                        "onlyMainContent": False,
                        "waitFor": 5000
                    },
                    timeout=60
                )
                data = response.json()
                html = data.get('data', {}).get('html', '')
        else:
            import requests
            response = requests.post(
                "https://api.firecrawl.dev/v1/scrape",
                headers={"Authorization": f"Bearer {self.firecrawl_key}"},
                json={
                    "url": self.base_url,
                    "formats": ["html", "markdown"],
                    "onlyMainContent": False,
                    "waitFor": 5000
                },
                timeout=60
            )
            data = response.json()
            html = data.get('data', {}).get('html', '')
        
        return ScrapeResult(
            html=html,
            site_type=SiteType.PROTECTED,
            tier_used=ScraperTier.PAID_FIRECRAWL,
            assets=self.assets,
            metadata={'method': 'firecrawl', 'raw_response': data},
            success=True
        )
    
    async def _fallback_scrape(self, failed_tier: ScraperTier, error: str) -> ScrapeResult:
        """Fallback to next tier on failure."""
        print(f"⚠️ {failed_tier.value} failed: {error}")
        
        fallback_chain = {
            ScraperTier.FREE_STATIC: ScraperTier.FREE_PLAYWRIGHT,
            ScraperTier.FREE_PLAYWRIGHT: ScraperTier.PAID_BROWSERLESS,
            ScraperTier.PAID_BROWSERLESS: ScraperTier.PAID_FIRECRAWL,
        }
        
        next_tier = fallback_chain.get(failed_tier)
        if next_tier:
            print(f"🔄 Falling back to {next_tier.value}")
            return await self._execute_scrape(next_tier, "")
        else:
            return ScrapeResult(
                html="", site_type=SiteType.UNKNOWN, tier_used=failed_tier,
                assets={}, metadata={}, success=False,
                error=f"All tiers exhausted. Last error: {error}"
            )
    
    def _create_vite_structure(self):
        """Create Vite project structure."""
        dirs = [
            self.output_dir,
            f"{self.output_dir}/src",
            f"{self.output_dir}/src/pages",
            f"{self.output_dir}/src/assets/images",
            f"{self.output_dir}/src/assets/css",
            f"{self.output_dir}/src/assets/js",
            f"{self.output_dir}/src/assets/fonts",
            f"{self.output_dir}/public",
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
    
    def _process_and_save(self, html: str):
        """Process HTML and save to Vite structure."""
        with open(f"{self.output_dir}/index.html", 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Also save to src/pages for multi-page support
        with open(f"{self.output_dir}/src/pages/index.html", 'w', encoding='utf-8') as f:
            f.write(html)
    
    def _create_project_files(self):
        """Create Vite project configuration files."""
        # package.json
        package = {
            "name": os.path.basename(self.output_dir),
            "private": True,
            "version": "0.0.1",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview"
            },
            "devDependencies": {
                "vite": "^5.0.0"
            }
        }
        with open(f"{self.output_dir}/package.json", 'w') as f:
            json.dump(package, f, indent=2)
        
        # vite.config.js
        vite_config = '''import { defineConfig } from 'vite'

export default defineConfig({
  base: './',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    minify: 'terser',
  },
  server: {
    port: 3000,
    open: true
  }
})
'''
        with open(f"{self.output_dir}/vite.config.js", 'w') as f:
            f.write(vite_config)
        
        # .gitignore
        gitignore = '''node_modules
dist
.DS_Store
*.local
.env
'''
        with open(f"{self.output_dir}/.gitignore", 'w') as f:
            f.write(gitignore)


async def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python website_scraper_v2.py <url> [output-dir]")
        print("Example: python website_scraper_v2.py https://example.com my-project")
        sys.exit(1)
    
    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "scraped-site"
    
    scraper = WebsiteToViteScraperV2(url, output_dir)
    result = await scraper.scrape()
    
    if result.success:
        print(f"\n🚀 Next steps:")
        print(f"   cd {output_dir}")
        print(f"   npm install")
        print(f"   npm run dev")
    else:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
