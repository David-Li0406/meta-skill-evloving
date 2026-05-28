#!/usr/bin/env python3
"""
Website-to-Vite Scraper
Converts any website into a deployable Vite project with proper asset handling.

Usage:
    python website_scraper.py https://example.com my-project
    
Or programmatically:
    from website_scraper import WebsiteToViteScraper
    scraper = WebsiteToViteScraper("https://example.com", "my-project")
    scraper.scrape()
"""

import os
import re
import sys
import time
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


class WebsiteToViteScraper:
    """Scrape websites and convert to Vite project structure."""
    
    def __init__(self, base_url, output_dir="scraped-site"):
        self.base_url = base_url.rstrip('/')
        self.output_dir = output_dir
        self.parsed_base = urlparse(base_url)
        self.domain = self.parsed_base.netloc
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        self.assets = {
            'images': [],
            'css': [],
            'js': [],
            'fonts': []
        }
        self.scraped_pages = set()
        self.rate_limit = 0.5  # seconds between requests
        
    def scrape(self):
        """Main entry point - scrape the website."""
        print(f"🕷️ Starting scrape of {self.base_url}")
        
        # Create Vite project structure
        self.create_vite_structure()
        
        # Scrape main page
        self.scrape_page(self.base_url)
        
        # Create project files
        self.create_package_json()
        self.create_vite_config()
        self.create_main_js()
        self.create_gitignore()
        self.create_readme()
        
        print(f"\n✅ Scraping complete!")
        print(f"📁 Output: {self.output_dir}/")
        print(f"📊 Stats: {len(self.scraped_pages)} pages, {sum(len(v) for v in self.assets.values())} assets")
        print(f"\n🚀 Next steps:")
        print(f"   cd {self.output_dir}")
        print(f"   npm install")
        print(f"   npm run dev")
        
    def create_vite_structure(self):
        """Create the Vite project folder structure."""
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
        print(f"📁 Created project structure: {self.output_dir}/")
        
    def scrape_page(self, url, depth=0, max_depth=2):
        """Scrape a single page and its assets."""
        if url in self.scraped_pages or depth > max_depth:
            return
        
        # Only scrape pages on the same domain
        parsed = urlparse(url)
        if parsed.netloc and parsed.netloc != self.domain:
            return
            
        self.scraped_pages.add(url)
        time.sleep(self.rate_limit)
        
        try:
            print(f"📄 Scraping: {url}")
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Download and update asset references
            self.process_images(soup)
            self.process_stylesheets(soup, url)
            self.process_scripts(soup)
            self.process_fonts(soup)
            
            # Fix relative links
            self.fix_links(soup)
            
            # Save the HTML
            page_name = self.get_page_name(url)
            self.save_html(soup, page_name)
            
            # Find and scrape internal links
            for link in soup.find_all('a', href=True):
                href = link['href']
                if not href.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
                    full_url = urljoin(url, href)
                    if urlparse(full_url).netloc == self.domain:
                        self.scrape_page(full_url, depth + 1, max_depth)
                        
        except Exception as e:
            print(f"⚠️ Error scraping {url}: {e}")
            
    def process_images(self, soup):
        """Download images and update src attributes."""
        for img in soup.find_all('img', src=True):
            old_src = img['src']
            new_path = self.download_asset(old_src, 'images')
            if new_path:
                img['src'] = new_path
                
        # Also check for background images in style attributes
        for elem in soup.find_all(style=True):
            style = elem['style']
            urls = re.findall(r'url\(["\']?([^"\')]+)["\']?\)', style)
            for url in urls:
                if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp']):
                    new_path = self.download_asset(url, 'images')
                    if new_path:
                        elem['style'] = style.replace(url, new_path)
                        
    def process_stylesheets(self, soup, page_url):
        """Download CSS files and process their contents."""
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                css_path = self.download_asset(href, 'css')
                if css_path:
                    link['href'] = css_path
                    # Process CSS content for additional assets
                    self.process_css_file(href, page_url)
                    
        # Process inline styles
        for style in soup.find_all('style'):
            if style.string:
                style.string = self.process_css(style.string, page_url)
                
    def process_css_file(self, css_url, page_url):
        """Download and process a CSS file's contents."""
        try:
            full_url = urljoin(page_url, css_url)
            response = self.session.get(full_url, timeout=10)
            if response.ok:
                processed_css = self.process_css(response.text, full_url)
                # Save processed CSS
                filename = self.get_safe_filename(css_url, '.css')
                css_path = f"{self.output_dir}/src/assets/css/{filename}"
                with open(css_path, 'w', encoding='utf-8') as f:
                    f.write(processed_css)
        except Exception as e:
            print(f"⚠️ Error processing CSS {css_url}: {e}")
            
    def process_css(self, css_content, base_url):
        """Process CSS and download referenced assets."""
        url_pattern = r'url\(["\']?([^"\')]+)["\']?\)'
        
        def replace_url(match):
            url = match.group(1)
            if url.startswith('data:'):
                return match.group(0)
                
            full_url = urljoin(base_url, url)
            
            # Determine asset type and download
            if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp']):
                new_path = self.download_asset(full_url, 'images')
            elif any(ext in url.lower() for ext in ['.woff', '.woff2', '.ttf', '.eot', '.otf']):
                new_path = self.download_asset(full_url, 'fonts')
            else:
                new_path = url
                
            return f'url("{new_path or url}")'
            
        return re.sub(url_pattern, replace_url, css_content)
        
    def process_scripts(self, soup):
        """Download JavaScript files."""
        for script in soup.find_all('script', src=True):
            src = script['src']
            # Skip external CDN scripts (keep them as-is)
            if not self.is_external_cdn(src):
                new_path = self.download_asset(src, 'js')
                if new_path:
                    script['src'] = new_path
                    
    def process_fonts(self, soup):
        """Process font references."""
        # Fonts are typically in CSS, handled by process_css
        pass
        
    def fix_links(self, soup):
        """Convert absolute links to relative for Vite."""
        for a in soup.find_all('a', href=True):
            href = a['href']
            parsed = urlparse(href)
            if parsed.netloc == self.domain:
                # Convert to relative path
                path = parsed.path or '/'
                if path == '/':
                    a['href'] = '/index.html'
                elif not path.endswith('.html'):
                    a['href'] = f"/{path.strip('/').replace('/', '-') or 'index'}.html"
                    
    def download_asset(self, url, asset_type):
        """Download an asset and return the new local path."""
        try:
            # Skip data URLs
            if url.startswith('data:'):
                return url
                
            full_url = urljoin(self.base_url, url)
            
            # Skip external CDNs for JS/CSS (keep them as-is)
            if self.is_external_cdn(full_url) and asset_type in ['js', 'css']:
                return url
                
            response = self.session.get(full_url, timeout=10)
            response.raise_for_status()
            
            # Generate safe filename
            filename = self.get_safe_filename(url, self.get_extension(url, asset_type))
            asset_path = f"{self.output_dir}/src/assets/{asset_type}/{filename}"
            
            # Write file
            with open(asset_path, 'wb') as f:
                f.write(response.content)
                
            self.assets[asset_type].append(filename)
            relative_path = f"/src/assets/{asset_type}/{filename}"
            print(f"  ⬇️ {asset_type}: {filename}")
            return relative_path
            
        except Exception as e:
            print(f"  ⚠️ Failed to download {url}: {e}")
            return None
            
    def is_external_cdn(self, url):
        """Check if URL is an external CDN."""
        external_domains = [
            'cdnjs.cloudflare.com',
            'cdn.jsdelivr.net',
            'unpkg.com',
            'fonts.googleapis.com',
            'fonts.gstatic.com',
            'ajax.googleapis.com',
            'code.jquery.com',
        ]
        parsed = urlparse(url)
        return any(domain in parsed.netloc for domain in external_domains)
        
    def get_safe_filename(self, url, extension):
        """Generate a safe filename from URL."""
        parsed = urlparse(url)
        path = parsed.path
        
        # Get the original filename
        original_name = os.path.basename(path)
        if original_name and '.' in original_name:
            # Clean the name
            name = re.sub(r'[^\w\-.]', '_', original_name)
            return name
        else:
            # Generate hash-based name
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            return f"asset_{url_hash}{extension}"
            
    def get_extension(self, url, asset_type):
        """Get file extension from URL or default based on type."""
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        # Try to get extension from URL
        if '.' in path:
            ext = os.path.splitext(path)[1]
            if ext:
                return ext
                
        # Default extensions by type
        defaults = {
            'images': '.jpg',
            'css': '.css',
            'js': '.js',
            'fonts': '.woff2'
        }
        return defaults.get(asset_type, '')
        
    def get_page_name(self, url):
        """Convert URL to page filename."""
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        
        if not path or path == '/':
            return 'index.html'
            
        # Convert path to filename
        name = path.replace('/', '-').replace('.html', '').replace('.htm', '')
        name = re.sub(r'[^\w\-]', '_', name)
        return f"{name}.html"
        
    def save_html(self, soup, filename):
        """Save processed HTML to file."""
        # Add Vite-compatible script tag
        if soup.body:
            vite_script = soup.new_tag('script', type='module', src='/src/main.js')
            soup.body.append(vite_script)
            
        html_path = f"{self.output_dir}/src/pages/{filename}"
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
            
        # Also copy index.html to root for Vite
        if filename == 'index.html':
            with open(f"{self.output_dir}/index.html", 'w', encoding='utf-8') as f:
                f.write(str(soup.prettify()))
                
    def create_package_json(self):
        """Create package.json for npm."""
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
        
        import json
        with open(f"{self.output_dir}/package.json", 'w') as f:
            json.dump(package, f, indent=2)
            
    def create_vite_config(self):
        """Create vite.config.js."""
        config = '''import { defineConfig } from 'vite'

export default defineConfig({
  base: './',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    minify: 'terser',
    rollupOptions: {
      input: {
        main: 'index.html'
      }
    }
  },
  server: {
    port: 3000,
    open: true
  }
})
'''
        with open(f"{self.output_dir}/vite.config.js", 'w') as f:
            f.write(config)
            
    def create_main_js(self):
        """Create main.js entry point."""
        main_js = '''// Main entry point
console.log('🚀 Vite project loaded!')

// Import styles
// import './style.css'

// Your custom JavaScript here
document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM ready!')
})
'''
        with open(f"{self.output_dir}/src/main.js", 'w') as f:
            f.write(main_js)
            
    def create_gitignore(self):
        """Create .gitignore."""
        gitignore = '''node_modules
dist
.DS_Store
*.local
.env
'''
        with open(f"{self.output_dir}/.gitignore", 'w') as f:
            f.write(gitignore)
            
    def create_readme(self):
        """Create README.md."""
        readme = f'''# {os.path.basename(self.output_dir)}

Scraped from: {self.base_url}

## Getting Started

```bash
npm install
npm run dev
```

## Build for Production

```bash
npm run build
```

## Deploy to Cloudflare Pages

```bash
npx wrangler pages deploy dist --project-name={os.path.basename(self.output_dir)}
```

## Scraped Assets

- **Pages**: {len(self.scraped_pages)}
- **Images**: {len(self.assets['images'])}
- **CSS**: {len(self.assets['css'])}
- **JS**: {len(self.assets['js'])}
- **Fonts**: {len(self.assets['fonts'])}

---
Generated by Website-to-Vite Scraper
'''
        with open(f"{self.output_dir}/README.md", 'w') as f:
            f.write(readme)


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python website_scraper.py <url> [output-dir]")
        print("Example: python website_scraper.py https://example.com my-project")
        sys.exit(1)
        
    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "scraped-site"
    
    scraper = WebsiteToViteScraper(url, output_dir)
    scraper.scrape()


if __name__ == "__main__":
    main()
