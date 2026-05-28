# Animation Systems - Validations

## Instant Layer Weight Change

### **Id**
instant-layer-weight
### **Description**
Layer weight set instantly instead of interpolated
### **Severity**
warning
### **Languages**
  - csharp
  - gdscript
### **Patterns**
  
---
    ##### **Regex**
SetLayerWeight\s*\([^,]+,\s*[01]\s*\)
    ##### **Message**
Setting layer weight to 0 or 1 instantly causes visual pops
  
---
    ##### **Regex**
SetLayerWeight\s*\([^,]+,\s*[^M][^a][^t][^h]
    ##### **Message**
Consider using Mathf.MoveTowards for smooth layer weight changes
### **Fix Hint**
  Use interpolation for smooth transitions:
  ```csharp
  currentWeight = Mathf.MoveTowards(currentWeight, targetWeight, speed * Time.deltaTime);
  animator.SetLayerWeight(layerIndex, currentWeight);
  ```
  

## IK Logic Outside OnAnimatorIK

### **Id**
ik-in-update
### **Description**
IK position/rotation set outside proper callback
### **Severity**
error
### **Languages**
  - csharp
### **Patterns**
  
---
    ##### **Regex**
void\s+Update\s*\([^)]*\)[^{]*\{[^}]*SetIKPosition
    ##### **Message**
IK must be set in OnAnimatorIK, not Update
  
---
    ##### **Regex**
void\s+LateUpdate\s*\([^)]*\)[^{]*SetIKPosition
    ##### **Message**
IK must be set in OnAnimatorIK, not LateUpdate
### **Fix Hint**
  Move IK logic to OnAnimatorIK callback:
  ```csharp
  void OnAnimatorIK(int layerIndex)
  {
      animator.SetIKPositionWeight(AvatarIKGoal.LeftFoot, 1f);
      animator.SetIKPosition(AvatarIKGoal.LeftFoot, targetPosition);
  }
  ```
  

## Animation Trigger Not Reset

### **Id**
missing-trigger-reset
### **Description**
Trigger parameters not reset after use
### **Severity**
warning
### **Languages**
  - csharp
### **Patterns**
  
---
    ##### **Regex**
SetTrigger\s*\([^)]+\)(?![\s\S]{0,200}ResetTrigger)
    ##### **Message**
SetTrigger without corresponding ResetTrigger can cause re-triggering
### **Fix Hint**
  Reset triggers after transition completes:
  ```csharp
  // In StateMachineBehaviour.OnStateEnter
  animator.ResetTrigger("Attack");
  ```
  

## Animator Speed Set to Zero

### **Id**
animator-speed-zero
### **Description**
Setting animator speed to 0 stops all animation processing
### **Severity**
warning
### **Languages**
  - csharp
### **Patterns**
  
---
    ##### **Regex**
animator\.speed\s*=\s*0
    ##### **Message**
animator.speed = 0 stops events and IK. Use SetFloat for playback speed.
### **Fix Hint**
  Instead of stopping animator, use a pause state or time scale:
  ```csharp
  // Option 1: Speed parameter
  animator.SetFloat("PlaybackSpeed", 0f);
  
  // Option 2: Pause state in state machine
  animator.SetBool("Paused", true);
  ```
  

## Crossfade with Zero Duration

### **Id**
crossfade-duration-zero
### **Description**
CrossFade called with 0 duration causes instant snap
### **Severity**
warning
### **Languages**
  - csharp
### **Patterns**
  
---
    ##### **Regex**
CrossFade\s*\([^,]+,\s*0\s*[,)]
    ##### **Message**
CrossFade with duration 0 causes instant snap - use at least 0.1
  
---
    ##### **Regex**
CrossFadeInFixedTime\s*\([^,]+,\s*0\s*[,)]
    ##### **Message**
CrossFade with duration 0 causes instant snap
### **Fix Hint**
  Use a minimum blend duration:
  ```csharp
  animator.CrossFade("StateName", 0.15f); // 150ms blend
  ```
  

## Root Motion Without OnAnimatorMove

### **Id**
root-motion-without-callback
### **Description**
Using root motion but not implementing OnAnimatorMove
### **Severity**
info
### **Languages**
  - csharp
### **Patterns**
  
---
    ##### **Regex**
