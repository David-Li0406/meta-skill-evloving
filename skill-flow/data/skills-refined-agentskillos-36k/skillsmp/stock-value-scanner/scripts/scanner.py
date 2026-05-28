import sys
import argparse
import time
import warnings

# Suppress pandas/yfinance deprecation warnings
warnings.filterwarnings("ignore", category=FutureWarning)
# Catch specific text if category is custom or not easily imported without pandas
warnings.filterwarnings("ignore", message=".*Timestamp.utcnow is deprecated.*")

try:
    import yfinance as yf
except ImportError:
    print("❌ 错误: 未安装 yfinance 库。")
    print("请运行: pip install yfinance")
    sys.exit(1)

def get_data(symbol):
    """从 Yahoo Finance 获取概览数据"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        # 简单验证数据有效性
        if 'regularMarketPrice' not in info and 'currentPrice' not in info:
            # 有些时候 info 为空或获取失败
            return None
        return info
    except Exception as e:
        print(f"❌ {symbol} 请求错误: {e}")
        return None

def analyze_single_stock(data, quiet=False):
    """分析单个股票数据并返回得分和摘要"""
    if not data: return 0, None
    
    symbol = data.get("symbol", "UNKNOWN")
    try:
        price = float(data.get("currentPrice") or data.get("regularMarketPrice") or 0)
        pb = float(data.get("priceToBook") or 0)
        pe = float(data.get("trailingPE") or data.get("forwardPE") or 999)
        roe = float(data.get("returnOnEquity") or 0) * 100
        profit_margin = float(data.get("profitMargins") or 0) * 100
        
        # 补充：债务权益比
        debt_to_equity = float(data.get("debtToEquity") or 999)
    except (ValueError, TypeError):
        # 数据不全时的容错
        return 0, None

    # 评分逻辑 (巴菲特风格简化版)
    score = 0
    reasons = []

    # 1. 估值分 (P/B, P/E)
    if 0 < pb < 1.5: score += 2; reasons.append("P/B极低")
    elif pb < 3.0: score += 1
    
    if 0 < pe < 15: score += 1; reasons.append("P/E便宜")
    elif pe > 50: score -= 1; reasons.append("估值过高")
    
    # 2. 质量分 (ROE, Margin)
    if roe > 15: score += 2; reasons.append("高ROE")
    elif roe < 5: score -= 1; reasons.append("ROE过低")
    
    if profit_margin > 20: score += 1; reasons.append("高净利")
    
    # 3. 风险分
    if debt_to_equity > 200: score -= 1; reasons.append("高负债")

    summary = {
        "symbol": symbol,
        "price": price,
        "score": score,
        "pb": pb,
        "pe": pe,
        "roe": roe,
        "reasons": ", ".join(reasons)
    }

    if not quiet:
        analyze_value(data, summary)
    
    return score, summary

def analyze_value(data, summary):
    """打印详细报告"""
    symbol = data.get("symbol")
    target = data.get("targetMeanPrice", "N/A")
    recommendation = data.get("recommendationKey", "N/A")
    
    print(f"\n📊 {symbol} | 价: ${summary['price']} | 目标: ${target}")
    print(f"   评分: {summary['score']}/6 | 建议: {recommendation.upper()}")
    print("-" * 40)
    print(f"   P/E : {summary['pe']:.2f}")
    print(f"   P/B : {summary['pb']:.2f}")
    print(f"   ROE : {summary['roe']:.2f}%")
    print(f"   结论: {summary['reasons'] if summary['reasons'] else '表现平平'}")

def scan_watchlist(symbols):
    """批量扫描列表"""
    print(f"📋 正在扫描 {len(symbols)} 只股票...")
    results = []
    
    for i, symbol in enumerate(symbols):
        print(f"[{i+1}/{len(symbols)}] 分析 {symbol} ...", end="\r")
        data = get_data(symbol)
        if data:
            _, summary = analyze_single_stock(data, quiet=True)
            if summary:
                results.append(summary)
        # yfinance 通常不需要像 Alpha Vantage 那样严格的 sleep，但为了礼貌保持一点间隔
        time.sleep(0.5)

    # 打印排行榜
    print("\n" + "="*70)
    print(f"🏆 价值选股排行榜")
    print("="*70)
    print(f"{'代码':<8} {'得分':<5} {'股价':<10} {'P/B':<8} {'ROE':<8} {'亮点'}")
    print("-" * 70)
    
    # 按得分降序排列
    results.sort(key=lambda x: x['score'], reverse=True)
    
    for res in results:
        print(f"{res['symbol']:<8} {res['score']:<5} ${res['price']:<9.2f} {res['pb']:<8.2f} {res['roe']:<7.1f}% {res['reasons']}")
    print("="*70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='股票价值分析与扫描器 (Yahoo Finance 版)')
    parser.add_argument('symbol', nargs='?', help='单个股票代码 (例如 AAPL)')
    parser.add_argument('--scan', action='store_true', help='扫描预设关注列表 (Tech Giants)')
    
    args = parser.parse_args()

    # 默认关注列表 (如果用户选择扫描)
    DEFAULT_WATCHLIST = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX', 'AMD', 'INTC']

    if args.scan:
        scan_watchlist(DEFAULT_WATCHLIST)
    elif args.symbol:
        data = get_data(args.symbol.upper())
        if data:
            analyze_single_stock(data, quiet=False)
        else:
            print(f"❌ 无法获取 {args.symbol} 的数据")
    else:
        parser.print_help()
