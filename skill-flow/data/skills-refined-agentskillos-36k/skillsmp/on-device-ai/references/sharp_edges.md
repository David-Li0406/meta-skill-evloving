# On Device Ai - Sharp Edges

## Webgpu Not Available

### **Id**
webgpu-not-available
### **Summary**
WebGPU not available on user's browser
### **Severity**
critical
### **Situation**
Assuming WebGPU support
### **Why**
  WebGPU support varies widely (as of 2025):
  - Chrome 113+: Full support
  - Edge 113+: Full support
  - Firefox 141+: Windows only, behind flag on other platforms
  - Safari: macOS 26+, iOS 26+
  - Android: Chrome 121+ with compatible GPU
  
  If you build for WebGPU without fallback, many users get errors.
  
### **Detection Pattern**
  device.*webgpu(?!.*fallback|wasm|check)
  
### **Solution**
  Always check and provide fallback:
  
  ```typescript
  interface GPUCapabilities {
    webgpu: boolean;
    webgl: boolean;
    wasm: boolean;
    recommended: "webgpu" | "webgl" | "wasm";
  }
  
  async function checkGPUCapabilities(): Promise<GPUCapabilities> {
    const capabilities: GPUCapabilities = {
      webgpu: false,
      webgl: false,
      wasm: true, // Always available
      recommended: "wasm",
    };
  
    // Check WebGPU
    if ("gpu" in navigator) {
      try {
        const adapter = await navigator.gpu.requestAdapter();
        if (adapter) {
          const device = await adapter.requestDevice();
          if (device) {
            capabilities.webgpu = true;
            capabilities.recommended = "webgpu";
          }
        }
      } catch {
        // WebGPU not available
      }
    }
  
    // Check WebGL as fallback
    try {
      const canvas = document.createElement("canvas");
      const gl = canvas.getContext("webgl2") || canvas.getContext("webgl");
      if (gl) {
        capabilities.webgl = true;
        if (!capabilities.webgpu) {
          capabilities.recommended = "webgl";
        }
      }
    } catch {
      // WebGL not available
    }
  
    return capabilities;
  }
  
  // Use in model loading
  async function loadModelWithFallback(modelId: string) {
    const caps = await checkGPUCapabilities();
  
    console.log(`Using ${caps.recommended} backend`);
  
    return pipeline("text-generation", modelId, {
      device: caps.recommended === "webgpu" ? "webgpu" : "wasm",
      dtype: caps.recommended === "webgpu" ? "q4" : "q8",
    });
  }
  ```
  

## Memory Exhaustion

### **Id**
memory-exhaustion
### **Summary**
Browser runs out of memory
### **Severity**
critical
### **Situation**
Loading large models or multiple models
### **Why**
  Browser memory is limited:
  - Chrome: ~4GB per tab (can be less on 32-bit)
  - Safari: More aggressive memory limits
  - Mobile: Often 2-4GB total for browser
  
  A 7B quantized model needs ~4GB. Add embeddings and you're over.
  
### **Detection Pattern**
  pipeline.*7B|8B|13B(?!.*mobile.*check)
  
