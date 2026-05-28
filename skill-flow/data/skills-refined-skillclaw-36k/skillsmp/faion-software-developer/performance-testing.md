---
id: performance-testing
name: "Performance Testing"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Performance Testing

## Overview

Performance testing validates that applications meet speed, scalability, and stability requirements under various load conditions. It includes load testing, stress testing, endurance testing, and profiling to identify bottlenecks and ensure acceptable user experience.

## When to Use

- Before major releases or launches
- After significant code changes affecting performance
- When scaling infrastructure
- Setting performance baselines
- Identifying bottlenecks in critical paths

## Key Principles

- **Test realistic scenarios**: Mirror production usage patterns
- **Establish baselines**: Know normal performance before testing
- **Test in production-like environment**: Similar hardware, data, network
- **Monitor everything**: CPU, memory, I/O, network, application metrics
- **Iterative optimization**: Test, identify, fix, repeat

## Best Practices

### Performance Testing Types

```
┌─────────────────────────────────────────────────────────────┐
│                 PERFORMANCE TEST TYPES                      │
├─────────────────────────────────────────────────────────────┤
│ LOAD TEST                                                   │
│   Purpose: Verify system under expected load                │
│   Duration: Extended period (hours)                         │
│   Users: Normal to peak expected users                      │
├─────────────────────────────────────────────────────────────┤
│ STRESS TEST                                                 │
│   Purpose: Find breaking point                              │
│   Duration: Until failure                                   │
│   Users: Beyond maximum capacity                            │
├─────────────────────────────────────────────────────────────┤
│ SPIKE TEST                                                  │
│   Purpose: Test sudden load increases                       │
│   Duration: Short bursts                                    │
│   Users: Sudden jump from low to high                       │
├─────────────────────────────────────────────────────────────┤
│ ENDURANCE TEST (Soak)                                       │
│   Purpose: Find memory leaks, resource exhaustion           │
│   Duration: Very long (12-72 hours)                         │
│   Users: Normal load sustained                              │
├─────────────────────────────────────────────────────────────┤
│ SCALABILITY TEST                                            │
│   Purpose: Verify horizontal/vertical scaling               │
│   Duration: Varied                                          │
│   Users: Incrementally increasing                           │
└─────────────────────────────────────────────────────────────┘
```

### Locust Load Testing

```python
# locustfile.py
from locust import HttpUser, task, between, events
from locust.runners import MasterRunner
import json
import random

class WebsiteUser(HttpUser):
    """Simulates typical user behavior."""

    wait_time = between(1, 5)  # Wait 1-5 seconds between tasks
    host = "https://api.example.com"

    def on_start(self):
        """Called when user starts. Login and setup."""
        response = self.client.post("/auth/login", json={
            "email": f"user{random.randint(1, 1000)}@example.com",
            "password": "testpassword"
        })
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = None
            self.headers = {}

    @task(10)  # Weight: 10x more likely than weight 1
    def browse_products(self):
        """Simulate browsing products."""
        self.client.get("/api/products", headers=self.headers)

    @task(5)
    def view_product_detail(self):
        """View a specific product."""
        product_id = random.randint(1, 100)
        self.client.get(f"/api/products/{product_id}", headers=self.headers)

    @task(3)
    def search_products(self):
        """Search for products."""
        terms = ["laptop", "phone", "headphones", "camera", "tablet"]
        self.client.get(
            f"/api/products/search?q={random.choice(terms)}",
            headers=self.headers
        )

    @task(1)
    def add_to_cart(self):
        """Add item to cart."""
        self.client.post("/api/cart/items", json={
            "product_id": random.randint(1, 100),
            "quantity": random.randint(1, 3)
        }, headers=self.headers)

    @task(1)
    def checkout(self):
        """Complete checkout (less frequent)."""
        self.client.post("/api/orders", json={
            "payment_method": "card",
            "shipping_address_id": 1
        }, headers=self.headers)


class AdminUser(HttpUser):
    """Simulates admin operations (fewer users)."""

    wait_time = between(2, 10)
    weight = 1  # 1/10th of regular users

    @task
    def view_dashboard(self):
        self.client.get("/admin/dashboard", headers=self.admin_headers)

    @task
    def export_report(self):
        self.client.get("/admin/reports/sales?format=csv", headers=self.admin_headers)


# Custom metrics
@events.request.add_listener
def on_request(request_type, name, response_time, response_length, **kwargs):
    """Log custom metrics."""
    if response_time > 2000:  # > 2 seconds
        print(f"SLOW REQUEST: {name} took {response_time}ms")

# Run with: locust -f locustfile.py --host=https://api.example.com
# Or headless: locust -f locustfile.py --headless -u 100 -r 10 -t 5m
```

