# Unity LLM Integration

## Patterns


---
  #### **Name**
LLMUnity Basic Setup
  #### **Description**
Standard LLMUnity configuration for Unity projects
  #### **When**
Starting a new Unity project with LLM features
  #### **Example**
    // 1. Install via Package Manager
    // Add git URL: https://github.com/undreamai/LLMUnity.git
    
    // 2. Create LLM GameObject
    using LLMUnity;
    
    public class LLMManager : MonoBehaviour
    {
        public LLM llm;
        public LLMCharacter character;
    
        void Start()
        {
            // LLM and LLMCharacter are set up in Inspector
            // Model downloaded via LLM Model Manager window
        }
    
        public async void GetResponse(string playerInput)
        {
            // Non-blocking call
            string response = await character.Chat(playerInput);
            Debug.Log($"NPC says: {response}");
        }
    }
    
    // 3. Inspector Configuration:
    // - LLM: Set model path, context size (2048-4096)
    // - LLMCharacter: Set system prompt, temperature (0.7)
    

---
  #### **Name**
Async Dialogue with UniTask
  #### **Description**
Non-blocking dialogue using UniTask for better async control
  #### **When**
Need cancellation, timeouts, or complex async flow
  #### **Example**
    using Cysharp.Threading.Tasks;
    using LLMUnity;
    using System.Threading;
    
    public class AsyncDialogueManager : MonoBehaviour
    {
        public LLMCharacter character;
        private CancellationTokenSource cts;
    
        public async UniTask<string> GetResponseAsync(
            string input,
            float timeout = 5f)
        {
            cts?.Cancel();
            cts = new CancellationTokenSource();
    
            try
            {
                // Race between response and timeout
                var responseTask = character.Chat(input)
                    .AsUniTask()
                    .AttachExternalCancellation(cts.Token);
    
                var timeoutTask = UniTask.Delay(
                    TimeSpan.FromSeconds(timeout),
                    cancellationToken: cts.Token);
    
                var (hasResponse, response) = await UniTask.WhenAny(
                    responseTask,
                    timeoutTask.ContinueWith(() => (string)null));
    
                if (hasResponse)
                    return response;
    
                // Timeout - return fallback
                return GetFallbackResponse(input);
            }
            catch (OperationCanceledException)
            {
                return GetFallbackResponse(input);
            }
        }
    
        private string GetFallbackResponse(string input)
        {
            // Pre-written fallbacks for common inputs
            return "Hmm, let me think about that...";
        }
    
        void OnDestroy()
        {
            cts?.Cancel();
            cts?.Dispose();
        }
    }
    

---
  #### **Name**
Platform-Specific Model Loading
  #### **Description**
Load appropriate model size based on target platform
  #### **When**
Building for multiple platforms with different capabilities
  #### **Example**
    using LLMUnity;
    using UnityEngine;
    
    public class PlatformModelLoader : MonoBehaviour
    {
        [Header("Model Paths (set in StreamingAssets)")]
        public string desktopModel = "models/llama-8b-q4.gguf";
        public string mobileModel = "models/qwen-1.5b-q4.gguf";
        public string webModel = ""; // Cloud API only
    
        public LLM llm;
    
        void Awake()
        {
            ConfigureForPlatform();
        }
    
        void ConfigureForPlatform()
        {
            #if UNITY_STANDALONE || UNITY_EDITOR
                llm.SetModel(desktopModel);
                llm.numGPULayers = -1; // Full GPU offload
                llm.contextSize = 4096;
            #elif UNITY_ANDROID || UNITY_IOS
                llm.SetModel(mobileModel);
                llm.numGPULayers = 0; // CPU only on mobile
                llm.contextSize = 2048;
                llm.numThreads = 4;
            #elif UNITY_WEBGL
                // WebGL can't run local LLMs effectively
                // Switch to cloud API
                Debug.LogWarning("WebGL: Using cloud API fallback");
                enabled = false;
            #endif
        }
    }
    

---
  #### **Name**
Streaming Response Display
  #### **Description**
Show LLM responses as they're generated for better UX
  #### **When**
Dialogue boxes, chat interfaces, or any text display
  #### **Example**
    using LLMUnity;
    using TMPro;
    using UnityEngine;
    
    public class StreamingDialogue : MonoBehaviour
    {
        public LLMCharacter character;
        public TMP_Text dialogueText;
        public GameObject thinkingIndicator;
    
        private bool isGenerating = false;
    
        public void OnPlayerSpeak(string input)
        {
            if (isGenerating) return;
            StartCoroutine(StreamResponse(input));
        }
    
        private IEnumerator StreamResponse(string input)
        {
            isGenerating = true;
            dialogueText.text = "";
            thinkingIndicator.SetActive(true);
    
            // Small delay for natural pacing
            yield return new WaitForSeconds(0.3f);
            thinkingIndicator.SetActive(false);
    
            // Stream the response token by token
            yield return character.Chat(
                input,
                callback: (partialResponse) =>
                {
                    dialogueText.text = partialResponse;
                },
                completionCallback: () =>
                {
                    isGenerating = false;
                }
            );
        }
    }
    

---
  #### **Name**
Memory-Safe Model Management
  #### **Description**
Properly load and unload models to prevent memory issues
  #### **When**
