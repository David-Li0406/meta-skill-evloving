# Animation Systems - Sharp Edges

## Root Motion Network Desynchronization

### **Id**
root-motion-network-desync
### **Severity**
critical
### **Description**
  Root motion in networked games causes position desync between clients.
  Animation-driven movement doesn't account for network latency.
  
### **Symptoms**
  - Characters teleport or rubber-band
  - Player position differs between clients
  - Attacks miss despite appearing to hit
  - Characters slide after animation ends
### **Cause**
  Root motion applies delta movement each frame. With network latency,
  clients animate at different times, accumulating position errors.
  
### **Solution**
  1. Server-authoritative position, client-side animation
  2. Snapshot root motion destination, lerp to it
  3. Use root motion for visuals only, code for actual movement
  4. Send target position with animation trigger
  
  ```csharp
  // Network-safe root motion
  [Command]
  void CmdPlayAttack(Vector3 startPos, Vector3 targetPos)
  {
      // Server validates and broadcasts
      RpcPlayAttackAnimation(startPos, targetPos);
  }
  
  [ClientRpc]
  void RpcPlayAttackAnimation(Vector3 startPos, Vector3 targetPos)
  {
      // Client plays animation but lerps to authoritative position
      StartCoroutine(AnimateToPosition(startPos, targetPos, attackDuration));
  }
  ```
  
### **References**
  - GDC: Networking in For Honor
### **Tags**
  - networking
  - root-motion
  - multiplayer

## Blend Tree Foot Synchronization

### **Id**
blend-tree-foot-sync
### **Severity**
high
### **Description**
  Blending between locomotion animations with different foot timing
  causes feet to blend through the ground or float.
  
### **Symptoms**
  - Feet clip through ground during walk-to-run transition
  - Character appears to hover at certain blend values
  - Foot IK goes crazy trying to compensate
  - Legs twist unnaturally during blends
### **Cause**
  Animation A has left foot down at frame 10, Animation B has right foot down.
  Blending 50/50 puts both feet at half-height = floating.
  
### **Solution**
  1. **Sync markers**: Tag foot contact points in all blend animations
  2. **Matching**: Only blend animations at matching foot phases
  3. **Normalized time**: Ensure all locomotion loops have same phase
  4. **Animation authoring**: Create animations with matched timing
  
  ```
  Walk cycle:    [L down]----[R down]----[L down]
  Run cycle:     [L down]----[R down]----[L down]
                      ↑           ↑
                 Sync points must align
  ```
  
  Unity: Use "Foot IK" on Humanoid with proper foot contacts
  Unreal: Use Sync Groups in Anim Graph
  
### **Tags**
  - blend-tree
  - locomotion
  - foot-sync

## Animation Compression Destroying Quality

### **Id**
animation-compression-artifacts
### **Severity**
medium
### **Description**
  Aggressive animation compression causes visible artifacts,
  especially on extremities and fast movements.
  
### **Symptoms**
  - Fingers jitter or pop
  - Weapon wobbles unnaturally
  - Fast swings have visible stepping
  - Facial animation looks robotic
### **Cause**
  Default compression settings optimize for size, not quality.
  Keyframe reduction removes important in-betweens.
  Quaternion compression loses precision on small bones.
  
### **Solution**
  Per-bone compression settings:
  ```
  Spine/Major bones: Normal compression (0.5 degrees)
  Hands/Fingers: Reduced compression (0.1 degrees)
  Weapons/Props: Minimal compression
  Facial: Minimal compression
  Fast actions: Increase keyframe density
  
  Unity AnimationClip settings:
  - Rotation Error: 0.5 (default) → 0.1 for fingers
  - Position Error: Increase precision for IK targets
  
  Unreal:
  - Per-track compression settings
  - "Bitwise Compress Only" for important bones
  ```
  
### **Tags**
  - compression
  - quality
  - mobile

## Any State Transition Trap

### **Id**
state-machine-any-state-trap
### **Severity**
high
### **Description**
  "Any State" transitions that trigger unexpectedly, creating
  animation loops or preventing normal state flow.
  
### **Symptoms**
  - Character stuck in animation loop
  - Can't exit a state despite meeting conditions
  - State machine behaves differently than expected
  - Same animation plays repeatedly
