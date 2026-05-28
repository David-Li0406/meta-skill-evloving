#!/usr/bin/env python3
"""
DuckDB Remote Parquet Query Examples

Demonstrates how to query remote Parquet files via HTTP without downloading the entire file.
Uses DuckDB's httpfs extension to perform range requests and leverage column/row pruning.

Prerequisites:
- DuckDB >= 1.0.0
- Internet connection

Usage:
    python remote_query_example.py
"""

import duckdb

# Example: Binance Futures Availability Database (GitHub Releases)
# Replace with your own remote Parquet URL
REMOTE_PARQUET_URL = "https://cdn.jsdelivr.net/gh/your-org/your-repo@main/availability.parquet"


def setup_duckdb_http():
    """Initialize DuckDB connection with httpfs extension for remote queries."""
    conn = duckdb.connect(":memory:")

    # Install and load httpfs extension (enables HTTP/HTTPS reads)
    conn.execute("INSTALL httpfs")
    conn.execute("LOAD httpfs")

    # Optional: Configure HTTP settings
    # conn.execute("SET http_timeout=30000")  # 30 second timeout
    # conn.execute("SET http_retries=3")      # Retry failed requests

    return conn


def example_1_basic_query(conn, url):
    """Example 1: Basic query - Count rows without downloading full file."""
    print("\n=== Example 1: Basic Row Count ===")

    query = f"""
    SELECT COUNT(*) as row_count
    FROM read_parquet('{url}')
    """

    result = conn.execute(query).fetchone()
    print(f"Total rows: {result[0]:,}")


def example_2_column_pruning(conn, url):
    """Example 2: Column pruning - Only read specific columns (saves bandwidth)."""
    print("\n=== Example 2: Column Pruning (Select Specific Columns) ===")

    # Only reads 'date' and 'symbol' columns from Parquet file
    query = f"""
    SELECT date, symbol
    FROM read_parquet('{url}')
    LIMIT 10
    """

    results = conn.execute(query).fetchall()
    print(f"Retrieved {len(results)} rows with 2 columns")
    for row in results[:3]:  # Show first 3
        print(f"  {row}")


def example_3_row_filtering(conn, url):
    """Example 3: Row filtering with WHERE clause (saves bandwidth via predicate pushdown)."""
    print("\n=== Example 3: Row Filtering (WHERE Clause) ===")

    # DuckDB pushes filter to Parquet reader, skips irrelevant row groups
    query = f"""
    SELECT date, symbol, is_available
    FROM read_parquet('{url}')
    WHERE symbol = 'BTCUSDT'
      AND date >= '2024-01-01'
    ORDER BY date
    LIMIT 10
    """

    results = conn.execute(query).fetchall()
    print(f"BTCUSDT availability records (2024+): {len(results)} rows")
    for row in results[:3]:
        print(f"  {row}")


def example_4_aggregation(conn, url):
    """Example 4: Aggregation - Count available days per symbol."""
    print("\n=== Example 4: Aggregation (Count by Symbol) ===")

    query = f"""
    SELECT
        symbol,
        COUNT(*) as total_days,
        SUM(CASE WHEN is_available THEN 1 ELSE 0 END) as available_days,
        ROUND(100.0 * SUM(CASE WHEN is_available THEN 1 ELSE 0 END) / COUNT(*), 2) as availability_pct
    FROM read_parquet('{url}')
    WHERE date >= '2024-01-01'
    GROUP BY symbol
    ORDER BY total_days DESC
    LIMIT 10
    """

    results = conn.execute(query).fetchall()
    print("Top 10 symbols by data coverage (2024):")
    print(f"{'Symbol':<12} {'Total Days':>12} {'Available':>12} {'Availability %':>15}")
    print("-" * 55)
    for row in results:
        print(f"{row[0]:<12} {row[1]:>12,} {row[2]:>12,} {row[3]:>14.2f}%")