### **Solution**
  Monitor memory and use appropriate models:
  
  ```typescript
  interface MemoryStatus {
    available: number | null; // MB
    total: number | null;
    canLoad: boolean;
    recommendedModel: string;
  }
  
  async function checkMemoryForModel(modelSizeMB: number): Promise<MemoryStatus> {
    const status: MemoryStatus = {
      available: null,
      total: null,
      canLoad: true,
      recommendedModel: "Llama-3.2-1B-Instruct-q4f16_1-MLC",
    };
  
    // Check if memory API is available (Chrome)
    if ("memory" in performance) {
      const memory = (performance as any).memory;
      status.total = Math.round(memory.jsHeapSizeLimit / 1024 / 1024);
      status.available = Math.round((memory.jsHeapSizeLimit - memory.usedJSHeapSize) / 1024 / 1024);
    }
  
    // Estimate based on device
    const isMobile = /iPhone|iPad|Android/i.test(navigator.userAgent);
  
    if (isMobile) {
      // Conservative: assume 2GB available
      status.available = status.available ?? 2000;
      status.recommendedModel = "Llama-3.2-1B-Instruct-q4f16_1-MLC"; // 1B
    } else {
      // Desktop: assume 4GB available
      status.available = status.available ?? 4000;
  
      if (status.available > 6000) {
        status.recommendedModel = "Phi-3.5-mini-instruct-q4f16_1-MLC"; // 3.8B
      } else if (status.available > 3000) {
        status.recommendedModel = "Llama-3.2-3B-Instruct-q4f16_1-MLC"; // 3B
      }
    }
  
    // Check if requested model fits
    const safetyMargin = 500; // MB for other operations
    status.canLoad = (status.available - safetyMargin) >= modelSizeMB;
  
    return status;
  }
  
  // Model size estimates (Q4 quantized)
  const MODEL_SIZES_MB = {
    "Llama-3.2-1B-Instruct-q4f16_1-MLC": 700,
    "Llama-3.2-3B-Instruct-q4f16_1-MLC": 1800,
    "Phi-3.5-mini-instruct-q4f16_1-MLC": 2200,
    "Llama-3.1-8B-Instruct-q4f16_1-MLC": 4500,
  };
  ```
  

## Slow First Load

### **Id**
slow-first-load
### **Summary**
First model load takes 30+ seconds
### **Severity**
high
### **Situation**
User waits for model download
### **Why**
  First-time model download is slow:
  - 1B model: ~500MB-1GB download
  - 3B model: ~1.5-2GB download
  - User on slow connection: minutes of waiting
  
  Users leave before model loads.
  
### **Detection Pattern**
  await.*pipeline|CreateMLCEngine(?!.*progress|loading)
  
### **Solution**
  Show progress and offer preload:
  
  ```typescript
  import { useState, useEffect } from "react";
  
  interface LoadingState {
    stage: "idle" | "downloading" | "compiling" | "ready" | "error";
    progress: number; // 0-1
    bytesLoaded: number;
    totalBytes: number;
    estimatedTimeLeft: number; // seconds
    error?: string;
  }
  
  function useModelLoading(modelId: string) {
    const [state, setState] = useState<LoadingState>({
      stage: "idle",
      progress: 0,
      bytesLoaded: 0,
      totalBytes: 0,
      estimatedTimeLeft: 0,
    });
  
    const [startTime, setStartTime] = useState<number | null>(null);
  
    const load = useCallback(async () => {
      setState((s) => ({ ...s, stage: "downloading" }));
      setStartTime(Date.now());
  
      try {
        await CreateMLCEngine(modelId, {
          initProgressCallback: (report) => {
            const elapsed = (Date.now() - (startTime ?? Date.now())) / 1000;
            const rate = report.progress > 0 ? elapsed / report.progress : 0;
            const remaining = rate * (1 - report.progress);
  
            setState({
              stage: report.text.includes("compil") ? "compiling" : "downloading",
              progress: report.progress,
              bytesLoaded: 0, // Would need to track from fetch
              totalBytes: 0,
              estimatedTimeLeft: remaining,
            });
          },
        });
  
        setState((s) => ({ ...s, stage: "ready", progress: 1 }));
      } catch (error) {
        setState((s) => ({
          ...s,
          stage: "error",
          error: error instanceof Error ? error.message : "Unknown error",
        }));
      }
    }, [modelId, startTime]);
  
    return { state, load };
  }
  
  // Loading UI component
  function ModelLoadingUI({ state }: { state: LoadingState }) {
    if (state.stage === "idle") {
      return <button onClick={load}>Load AI Model</button>;
    }
  
    if (state.stage === "error") {
      return <div className="error">Failed to load: {state.error}</div>;
    }
  
    if (state.stage === "ready") {
      return <div className="success">Model ready!</div>;
    }
  
    return (
      <div className="loading">
        <div className="progress-bar">
          <div style={{ width: `${state.progress * 100}%` }} />
        </div>
        <p>
          {state.stage === "downloading" ? "Downloading" : "Preparing"} model...
          {" "}{(state.progress * 100).toFixed(0)}%
        </p>
        {state.estimatedTimeLeft > 0 && (
          <p className="eta">
            ~{Math.ceil(state.estimatedTimeLeft)}s remaining
          </p>
        )}
      </div>
    );
  }
  ```
  

