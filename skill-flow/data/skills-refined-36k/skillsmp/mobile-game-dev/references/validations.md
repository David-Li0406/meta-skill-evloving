# Mobile Game Dev - Validations

## Uncapped Frame Rate on Mobile

### **Id**
mobile-uncapped-framerate
### **Severity**
error
### **Type**
regex
### **Pattern**
Application\.targetFrameRate\s*=\s*-1
### **Message**
Uncapped frame rate (-1) on mobile causes battery drain and thermal throttling. Set explicit cap (30/60).
### **Fix Action**
  Set appropriate frame rate:
  Application.targetFrameRate = 60; // or 30 for battery saver
  
### **Applies To**
  - *.cs
  - *.gd

## Synchronous Loading in Update

### **Id**
mobile-sync-loading-update
### **Severity**
error
### **Type**
regex
### **Pattern**
void\s+(Update|FixedUpdate|LateUpdate)\s*\([^)]*\)[^}]*(Resources\.Load|Addressables\.LoadAsset(?!Async))
### **Message**
Synchronous loading in Update blocks main thread - causes ANR on Android.
### **Fix Action**
  Use async loading:
  var handle = Addressables.LoadAssetAsync<GameObject>(key);
  await handle;
  
### **Applies To**
  - *.cs

## Thread.Sleep on Main Thread

### **Id**
mobile-thread-sleep-main
### **Severity**
error
### **Type**
regex
### **Pattern**
Thread\.Sleep\s*\(\s*\d+
### **Message**
Thread.Sleep blocks main thread - causes ANR on Android (5s limit).
### **Fix Action**
  Use async/await or coroutines:
  await Task.Delay(milliseconds);
  // or
  yield return new WaitForSeconds(seconds);
  
### **Applies To**
  - *.cs

## GC.Collect in Hot Path

### **Id**
mobile-gc-in-update
### **Severity**
error
### **Type**
regex
### **Pattern**
void\s+(Update|FixedUpdate|LateUpdate)\s*\([^)]*\)[^}]*GC\.Collect
### **Message**
GC.Collect in Update causes frame spikes. Only call during loading screens.
### **Fix Action**
Move GC.Collect to loading screens or scene transitions only
### **Applies To**
  - *.cs

## Deprecated WWW Class

### **Id**
mobile-www-deprecated
### **Severity**
error
### **Type**
regex
### **Pattern**
new\s+WWW\s*\(
### **Message**
WWW class is deprecated and blocks main thread. Use UnityWebRequest.
### **Fix Action**
  Replace with async UnityWebRequest:
  using (var request = UnityWebRequest.Get(url))
  {
      await request.SendWebRequest();
  }
  
### **Applies To**
  - *.cs

## Texture Creation in Update

### **Id**
mobile-texture-create-update
### **Severity**
error
### **Type**
regex
### **Pattern**
void\s+Update\s*\([^)]*\)[^}]*new\s+Texture2D\s*\(
### **Message**
Creating Texture2D in Update causes memory growth and GC spikes.
### **Fix Action**
Create textures once and reuse. Pool textures if needed.
### **Applies To**
  - *.cs

## Allocating Raycast in Hot Path

### **Id**
mobile-raycast-allocating
### **Severity**
warning
### **Type**
regex
### **Pattern**
void\s+(Update|FixedUpdate)\s*\([^)]*\)[^}]*Physics\.RaycastAll\s*\(
### **Message**
RaycastAll allocates array every call. Use RaycastNonAlloc with buffer.
### **Fix Action**
  Use non-allocating version:
  private RaycastHit[] _hits = new RaycastHit[10];
  int count = Physics.RaycastNonAlloc(ray, _hits);
  
### **Applies To**
  - *.cs

## Allocating Physics Overlap

### **Id**
mobile-overlap-allocating
### **Severity**
warning
### **Type**
regex
### **Pattern**
void\s+(Update|FixedUpdate)\s*\([^)]*\)[^}]*Physics\.(OverlapSphere|OverlapBox|OverlapCapsule)\s*\([^)]+\)
### **Message**
Overlap methods allocate arrays. Use NonAlloc variants.
### **Fix Action**
  private Collider[] _results = new Collider[20];
  int count = Physics.OverlapSphereNonAlloc(pos, radius, _results);
  
