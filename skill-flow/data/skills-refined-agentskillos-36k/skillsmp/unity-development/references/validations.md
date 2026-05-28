# Unity Development - Validations

## GetComponent in Update Loop

### **Id**
unity-getcomponent-in-update
### **Severity**
error
### **Type**
regex
### **Pattern**
void\s+(Update|FixedUpdate|LateUpdate)\s*\([^)]*\)[^}]*GetComponent\s*<
### **Message**
GetComponent called in Update loop. Cache the component reference in Awake or Start.
### **Fix Action**
  Cache in Awake:
  private ComponentType _cached;
  void Awake() => _cached = GetComponent<ComponentType>();
  
### **Applies To**
  - *.cs

## GetComponent (non-generic) in Update

### **Id**
unity-getcomponent-in-update-nongeneric
### **Severity**
error
### **Type**
regex
### **Pattern**
void\s+(Update|FixedUpdate|LateUpdate)\s*\([^)]*\)[^}]*GetComponent\s*\(\s*typeof
### **Message**
GetComponent(typeof()) called in Update. Cache the reference.
### **Fix Action**
Cache in Awake using the generic version: GetComponent<T>()
### **Applies To**
  - *.cs

## Find Methods at Runtime

### **Id**
unity-find-at-runtime
### **Severity**
error
### **Type**
regex
### **Pattern**
void\s+(Update|FixedUpdate|Start|OnEnable)\s*\([^)]*\)[^}]*(GameObject\.Find|FindObjectOfType|FindObjectsOfType|FindGameObjectsWithTag)
### **Message**
Find methods are expensive. Use SerializeField references or event-based architecture.
### **Fix Action**
  Replace with:
  [SerializeField] private TargetType _target;
  Or use a ScriptableObject registry pattern.
  
### **Applies To**
  - *.cs

## Find Methods Usage (Warning)

### **Id**
unity-find-any-usage
### **Severity**
warning
### **Type**
regex
### **Pattern**
(GameObject\.Find\s*\(|FindObjectOfType\s*<|FindObjectsOfType\s*<|FindGameObjectsWithTag\s*\()
### **Message**
Find methods should be avoided. Consider using direct references or registries.
### **Fix Action**
Use [SerializeField] references or ScriptableObject registries
### **Applies To**
  - *.cs

## Physics Operations in Update

### **Id**
unity-physics-in-update
### **Severity**
error
### **Type**
regex
### **Pattern**
void\s+Update\s*\([^)]*\)[^}]*(\.AddForce|\.AddTorque|\.velocity\s*=|\.angularVelocity\s*=|\.MovePosition|\.MoveRotation)
### **Message**
Physics operations should be in FixedUpdate, not Update.
### **Fix Action**
Move physics code to FixedUpdate()
### **Applies To**
  - *.cs

## Instantiate/Destroy Pattern

### **Id**
unity-instantiate-destroy-loop
### **Severity**
error
### **Type**
regex
### **Pattern**
Instantiate\s*\([^)]+\)[^}]{0,500}Destroy\s*\([^)]+\)
### **Message**
Instantiate/Destroy pattern detected. Use object pooling for frequently spawned objects.
### **Fix Action**
Implement an object pool - reuse objects instead of creating/destroying
### **Applies To**
  - *.cs

## Object Allocation in Update

### **Id**
unity-new-in-update
### **Severity**
warning
### **Type**
regex
### **Pattern**
void\s+(Update|FixedUpdate|LateUpdate)\s*\([^)]*\)[^}]*new\s+(Vector3|Vector2|Quaternion|List|Dictionary|HashSet|StringBuilder)\s*\(
### **Message**
Creating new objects in Update causes GC pressure. Reuse or cache.
### **Fix Action**
  Cache and reuse:
  private Vector3 _cachedVector;
  void Update() { _cachedVector.Set(x, y, z); }
  
### **Applies To**
  - *.cs

## String Concatenation in Update

### **Id**
unity-string-concat-update
### **Severity**
warning
### **Type**
regex
### **Pattern**
void\s+(Update|FixedUpdate|LateUpdate)\s*\([^)]*\)[^}]*(\+\s*"|\+\s*\w+\.ToString\(\))
### **Message**
String concatenation in Update allocates memory. Use StringBuilder or cache.
### **Fix Action**
Use StringBuilder or string interpolation outside hot paths
### **Applies To**
  - *.cs

## Animator String Parameter in Update

### **Id**
unity-animator-string-update
### **Severity**
warning
### **Type**
regex
### **Pattern**
void\s+Update\s*\([^)]*\)[^}]*_?[aA]nimator\s*\.\s*(SetFloat|SetBool|SetInteger|SetTrigger)\s*\(\s*"
### **Message**
String-based Animator parameter in Update. Cache hash with Animator.StringToHash.
### **Fix Action**
  Cache the hash:
  private static readonly int SpeedHash = Animator.StringToHash("Speed");
  void Update() { animator.SetFloat(SpeedHash, speed); }
  
### **Applies To**
  - *.cs

## SendMessage Usage

### **Id**
unity-sendmessage
### **Severity**
warning
### **Type**
regex
### **Pattern**
\.(SendMessage|BroadcastMessage|SendMessageUpwards)\s*\(
### **Message**
SendMessage is slow and error-prone. Use direct calls, interfaces, or events.
### **Fix Action**
Use interfaces, UnityEvents, or direct method calls
### **Applies To**
  - *.cs

## Tag Comparison with String

### **Id**
unity-tag-compare-string
### **Severity**
warning
### **Type**
regex
### **Pattern**
\.tag\s*==\s*"
### **Message**
String comparison for tags. Use CompareTag() for better performance.
### **Fix Action**
Replace with: gameObject.CompareTag("TagName")
### **Applies To**
  - *.cs

## StartCoroutine Without Stop

### **Id**
unity-coroutine-no-stop
### **Severity**
warning
### **Type**
regex
### **Pattern**
StartCoroutine\s*\([^)]+\)(?![^}]*(StopCoroutine|StopAllCoroutines))
### **Message**
Coroutine started without stop logic. May cause memory leaks.
### **Fix Action**
  Track and stop coroutines:
  private Coroutine _routine;
  void OnEnable() { _routine = StartCoroutine(MyRoutine()); }
  void OnDisable() { if (_routine != null) StopCoroutine(_routine); }
  