## Main Thread Blocking

### **Id**
main-thread-blocking
### **Summary**
UI freezes during inference
### **Severity**
high
### **Situation**
Running inference on main thread
### **Why**
  Large inference operations block the main thread:
  - Text generation: 100-500ms per token
  - Embeddings: 50-200ms per text
  - Users can't scroll, click, or interact
  
  Even with WebGPU, JS-side operations block.
  
### **Detection Pattern**
  await.*generate|pipeline\((?!.*Worker)
  
### **Solution**
  Use Web Workers for heavy operations:
  
  ```typescript
  // worker.ts
  import { pipeline } from "@huggingface/transformers";
  
  let generator: Awaited<ReturnType<typeof pipeline>> | null = null;
  
  self.onmessage = async (event) => {
    const { type, data, id } = event.data;
  
    try {
      if (type === "load") {
        generator = await pipeline("text-generation", data.modelId, {
          device: "webgpu",
          dtype: "q4",
          progress_callback: (p) => {
            self.postMessage({ type: "progress", id, progress: p.progress });
          },
        });
        self.postMessage({ type: "loaded", id });
      }
  
      if (type === "generate") {
        if (!generator) throw new Error("Model not loaded");
  
        const result = await generator(data.prompt, {
          max_new_tokens: data.maxTokens ?? 256,
          temperature: data.temperature ?? 0.7,
        });
  
        self.postMessage({
          type: "result",
          id,
          text: result[0].generated_text,
        });
      }
    } catch (error) {
      self.postMessage({
        type: "error",
        id,
        error: error instanceof Error ? error.message : "Unknown error",
      });
    }
  };
  
  // main.ts
  class AIWorker {
    private worker: Worker;
    private pending = new Map<string, {
      resolve: (value: unknown) => void;
      reject: (error: Error) => void;
    }>();
    private idCounter = 0;
  
    constructor() {
      this.worker = new Worker(new URL("./worker.ts", import.meta.url), {
        type: "module",
      });
  
      this.worker.onmessage = (event) => {
        const { type, id, ...data } = event.data;
        const handler = this.pending.get(id);
  
        if (type === "progress") {
          // Handle progress updates
          return;
        }
  
        if (handler) {
          if (type === "error") {
            handler.reject(new Error(data.error));
          } else {
            handler.resolve(data);
          }
          this.pending.delete(id);
        }
      };
    }
  
    private call<T>(type: string, data: unknown): Promise<T> {
      const id = String(this.idCounter++);
  
      return new Promise((resolve, reject) => {
        this.pending.set(id, { resolve: resolve as any, reject });
        this.worker.postMessage({ type, id, data });
      });
    }
  
    load(modelId: string) {
      return this.call<void>("load", { modelId });
    }
  
    generate(prompt: string, options?: { maxTokens?: number; temperature?: number }) {
      return this.call<{ text: string }>("generate", { prompt, ...options });
    }
  }
  ```
  

## Model Not Cached

### **Id**
model-not-cached
### **Summary**
Model re-downloads on every visit
### **Severity**
medium
### **Situation**
Browser clears cache or user clears data
### **Why**
  Model caching can fail:
  - Private browsing: No persistent cache
  - Low storage: Browser evicts large files
  - User clears data: Loses cached models
  - Cache expired: Models re-download
  
  500MB+ downloads on every visit is unacceptable.
  
### **Detection Pattern**
  pipeline|CreateMLCEngine(?!.*cache.*check|storage)
  
### **Solution**
  Check cache status and inform users:
  
  ```typescript
  interface CacheStatus {
    modelId: string;
    cached: boolean;
    sizeBytes: number;
    lastAccessed?: Date;
  }
  
  async function checkModelCache(modelId: string): Promise<CacheStatus> {
    // Check Cache API
    if ("caches" in window) {
      const cacheNames = await caches.keys();
  
      for (const name of cacheNames) {
        if (name.includes(modelId) || name.includes("transformers")) {
          const cache = await caches.open(name);
          const keys = await cache.keys();
  
          // Check if model files are cached
          const modelFiles = keys.filter((k) =>
            k.url.includes(modelId) || k.url.includes("model")
          );
  
          if (modelFiles.length > 0) {
            let totalSize = 0;
            for (const req of modelFiles) {
              const resp = await cache.match(req);
              if (resp) {
                const blob = await resp.blob();
                totalSize += blob.size;
              }
            }
  
            return {
              modelId,
              cached: true,
              sizeBytes: totalSize,
            };
          }
        }
      }
    }
  
    // Check IndexedDB
    try {
      const databases = await indexedDB.databases();
      for (const db of databases) {
        if (db.name?.includes(modelId)) {
          return {
            modelId,
            cached: true,
            sizeBytes: 0, // Can't easily get size from IndexedDB
          };
        }
      }
    } catch {
      // IndexedDB not available
    }
  
    return {
      modelId,
      cached: false,
      sizeBytes: 0,
    };
  }
  
  // Show appropriate UI
  async function ModelLoader({ modelId }: { modelId: string }) {
    const cacheStatus = await checkModelCache(modelId);
  
    if (cacheStatus.cached) {
      return (
        <div>
          <p>Model cached locally ({formatBytes(cacheStatus.sizeBytes)})</p>
          <button onClick={load}>Load instantly</button>
        </div>
      );
    }
  
    return (
      <div>
        <p>First-time download required (~{MODEL_SIZES[modelId]}MB)</p>
        <p>This may take 1-3 minutes on a typical connection.</p>
        <button onClick={load}>Download & Load</button>
      </div>
    );
  }
  ```
  

## Quantization Quality

### **Id**
quantization-quality
### **Summary**
Q4 quantization produces poor quality output
### **Severity**
medium
### **Situation**
Using aggressive quantization
### **Why**
  More aggressive quantization = smaller model + faster inference
  BUT also = lower quality:
  - FP32: Full quality, huge size
  - FP16: Near-full quality, half size
  - Q8: Good quality, quarter size
  - Q4: Noticeable degradation, eighth size
  
  For some tasks (code, math), Q4 quality is unacceptable.
  
### **Detection Pattern**
  dtype.*q4.*code|math|precise
  
### **Solution**
  Match quantization to task requirements:
  
  ```typescript
  type TaskType = "chat" | "code" | "math" | "embedding" | "classification";
  
  interface QuantizationConfig {
    recommended: "fp32" | "fp16" | "q8" | "q4";
    fallback: "fp32" | "fp16" | "q8" | "q4";
    reason: string;
  }
  
  function getQuantizationForTask(task: TaskType): QuantizationConfig {
    switch (task) {
      case "chat":
        return {
          recommended: "q4",
          fallback: "q8",
          reason: "Casual conversation tolerates some quality loss",
        };
  
      case "code":
        return {
          recommended: "q8",
          fallback: "fp16",
          reason: "Code generation needs higher precision for syntax accuracy",
        };
  
      case "math":
        return {
          recommended: "fp16",
          fallback: "fp32",
          reason: "Math requires high precision for correct calculations",
        };
  
      case "embedding":
        return {
          recommended: "fp32",
          fallback: "fp16",
          reason: "Embeddings need full precision for accurate similarity",
        };
  
      case "classification":
        return {
          recommended: "q8",
          fallback: "q4",
          reason: "Classification is robust to quantization",
        };
  
      default:
        return {
          recommended: "q4",
          fallback: "q8",
          reason: "Default to smallest for general use",
        };
    }
  }
  
  // Adaptive loading based on task
  async function loadModelForTask(modelId: string, task: TaskType) {
    const config = getQuantizationForTask(task);
    const memory = await checkMemoryForModel(MODEL_SIZES_MB[modelId]);
  
    // Use recommended if memory allows, otherwise fallback
    const dtype = memory.available! > 4000 ? config.recommended : config.fallback;
  
    return pipeline(taskToPipeline(task), modelId, { dtype });
  }
  ```
  

## Mobile Performance

### **Id**
mobile-performance
### **Summary**
Inference too slow on mobile devices
### **Severity**
high
### **Situation**
Running models on mobile browsers
### **Why**
  Mobile GPUs are much weaker than desktop:
  - iPhone 15 Pro GPU: ~10-20 tokens/sec
  - Older phones: <5 tokens/sec
  - Android varies wildly by device
  
  Desktop-sized models are unusable on mobile.
  
### **Detection Pattern**
  3B|7B|8B(?!.*isMobile.*check)
  
### **Solution**
  Detect device and adapt model choice:
  
  ```typescript
  interface DeviceCapabilities {
    isMobile: boolean;
    isLowEnd: boolean;
    recommendedMaxParams: number;
    recommendedModel: string;
  }
  
  function detectDeviceCapabilities(): DeviceCapabilities {
    const ua = navigator.userAgent;
    const isMobile = /iPhone|iPad|iPod|Android/i.test(ua);
  
    // Check for low-end indicators
    const hardwareConcurrency = navigator.hardwareConcurrency ?? 4;
    const deviceMemory = (navigator as any).deviceMemory ?? 4; // GB
    const isLowEnd = hardwareConcurrency <= 4 || deviceMemory <= 4;
  
    let recommendedMaxParams: number;
    let recommendedModel: string;
  
    if (isMobile) {
      if (isLowEnd) {
        recommendedMaxParams = 500_000_000; // 500M
        recommendedModel = "Xenova/Phi-2"; // Not ideal, but works
      } else {
        recommendedMaxParams = 1_000_000_000; // 1B
        recommendedModel = "Llama-3.2-1B-Instruct-q4f16_1-MLC";
      }
    } else {
      if (isLowEnd) {
        recommendedMaxParams = 3_000_000_000; // 3B
        recommendedModel = "Llama-3.2-3B-Instruct-q4f16_1-MLC";
      } else {
        recommendedMaxParams = 8_000_000_000; // 8B
        recommendedModel = "Phi-3.5-mini-instruct-q4f16_1-MLC";
      }
    }
  
    return {
      isMobile,
      isLowEnd,
      recommendedMaxParams,
      recommendedModel,
    };
  }
  
  // Warn user about performance
  function PerformanceWarning({ modelParams }: { modelParams: number }) {
    const device = detectDeviceCapabilities();
  
    if (modelParams > device.recommendedMaxParams) {
      return (
        <div className="warning">
          <p>
            This model may run slowly on your device.
            Consider using {device.recommendedModel} instead.
          </p>
        </div>
      );
    }
  
    return null;
  }
  ```
  

## Concurrent Inference

### **Id**
concurrent-inference
### **Summary**
Running multiple inferences crashes browser
### **Severity**
high
### **Situation**
Parallel model calls
### **Why**
  Each inference uses significant GPU memory:
  - Running 2+ inferences simultaneously can OOM
  - WebGPU doesn't handle concurrent requests well
  - No built-in queuing mechanism
  
### **Detection Pattern**
  Promise\.all.*generate|parallel.*inference
  
### **Solution**
  Queue inference requests:
  
  ```typescript
  class InferenceQueue {
    private queue: Array<{
      fn: () => Promise<unknown>;
      resolve: (value: unknown) => void;
      reject: (error: Error) => void;
    }> = [];
    private running = false;
  
    async enqueue<T>(fn: () => Promise<T>): Promise<T> {
      return new Promise((resolve, reject) => {
        this.queue.push({ fn, resolve: resolve as any, reject });
        this.process();
      });
    }
  
    private async process(): Promise<void> {
      if (this.running || this.queue.length === 0) return;
  
      this.running = true;
  
      while (this.queue.length > 0) {
        const { fn, resolve, reject } = this.queue.shift()!;
  
        try {
          const result = await fn();
          resolve(result);
        } catch (error) {
          reject(error instanceof Error ? error : new Error(String(error)));
        }
      }
  
      this.running = false;
    }
  }
  
  // Usage
  const queue = new InferenceQueue();
  
  // These run sequentially, not in parallel
  const results = await Promise.all([
    queue.enqueue(() => model.generate("prompt 1")),
    queue.enqueue(() => model.generate("prompt 2")),
    queue.enqueue(() => model.generate("prompt 3")),
  ]);
  ```
  