### **Cause**
  Any State checks EVERY frame, ignoring current state.
  If condition is met, it transitions even from the target state.
  Creates: A → B → A → B infinite loop.
  
### **Solution**
  1. **Guard conditions**: Check current state in transition
  2. **Can Transition To Self = false**: Prevent self-transitions
  3. **Exit time requirements**: Add minimum time in state
  4. **Use specific transitions**: Avoid Any State when possible
  
  ```csharp
  // In animator controller:
  // Any State → HitReact
  // Conditions: TookDamage = true
  // Settings: Can Transition To Self = FALSE
  
  // Reset trigger after transition
  void OnStateEnter(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)
  {
      if (stateInfo.IsName("HitReact"))
      {
          animator.ResetTrigger("TookDamage");
      }
  }
  ```
  
### **Tags**
  - state-machine
  - any-state
  - transitions

## IK Solver Performance Explosion

### **Id**
ik-performance-cost
### **Severity**
high
### **Description**
  IK solvers are expensive and scale poorly with bone chains
  and iteration counts.
  
### **Symptoms**
  - Frame rate drops with many characters
  - Animation update dominates profiler
  - IK quality varies with frame rate
  - Characters freeze momentarily
### **Cause**
  Each IK chain requires multiple iterations per frame.
  Full-body IK can be 10x more expensive than FK.
  IK runs on main thread, blocking gameplay.
  
### **Solution**
  ```
  IK Budget Guidelines (per character):
  - Foot IK: 2 chains, 3 iterations each (~0.1ms)
  - Hand IK: 2 chains, 3 iterations (~0.1ms)
  - Look At: 1 chain, single pass (~0.02ms)
  - Full Body: AVOID or LOD aggressively (~1-2ms)
  
  LOD Strategy:
  - Distance 0-10m: Full IK
  - Distance 10-25m: Foot IK only
  - Distance 25m+: No IK, baked animation
  
  Optimization:
  1. Reduce iteration count (3 is usually enough)
  2. Skip IK when not visible
  3. Update IK at reduced frequency (every 2-3 frames)
  4. Use analytical IK for 2-bone chains
  ```
  
### **Tags**
  - performance
  - ik
  - optimization

## Additive Animation Reference Pose Mismatch

### **Id**
additive-reference-pose-mismatch
### **Severity**
critical
### **Description**
  Additive animations created with wrong reference pose cause
  extreme deformation or bone explosion.
  
### **Symptoms**
  - Character explodes when additive plays
  - Bones rotate to impossible angles
  - Additive looks completely different on different bases
  - Subtle additive becomes extreme
### **Cause**
  Additive = TargetPose - ReferencePose
  If ReferencePose doesn't match base animation pose,
  the delta is wrong and compounds.
  
### **Solution**
  1. **Use consistent reference pose**: Usually T-pose or first frame
  2. **Create additive from same base**:
     ```
     Walking + Tired Additive = Walking Tired
     Reference for Tired Additive = Walking (first frame)
     ```
  3. **Test on multiple bases**: Verify additive works on all intended bases
  4. **Clamp extreme values**: Limit bone rotations
  
  Unity:
  - Set "Additive Reference Pose" in animation import
  - Use same rig reference pose for all additives
  
  Unreal:
  - "Apply Mesh Space Additive" vs "Local Space"
  - Define reference pose in skeleton
  
### **Tags**
  - additive
  - reference-pose
  - critical

## Animation Events Miss at Low Frame Rates

### **Id**
animation-event-timing-frame-rate
### **Severity**
medium
### **Description**
  Animation events can be skipped when frame rate drops,
  causing gameplay desync.
  
### **Symptoms**
  - Footstep sounds don't play at low FPS
  - Damage frame never triggers
  - VFX spawns at wrong time
  - Events work in editor, fail in build
### **Cause**
  Events fire when animation time crosses event time.
  Large delta times can skip over events entirely.
  Single-frame events are most vulnerable.
  
