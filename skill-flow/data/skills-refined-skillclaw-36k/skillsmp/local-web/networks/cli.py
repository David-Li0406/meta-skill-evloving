#!/usr/bin/env python3
"""
Networks CLI - Network utilities from the command line
"""
import argparse
import json
import sys
from pathlib import Path
from networks.core import (
    get_lan_ip,
    get_all_ips,
    get_network_info,
    ensure_port_accessible,
    check_port_open,
    get_wsl2_host_ip,
    get_wsl2_network_info,
    list_port_forwards,
    remove_port_forward,
)
from networks.local_web import (
    fetch_url,
    screenshot_url,
    check_local_access,
    interact_with_page,
    crawl_site,
    list_elements,
)


def cmd_ip(args):
    """Show LAN IP address"""
    ip = get_lan_ip()
    if ip:
        print(ip)
        return 0
    else:
        print("Could not determine LAN IP", file=sys.stderr)
        return 1


def cmd_info(args):
    """Show comprehensive network information"""
    info = get_network_info()

    if args.json:
        print(json.dumps(info, indent=2, default=str))
    else:
        print(f"LAN IP:     {info['lan_ip']}")
        print(f"Hostname:   {info['hostname']}")
        print(f"Is WSL2:    {info['is_wsl']}")

        if info['is_wsl']:
            print(f"Host IP:    {info['wsl_host_ip']}")

        print(f"\nAll interfaces:")
        for iface in info['all_ips']:
            print(f"  {iface['interface']:15} {iface['ip']}")

    return 0


def cmd_ensure(args):
    """Ensure port is accessible on LAN"""
    success, message = ensure_port_accessible(
        args.port,
        protocol=args.protocol,
        name=args.name
    )

    print(message)

    if success:
        ip = get_lan_ip()
        if ip:
            print(f"\n✓ Access from LAN: http://{ip}:{args.port}")
        return 0
    else:
        return 1


def cmd_check(args):
    """Check if a port is open"""
    is_open = check_port_open(args.host, args.port, timeout=args.timeout)

    if is_open:
        print(f"✓ {args.host}:{args.port} is OPEN")
        return 0
    else:
        print(f"✗ {args.host}:{args.port} is CLOSED")
        return 1


def cmd_wsl_host(args):
    """Get WSL2 Windows host IP"""
    ip = get_wsl2_host_ip()
    if ip:
        print(ip)
        return 0
    else:
        print("Not running in WSL2 or could not determine host IP", file=sys.stderr)
        return 1


def cmd_wsl_info(args):
    """Show detailed WSL2 network information"""
    info = get_wsl2_network_info()
    if not info:
        print("Not running in WSL2", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(info, indent=2, default=str))
    else:
        print("WSL2 Network Information")
        print("=" * 70)
        print(f"WSL2 IP:        {info['wsl2_ip']}")
        print(f"Windows Host:   {info['windows_host_ip']} (WSL2 gateway)")
        print(f"Windows LAN:    {info['windows_lan_ip']} (accessible from network)")
        print()

        if info['port_forwards']:
            print("Port Forwarding Rules:")
            print(f"{'Listen':<20} {'Forward To':<25} {'Port':<10}")
            print("-" * 70)
            for fwd in info['port_forwards']:
                listen = f"{fwd['listen_address']}:{fwd['listen_port']}"
                forward_to = f"{fwd['connect_address']}:{fwd['connect_port']}"
                print(f"{listen:<20} → {forward_to:<23} {fwd['listen_port']:<10}")
        else:
            print("No port forwarding rules configured")

    return 0


def cmd_port_list(args):
    """List port forwarding rules"""
    forwards = list_port_forwards()

    if not forwards:
        print("No port forwarding rules found")
        return 0

    if args.json:
        print(json.dumps(forwards, indent=2))
    else:
        print(f"{'Listen Address':<20} {'Port':<10} {'→':<5} {'WSL2 Address':<20} {'Port':<10}")
        print("=" * 70)
        for fwd in forwards:
            print(f"{fwd['listen_address']:<20} {fwd['listen_port']:<10} {'→':<5} {fwd['connect_address']:<20} {fwd['connect_port']:<10}")

    return 0


def cmd_port_remove(args):
    """Remove a port forwarding rule"""
    success, message = remove_port_forward(args.port)
    print(message)
    return 0 if success else 1


# ============== Local Web Commands ==============
# These commands access local/LAN URLs that cloud AI tools cannot reach

