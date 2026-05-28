# Game Ai Behavior - Validations

## Synchronous Pathfinding

### **Id**
ai-sync-pathfind
### **Severity**
critical
### **Title**
Synchronous Pathfinding in Update
### **Description**
Blocking pathfinding calls in Update cause frame spikes
### **Languages**
  - csharp
  - cpp
  - gdscript
### **Patterns**
  
---
    ##### **Regex**
void\s+Update\s*\([^)]*\)[^}]*FindPath\s*\(
    ##### **Message**
Pathfinding in Update() blocks main thread
  
---
    ##### **Regex**
void\s+Update\s*\([^)]*\)[^}]*CalculatePath\s*\(
    ##### **Message**
Path calculation in Update() blocks main thread
  
---
    ##### **Regex**
_process\s*\([^)]*\)[^}]*find_path\s*\(
    ##### **Message**
Pathfinding in _process() blocks main thread
### **Fix**
  Use async pathfinding or coroutines:
  ```csharp
  IEnumerator RequestPath(Vector3 target) {
      var request = new PathRequest(transform.position, target);
      pathManager.RequestPath(request);
      while (!request.IsComplete) yield return null;
      path = request.Result;
  }
  ```
  

## Expensive Find In Loop

### **Id**
ai-expensive-find
### **Severity**
critical
### **Title**
Expensive Find Operations in AI Loop
### **Description**
FindGameObjects is O(n) and should not run every frame
### **Languages**
  - csharp
### **Patterns**
  
---
    ##### **Regex**
void\s+Update\s*\([^)]*\)[^}]*FindGameObject
    ##### **Message**
FindGameObject in Update is expensive - cache references
  
---
    ##### **Regex**
void\s+Update\s*\([^)]*\)[^}]*FindObjectsOfType
    ##### **Message**
FindObjectsOfType in Update is very expensive
  
---
    ##### **Regex**
foreach.*FindGameObjectsWithTag
    ##### **Message**
Finding objects in loop - use cached list
### **Fix**
  Cache object references:
  ```csharp
  private List<Enemy> cachedEnemies;
  private float cacheRefreshTime = 1f;
  
  void Start() {
      InvokeRepeating(nameof(RefreshCache), 0, cacheRefreshTime);
  }
  
  void RefreshCache() {
      cachedEnemies = FindObjectsOfType<Enemy>().ToList();
  }
  ```
  

## Raycast Per Frame Per Target

### **Id**
ai-raycast-spam
### **Severity**
critical
### **Title**
Multiple Raycasts Per Frame
### **Description**
Raycasting for each target each frame is expensive
### **Languages**
  - csharp
  - cpp
### **Patterns**
  
---
    ##### **Regex**
foreach.*\{[^}]*Physics\.Raycast
    ##### **Message**
Raycast inside foreach loop - consider staggering
  
---
    ##### **Regex**
for\s*\([^)]*\)[^}]*Physics\.Linecast
    ##### **Message**
Linecast inside for loop - use tiered checks
  
---
    ##### **Regex**
void\s+Update[^}]*foreach[^}]*Raycast
    ##### **Message**
Multiple raycasts per frame in perception
### **Fix**
  Stagger perception and use tiered checks:
  ```csharp
  // Check distance first (cheap), then angle, then raycast
  if (distanceSquared > maxRangeSq) return false;
  if (Vector3.Dot(forward, toTarget) < cosFOV) return false;
  return !Physics.Linecast(eye, target, occlusionMask);
  ```
  

## Non Deterministic Random

### **Id**
ai-nondeterministic-random
### **Severity**
high
### **Title**
Non-Deterministic Random in AI
### **Description**
UnityEngine.Random is not seedable and causes multiplayer desync
### **Languages**
  - csharp
### **Patterns**
  
---
    ##### **Regex**
Random\.value
    ##### **Message**
Random.value is not deterministic - use seeded System.Random
  
---
    ##### **Regex**
Random\.Range\s*\(
    ##### **Message**
Random.Range is not deterministic for multiplayer
  
---
    ##### **Regex**
UnityEngine\.Random
    ##### **Message**
UnityEngine.Random not recommended for AI decisions
### **Fix**
  Use seeded random for deterministic behavior:
  ```csharp
  private System.Random rng;
  
  public void Initialize(int seed) {
      rng = new System.Random(seed);
  }
  
  public float GetRandomValue() {
      return (float)rng.NextDouble();
  }
  ```
  
### **Context**
Only applies to multiplayer games requiring determinism

## Giant State Switch

### **Id**
ai-state-explosion
### **Severity**
high
### **Title**
State Machine Complexity Explosion
### **Description**
Large switch statement indicates FSM needs refactoring
### **Languages**
  - csharp
  - cpp
  - gdscript
### **Patterns**
  
---
    ##### **Regex**
switch\s*\([^)]*state[^)]*\)[^}]*case[^}]*case[^}]*case[^}]*case[^}]*case[^}]*case
    ##### **Message**
