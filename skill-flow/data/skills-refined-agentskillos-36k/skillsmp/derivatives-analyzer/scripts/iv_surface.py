#!/usr/bin/env python3
"""Implied Volatility surface analysis using OpenBB."""
import argparse

def analyze_iv_surface(symbol: str, provider: str = 'cboe', plot: bool = True):
    """Analyze and optionally plot IV surface."""
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

    price = chains['underlying_price'].iloc[0]

    # Filter valid data
    valid = chains[
        (chains['dte'] >= 7) &
        (chains['dte'] <= 180) &
        (chains['implied_volatility'].notna()) &
        (chains['implied_volatility'] > 0)
    ]

    if valid.empty:
        print("No valid IV data found")
        return

    # Analyze by expiration
    expirations = sorted(valid['expiration'].unique())

    print(f"\nUnderlying: ${price:.2f}")
    print(f"\n{'='*70}")
    print("IV SUMMARY BY EXPIRATION")
    print(f"{'='*70}")
    print(f"{'Expiration':<12} {'DTE':>6} {'ATM IV':>10} {'Call IV':>10} {'Put IV':>10}")
    print("-" * 70)

    iv_data = []
    for exp in expirations[:8]:  # Limit to 8 expirations
        exp_data = valid[valid['expiration'] == exp]
        dte = exp_data['dte'].iloc[0]

        # ATM options
        atm = exp_data[(exp_data['strike'] >= price * 0.98) &
                       (exp_data['strike'] <= price * 1.02)]

        calls = exp_data[exp_data['option_type'] == 'call']
        puts = exp_data[exp_data['option_type'] == 'put']

        atm_iv = atm['implied_volatility'].mean() * 100 if not atm.empty else 0
        call_iv = calls['implied_volatility'].mean() * 100 if not calls.empty else 0
        put_iv = puts['implied_volatility'].mean() * 100 if not puts.empty else 0

        print(f"{str(exp):<12} {dte:>6} {atm_iv:>9.1f}% {call_iv:>9.1f}% {put_iv:>9.1f}%")

        iv_data.append({
            'expiration': exp,
            'dte': dte,
            'atm_iv': atm_iv,
            'call_iv': call_iv,
            'put_iv': put_iv
        })

    # IV Skew analysis
    print(f"\n{'='*70}")
    print("IV SKEW (Put IV - Call IV)")
    print(f"{'='*70}")
    for d in iv_data:
        skew = d['put_iv'] - d['call_iv']
        direction = "↑ Bearish" if skew > 2 else "↓ Bullish" if skew < -2 else "→ Neutral"
        print(f"{str(d['expiration']):<12} Skew: {skew:+.1f}% {direction}")

    if plot:
        plot_iv_surface(valid, price, symbol)

def plot_iv_surface(data, price, symbol):
    """Plot 3D IV surface."""
    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        import numpy as np
    except ImportError:
        print("\nmatplotlib not installed. Skipping visualization.")
        return

    calls = data[data['option_type'] == 'call']
    calls = calls[(calls['strike'] >= price * 0.8) & (calls['strike'] <= price * 1.2)]

    if len(calls) < 10:
        print("Not enough data for surface plot")
        return

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    strikes = calls['strike'].values
    dtes = calls['dte'].values
    ivs = calls['implied_volatility'].values * 100

    ax.scatter(strikes, dtes, ivs, c=ivs, cmap='viridis', alpha=0.6)
    ax.set_xlabel('Strike')
    ax.set_ylabel('DTE')
    ax.set_zlabel('IV (%)')
    ax.set_title(f'{symbol} Implied Volatility Surface')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze IV surface")
    parser.add_argument('symbol', help='Stock symbol (e.g., SPY, AAPL)')
    parser.add_argument('--provider', default='cboe', choices=['cboe', 'yfinance', 'deribit'],
                        help='Data provider (default: cboe)')
    parser.add_argument('--no-plot', action='store_true', help='Skip visualization')

    args = parser.parse_args()
    analyze_iv_surface(args.symbol, args.provider, not args.no_plot)