### **Applies To**
  - *.cs

## Async Void Method

### **Id**
unity-async-void
### **Severity**
warning
### **Type**
regex
### **Pattern**
async\s+void\s+\w+\s*\(
### **Message**
async void cannot be cancelled or awaited. Use async UniTaskVoid or async Task.
### **Fix Action**
Use UniTask: async UniTaskVoid MethodName() with CancellationToken
### **Applies To**
  - *.cs

## GetComponent Without RequireComponent

### **Id**
unity-missing-requirecomponent
### **Severity**
info
### **Type**
regex
### **Pattern**
GetComponent<(Rigidbody|Rigidbody2D|Collider|Collider2D|Animator|AudioSource)>\s*\(\s*\)(?![^}]*\[RequireComponent)
### **Message**
GetComponent for common component without RequireComponent attribute.
### **Fix Action**
Add [RequireComponent(typeof(ComponentType))] to the class
### **Applies To**
  - *.cs

## DestroyImmediate Usage

### **Id**
unity-destroy-immediate
### **Severity**
warning
### **Type**
regex
### **Pattern**
DestroyImmediate\s*\(
### **Message**
DestroyImmediate should only be used in editor scripts. Use Destroy() in runtime.
### **Fix Action**
Replace with Destroy() for runtime, keep DestroyImmediate only in Editor scripts
### **Applies To**
  - *.cs

## Camera.main in Update

### **Id**
unity-camera-main
### **Severity**
warning
### **Type**
regex
### **Pattern**
void\s+Update\s*\([^)]*\)[^}]*Camera\.main
### **Message**
Camera.main does a FindWithTag internally. Cache the reference.
### **Fix Action**
  Cache in Awake:
  private Camera _mainCamera;
  void Awake() => _mainCamera = Camera.main;
  
### **Applies To**
  - *.cs

## Potentially Incorrect Null Check

### **Id**
unity-null-check-pattern
### **Severity**
info
### **Type**
regex
### **Pattern**
if\s*\(\s*\w+\s*!=\s*null\s*\)[^}]*\.(transform|gameObject|GetComponent)
### **Message**
Unity objects may pass C# null check but still be destroyed. Use Unity's bool operator.
### **Fix Action**
Use: if (obj) { } instead of if (obj != null) { }
### **Applies To**
  - *.cs

## Resources.Load in Update

### **Id**
unity-resources-load-update
### **Severity**
error
### **Type**
regex
### **Pattern**
void\s+Update\s*\([^)]*\)[^}]*Resources\.Load
### **Message**
Resources.Load in Update is extremely expensive. Load and cache in Awake/Start.
### **Fix Action**
Load in Awake/Start and cache the reference
### **Applies To**
  - *.cs

## Addressables Load Without Release

### **Id**
unity-addressables-no-release
### **Severity**
warning
### **Type**
regex
### **Pattern**
Addressables\.LoadAssetAsync(?![^}]*Addressables\.Release)
### **Message**
Addressables load without apparent release. Remember to release handles.
### **Fix Action**
  Track and release:
  private AsyncOperationHandle _handle;
  void OnDestroy() { if (_handle.IsValid()) Addressables.Release(_handle); }
  
### **Applies To**
  - *.cs

## GetComponents (plural) in Update

