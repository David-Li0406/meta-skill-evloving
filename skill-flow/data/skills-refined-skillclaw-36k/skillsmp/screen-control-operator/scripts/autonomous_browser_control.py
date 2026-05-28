#!/usr/bin/env python3
"""
Autonomous Browser Control - Screen Control Operator
Acts like GPT Operator using CDP + Accessibility Tree (NO screenshots)
"""

import sys
import json
import argparse
from datetime import datetime
from playwright.sync_api import sync_playwright, Page

class ScreenControlOperator:
    """Autonomous browser controller using CDP and A11y tree"""
    
    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.console_errors = []
        self.network_requests = []
    
    def start(self):
        """Initialize browser with CDP"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=['--remote-debugging-port=9222']
        )
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.page = self.context.new_page()
        
        # Set up monitoring
        self.page.on('console', self._handle_console)
        self.page.on('request', self._handle_request)
    
    def _handle_console(self, msg):
        """Monitor console messages"""
        if msg.type == 'error':
            self.console_errors.append({
                'text': msg.text,
                'timestamp': datetime.now().isoformat()
            })
    
    def _handle_request(self, request):
        """Track network requests"""
        self.network_requests.append({
            'url': request.url,
            'method': request.method,
            'timestamp': datetime.now().isoformat()
        })
    
    def navigate(self, url, wait_until='networkidle'):
        """Navigate to URL"""
        print(f"📍 Navigating to: {url}")
        self.page.goto(url, wait_until=wait_until)
        self.page.wait_for_timeout(2000)
        return self.get_page_state()
    
    def get_page_state(self):
        """Get current page state via A11y tree"""
        elements = self.page.query_selector_all('[role], button, a, input, select, textarea')
        
        state = {
            'url': self.page.url,
            'title': self.page.title(),
            'interactive_elements': [],
            'console_errors': len(self.console_errors),
            'network_requests': len(self.network_requests)
        }
        
        for elem in elements[:50]:  # Limit to first 50
            try:
                state['interactive_elements'].append({
                    'tag': elem.evaluate('el => el.tagName'),
                    'role': elem.get_attribute('role'),
                    'text': elem.inner_text()[:50] if elem.inner_text() else '',
                    'visible': elem.is_visible(),
                    'enabled': elem.is_enabled()
                })
            except:
                continue
        
        return state
    
    def find_element(self, selector=None, role=None, text=None):
        """Find element by selector, role, or text"""
        if role:
            return self.page.get_by_role(role, name=text)
        elif text:
            return self.page.get_by_text(text)
        elif selector:
            return self.page.locator(selector)
        else:
            raise ValueError("Must provide selector, role, or text")
    
    def click(self, selector=None, role=None, text=None):
        """Click element"""
        elem = self.find_element(selector, role, text)
        if elem.is_visible():
            elem.click()
            self.page.wait_for_timeout(1000)
            return True
        return False
    
    def type_text(self, text, selector=None, role=None):
        """Type text into input"""
        elem = self.find_element(selector=selector, role=role)
        elem.fill(text)
        return True
    
    def verify_visible(self, selector=None, role=None, text=None):
        """Verify element is visible"""
        elem = self.find_element(selector, role, text)
        return elem.is_visible()
    
    def verify_text(self, expected_text, selector=None, role=None):
        """Verify element contains text"""
        elem = self.find_element(selector=selector, role=role)
        actual_text = elem.inner_text()
        return expected_text in actual_text
    
    def get_attribute(self, attribute, selector=None, role=None):
        """Get element attribute"""
        elem = self.find_element(selector=selector, role=role)
        return elem.get_attribute(attribute)
    
    def measure_performance(self):
        """Get performance metrics"""
        metrics = self.page.evaluate('''() => {
            const perf = performance.getEntriesByType('navigation')[0];
            return {
                dom_loaded_ms: perf.domContentLoadedEventEnd - perf.fetchStart,
                fully_loaded_ms: perf.loadEventEnd - perf.fetchStart,
                first_paint_ms: performance.getEntriesByType('paint')[0]?.startTime || 0
            };
        }''')
        return metrics
    
    def screenshot(self, path):
        """Take screenshot (optional, for debugging only)"""
        self.page.screenshot(path=path)
        return path
    
    def stop(self):
        """Cleanup"""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()


class LovableVerifier:
    """Specialized verifier for Lovable previews"""
    
    def __init__(self, operator: ScreenControlOperator):
        self.operator = operator
        self.issues = []
    
    def verify_preview(self, project_id):
        """Verify Lovable preview autonomously"""
        print(f"\n🔍 Verifying Lovable Preview: {project_id}")
        print("=" * 60)
        
        # Navigate to project
        url = f"https://lovable.dev/projects/{project_id}"
        self.operator.navigate(url)
        
        # Click Preview button
        try:
            self.operator.click(role="button", text="Preview")
            self.operator.page.wait_for_timeout(2000)
            
            # Switch to preview page if opened in new tab
            pages = self.operator.context.pages
            if len(pages) > 1:
                self.operator.page = pages[-1]
                print("✓ Switched to preview page")
        except Exception as e:
            self.issues.append(f"Failed to open preview: {e}")
        
        # Run checkpoints
        self.check_map_loads()
        self.check_markers_visible()
        self.check_search_functionality()
        self.check_mobile_responsive()
        
        return self.generate_report()
    
    def check_map_loads(self):
        """Checkpoint: Map container renders"""
        print("\n📋 Checkpoint: Map Loads")
        try:
            map_visible = self.operator.verify_visible(selector="#map-container") or \
                         self.operator.verify_visible(selector="[class*='map']")
            if map_visible:
                print("✓ Map container visible")
            else:
                self.issues.append("Map container not found")
                print("✗ Map container not visible")
        except Exception as e:
            self.issues.append(f"Map check failed: {e}")
            print(f"✗ Error: {e}")
    
    def check_markers_visible(self):
        """Checkpoint: Property markers display"""
        print("\n📋 Checkpoint: Markers Visible")
        try:
            markers = self.operator.page.query_selector_all('[class*="marker"], [data-testid*="marker"]')
            if len(markers) > 0:
                print(f"✓ Found {len(markers)} markers")
            else:
                self.issues.append("No property markers found")
                print("✗ No markers visible")
        except Exception as e:
            self.issues.append(f"Marker check failed: {e}")
            print(f"✗ Error: {e}")
    
    def check_search_functionality(self):
        """Checkpoint: Search works"""
        print("\n📋 Checkpoint: Search Functionality")
        try:
            search_visible = self.operator.verify_visible(selector="input[type='search']") or \
                           self.operator.verify_visible(selector="[placeholder*='Search']")
            if search_visible:
                print("✓ Search input visible")
            else:
                self.issues.append("Search input not found")
                print("✗ Search not visible")
        except Exception as e:
            self.issues.append(f"Search check failed: {e}")
            print(f"✗ Error: {e}")
    
    def check_mobile_responsive(self):
        """Checkpoint: Mobile view works"""
        print("\n📋 Checkpoint: Mobile Responsive")
        try:
            # Set mobile viewport
            self.operator.page.set_viewport_size({'width': 375, 'height': 667})
            self.operator.page.wait_for_timeout(1000)
            
            # Check if content still visible
            state = self.operator.get_page_state()
            visible_elements = sum(1 for elem in state['interactive_elements'] if elem['visible'])
            
            if visible_elements > 0:
                print(f"✓ Mobile view renders ({visible_elements} visible elements)")
            else:
                self.issues.append("Mobile view broken")
                print("✗ Mobile view issue")
            
            # Reset viewport
            self.operator.page.set_viewport_size({'width': 1920, 'height': 1080})
        except Exception as e:
            self.issues.append(f"Mobile check failed: {e}")
            print(f"✗ Error: {e}")
    
    def generate_report(self):
        """Generate verification report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'url': self.operator.page.url,
            'title': self.operator.page.title(),
            'issues': self.issues,
            'console_errors': self.operator.console_errors,
            'performance': self.operator.measure_performance(),
            'passed': len(self.issues) == 0
        }
        return report


