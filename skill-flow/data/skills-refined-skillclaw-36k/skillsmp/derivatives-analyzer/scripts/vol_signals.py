#!/usr/bin/env python3
"""Volatility trading signals and indicators using OpenBB.

Based on Jeff Liang's volatility trading methodology.
"""
import argparse

def analyze_vol_signals(symbol: str, provider: str = 'deribit'):
    """Analyze volatility trading signals for a symbol."""
    from openbb import obb
    obb.user.preferences.output_type = "dataframe"

    print(f"\n{'='*60}")
    print(f"VOLATILITY SIGNALS: {symbol}")
    print(f"{'='*60}")

    try:
        result = obb.derivatives.options.chains(symbol, provider=provider)
        chains = result.to_df() if hasattr(result, 'to_df') else result
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    if chains is None or chains.empty:
        print("No options data available")
        return

    # Get current price
    price_col = 'underlying_price' if 'underlying_price' in chains.columns else 'spot_price'
    if price_col not in chains.columns:
        print("Cannot determine underlying price")
        return
    price = chains[price_col].iloc[0]

    # Filter valid options
    valid = chains[
        (chains['dte'] >= 1) &
        (chains['implied_volatility'].notna()) &
        (chains['implied_volatility'] > 0)
    ]

    if valid.empty:
        print("No valid options data")
        return

    # Get expirations
    expirations = sorted(valid['dte'].unique())

    print(f"\nUnderlying: ${price:,.2f}")
    print(f"Expirations (DTE): {expirations[:8]}")

    # 1. Term Structure Analysis
    print(f"\n{'─'*60}")
    print("TERM STRUCTURE")
    print(f"{'─'*60}")

    ts_data = []
    for dte in expirations[:6]:
        exp_data = valid[valid['dte'] == dte]
        atm = exp_data[(exp_data['strike'] >= price * 0.98) &
                       (exp_data['strike'] <= price * 1.02)]
        if not atm.empty:
            atm_iv = atm['implied_volatility'].mean() * 100
            ts_data.append({'dte': dte, 'atm_iv': atm_iv})
            print(f"  DTE {dte:3d}: ATM IV = {atm_iv:.1f}%")

    if len(ts_data) >= 2:
        near_iv = ts_data[0]['atm_iv']
        far_iv = ts_data[-1]['atm_iv']
        ts_spread = far_iv - near_iv
        structure = "CONTANGO" if ts_spread > 0 else "BACKWARDATION"
        print(f"\n  Structure: {structure} (spread: {ts_spread:+.1f}%)")
        if structure == "CONTANGO":
            print("  Signal: Calendar spread opportunity (+Theta, +Gamma)")

    # 2. Fly Analysis (Vol-of-Vol proxy)
    print(f"\n{'─'*60}")
    print("FLY ANALYSIS (Vol-of-Vol)")
    print(f"{'─'*60}")

    for dte in expirations[:3]:
        exp_data = valid[valid['dte'] == dte]
        calls = exp_data[exp_data['option_type'] == 'call']
        puts = exp_data[exp_data['option_type'] == 'put']

        # ATM IV
        atm_calls = calls[(calls['strike'] >= price * 0.98) &
                          (calls['strike'] <= price * 1.02)]
        atm_iv = atm_calls['implied_volatility'].mean() * 100 if not atm_calls.empty else 0

        # 25 Delta wings (approximate with 5% OTM)
        otm_calls = calls[(calls['strike'] >= price * 1.03) &
                          (calls['strike'] <= price * 1.08)]
        otm_puts = puts[(puts['strike'] >= price * 0.92) &
                        (puts['strike'] <= price * 0.97)]

        call_25d_iv = otm_calls['implied_volatility'].mean() * 100 if not otm_calls.empty else 0
        put_25d_iv = otm_puts['implied_volatility'].mean() * 100 if not otm_puts.empty else 0

        if atm_iv > 0 and call_25d_iv > 0 and put_25d_iv > 0:
            fly = (call_25d_iv + put_25d_iv) / 2 - atm_iv
            print(f"  DTE {dte:3d}: Fly = {fly:+.2f}% (ATM={atm_iv:.1f}%, Wings avg={((call_25d_iv+put_25d_iv)/2):.1f}%)")

    # 3. Skew Analysis
    print(f"\n{'─'*60}")
    print("SKEW ANALYSIS")
    print(f"{'─'*60}")

    for dte in expirations[:3]:
        exp_data = valid[valid['dte'] == dte]
        calls = exp_data[exp_data['option_type'] == 'call']
        puts = exp_data[exp_data['option_type'] == 'put']

        otm_calls = calls[(calls['strike'] >= price * 1.03) &
                          (calls['strike'] <= price * 1.08)]
        otm_puts = puts[(puts['strike'] >= price * 0.92) &
                        (puts['strike'] <= price * 0.97)]

        call_iv = otm_calls['implied_volatility'].mean() * 100 if not otm_calls.empty else 0
        put_iv = otm_puts['implied_volatility'].mean() * 100 if not otm_puts.empty else 0

        if call_iv > 0 and put_iv > 0:
            skew = put_iv - call_iv
            direction = "BEARISH" if skew > 2 else "BULLISH" if skew < -2 else "NEUTRAL"
            print(f"  DTE {dte:3d}: Skew = {skew:+.2f}% ({direction})")

    # 4. Straddle Premium
    print(f"\n{'─'*60}")
    print("ATM STRADDLE ANALYSIS")
    print(f"{'─'*60}")

    for dte in expirations[:3]:
        exp_data = valid[valid['dte'] == dte]
        atm_strike = round(price / 5) * 5  # Round to nearest 5

        atm_call = exp_data[(exp_data['option_type'] == 'call') &
                            (abs(exp_data['strike'] - price) == abs(exp_data['strike'] - price).min())]
        atm_put = exp_data[(exp_data['option_type'] == 'put') &
                           (abs(exp_data['strike'] - price) == abs(exp_data['strike'] - price).min())]

        if not atm_call.empty and not atm_put.empty:
            call_mid = (atm_call['bid'].iloc[0] + atm_call['ask'].iloc[0]) / 2
            put_mid = (atm_put['bid'].iloc[0] + atm_put['ask'].iloc[0]) / 2
            straddle_cost = call_mid + put_mid
            pct_move = (straddle_cost / price) * 100

            call_theta = atm_call['theta'].iloc[0] if 'theta' in atm_call.columns else 0
            put_theta = atm_put['theta'].iloc[0] if 'theta' in atm_put.columns else 0
            total_theta = call_theta + put_theta

            print(f"  DTE {dte:3d}: Straddle = ${straddle_cost:.2f} ({pct_move:.2f}% move needed)")
            print(f"           Theta = ${total_theta:.2f}/day | BE Daily Move = {pct_move/dte:.3f}%")

    # 5. Trading Signals Summary
    print(f"\n{'='*60}")
    print("TRADING SIGNALS SUMMARY")
    print(f"{'='*60}")

    signals = []

    # Check term structure
    if len(ts_data) >= 2:
        if ts_spread > 2:
            signals.append("[+] Strong Contango: Sell calendar spreads")
        elif ts_spread < -2:
            signals.append("[+] Backwardation: Vol compression expected")

    print("\n".join(signals) if signals else "No strong signals detected")
    print()


