# Animation Systems Architect

## Patterns

### **Animation State Machine**
  #### **Name**
Hierarchical State Machine Pattern
  #### **Description**
Organize animation states into logical hierarchies
  #### **When**
Character has multiple movement modes with sub-states
  #### **Structure**
    ```
    Locomotion (super state)
    ├── Idle
    │   ├── Idle_Relaxed
    │   ├── Idle_Alert
    │   └── Idle_Tired
    ├── Walk
    │   ├── Walk_Forward
    │   └── Walk_Strafe (blend space)
    ├── Run
    │   ├── Run_Forward
    │   └── Run_Strafe (blend space)
    └── Sprint
    
    Combat (super state)
    ├── Ready
    ├── Attack
    │   ├── Light_Attack_Chain
    │   └── Heavy_Attack
    └── Block
    
    Global transitions:
    - Any → Death (priority: highest)
    - Any → Hit_React (priority: high)
    - Locomotion ↔ Combat (via draw/sheathe)
    ```
    
  #### **Benefits**
    - Reduces transition complexity
    - Enables shared transitions at super-state level
    - Makes state machine readable
    - Isolates concerns
### **Blend Tree Design**
  #### **Name**
Multi-Dimensional Blend Space
  #### **Description**
Use blend spaces for continuous parameter animation
  #### **Example**
    ```csharp
    // Unity: 2D Blend Tree for directional movement
    // Parameters: MoveX (-1 to 1), MoveY (-1 to 1)
    
    // Blend tree samples:
    // (0, 0)    → Idle
    // (0, 1)    → Walk_Forward
    // (0, -1)   → Walk_Backward
    // (1, 0)    → Walk_Right
    // (-1, 0)   → Walk_Left
    // (0.7, 0.7) → Walk_Forward_Right (interpolated)
    
    // Speed-based blend (1D):
    // 0.0 → Idle
    // 0.5 → Walk
    // 1.0 → Run
    // 1.5 → Sprint
    ```
    
  #### **Guidelines**
    - Place samples at extremes and key points
    - Ensure animations have matching foot timing
    - Use normalized time for looping blends
    - Consider velocity vs direction separation
### **Animation Layers**
  #### **Name**
Layered Animation System
  #### **Description**
Separate body parts for independent animation
  #### **Structure**
    ```
    Layer 0: Base (Full Body)
      - Locomotion state machine
      - Weight: 1.0, Mask: Full body
    
    Layer 1: Upper Body Override
      - Weapon animations, gestures
      - Weight: Variable, Mask: Spine and above
      - Blend: Override or Additive
    
    Layer 2: Additive
      - Breathing, head look, hit reactions
      - Weight: Variable, Mask: Specific bones
      - Blend: Additive only
    
    Layer 3: IK Corrections
      - Foot placement, hand IK
      - Weight: 1.0, Mask: IK targets
      - Applied post-animation
    ```
    
  #### **When To Use**
    - Character needs to run while aiming
    - Facial animation independent of body
    - Additive hit reactions without interrupting movement
### **Root Motion Integration**
  #### **Name**
Root Motion Control Pattern
  #### **Description**
Properly integrate root motion with gameplay
  #### **Implementation**
    ```csharp
    public class RootMotionController : MonoBehaviour
    {
        private Animator animator;
        private CharacterController controller;
    
        [SerializeField] private bool useRootMotion = true;
        [SerializeField] private bool applyRootRotation = true;
    
        // Root motion works in OnAnimatorMove
        void OnAnimatorMove()
        {
            if (!useRootMotion) return;
    
            // Apply root motion delta
            Vector3 deltaPosition = animator.deltaPosition;
            Quaternion deltaRotation = animator.deltaRotation;
    
            // Optional: Project onto ground plane
            deltaPosition.y = 0;
    
            // Apply movement
            controller.Move(deltaPosition);
    
            if (applyRootRotation)
            {
                transform.rotation *= deltaRotation;
            }
        }
    
        // For specific animations, can override
        public void SetRootMotionMode(bool position, bool rotation)
        {
            useRootMotion = position;
            applyRootRotation = rotation;
        }
    }
    ```
    
  #### **Critical Notes**
    - Animator.applyRootMotion must be true
    - OnAnimatorMove replaces default root motion application
    - Root motion and physics can conflict - choose one authority
    - Networked games need special handling for root motion
