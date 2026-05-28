# Unity Development

## Patterns


---
  #### **Name**
Component Caching
  #### **Description**
Cache component references in Awake/Start instead of calling GetComponent repeatedly
  #### **When**
Any component that needs to reference other components on the same or other GameObjects
  #### **Example**
    // WRONG: GetComponent every frame
    public class BadPlayer : MonoBehaviour
    {
        void Update()
        {
            GetComponent<Rigidbody>().velocity = Vector3.forward;  // Expensive!
            transform.position += Vector3.up;  // transform is already cached, but others aren't
        }
    }
    
    // RIGHT: Cache in Awake
    public class GoodPlayer : MonoBehaviour
    {
        private Rigidbody _rb;
        private Transform _transform;
    
        void Awake()
        {
            _rb = GetComponent<Rigidbody>();
            _transform = transform;  // Even transform benefits from caching in hot paths
        }
    
        void Update()
        {
            _rb.velocity = Vector3.forward;
            _transform.position += Vector3.up;
        }
    }
    
    // BETTER: Use RequireComponent and SerializeField
    [RequireComponent(typeof(Rigidbody))]
    public class BetterPlayer : MonoBehaviour
    {
        [SerializeField] private Rigidbody _rb;  // Assign in Inspector or via Reset
    
        void Reset()
        {
            _rb = GetComponent<Rigidbody>();  // Auto-assign in editor
        }
    }
    

---
  #### **Name**
ScriptableObject Event Channel
  #### **Description**
Use ScriptableObjects as decoupled event channels between systems
  #### **When**
Systems need to communicate without direct references
  #### **Example**
    // Event channel definition
    [CreateAssetMenu(menuName = "Events/Void Event")]
    public class VoidEventChannel : ScriptableObject
    {
        private readonly HashSet<Action> _listeners = new();
    
        public void Raise()
        {
            foreach (var listener in _listeners)
            {
                listener?.Invoke();
            }
        }
    
        public void Subscribe(Action listener) => _listeners.Add(listener);
        public void Unsubscribe(Action listener) => _listeners.Remove(listener);
    }
    
    // Generic version for data
    public abstract class EventChannel<T> : ScriptableObject
    {
        private readonly HashSet<Action<T>> _listeners = new();
    
        public void Raise(T value)
        {
            foreach (var listener in _listeners)
            {
                listener?.Invoke(value);
            }
        }
    
        public void Subscribe(Action<T> listener) => _listeners.Add(listener);
        public void Unsubscribe(Action<T> listener) => _listeners.Remove(listener);
    }
    
    [CreateAssetMenu(menuName = "Events/Int Event")]
    public class IntEventChannel : EventChannel<int> { }
    
    // Usage in components
    public class PlayerHealth : MonoBehaviour
    {
        [SerializeField] private IntEventChannel _onHealthChanged;
        [SerializeField] private VoidEventChannel _onPlayerDied;
    
        private int _health = 100;
    
        public void TakeDamage(int amount)
        {
            _health -= amount;
            _onHealthChanged.Raise(_health);
            if (_health <= 0) _onPlayerDied.Raise();
        }
    }
    
    public class HealthUI : MonoBehaviour
    {
        [SerializeField] private IntEventChannel _onHealthChanged;
        [SerializeField] private TextMeshProUGUI _healthText;
    
        void OnEnable() => _onHealthChanged.Subscribe(UpdateHealth);
        void OnDisable() => _onHealthChanged.Unsubscribe(UpdateHealth);
    
        private void UpdateHealth(int health) => _healthText.text = health.ToString();
    }
    

---
  #### **Name**
Object Pooling
  #### **Description**
Reuse GameObjects instead of Instantiate/Destroy for frequently spawned objects
  #### **When**
