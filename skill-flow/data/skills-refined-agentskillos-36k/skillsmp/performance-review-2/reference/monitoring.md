# Performance Metrics and Monitoring

## Set Performance Targets

Define clear, measurable performance goals for your application.

### Common Metrics

| Metric | Description | Typical Target |
|--------|-------------|----------------|
| **Response Time** | Time to complete a request | < 200ms (p95) |
| **Throughput** | Requests processed per second | > 1000 req/s |
| **Memory Usage** | RAM consumed by application | < 512MB (steady state) |
| **CPU Utilization** | CPU usage percentage | < 70% (average) |
| **Error Rate** | Percentage of failed requests | < 0.1% |
| **Uptime** | Percentage of time service is available | > 99.9% |

### Setting Targets

```cpp
// performance_config.h
namespace performance {

// Response time targets (milliseconds)
constexpr int TARGET_RESPONSE_P50 = 50;   // 50th percentile
constexpr int TARGET_RESPONSE_P95 = 200;  // 95th percentile
constexpr int TARGET_RESPONSE_P99 = 500;  // 99th percentile

// Throughput targets
constexpr int TARGET_REQUESTS_PER_SECOND = 1000;

// Resource limits
constexpr size_t MAX_MEMORY_BYTES = 512 * 1024 * 1024;  // 512MB
constexpr double MAX_CPU_UTILIZATION = 0.70;             // 70%

// Availability
constexpr double TARGET_UPTIME = 0.999;  // 99.9%

}  // namespace performance
```

## Monitoring Implementation

### Response Time Tracking

```cpp
#include <chrono>
#include <vector>
#include <algorithm>

class PerformanceMonitor {
    std::vector<std::chrono::microseconds> responseTimes_;
    std::mutex mutex_;

public:
    void recordResponseTime(std::chrono::microseconds duration) {
        std::lock_guard<std::mutex> lock(mutex_);
        responseTimes_.push_back(duration);

        // Keep only recent data (last 10,000 requests)
        if (responseTimes_.size() > 10000) {
            responseTimes_.erase(responseTimes_.begin());
        }
    }

    struct Statistics {
        double p50;
        double p95;
        double p99;
        double average;
    };

    Statistics getStatistics() const {
        std::lock_guard<std::mutex> lock(mutex_);

        if (responseTimes_.empty()) {
            return {0, 0, 0, 0};
        }

        auto sorted = responseTimes_;
        std::sort(sorted.begin(), sorted.end());

        auto percentile = [&sorted](double p) {
            size_t index = static_cast<size_t>(sorted.size() * p);
            return sorted[index].count() / 1000.0;  // Convert to milliseconds
        };

        double sum = 0;
        for (const auto& time : sorted) {
            sum += time.count();
        }
        double average = (sum / sorted.size()) / 1000.0;

        return {
            percentile(0.50),
            percentile(0.95),
            percentile(0.99),
            average
        };
    }
};

// Usage
class RequestHandler {
    PerformanceMonitor& monitor_;

public:
    void handleRequest(const Request& req) {
        auto start = std::chrono::steady_clock::now();

        // Process request
        processRequest(req);

        auto end = std::chrono::steady_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(
            end - start
        );

        monitor_.recordResponseTime(duration);
    }
};
```

### Memory Monitoring

```cpp
#include <sys/resource.h>

class MemoryMonitor {
public:
    struct MemoryUsage {
        size_t residentSetSize;  // RAM actually used
        size_t virtualMemorySize;
    };

    static MemoryUsage getCurrentUsage() {
#ifdef __linux__
        std::ifstream statm("/proc/self/statm");
        long pageSize = sysconf(_SC_PAGESIZE);

        size_t size, resident;
        statm >> size >> resident;

        return {
            resident * pageSize,
            size * pageSize
        };
#elif __APPLE__
        struct rusage usage;
        getrusage(RUSAGE_SELF, &usage);

        return {
            static_cast<size_t>(usage.ru_maxrss),
            0  // Virtual memory not easily available on macOS
        };
#else
        return {0, 0};
#endif
    }

    static std::string formatBytes(size_t bytes) {
        const char* units[] = {"B", "KB", "MB", "GB"};
        int unit = 0;
        double size = bytes;

        while (size >= 1024 && unit < 3) {
            size /= 1024;
            unit++;
        }

        std::ostringstream oss;
        oss << std::fixed << std::setprecision(2) << size << " " << units[unit];
        return oss.str();
    }
};

// Usage
void logMemoryUsage() {
    auto usage = MemoryMonitor::getCurrentUsage();
    logger.info("Memory usage: RSS=" +
                MemoryMonitor::formatBytes(usage.residentSetSize));

    if (usage.residentSetSize > performance::MAX_MEMORY_BYTES) {
        logger.warn("Memory usage exceeds target!");
    }
}
```