### **Ik System**
  #### **Name**
IK System Architecture
  #### **Description**
Layered IK for different body parts
  #### **Implementation**
    ```csharp
    public class IKController : MonoBehaviour
    {
        private Animator animator;
    
        [Header("Foot IK")]
        [SerializeField] private bool enableFootIK = true;
        [SerializeField] private LayerMask groundLayer;
        [SerializeField] private float footOffset = 0.1f;
        [SerializeField] private float raycastDistance = 1.5f;
    
        [Header("Look At IK")]
        [SerializeField] private bool enableLookAt = true;
        [SerializeField] private Transform lookTarget;
        [SerializeField] private float lookAtWeight = 0.7f;
        [SerializeField] private float bodyWeight = 0.3f;
        [SerializeField] private float headWeight = 1.0f;
    
        void OnAnimatorIK(int layerIndex)
        {
            if (animator == null) return;
    
            // Foot IK
            if (enableFootIK)
            {
                ApplyFootIK(AvatarIKGoal.LeftFoot);
                ApplyFootIK(AvatarIKGoal.RightFoot);
            }
    
            // Look At IK
            if (enableLookAt && lookTarget != null)
            {
                animator.SetLookAtWeight(lookAtWeight, bodyWeight, headWeight);
                animator.SetLookAtPosition(lookTarget.position);
            }
        }
    
        private void ApplyFootIK(AvatarIKGoal foot)
        {
            // Get current foot position
            Vector3 footPos = animator.GetIKPosition(foot);
    
            // Raycast down
            if (Physics.Raycast(footPos + Vector3.up, Vector3.down,
                out RaycastHit hit, raycastDistance, groundLayer))
            {
                // Set position
                Vector3 targetPos = hit.point + Vector3.up * footOffset;
                animator.SetIKPositionWeight(foot, 1f);
                animator.SetIKPosition(foot, targetPos);
    
                // Align rotation to surface
                Quaternion footRotation = Quaternion.LookRotation(
                    Vector3.ProjectOnPlane(transform.forward, hit.normal),
                    hit.normal);
                animator.SetIKRotationWeight(foot, 1f);
                animator.SetIKRotation(foot, footRotation);
            }
        }
    }
    ```
    
### **Animation Events**
  #### **Name**
Animation Event System
  #### **Description**
Decouple animation timing from gameplay logic
  #### **Pattern**
    ```csharp
    // Event receiver - handles animation callbacks
    public class AnimationEventReceiver : MonoBehaviour
    {
        public event Action<string> OnFootstep;
        public event Action<int> OnAttackFrame;
        public event Action OnAttackEnd;
        public event Action<string> OnSoundEvent;
        public event Action<string, Vector3> OnVFXEvent;
    
        // Called from animation events
        public void Footstep(string surface)
        {
            OnFootstep?.Invoke(surface);
        }
    
        public void AttackDamageFrame(int attackId)
        {
            OnAttackFrame?.Invoke(attackId);
        }
    
        public void AttackFinished()
        {
            OnAttackEnd?.Invoke();
        }
    
        public void PlaySound(string soundId)
        {
            OnSoundEvent?.Invoke(soundId);
        }
    
        public void SpawnVFX(string vfxId)
        {
            // Use animation event's transform for position
            OnVFXEvent?.Invoke(vfxId, transform.position);
        }
    }
    
    // Combat system subscribes to events
    public class CombatController : MonoBehaviour
    {
        private AnimationEventReceiver eventReceiver;
    
        void Start()
        {
            eventReceiver = GetComponent<AnimationEventReceiver>();
            eventReceiver.OnAttackFrame += HandleDamageFrame;
            eventReceiver.OnAttackEnd += HandleAttackEnd;
        }
    
        private void HandleDamageFrame(int attackId)
        {
            // Only now do we check for hits
            PerformDamageCheck(attackId);
        }
    }
    ```
    
### **Motion Matching**
  #### **Name**
Motion Matching Setup
  #### **Description**
