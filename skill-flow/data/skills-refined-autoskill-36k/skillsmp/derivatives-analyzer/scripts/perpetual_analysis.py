#!/usr/bin/env python3
"""Crypto perpetual contracts analysis using OpenBB + Deribit."""
import argparse
import sys

def analyze_perpetuals(symbols: list[str], show_all: bool = False):
    """Analyze crypto perpetual contracts."""
    from openbb import obb
    obb.user.preferences.output_type = "dataframe"

    symbol_str = ','.join(symbols)
    try:
        result = obb.derivatives.futures.info(provider='deribit', symbol=symbol_str)
        info = result.to_df() if hasattr(result, 'to_df') else result
    except Exception as e:
        print(f"Error fetching data for {symbol_str}: {e}")
        return

    if info is None or info.empty:
        print(f"No data for {symbol_str}")
        return

    cols = ['symbol', 'last_price', 'mark_price', 'current_funding',
            'funding_8h', 'open_interest', 'volume_usd', 'change_percent']
    available = [c for c in cols if c in info.columns]

    print(f"\n{'='*60}")
    print("CRYPTO PERPETUAL ANALYSIS")
    print(f"{'='*60}\n")

    for _, row in info.iterrows():
        sym = row.get('symbol', 'N/A')
        print(f"Symbol: {sym}")
        print(f"  Last Price:    ${row.get('last_price') or 0:,.2f}")
        print(f"  Mark Price:    ${row.get('mark_price') or 0:,.2f}")

        funding = row.get('current_funding') or 0
        funding_8h = row.get('funding_8h') or 0
        print(f"  Funding Rate:  {funding*100:.4f}% (8h: {funding_8h*100:.4f}%)")

        oi = row.get('open_interest') or 0
        vol = row.get('volume_usd') or 0
        print(f"  Open Interest: ${oi:,.0f}")
        print(f"  24h Volume:    ${vol:,.0f}")
        print(f"  24h Change:    {row.get('change_percent') or 0:.2f}%")
        print()

    if show_all:
        print("\nRaw Data:")
        print(info[available].to_string(index=False))

def list_instruments():
    """List all available perpetual instruments."""
    from openbb import obb
    obb.user.preferences.output_type = "dataframe"

    try:
        result = obb.derivatives.futures.instruments(provider='deribit')
        instruments = result.to_df() if hasattr(result, 'to_df') else result
    except Exception as e:
        print(f"Error fetching instruments: {e}")
        return
    perps = instruments[instruments['symbol'].str.contains('PERPETUAL', na=False)]

    print("\nAvailable Perpetual Contracts:")
    print(perps[['symbol', 'last_price', 'open_interest']].to_string(index=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze crypto perpetuals")
    parser.add_argument('symbols', nargs='*', default=['BTC', 'ETH', 'SOL'],
                        help='Symbols to analyze (default: BTC ETH SOL)')
    parser.add_argument('--list', action='store_true', help='List all instruments')
    parser.add_argument('--all', action='store_true', help='Show all raw data')

    args = parser.parse_args()

    if args.list:
        list_instruments()
    else:
        analyze_perpetuals(args.symbols, args.all)