### CPU Monitoring

```cpp
#include <thread>

class CpuMonitor {
    struct CpuTimes {
        long long user;
        long long system;
        long long idle;
    };

    static CpuTimes getCpuTimes() {
#ifdef __linux__
        std::ifstream stat("/proc/stat");
        std::string cpu;
        long long user, nice, system, idle;

        stat >> cpu >> user >> nice >> system >> idle;
        return {user + nice, system, idle};
#else
        return {0, 0, 0};
#endif
    }

public:
    static double getCpuUtilization() {
        auto times1 = getCpuTimes();
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        auto times2 = getCpuTimes();

        long long totalDelta = (times2.user - times1.user) +
                              (times2.system - times1.system) +
                              (times2.idle - times1.idle);

        long long idleDelta = times2.idle - times1.idle;

        if (totalDelta == 0) return 0.0;

        return 1.0 - (static_cast<double>(idleDelta) / totalDelta);
    }
};
```

## Monitoring and Alerting

### Logging Performance Metrics

```cpp
class MetricsLogger {
    PerformanceMonitor& perfMonitor_;

public:
    void logMetrics() {
        auto stats = perfMonitor_.getStatistics();
        auto memUsage = MemoryMonitor::getCurrentUsage();
        auto cpuUsage = CpuMonitor::getCpuUtilization();

        logger.info("Performance Metrics",
            "response_p50_ms", stats.p50,
            "response_p95_ms", stats.p95,
            "response_p99_ms", stats.p99,
            "memory_mb", memUsage.residentSetSize / (1024 * 1024),
            "cpu_percent", cpuUsage * 100
        );

        // Check against targets
        if (stats.p95 > performance::TARGET_RESPONSE_P95) {
            logger.warn("Response time exceeds target",
                "actual", stats.p95,
                "target", performance::TARGET_RESPONSE_P95);
        }

        if (cpuUsage > performance::MAX_CPU_UTILIZATION) {
            logger.warn("CPU utilization exceeds target",
                "actual", cpuUsage * 100,
                "target", performance::MAX_CPU_UTILIZATION * 100);
        }
    }
};
```

### Alerting on Regressions

```cpp
class PerformanceAlert {
    struct Thresholds {
        double maxResponseTimeMs;
        double maxCpuUtilization;
        size_t maxMemoryBytes;
    };

    Thresholds thresholds_;
    std::function<void(const std::string&)> alertCallback_;

public:
    PerformanceAlert(Thresholds thresholds,
                    std::function<void(const std::string&)> callback)
        : thresholds_(thresholds), alertCallback_(callback) {}

    void checkMetrics(const PerformanceMonitor::Statistics& stats,
                     size_t memoryUsage,
                     double cpuUtilization) {
        if (stats.p95 > thresholds_.maxResponseTimeMs) {
            alertCallback_(
                "CRITICAL: Response time p95 is " +
                std::to_string(stats.p95) + "ms, exceeds threshold of " +
                std::to_string(thresholds_.maxResponseTimeMs) + "ms"
            );
        }

        if (cpuUtilization > thresholds_.maxCpuUtilization) {
            alertCallback_(
                "WARNING: CPU utilization is " +
                std::to_string(cpuUtilization * 100) +
                "%, exceeds threshold of " +
                std::to_string(thresholds_.maxCpuUtilization * 100) + "%"
            );
        }

        if (memoryUsage > thresholds_.maxMemoryBytes) {
            alertCallback_(
                "WARNING: Memory usage is " +
                MemoryMonitor::formatBytes(memoryUsage) +
                ", exceeds threshold of " +
                MemoryMonitor::formatBytes(thresholds_.maxMemoryBytes)
            );
        }
    }
};

// Usage
PerformanceAlert alert(
    {
        .maxResponseTimeMs = 200,
        .maxCpuUtilization = 0.70,
        .maxMemoryBytes = 512 * 1024 * 1024
    },
    [](const std::string& message) {
        // Send alert (email, Slack, PagerDuty, etc.)
        logger.critical(message);
        sendSlackAlert(message);
    }
);
```