### **Applies To**
  - *.cs

## LINQ Allocation in Update

### **Id**
mobile-linq-in-update
### **Severity**
warning
### **Type**
regex
### **Pattern**
void\s+(Update|FixedUpdate)\s*\([^)]*\)[^}]*\.(Where|Select|OrderBy|FirstOrDefault|ToList|ToArray|Any\(\)|Count\(\))
### **Message**
LINQ methods allocate on every call. Use loops for hot paths.
### **Fix Action**
Replace LINQ with for/foreach loops in Update methods
### **Applies To**
  - *.cs

## String Formatting in Update

### **Id**
mobile-string-format-update
### **Severity**
warning
### **Type**
regex
### **Pattern**
void\s+Update\s*\([^)]*\)[^}]*(string\.Format|String\.Format|\$"|\+\s*\w+\.ToString\(\))
### **Message**
String operations in Update cause GC allocations. Cache or use StringBuilder.
### **Fix Action**
  Cache strings or use StringBuilder:
  private StringBuilder _sb = new StringBuilder();
  _sb.Clear().Append("Score: ").Append(score);
  
### **Applies To**
  - *.cs

## Debug.Log Without Conditional

### **Id**
mobile-debug-log-release
### **Severity**
warning
### **Type**
regex
### **Pattern**
Debug\.(Log|LogWarning|LogError)\s*\([^)]+\)
### **Message**
Debug.Log in release builds impacts performance. Use conditional compilation.
### **Fix Action**
  Wrap with conditional:
  #if UNITY_EDITOR || DEVELOPMENT_BUILD
  Debug.Log(message);
  #endif
  
### **Applies To**
  - *.cs

## Camera.main in Update

### **Id**
mobile-camera-main-update
### **Severity**
warning
### **Type**
regex
### **Pattern**
void\s+(Update|FixedUpdate|LateUpdate)\s*\([^)]*\)[^}]*Camera\.main
### **Message**
Camera.main searches by tag every call. Cache the reference.
### **Fix Action**
  Cache in Start:
  private Camera _mainCamera;
  void Start() => _mainCamera = Camera.main;
  
### **Applies To**
  - *.cs

## Mouse Input Instead of Touch

### **Id**
mobile-mouse-input
### **Severity**
warning
### **Type**
regex
### **Pattern**
Input\.(GetMouseButton|GetMouseButtonDown|GetMouseButtonUp|mousePosition)
### **Message**
Mouse input on mobile. Use Input.GetTouch or Input.touches for proper touch handling.
### **Fix Action**
  Use touch input for mobile:
  if (Input.touchCount > 0)
  {
      Touch touch = Input.GetTouch(0);
      // handle touch.phase, touch.position
  }
  
### **Applies To**
  - *.cs

## OnApplicationPause Without Save

### **Id**
mobile-no-pause-save
### **Severity**
warning
### **Type**
regex
### **Pattern**
void\s+OnApplicationPause\s*\([^)]*\)[^}]{0,200}$
### **Message**
OnApplicationPause without apparent save logic. State may be lost if OS kills app.
### **Fix Action**
  Save state when pausing:
  void OnApplicationPause(bool pauseStatus)
  {
      if (pauseStatus)
      {
          SaveManager.Instance.QuickSave();
      }
  }
  
### **Applies To**
  - *.cs

## PlayerPrefs Without Explicit Save

### **Id**
mobile-playerprefs-no-save
### **Severity**
warning
### **Type**
regex
### **Pattern**
PlayerPrefs\.(SetString|SetInt|SetFloat)\s*\([^)]+\)(?!.*PlayerPrefs\.Save)
### **Message**
PlayerPrefs changes may not persist on mobile without explicit Save().
### **Fix Action**
  Call Save after writing:
  PlayerPrefs.SetInt("HighScore", score);
  PlayerPrefs.Save(); // Required for mobile
  
