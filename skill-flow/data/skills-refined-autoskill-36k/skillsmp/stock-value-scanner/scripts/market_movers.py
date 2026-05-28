import sys
import argparse
import urllib.request
import json
import ssl

def fetch_movers(category, limit=10):
    """
    Fetch market movers from Yahoo Finance.
    Categories: day_gainers, day_losers, most_actives
    """
    base_url = "https://query2.finance.yahoo.com/v1/finance/screener/predefined/saved"
    url = f"{base_url}?scrIds={category}&count={limit}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "*/*",
        "Origin": "https://finance.yahoo.com",
        "Referer": "https://finance.yahoo.com/markets/stocks/gainers/"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        # Handle SSL context
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=context) as response:
            data = json.loads(response.read().decode())
            
            # Navigate the JSON structure
            # Structure usually: finance -> result -> [0] -> quotes
            root = data.get("finance", {})
            result = root.get("result", [])
            
            if not result:
                print("No data returned.")
                return

            quotes = result[0].get("quotes", [])
            return quotes

    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        return []

def print_table(title, quotes):
    print(f"\n📢 {title}")
    print("=" * 65)
    # Header
    print(f"{'Symbol':<8} {'Name':<20} {'Price':<10} {'Change %':<10} {'Volume':<10}")
    print("-" * 65)
    
    for q in quotes:
        symbol = q.get('symbol', 'N/A')
        name = q.get('shortName', 'N/A')[:18] # Truncate name
        price = q.get('regularMarketPrice', 0)
        change_p = q.get('regularMarketChangePercent', 0)
        volume = q.get('regularMarketVolume', 0)
        
        # Color coding for change (basic visual indicator)
        sign = "+" if change_p >= 0 else ""
        
        # Format large volume numbers
        if volume > 1_000_000:
            vol_str = f"{volume/1_000_000:.1f}M"
        elif volume > 1_000:
            vol_str = f"{volume/1_000:.1f}K"
        else:
            vol_str = str(volume)

        print(f"{symbol:<8} {name:<20} ${price:<9.2f} {sign}{change_p:<9.2f}% {vol_str:<10}")
    print("=" * 65)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scan Market Movers (Yahoo Finance)')
    parser.add_argument('--type', choices=['gainers', 'losers', 'active'], default='active', help='Scan type: gainers, losers, active')
    parser.add_argument('--limit', type=int, default=10, help='Number of results')
    
    args = parser.parse_args()
    
    category_map = {
        'gainers': 'day_gainers',
        'losers': 'day_losers',
        'active': 'most_actives'
    }
    
    title_map = {
        'gainers': 'Top Gainers (涨幅榜)',
        'losers': 'Top Losers (跌幅榜)',
        'active': 'Most Actives (热门交易)'
    }
    
    cat_id = category_map[args.type]
    title = title_map[args.type]
    
    quotes = fetch_movers(cat_id, args.limit)
    if quotes:
        print_table(title, quotes)
    else:
        print("Failed to retrieve market data.")
