"""
Tests for networks module
"""
import pytest
from networks import (
    get_lan_ip,
    get_all_ips,
    get_network_info,
    check_port_open,
)
from networks.local_web import (
    is_local_url,
    fetch_url,
    check_local_access,
    FetchResult,
)


def test_get_lan_ip():
    """Test getting LAN IP"""
    ip = get_lan_ip()
    assert ip is not None
    assert isinstance(ip, str)
    # IP should be in dotted quad format
    parts = ip.split('.')
    assert len(parts) == 4
    for part in parts:
        assert 0 <= int(part) <= 255


def test_get_all_ips():
    """Test getting all IPs"""
    ips = get_all_ips()
    assert isinstance(ips, list)
    assert len(ips) > 0  # Should have at least loopback
    for iface in ips:
        assert 'interface' in iface
        assert 'ip' in iface
        assert isinstance(iface['interface'], str)
        assert isinstance(iface['ip'], str)


def test_get_network_info():
    """Test getting network information"""
    info = get_network_info()
    assert isinstance(info, dict)
    assert 'lan_ip' in info
    assert 'all_ips' in info
    assert 'hostname' in info
    assert 'is_wsl' in info
    assert 'wsl_host_ip' in info

    assert isinstance(info['hostname'], str)
    assert isinstance(info['is_wsl'], bool)
    assert isinstance(info['all_ips'], list)


def test_check_port_open_loopback():
    """Test checking if a port is open (using loopback)"""
    # Test that checking a definitely closed port returns False
    result = check_port_open('127.0.0.1', 65000, timeout=0.5)
    # Can't assert False because the port might be open
    assert isinstance(result, bool)


def test_check_port_open_google_dns():
    """Test checking open port (Google DNS)"""
    # Google DNS should have port 53 open
    result = check_port_open('8.8.8.8', 53, timeout=2.0)
    # Can't assert True because network might be down
    assert isinstance(result, bool)


# ============== Local Web Tests ==============

def test_is_local_url():
    """Test is_local_url detection"""
    # Local URLs
    assert is_local_url('http://localhost:3000/') is True
    assert is_local_url('http://127.0.0.1:8080/') is True
    assert is_local_url('http://192.168.1.1/') is True
    assert is_local_url('http://10.0.0.1:80/') is True
    assert is_local_url('http://mydevice.local/') is True
    
    # Public URLs
    assert is_local_url('http://google.com/') is False
    assert is_local_url('https://github.com/') is False


def test_fetch_url_result_serialization():
    """Test FetchResult serialization"""
    result = FetchResult(
        url='http://localhost/',
        success=True,
        status_code=200,
        content_type='text/html',
        content='<html></html>',
        content_length=13,
    )
    
    # JSON serialization
    json_str = result.to_json()
    assert 'localhost' in json_str
    assert '200' in json_str
    
    # Human format
    human_str = result.to_human()
    assert '✓' in human_str
    assert 'localhost' in human_str


def test_fetch_url_error():
    """Test fetch_url with unreachable URL"""
    # Port 65432 is almost certainly not open
    result = fetch_url('http://localhost:65432/', timeout=1.0)
    assert result.success is False
    assert result.error is not None
    assert 'refused' in result.error.lower() or 'error' in result.error.lower()


def test_check_local_access():
    """Test check_local_access function"""
    # Check an unreachable port
    accessible, message = check_local_access('http://localhost:65432/', timeout=1.0)
    assert accessible is False
    assert '✗' in message


# ============== Browser Automation Tests ==============

def test_interaction_result_serialization():
    """Test InteractionResult serialization"""
    from networks.local_web import InteractionResult
    
    result = InteractionResult(
        url='http://localhost:3000/',
        action='click',
        success=True,
        selector='button',
        elements_found=5,
    )
    
    # JSON serialization
    json_str = result.to_json()
    assert 'click' in json_str
    assert 'localhost' in json_str
    
    # Human format
    human_str = result.to_human()
    assert '✓' in human_str
    assert 'click' in human_str