### **Solution**
  ```csharp
  // Option 1: Use event ranges instead of points
  // Event at frame 10-12 instead of exactly frame 10
  
  // Option 2: Check event window in code
  public class SafeAnimationEvents : StateMachineBehaviour
  {
      public float damageWindowStart = 0.3f;
      public float damageWindowEnd = 0.5f;
      private bool damageDealt = false;
  
      public override void OnStateUpdate(Animator animator,
          AnimatorStateInfo stateInfo, int layerIndex)
      {
          float normalizedTime = stateInfo.normalizedTime % 1f;
  
          if (!damageDealt &&
              normalizedTime >= damageWindowStart &&
              normalizedTime <= damageWindowEnd)
          {
              // Deal damage
              damageDealt = true;
          }
      }
  
      public override void OnStateExit(Animator animator,
          AnimatorStateInfo stateInfo, int layerIndex)
      {
          damageDealt = false;
      }
  }
  ```
  
### **Tags**
  - events
  - frame-rate
  - reliability

## Humanoid Retargeting Scale Problems

### **Id**
humanoid-retarget-scale-issues
### **Severity**
medium
### **Description**
  Retargeted animations look wrong due to different character
  proportions and scale.
  
### **Symptoms**
  - Hands don't reach targets
  - Feet float or clip through ground
  - Animations look stretched or compressed
  - IK targets are in wrong positions
### **Cause**
  Humanoid retargeting normalizes animations but can't account
  for all proportion differences. Arm length ratios, leg length,
  spine curvature all affect results.
  
### **Solution**
  1. **Match proportions**: Design characters with similar ratios
  2. **Use IK for contacts**: Hands reaching objects, feet on ground
  3. **Per-character adjustments**: Scale offsets for specific bones
  4. **Motion warping**: Adjust root motion for character scale
  
  ```
  Character A (source): Arm reach 1.0m
  Character B (target): Arm reach 0.8m
  
  Without correction: B's hands don't reach objects
  With IK correction: IK pulls hands to target positions
  
  Per-bone scale adjustment:
  - Import animation with "Preserve Hierarchy"
  - Apply bone-level scale multipliers
  ```
  
### **Tags**
  - retargeting
  - humanoid
  - scale

## Animation Layer Weight Popping

### **Id**
layer-weight-interpolation
### **Severity**
medium
### **Description**
  Instantly changing layer weights causes visible pops
  and unnatural transitions.
  
### **Symptoms**
  - Upper body snaps when aiming
  - Visible pop when enabling layer
  - Blending looks unnatural
### **Cause**
  Setting layer weight from 0 to 1 instantly blends
  current pose with layer pose in one frame.
  
### **Solution**
  ```csharp
  public class LayerWeightController : MonoBehaviour
  {
      private Animator animator;
      private float targetWeight;
      private float currentWeight;
      private int layerIndex = 1;
  
      [SerializeField] private float blendSpeed = 5f;
  
      void Update()
      {
          // Smoothly interpolate layer weight
          currentWeight = Mathf.MoveTowards(currentWeight, targetWeight,
              blendSpeed * Time.deltaTime);
          animator.SetLayerWeight(layerIndex, currentWeight);
      }
  
      public void EnableLayer()
      {
          targetWeight = 1f;
      }
  
      public void DisableLayer()
      {
          targetWeight = 0f;
      }
  }
  ```
  
### **Tags**
  - layers
  - blending
  - transitions

## Motion Matching Memory Explosion

### **Id**
motion-matching-memory
### **Severity**
high
### **Description**
  Motion matching pose databases can consume massive memory,
  especially with large motion capture libraries.
  
### **Symptoms**
  - Memory usage spikes on animation load
  - Long load times
  - Out of memory on consoles
  - Can't fit all characters in memory
### **Cause**
  Each frame of motion capture becomes a searchable pose.
  30 minutes of mocap at 30fps = 54,000 poses
  Each pose stores bone transforms + velocities + trajectory
  
### **Solution**
  ```
  Memory Optimization:
  1. Reduce pose database resolution (15fps vs 30fps)
  2. Compress pose data (quantize, delta encoding)
  3. Cluster similar poses, store representatives
  4. Stream pose data (load chunks as needed)
  5. Share databases between similar characters
  
  Typical budgets:
  - Main character: 50-100MB pose database
  - NPCs: 10-20MB shared database
  - Crowds: 2-5MB minimal database
  
  Compression techniques:
  - Store deltas from previous pose
  - Quantize floats to 16-bit
  - PCA dimensionality reduction on features
  ```
  
### **Tags**
  - motion-matching
  - memory
  - optimization