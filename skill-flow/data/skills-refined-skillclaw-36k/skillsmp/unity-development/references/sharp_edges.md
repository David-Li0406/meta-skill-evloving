# Unity Development - Sharp Edges

## Update Vs Fixedupdate

### **Id**
update-vs-fixedupdate
### **Summary**
Using Update for physics or FixedUpdate for input
### **Severity**
critical
### **Situation**
Applying forces in Update, checking input in FixedUpdate
### **Why**
  Update runs every frame (variable rate). FixedUpdate runs at fixed intervals (default 50/sec).
  Physics in Update = inconsistent behavior based on frame rate. Fast machines move faster.
  Input in FixedUpdate = missed inputs because it runs less frequently than frames.
  
### **Solution**
  // WRONG: Physics in Update
  void Update()
  {
      _rb.AddForce(Vector3.forward * force);  // Inconsistent at different frame rates!
      _rb.velocity = newVelocity;  // Frame-rate dependent
  }
  
  // WRONG: Input in FixedUpdate
  void FixedUpdate()
  {
      if (Input.GetKeyDown(KeyCode.Space))  // Might miss key presses!
      {
          Jump();
      }
  }
  
  // RIGHT: Separate concerns
  void Update()
  {
      // Input and game logic
      if (Input.GetKeyDown(KeyCode.Space))
      {
          _jumpRequested = true;
      }
  }
  
  void FixedUpdate()
  {
      // Physics only
      if (_jumpRequested)
      {
          _rb.AddForce(Vector3.up * jumpForce, ForceMode.Impulse);
          _jumpRequested = false;
      }
  
      _rb.AddForce(moveDirection * moveForce);
  }
  
### **Symptoms**
  - Movement feels different on different machines
  - Physics seems "floaty" or inconsistent
  - Input sometimes doesn't register
  - Jump height varies with frame rate
### **Detection Pattern**
void Update\(\)[^}]*AddForce|void Update\(\)[^}]*\.velocity\s*=

## Coroutine Memory Leak

### **Id**
coroutine-memory-leak
### **Summary**
Starting coroutines without proper cleanup
### **Severity**
critical
### **Situation**
Coroutines keep running after object is disabled or destroyed
### **Why**
  Coroutines are NOT stopped when MonoBehaviour is disabled (only when destroyed).
  They hold references to captured variables. They can cause null reference exceptions
  when accessing destroyed objects. Memory accumulates over time.
  
### **Solution**
  // WRONG: Fire and forget coroutines
  public class BadCoroutine : MonoBehaviour
  {
      void Start()
      {
          StartCoroutine(DoSomethingForever());
      }
  
      IEnumerator DoSomethingForever()
      {
          while (true)
          {
              // This keeps running even when disabled!
              DoThing();
              yield return new WaitForSeconds(1f);
          }
      }
  }
  
  // RIGHT: Track and stop coroutines
  public class GoodCoroutine : MonoBehaviour
  {
      private Coroutine _runningCoroutine;
      private bool _isRunning;
  
      void OnEnable()
      {
          _isRunning = true;
          _runningCoroutine = StartCoroutine(DoSomethingWhileEnabled());
      }
  
      void OnDisable()
      {
          _isRunning = false;
          if (_runningCoroutine != null)
          {
              StopCoroutine(_runningCoroutine);
              _runningCoroutine = null;
          }
      }
  
      IEnumerator DoSomethingWhileEnabled()
      {
          while (_isRunning)
          {
              DoThing();
              yield return new WaitForSeconds(1f);
          }
      }
  }
  
  // BETTER: Use async/await with CancellationToken
  public class AsyncPattern : MonoBehaviour
  {
      private CancellationTokenSource _cts;
  
      void OnEnable() => _cts = new CancellationTokenSource();
  
      void OnDisable()
      {
          _cts?.Cancel();
          _cts?.Dispose();
      }
  
      async void Start()
      {
          try
          {
              await DoThingAsync(_cts.Token);
          }
          catch (OperationCanceledException) { }
      }
  }
  
### **Symptoms**
  - Memory grows over time
  - NullReferenceException in coroutines after scene change
  - Coroutines "keep going" after disabling object
  - Events fire on destroyed objects