### **Applies To**
  - *.cs

## High Quality Preset on Mobile

### **Id**
mobile-high-quality-preset
### **Severity**
info
### **Type**
regex
### **Pattern**
QualitySettings\.SetQualityLevel\s*\(\s*[3-6]\s*[,)]
### **Message**
High quality presets (3+) may cause thermal throttling on mobile.
### **Fix Action**
Consider using quality level 0-2 for mobile, with adaptive quality system
### **Applies To**
  - *.cs

## GPS Location Without Management

### **Id**
mobile-location-start
### **Severity**
warning
### **Type**
regex
### **Pattern**
Input\.location\.Start\s*\([^)]*\)(?![^}]*Input\.location\.Stop)
### **Message**
GPS location started without apparent stop. Location drains battery.
### **Fix Action**
  Stop location when not needed:
  Input.location.Start();
  // ... use location ...
  Input.location.Stop();
  
### **Applies To**
  - *.cs

## Gyroscope Without Disable

### **Id**
mobile-gyroscope-enabled
### **Severity**
info
### **Type**
regex
### **Pattern**
Input\.gyro\.enabled\s*=\s*true(?![^}]*Input\.gyro\.enabled\s*=\s*false)
### **Message**
Gyroscope enabled without apparent disable. Sensors drain battery.
### **Fix Action**
Disable gyroscope when not actively using it
### **Applies To**
  - *.cs

## Accelerometer in Every Frame

### **Id**
mobile-accelerometer-update
### **Severity**
info
### **Type**
regex
### **Pattern**
void\s+Update\s*\([^)]*\)[^}]*Input\.acceleration
### **Message**
Reading accelerometer every frame. Consider reducing poll rate.
### **Fix Action**
  Throttle accelerometer reads:
  if (Time.frameCount % 3 == 0)  // Every 3rd frame
  {
      var acceleration = Input.acceleration;
  }
  
### **Applies To**
  - *.cs

## VSync Without Mobile Consideration

### **Id**
mobile-no-vsync-control
### **Severity**
info
### **Type**
regex
### **Pattern**
QualitySettings\.vSyncCount\s*=\s*1
### **Message**
VSync adds latency. Consider vSyncCount=0 with targetFrameRate on mobile.
### **Fix Action**
  For mobile, disable VSync and use frame rate cap:
  QualitySettings.vSyncCount = 0;
  Application.targetFrameRate = 60;
  
### **Applies To**
  - *.cs

## Potential Small Touch Target

### **Id**
mobile-touch-small-targets
### **Severity**
info
### **Type**
regex
### **Pattern**
RectTransform.*sizeDelta\s*=\s*new\s+Vector2\s*\(\s*\d{1,2}\s*,\s*\d{1,2}\s*\)
### **Message**
Small UI element size. Minimum touch target should be 44x44 points.
### **Fix Action**
Ensure touch targets are at least 44x44 points for comfortable tapping
### **Applies To**
  - *.cs

## Hover State in Mobile UI

### **Id**
mobile-hover-state
### **Severity**
info
### **Type**
regex
### **Pattern**
(OnPointerEnter|OnMouseEnter|IPointerEnterHandler)
### **Message**
Hover state detected. Mobile has no hover - use press/release states instead.
### **Fix Action**
Replace hover with pointer down/up states for mobile
### **Applies To**
  - *.cs

## Realtime Reflection Probes

### **Id**
mobile-realtime-reflection
### **Severity**
warning
### **Type**
regex
### **Pattern**
ReflectionProbeMode\s*\.\s*Realtime
### **Message**
Realtime reflection probes are expensive on mobile. Use baked probes.
### **Fix Action**
Use ReflectionProbeMode.Baked for mobile
### **Applies To**
  - *.cs

## Realtime Shadows Configuration

### **Id**
mobile-realtime-shadows
### **Severity**
info
### **Type**
regex
### **Pattern**
shadowType\s*=\s*LightShadows\.Hard|shadowType\s*=\s*LightShadows\.Soft
### **Message**
Realtime shadows are expensive on mobile. Consider baked shadows or no shadows.
### **Fix Action**
Use baked shadows or disable for low-tier devices
### **Applies To**
  - *.cs