### Integration with Monitoring Tools

**Prometheus Metrics** (C++):
```cpp
#include <prometheus/exposer.h>
#include <prometheus/registry.h>
#include <prometheus/counter.h>
#include <prometheus/histogram.h>
#include <prometheus/gauge.h>

class PrometheusMetrics {
    std::shared_ptr<prometheus::Registry> registry_;
    prometheus::Family<prometheus::Histogram>& responseTimeHistogram_;
    prometheus::Family<prometheus::Gauge>& memoryGauge_;
    prometheus::Family<prometheus::Counter>& requestCounter_;

public:
    PrometheusMetrics()
        : registry_(std::make_shared<prometheus::Registry>()),
          responseTimeHistogram_(prometheus::BuildHistogram()
              .Name("http_request_duration_seconds")
              .Help("HTTP request latency")
              .Register(*registry_)),
          memoryGauge_(prometheus::BuildGauge()
              .Name("process_memory_bytes")
              .Help("Memory usage in bytes")
              .Register(*registry_)),
          requestCounter_(prometheus::BuildCounter()
              .Name("http_requests_total")
              .Help("Total HTTP requests")
              .Register(*registry_)) {}

    void recordRequest(std::chrono::microseconds duration) {
        responseTimeHistogram_.Add({})
            .Observe(duration.count() / 1e6);
        requestCounter_.Add({}).Increment();
    }

    void updateMemory(size_t bytes) {
        memoryGauge_.Add({}).Set(bytes);
    }

    std::shared_ptr<prometheus::Registry> getRegistry() {
        return registry_;
    }
};

// Start Prometheus exporter
prometheus::Exposer exposer{"127.0.0.1:9090"};
exposer.RegisterCollectable(metrics.getRegistry());
```

**StatsD Integration**:
```cpp
#include <statsd_client.h>

class StatsDMetrics {
    statsd::StatsdClient client_;

public:
    StatsDMetrics(const std::string& host, int port)
        : client_{host, port, "myapp"} {}

    void recordResponseTime(std::chrono::milliseconds duration) {
        client_.timing("response_time", duration.count());
    }

    void incrementRequestCount() {
        client_.increment("requests");
    }

    void setMemoryUsage(size_t bytes) {
        client_.gauge("memory_bytes", bytes);
    }
};
```

### Continuous Monitoring

```cpp
class ContinuousMonitor {
    std::atomic<bool> running_{true};
    std::thread monitorThread_;

    void monitorLoop() {
        while (running_) {
            // Collect metrics
            auto stats = perfMonitor_.getStatistics();
            auto memory = MemoryMonitor::getCurrentUsage();
            auto cpu = CpuMonitor::getCpuUtilization();

            // Log metrics
            metricsLogger_.logMetrics();

            // Check alerts
            alert_.checkMetrics(stats, memory.residentSetSize, cpu);

            // Sleep before next check
            std::this_thread::sleep_for(std::chrono::seconds(60));
        }
    }

public:
    void start() {
        monitorThread_ = std::thread(&ContinuousMonitor::monitorLoop, this);
    }

    void stop() {
        running_ = false;
        if (monitorThread_.joinable()) {
            monitorThread_.join();
        }
    }

    ~ContinuousMonitor() {
        stop();
    }
};
```