### **Detection Pattern**
StartCoroutine\([^)]+\)(?![^}]*StopCoroutine)

## Getcomponent In Update

### **Id**
getcomponent-in-update
### **Summary**
Calling GetComponent every frame instead of caching
### **Severity**
critical
### **Situation**
GetComponent, GetComponentInChildren, or GetComponents in Update loop
### **Why**
  GetComponent searches the component list every call. It's not free.
  60+ calls per second per object adds up fast. This is one of the most common
  Unity performance problems and completely unnecessary.
  
### **Solution**
  // WRONG: GetComponent every frame
  void Update()
  {
      GetComponent<Rigidbody>().velocity = direction;  // Searches every frame!
      GetComponent<Animator>().SetFloat("Speed", speed);
      GetComponentInChildren<Renderer>().material.color = color;
  }
  
  // RIGHT: Cache once, use forever
  private Rigidbody _rb;
  private Animator _animator;
  private Renderer _renderer;
  
  void Awake()
  {
      _rb = GetComponent<Rigidbody>();
      _animator = GetComponent<Animator>();
      _renderer = GetComponentInChildren<Renderer>();
  }
  
  void Update()
  {
      _rb.velocity = direction;
      _animator.SetFloat("Speed", speed);
      _renderer.material.color = color;
  }
  
  // EVEN BETTER: SerializeField + RequireComponent
  [RequireComponent(typeof(Rigidbody))]
  public class Player : MonoBehaviour
  {
      [SerializeField] private Rigidbody _rb;
  
      void Reset()  // Called in editor when adding component
      {
          _rb = GetComponent<Rigidbody>();
      }
  }
  
### **Symptoms**
  - Frame rate drops with many objects
  - Profiler shows GetComponent taking time
  - Performance degrades as scene grows
  - CPU spikes in Update
### **Detection Pattern**
void (Update|FixedUpdate|LateUpdate)\s*\([^)]*\)[^}]*GetComponent

## Instantiate Destroy Spam

### **Id**
instantiate-destroy-spam
### **Summary**
Creating and destroying objects frequently without pooling
### **Severity**
critical
### **Situation**
Bullets, particles, enemies, or other objects spawned frequently
### **Why**
  Instantiate clones prefab, initializes all components, allocates memory.
  Destroy marks for garbage collection but doesn't free immediately.
  GC spikes cause visible frame drops. Memory fragments over time.
  This is particularly bad on mobile devices.
  
### **Solution**
  // WRONG: Instantiate/Destroy every shot
  public class BadGun : MonoBehaviour
  {
      [SerializeField] private GameObject bulletPrefab;
  
      void Fire()
      {
          var bullet = Instantiate(bulletPrefab, firePoint.position, firePoint.rotation);
          Destroy(bullet, 2f);  // GC spike every 2 seconds!
      }
  }
  
  // RIGHT: Object pooling
  public class BulletPool : MonoBehaviour
  {
      [SerializeField] private Bullet prefab;
      [SerializeField] private int poolSize = 50;
  
      private Queue<Bullet> _available = new();
      private HashSet<Bullet> _inUse = new();
  
      void Awake()
      {
          for (int i = 0; i < poolSize; i++)
          {
              var bullet = Instantiate(prefab, transform);
              bullet.gameObject.SetActive(false);
              _available.Enqueue(bullet);
          }
      }
  
      public Bullet Get(Vector3 position, Quaternion rotation)
      {
          var bullet = _available.Count > 0
              ? _available.Dequeue()
              : Instantiate(prefab, transform);
  
          bullet.transform.SetPositionAndRotation(position, rotation);
          bullet.gameObject.SetActive(true);
          bullet.OnSpawned();
          _inUse.Add(bullet);
  
          return bullet;
      }
  
      public void Return(Bullet bullet)
      {
          if (!_inUse.Contains(bullet)) return;
  
          bullet.OnDespawned();
          bullet.gameObject.SetActive(false);
          _inUse.Remove(bullet);
          _available.Enqueue(bullet);
      }
  }
  
### **Symptoms**
  - Frame rate hitches during gameplay
  - Profiler shows GC.Alloc spikes
  - Memory grows during play sessions
  - Stuttering when spawning many objects