Spawning bullets, particles, enemies, VFX, or any frequently created objects
  #### **Example**
    public class ObjectPool<T> where T : Component
    {
        private readonly T _prefab;
        private readonly Transform _parent;
        private readonly Queue<T> _pool = new();
        private readonly HashSet<T> _active = new();
    
        public ObjectPool(T prefab, int initialSize, Transform parent = null)
        {
            _prefab = prefab;
            _parent = parent;
    
            for (int i = 0; i < initialSize; i++)
            {
                CreateInstance();
            }
        }
    
        private T CreateInstance()
        {
            var instance = Object.Instantiate(_prefab, _parent);
            instance.gameObject.SetActive(false);
            _pool.Enqueue(instance);
            return instance;
        }
    
        public T Get(Vector3 position, Quaternion rotation)
        {
            var instance = _pool.Count > 0 ? _pool.Dequeue() : CreateInstance();
            instance.transform.SetPositionAndRotation(position, rotation);
            instance.gameObject.SetActive(true);
            _active.Add(instance);
    
            if (instance is IPoolable poolable)
            {
                poolable.OnSpawn();
            }
    
            return instance;
        }
    
        public void Release(T instance)
        {
            if (!_active.Contains(instance)) return;
    
            if (instance is IPoolable poolable)
            {
                poolable.OnDespawn();
            }
    
            instance.gameObject.SetActive(false);
            _active.Remove(instance);
            _pool.Enqueue(instance);
        }
    
        public void ReleaseAll()
        {
            foreach (var instance in _active.ToArray())
            {
                Release(instance);
            }
        }
    }
    
    public interface IPoolable
    {
        void OnSpawn();
        void OnDespawn();
    }
    
    // Usage
    public class BulletSpawner : MonoBehaviour
    {
        [SerializeField] private Bullet _bulletPrefab;
        private ObjectPool<Bullet> _bulletPool;
    
        void Awake()
        {
            _bulletPool = new ObjectPool<Bullet>(_bulletPrefab, 50, transform);
        }
    
        public void FireBullet(Vector3 position, Vector3 direction)
        {
            var bullet = _bulletPool.Get(position, Quaternion.LookRotation(direction));
            bullet.Initialize(direction, () => _bulletPool.Release(bullet));
        }
    }
    

---
  #### **Name**
Proper Update Selection
  #### **Description**
Use the correct update method for different types of logic
  #### **When**
Implementing any per-frame logic
  #### **Example**
    public class UpdatePatterns : MonoBehaviour
    {
        // Update - for game logic, input, non-physics movement
        // Called every frame, varies with frame rate
        void Update()
        {
            // Input handling
            if (Input.GetKeyDown(KeyCode.Space))
            {
                Jump();
            }
    
            // Non-physics movement (use Time.deltaTime)
            transform.Rotate(Vector3.up, _rotationSpeed * Time.deltaTime);
    
            // Animation state updates
            _animator.SetFloat("Speed", _currentSpeed);
        }
    
        // FixedUpdate - for physics operations ONLY
        // Called at fixed intervals (default 50 times/second)
        void FixedUpdate()
        {
            // Rigidbody forces and velocity
            _rb.AddForce(Vector3.forward * _moveForce);
    
            // Physics queries that affect physics
            if (Physics.Raycast(transform.position, Vector3.down, out var hit, 1f))
            {
                _isGrounded = true;
            }
        }
    
        // LateUpdate - for camera follow, after all Update calls
        // Called every frame after all Update methods
        void LateUpdate()
        {
            // Camera following
            _camera.position = Vector3.Lerp(
                _camera.position,
                _target.position + _offset,
                Time.deltaTime * _smoothSpeed
            );
    
            // IK adjustments
            // Cleanup after movement
        }
    }
    

---
  #### **Name**
Singleton Pattern (Unity-Safe)
  #### **Description**
Implement singletons correctly for managers and services
  #### **When**
Creating game-wide managers like AudioManager, GameManager, etc.
  #### **Example**
    // WRONG: Naive singleton - breaks on scene reload
    public class BadManager : MonoBehaviour
    {
        public static BadManager Instance;
        void Awake() => Instance = this;  // Overwrites on scene reload!
    }
    
    // RIGHT: Lazy singleton with DontDestroyOnLoad
    public abstract class Singleton<T> : MonoBehaviour where T : MonoBehaviour
    {
        private static T _instance;
        private static readonly object _lock = new();
        private static bool _applicationIsQuitting;
    
        public static T Instance
        {
            get
            {
                if (_applicationIsQuitting)
                {
                    Debug.LogWarning($"[Singleton] Instance of {typeof(T)} already destroyed.");
                    return null;
                }
    
                lock (_lock)
                {
                    if (_instance == null)
                    {
                        _instance = FindObjectOfType<T>();
    
                        if (_instance == null)
                        {
                            var singletonObject = new GameObject($"{typeof(T).Name} (Singleton)");
                            _instance = singletonObject.AddComponent<T>();
                            DontDestroyOnLoad(singletonObject);
                        }
                    }
    
                    return _instance;
                }
            }
        }
    
        protected virtual void Awake()
        {
            if (_instance == null)
            {
                _instance = this as T;
                DontDestroyOnLoad(gameObject);
            }
            else if (_instance != this)
            {
                Destroy(gameObject);
            }
        }
    
        protected virtual void OnApplicationQuit()
        {
            _applicationIsQuitting = true;
        }
    }
    
    // Usage
    public class AudioManager : Singleton<AudioManager>
    {
        public void PlaySound(AudioClip clip) { /* ... */ }
    }
    
    // BETTER: Use ScriptableObject services instead for testability
    [CreateAssetMenu(menuName = "Services/Audio Service")]
    public class AudioService : ScriptableObject
    {
        [SerializeField] private AudioSource _prefab;
        // No singleton needed - reference via SerializeField
    }
    