def cmd_web_fetch(args):
    """Fetch HTML content from a local/LAN URL"""
    result = fetch_url(
        args.url,
        timeout=args.timeout,
        include_headers=args.headers,
        verify_ssl=not args.insecure,
    )

    if args.json:
        print(result.to_json())
    elif args.content_only and result.success:
        print(result.content)
    else:
        print(result.to_human())

    return 0 if result.success else 1


def cmd_web_screenshot(args):
    """Take a screenshot of a local/LAN URL"""
    output_path = Path(args.output) if args.output else None

    result = screenshot_url(
        args.url,
        output_path=output_path,
        width=args.width,
        height=args.height,
        full_page=not args.viewport_only,
        timeout=args.timeout,
        include_base64=args.base64,
        browser=args.browser,
    )

    if args.json:
        print(result.to_json())
    else:
        print(result.to_human())

    return 0 if result.success else 1


def cmd_web_check(args):
    """Check if a local/LAN URL is accessible"""
    accessible, message = check_local_access(args.url, timeout=args.timeout)

    if args.json:
        print(json.dumps({
            'url': args.url,
            'accessible': accessible,
            'message': message,
        }, indent=2))
    else:
        print(message)

    return 0 if accessible else 1


def cmd_web_interact(args):
    """Interact with webpage elements"""
    result = interact_with_page(
        args.url,
        action=args.action,
        selector=args.selector,
        text=args.text,
        wait_after=args.wait,
        timeout=args.timeout,
        browser=args.browser,
    )

    if args.json:
        print(result.to_json())
    else:
        print(result.to_human())
        if result.success:
            if result.before_screenshot:
                print(f"  Before: {result.before_screenshot}")
            if result.after_screenshot:
                print(f"  After: {result.after_screenshot}")

    return 0 if result.success else 1


def cmd_web_crawl(args):
    """Crawl a website"""
    output_dir = Path(args.output_dir) if args.output_dir else None
    
    result = crawl_site(
        args.url,
        max_pages=args.max_pages,
        screenshot_each=not args.no_screenshots,
        timeout=args.timeout,
        output_dir=output_dir,
        browser=args.browser,
    )

    if args.json:
        print(result.to_json())
    else:
        print(result.to_human())

    return 0 if result.success else 1