### **Detection Pattern**
Instantiate\([^)]+\)[^;]*;[^}]*Destroy\(

## Physics In Wrong Update

### **Id**
physics-in-wrong-update
### **Summary**
Physics queries or operations outside FixedUpdate
### **Why**
  Physics simulation runs at fixed intervals. Doing physics work in Update means you're
  working with potentially stale data. Results can be inconsistent between frames.
  Raycasts in Update are usually fine, but force application is not.
  
### **Severity**
high
### **Situation**
Rigidbody manipulation, collision detection, or force application in Update
### **Solution**
  // WRONG: Setting velocity in Update
  void Update()
  {
      // This runs at variable rate - physics becomes inconsistent
      _rb.velocity = new Vector3(input.x, _rb.velocity.y, input.z) * speed;
  }
  
  // RIGHT: Use FixedUpdate for physics
  void FixedUpdate()
  {
      _rb.velocity = new Vector3(_input.x, _rb.velocity.y, _input.z) * speed;
  }
  
  void Update()
  {
      // Read input in Update (runs every frame)
      _input = new Vector2(Input.GetAxis("Horizontal"), Input.GetAxis("Vertical"));
  }
  
  // For Rigidbody movement without forces, use MovePosition in FixedUpdate
  void FixedUpdate()
  {
      Vector3 newPos = _rb.position + _moveDirection * speed * Time.fixedDeltaTime;
      _rb.MovePosition(newPos);
  }
  
### **Symptoms**
  - Physics feels "jittery"
  - Movement inconsistent across frame rates
  - Collisions sometimes miss
  - Character "slides" on slopes
### **Detection Pattern**
void Update\([^)]*\)[^}]*(\.velocity\s*=|MovePosition|AddForce)

## Serialization Trap

### **Id**
serialization-trap
### **Summary**
Not understanding Unity's serialization rules
### **Severity**
high
### **Situation**
Data not saving, prefab overrides not working, values resetting
### **Why**
  Unity serialization has specific rules that aren't obvious:
  - Private fields need [SerializeField]
  - Properties don't serialize
  - Static fields don't serialize
  - Dictionary doesn't serialize
  - Polymorphism requires [SerializeReference]
  Breaking these causes silent data loss.
  
### **Solution**
  // WRONG: Expecting these to serialize
  public class BadSerialization : MonoBehaviour
  {
      private int health = 100;  // Won't serialize - private without attribute
      public int Health { get; set; }  // Won't serialize - property
      static int score;  // Won't serialize - static
      public Dictionary<string, int> inventory;  // Won't serialize - Dictionary
  }
  
  // RIGHT: Proper serialization
  public class GoodSerialization : MonoBehaviour
  {
      [SerializeField] private int _health = 100;  // Serializes with attribute
  
      [field: SerializeField]  // C# 7.3+ - serializes backing field
      public int Armor { get; private set; }
  
      // Dictionary alternative - use two lists
      [SerializeField] private List<string> _inventoryKeys;
      [SerializeField] private List<int> _inventoryValues;
  
      // Or use serializable wrapper
      [Serializable]
      public class SerializableDictionary
      {
          public List<string> keys = new();
          public List<int> values = new();
      }
      [SerializeField] private SerializableDictionary _inventory;
  
      // Polymorphism requires SerializeReference
      [SerializeReference] private IWeapon _currentWeapon;
  }
  
  // Check what serializes with debug inspector
  // Or use SerializationUtility.HasManagedReferencesWithMissingTypes
  
### **Symptoms**
  - Values reset after play mode
  - Prefab overrides don't stick
  - Data lost between sessions
  - Inspector shows unexpected values
### **Detection Pattern**
private\s+\w+\s+\w+\s*=\s*[^;]+;(?![^}]*\[SerializeField\])

## Mobile Performance Traps

### **Id**
mobile-performance-traps
### **Summary**
Not considering mobile device limitations
### **Severity**
high
### **Situation**
Building for iOS/Android without mobile-specific optimizations
### **Why**
  Mobile GPUs are fill-rate limited. Mobile CPUs throttle under load.
  Memory is constrained. Battery drain matters. What runs fine in editor
  will melt a phone.
  