def calculate_vrp(symbol: str, lookback_days: int = 30):
    """Calculate Variance Risk Premium approximation."""
    from openbb import obb
    obb.user.preferences.output_type = "dataframe"

    print(f"\n{'='*60}")
    print(f"VRP ANALYSIS: {symbol}")
    print(f"{'='*60}")

    try:
        # Get current IV
        result = obb.derivatives.options.chains(symbol, provider='deribit')
        chains = result.to_df() if hasattr(result, 'to_df') else result

        if chains is None or chains.empty:
            print("No options data")
            return

        # Get 30-day ATM IV
        price_col = 'underlying_price' if 'underlying_price' in chains.columns else 'spot_price'
        price = chains[price_col].iloc[0]

        month_options = chains[(chains['dte'] >= 25) & (chains['dte'] <= 35)]
        atm = month_options[(month_options['strike'] >= price * 0.98) &
                            (month_options['strike'] <= price * 1.02)]

        if atm.empty:
            print("No ATM options for 30-day expiry")
            return

        iv_30d = atm['implied_volatility'].mean() * 100
        print(f"\n30-Day IV: {iv_30d:.1f}%")

        # Get historical prices for RV calculation
        hist_result = obb.equity.price.historical(symbol=symbol, provider='yfinance')
        hist = hist_result.to_df() if hasattr(hist_result, 'to_df') else hist_result

        if hist is None or len(hist) < lookback_days:
            print("Insufficient historical data for RV")
            return

        # Calculate realized volatility
        returns = hist['close'].pct_change().dropna().tail(lookback_days)
        rv_30d = returns.std() * (252 ** 0.5) * 100

        print(f"30-Day RV: {rv_30d:.1f}%")

        vrp = iv_30d - rv_30d
        print(f"\nVRP (IV - RV): {vrp:+.1f}%")

        if vrp > 5:
            print("Signal: HIGH VRP - Favorable for vol selling")
        elif vrp < -5:
            print("Signal: NEGATIVE VRP - Pause vol selling strategies")
        else:
            print("Signal: NEUTRAL VRP")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Volatility trading signals")
    parser.add_argument('symbol', help='Symbol (e.g., BTC, SPY)')
    parser.add_argument('--provider', default='deribit',
                        choices=['deribit', 'cboe', 'yfinance'])
    parser.add_argument('--vrp', action='store_true', help='Calculate VRP')

    args = parser.parse_args()

    if args.vrp:
        calculate_vrp(args.symbol)
    else:
        analyze_vol_signals(args.symbol, args.provider)