### **Id**
unity-getcomponents-update
### **Severity**
error
### **Type**
regex
### **Pattern**
void\s+(Update|FixedUpdate)\s*\([^)]*\)[^}]*GetComponents\s*[<\(]
### **Message**
GetComponents allocates a new array every call. Use GetComponentsNonAlloc.
### **Fix Action**
  Use non-allocating version:
  private ComponentType[] _buffer = new ComponentType[10];
  void Update() { int count = GetComponents(_buffer); }
  
### **Applies To**
  - *.cs

## Allocating Raycast in Update

### **Id**
unity-raycast-allocating
### **Severity**
warning
### **Type**
regex
### **Pattern**
void\s+Update\s*\([^)]*\)[^}]*Physics\.RaycastAll\s*\(
### **Message**
RaycastAll allocates. Use RaycastNonAlloc with pre-allocated buffer.
### **Fix Action**
  Use non-allocating version:
  private RaycastHit[] _hits = new RaycastHit[10];
  void Update() { int count = Physics.RaycastNonAlloc(ray, _hits); }
  
### **Applies To**
  - *.cs

## Allocating Overlap in Update

### **Id**
unity-overlap-allocating
### **Severity**
warning
### **Type**
regex
### **Pattern**
void\s+Update\s*\([^)]*\)[^}]*Physics\.(OverlapSphere|OverlapBox|OverlapCapsule)\s*\([^)]*\)
### **Message**
Overlap methods allocate. Use OverlapNonAlloc variants.
### **Fix Action**
  Use non-allocating version:
  private Collider[] _colliders = new Collider[10];
  void Update() { int count = Physics.OverlapSphereNonAlloc(pos, radius, _colliders); }
  
### **Applies To**
  - *.cs

## Magic Numbers in Game Logic

### **Id**
unity-magic-numbers
### **Severity**
info
### **Type**
regex
### **Pattern**
(speed|velocity|force|damage|health|gravity)\s*[+\-*/]=?\s*\d+\.\d+
### **Message**
Consider using SerializeField or ScriptableObject for game constants.
### **Fix Action**
  Use configurable values:
  [SerializeField] private float _speed = 5f;
  Or use ScriptableObject for shared configuration.
  
### **Applies To**
  - *.cs

## Public Field Without SerializeField

### **Id**
unity-public-field
### **Severity**
info
### **Type**
regex
### **Pattern**
public\s+(int|float|string|bool|Vector[23]|Transform|GameObject)\s+\w+\s*;
### **Message**
Public fields are serialized by default. Consider [SerializeField] private for encapsulation.
### **Fix Action**
Use: [SerializeField] private TypeName _fieldName;
### **Applies To**
  - *.cs

## Hardcoded Layer Number

### **Id**
unity-hardcoded-layer
### **Severity**
info
### **Type**
regex
### **Pattern**
LayerMask\s*\.\s*GetMask\s*\(\s*\d+|1\s*<<\s*\d+
### **Message**
Hardcoded layer numbers are fragile. Use LayerMask.GetMask with names.
### **Fix Action**
Use: LayerMask.GetMask("LayerName") or [SerializeField] LayerMask
### **Applies To**
  - *.cs

## GetComponent Without Null Check in Awake

### **Id**
unity-awake-getcomponent-null
### **Severity**
info
### **Type**
regex
### **Pattern**
void\s+Awake\s*\(\s*\)[^}]*=\s*GetComponent\s*<[^>]+>\s*\(\s*\)\s*;(?![^}]*!=\s*null|[^}]*==\s*null)
### **Message**
GetComponent in Awake without null check. Component might not exist.
### **Fix Action**
  Add null check or use TryGetComponent:
  if (!TryGetComponent<ComponentType>(out _cached))
  {
      Debug.LogError("Missing required component", this);
  }
  
### **Applies To**
  - *.cs

## LINQ in Update Loop

### **Id**
unity-linq-in-update
### **Severity**
warning
### **Type**
regex
### **Pattern**
void\s+(Update|FixedUpdate)\s*\([^)]*\)[^}]*\.(Where|Select|OrderBy|FirstOrDefault|ToList|ToArray|Count\(\))
### **Message**
LINQ methods allocate. Use loops or cache results.
### **Fix Action**
Replace LINQ with for loops in hot paths
### **Applies To**
  - *.cs

## Debug.Log Without Conditional

### **Id**
unity-debug-log-build
### **Severity**
info
### **Type**
regex
### **Pattern**
Debug\.(Log|LogWarning|LogError)\s*\([^)]+\)
### **Message**
Debug.Log calls remain in builds. Consider using [Conditional] or removing for release.
### **Fix Action**
  Wrap with conditional:
  [Conditional("UNITY_EDITOR")]
  void Log(string msg) => Debug.Log(msg);
  
### **Applies To**
  - *.cs

## String-Based Invoke

### **Id**
unity-invoke-string
### **Severity**
warning
### **Type**
regex
### **Pattern**
\.(Invoke|InvokeRepeating|CancelInvoke)\s*\(\s*"
### **Message**
String-based Invoke is slow and error-prone. Use coroutines or async.
### **Fix Action**
Replace with coroutines or async/await patterns
### **Applies To**
  - *.cs

## Foreach on Collection in Update

### **Id**
unity-foreach-update
### **Severity**
info
### **Type**
regex
### **Pattern**
void\s+Update\s*\([^)]*\)[^}]*foreach\s*\([^)]*\s+in\s+\w+\)
### **Message**
foreach may allocate enumerator. Consider using for loop in hot paths.
### **Fix Action**
Use for loop: for (int i = 0; i < list.Count; i++)
### **Applies To**
  - *.cs