def cmd_web_list(args):
    """List interactive elements on a page"""
    result = list_elements(
        args.url,
        element_type=args.element_type,
        timeout=args.timeout,
        browser=args.browser,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result.get('success'):
            print(f"Found {result['count']} {args.element_type} elements on {args.url}:")
            for i, el in enumerate(result.get('elements', [])[:50]):
                text = el.get('text', '').strip()[:40] or el.get('id') or el.get('name') or '(no text)'
                selector = f"#{el['id']}" if el.get('id') else f".{el['class'].split()[0]}" if el.get('class') else el['tag']
                print(f"  {i+1}. [{el['tag']}] {text} → {selector}")
            if result['count'] > 50:
                print(f"  ... and {result['count'] - 50} more")
        else:
            print(f"Error: {result.get('error')}")

    return 0 if result.get('success') else 1


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Network utilities - cross-platform networking tools",
        prog='networks'
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # networks ip - Show LAN IP
    parser_ip = subparsers.add_parser('ip', help='Show LAN IP address')
    parser_ip.set_defaults(func=cmd_ip)

    # networks info - Show all network info
    parser_info = subparsers.add_parser('info', help='Show network information')
    parser_info.add_argument(
        '-j', '--json',
        action='store_true',
        help='Output as JSON'
    )
    parser_info.set_defaults(func=cmd_info)

    # networks ensure - Make port accessible
    parser_ensure = subparsers.add_parser('ensure', help='Ensure port is accessible on LAN')
    parser_ensure.add_argument(
        '-p', '--port',
        type=int,
        required=True,
        help='Port number'
    )
    parser_ensure.add_argument(
        '-t', '--protocol',
        default='tcp',
        choices=['tcp', 'udp'],
        help='Protocol (default: tcp)'
    )
    parser_ensure.add_argument(
        '-n', '--name',
        default=None,
        help='Name for firewall rule'
    )
    parser_ensure.set_defaults(func=cmd_ensure)

    # networks check - Check if port is open
    parser_check = subparsers.add_parser('check', help='Check if a port is open')
    parser_check.add_argument(
        '-H', '--host',
        required=True,
        help='Hostname or IP address'
    )
    parser_check.add_argument(
        '-p', '--port',
        type=int,
        required=True,
        help='Port number'
    )
    parser_check.add_argument(
        '-t', '--timeout',
        type=float,
        default=2.0,
        help='Timeout in seconds (default: 2.0)'
    )
    parser_check.set_defaults(func=cmd_check)

    # networks wsl-host - Get WSL2 host IP
    parser_wsl = subparsers.add_parser('wsl-host', help='Get WSL2 Windows host IP')
    parser_wsl.set_defaults(func=cmd_wsl_host)

    # networks wsl-info - Show detailed WSL2 network info
    parser_wsl_info = subparsers.add_parser('wsl-info', help='Show detailed WSL2 network information')
    parser_wsl_info.add_argument(
        '-j', '--json',
        action='store_true',
        help='Output as JSON'
    )
    parser_wsl_info.set_defaults(func=cmd_wsl_info)

    # networks port-list - List port forwarding rules
    parser_port_list = subparsers.add_parser('port-list', help='List port forwarding rules (WSL2)')
    parser_port_list.add_argument(
        '-j', '--json',
        action='store_true',
        help='Output as JSON'
    )
    parser_port_list.set_defaults(func=cmd_port_list)

    # networks port-remove - Remove port forwarding rule
    parser_port_remove = subparsers.add_parser('port-remove', help='Remove port forwarding rule (WSL2)')
    parser_port_remove.add_argument(
        '-p', '--port',
        type=int,
        required=True,
        help='Port number to remove'
    )
    parser_port_remove.set_defaults(func=cmd_port_remove)

    # ============== Local Web Commands ==============
    # Access local/LAN URLs that cloud AI tools cannot reach

    # networks web-fetch - Fetch HTML from local URL
    parser_web_fetch = subparsers.add_parser(
        'web-fetch',
        help='Fetch HTML from local/LAN URL (AI tools cannot access these)',
        description='Fetch HTML content from URLs on your local network that cloud AI tools cannot reach.'
    )
    parser_web_fetch.add_argument(
        'url',
        help='URL to fetch (e.g., http://192.168.1.100:3000/)'
    )
    parser_web_fetch.add_argument(
        '-t', '--timeout',
        type=float,
        default=10.0,
        help='Request timeout in seconds (default: 10)'
    )
    parser_web_fetch.add_argument(
        '-j', '--json',
        action='store_true',
        help='Output as JSON (LLM-optimized)'
    )
    parser_web_fetch.add_argument(
        '-c', '--content-only',
        action='store_true',
        help='Output only the HTML content (no metadata)'
    )
    parser_web_fetch.add_argument(
        '-H', '--headers',
        action='store_true',
        help='Include response headers in output'
    )
    parser_web_fetch.add_argument(
        '-k', '--insecure',
        action='store_true',
        help='Skip SSL certificate verification (for self-signed certs)'
    )
    parser_web_fetch.set_defaults(func=cmd_web_fetch)

    # networks web-screenshot - Screenshot local URL
    parser_web_ss = subparsers.add_parser(
        'web-screenshot',
        help='Take screenshot of local/LAN URL (requires playwright)',
        description='Capture a visual screenshot of a local/LAN webpage. Requires: pip install playwright && playwright install chromium'
    )
    parser_web_ss.add_argument(
        'url',
        help='URL to screenshot'
    )
    parser_web_ss.add_argument(
        '-o', '--output',
        help='Output file path (default: temp file)'
    )
    parser_web_ss.add_argument(
        '-w', '--width',
        type=int,
        default=1280,
        help='Viewport width (default: 1280)'
    )
    parser_web_ss.add_argument(
        '-H', '--height',
        type=int,
        default=720,
        help='Viewport height (default: 720)'
    )
    parser_web_ss.add_argument(
        '-v', '--viewport-only',
        action='store_true',
        help='Only capture viewport (not full page)'
    )
    parser_web_ss.add_argument(
        '-t', '--timeout',
        type=float,
        default=30.0,
        help='Page load timeout in seconds (default: 30)'
    )
    parser_web_ss.add_argument(
        '-b', '--base64',
        action='store_true',
        help='Include base64-encoded image in output (for inline LLM viewing)'
    )
    parser_web_ss.add_argument(
        '-j', '--json',
        action='store_true',
        help='Output as JSON'
    )
    parser_web_ss.add_argument(
        '-B', '--browser',
        choices=['firefox', 'chromium', 'webkit'],
        default='firefox',
        help='Browser to use (default: firefox)'
    )
    parser_web_ss.set_defaults(func=cmd_web_screenshot)

    # networks web-check - Check if local URL is accessible
    parser_web_check = subparsers.add_parser(
        'web-check',
        help='Check if local/LAN URL is accessible',
        description='Quick connectivity check for local URLs.'
    )
    parser_web_check.add_argument(
        'url',
        help='URL to check'
    )
    parser_web_check.add_argument(
        '-t', '--timeout',
        type=float,
        default=5.0,
        help='Connection timeout in seconds (default: 5)'
    )
    parser_web_check.add_argument(
        '-j', '--json',
        action='store_true',
        help='Output as JSON'
    )
    parser_web_check.set_defaults(func=cmd_web_check)

    # networks web-interact - Interact with page elements
    parser_web_interact = subparsers.add_parser(
        'web-interact',
        help='Interact with webpage elements (click, type, hover)',
        description='Use headless browser to interact with page elements and observe effects.'
    )
    parser_web_interact.add_argument(
        'url',
        help='URL to interact with'
    )
    parser_web_interact.add_argument(
        '-a', '--action',
        choices=['click', 'type', 'hover', 'scroll', 'wait'],
        default='click',
        help='Action to perform (default: click)'
    )
    parser_web_interact.add_argument(
        '-s', '--selector',
        help='CSS selector or text to find element'
    )
    parser_web_interact.add_argument(
        '-T', '--text',
        help='Text to type (for type action) or text content to find'
    )
    parser_web_interact.add_argument(
        '-w', '--wait',
        type=float,
        default=1.0,
        help='Seconds to wait after action (default: 1)'
    )
    parser_web_interact.add_argument(
        '-t', '--timeout',
        type=float,
        default=30.0,
        help='Page load timeout (default: 30)'
    )
    parser_web_interact.add_argument(
        '-j', '--json',
        action='store_true',
        help='Output as JSON'
    )
    parser_web_interact.add_argument(
        '-B', '--browser',
        choices=['firefox', 'chromium', 'webkit'],
        default='firefox',
        help='Browser to use (default: firefox)'
    )
    parser_web_interact.set_defaults(func=cmd_web_interact)

    # networks web-crawl - Crawl a site
    parser_web_crawl = subparsers.add_parser(
        'web-crawl',
        help='Crawl a website, discover pages, take screenshots',
        description='Automatically crawl a site, capturing screenshots of each page.'
    )
    parser_web_crawl.add_argument(
        'url',
        help='Starting URL'
    )
    parser_web_crawl.add_argument(
        '-n', '--max-pages',
        type=int,
        default=20,
        help='Maximum pages to crawl (default: 20)'
    )
    parser_web_crawl.add_argument(
        '-o', '--output-dir',
        help='Directory to save screenshots'
    )
    parser_web_crawl.add_argument(
        '--no-screenshots',
        action='store_true',
        help='Skip screenshots (faster)'
    )
    parser_web_crawl.add_argument(
        '-t', '--timeout',
        type=float,
        default=30.0,
        help='Timeout per page (default: 30)'
    )
    parser_web_crawl.add_argument(
        '-j', '--json',
        action='store_true',
        help='Output as JSON'
    )
    parser_web_crawl.add_argument(
        '-B', '--browser',
        choices=['firefox', 'chromium', 'webkit'],
        default='firefox',
        help='Browser to use (default: firefox)'
    )
    parser_web_crawl.set_defaults(func=cmd_web_crawl)

    # networks web-list - List interactive elements
    parser_web_list = subparsers.add_parser(
        'web-list',
        help='List interactive elements on a page',
        description='Find buttons, links, inputs, and forms on a webpage.'
    )
    parser_web_list.add_argument(
        'url',
        help='URL to analyze'
    )
    parser_web_list.add_argument(
        '-e', '--element-type',
        choices=['button', 'link', 'input', 'form', 'all'],
        default='all',
        help='Type of elements to find (default: all)'
    )
    parser_web_list.add_argument(
        '-t', '--timeout',
        type=float,
        default=30.0,
        help='Page load timeout (default: 30)'
    )
    parser_web_list.add_argument(
        '-j', '--json',
        action='store_true',
        help='Output as JSON'
    )
    parser_web_list.add_argument(
        '-B', '--browser',
        choices=['firefox', 'chromium', 'webkit'],
        default='firefox',
        help='Browser to use (default: firefox)'
    )
    parser_web_list.set_defaults(func=cmd_web_list)

    # Parse args
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Run command
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
