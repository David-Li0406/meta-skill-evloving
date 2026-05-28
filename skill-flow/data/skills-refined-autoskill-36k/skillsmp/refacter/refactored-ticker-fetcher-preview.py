"""
Preview of refactored ticker_fetcher.py with legacy enable_aurora path removed.

CHANGES SUMMARY:
- Removed enable_aurora parameter from __init__ (line 40)
- Removed _aurora_repo initialization logic (lines 59-70)
- Removed conditional Aurora write in fetch_ticker (lines 240-244)
- Removed _write_to_aurora method entirely (lines 262-303)
- Kept PrecomputeService integration (modern, always-on)

IMPACT:
- Lines removed: ~80 lines
- Complexity reduction: fetch_ticker C(15) → B(10-12)
- Breaking changes: None (feature was disabled)
"""

# === SNIPPET 1: __init__ signature (BEFORE) ===
# Lines 37-50 (OLD)
"""
def __init__(
    self,
    bucket_name: Optional[str] = None,
    enable_aurora: bool = False,  # ← REMOVED
    data_lake_bucket: Optional[str] = None
):
    '''
    Initialize TickerFetcher.

    Args:
        bucket_name: S3 bucket for cache storage. Defaults to PDF_BUCKET_NAME env var.
        enable_aurora: Enable writing to Aurora MySQL (default: False)  # ← REMOVED
        data_lake_bucket: S3 bucket for data lake storage. Defaults to DATA_LAKE_BUCKET env var.
    '''
"""

# === SNIPPET 1: __init__ signature (AFTER) ===
def __init__(
    self,
    bucket_name: Optional[str] = None,
    data_lake_bucket: Optional[str] = None
):
    """
    Initialize TickerFetcher.

    Args:
        bucket_name: S3 bucket for cache storage. Defaults to PDF_BUCKET_NAME env var.
        data_lake_bucket: S3 bucket for data lake storage. Defaults to DATA_LAKE_BUCKET env var.
    """
    self.bucket_name = bucket_name or os.environ.get('PDF_BUCKET_NAME', 'line-bot-pdf-reports-755283537543')
    self.data_fetcher = DataFetcher()
    self.s3_cache = S3Cache(bucket_name=self.bucket_name, ttl_hours=24)
    self.tickers = self._load_supported_tickers()

    # Data Lake storage (optional, for raw data archival)
    self.data_lake = DataLakeStorage(bucket_name=data_lake_bucket)

    # === REMOVED: Legacy Aurora integration (lines 59-70) ===
    # self.enable_aurora = enable_aurora or os.environ.get('AURORA_ENABLED', 'false').lower() == 'true'
    # self._aurora_repo = None
    #
    # if self.enable_aurora:
    #     try:
    #         from src.data.aurora import TickerRepository
    #         self._aurora_repo = TickerRepository()
    #         logger.info("Aurora MySQL integration enabled")
    #     except Exception as e:
    #         logger.warning(f"Failed to initialize Aurora repository: {e}")
    #         self.enable_aurora = False

    # PrecomputeService for ticker_data table (ground truth storage)
    # Always enabled - Aurora is the primary data store
    print("🔧 DEBUG: About to initialize PrecomputeService")  # DEBUG
    try:
        from src.data.aurora.precompute_service import PrecomputeService
        self.precompute_service = PrecomputeService()
        print("🔧 DEBUG: PrecomputeService initialized successfully")  # DEBUG
        logger.info("PrecomputeService initialized for ticker_data storage")
    except Exception as e:
        print(f"🔧 DEBUG: PrecomputeService init FAILED: {e}")  # DEBUG
        logger.error(f"Failed to initialize PrecomputeService: {e}")
        self.precompute_service = None

    logger.info(
        f"TickerFetcher initialized with {len(self.tickers)} tickers, "
        f"bucket: {self.bucket_name}, "
        f"data_lake: {self.data_lake.is_enabled()}"
        # Removed: f"aurora: {self.enable_aurora}"
    )


# === SNIPPET 2: fetch_ticker storage logic (BEFORE) ===
# Lines 164-252 (OLD)
"""
        # Store to Aurora ticker_data table (PRIMARY STORAGE - GROUND TRUTH)
        # This must succeed before other storage operations
        if self.precompute_service:
            try:
                self.precompute_service.store_ticker_data(
                    symbol=ticker,
                    data_date=datetime.now(bangkok_tz).date(),
                    price_history=price_history,
                    company_info=company_info,
                    financials=None
                )
                logger.info(f"✅ Stored {ticker} to Aurora ticker_data table ({len(price_history)} rows)")
            except Exception as e:
                logger.error(f"Failed to store {ticker} to Aurora ticker_data: {e}")

        # ... (S3 cache storage) ...

        # Store in Data Lake (optional, raw data archival)
        if self.data_lake.is_enabled():
            try:
                self.data_lake.store_ticker_data(ticker, data)
                logger.debug(f"Stored {ticker} to data lake")
            except Exception as e:
                logger.warning(f"Failed to store {ticker} to data lake: {e}")

        # Store in Aurora MySQL (optional)  # ← LEGACY PATH, REMOVED BELOW
        # Use Yahoo ticker for Aurora storage (Aurora stores prices with Yahoo symbols)
        aurora_rows = 0
        if self.enable_aurora and self._aurora_repo:  # ← REMOVED
            aurora_rows = self._write_to_aurora(yahoo_ticker, data)  # ← REMOVED

        return {
            'ticker': ticker,
            'status': 'success',
            'date': today,
            'company_name': data.get('company_name', ticker),
            'aurora_rows': aurora_rows  # ← REMOVED (legacy)
        }
"""