## High Texture Without Compression

### **Id**
mobile-high-texture-resolution
### **Severity**
info
### **Type**
regex
### **Pattern**
new\s+Texture2D\s*\(\s*\d{4,}\s*,\s*\d{4,}
### **Message**
Large texture creation (4K+). Ensure ASTC/ETC2 compression for mobile.
### **Fix Action**
  Use compressed formats:
  // In import settings: Format = ASTC (iOS) or ETC2 (Android)
  // Or use smaller textures with mipmaps
  
### **Applies To**
  - *.cs

## Audio Without Focus Handling

### **Id**
mobile-no-focus-handler
### **Severity**
warning
### **Type**
regex
### **Pattern**
AudioSource\.Play\s*\([^)]*\)
### **Message**
AudioSource.Play without OnApplicationFocus handling may cause audio issues during interruptions.
### **Fix Action**
  Handle audio focus:
  void OnApplicationFocus(bool hasFocus)
  {
      AudioListener.pause = !hasFocus;
  }
  
### **Applies To**
  - *.cs

## Infinite Coroutine Without Yield

### **Id**
mobile-infinite-coroutine
### **Severity**
warning
### **Type**
regex
### **Pattern**
while\s*\(\s*true\s*\)\s*\{[^}]*yield\s+return\s+null
### **Message**
Infinite coroutine with yield return null runs every frame. Consider throttling.
### **Fix Action**
  Throttle infinite coroutines:
  while (true)
  {
      DoWork();
      yield return new WaitForSeconds(0.1f);  // Not every frame
  }
  
### **Applies To**
  - *.cs

## Synchronous Web Request

### **Id**
mobile-sync-web-request
### **Severity**
error
### **Type**
regex
### **Pattern**
(WebClient|HttpWebRequest).*Get(String|Stream)\s*\(
### **Message**
Synchronous web requests block main thread - causes ANR. Use async.
### **Fix Action**
  Use UnityWebRequest with async:
  using (var request = UnityWebRequest.Get(url))
  {
      var operation = request.SendWebRequest();
      while (!operation.isDone)
      {
          yield return null;
      }
  }
  
### **Applies To**
  - *.cs

## Large JSON Parse on Main Thread

### **Id**
mobile-large-json-parse
### **Severity**
warning
### **Type**
regex
### **Pattern**
JsonUtility\.FromJson|JsonConvert\.Deserialize
### **Message**
JSON parsing on main thread may cause frame drops for large payloads.
### **Fix Action**
  Move large JSON parsing off main thread:
  await Task.Run(() => JsonUtility.FromJson<T>(json));
  
### **Applies To**
  - *.cs

## Godot Physics in _process

### **Id**
mobile-godot-process-physics
### **Severity**
error
### **Type**
regex
### **Pattern**
func\s+_process\s*\([^)]*\)[^}]*(move_and_slide|velocity|apply_force)
### **Message**
Physics in _process causes inconsistent behavior. Use _physics_process.
### **Fix Action**
Move physics code to _physics_process for fixed timestep
### **Applies To**
  - *.gd

## Godot get_node in Process

### **Id**
mobile-godot-get-node-process
### **Severity**
warning
### **Type**
regex
### **Pattern**
func\s+_process\s*\([^)]*\)[^}]*(get_node\(|\$)
### **Message**
get_node in _process is expensive. Cache with @onready.
### **Fix Action**
  Cache references:
  @onready var player = $"../Player"
  
### **Applies To**
  - *.gd

## Godot load in Process

### **Id**
mobile-godot-load-process
### **Severity**
error
### **Type**
regex
### **Pattern**
func\s+_process\s*\([^)]*\)[^}]*load\s*\(
### **Message**
load() in _process blocks. Use preload() or ResourceLoader.load_threaded.
### **Fix Action**
Use preload for constants or async loading
### **Applies To**
  - *.gd