---
  #### **Name**
Async/Await Unity Pattern
  #### **Description**
Use modern async/await with proper Unity lifecycle handling
  #### **When**
Loading assets, making web requests, or any async operation
  #### **Example**
    using System.Threading;
    using UnityEngine;
    using Cysharp.Threading.Tasks;  // UniTask for better performance
    
    public class AsyncPatterns : MonoBehaviour
    {
        private CancellationTokenSource _cts;
    
        void OnEnable()
        {
            _cts = new CancellationTokenSource();
        }
    
        void OnDisable()
        {
            _cts?.Cancel();
            _cts?.Dispose();
        }
    
        // WRONG: Fire and forget async
        async void BadAsyncMethod()  // async void is dangerous!
        {
            await SomeAsyncOperation();  // No cancellation, no error handling
        }
    
        // RIGHT: Proper async with cancellation
        public async UniTaskVoid LoadDataAsync()
        {
            try
            {
                var data = await LoadFromServerAsync(_cts.Token);
                ProcessData(data);
            }
            catch (OperationCanceledException)
            {
                // Expected when cancelled - silent
            }
            catch (Exception e)
            {
                Debug.LogError($"Load failed: {e.Message}");
            }
        }
    
        // With timeout
        public async UniTask<Texture2D> LoadTextureWithTimeout(string url, float timeout)
        {
            using var timeoutCts = new CancellationTokenSource();
            timeoutCts.CancelAfter(TimeSpan.FromSeconds(timeout));
    
            using var linkedCts = CancellationTokenSource.CreateLinkedTokenSource(
                _cts.Token, timeoutCts.Token);
    
            var request = UnityWebRequestTexture.GetTexture(url);
            await request.SendWebRequest().WithCancellation(linkedCts.Token);
    
            return DownloadHandlerTexture.GetContent(request);
        }
    }
    

---
  #### **Name**
ScriptableObject Configuration
  #### **Description**
Use ScriptableObjects for game data and configuration
  #### **When**
Defining weapon stats, enemy types, level data, game settings
  #### **Example**
    // Define data structure
    [CreateAssetMenu(menuName = "Game/Weapon Data")]
    public class WeaponData : ScriptableObject
    {
        [Header("Basic Stats")]
        public string weaponName;
        public int damage;
        public float fireRate;
        public float range;
    
        [Header("Audio/Visual")]
        public AudioClip fireSound;
        public GameObject muzzleFlashPrefab;
        public AnimationClip fireAnimation;
    
        [Header("Ammo")]
        public int maxAmmo;
        public float reloadTime;
    }
    
    // Use in component
    public class Weapon : MonoBehaviour
    {
        [SerializeField] private WeaponData _data;
    
        private float _nextFireTime;
        private int _currentAmmo;
    
        void Start()
        {
            _currentAmmo = _data.maxAmmo;
        }
    
        public void Fire()
        {
            if (Time.time < _nextFireTime || _currentAmmo <= 0) return;
    
            _nextFireTime = Time.time + (1f / _data.fireRate);
            _currentAmmo--;
    
            // Use data from ScriptableObject
            DealDamage(_data.damage);
            PlaySound(_data.fireSound);
        }
    }
    
    // Create variants easily:
    // - Pistol.asset (damage: 10, fireRate: 5)
    // - Rifle.asset (damage: 25, fireRate: 10)
    // - Shotgun.asset (damage: 50, fireRate: 1)
    

---
  #### **Name**
Addressables Asset Loading
  #### **Description**
Load assets asynchronously using Addressables for better memory management
  #### **When**
Loading levels, characters, or any assets that shouldn't be in memory always
  #### **Example**
    using UnityEngine.AddressableAssets;
    using UnityEngine.ResourceManagement.AsyncOperations;
    
    public class AddressableLoader : MonoBehaviour
    {
        [SerializeField] private AssetReference _characterReference;
        private AsyncOperationHandle<GameObject> _loadHandle;
        private GameObject _loadedCharacter;
    
        public async UniTask<GameObject> LoadCharacterAsync()
        {
            // Load asset
            _loadHandle = _characterReference.LoadAssetAsync<GameObject>();
            await _loadHandle;
    
            if (_loadHandle.Status == AsyncOperationStatus.Succeeded)
            {
                _loadedCharacter = Instantiate(_loadHandle.Result);
                return _loadedCharacter;
            }
    
            Debug.LogError("Failed to load character");
            return null;
        }
    
        void OnDestroy()
        {
            // CRITICAL: Release handles to prevent memory leaks
            if (_loadHandle.IsValid())
            {
                Addressables.Release(_loadHandle);
            }
    
            if (_loadedCharacter != null)
            {
                Destroy(_loadedCharacter);
            }
        }
    
        // For instantiation, use InstantiateAsync for automatic cleanup
        public async UniTask<GameObject> SpawnEnemyAsync(AssetReference enemyRef, Vector3 pos)
        {
            var handle = enemyRef.InstantiateAsync(pos, Quaternion.identity);
            await handle;
    
            // InstantiateAsync tracks instance - released when destroyed
            return handle.Result;
        }
    }
    

