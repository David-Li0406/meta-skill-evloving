---
name: cpp-specific
version: 1.0.0
description: C++语言特有审查规则（内存管理、并发编程、现代C++特性）
language: cpp
tags: [cpp, c++, memory-management, concurrency, modern-cpp, raii]
frameworks: [qt, boost, stl, eigen]
---

# C++特有审查规则

## 内存管理
- **RAII原则**: 使用智能指针管理资源、避免手动delete、使用构造函数/析构函数
- **智能指针**: 优先使用unique_ptr、共享所有权使用shared_ptr、避免裸指针
- **内存泄漏**: 检查new/delete匹配、使用valgrind检测、避免循环引用
- **资源管理**: 使用lock_guard管理锁、使用fstream管理文件、使用vector管理数组

## 并发编程
- **线程安全**: 使用std::thread、避免数据竞争、使用互斥锁保护共享数据
- **原子操作**: 使用std::atomic、避免锁竞争、使用无锁数据结构
- **异步编程**: 使用std::async、std::future、避免阻塞操作
- **并发容器**: 使用concurrent_queue、避免手动同步容器

## 现代C++特性
- **C++11/14**: 使用auto类型推导、范围for循环、nullptr替代NULL
- **C++17**: 使用if constexpr、结构化绑定、string_view
- **C++20**: 使用concept、协程、ranges库
- **移动语义**: 使用std::move、避免不必要的拷贝、实现移动构造函数

## 性能优化
- **移动语义**: 使用std::move转移资源、实现移动构造函数、避免拷贝
- **内联优化**: 使用inline关键字、避免过度内联、使用constexpr
- **缓存优化**: 使用连续内存容器、避免虚函数、考虑数据局部性
- **编译优化**: 使用-O2/-O3优化、使用LTO链接优化、避免RTTI

## 代码示例

### 正面示例 - RAII和智能指针
```cpp
// 推荐：使用RAII管理资源
class FileHandler {
public:
    explicit FileHandler(const std::string& filename) 
        : file_(filename, std::ios::in | std::ios::out) {
        if (!file_.is_open()) {
            throw std::runtime_error("Failed to open file");
        }
    }
    
    ~FileHandler() {
        if (file_.is_open()) {
            file_.close();
        }
    }
    
    // 删除拷贝构造函数，避免重复管理资源
    FileHandler(const FileHandler&) = delete;
    FileHandler& operator=(const FileHandler&) = delete;
    
    // 允许移动
    FileHandler(FileHandler&&) noexcept = default;
    FileHandler& operator=(FileHandler&&) noexcept = default;
    
private:
    std::fstream file_;
};

// 推荐：使用智能指针
std::unique_ptr<Resource> createResource() {
    return std::make_unique<Resource>();
}

std::shared_ptr<Resource> sharedResource() {
    return std::make_shared<Resource>();
}
```

### 反面示例 - 手动内存管理
```cpp
// 不推荐：手动内存管理
class BadFileHandler {
public:
    BadFileHandler(const std::string& filename) {
        file_ = new std::fstream(filename);
        if (!file_->is_open()) {
            delete file_;  // 容易忘记释放
            throw std::runtime_error("Failed to open file");
        }
    }
    
    ~BadFileHandler() {
        // 如果忘记delete，会造成内存泄漏
    }
    
private:
    std::fstream* file_;  // 裸指针
};
```

### 正面示例 - 现代C++特性
```cpp
// 推荐：使用现代C++特性
#include <vector>
#include <algorithm>
#include <string_view>

// C++17结构化绑定
auto [min_it, max_it] = std::minmax_element(vec.begin(), vec.end());

// C++20 concept
template<typename T>
concept Numeric = std::is_arithmetic_v<T>;

template<Numeric T>
T calculate_average(const std::vector<T>& values) {
    if (values.empty()) return T{};
    
    auto sum = std::reduce(values.begin(), values.end(), T{});
    return sum / static_cast<T>(values.size());
}

// C++20协程
#include <coroutine>
#include <iostream>

struct Generator {
    struct promise_type {
        int current_value;
        
        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        
        std::suspend_always initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        
        std::suspend_always yield_value(int value) {
            current_value = value;
            return {};
        }
        
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };
    
    std::coroutine_handle<promise_type> h;
    
    Generator(std::coroutine_handle<promise_type> h) : h(h) {}
    ~Generator() { if (h) h.destroy(); }
    
    int next() {
        h.resume();
        return h.promise().current_value;
    }
};

Generator fibonacci() {
    int a = 0, b = 1;
    while (true) {
        co_yield a;
        auto next = a + b;
        a = b;
        b = next;
    }
}
```

### 反面示例 - 过时写法
```cpp
// 不推荐：使用C风格代码
int* create_array(int size) {
    int* arr = new int[size];  // 需要手动释放
    for (int i = 0; i < size; ++i) {
        arr[i] = i * 2;
    }
    return arr;
}

// 不推荐：使用宏
#define MAX(a, b) ((a) > (b) ? (a) : (b))  // 容易出错
```

### 正面示例 - 并发编程
```cpp
// 推荐：使用现代C++并发特性
#include <thread>
#include <mutex>
#include <future>
#include <vector>

class ThreadSafeCounter {
public:
    void increment() {
        std::lock_guard<std::mutex> lock(mutex_);
        ++value_;
    }
    
    int get() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return value_;
    }
    
private:
    mutable std::mutex mutex_;
    int value_ = 0;
};

// 推荐：使用async/future
std::future<int> async_calculation(int x) {
    return std::async(std::launch::async, [x]() {
        // 耗时计算
        return x * x + 42;
    });
}

// 推荐：使用原子操作
std::atomic<int> atomic_counter{0};

void atomic_increment() {
    atomic_counter.fetch_add(1, std::memory_order_relaxed);
}
```

### 反面示例 - 线程安全问题
```cpp
// 不推荐：无保护的共享数据
class BadCounter {
public:
    void increment() {
        ++value_;  // 数据竞争
    }
    
    int get() const {
        return value_;
    }
    
private:
    int value_ = 0;  // 无保护
};

// 不推荐：手动线程管理
void bad_thread_usage() {
    int result = 0;
    std::thread t([&result]() {
        result = 42;  // 潜在的数据竞争
    });
    t.detach();  // 不推荐：分离线程
    std::cout << result << std::endl;  // 未定义行为
}
```

### 正面示例 - 移动语义
```cpp
// 推荐：使用移动语义避免拷贝
class DataBuffer {
public:
    DataBuffer(size_t size) : data_(new int[size]), size_(size) {}
    
    // 移动构造函数
    DataBuffer(DataBuffer&& other) noexcept 
        : data_(other.data_), size_(other.size_) {
        other.data_ = nullptr;
        other.size_ = 0;
    }
    
    // 移动赋值运算符
    DataBuffer& operator=(DataBuffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            data_ = other.data_;
            size_ = other.size_;
            other.data_ = nullptr;
            other.size_ = 0;
        }
        return *this;
    }
    
    ~DataBuffer() {
        delete[] data_;
    }
    
private:
    int* data_;
    size_t size_;
};

// 使用示例
DataBuffer create_buffer(size_t size) {
    return DataBuffer(size);  // 返回值优化(RVO)
}
```

### 反面示例 - 不必要的拷贝
```cpp
// 不推荐：不必要的拷贝
class BadBuffer {
public:
    BadBuffer(const std::vector<int>& data) : data_(data) {}  // 拷贝
    
    std::vector<int> get_data() const {  // 返回拷贝
        return data_;
    }
    
private:
    std::vector<int> data_;
};