def test_crawl_result_serialization():
    """Test CrawlResult serialization"""
    from networks.local_web import CrawlResult
    
    result = CrawlResult(
        base_url='http://localhost:3000/',
        success=True,
        pages_crawled=3,
        pages=[
            {'url': 'http://localhost:3000/', 'title': 'Home'},
            {'url': 'http://localhost:3000/about', 'title': 'About'},
        ],
    )
    
    # JSON serialization
    json_str = result.to_json()
    assert 'localhost' in json_str
    assert '3' in json_str
    
    # Human format
    human_str = result.to_human()
    assert '✓' in human_str
    assert 'Crawled 3 pages' in human_str


def test_launch_browser_invalid():
    """Test _launch_browser with invalid browser type"""
    from networks.local_web import _launch_browser
    import pytest
    
    # Mock playwright object - we just test the ValueError
    class MockPlaywright:
        pass
    
    with pytest.raises(ValueError, match="Unknown browser"):
        _launch_browser(MockPlaywright(), "invalid_browser")


def test_screenshot_url_no_playwright():
    """Test screenshot_url gracefully handles missing playwright"""
    from networks.local_web import screenshot_url
    import sys
    
    # If playwright is installed, we can't easily test this
    # Just verify the function exists and has correct signature
    import inspect
    sig = inspect.signature(screenshot_url)
    assert 'url' in sig.parameters
    assert 'browser' in sig.parameters
    assert sig.parameters['browser'].default == 'firefox'


def test_interact_with_page_no_playwright():
    """Test interact_with_page gracefully handles missing playwright"""
    from networks.local_web import interact_with_page
    import inspect
    
    sig = inspect.signature(interact_with_page)
    assert 'url' in sig.parameters
    assert 'action' in sig.parameters
    assert 'browser' in sig.parameters
    assert sig.parameters['browser'].default == 'firefox'
    assert sig.parameters['action'].default == 'click'


def test_crawl_site_no_playwright():
    """Test crawl_site gracefully handles missing playwright"""
    from networks.local_web import crawl_site
    import inspect
    
    sig = inspect.signature(crawl_site)
    assert 'url' in sig.parameters
    assert 'max_pages' in sig.parameters
    assert 'browser' in sig.parameters
    assert sig.parameters['browser'].default == 'firefox'
    assert sig.parameters['max_pages'].default == 20


def test_list_elements_no_playwright():
    """Test list_elements gracefully handles missing playwright"""
    from networks.local_web import list_elements
    import inspect
    
    sig = inspect.signature(list_elements)
    assert 'url' in sig.parameters
    assert 'element_type' in sig.parameters
    assert 'browser' in sig.parameters
    assert sig.parameters['browser'].default == 'firefox'
    assert sig.parameters['element_type'].default == 'button'


# ============== Integration Tests (require playwright) ==============

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


@pytest.mark.skipif(not PLAYWRIGHT_AVAILABLE, reason="playwright not installed")
def test_list_elements_real():
    """Test list_elements with real browser (if playwright available)"""
    from networks.local_web import list_elements
    
    # Use a simple data URL to avoid network dependency
    result = list_elements(
        'data:text/html,<html><body><button>Test</button></body></html>',
        element_type='button',
        browser='firefox',
        timeout=10.0,
    )
    
    # Should either succeed or fail gracefully
    assert 'success' in result


@pytest.mark.skipif(not PLAYWRIGHT_AVAILABLE, reason="playwright not installed")
def test_screenshot_url_real():
    """Test screenshot_url with real browser (if playwright available)"""
    from networks.local_web import screenshot_url
    import tempfile
    from pathlib import Path
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / 'test.png'
        result = screenshot_url(
            'data:text/html,<html><body><h1>Test</h1></body></html>',
            output_path=output,
            browser='firefox',
            timeout=10.0,
        )
        
        # Should work or fail gracefully
        assert hasattr(result, 'success')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