## Anti-Patterns


---
  #### **Name**
GetComponent in Update
  #### **Description**
Calling GetComponent every frame instead of caching
  #### **Why**
    GetComponent is not free - it searches the component list. Called 60+ times per second
    across many objects, it adds up. This is one of the most common Unity performance mistakes.
    
  #### **Instead**
Cache in Awake/Start, use [SerializeField], or RequireComponent attribute.

---
  #### **Name**
Find Methods in Runtime
  #### **Description**
Using Find, FindObjectOfType, or FindObjectsOfType in Update or frequently called methods
  #### **Why**
    These methods search the entire scene hierarchy. They're O(n) where n is all GameObjects.
    Extremely expensive and completely unnecessary with proper architecture.
    
  #### **Instead**
Use SerializeField references, ScriptableObject registries, or event-based communication.

---
  #### **Name**
String-Based Operations in Hot Paths
  #### **Description**
Using CompareTag with strings, Animator.SetBool with strings in Update
  #### **Why**
    String comparisons are slow. String hashing happens every call. Garbage is generated.
    Unity provides alternatives for a reason.
    
  #### **Instead**
Use Animator.StringToHash for parameter IDs. Cache CompareTag results or use layer masks.

---
  #### **Name**
Instantiate/Destroy in Loops
  #### **Description**
Creating and destroying objects frequently instead of pooling
  #### **Why**
    Instantiate is expensive - it clones the prefab and initializes all components.
    Destroy doesn't free memory immediately - it marks for garbage collection.
    GC spikes cause frame drops.
    
  #### **Instead**
Object pooling for anything spawned more than once per second.

---
  #### **Name**
Physics in Update
  #### **Description**
Applying forces, setting velocity, or doing physics queries in Update instead of FixedUpdate
  #### **Why**
    Update runs at variable rate (frame rate dependent). Physics runs at fixed intervals.
    Applying forces in Update causes inconsistent physics behavior. Fast machines move faster.
    
  #### **Instead**
All Rigidbody operations in FixedUpdate. Use Time.deltaTime in Update for non-physics movement.

---
  #### **Name**
Deep Prefab Nesting
  #### **Description**
Prefabs containing prefabs containing prefabs
  #### **Why**
    Merge conflicts become impossible to resolve. Changes don't propagate as expected.
    Prefab overrides become confusing. Performance impact from nested instantiation.
    
  #### **Instead**
Flat prefab hierarchy. Use prefab variants. Compose at runtime when needed.

---
  #### **Name**
Coroutine Memory Leaks
  #### **Description**
Starting coroutines without stopping them when the object is disabled/destroyed
  #### **Why**
    Coroutines keep running after the object that started them is disabled.
    They hold references, preventing garbage collection. They can cause null reference exceptions.
    
  #### **Instead**
Store coroutine handles and stop in OnDisable. Use async/await with cancellation tokens.

---
  #### **Name**
SendMessage/BroadcastMessage
  #### **Description**
Using SendMessage for component communication
  #### **Why**
    Slow reflection-based calls. No compile-time checking. Silently fails if method doesn't exist.
    Encourages stringly-typed programming. Terrible for maintenance.
    
  #### **Instead**
Direct references, interfaces, UnityEvents, or ScriptableObject event channels.

---
  #### **Name**
MonoBehaviour for Data
  #### **Description**
Using MonoBehaviour scripts to hold configuration data
  #### **Why**
    MonoBehaviours require a GameObject. They have lifecycle overhead.
    They can't be easily shared or referenced across the project.
    
  #### **Instead**
ScriptableObjects for data. They're assets, versionable, and shareable.

---
  #### **Name**
Ignoring Serialization Rules
  #### **Description**
Expecting private fields to serialize, or using properties
  #### **Why**
    Unity's serialization has specific rules. Private fields need [SerializeField].
    Properties don't serialize. Non-serializable types silently fail. Data gets lost.
    
  #### **Instead**
Understand serialization rules. Use [SerializeField] for private fields. Test serialization.