6+ state cases - consider hierarchical FSM or behavior tree
  
---
    ##### **Regex**
if.*state.*==.*else if.*state.*==.*else if.*state.*==.*else if.*state
    ##### **Message**
Multiple state checks - refactor to state pattern
### **Fix**
  Use hierarchical state machine or behavior tree:
  ```csharp
  // Instead of giant switch, use state pattern
  public abstract class AIState {
      public abstract void Enter();
      public abstract void Update();
      public abstract void Exit();
  }
  
  // Or consider behavior tree for complex logic
  ```
  

## Magic Number Thresholds

### **Id**
ai-magic-numbers
### **Severity**
high
### **Title**
Hardcoded AI Thresholds
### **Description**
Magic numbers make AI difficult to tune and balance
### **Languages**
  - csharp
  - cpp
  - gdscript
### **Patterns**
  
---
    ##### **Regex**
if\s*\([^)]*health\s*[<>]=?\s*[0-9]+
    ##### **Message**
Hardcoded health threshold - use configurable value
  
---
    ##### **Regex**
if\s*\([^)]*distance\s*[<>]=?\s*[0-9]+\.?[0-9]*
    ##### **Message**
Hardcoded distance threshold - extract to constant
  
---
    ##### **Regex**
awareness\s*[<>]=?\s*0\.[0-9]+
    ##### **Message**
Hardcoded awareness threshold - make data-driven
### **Fix**
  Use ScriptableObject or config:
  ```csharp
  [CreateAssetMenu]
  public class AIConfig : ScriptableObject {
      public float AttackRange = 5f;
      public float FleeHealthPercent = 0.3f;
      public float AwarenessThreshold = 0.7f;
  }
  
  // Usage
  if (health < config.FleeHealthPercent * maxHealth) Flee();
  ```
  

## Unthrottled Perception

### **Id**
ai-unthrottled-perception
### **Severity**
high
### **Title**
Perception System Without Throttling
### **Description**
Perception running every frame for all AI is expensive
### **Languages**
  - csharp
### **Patterns**
  
---
    ##### **Regex**
void\s+Update\s*\([^)]*\)[^}]*UpdatePerception
    ##### **Message**
Perception in Update - add throttling/staggering
  
---
    ##### **Regex**
void\s+Update\s*\([^)]*\)[^}]*CheckVisibility
    ##### **Message**
Visibility check every frame - stagger across frames
### **Fix**
  Stagger perception updates:
  ```csharp
  private float perceptionTimer;
  private const float PerceptionInterval = 0.15f;
  
  void Update() {
      perceptionTimer += Time.deltaTime;
      if (perceptionTimer >= PerceptionInterval) {
          UpdatePerception();
          perceptionTimer = 0;
      }
  }
  ```
  

## Allocations In Update

### **Id**
ai-update-allocations
### **Severity**
medium
### **Title**
Memory Allocations in AI Update
### **Description**
Allocating in hot loops causes GC spikes
### **Languages**
  - csharp
### **Patterns**
  
---
    ##### **Regex**
void\s+Update[^}]*new\s+List
    ##### **Message**
List allocation in Update causes GC pressure
  
---
    ##### **Regex**
void\s+Update[^}]*\.ToList\(\)
    ##### **Message**
ToList() allocates - cache the list
  
---
    ##### **Regex**
void\s+Update[^}]*new\s+Dictionary
    ##### **Message**
Dictionary allocation in Update loop
  
---
    ##### **Regex**
void\s+Update[^}]*\.ToArray\(\)
    ##### **Message**
ToArray() allocates - reuse array
### **Fix**
  Cache and reuse collections:
  ```csharp
  private List<Enemy> nearbyEnemies = new List<Enemy>();
  
  void UpdatePerception() {
      nearbyEnemies.Clear();  // Reuse, don't reallocate
      foreach (var enemy in cachedEnemyList) {
          if (IsNearby(enemy)) nearbyEnemies.Add(enemy);
      }
  }
  ```
  

## Missing Null Checks

### **Id**
ai-null-checks
### **Severity**
medium
### **Title**
Missing Null Checks on AI Targets
### **Description**
Targets can be destroyed mid-behavior, causing errors
### **Languages**
  - csharp
### **Patterns**
  
---
    ##### **Regex**
target\.position
    ##### **Message**
Access target.position without null check
  
---
    ##### **Regex**
currentTarget\.transform
    ##### **Message**