def example_5_schema_inspection(conn, url):
    """Example 5: Inspect schema without reading data."""
    print("\n=== Example 5: Schema Inspection ===")

    query = f"""
    DESCRIBE SELECT * FROM read_parquet('{url}')
    """

    results = conn.execute(query).fetchall()
    print("Parquet file schema:")
    print(f"{'Column Name':<20} {'Type':<15} {'Nullable':<10}")
    print("-" * 50)
    for row in results:
        print(f"{row[0]:<20} {row[1]:<15} {'Yes' if row[2] == 'YES' else 'No':<10}")


def example_6_performance_comparison(conn, url):
    """Example 6: Compare query performance with/without filtering."""
    print("\n=== Example 6: Performance Comparison ===")

    import time

    # Query 1: Full scan (no filters)
    start = time.time()
    query1 = f"SELECT COUNT(*) FROM read_parquet('{url}')"
    result1 = conn.execute(query1).fetchone()
    elapsed1 = time.time() - start

    # Query 2: Filtered query (predicate pushdown)
    start = time.time()
    query2 = f"""
    SELECT COUNT(*)
    FROM read_parquet('{url}')
    WHERE symbol = 'BTCUSDT' AND date >= '2024-01-01'
    """
    result2 = conn.execute(query2).fetchone()
    elapsed2 = time.time() - start

    print(f"Full scan:     {result1[0]:,} rows in {elapsed1:.3f}s")
    print(f"Filtered scan: {result2[0]:,} rows in {elapsed2:.3f}s")
    print(f"Speedup: {elapsed1/elapsed2:.2f}x faster with filtering")


def example_7_create_local_view(conn, url):
    """Example 7: Create reusable view for complex queries."""
    print("\n=== Example 7: Create Reusable View ===")

    # Create view (doesn't download data)
    conn.execute(f"""
    CREATE OR REPLACE VIEW availability AS
    SELECT * FROM read_parquet('{url}')
    """)

    # Query the view multiple times
    result1 = conn.execute("SELECT COUNT(DISTINCT symbol) FROM availability").fetchone()
    result2 = conn.execute("SELECT MIN(date), MAX(date) FROM availability").fetchone()

    print(f"Unique symbols: {result1[0]}")
    print(f"Date range: {result2[0]} to {result2[1]}")
    print("\nView created - can now query 'availability' table in subsequent queries")


def example_8_export_filtered_data(conn, url):
    """Example 8: Export filtered subset to local Parquet/CSV."""
    print("\n=== Example 8: Export Filtered Subset ===")

    # Export BTCUSDT data to local Parquet file
    export_query = f"""
    COPY (
        SELECT date, symbol, is_available, file_size_bytes
        FROM read_parquet('{url}')
        WHERE symbol = 'BTCUSDT'
        ORDER BY date
    ) TO '/tmp/btcusdt_availability.parquet' (FORMAT PARQUET)
    """

    conn.execute(export_query)
    print("Exported BTCUSDT data to /tmp/btcusdt_availability.parquet")

    # Verify export
    verify_query = "SELECT COUNT(*) FROM read_parquet('/tmp/btcusdt_availability.parquet')"
    result = conn.execute(verify_query).fetchone()
    print(f"Exported {result[0]:,} rows")


def main():
    """Run all examples."""
    print("=" * 70)
    print("DuckDB Remote Parquet Query Examples")
    print("=" * 70)

    # Initialize DuckDB with HTTP support
    conn = setup_duckdb_http()

    # Note: Replace REMOTE_PARQUET_URL with your actual remote Parquet file
    url = REMOTE_PARQUET_URL

    print(f"\nQuerying remote Parquet file:")
    print(f"  URL: {url}")
    print(f"  Method: HTTP range requests (no full download)")

    try:
        # Run examples
        example_1_basic_query(conn, url)
        example_2_column_pruning(conn, url)
        example_3_row_filtering(conn, url)
        example_4_aggregation(conn, url)
        example_5_schema_inspection(conn, url)
        example_6_performance_comparison(conn, url)
        example_7_create_local_view(conn, url)
        example_8_export_filtered_data(conn, url)

        print("\n" + "=" * 70)
        print("All examples completed successfully!")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Verify remote URL is accessible via HTTP/HTTPS")
        print("2. Check that DuckDB >= 1.0.0 is installed")
        print("3. Ensure httpfs extension is available")
        print("4. Confirm Parquet file format is valid")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