### k6 Load Testing

```javascript
// k6-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const loginDuration = new Trend('login_duration');

// Test configuration
export const options = {
  stages: [
    { duration: '2m', target: 50 },   // Ramp up to 50 users
    { duration: '5m', target: 50 },   // Stay at 50 users
    { duration: '2m', target: 100 },  // Ramp up to 100 users
    { duration: '5m', target: 100 },  // Stay at 100 users
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests < 500ms
    http_req_failed: ['rate<0.01'],    // Error rate < 1%
    errors: ['rate<0.05'],             // Custom error rate < 5%
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';

export function setup() {
  // Run once before test
  const loginRes = http.post(`${BASE_URL}/auth/login`, JSON.stringify({
    email: 'loadtest@example.com',
    password: 'testpassword',
  }), {
    headers: { 'Content-Type': 'application/json' },
  });

  return { token: loginRes.json('access_token') };
}

export default function(data) {
  const headers = {
    'Authorization': `Bearer ${data.token}`,
    'Content-Type': 'application/json',
  };

  // Test scenario: Browse and purchase
  const scenarios = [
    () => browseProducts(headers),
    () => searchProducts(headers),
    () => viewProduct(headers),
    () => addToCart(headers),
  ];

  // Random scenario selection
  const scenario = scenarios[Math.floor(Math.random() * scenarios.length)];
  scenario();

  sleep(Math.random() * 3 + 1);  // 1-4 seconds between requests
}

function browseProducts(headers) {
  const res = http.get(`${BASE_URL}/api/products?page=1&limit=20`, { headers });

  check(res, {
    'products status is 200': (r) => r.status === 200,
    'products list not empty': (r) => r.json('data').length > 0,
  }) || errorRate.add(1);
}

function searchProducts(headers) {
  const terms = ['laptop', 'phone', 'tablet'];
  const term = terms[Math.floor(Math.random() * terms.length)];

  const res = http.get(`${BASE_URL}/api/products/search?q=${term}`, { headers });

  check(res, {
    'search status is 200': (r) => r.status === 200,
  }) || errorRate.add(1);
}

function viewProduct(headers) {
  const productId = Math.floor(Math.random() * 100) + 1;
  const res = http.get(`${BASE_URL}/api/products/${productId}`, { headers });

  check(res, {
    'product detail status is 200': (r) => r.status === 200,
    'product has name': (r) => r.json('name') !== undefined,
  }) || errorRate.add(1);
}

function addToCart(headers) {
  const payload = JSON.stringify({
    product_id: Math.floor(Math.random() * 100) + 1,
    quantity: 1,
  });

  const res = http.post(`${BASE_URL}/api/cart/items`, payload, { headers });

  check(res, {
    'add to cart successful': (r) => r.status === 201 || r.status === 200,
  }) || errorRate.add(1);
}

// Run with: k6 run k6-test.js
// Or with cloud: k6 cloud k6-test.js
```

### pytest-benchmark for Micro-benchmarks

```python
import pytest
from decimal import Decimal

def test_price_calculation_performance(benchmark):
    """Benchmark price calculation function."""
    items = [
        {"price": Decimal("10.00"), "quantity": 2},
        {"price": Decimal("25.50"), "quantity": 1},
        {"price": Decimal("5.00"), "quantity": 10},
    ] * 100  # 300 items

    def calculate():
        return sum(item["price"] * item["quantity"] for item in items)

    result = benchmark(calculate)
    assert result == Decimal("7050.00")

def test_json_serialization_performance(benchmark):
    """Compare JSON serialization methods."""
    import json
    import orjson

    data = {"users": [{"id": i, "name": f"User {i}"} for i in range(1000)]}

    def serialize_stdlib():
        return json.dumps(data)

    def serialize_orjson():
        return orjson.dumps(data)

    # Run benchmark
    result = benchmark.pedantic(
        serialize_orjson,
        iterations=100,
        rounds=10
    )

@pytest.mark.benchmark(group="database")
def test_bulk_insert_performance(benchmark, db_session):
    """Benchmark bulk insert vs individual inserts."""
    users = [User(name=f"User {i}", email=f"user{i}@example.com")
             for i in range(1000)]

    def bulk_insert():
        db_session.bulk_save_objects(users)
        db_session.commit()
        db_session.rollback()

    benchmark(bulk_insert)

# Run with: pytest --benchmark-only
# Compare: pytest --benchmark-compare
```

### Application Profiling

