#!/usr/bin/env python3
"""Options Greeks analysis and visualization using OpenBB."""
import argparse

def analyze_options_greeks(symbol: str, provider: str = 'cboe',
                           min_dte: int = 7, max_dte: int = 60,
                           pct_range: float = 0.05, visualize: bool = False):
    """Analyze options Greeks for a given symbol."""
    from openbb import obb
    obb.user.preferences.output_type = "dataframe"

    print(f"\nFetching options chain for {symbol}...")
    try:
        result = obb.derivatives.options.chains(symbol, provider=provider)
        chains = result.to_df() if hasattr(result, 'to_df') else result
    except Exception as e:
        print(f"Error fetching options chain: {e}")
        return

    if chains is None or chains.empty:
        print(f"No options data for {symbol}")
        return

    # Handle different column names across providers
    price_col = 'underlying_price' if 'underlying_price' in chains.columns else 'spot_price'
    if price_col not in chains.columns:
        print("Cannot determine underlying price from data")
        return
    price = chains[price_col].iloc[0]
    print(f"Underlying Price: ${price:.2f}")

    # Filter valid Greeks
    valid = chains[
        (chains['dte'] >= min_dte) &
        (chains['dte'] <= max_dte) &
        (chains['delta'] != 0) &
        (chains['delta'] != 1) &
        (chains['delta'] != -1)
    ]

    if valid.empty:
        print("No valid options found with Greeks data")
        return

    # Select first expiration
    expirations = sorted(valid['expiration'].unique())
    if len(expirations) == 0:
        print("No expirations found after filtering")
        return
    expiry = expirations[0]
    selected = valid[valid['expiration'] == expiry]

    print(f"Expiration: {expiry} (DTE: {selected['dte'].iloc[0]})")
    print(f"Total contracts: {len(selected)}")

    # ATM filter
    lower = price * (1 - pct_range)
    upper = price * (1 + pct_range)

    calls = selected[(selected['option_type'] == 'call') &
                     (selected['strike'] >= lower) &
                     (selected['strike'] <= upper)]
    puts = selected[(selected['option_type'] == 'put') &
                    (selected['strike'] >= lower) &
                    (selected['strike'] <= upper)]

    cols = ['strike', 'delta', 'gamma', 'theta', 'vega', 'implied_volatility', 'bid', 'ask']
    available = [c for c in cols if c in calls.columns]

    print(f"\n{'='*60}")
    print(f"ATM CALLS (±{pct_range*100:.0f}%)")
    print(f"{'='*60}")
    if not calls.empty:
        print(calls[available].to_string(index=False))
    else:
        print("No ATM calls found")

    print(f"\n{'='*60}")
    print(f"ATM PUTS (±{pct_range*100:.0f}%)")
    print(f"{'='*60}")
    if not puts.empty:
        print(puts[available].to_string(index=False))
    else:
        print("No ATM puts found")

    if visualize:
        plot_greeks(selected, price, expiry)

def plot_greeks(data, price, expiry):
    """Visualize Greeks across strikes."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("\nmatplotlib not installed. Skipping visualization.")
        return

    calls = data[data['option_type'] == 'call'].sort_values('strike')
    calls = calls[(calls['strike'] >= price * 0.85) & (calls['strike'] <= price * 1.15)]

    if calls.empty:
        print("Not enough data for visualization")
        return

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f'Greeks Analysis - Expiry: {expiry}', fontsize=14)

    for ax, greek, color in zip(axes.flatten(),
                                 ['delta', 'gamma', 'theta', 'vega'],
                                 ['blue', 'green', 'red', 'purple']):
        if greek in calls.columns:
            ax.plot(calls['strike'], calls[greek], f'{color[0]}-o', markersize=3)
            ax.axvline(x=price, color='r', linestyle='--', alpha=0.7, label=f'Spot ${price:.0f}')
            ax.set_xlabel('Strike')
            ax.set_ylabel(greek.capitalize())
            ax.set_title(f'{greek.upper()} vs Strike')
            ax.legend()
            ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze options Greeks")
    parser.add_argument('symbol', help='Stock symbol (e.g., SPY, AAPL)')
    parser.add_argument('--provider', default='cboe', choices=['cboe', 'yfinance', 'deribit'],
                        help='Data provider (default: cboe)')
    parser.add_argument('--min-dte', type=int, default=7, help='Minimum DTE (default: 7)')
    parser.add_argument('--max-dte', type=int, default=60, help='Maximum DTE (default: 60)')
    parser.add_argument('--range', type=float, default=0.05,
                        help='ATM range as decimal (default: 0.05 = ±5%%)')
    parser.add_argument('--plot', action='store_true', help='Show Greeks visualization')

    args = parser.parse_args()
    analyze_options_greeks(args.symbol, args.provider, args.min_dte,
                          args.max_dte, args.range, args.plot)