applyRootMotion\s*=\s*true(?![\s\S]{0,500}OnAnimatorMove)
    ##### **Message**
Consider implementing OnAnimatorMove for root motion control
### **Fix Hint**
  Implement OnAnimatorMove for precise control:
  ```csharp
  void OnAnimatorMove()
  {
      Vector3 deltaPosition = animator.deltaPosition;
      transform.position += deltaPosition;
      transform.rotation *= animator.deltaRotation;
  }
  ```
  

## GetComponent in Animation Callback

### **Id**
getcomponent-in-animator-callback
### **Description**
GetComponent called every frame in animation callback
### **Severity**
warning
### **Languages**
  - csharp
### **Patterns**
  
---
    ##### **Regex**
OnAnimatorIK[^}]*GetComponent
    ##### **Message**
Cache GetComponent results - OnAnimatorIK runs every frame
  
---
    ##### **Regex**
OnAnimatorMove[^}]*GetComponent
    ##### **Message**
Cache GetComponent results - OnAnimatorMove runs every frame
### **Fix Hint**
  Cache component references:
  ```csharp
  private Rigidbody rb;
  void Awake() { rb = GetComponent<Rigidbody>(); }
  ```
  

## Raycast in IK Callback Every Frame

### **Id**
raycast-in-ik
### **Description**
Physics raycast in OnAnimatorIK without optimization
### **Severity**
warning
### **Languages**
  - csharp
### **Patterns**
  
---
    ##### **Regex**
OnAnimatorIK[^}]*Physics\.Raycast
    ##### **Message**
Consider caching raycast results or reducing frequency
### **Fix Hint**
  Optimize raycast frequency:
  ```csharp
  private int ikUpdateFrame;
  void OnAnimatorIK(int layerIndex)
  {
      // Only raycast every 3 frames
      if (Time.frameCount % 3 == 0)
      {
          UpdateFootIKTargets();
      }
      ApplyFootIK();
  }
  ```
  

## String-Based Animator Parameter Access

### **Id**
string-parameter-access
### **Description**
Using strings instead of hashed IDs for animator parameters
### **Severity**
info
### **Languages**
  - csharp
### **Patterns**
  
---
    ##### **Regex**
SetFloat\s*\(\s*"[^"]+"
    ##### **Message**
Use Animator.StringToHash for parameter names to avoid GC alloc
  
---
    ##### **Regex**
SetBool\s*\(\s*"[^"]+"
    ##### **Message**
Use Animator.StringToHash for parameter names
  
---
    ##### **Regex**
SetTrigger\s*\(\s*"[^"]+"
    ##### **Message**
Use Animator.StringToHash for parameter names
### **Fix Hint**
  Cache parameter hashes:
  ```csharp
  private static readonly int SpeedHash = Animator.StringToHash("Speed");
  private static readonly int JumpHash = Animator.StringToHash("Jump");
  
  void Update()
  {
      animator.SetFloat(SpeedHash, currentSpeed);
  }
  ```
  

## Play/CrossFade Without Layer Index

### **Id**
play-without-layer
### **Description**
Animation play call missing layer index in multi-layer setup
### **Severity**
info
### **Languages**
  - csharp
### **Patterns**
  
---
    ##### **Regex**
animator\.Play\s*\([^,)]+\)(?!.*\d)
    ##### **Message**
Consider specifying layer index for multi-layer animators
### **Fix Hint**
  Specify layer index explicitly:
  ```csharp
  animator.Play("StateName", 0);  // Layer 0
  animator.CrossFade("StateName", 0.2f, 1);  // Layer 1
  ```
  

## State Check Using String

### **Id**
state-check-string
### **Description**
Checking animator state with string instead of hash
### **Severity**
info
### **Languages**
  - csharp
### **Patterns**
  
---
    ##### **Regex**
