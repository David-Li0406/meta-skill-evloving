# Concurrency Guidelines

## Avoid Data Races

Use synchronization primitives to protect shared state.

### Identify Shared State

Data races occur when:
1. Multiple threads access the same memory location
2. At least one access is a write
3. No synchronization coordinates the accesses

### Protection Mechanisms

**Mutexes** (C++):
```cpp
#include <mutex>

class ThreadSafeCounter {
    mutable std::mutex mutex_;
    int count_ = 0;

public:
    void increment() {
        std::lock_guard<std::mutex> lock(mutex_);
        ++count_;
    }

    int get() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return count_;
    }
};
```

**Atomic Operations** (C++):
```cpp
#include <atomic>

class ThreadSafeCounter {
    std::atomic<int> count_{0};

public:
    void increment() {
        count_.fetch_add(1, std::memory_order_relaxed);
    }

    int get() const {
        return count_.load(std::memory_order_relaxed);
    }
};
```

**Synchronized Methods** (Kotlin):
```kotlin
class ThreadSafeCounter {
    private var count = 0

    @Synchronized
    fun increment() {
        count++
    }

    @Synchronized
    fun get(): Int = count
}
```

**Locks** (Python):
```python
import threading

class ThreadSafeCounter:
    def __init__(self):
        self._lock = threading.Lock()
        self._count = 0

    def increment(self):
        with self._lock:
            self._count += 1

    def get(self):
        with self._lock:
            return self._count
```

## Choose the Right Concurrency Model

### Threading

**Use when**:
- CPU-bound parallel work
- Need shared memory between concurrent tasks
- Working in languages with real threads (C++, Java, Kotlin)

**Example** (C++):
```cpp
#include <thread>
#include <vector>

void processBatch(const std::vector<int>& data, int start, int end) {
    // Process data[start:end]
}

void parallelProcess(const std::vector<int>& data) {
    const int numThreads = std::thread::hardware_concurrency();
    std::vector<std::thread> threads;

    int chunkSize = data.size() / numThreads;

    for (int i = 0; i < numThreads; ++i) {
        int start = i * chunkSize;
        int end = (i == numThreads - 1) ? data.size() : (i + 1) * chunkSize;
        threads.emplace_back(processBatch, std::ref(data), start, end);
    }

    for (auto& thread : threads) {
        thread.join();
    }
}
```

### Coroutines

**Use when**:
- I/O-bound concurrent work
- Need lightweight concurrency
- Want to avoid callback hell

**Example** (Kotlin):
```kotlin
import kotlinx.coroutines.*

suspend fun fetchUser(id: Int): User {
    return withContext(Dispatchers.IO) {
        // I/O operation
        database.getUser(id)
    }
}

suspend fun fetchPosts(userId: Int): List<Post> {
    return withContext(Dispatchers.IO) {
        api.getPosts(userId)
    }
}

// Concurrent execution
suspend fun getUserWithPosts(id: Int): UserWithPosts = coroutineScope {
    val user = async { fetchUser(id) }
    val posts = async { fetchPosts(id) }

    UserWithPosts(user.await(), posts.await())
}
```

### Async/Await

**Use when**:
- I/O-bound work in languages with async support
- Building responsive UIs
- Handling many concurrent I/O operations

**Example** (TypeScript):
```typescript
async function fetchUserData(userId: number): Promise<UserData> {
    const [user, posts, comments] = await Promise.all([
        fetchUser(userId),
        fetchPosts(userId),
        fetchComments(userId)
    ]);

    return { user, posts, comments };
}
```

**Example** (Python):
```python
import asyncio

async def fetch_user_data(user_id: int) -> UserData:
    user, posts, comments = await asyncio.gather(
        fetch_user(user_id),
        fetch_posts(user_id),
        fetch_comments(user_id)
    )

    return UserData(user, posts, comments)
```

### Process-Based Parallelism

**Use when**:
- True CPU parallelism needed (especially in Python with GIL)
- Isolation between tasks required
- Heavy CPU-bound work

