#!/usr/bin/env python3
"""
Exchange Mail CLI - Full email management for Microsoft Exchange/Outlook.

A Claude Code skill for managing Exchange emails from the terminal.

Commands:
  list      - List unread emails (default)
  read      - Read full email by ID
  reply     - Reply to email
  mark-read - Mark email(s) as read
  archive   - Archive email(s)

Usage:
  python3 exchange_mail.py list [--days N] [--all]
  python3 exchange_mail.py read <email_id>
  python3 exchange_mail.py reply <email_id> "<message>"
  python3 exchange_mail.py mark-read <email_id|--external|--internal|--all>
  python3 exchange_mail.py archive <email_id|--external|--internal|--all>

Environment Variables:
  EXCHANGE_SERVER   - Exchange server hostname (required)
  EXCHANGE_EMAIL    - Your email address (required)
  EXCHANGE_USERNAME - Your username (required)
  EXCHANGE_PASSWORD - Your password (required)
  EXCHANGE_DOMAIN   - Windows domain (optional)

Author: DmitryBMsk (https://github.com/DmitryBMsk)
License: MIT
"""
import os
import sys
import argparse
import json
import hashlib
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any

# Suppress SSL warnings for corporate certificates
import urllib3
urllib3.disable_warnings()

# Global connection cache
_account = None
_emails_cache = {}


def get_account():
    """Get or create Exchange account connection."""
    global _account
    if _account:
        return _account

    try:
        from exchangelib import Credentials, Account, Configuration, DELEGATE
        from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
    except ImportError:
        print("Error: exchangelib not installed.", file=sys.stderr)
        print("Run: pip install exchangelib", file=sys.stderr)
        sys.exit(1)

    # Disable SSL verification for corporate certificates
    BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter

    # Get credentials from environment
    server = os.environ.get('EXCHANGE_SERVER')
    email = os.environ.get('EXCHANGE_EMAIL')
    username = os.environ.get('EXCHANGE_USERNAME')
    password = os.environ.get('EXCHANGE_PASSWORD')
    domain = os.environ.get('EXCHANGE_DOMAIN')

    # Validate required environment variables
    missing = []
    if not server:
        missing.append('EXCHANGE_SERVER')
    if not email:
        missing.append('EXCHANGE_EMAIL')
    if not username:
        missing.append('EXCHANGE_USERNAME')
    if not password:
        missing.append('EXCHANGE_PASSWORD')

    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}", file=sys.stderr)
        print("\nRequired environment variables:", file=sys.stderr)
        print("  EXCHANGE_SERVER   - Exchange server hostname", file=sys.stderr)
        print("  EXCHANGE_EMAIL    - Your email address", file=sys.stderr)
        print("  EXCHANGE_USERNAME - Your username", file=sys.stderr)
        print("  EXCHANGE_PASSWORD - Your password", file=sys.stderr)
        sys.exit(1)

    # Build credentials
    if domain:
        username = f"{domain}\\{username}"

    credentials = Credentials(username=username, password=password)
    config = Configuration(server=server, credentials=credentials)

    try:
        _account = Account(
            primary_smtp_address=email,
            config=config,
            autodiscover=False,
            access_type=DELEGATE
        )
    except Exception as e:
        print(f"Error connecting to Exchange: {e}", file=sys.stderr)
        sys.exit(1)

    return _account


def get_internal_domain() -> str:
    """Get internal domain from email address."""
    email = os.environ.get('EXCHANGE_EMAIL', '')
    if '@' in email:
        return '@' + email.split('@')[1].lower()
    return ''


def generate_email_id(item) -> str:
    """Generate stable 8-character ID from email."""
    id_source = (item.message_id or item.id or str(item.datetime_received))
    return hashlib.md5(id_source.encode()).hexdigest()[:8]


def get_unread_emails(days_back: int = 0, show_all: bool = False) -> List[Dict[str, Any]]:
    """Fetch unread emails from Exchange."""
    global _emails_cache

    account = get_account()
    user_email = account.primary_smtp_address.lower()
    internal_domain = get_internal_domain()

    # Calculate date filter
    if days_back > 0:
        start_date = datetime.now(timezone.utc) - timedelta(days=days_back)
    else:
        start_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

    emails = []

    for item in account.inbox.filter(
        is_read=False,
        datetime_received__gte=start_date
    ).order_by('-datetime_received')[:50]:

        # Get recipients
        to_list = [r.email_address.lower() for r in (item.to_recipients or []) if r.email_address]
        cc_list = [r.email_address.lower() for r in (item.cc_recipients or []) if r.email_address]
        is_direct = user_email in to_list + cc_list

        # Skip if not direct recipient (unless --all flag)
        if not show_all and not is_direct:
            continue

        sender = item.sender.email_address if item.sender else 'Unknown'
        sender_name = item.sender.name if item.sender and item.sender.name else sender
        is_internal = sender.lower().endswith(internal_domain) if sender and internal_domain else False

        email_id = generate_email_id(item)

        email_data = {
            'id': email_id,
            'item_id': item.id,
            'message_id': item.message_id,
            'time': item.datetime_received.strftime('%H:%M') if item.datetime_received else '??:??',
            'date': item.datetime_received.strftime('%Y-%m-%d') if item.datetime_received else '',
            'sender': sender,
            'sender_name': sender_name,
            'subject': item.subject or '(No subject)',
            'preview': (item.text_body or '')[:150].replace('\n', ' ').strip(),
            'is_internal': is_internal,
            'is_direct': is_direct,
            'to': to_list[:5],
            'cc': cc_list[:5],
        }

        emails.append(email_data)
        _emails_cache[email_id] = item

    return emails