### **Solution**
  // Mobile performance checklist:
  
  // 1. Draw call batching
  // Use GPU Instancing, SRP Batcher, or Static/Dynamic batching
  // Target < 100 draw calls for low-end mobile
  
  // 2. Texture compression
  // Use ASTC for modern devices, ETC2 for older Android
  // Generate mipmaps for 3D, disable for UI
  
  // 3. Reduce overdraw
  // - Use occlusion culling
  // - Avoid transparent objects
  // - Use cutout instead of transparent when possible
  Graphics.activeTier = GraphicsTier.Tier1;  // For testing
  
  // 4. Optimize scripts
  void Update()
  {
      // DON'T do expensive operations every frame
      // Use coroutines or spread across frames
  }
  
  // Spread work across frames
  IEnumerator ProcessEnemiesOverFrames()
  {
      int processed = 0;
      foreach (var enemy in _enemies)
      {
          enemy.UpdateAI();
          processed++;
          if (processed % 10 == 0)  // Process 10 per frame
          {
              yield return null;
          }
      }
  }
  
  // 5. Profile on actual devices
  // Editor performance != Device performance
  // Test on lowest target device
  
  // 6. Memory management
  Resources.UnloadUnusedAssets();  // Periodically
  System.GC.Collect();  // Only at loading screens
  
### **Symptoms**
  - Works in editor, not on device
  - Device overheats
  - Frame rate drops on mobile
  - App gets killed by OS
### **Detection Pattern**


## String Animator Parameters

### **Id**
string-animator-parameters
### **Summary**
Using string-based Animator parameter access in hot paths
### **Severity**
high
### **Situation**
Setting animator parameters using strings in Update
### **Why**
  String hashing happens every call. Animator.StringToHash caches the hash.
  The difference is small but adds up across many objects every frame.
  
### **Solution**
  // WRONG: String every frame
  void Update()
  {
      animator.SetFloat("Speed", currentSpeed);  // String hash every frame!
      animator.SetBool("IsGrounded", isGrounded);
      animator.SetTrigger("Attack");
  }
  
  // RIGHT: Cache hashes
  private static readonly int SpeedHash = Animator.StringToHash("Speed");
  private static readonly int IsGroundedHash = Animator.StringToHash("IsGrounded");
  private static readonly int AttackHash = Animator.StringToHash("Attack");
  
  void Update()
  {
      animator.SetFloat(SpeedHash, currentSpeed);
      animator.SetBool(IsGroundedHash, isGrounded);
      animator.SetTrigger(AttackHash);
  }
  
### **Symptoms**
  - Profiler shows Animator string operations
  - Performance degrades with many animated objects
  - Unnecessary allocations each frame