Access target transform without null check
  
---
    ##### **Regex**
enemy\.(position|transform|Health)
    ##### **Message**
Direct enemy property access - target may be dead
### **Fix**
  Always check target validity:
  ```csharp
  void Update() {
      if (target == null || !target.gameObject.activeInHierarchy) {
          target = null;
          TransitionTo<IdleState>();
          return;
      }
      // Safe to use target
  }
  ```
  

## Behavior Tree Depth

### **Id**
ai-bt-depth
### **Severity**
medium
### **Title**
Deep Behavior Tree Nesting
### **Description**
Deeply nested BTs are hard to debug and visualize
### **Languages**
  - csharp
  - gdscript
### **Patterns**
  
---
    ##### **Regex**
Selector\s*\{[^}]*Selector\s*\{[^}]*Selector
    ##### **Message**
3+ levels of nested Selectors - consider subtrees
  
---
    ##### **Regex**
Sequence\s*\{[^}]*Sequence\s*\{[^}]*Sequence\s*\{[^}]*Sequence
    ##### **Message**
Deep nested Sequences - flatten or use subtrees
### **Fix**
  Extract to subtrees:
  ```csharp
  // Instead of deep nesting
  var combatSubtree = new Subtree("Combat", new Selector(
      new AttackSequence(),
      new DefendSequence()
  ));
  
  var root = new Selector(
      combatSubtree,
      investigateSubtree,
      patrolSubtree
  );
  ```
  

## Goap Missing Procedural Check

### **Id**
ai-goap-procedural
### **Severity**
medium
### **Title**
GOAP Action Missing Procedural Precondition
### **Description**
Actions need runtime validity checks beyond world state
### **Languages**
  - csharp
### **Patterns**
  
---
    ##### **Regex**
class\s+\w+Action[^}]*Preconditions[^}]*(?!.*CheckProceduralPrecondition)
    ##### **Message**
GOAP action may need procedural precondition check
### **Fix**
  Add procedural precondition:
  ```csharp
  public class AttackAction : GOAPAction {
      public override bool CheckProceduralPrecondition(Agent agent) {
          // Runtime checks that can't be in static world state
          return agent.Weapon != null &&
                 agent.Weapon.HasAmmo &&
                 !agent.IsStunned;
      }
  }
  ```
  

## Missing Ai Visualization

### **Id**
ai-no-debug-viz
### **Severity**
low
### **Title**
AI Without Debug Visualization
### **Description**
Debug visualization is essential for tuning AI
### **Languages**
  - csharp
### **Patterns**
  
---
    ##### **Regex**
class\s+\w+(AI|Brain|Controller)[^}]+(?!.*OnDrawGizmos)
    ##### **Message**
Consider adding OnDrawGizmos for AI debugging
  
---
    ##### **Regex**
class\s+\w+Perception[^}]+(?!.*Debug\.Draw)
    ##### **Message**
Perception system should have debug visualization
### **Fix**
  Add gizmos for debugging:
  ```csharp
  void OnDrawGizmosSelected() {
      // Sight range
      Gizmos.color = Color.yellow;
      Gizmos.DrawWireSphere(transform.position, sightRange);
  
      // FOV
      Gizmos.color = Color.red;
      Vector3 leftBound = Quaternion.Euler(0, -fov/2, 0) * transform.forward;
      Vector3 rightBound = Quaternion.Euler(0, fov/2, 0) * transform.forward;
      Gizmos.DrawLine(transform.position, transform.position + leftBound * sightRange);
      Gizmos.DrawLine(transform.position, transform.position + rightBound * sightRange);
  
      // Current target
      if (currentTarget != null) {
          Gizmos.color = Color.green;
          Gizmos.DrawLine(transform.position, currentTarget.position);
      }
  }
  ```
  

## Steering Without Arrival

### **Id**
ai-no-arrival
### **Severity**
low
### **Title**
Seek Without Arrival Behavior
### **Description**
Pure seek causes oscillation near target
### **Languages**
  - csharp
### **Patterns**
  
---
    ##### **Regex**
Seek\s*\([^)]*\)[^}]*(?!.*Arrive|slowingRadius|arrivalRadius)
    ##### **Message**
Seek behavior should include arrival slowdown
### **Fix**
  Add arrival behavior:
  ```csharp
  Vector3 Seek(Vector3 target) {
      Vector3 toTarget = target - transform.position;
      float distance = toTarget.magnitude;
  
      // Arrival behavior
      float speed = (distance < arrivalRadius)
          ? maxSpeed * (distance / arrivalRadius)
          : maxSpeed;
  
      if (distance < deadZone) return -velocity; // Brake
  
      return toTarget.normalized * speed - velocity;
  }
  ```
  