def find_email_by_id(email_id: str):
    """Find email item by short ID."""
    global _emails_cache

    if email_id in _emails_cache:
        return _emails_cache[email_id]

    # Search in recent emails
    account = get_account()
    start_date = datetime.now(timezone.utc) - timedelta(days=7)

    for item in account.inbox.filter(
        datetime_received__gte=start_date
    ).order_by('-datetime_received')[:100]:
        item_id = generate_email_id(item)
        _emails_cache[item_id] = item
        if item_id == email_id:
            return item

    return None


def cmd_list(args):
    """List unread emails."""
    emails = get_unread_emails(days_back=args.days, show_all=args.all)

    if args.json:
        print(json.dumps(emails, ensure_ascii=False, indent=2))
        return

    if not emails:
        period = f"from last {args.days} days" if args.days > 0 else "today"
        print(f"📭 No unread emails {period}")
        return

    internal = [e for e in emails if e['is_internal']]
    external = [e for e in emails if not e['is_internal']]

    period = f"from last {args.days} days" if args.days > 0 else "today"
    print(f"📧 {len(emails)} unread emails {period}:")
    print()

    if internal:
        print(f"━━━ Internal ({len(internal)}) ━━━")
        for e in internal:
            print(f"[{e['id']}] [{e['time']}] {e['sender_name']}")
            print(f"        {e['subject']}")
            if e['preview']:
                print(f"        {e['preview'][:60]}...")
            print()

    if external:
        print(f"━━━ External ({len(external)}) ━━━")
        for e in external[:10]:
            print(f"[{e['id']}] [{e['time']}] {e['sender']}")
            print(f"        {e['subject']}")
            print()
        if len(external) > 10:
            print(f"        ... and {len(external) - 10} more")

    print("─" * 50)
    print("Commands: read <id>, reply <id> \"text\", mark-read <id>, archive <id>")


def cmd_read(args):
    """Read full email content."""
    item = find_email_by_id(args.email_id)

    if not item:
        print(f"❌ Email with ID {args.email_id} not found")
        return

    sender = item.sender.email_address if item.sender else 'Unknown'
    sender_name = item.sender.name if item.sender and item.sender.name else sender

    print("=" * 60)
    print(f"📧 {item.subject or '(No subject)'}")
    print("=" * 60)
    print(f"From:  {sender_name} <{sender}>")
    print(f"Date:  {item.datetime_received.strftime('%Y-%m-%d %H:%M') if item.datetime_received else 'Unknown'}")

    to_list = [r.email_address for r in (item.to_recipients or []) if r.email_address]
    if to_list:
        print(f"To:    {', '.join(to_list[:5])}")

    cc_list = [r.email_address for r in (item.cc_recipients or []) if r.email_address]
    if cc_list:
        print(f"CC:    {', '.join(cc_list[:5])}")

    print("-" * 60)

    body = item.text_body or item.body or ''
    if hasattr(body, 'text'):
        body = body.text or ''

    body = body.strip()
    if len(body) > 3000:
        body = body[:3000] + "\n\n... [truncated, email too long]"

    print(body if body else "(Empty email)")
    print("=" * 60)
    print(f"\nID for reply: {args.email_id}")
    print(f"Commands: reply {args.email_id} \"text\", mark-read {args.email_id}, archive {args.email_id}")


def cmd_reply(args):
    """Reply to email."""
    item = find_email_by_id(args.email_id)

    if not item:
        print(f"❌ Email with ID {args.email_id} not found")
        return

    reply_body = args.message

    # Add original message quote
    original_sender = item.sender.email_address if item.sender else 'Unknown'
    original_date = item.datetime_received.strftime('%Y-%m-%d %H:%M') if item.datetime_received else ''
    original_body = (item.text_body or '')[:500]

    full_body = f"""{reply_body}

---
{original_date}, {original_sender} wrote:
> {original_body.replace(chr(10), chr(10) + '> ')}
"""

    try:
        subject = item.subject or ''
        if not subject.lower().startswith('re:'):
            subject = f"Re: {subject}"

        item.reply(
            subject=subject,
            body=full_body,
            to_recipients=[item.sender] if item.sender else None
        )
        print(f"✅ Reply sent to {original_sender}")
        print(f"   Subject: {subject}")
    except Exception as e:
        print(f"❌ Send error: {e}")


