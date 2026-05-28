#!/usr/bin/env python3
import csv
import sys
from collections import defaultdict

# Account group mappings
ACCOUNT_GROUPS = {
    'Galicia': ['Galicia Mas - Caja de ahorro'],
    'Mercado Pago': ['Mercado Pago'],
    'Quiena': ['Quiena'],
    'LLC': ['Relay Checking Account', 'Relay Saving Account'],
    'HSBC': ['HSBC Current Account', 'HSBC Saving Account'],
    'Crypto': ['Fiwind', 'Uglycash', 'Nexo']
}

def parse_csv(filepath):
    transactions = []
    unknown_accounts = set()

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            # Convert amount to float
            try:
                row['amount'] = float(row['amount'].replace(',', '.'))
            except (ValueError, AttributeError):
                row['amount'] = 0.0

            # Normalize boolean transfer field
            row['transfer'] = row.get('transfer', '').lower() == 'true'

            transactions.append(row)

            # Check for unknown accounts
            account = row['account']
            is_known = any(account in accounts for accounts in ACCOUNT_GROUPS.values())
            if not is_known:
                unknown_accounts.add(account)

    return transactions, unknown_accounts

def find_internal_transfer_pairs(transactions, account_names):
    """Find pairs of transactions that represent internal transfers within the same account group."""
    internal_transfer_ids = set()

    # Get all transfers within this account group
    transfers = [t for t in transactions
                if t['account'] in account_names and t['transfer']]

    # Find matching pairs: same amount (opposite sign), same date, same currency
    for i, t1 in enumerate(transfers):
        for t2 in transfers[i+1:]:
            # Check if they form a transfer pair
            if (t1['date'] == t2['date'] and
                t1['currency'] == t2['currency'] and
                abs(t1['amount'] + t2['amount']) < 0.01):  # Same amount, opposite signs

                # Both transactions are internal transfers
                internal_transfer_ids.add(id(t1))
                internal_transfer_ids.add(id(t2))

    return internal_transfer_ids

def filter_transactions(transactions, account_names=None, transfer=None,
                        transaction_type=None, category=None, currency=None,
                        exclude_internal_transfers=False):
    filtered = transactions

    if account_names:
        filtered = [t for t in filtered if t['account'] in account_names]

    if transfer is not None:
        filtered = [t for t in filtered if t['transfer'] == transfer]

    if transaction_type:
        filtered = [t for t in filtered if t['type'] == transaction_type]

    if category:
        filtered = [t for t in filtered if t['category'] == category]

    if currency:
        filtered = [t for t in filtered if t['currency'] == currency]

    # Exclude internal transfers within the same account group
    if exclude_internal_transfers and account_names:
        internal_ids = find_internal_transfer_pairs(transactions, account_names)
        filtered = [t for t in filtered if id(t) not in internal_ids]

    return filtered

def calculate_sum(transactions):
    return sum(t['amount'] for t in transactions)

def show_group_details(transactions, group_name):
    """Show detailed breakdown of transactions for a specific account group."""
    if group_name not in ACCOUNT_GROUPS:
        print(f"\n❌ Unknown group: {group_name}")
        print(f"Available groups: {', '.join(ACCOUNT_GROUPS.keys())}")
        return

    accounts = ACCOUNT_GROUPS[group_name]
    group_txns = [t for t in transactions if t['account'] in accounts]

    if not group_txns:
        print(f"\n⚠️  No transactions found for group: {group_name}")
        return

    # Sort by date
    group_txns.sort(key=lambda t: t['date'])

    print(f"\n╔════════════════════════════════════════════════════════════════════════════════╗")
    print(f"║  {group_name.upper()} - DETAILED TRANSACTIONS{' ' * (62 - len(group_name))}║")
    print("╠════════════════════════════════════════════════════════════════════════════════╣")
    print("║ Date       | Account                   | Currency |    Amount | Type      | Note      ║")
    print("╠════════════════════════════════════════════════════════════════════════════════╣")

    total_ars = 0
    total_usd = 0

    for t in group_txns:
        note = t.get('note', '')[:10]
        transfer_marker = " [T]" if t['transfer'] else "    "
        type_str = f"{t['type'][:10]}{transfer_marker}"

        print(f"║ {t['date'][:10]} | {t['account'][:25]:<25} | {t['currency']:>8} | {t['amount']:>9.2f} | {type_str:<13} | {note:<10}║")

        if t['currency'] == 'ARS':
            total_ars += t['amount']
        elif t['currency'] == 'USD':
            total_usd += t['amount']

    print("╠════════════════════════════════════════════════════════════════════════════════╣")

    if total_ars != 0:
        print(f"║ TOTAL ARS: {total_ars:>10.2f}                                                           ║")

    if total_usd != 0:
        print(f"║ TOTAL USD: {total_usd:>10.2f}                                                           ║")

    print("╚════════════════════════════════════════════════════════════════════════════════╝")