### **Detection Pattern**
animator\.(SetFloat|SetBool|SetInteger|SetTrigger)\s*\(\s*"

## Find Methods Runtime

### **Id**
find-methods-runtime
### **Summary**
Using Find methods during gameplay
### **Severity**
critical
### **Situation**
Calling Find, FindObjectOfType, FindObjectsOfType frequently
### **Why**
  Find methods search the entire scene hierarchy. O(n) complexity where n is all GameObjects.
  FindObjectsOfType is even worse - searches all objects of type. Extremely expensive.
  There's almost never a good reason to use these at runtime.
  
### **Solution**
  // WRONG: Finding at runtime
  void Update()
  {
      var player = GameObject.Find("Player");  // Searches entire hierarchy!
      var enemies = FindObjectsOfType<Enemy>();  // Searches ALL components!
  }
  
  // WRONG: Finding in Start (still bad pattern)
  void Start()
  {
      _player = FindObjectOfType<Player>();  // Works but poor architecture
  }
  
  // RIGHT: Direct references
  public class EnemyAI : MonoBehaviour
  {
      [SerializeField] private Transform _player;  // Assign in inspector
      [SerializeField] private EnemyManager _manager;  // Reference manager
  }
  
  // RIGHT: ScriptableObject registry
  [CreateAssetMenu]
  public class PlayerRegistry : ScriptableObject
  {
      public Transform CurrentPlayer { get; private set; }
  
      public void Register(Transform player) => CurrentPlayer = player;
      public void Unregister() => CurrentPlayer = null;
  }
  
  public class Player : MonoBehaviour
  {
      [SerializeField] private PlayerRegistry _registry;
  
      void OnEnable() => _registry.Register(transform);
      void OnDisable() => _registry.Unregister();
  }
  
  // RIGHT: Event-based discovery
  public class EnemySpawner : MonoBehaviour
  {
      public event Action<Enemy> OnEnemySpawned;
      public event Action<Enemy> OnEnemyDestroyed;
  
      void SpawnEnemy()
      {
          var enemy = Instantiate(_prefab);
          OnEnemySpawned?.Invoke(enemy);
      }
  }
  
### **Symptoms**
  - Frame rate drops during gameplay
  - Profiler shows Find operations
  - Long frames when many objects exist - '"Stuttering" as scene grows'
### **Detection Pattern**
GameObject\.Find\s*\(|FindObjectOfType|FindObjectsOfType

## New Allocations Update

### **Id**
new-allocations-update
### **Summary**
Creating new objects in Update causes GC pressure
### **Severity**
high
### **Situation**
new Vector3, new List, string concatenation in Update
### **Why**
  Every 'new' allocates memory. Unity's GC is stop-the-world.
  Enough allocations trigger GC, causing frame drops.
  This is especially bad on mobile where GC is slower.
  
### **Solution**
  // WRONG: Allocations in Update
  void Update()
  {
      var direction = new Vector3(input.x, 0, input.y);  // Allocation!
      var enemies = new List<Enemy>();  // Allocation!
      Debug.Log("Position: " + transform.position);  // String allocation!
  
      foreach (var item in GetComponents<Collider>())  // Array allocation!
      {
          // ...
      }
  }
  
  // RIGHT: Reuse and cache
  private Vector3 _direction;
  private List<Enemy> _enemiesBuffer = new();
  private Collider[] _colliderBuffer = new Collider[10];
  private StringBuilder _sb = new();
  
  void Update()
  {
      _direction.Set(input.x, 0, input.y);  // No allocation
  
      _enemiesBuffer.Clear();  // Reuse list
      GetEnemiesNonAlloc(_enemiesBuffer);
  
      // Use GetComponentsNonAlloc
      int count = GetComponents(_colliderBuffer);
      for (int i = 0; i < count; i++)
      {
          var collider = _colliderBuffer[i];
          // ...
      }
  
      // StringBuilder for strings
      _sb.Clear();
      _sb.Append("Position: ").Append(transform.position);
      Debug.Log(_sb);  // Still allocates, but less
  }
  
  // Use struct instead of class for temporary data
  public readonly struct DamageEvent
  {
      public readonly float Amount;
      public readonly Vector3 Position;
  }
  
### **Symptoms**
  - GC.Alloc in profiler
  - Periodic frame drops
  - Memory grows during play
  - Stuttering every few seconds
### **Detection Pattern**
void (Update|FixedUpdate|LateUpdate)\s*\([^)]*\)[^}]*(new\s+(List|Vector|Array|\w+\[\])|\+\s*")

## Addressables Release Forgotten

### **Id**
addressables-release-forgotten
### **Summary**
Not releasing Addressables handles causes memory leaks
### **Severity**
high
### **Situation**
Loading Addressables assets without releasing them
### **Why**
  Addressables uses reference counting. Each LoadAssetAsync needs a Release.
  Without Release, assets stay in memory forever. This is different from
  Resources which Unity manages automatically.
  
### **Solution**
  // WRONG: Load without release
  public class BadLoader : MonoBehaviour
  {
      async void LoadCharacter()
      {
          var handle = Addressables.LoadAssetAsync<GameObject>("character");
          await handle.Task;
          Instantiate(handle.Result);
          // handle never released - MEMORY LEAK!
      }
  }
  
  // RIGHT: Track and release handles
  public class GoodLoader : MonoBehaviour
  {
      private AsyncOperationHandle<GameObject> _handle;
      private GameObject _instance;
  
      public async UniTask LoadCharacter()
      {
          _handle = Addressables.LoadAssetAsync<GameObject>("character");
          await _handle;
  
          if (_handle.Status == AsyncOperationStatus.Succeeded)
          {
              _instance = Instantiate(_handle.Result);
          }
      }
  
      void OnDestroy()
      {
          // CRITICAL: Release the handle
          if (_handle.IsValid())
          {
              Addressables.Release(_handle);
          }
  
          if (_instance != null)
          {
              Destroy(_instance);
          }
      }
  }
  
  // BETTER: Use InstantiateAsync for automatic tracking
  public async UniTask<GameObject> SpawnTracked(AssetReference reference)
  {
      // InstantiateAsync tracks the instance
      // Destroying the instance releases the reference
      var handle = reference.InstantiateAsync();
      await handle;
      return handle.Result;
  }
  
### **Symptoms**
  - Memory grows over time
  - Assets stay loaded after scene change
  - "Memory pressure" warnings
  - App crashes after extended play
### **Detection Pattern**
Addressables\.LoadAssetAsync(?![^}]*Release)

