# JVM Memory Model

## Memory Layout

```
+------------------+
|   Method Area    |  <- Class metadata, static fields
+------------------+
|       Heap       |  <- Objects, arrays
|  +------------+  |
|  |   Young    |  |  <- New objects (Eden + Survivor)
|  +------------+  |
|  |    Old     |  |  <- Long-lived objects
|  +------------+  |
+------------------+
|      Stack       |  <- Per-thread, local variables, method calls
+------------------+
|   Native Stack   |  <- JNI calls
+------------------+
```

## Garbage Collection

### GC Algorithms

```java
// G1GC (default since Java 9) - balanced latency/throughput
// -XX:+UseG1GC
// Good for: heap > 4GB, pause time < 200ms

// ZGC (Java 15+) - ultra-low latency
// -XX:+UseZGC
// Good for: heap > 16GB, pause time < 10ms

// Shenandoah (Java 15+) - low latency, Red Hat
// -XX:+UseShenandoahGC

// Parallel GC - high throughput
// -XX:+UseParallelGC
// Good for: batch processing, throughput > latency
```

### GC Tuning Parameters

```bash
# Heap sizing
-Xms4g                    # Initial heap size
-Xmx4g                    # Maximum heap size
-XX:NewRatio=2            # Old/Young ratio (Old = 2x Young)

# G1GC tuning
-XX:MaxGCPauseMillis=200  # Target pause time
-XX:G1HeapRegionSize=8m   # Region size (1-32MB)
-XX:InitiatingHeapOccupancyPercent=45

# ZGC tuning
-XX:ZAllocationSpikeTolerance=2
-XX:ZCollectionInterval=0  # Disable proactive GC

# Logging
-Xlog:gc*:file=gc.log:time,level,tags
```

## Memory Leak Prevention

```java
// 1. Close resources properly
try (Connection conn = dataSource.getConnection();
     PreparedStatement stmt = conn.prepareStatement(sql)) {
    // use resources
}

// 2. Remove listeners when done
public class MyComponent {
    private final EventListener listener;

    public void init() {
        listener = event -> handle(event);
        eventBus.register(listener);
    }

    public void destroy() {
        eventBus.unregister(listener);  // Important!
    }
}

// 3. Use WeakReference for caches
Map<Key, WeakReference<Value>> cache = new WeakHashMap<>();

// 4. Avoid static collections holding object references
// BAD: static List<Object> cache = new ArrayList<>();
// GOOD: Use proper caching library with eviction

// 5. Be careful with inner classes
// Non-static inner class holds reference to outer class
class Outer {
    // BAD: holds reference to Outer
    class Inner {}

    // GOOD: no reference to Outer
    static class StaticInner {}
}
```

## Profiling Tools

```bash
# JFR (Java Flight Recorder)
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr MyApp

# Heap dump
jmap -dump:format=b,file=heap.hprof <pid>

# Thread dump
jstack <pid> > threads.txt

# Native Memory Tracking
java -XX:NativeMemoryTracking=summary MyApp
jcmd <pid> VM.native_memory summary
```

## Performance Best Practices

```java
// 1. Avoid creating unnecessary objects
// BAD
for (int i = 0; i < 1000; i++) {
    String s = new String("constant");  // Creates 1000 objects
}
// GOOD
String s = "constant";  // String pool, single object

// 2. Use StringBuilder for concatenation in loops
StringBuilder sb = new StringBuilder();
for (String item : items) {
    sb.append(item).append(",");
}

// 3. Size collections appropriately
List<String> list = new ArrayList<>(expectedSize);
Map<K, V> map = new HashMap<>(expectedSize, 0.75f);

// 4. Use primitives over wrappers when possible
// BAD: Long sum = 0L;
// GOOD: long sum = 0L;

// 5. Lazy initialization for expensive objects
private volatile ExpensiveObject instance;

public ExpensiveObject getInstance() {
    if (instance == null) {
        synchronized (this) {
            if (instance == null) {
                instance = new ExpensiveObject();
            }
        }
    }
    return instance;
}
```