**Example** (Python):
```python
from multiprocessing import Pool

def process_chunk(data_chunk):
    # CPU-intensive processing
    return result

def parallel_process(data, num_processes=4):
    with Pool(num_processes) as pool:
        results = pool.map(process_chunk, data)
    return results
```

## Common Concurrency Patterns

### Producer-Consumer

```cpp
#include <queue>
#include <mutex>
#include <condition_variable>

template<typename T>
class ThreadSafeQueue {
    std::queue<T> queue_;
    mutable std::mutex mutex_;
    std::condition_variable cond_;

public:
    void push(T value) {
        {
            std::lock_guard<std::mutex> lock(mutex_);
            queue_.push(std::move(value));
        }
        cond_.notify_one();
    }

    T pop() {
        std::unique_lock<std::mutex> lock(mutex_);
        cond_.wait(lock, [this] { return !queue_.empty(); });

        T value = std::move(queue_.front());
        queue_.pop();
        return value;
    }
};
```

### Read-Write Lock

```cpp
#include <shared_mutex>

class SharedResource {
    mutable std::shared_mutex mutex_;
    std::string data_;

public:
    // Multiple readers can access simultaneously
    std::string read() const {
        std::shared_lock<std::shared_mutex> lock(mutex_);
        return data_;
    }

    // Only one writer can access
    void write(std::string newData) {
        std::unique_lock<std::shared_mutex> lock(mutex_);
        data_ = std::move(newData);
    }
};
```

### Thread Pool

```cpp
class ThreadPool {
    std::vector<std::thread> workers_;
    ThreadSafeQueue<std::function<void()>> tasks_;
    std::atomic<bool> stop_{false};

public:
    ThreadPool(size_t numThreads) {
        for (size_t i = 0; i < numThreads; ++i) {
            workers_.emplace_back([this] {
                while (!stop_) {
                    auto task = tasks_.pop();
                    if (task) task();
                }
            });
        }
    }

    template<typename Func>
    void submit(Func task) {
        tasks_.push(std::move(task));
    }

    ~ThreadPool() {
        stop_ = true;
        // Wake all threads and join
    }
};
```

## Deadlock Prevention

### Strategies

1. **Lock Ordering**: Always acquire locks in the same order
2. **Timeout**: Use timed locks and retry if timeout occurs
3. **Try-Lock**: Use non-blocking lock attempts
4. **Lock Hierarchy**: Assign levels to locks and only acquire higher levels

### Example: Lock Ordering

```cpp
class BankAccount {
    std::mutex mutex_;
    int balance_;

public:
    friend void transfer(BankAccount& from, BankAccount& to, int amount) {
        // Always lock in address order to prevent deadlock
        std::unique_lock<std::mutex> lock1(from.mutex_, std::defer_lock);
        std::unique_lock<std::mutex> lock2(to.mutex_, std::defer_lock);

        if (&from < &to) {
            lock1.lock();
            lock2.lock();
        } else {
            lock2.lock();
            lock1.lock();
        }

        from.balance_ -= amount;
        to.balance_ += amount;
    }
};
```

## Testing Concurrent Code

### Stress Testing

```cpp
#include <gtest/gtest.h>

TEST(ThreadSafeCounter, StressTest) {
    ThreadSafeCounter counter;
    const int numThreads = 10;
    const int incrementsPerThread = 10000;

    std::vector<std::thread> threads;
    for (int i = 0; i < numThreads; ++i) {
        threads.emplace_back([&counter, incrementsPerThread] {
            for (int j = 0; j < incrementsPerThread; ++j) {
                counter.increment();
            }
        });
    }

    for (auto& t : threads) {
        t.join();
    }

    EXPECT_EQ(counter.get(), numThreads * incrementsPerThread);
}
```

### Race Condition Detection

Use tools to detect race conditions:

- **C++**: ThreadSanitizer (`-fsanitize=thread`)
- **Java/Kotlin**: Concurrency testing frameworks
- **Python**: pytest-timeout, pytest-xdist
