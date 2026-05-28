# Data Management

## Data Importers

### Exchange Data Importer

Fetch historical data directly from exchanges:

```python
from octobot_backtesting.importers import ExchangeDataImporter

class ExchangeDataImporter:
    """Import data from cryptocurrency exchanges"""
    
    def __init__(self, exchange_name: str):
        self.exchange_name = exchange_name
        self.exchange = None  # CCXT exchange instance
    
    async def import_ohlcv(self, symbol: str, timeframe: str,
                          start_time: float, end_time: float) -> list:
        """Import OHLCV candlestick data"""
        all_candles = []
        current_time = start_time
        
        while current_time < end_time:
            candles = await self.exchange.fetch_ohlcv(
                symbol, timeframe, since=int(current_time * 1000), limit=1000
            )
            if not candles:
                break
            all_candles.extend(candles)
            current_time = candles[-1][0] / 1000  # Last timestamp
            await asyncio.sleep(1)  # Rate limiting
        
        return all_candles
    
    async def save_data(self, data: list, output_file: str):
        """Save imported data to file"""
        await self._write_data_file(output_file, {
            "exchange": self.exchange_name,
            "data": data
        })
```

**Usage**:
```python
importer = ExchangeDataImporter("binance")
await importer.initialize()

candles = await importer.import_ohlcv(
    symbol="BTC/USDT",
    timeframe="1h",
    start_time=start_timestamp,
    end_time=end_timestamp
)

await importer.save_data(candles, "BTC_USDT_1h.data")
```

---

### File Data Importer

Load data from existing files:

```python
from octobot_backtesting.importers import DataImporter

class DataImporter:
    """Import from local data files"""
    
    @staticmethod
    async def load_data(file_path: str) -> dict:
        """Load backtesting data from file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    
    @staticmethod
    def parse_data(data: dict) -> BacktestData:
        """Parse loaded data into BacktestData"""
        backtest_data = BacktestData(
            exchange=data["exchange"],
            symbol=data["symbol"],
            timeframe=data["time_frame"]
        )
        
        for candle in data.get("candles", []):
            backtest_data.add_candle(
                timestamp=candle[0],
                ohlcv=candle[1:]
            )
        
        return backtest_data
```

---

## Data Collectors

### Real-time Data Collector

Collect data in real-time for future backtesting:

```python
from octobot_backtesting.collectors import DataCollector

class DataCollector:
    """Collect real-time data for backtesting"""
    
    def __init__(self, exchange_manager, symbols: list, timeframes: list):
        self.exchange_manager = exchange_manager
        self.symbols = symbols
        self.timeframes = timeframes
        self.collected_data = {}
        self.running = False
    
    async def start(self):
        """Start collecting data"""
        self.running = True
        await self._setup_channels()
        await self._subscribe_to_data()
    
    async def _subscribe_to_data(self):
        """Subscribe to market data channels"""
        for symbol in self.symbols:
            for timeframe in self.timeframes:
                await self._subscribe_candles(symbol, timeframe)
    
    async def _on_candle(self, candle_data: dict):
        """Handle incoming candle data"""
        key = (candle_data["symbol"], candle_data["timeframe"])
        if key not in self.collected_data:
            self.collected_data[key] = []
        
        self.collected_data[key].append(candle_data["candle"])
    
    async def save_collected_data(self, output_dir: str):
        """Save collected data to files"""
        for (symbol, timeframe), candles in self.collected_data.items():
            filename = f"{symbol.replace('/', '_')}_{timeframe}.data"
            filepath = os.path.join(output_dir, filename)
            await self._save_data(filepath, candles)
```

**Usage**:
```python
collector = DataCollector(
    exchange_manager,
    symbols=["BTC/USDT", "ETH/USDT"],
    timeframes=["1m", "5m", "1h"]
)

await collector.start()
# Let it run...
await asyncio.sleep(3600)  # Collect for 1 hour
await collector.save_collected_data("data/")
```

---

## Data Converters

### Format Conversion

Convert between different data formats:

```python
from octobot_backtesting.converters import DataConverter

class DataConverter:
    """Convert backtesting data formats"""
    
    @staticmethod
    async def csv_to_octobot(csv_file: str, output_file: str):
        """Convert CSV to OctoBot format"""
        import pandas as pd
        
        df = pd.read_csv(csv_file)
        candles = []
        
        for _, row in df.iterrows():
            candles.append([
                row['timestamp'],
                row['open'],
                row['high'],
                row['low'],
                row['close'],
                row['volume']
            ])
        
        data = {
            "exchange": "unknown",
            "symbol": "BTC/USDT",
            "time_frame": "1h",
            "candles": candles
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f)
    
    @staticmethod
    async def octobot_to_csv(octobot_file: str, csv_file: str):
        """Convert OctoBot format to CSV"""
        import pandas as pd
        
        with open(octobot_file, 'r') as f:
            data = json.load(f)
        
        df = pd.DataFrame(
            data["candles"],
            columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
        )
        df.to_csv(csv_file, index=False)
```

---

## Data Storage

### Database Storage

Store backtesting data in SQLite database:

```python
from octobot_backtesting.data import Database

class BacktestingDatabase:
    """SQLite database for backtesting data"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
    
    async def initialize(self):
        """Create database tables"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS candles (
                id INTEGER PRIMARY KEY,
                exchange TEXT,
                symbol TEXT,
                timeframe TEXT,
                timestamp REAL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL
            )
        ''')
        self.conn.commit()
    
    async def insert_candles(self, exchange: str, symbol: str, 
                            timeframe: str, candles: list):
        """Insert candles into database"""
        for candle in candles:
            self.conn.execute('''
                INSERT INTO candles (exchange, symbol, timeframe, 
                                   timestamp, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (exchange, symbol, timeframe, *candle))
        self.conn.commit()
    
    async def get_candles(self, exchange: str, symbol: str, 
                         timeframe: str, start_time: float, 
                         end_time: float) -> list:
        """Retrieve candles from database"""
        cursor = self.conn.execute('''
            SELECT timestamp, open, high, low, close, volume
            FROM candles
            WHERE exchange = ? AND symbol = ? AND timeframe = ?
              AND timestamp >= ? AND timestamp <= ?
            ORDER BY timestamp
        ''', (exchange, symbol, timeframe, start_time, end_time))
        
        return cursor.fetchall()
```

---

## Data Validation

### Integrity Checks

Validate historical data quality:

```python
class DataValidator:
    """Validate backtesting data"""
    
    @staticmethod
    def validate_candles(candles: list) -> list:
        """Check candle data integrity"""
        errors = []
        
        for i, candle in enumerate(candles):
            # Check structure
            if len(candle) != 6:
                errors.append(f"Candle {i}: Invalid structure (expected 6 fields)")
                continue
            
            timestamp, open, high, low, close, volume = candle
            
            # Check OHLCV relationships
            if high < low:
                errors.append(f"Candle {i}: High < Low")
            if high < open or high < close:
                errors.append(f"Candle {i}: High < Open/Close")
            if low > open or low > close:
                errors.append(f"Candle {i}: Low > Open/Close")
            if volume < 0:
                errors.append(f"Candle {i}: Negative volume")
            
            # Check for gaps (if not first candle)
            if i > 0:
                prev_timestamp = candles[i-1][0]
                expected_interval = DataValidator._get_timeframe_seconds(timeframe)
                actual_interval = timestamp - prev_timestamp
                
                if abs(actual_interval - expected_interval) > expected_interval * 0.1:
                    errors.append(f"Candle {i}: Time gap detected")
        
        return errors
    
    @staticmethod
    def _get_timeframe_seconds(timeframe: str) -> int:
        """Convert timeframe to seconds"""
        mapping = {
            "1m": 60, "5m": 300, "15m": 900, "30m": 1800,
            "1h": 3600, "4h": 14400, "1d": 86400
        }
        return mapping.get(timeframe, 0)
    
    @staticmethod
    def fill_gaps(candles: list, timeframe: str) -> list:
        """Fill missing candles with forward-fill"""
        if not candles:
            return candles
        
        filled_candles = [candles[0]]
        interval = DataValidator._get_timeframe_seconds(timeframe)
        
        for i in range(1, len(candles)):
            prev_candle = filled_candles[-1]
            current_candle = candles[i]
            
            # Check for gap
            expected_time = prev_candle[0] + interval
            actual_time = current_candle[0]
            
            # Fill gap with previous close price
            while expected_time < actual_time:
                filled_candles.append([
                    expected_time,
                    prev_candle[4],  # open = prev close
                    prev_candle[4],  # high = prev close
                    prev_candle[4],  # low = prev close
                    prev_candle[4],  # close = prev close
                    0  # volume = 0
                ])
                expected_time += interval
            
            filled_candles.append(current_candle)
        
        return filled_candles
```

---

## Data Preprocessing

### Normalization

Prepare data for backtesting:

```python
class DataPreprocessor:
    """Preprocess data for backtesting"""
    
    @staticmethod
    def normalize_prices(candles: list, method: str = "minmax") -> list:
        """Normalize price data"""
        if method == "minmax":
            prices = [c[4] for c in candles]  # Close prices
            min_price = min(prices)
            max_price = max(prices)
            
            normalized = []
            for candle in candles:
                norm_open = (candle[1] - min_price) / (max_price - min_price)
                norm_high = (candle[2] - min_price) / (max_price - min_price)
                norm_low = (candle[3] - min_price) / (max_price - min_price)
                norm_close = (candle[4] - min_price) / (max_price - min_price)
                
                normalized.append([
                    candle[0], norm_open, norm_high, 
                    norm_low, norm_close, candle[5]
                ])
            
            return normalized
    
    @staticmethod
    def add_technical_indicators(candles: list) -> dict:
        """Calculate technical indicators"""
        closes = [c[4] for c in candles]
        
        # Simple Moving Average
        sma_20 = DataPreprocessor._calculate_sma(closes, 20)
        
        # RSI
        rsi_14 = DataPreprocessor._calculate_rsi(closes, 14)
        
        return {
            "candles": candles,
            "indicators": {
                "sma_20": sma_20,
                "rsi_14": rsi_14
            }
        }
    
    @staticmethod
    def _calculate_sma(prices: list, period: int) -> list:
        """Calculate Simple Moving Average"""
        sma = []
        for i in range(len(prices)):
            if i < period - 1:
                sma.append(None)
            else:
                avg = sum(prices[i-period+1:i+1]) / period
                sma.append(avg)
        return sma
```