def main():
    if len(sys.argv) < 2:
        print("Usage: python process_transactions.py <csv_path> [--details=GROUP]")
        print("Available groups: Galicia, Mercado Pago, Quiena, LLC, HSBC, Crypto")
        sys.exit(1)

    filepath = sys.argv[1]

    # Check for --details flag with group name
    detail_group = None
    for arg in sys.argv[2:]:
        if arg.startswith('--details='):
            detail_group = arg.split('=', 1)[1]
            break

    transactions, unknown_accounts = parse_csv(filepath)

    if unknown_accounts:
        print("⚠️  WARNING: Unknown accounts found:")
        for account in sorted(unknown_accounts):
            print(f"  - {account}")
        print()

    results = []

    # 1. Bank account (ARS) - Galicia
    galicia_txns = filter_transactions(transactions,
                                       account_names=ACCOUNT_GROUPS['Galicia'],
                                       currency='ARS')
    results.append(('Bank account (ARS)', calculate_sum(galicia_txns), len(galicia_txns)))

    # 2. Mercado Pago FCI (ARS)
    mp_txns = filter_transactions(transactions,
                                  account_names=ACCOUNT_GROUPS['Mercado Pago'],
                                  currency='ARS')
    results.append(('Mercado Pago FCI (ARS)', calculate_sum(mp_txns), len(mp_txns)))

    # 3. Quiena - Posición (USD)
    quiena_position = filter_transactions(transactions,
                                         account_names=ACCOUNT_GROUPS['Quiena'],
                                         transfer=True,
                                         transaction_type='Income',
                                         currency='USD')
    results.append(('Quiena - Posición (USD)', calculate_sum(quiena_position), len(quiena_position)))

    # 4. Quiena - Incremento de valor (USD)
    quiena_increment = filter_transactions(transactions,
                                          account_names=ACCOUNT_GROUPS['Quiena'],
                                          category='Financial investments',
                                          transfer=False,
                                          currency='USD')
    results.append(('Quiena - Incremento de valor (USD)', calculate_sum(quiena_increment), len(quiena_increment)))

    # 5. Quiena - Dividendos (USD)
    results.append(('Quiena - Dividendos (USD)', 0.0, 0))

    # 6. Quiena - Retiros (USD)
    results.append(('Quiena - Retiros (USD)', 0.0, 0))

    # 7. LLC - Ganancia (USD)
    llc_income = filter_transactions(transactions,
                                     account_names=ACCOUNT_GROUPS['LLC'],
                                     category='Wage, invoices',
                                     currency='USD')
    results.append(('LLC - Ganancia (USD)', calculate_sum(llc_income), len(llc_income)))

    # 8. LLC - Gastos (USD)
    llc_expenses = filter_transactions(transactions,
                                       account_names=ACCOUNT_GROUPS['LLC'],
                                       transaction_type='Expenses',
                                       transfer=False,
                                       currency='USD')
    results.append(('LLC - Gastos (USD)', calculate_sum(llc_expenses), len(llc_expenses)))

    # 9. LLC - Retiros (USD)
    llc_withdrawals = filter_transactions(transactions,
                                         account_names=ACCOUNT_GROUPS['LLC'],
                                         transfer=True,
                                         transaction_type='Expenses',
                                         currency='USD',
                                         exclude_internal_transfers=True)
    results.append(('LLC - Retiros (USD)', calculate_sum(llc_withdrawals), len(llc_withdrawals)))

    # 10. HSBC - Ingresos (USD)
    hsbc_income = filter_transactions(transactions,
                                      account_names=ACCOUNT_GROUPS['HSBC'],
                                      transfer=True,
                                      transaction_type='Income',
                                      currency='USD',
                                      exclude_internal_transfers=True)
    results.append(('HSBC - Ingresos (USD)', calculate_sum(hsbc_income), len(hsbc_income)))

    # 11. HSBC - Retiros (USD)
    hsbc_withdrawals = filter_transactions(transactions,
                                          account_names=ACCOUNT_GROUPS['HSBC'],
                                          transfer=True,
                                          transaction_type='Expenses',
                                          currency='USD',
                                          exclude_internal_transfers=True)
    results.append(('HSBC - Retiros (USD)', calculate_sum(hsbc_withdrawals), len(hsbc_withdrawals)))

    # 12. HSBC - Gastos (USD)
    hsbc_expenses = filter_transactions(transactions,
                                       account_names=ACCOUNT_GROUPS['HSBC'],
                                       transaction_type='Expenses',
                                       transfer=False,
                                       currency='USD')
    results.append(('HSBC - Gastos (USD)', calculate_sum(hsbc_expenses), len(hsbc_expenses)))

    # 13. Crypto - Posición (USD)
    crypto_position = filter_transactions(transactions,
                                         account_names=ACCOUNT_GROUPS['Crypto'],
                                         transfer=True,
                                         transaction_type='Income',
                                         currency='USD')
    results.append(('Crypto - Posición (USD)', calculate_sum(crypto_position), len(crypto_position)))

    # 14. Crypto - Incremento de valor (USD)
    crypto_increment = filter_transactions(transactions,
                                          account_names=ACCOUNT_GROUPS['Crypto'],
                                          category='Financial investments',
                                          transfer=False,
                                          currency='USD')
    results.append(('Crypto - Incremento de valor (USD)', calculate_sum(crypto_increment), len(crypto_increment)))

    # 15. Crypto - Retiros (USD)
    crypto_withdrawals_transfer = filter_transactions(transactions,
                                                     account_names=ACCOUNT_GROUPS['Crypto'],
                                                     transfer=True,
                                                     transaction_type='Expenses',
                                                     currency='USD')
    crypto_withdrawals_expense = filter_transactions(transactions,
                                                    account_names=ACCOUNT_GROUPS['Crypto'],
                                                    transaction_type='Expenses',
                                                    transfer=False,
                                                    currency='USD')
    crypto_total_withdrawals = calculate_sum(crypto_withdrawals_transfer) + calculate_sum(crypto_withdrawals_expense)
    crypto_withdrawal_count = len(crypto_withdrawals_transfer) + len(crypto_withdrawals_expense)
    results.append(('Crypto - Retiros (USD)', crypto_total_withdrawals, crypto_withdrawal_count))

    # Print results
    print("\n╔═══════════════════════════════════════════════════════════════╗")
    print("║                    FINANCIAL SUMMARY                          ║")
    print("╠═══════════════════════════════════════════════════════════════╣")

    for category, value, count in results:
        value_str = f"{value:.2f}"
        print(f"║ {category:<40} {value_str:>15} ({count:>3} txns) ║")

    print("╚═══════════════════════════════════════════════════════════════╝")
    print()

    # Show detailed transactions for a specific group if requested
    if detail_group:
        show_group_details(transactions, detail_group)

if __name__ == '__main__':
    main()