# === SNIPPET 2: fetch_ticker storage logic (AFTER) ===
def fetch_ticker(self, ticker: str) -> Dict[str, Any]:
    """
    Fetch data for a single ticker and cache it.

    (docstring truncated for brevity)
    """
    try:
        # ... (data fetching logic unchanged) ...

        # Store to Aurora ticker_data table (PRIMARY STORAGE - GROUND TRUTH)
        # This must succeed before other storage operations
        if self.precompute_service:
            try:
                self.precompute_service.store_ticker_data(
                    symbol=ticker,
                    data_date=datetime.now(bangkok_tz).date(),
                    price_history=price_history,
                    company_info=company_info,
                    financials=None
                )
                logger.info(f"✅ Stored {ticker} to Aurora ticker_data table ({len(price_history)} rows)")
            except Exception as e:
                logger.error(f"Failed to store {ticker} to Aurora ticker_data: {e}")

        # ... (S3 cache storage - unchanged) ...

        # Store in Data Lake (optional, raw data archival)
        if self.data_lake.is_enabled():
            try:
                self.data_lake.store_ticker_data(ticker, data)
                logger.debug(f"Stored {ticker} to data lake")
            except Exception as e:
                logger.warning(f"Failed to store {ticker} to data lake: {e}")

        # === REMOVED: Legacy Aurora write (lines 240-244) ===
        # aurora_rows = 0
        # if self.enable_aurora and self._aurora_repo:
        #     aurora_rows = self._write_to_aurora(yahoo_ticker, data)

        return {
            'ticker': ticker,
            'status': 'success',
            'date': today,
            'company_name': data.get('company_name', ticker),
            # Removed: 'aurora_rows': aurora_rows (legacy field)
        }

    except Exception as e:
        logger.error(f"Failed to fetch {ticker}: {e}")
        return {
            'ticker': ticker,
            'status': 'failed',
            'error': str(e)
        }


# === SNIPPET 3: _write_to_aurora method (REMOVED ENTIRELY) ===
# Lines 262-303 (OLD) - DELETED
"""
def _write_to_aurora(self, ticker: str, data: Dict[str, Any]) -> int:
    '''
    Write ticker data to Aurora MySQL.

    Args:
        ticker: Yahoo Finance ticker symbol (must be resolved before calling)
        data: Data dict from DataFetcher

    Returns:
        Number of price rows written
    '''
    if not self._aurora_repo:
        return 0

    try:
        # Upsert ticker info
        info = data.get('info', {})
        self._aurora_repo.upsert_ticker_info(
            symbol=ticker,
            display_name=info.get('shortName', ticker),
            company_name=info.get('longName'),
            exchange=info.get('exchange'),
            market=info.get('market'),
            currency=info.get('currency'),
            sector=info.get('sector'),
            industry=info.get('industry'),
            quote_type=info.get('quoteType'),
        )
        logger.debug(f"Aurora: upserted ticker_info for {ticker}")

        # Upsert historical prices
        history = data.get('history')
        if history is not None and isinstance(history, pd.DataFrame) and not history.empty:
            rows = self._aurora_repo.bulk_upsert_from_dataframe(ticker, history)
            logger.info(f"Aurora: upserted {rows} price rows for {ticker}")
            return rows

        return 0

    except Exception as e:
        logger.error(f"Aurora write failed for {ticker}: {e}")
        return 0
"""
# ↑ THIS ENTIRE METHOD IS REMOVED


# === COMPLEXITY COMPARISON ===
"""
BEFORE:
- TickerFetcher.__init__: B (6) - conditional TickerRepository init
- TickerFetcher.fetch_ticker: C (15) - multiple storage paths (S3, DataLake, Aurora legacy, Aurora modern)
- TickerFetcher._write_to_aurora: B (6) - legacy method
Total cyclomatic: 27

AFTER:
- TickerFetcher.__init__: A (3-4) - one less conditional branch
- TickerFetcher.fetch_ticker: B (10-12) - one less storage path
- (Method removed)
Total cyclomatic: 16

REDUCTION: 27 → 16 (-40%)
"""


# === TEST CHANGES REQUIRED ===
"""
Example test that needs updating:

# BEFORE
def test_ticker_fetcher_with_aurora():
    fetcher = TickerFetcher(enable_aurora=True)  # ← Parameter removed
    assert fetcher.enable_aurora is True  # ← Attribute removed
    assert fetcher._aurora_repo is not None  # ← Attribute removed

# AFTER
def test_ticker_fetcher_initializes_precompute_service():
    fetcher = TickerFetcher()  # No enable_aurora parameter
    assert fetcher.precompute_service is not None  # Modern integration

# Tests that mock _write_to_aurora or _aurora_repo need to be removed entirely.
"""