```python
# cProfile for function-level profiling
import cProfile
import pstats
from io import StringIO

def profile_function(func):
    """Decorator to profile a function."""
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()

        result = func(*args, **kwargs)

        profiler.disable()
        stream = StringIO()
        stats = pstats.Stats(profiler, stream=stream)
        stats.sort_stats('cumulative')
        stats.print_stats(20)  # Top 20 functions
        print(stream.getvalue())

        return result
    return wrapper

@profile_function
def expensive_operation():
    # Your code here
    pass

# Memory profiling with memory_profiler
from memory_profiler import profile

@profile
def memory_intensive_function():
    """Function with memory profiling."""
    large_list = [i ** 2 for i in range(1000000)]
    return sum(large_list)

# Line-by-line profiling with line_profiler
# Add @profile decorator and run: kernprof -l -v script.py

# Async profiling with py-spy
# Run: py-spy top --pid <PID>
# Or: py-spy record -o profile.svg --pid <PID>
```

### Database Query Performance

```python
import pytest
from sqlalchemy import event
from sqlalchemy.engine import Engine
import time

# Query timing middleware
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop()
    if total > 0.1:  # Log slow queries > 100ms
        print(f"SLOW QUERY ({total:.3f}s): {statement[:100]}...")

# Test query performance
def test_query_performance(db_session, benchmark):
    """Ensure critical queries meet performance requirements."""
    # Seed test data
    for i in range(10000):
        db_session.add(User(name=f"User {i}", email=f"user{i}@example.com"))
    db_session.commit()

    def query_users():
        return db_session.query(User).filter(
            User.name.like("User 5%")
        ).limit(100).all()

    result = benchmark(query_users)

    # Assert query time is acceptable
    assert benchmark.stats.stats.mean < 0.1  # < 100ms average

# N+1 query detection
def test_no_n_plus_one_queries(db_session, caplog):
    """Detect N+1 query problems."""
    import logging
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

    orders = db_session.query(Order).limit(10).all()

    query_count = 0
    for record in caplog.records:
        if 'SELECT' in record.message:
            query_count += 1

    # Should be 1-2 queries, not 11+ (N+1)
    assert query_count < 5, f"Potential N+1: {query_count} queries for 10 orders"
```

### CI/CD Performance Gates

```yaml
# .github/workflows/performance.yml
name: Performance Tests

on:
  push:
    branches: [main]
  pull_request:

jobs:
  load-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Start application
        run: |
          docker-compose up -d
          sleep 30  # Wait for startup

      - name: Run k6 load test
        uses: grafana/k6-action@v0.3.1
        with:
          filename: tests/performance/k6-test.js
          flags: --out json=results.json

      - name: Check performance thresholds
        run: |
          python scripts/check_performance.py results.json

      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: performance-results
          path: results.json

  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run benchmarks
        run: |
          pytest tests/benchmarks/ \
            --benchmark-only \
            --benchmark-json=benchmark.json \
            --benchmark-compare-fail=mean:10%  # Fail if 10% slower

      - name: Store benchmark result
        uses: benchmark-action/github-action-benchmark@v1
        with:
          tool: 'pytest'
          output-file-path: benchmark.json
          fail-on-alert: true
          alert-threshold: '150%'
```

### Performance Monitoring Script

```python
# scripts/check_performance.py
import json
import sys

def check_results(results_file: str) -> bool:
    with open(results_file) as f:
        results = json.load(f)

    thresholds = {
        'http_req_duration_p95': 500,    # 95th percentile < 500ms
        'http_req_failed_rate': 0.01,    # Error rate < 1%
        'http_reqs_rate': 100,           # At least 100 req/s throughput
    }

    passed = True
    for metric, threshold in thresholds.items():
        actual = results.get('metrics', {}).get(metric, {}).get('value', 0)

        if 'rate' in metric or 'failed' in metric:
            check = actual <= threshold
        else:
            check = actual >= threshold if 'rate' in metric else actual <= threshold

        status = "PASS" if check else "FAIL"
        print(f"{metric}: {actual:.2f} (threshold: {threshold}) - {status}")

        if not check:
            passed = False

    return passed

if __name__ == "__main__":
    if not check_results(sys.argv[1]):
        sys.exit(1)
```

## Anti-patterns

- **Testing in unrealistic environments**: Using weak hardware or empty databases
- **Ignoring warm-up time**: Not accounting for JIT compilation, caching
- **Testing single endpoints**: Missing integration performance issues
- **No baseline**: Can't detect regressions without comparison
- **Premature optimization**: Optimizing before measuring
- **Ignoring client-side**: Only testing backend performance

## References

- [Locust Documentation](https://docs.locust.io/)
- [k6 Documentation](https://k6.io/docs/)
- [pytest-benchmark](https://pytest-benchmark.readthedocs.io/)
- [Google Web Vitals](https://web.dev/vitals/)
- [Performance Testing Guidance](https://www.perfmatrix.com/)