Switching between NPCs or scenes with different models
  #### **Example**
    using LLMUnity;
    using UnityEngine;
    using System.Collections;
    
    public class ModelManager : MonoBehaviour
    {
        public LLM llm;
        private string currentModelPath = null;
    
        public IEnumerator SwitchModel(string newModelPath)
        {
            if (currentModelPath == newModelPath)
                yield break;
    
            // Unload current model first
            if (currentModelPath != null)
            {
                Debug.Log("Unloading current model...");
                yield return llm.Unload();
    
                // Force garbage collection to free memory
                System.GC.Collect();
                yield return Resources.UnloadUnusedAssets();
            }
    
            // Load new model
            Debug.Log($"Loading model: {newModelPath}");
            llm.SetModel(newModelPath);
            yield return llm.Load();
    
            currentModelPath = newModelPath;
            Debug.Log("Model loaded successfully");
        }
    
        // Call when changing scenes
        void OnDestroy()
        {
            if (llm != null && currentModelPath != null)
            {
                StartCoroutine(UnloadOnDestroy());
            }
        }
    
        private IEnumerator UnloadOnDestroy()
        {
            yield return llm.Unload();
        }
    }
    

---
  #### **Name**
Build Verification Workflow
  #### **Description**
Systematic testing across platforms to catch LLM issues
  #### **When**
Preparing for release or testing new LLM features
  #### **Example**
    // Build verification checklist for LLM Unity games
    
    /*
    PRE-BUILD CHECKS:
    1. Verify model files are in StreamingAssets
    2. Check LLMUnity package is latest stable version
    3. Confirm platform-specific settings in LLM component
    
    WINDOWS BUILD:
    - Test with both CUDA and CPU fallback
    - Verify DLL dependencies are included
    - Check model loads without editor context
    
    MACOS BUILD:
    - Test on both Intel and Apple Silicon
    - Verify code signing doesn't break dylibs
    - Check Metal acceleration works
    
    ANDROID BUILD:
    - Use IL2CPP, not Mono
    - Test on low-end device (2GB RAM)
    - Verify 32-bit and 64-bit architectures
    - Check thermal throttling after 5 min
    
    iOS BUILD:
    - Check code signing for frameworks
    - Test on older devices (iPhone 11)
    - Verify static library linking
    - App Store compliance (no JIT)
    
    WEBGL BUILD:
    - Confirm cloud API fallback works
    - Check CORS settings for API calls
    - Verify memory limits aren't exceeded
    */
    
    public class BuildVerifier : MonoBehaviour
    {
        void Start()
        {
            #if UNITY_EDITOR
            Debug.LogWarning("Running in editor - build test required!");
            #else
            Debug.Log($"Platform: {Application.platform}");
            Debug.Log($"Memory: {SystemInfo.systemMemorySize}MB");
            StartCoroutine(VerifyLLMFunctionality());
            #endif
        }
    
        IEnumerator VerifyLLMFunctionality()
        {
            var llm = FindObjectOfType<LLM>();
            if (llm == null)
            {
                Debug.LogError("No LLM component found!");
                yield break;
            }
    
            Debug.Log("Testing LLM response...");
            var startTime = Time.time;
    
            // Simple test prompt
            var character = FindObjectOfType<LLMCharacter>();
            string response = null;
    
            yield return character.Chat("Hello", (r) => response = r);
    
            var elapsed = Time.time - startTime;
            Debug.Log($"Response received in {elapsed:F2}s: {response}");
    
            if (string.IsNullOrEmpty(response))
            {
                Debug.LogError("LLM returned empty response!");
            }
            else
            {
                Debug.Log("LLM verification PASSED");
            }
        }
    }
    

## Anti-Patterns


---
  #### **Name**
Synchronous Chat Calls
  #### **Description**
Calling LLM.Chat() without async/await or coroutines
  #### **Why**
Blocks main thread, freezes game, drops frames. Even 50ms is 3 dropped frames at 60 FPS.
  #### **Instead**
Always use async/await, coroutines, or callbacks for LLM calls.

---
  #### **Name**
Editor-Only Testing
  #### **Description**
Only testing LLM features in Unity Editor, never in builds
  #### **Why**
LLMUnity uses native libraries that behave differently per platform. iOS signing, Android architectures, and WebGL limitations only appear in builds.
  #### **Instead**
Build and test on each target platform early and often.

---
  #### **Name**
One Model For All Platforms
  #### **Description**
Using the same large model (7B+) for both desktop and mobile
  #### **Why**
Mobile devices have 2-4GB RAM. A 7B Q4 model needs 4-5GB. App will crash or be killed by OS.
  #### **Instead**
Use tiered models—8B for desktop, 1-3B for mobile, cloud API for WebGL.

---
  #### **Name**
Loading Models in Start()
  #### **Description**
Loading large models during scene initialization
  #### **Why**
Model loading takes 2-10 seconds. Doing this in Start() freezes the game without feedback.
  #### **Instead**
Load during loading screen with progress UI, or lazy-load on first dialogue.

---
  #### **Name**
Ignoring Memory Cleanup
  #### **Description**
Not unloading models when switching scenes or NPCs
  #### **Why**
Models consume significant memory. Without cleanup, you'll hit memory limits on mobile.
  #### **Instead**
Explicitly unload models when done, call GC.Collect() and Resources.UnloadUnusedAssets().

---
  #### **Name**
Hardcoded Model Paths
  #### **Description**
Using absolute paths or Assets/ paths for models
  #### **Why**
Only StreamingAssets survives builds. Other paths don't exist in player builds.
  #### **Instead**
Always place models in StreamingAssets and use Application.streamingAssetsPath.