## Transform Hierarchy Deep

### **Id**
transform-hierarchy-deep
### **Summary**
Deep transform hierarchies hurt performance
### **Severity**
medium
### **Situation**
Many nested child objects, complex UI hierarchies
### **Why**
  Every Transform change propagates to all children. Deep hierarchies mean
  more matrices to update. UI Canvas rebuilds entire hierarchy on change.
  10+ levels deep starts to hurt.
  
### **Solution**
  // WRONG: Deep nesting
  // Player -> Body -> Arm -> Hand -> Fingers -> Finger1 -> Nail -> ...
  // Every move of Player recalculates entire chain
  
  // RIGHT: Flatten where possible
  // Player -> Body, Player -> Arm, Player -> Hand (siblings, not nested)
  
  // For UI specifically:
  // - Split into multiple Canvases
  // - Static elements on separate Canvas (no rebuild)
  // - Dynamic elements on minimal Canvas
  
  // Use Transform.SetParent with worldPositionStays=false
  // to avoid matrix recalculation
  child.SetParent(newParent, worldPositionStays: false);
  
  // Detach frequently-moving objects from static hierarchy
  public class DetachOnStart : MonoBehaviour
  {
      [SerializeField] private bool _detachFromParent = true;
  
      void Start()
      {
          if (_detachFromParent)
          {
              transform.SetParent(null);
          }
      }
  }
  
  // Profile with:
  Profiler.BeginSample("TransformWork");
  // ... transform operations
  Profiler.EndSample();
  
### **Symptoms**
  - UI feels slow
  - Moving parent causes lag
  - SetParent is expensive
  - Canvas.BuildBatch in profiler
### **Detection Pattern**


## Missing Null Checks

### **Id**
missing-null-checks
### **Summary**
Accessing destroyed Unity objects causes errors
### **Severity**
high
### **Situation**
Accessing components/GameObjects that might be destroyed
### **Why**
  Unity overloads == for UnityEngine.Object. Destroyed objects == null but aren't C# null.
  Accessing destroyed objects throws MissingReferenceException.
  This is common in callbacks, events, and coroutines.
  
### **Solution**
  // WRONG: No null check after potential destruction
  void OnEnemyKilled(Enemy enemy)
  {
      // Enemy might be destroyed by the time this event fires
      enemy.DropLoot();  // MissingReferenceException!
  }
  
  // WRONG: C# null check doesn't work for Unity objects
  if (enemy != null)  // This works but...
  {
      enemy.DropLoot();  // ...still might throw!
  }
  
  // RIGHT: Unity null check
  if (enemy != null && enemy)  // Redundant but clear
  {
      enemy.DropLoot();
  }
  
  // RIGHT: Unity-style null check
  if (enemy)  // Unity's operator bool
  {
      enemy.DropLoot();
  }
  
  // RIGHT: Explicit destroyed check
  if (!ReferenceEquals(enemy, null) && enemy != null)
  {
      enemy.DropLoot();
  }
  
  // For coroutines, check at yield points
  IEnumerator DelayedAction(Transform target)
  {
      yield return new WaitForSeconds(1f);
  
      if (!target)  // Target might be destroyed during wait
      {
          yield break;
      }
  
      target.position = newPosition;
  }
  
  // Use ?. with care - it uses C# null, not Unity null
  enemy?.DropLoot();  // Won't throw, but might not work as expected
  
### **Symptoms**
  - MissingReferenceException in callbacks
  - NullReferenceException after Destroy
  - Errors in coroutines
  - Race conditions with destruction
### **Detection Pattern**
Destroy\([^)]+\)[^}]*\n[^}]*\1\.