def main():
    parser = argparse.ArgumentParser(description='Autonomous Browser Control')
    parser.add_argument('--url', help='URL to navigate to')
    parser.add_argument('--project-id', help='Lovable project ID to verify')
    parser.add_argument('--tests', default='all', help='Tests to run (comma-separated)')
    parser.add_argument('--headless', action='store_true', default=True, help='Run headless')
    parser.add_argument('--output', default='report.json', help='Output report path')
    
    args = parser.parse_args()
    
    # Initialize operator
    operator = ScreenControlOperator(headless=args.headless)
    operator.start()
    
    try:
        if args.project_id:
            # Lovable verification workflow
            verifier = LovableVerifier(operator)
            report = verifier.verify_preview(args.project_id)
        elif args.url:
            # General navigation and inspection
            operator.navigate(args.url)
            report = {
                'timestamp': datetime.now().isoformat(),
                'url': operator.page.url,
                'state': operator.get_page_state(),
                'performance': operator.measure_performance()
            }
        else:
            print("Error: Must provide --url or --project-id")
            sys.exit(1)
        
        # Save report
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Report saved to: {args.output}")
        
        # Print summary
        if 'issues' in report:
            if report['passed']:
                print("\n✅ ALL CHECKPOINTS PASSED")
            else:
                print(f"\n❌ FOUND {len(report['issues'])} ISSUES:")
                for issue in report['issues']:
                    print(f"   - {issue}")
    
    finally:
        operator.stop()


if __name__ == '__main__':
    main()