def cmd_mark_read(args):
    """Mark email(s) as read."""
    batch_mode = args.external or args.internal or args.all_emails

    if batch_mode:
        emails = get_unread_emails(days_back=args.days, show_all=True)

        if args.external:
            emails = [e for e in emails if not e['is_internal']]
            mode_name = "external"
        elif args.internal:
            emails = [e for e in emails if e['is_internal']]
            mode_name = "internal"
        else:
            mode_name = "all"

        if not emails:
            print(f"📭 No {mode_name} emails to process")
            return

        count = 0
        for e in emails:
            item = find_email_by_id(e['id'])
            if item:
                item.is_read = True
                item.save(update_fields=['is_read'])
                count += 1

        print(f"✅ Marked as read: {count} {mode_name} emails")
    elif args.target:
        item = find_email_by_id(args.target)
        if not item:
            print(f"❌ Email with ID {args.target} not found")
            return

        item.is_read = True
        item.save(update_fields=['is_read'])
        print(f"✅ Email {args.target} marked as read")
    else:
        print("❌ Specify email ID or flag --external/--internal/--all")


def cmd_archive(args):
    """Archive email(s) - move to Archive folder."""
    account = get_account()

    # Find archive folder
    from exchangelib import Folder

    archive_folder = None
    for folder in account.root.walk():
        if folder.name.lower() in ['archive', 'архив', 'deleted items', 'удаленные']:
            archive_folder = folder
            break

    if not archive_folder:
        try:
            archive_folder = account.trash
        except:
            archive_folder = Folder(parent=account.inbox.parent, name='Archive')
            archive_folder.save()
            print("📁 Created Archive folder")

    batch_mode = args.external or args.internal or args.all_emails

    if batch_mode:
        emails = get_unread_emails(days_back=args.days, show_all=True)

        if args.external:
            emails = [e for e in emails if not e['is_internal']]
            mode_name = "external"
        elif args.internal:
            emails = [e for e in emails if e['is_internal']]
            mode_name = "internal"
        else:
            mode_name = "all"

        if not emails:
            print(f"📭 No {mode_name} emails to archive")
            return

        count = 0
        errors = 0
        for e in emails:
            item = find_email_by_id(e['id'])
            if item:
                try:
                    item.move(archive_folder)
                    count += 1
                except Exception:
                    errors += 1

        result = f"✅ Archived: {count} {mode_name} emails"
        if errors:
            result += f" (errors: {errors})"
        print(result)
    elif args.target:
        item = find_email_by_id(args.target)
        if not item:
            print(f"❌ Email with ID {args.target} not found")
            return

        try:
            item.move(archive_folder)
            print(f"✅ Email {args.target} archived")
        except Exception as e:
            print(f"❌ Archive error: {e}")
    else:
        print("❌ Specify email ID or flag --external/--internal/--all")


def main():
    parser = argparse.ArgumentParser(
        description='Exchange Mail CLI - Manage Exchange emails from terminal',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                      # Today's unread emails
  %(prog)s list --days 3             # Last 3 days
  %(prog)s read abc123               # Read email
  %(prog)s reply abc123 "Thanks!"    # Reply to email
  %(prog)s mark-read abc123          # Mark as read
  %(prog)s mark-read --external      # All external as read
  %(prog)s archive --external        # Archive all external
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command')

    # list command
    list_parser = subparsers.add_parser('list', help='List unread emails')
    list_parser.add_argument('--days', type=int, default=0, help='Days back (0=today)')
    list_parser.add_argument('--all', action='store_true', help='All emails (not just To/CC)')
    list_parser.add_argument('--json', action='store_true', help='JSON output')

    # read command
    read_parser = subparsers.add_parser('read', help='Read email')
    read_parser.add_argument('email_id', help='Email ID')

    # reply command
    reply_parser = subparsers.add_parser('reply', help='Reply to email')
    reply_parser.add_argument('email_id', help='Email ID')
    reply_parser.add_argument('message', help='Reply message')

    # mark-read command
    markread_parser = subparsers.add_parser('mark-read', help='Mark as read')
    markread_parser.add_argument('target', nargs='?', default=None, help='Email ID')
    markread_parser.add_argument('--external', action='store_true', help='All external')
    markread_parser.add_argument('--internal', action='store_true', help='All internal')
    markread_parser.add_argument('--all', action='store_true', dest='all_emails', help='All emails')
    markread_parser.add_argument('--days', type=int, default=0, help='Days back for batch')

    # archive command
    archive_parser = subparsers.add_parser('archive', help='Archive emails')
    archive_parser.add_argument('target', nargs='?', default=None, help='Email ID')
    archive_parser.add_argument('--external', action='store_true', help='All external')
    archive_parser.add_argument('--internal', action='store_true', help='All internal')
    archive_parser.add_argument('--all', action='store_true', dest='all_emails', help='All emails')
    archive_parser.add_argument('--days', type=int, default=0, help='Days back for batch')

    args = parser.parse_args()

    if not args.command or args.command == 'list':
        if not hasattr(args, 'days'):
            args.days = 0
            args.all = False
            args.json = False
        cmd_list(args)
    elif args.command == 'read':
        cmd_read(args)
    elif args.command == 'reply':
        cmd_reply(args)
    elif args.command == 'mark-read':
        cmd_mark_read(args)
    elif args.command == 'archive':
        cmd_archive(args)


if __name__ == '__main__':
    main()
