import sys
import argparse
import warnings

# Suppress pandas/yfinance deprecation warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*Timestamp.utcnow is deprecated.*")

try:
    import yfinance as yf
except ImportError:
    print("❌ Error: yfinance is not installed. Run: pip install yfinance")
    sys.exit(1)

def get_stock_trend(symbol):
    """
    Fetches historical stock data to analyze long-term trends.
    """
    try:
        ticker = yf.Ticker(symbol)
        
        # Fetch history (1 year for 52w, max for ATH)
        # We need enough data for MA200
        history = ticker.history(period="max")
        
        if history.empty:
            return None
        
        # Latest data
        latest = history.iloc[-1]
        current_price = latest["Close"]
        latest_date = latest.name.strftime('%Y-%m-%d')
        
        # All-Time High
        ath = history["High"].max()
        ath_date = history["High"].idxmax().strftime('%Y-%m-%d')
        drawdown = ((current_price - ath) / ath) * 100
        
        # 52-Week Range
        last_year = history.iloc[-252:] if len(history) > 252 else history
        high_52w = last_year["High"].max()
        low_52w = last_year["Low"].min()
        
        # Moving Averages
        ma50 = history["Close"].rolling(window=50).mean().iloc[-1]
        ma200 = history["Close"].rolling(window=200).mean().iloc[-1]
        
        return {
            "symbol": symbol.upper(),
            "date": latest_date,
            "price": current_price,
            "ath": ath,
            "ath_date": ath_date,
            "drawdown": drawdown,
            "high_52w": high_52w,
            "low_52w": low_52w,
            "ma50": ma50,
            "ma200": ma200
        }

    except Exception as e:
        print(f"Error analyzing {symbol}: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze stock price trends (ATH, Daily Close, MA).')
    parser.add_argument('symbol', help='Stock symbol (e.g., NVDA)')
    args = parser.parse_args()

    data = get_stock_trend(args.symbol)
    
    if data:
        print(f"\n📈 Trend Analysis for {data['symbol']} ({data['date']})")
        print("=" * 40)
        print(f"💰 Close Price : ${data['price']:.2f}")
        print("-" * 40)
        print(f"🏆 All-Time High: ${data['ath']:.2f} (on {data['ath_date']})")
        print(f"📉 Drawdown from ATH: {data['drawdown']:.2f}%")
        print("-" * 40)
        print(f"📅 52-Week High : ${data['high_52w']:.2f}")
        print(f"📅 52-Week Low  : ${data['low_52w']:.2f}")
        print("-" * 40)
        
        # Trend Context
        trend = "Neutral"
        if data['price'] > data['ma200']:
            trend = "Bullish (Above MA200)"
        else:
            trend = "Bearish (Below MA200)"
            
        print(f"📊 MA200       : ${data['ma200']:.2f}")
        print(f"🎯 Trend Context: {trend}")
        print("=" * 40)
    else:
        print(f"❌ Could not retrieve data for {args.symbol}")
        sys.exit(1)