IsName\s*\(\s*"
    ##### **Message**
Consider caching state name hash for frequent checks
### **Fix Hint**
  Use hashed state name:
  ```csharp
  private static readonly int IdleStateHash = Animator.StringToHash("Idle");
  
  if (stateInfo.shortNameHash == IdleStateHash)
  {
      // In idle state
  }
  ```
  

## Heavy Logic in Animation Event

### **Id**
animation-event-heavy-logic
### **Description**
Animation event handler doing expensive operations
### **Severity**
warning
### **Languages**
  - csharp
### **Patterns**
  
---
    ##### **Regex**
public void \w+Event\s*\([^)]*\)[^{]*\{[^}]*(Instantiate|GetComponent|Find|Load)
    ##### **Message**
Animation events should be lightweight - defer heavy work
### **Fix Hint**
  Keep animation events lightweight:
  ```csharp
  // Bad - heavy work in event
  public void SpawnEffectEvent()
  {
      Instantiate(effectPrefab, transform.position, Quaternion.identity);
  }
  
  // Good - use pooling and caching
  public void SpawnEffectEvent()
  {
      effectPool.Spawn(cachedSpawnPoint.position);
  }
  ```
  

## Blend Tree Threshold Gaps

### **Id**
blend-tree-threshold-gap
### **Description**
Blend tree with gaps in threshold values
### **Severity**
info
### **Languages**
  - yaml
  - json
### **Patterns**
  
---
    ##### **Regex**
threshold.*0\.0.*threshold.*1\.0
    ##### **Message**
Consider adding intermediate blend tree samples
### **Fix Hint**
  Add samples at key interpolation points:
  ```
  Speed blend tree:
  0.0 - Idle
  0.3 - Walk_Slow  (often missed!)
  0.6 - Walk
  1.0 - Run
  1.5 - Sprint
  ```
  

## Animation Blueprint Expensive Tick

### **Id**
anim-bp-tick-every-frame
### **Description**
Heavy logic in Animation Blueprint event graph
### **Severity**
warning
### **Languages**
  - cpp
### **Patterns**
  
---
    ##### **Regex**
NativeUpdateAnimation[^}]*(LineTrace|GetAllActors|SpawnActor)
    ##### **Message**
NativeUpdateAnimation runs every frame - avoid heavy operations
### **Fix Hint**
  Move expensive logic to gameplay code with lower frequency:
  ```cpp
  // In AnimInstance
  void UMyAnimInstance::NativeUpdateAnimation(float DeltaSeconds)
  {
      // Only use cached values here
      Speed = CachedSpeed;
  }
  
  // Update cached values from gameplay code at lower frequency
  void AMyCharacter::UpdateAnimationData()
  {
      AnimInstance->CachedSpeed = GetVelocity().Size();
  }
  ```
  

## Animation Montage Blend Out Not Handled

### **Id**
montage-blend-out-not-handled
### **Description**
Montage played without handling blend out completion
### **Severity**
info
### **Languages**
  - cpp
### **Patterns**
  
---
    ##### **Regex**
PlayAnimMontage\s*\([^)]+\)(?![\s\S]{0,200}OnMontageBlendingOut)
    ##### **Message**
Consider binding to OnMontageBlendingOut for cleanup
### **Fix Hint**
  Handle montage completion:
  ```cpp
  FOnMontageBlendingOutStarted BlendingOutDelegate;
  BlendingOutDelegate.BindUObject(this, &AMyCharacter::OnAttackMontageBlendOut);
  AnimInstance->Montage_Play(AttackMontage);
  AnimInstance->Montage_SetBlendingOutDelegate(BlendingOutDelegate, AttackMontage);
  ```
  

## AnimationTree Not Activated

### **Id**
animation-tree-not-active
### **Description**
AnimationTree created but not set to active
### **Severity**
warning
### **Languages**
  - gdscript
### **Patterns**
  
---
    ##### **Regex**
AnimationTree(?![\s\S]{0,100}active\s*=\s*true)
    ##### **Message**
AnimationTree must have active = true to process
### **Fix Hint**
  Activate the animation tree:
  ```gdscript
  func _ready():
      $AnimationTree.active = true
  ```
  

## Animation Callback Using String Method Name

### **Id**
animation-callback-string
### **Description**
Animation track calling method by string name
### **Severity**
info
### **Languages**
  - gdscript
### **Patterns**
  
---
    ##### **Regex**
method_track_add_key\([^)]*"[^"]+"
    ##### **Message**
Consider using Callable for type-safe animation callbacks
### **Fix Hint**
  Use Callable in Godot 4:
  ```gdscript
  # Instead of string method name
  animation.track_insert_key(track_idx, time, Callable(self, "my_method"))
  ```
  