Data-driven animation selection
  #### **Concept**
    ```
    Motion Matching Pipeline:
    
    1. Annotation Phase (Offline):
       - Tag motion capture data with features
       - Features: foot positions, velocities, trajectory
       - Build searchable pose database
    
    2. Runtime Query:
       Current State:
       - Current pose (bone positions/velocities)
       - Current trajectory (where we are going)
    
       Desired State:
       - Input trajectory (where player wants to go)
       - Desired velocity
    
    3. Pose Search:
       - Find pose in database that best matches:
         a) Current pose (for smooth transition)
         b) Desired trajectory (for responsiveness)
       - Cost = w1 * PoseCost + w2 * TrajectoryCost
    
    4. Transition:
       - Jump to best matching pose
       - Optional: blend for X frames
       - Continue playing from that point
    
    Key Parameters:
    - Search frequency: Every N frames (e.g., 10)
    - Blend time: 0.1-0.3 seconds
    - Pose vs trajectory weight balance
    ```
    
  #### **When To Use**
    - Large motion capture dataset available
    - Need natural, fluid locomotion
    - Traditional state machines too complex

## Anti-Patterns

### **State Machine Explosion**
  #### **Name**
State Machine Explosion
  #### **Description**
Too many states with too many transitions
  #### **Smell**
    - State machine has 50+ states at one level
    - Every state has transitions to every other state
    - Adding one animation requires touching 20 transitions
    - Animators can't understand the state machine
    
  #### **Problem**
    Results from not using hierarchical states or blend spaces.
    Every animation becomes its own state instead of a parameter.
    
  #### **Fix**
    1. Use super-states (hierarchies) to group related states
    2. Use blend trees for continuous variations (directions, speeds)
    3. Use global transitions for common interrupts (death, hit)
    4. Each state should have max 3-5 outgoing transitions
    
### **Animation Over Gameplay**
  #### **Name**
Animation Driving Gameplay
  #### **Description**
Letting animation dictate game feel instead of supporting it
  #### **Smell**
    - Player feels "sluggish" or "unresponsive"
    - Must wait for animation to complete before acting
    - Canceling moves feels impossible
    - Animation looks great in showcase, terrible in gameplay
    
  #### **Problem**
    Animation made in isolation without gameplay considerations.
    No interrupt points, no animation canceling, no blending out.
    
  #### **Fix**
    ```
    Design Principles:
    1. Input buffering - accept input during animations
    2. Clear interrupt windows - when can player cancel?
    3. Variable blend out times based on priority
    4. "Committal" moves should be explicit design choices
    
    Example Attack:
    - Frames 0-5: Can cancel into dodge
    - Frames 6-15: Damage active, fully committed
    - Frames 16-25: Recovery, can cancel into another attack
    - Frames 26+: Can transition to any state
    ```
    
### **Foot Sliding**
  #### **Name**
Foot Sliding
  #### **Description**
Feet moving across ground during locomotion
  #### **Causes**
    - Animation speed doesn't match character velocity
    - Blend tree mixing animations with different stride lengths
    - Root motion disabled but animation expects it
    - Incorrect animation clips for current speed
    
  #### **Fixes**
    1. Match animation playback speed to movement speed
    2. Use motion warping to stretch/compress animations
    3. Ensure blend tree clips have matching timing
    4. Use foot IK as last resort (doesn't fix root cause)
    
    ```csharp
    // Speed-matched playback
    float currentSpeed = velocity.magnitude;
    float animSpeed = currentAnimationVelocity;
    animator.speed = currentSpeed / animSpeed;
    ```
    
### **Ik Everywhere**
  #### **Name**
IK Overuse
  #### **Description**
Using IK when baked animation would be better
  #### **Problem**
    IK is expensive and can produce unnatural results.
    Using runtime IK for things that should be animated.
    
  #### **Guidelines**
    Use IK for:
    - Ground adaptation (foot IK)
    - Dynamic targets (look at, aim at)
    - Object interaction (grab handles)
    - Procedural adjustments
    
    Don't use IK for:
    - Standard locomotion
    - Pre-choreographed sequences
    - Cutscenes with known positions
    - Anything that can be baked
    
### **Additive Abuse**
  #### **Name**
Additive Animation Abuse
  #### **Description**
Using additive layers incorrectly
  #### **Problems**
    - Additive animation on wrong base pose
    - Too many additive layers stacking
    - Additive animations not designed as additive
    - Extreme values causing bone explosion
    
  #### **Rules**
    1. Additive = (Target Pose - Reference Pose)
    2. Reference pose MUST match the base animation's pose
    3. Keep additive animations subtle
    4. Clamp additive values to prevent over-rotation
    5. Max 2-3 additive layers
    