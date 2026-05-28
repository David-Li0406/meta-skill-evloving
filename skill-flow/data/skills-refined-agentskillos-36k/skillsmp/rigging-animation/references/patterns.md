# Rigging & Animation Systems

## Patterns


---
  #### **Name**
Proper Joint Orientation
  #### **Description**
All joints aim down the bone with consistent up-axis throughout the chain
  #### **When**
Creating any skeleton hierarchy
  #### **Example**
    # Maya joint orientation rules:
    # 1. Primary axis (X) aims DOWN the bone toward child
    # 2. Secondary axis (Y) aims toward the bend direction
    # 3. Tertiary axis (Z) is the twist axis
    
    # For a left arm chain:
    # Shoulder: X aims toward elbow, Y aims forward, Z aims up
    # Elbow: X aims toward wrist, Y aims up (matches bend), Z aims forward
    # Wrist: X aims toward fingers, Y aims up, Z aims forward
    
    # In Blender bone roll:
    # Roll should be consistent - typically Z-up for arms/legs
    # Use "Recalculate Roll" with "Global +Z Axis" as starting point
    # Then manually adjust for twist behavior
    
    # Key rule: Mirror joints should have MIRRORED orientations
    # Left arm Y+ forward = Right arm Y+ forward (NOT mirrored)
    # This ensures animations mirror correctly
    
    # Validation command (Maya):
    import maya.cmds as cmds
    def validate_joint_orientation(joint):
        children = cmds.listRelatives(joint, children=True, type='joint')
        if not children:
            return True
        # Check X axis points toward child
        joint_pos = cmds.xform(joint, q=True, ws=True, t=True)
        child_pos = cmds.xform(children[0], q=True, ws=True, t=True)
        # X should be the direction to child
        return True  # Add actual dot product validation
    

---
  #### **Name**
Twist Bone Setup
  #### **Description**
Add roll/twist bones to forearms and thighs to prevent candy wrapper deformation
  #### **When**
Rigging any humanoid or creature with twisting limbs
  #### **Example**
    # Forearm twist setup (distribute twist from wrist to elbow):
    # Without twist bones: wrist rotation = 100% twist at wrist, horrible candy wrapper
    # With twist bones: twist distributed = natural deformation
    
    # Maya setup with 2 twist bones:
    # ElbowTwist01 at 33% from elbow to wrist - receives 33% wrist twist
    # ElbowTwist02 at 66% from elbow to wrist - receives 66% wrist twist
    # Wrist receives 100% of its own twist
    
    # Constraint setup (Maya):
    # orientConstraint -mo -skip y -skip z wrist_jnt forearmTwist02_jnt;
    # Set weight to 0.66 for 66% influence
    
    # Blender setup using drivers:
    # Add "Copy Rotation" constraint to twist bone
    # Target: Wrist bone, Space: Local
    # Mix Mode: Add, Influence: 0.5 (for middle twist bone)
    # CRITICAL: Only copy the twist axis (typically Y for Blender's bone orientation)
    
    # Unity setup:
    # Use Animation Rigging package
    # Add TwistCorrection component to twist bones
    # Set Source: Wrist transform
    # Set Twist Axis: appropriate axis
    # Set Weight: 0.33, 0.66 for distribution
    
    # Twist bone count recommendations:
    # Stylized/Mobile: 1 twist bone per limb segment
    # Realistic/PC: 2 twist bones per limb segment
    # Film quality: 3+ twist bones with muscle simulation
    

---
  #### **Name**
Weight Painting Workflow
  #### **Description**
Systematic approach to skin weighting that avoids common pitfalls
  #### **When**
Binding mesh to skeleton
  #### **Example**
    # Professional weight painting workflow:
    
    # STEP 1: Pre-binding checklist
    # - All transforms frozen on joints (Maya) / Applied on armature (Blender)
    # - Mesh at world origin with clean transforms
    # - Joint orientations validated
    # - Character in bind pose (T-pose or A-pose)
    # - Mesh topology clean (no n-gons in deformation areas)
    
    # STEP 2: Initial bind
    # Maya: Smooth Bind with Max Influences = 4 (mobile) or 8 (PC)
    # Blender: Parent with Automatic Weights, then Limit Total = 4
    
    # STEP 3: Problem areas to check FIRST
    # 1. Shoulder/clavicle junction - check 90 degree arm raise
    # 2. Hip/pelvis junction - check leg spread and kick
    # 3. Spine twist - check 45 degree torso rotation
    # 4. Wrist rotation - check 180 degree forearm twist
    # 5. Knee/elbow at 90 degrees - check for volume loss
    
    # STEP 4: Weight painting rules
    # - Start with flood fill to establish base influence
    # - Use smooth brush at low intensity (0.1-0.2)
    # - ALWAYS work with Normalize on
    # - Never leave vertices with 0 total weight
    # - Check weights sum to 1.0 (normalization)
    
    # STEP 5: Iteration poses
    # Pose 1: Arms at 45 degrees (relaxed pose, most common)
    # Pose 2: Arms at 90 degrees (stress test shoulder)
    # Pose 3: Full arm twist (stress test forearm)
    # Pose 4: Deep knee bend (stress test hip/knee)
    # Pose 5: Spine twist + bend combo
    
    # Tools that save hours:
    # Maya: ngSkinTools (layer-based weights)
    # Blender: Mesh Data Transfer (copy weights from proxy mesh)
    # Both: Weight hammer to fix stray vertices
    

---
  #### **Name**
Control Rig Architecture
  #### **Description**
Build animator-friendly control rigs that are intuitive and non-destructive
  #### **When**
Creating production character rigs
  #### **Example**
    # Control rig hierarchy:
    #
    # Character_GRP
    # |-- CONTROLS_GRP (visible to animators)
    # |   |-- GLOBAL_CTRL (moves everything, world space)
    # |   |-- COG_CTRL (center of gravity, under global)
    # |   |-- BODY_CTRLS (spine, limbs, head)
    # |   |-- FACE_CTRLS (facial controls)
    # |   |-- SETTINGS (IK/FK switches, visibility)
    # |
    # |-- SKELETON_GRP (usually hidden)
    # |   |-- BIND_SKELETON (what mesh is bound to)
    # |   |-- DRIVER_SKELETON (controlled by rig)
    # |
    # |-- GEOMETRY_GRP (mesh, hidden in rig file)
    # |-- DO_NOT_TOUCH_GRP (constraints, nodes, systems)
    
    # Control shape conventions:
    # - Circles: Rotation controls (FK joints)
    # - Cubes/Boxes: Translation controls (IK targets)
    # - Arrows: Directional (foot roll, pole vectors)
    # - Diamonds: Attribute controls (blend, switches)
    # - Cross/Plus: Global or COG
    
    # Color coding (standard):
    # - Yellow: Center/spine controls
    # - Blue: Left side (L_)
    # - Red: Right side (R_)
    # - Green: Secondary/tweaks
    # - Purple: IK handles
    # - Cyan: FK controls
    
    # Control placement rules:
    # 1. Controls should be where animators expect them
    # 2. IK controls at the END of chains (wrist, ankle)
    # 3. FK controls at EACH joint in chain
    # 4. Pole vectors visible and snappable (knee, elbow)
    # 5. All controls should have predictable pivot points
    
    # Essential control features:
    # - Space switching (world/local/custom)
    # - IK/FK blending with matching
    # - Stretch on/off with volume preservation
    # - Bendy/ribbon controls for organic deformation
    # - Follow attributes (head follows body, hands follow)
    

---
  #### **Name**
FK/IK System Implementation
  #### **Description**
Build robust FK/IK systems with seamless switching and matching
  #### **When**
Creating limb rigs that need both control methods
  #### **Example**
    # FK vs IK decision guide:
    #
    # USE FK FOR:
    # - Overlapping action (follow-through)
    # - Swinging motions (arms walking)
    # - Swimming, flying
    # - Loose/relaxed poses
    # - Direct mocap input
    #
    # USE IK FOR:
    # - Planted contacts (feet on ground)
    # - Pushing/pulling (hands on objects)
    # - Climbing, hanging
    # - Precise endpoint control
    # - Maintaining contact during body movement
    
    # IK/FK Switch Architecture:
    #
    # Three skeleton chains:
    # 1. FK_chain - driven by FK controls
    # 2. IK_chain - driven by IK solver
    # 3. BIND_chain - constrained to blend between FK/IK
    #
    # BIND_chain joints are parentConstrained to both:
    # parentConstraint -mo FK_arm BIND_arm;
    # parentConstraint -mo IK_arm BIND_arm;
    #
    # IK_FK_Switch attribute (0=FK, 1=IK) drives constraint weights
    
    # FK to IK Matching (Maya):
    def fk_to_ik_match():
        # 1. Get FK chain world positions/rotations
        # 2. Snap IK handle to FK wrist position
        # 3. Calculate pole vector position from FK chain
        # 4. Snap pole vector to calculated position
        # 5. Switch to IK (set attribute to 1)
        pass
    
    # IK to FK Matching (Maya):
    def ik_to_fk_match():
        # 1. Get BIND chain world rotations
        # 2. Apply rotations to FK controls
        # 3. Switch to FK (set attribute to 0)
        pass
    
    # Pole vector placement:
    # Position should be on the plane defined by shoulder-elbow-wrist
    # Distance: ~1.5x the length of the upper arm segment
    # Direction: Perpendicular to limb, toward natural bend
    

---
  #### **Name**
Facial Rigging Strategy
  #### **Description**
Choose and implement the right facial deformation system
  #### **When**
Creating character facial rigs
  #### **Example**
    # Facial Deformation Methods Comparison:
    #
    # BLEND SHAPES (Morph Targets):
    # Pros:
    #   - Precise artist control
    #   - Perfect for stylized characters
    #   - Easy to art direct
    #   - No weight painting issues
    # Cons:
    #   - Memory heavy (full mesh per shape)
    #   - Hard to combine dynamically
    #   - No procedural adjustment
    #   - Lots of shapes needed (50-100+)
    #
    # JOINT-BASED:
    # Pros:
    #   - Light on memory
    #   - Good for mobile/performance
    #   - Easy to retarget
    #   - Works with engine systems
    # Cons:
    #   - Hard to get subtle deformation
    #   - Weight painting face is tedious
    #   - Limited expression range
    #
    # HYBRID (Recommended for games):
    # - Bones for broad movement (jaw, brows, cheeks)
    # - Blend shapes for specific expressions
    # - Corrective shapes for problem poses
    
    # Essential facial shapes (FACS-based):
    # Brows: Inner raise, outer raise, lower, squeeze
    # Eyes: Upper lid raise/lower, lower lid raise, squint, wide
    # Nose: Wrinkle, flare, sneer
    # Mouth: Open, wide, narrow, pucker, funnel, smile, frown
    # Jaw: Open, left, right, forward
    # Cheeks: Puff, suck, raise
    #
    # Typical counts:
    # Mobile game: 15-25 shapes
    # PC game: 40-60 shapes
    # AAA/Film: 100+ shapes with correctives
    
    # Jaw setup (hybrid approach):
    # 1. Jaw bone handles open/close rotation
    # 2. Blend shape handles lip seal (keeps lips together)
    # 3. Driven key: JawRotation drives LipSeal shape 0-1
    # 4. Secondary bones for lips can layer on top
    
    # Eye setup considerations:
    # - Eyelids should follow eyeball rotation
    # - Upper lid moves more than lower (70/30 split)
    # - Blink shape should work with any eye direction
    # - Cornea bulge blend shape for realistic eyes
    

---
  #### **Name**
Corrective Blend Shapes
  #### **Description**
Use pose-space deformation to fix problem areas that weights can't solve
  #### **When**
Dealing with volume loss, interpenetration, or complex deformation
  #### **Example**
    # Corrective shapes fix deformation at specific poses
    # They activate automatically based on joint rotations
    #
    # Common corrective targets:
    # - Shoulder at 90 degrees (deltoid collapse)
    # - Elbow at 90+ degrees (bicep/tricep)
    # - Hip at 90 degrees (glute flatten)
    # - Knee at 90+ degrees (quad/calf compression)
    # - Wrist flexion/extension (tendon visibility)
    
    # Maya workflow with Pose Space Deformation (PSD):
    # 1. Pose the joint to the problem position (e.g., shoulder 90)
    # 2. Duplicate the deformed mesh
    # 3. Sculpt the fix on the duplicate
    # 4. Create blend shape from sculpted to original
    # 5. Connect shape weight to joint rotation via driven key
    
    # Example driven key setup:
    # Shoulder rotation 0 degrees -> corrective shape 0.0
    # Shoulder rotation 45 degrees -> corrective shape 0.5
    # Shoulder rotation 90 degrees -> corrective shape 1.0
    # Use smooth interpolation (spline tangents)
    
    # Blender workflow with Shape Keys:
    # 1. Create shape key from basis at problem pose
    # 2. Apply armature modifier to see deformation
    # 3. Sculpt corrections on the shape key
    # 4. Add driver: Shape Key Value driven by bone rotation
    # 5. Use scripted expression for smooth falloff
    
    # Extraction workflow (cleaner method):
    # 1. Pose to problem position
    # 2. Duplicate mesh
    # 3. Remove skinning from duplicate
    # 4. Sculpt fixes with clean topology reference
    # 5. Create blend shape
    # 6. Invert the deformation so it corrects at pose
    
    # Performance note:
    # Each corrective shape = mesh data in memory
    # Limit to 10-20 correctives per character for real-time
    # Use helper bones where possible instead
    

---
  #### **Name**
Spine Deformation System
  #### **Description**
Create spine rigs that bend naturally without breaking
  #### **When**
Rigging humanoid or creature spines
  #### **Example**
    # Spine hierarchy (humanoid):
    #
    # Pelvis (root of spine, child of COG)
    # |-- Spine01 (lower back)
    # |   |-- Spine02 (mid back)
    # |       |-- Spine03 (upper back)
    # |           |-- Chest (ribcage)
    # |               |-- Neck01
    # |                   |-- Neck02
    # |                       |-- Head
    #
    # Minimum spine joints: 3 (mobile)
    # Recommended: 4-5 (good balance)
    # High detail: 6+ (film/cutscene)
    
    # FK spine with ribbon/spline IK overlay:
    # 1. FK controls at each spine joint (direct rotation)
    # 2. IK spline curve through spine for smooth arcs
    # 3. Blend between FK and spline IK per joint
    
    # Breathing setup:
    # - Scale Spine02/Spine03 slightly on breath attribute
    # - Scale should be Y-axis (vertical expansion)
    # - Subtle: 1.0 to 1.02 scale range
    # - Drive with sine wave for idle breathing
    
    # Twist distribution:
    # - Pelvis rotation should NOT twist spine
    # - Chest twist should distribute to Spine02/03
    # - Use aim constraints or twist extractors
    
    # Common spine problems and fixes:
    #
    # Problem: Spine joints collapse on side bend
    # Fix: Add volume preservation via scale compensation
    #      or corrective shapes at extreme bends
    #
    # Problem: Shoulders move with spine twist
    # Fix: Counter-rotate clavicles or add shoulder space
    #
    # Problem: Belly/chest interpenetration on bend
    # Fix: Lattice deformer or corrective shapes
    #
    # Problem: Hip bone twists unnaturally
    # Fix: Separate pelvis rotation from spine chain
    

---
  #### **Name**
Root Motion vs In-Place Animation
  #### **Description**
Understand and implement proper root motion systems for game engines
  #### **When**
Setting up character animation for gameplay
  #### **Example**
    # Root Motion: Character movement baked into animation
    # In-Place: Animation plays in place, code handles movement
    #
    # ROOT MOTION - Use when:
    # - Animation timing MUST match movement (footsteps)
    # - Complex locomotion (climbing, vaulting)
    # - Physics interactions (getting hit, stumbling)
    # - Cutscenes and mocap data
    #
    # IN-PLACE - Use when:
    # - Gameplay needs responsive controls
    # - Speed varies dynamically
    # - Network sync is critical (competitive games)
    # - Procedural movement (following splines)
    
    # Root bone setup:
    #
    # Required hierarchy:
    # Root (at world origin, this is your root motion bone)
    # |-- Pelvis (or Hips - the actual hip joint)
    #     |-- Spine...
    #     |-- L_Leg...
    #     |-- R_Leg...
    #
    # Root bone rules:
    # 1. MUST be at world origin in bind pose (0,0,0)
    # 2. Should have NO rotation in bind pose
    # 3. Sits on the ground plane (Y=0) typically
    # 4. Animation moves this bone for root motion
    
    # Unity root motion setup:
    # - Animator > Apply Root Motion = true
    # - Avatar must have correct Root Node assigned
    # - Call animator.deltaPosition in script for custom handling
    
    # Unreal root motion setup:
    # - Animation asset > Enable Root Motion = true
    # - Root Motion Mode = Root Motion from Everything
    # - Character Movement > Use Controller Desired Rotation
    
    # Extracting root motion in Maya:
    # 1. Bake animation to root joint
    # 2. Delete Y rotation if keeping feet on ground
    # 3. Verify root doesn't go through ground plane
    # 4. Export with "Bake Animation" enabled
    
    # Common root motion bugs:
    # - Character sliding (root motion not applied)
    # - Character teleporting (root in wrong location)
    # - Feet sliding (animation/movement speed mismatch)
    # - Rotation snapping (root rotation not smooth)
    

---
  #### **Name**
Animation Retargeting Setup
  #### **Description**
Create rigs that retarget animation cleanly to different proportions
  #### **When**
Building characters that share animation sets or use mocap
  #### **Example**
    # Retargeting requirements:
    #
    # 1. Consistent naming convention across all characters
    #    - "Spine", "Spine1", "Spine2" not "Back", "Torso", "Chest"
    #    - "LeftArm", "LeftForeArm" not "L_Arm", "L_Elbow"
    #
    # 2. Identical hierarchy structure
    #    - Same joint count in chains
    #    - Same parent-child relationships
    #    - Same joint order
    #
    # 3. Matching joint orientations
    #    - All characters X-axis down bone
    #    - All characters Y-axis same direction
    #    - This is the #1 retargeting failure cause
    #
    # 4. Similar bind pose
    #    - A-pose or T-pose
    #    - Consistent across characters
    #    - Finger spread matters!
    
    # Unity Humanoid retargeting:
    # 1. Set Rig type to "Humanoid"
    # 2. Configure Avatar - map bones to Unity's humanoid
    # 3. Required bones: Hips, Spine, Head, Arms, Legs
    # 4. Optional: Fingers, toes, extra spine joints
    #
    # Muscle limits (must configure):
    # - Shoulder range of motion
    # - Spine twist limits
    # - Neck limits
    # These prevent hyperextension on retarget
    
    # Unreal retargeting:
    # 1. Create IK Rig for source skeleton
    # 2. Create IK Rig for target skeleton
    # 3. Create IK Retargeter asset
    # 4. Map chains: Spine, Arms, Legs, Head
    # 5. Adjust bone mapping for mismatches
    
    # Proportion adjustment strategies:
    # - Long arms → reduce arm FK influence or scale keys
    # - Short legs → foot IK with ground contact
    # - Different spine length → interpolate extra joints
    #
    # What doesn't retarget well:
    # - Facial animation (use blend shapes directly)
    # - Finger animation (too proportion-sensitive)
    # - Props and contacts (need manual adjustment)
    # - Clothing/hair simulation (recalculate)
    

---
  #### **Name**
Additive Animation Layers
  #### **Description**
Implement layered animation systems for procedural and blended effects
  #### **When**
Adding breathing, hit reactions, or procedural motion to base animations
  #### **Example**
    # Additive animations add ON TOP of base animation
    # Base pose + Additive delta = Final pose
    #
    # Common additive uses:
    # - Breathing (chest expansion)
    # - Look-at/head tracking
    # - Weapon recoil
    # - Damage reactions (hit flinches)
    # - Tiredness/fatigue overlay
    # - Emotional states
    
    # Creating additive animations:
    #
    # Method 1: Reference pose subtraction
    # 1. Create "Reference Pose" (usually T-pose or idle)
    # 2. Create full animation (e.g., breathing idle)
    # 3. Engine subtracts reference from animation
    # 4. Result: Only the DIFFERENCE is stored
    #
    # Method 2: Artist creates deltas directly
    # 1. Start from bind pose (all zeroed)
    # 2. Animate ONLY what should change
    # 3. Mark as additive in engine
    
    # Unity additive setup:
    # 1. Animation clip > Additive Reference Pose = true
    # 2. Create Animator layer with Blending = Additive
    # 3. Set layer weight (0-1) for intensity
    # 4. Avatar Mask to limit affected bones
    
    # Unreal additive setup:
    # 1. AnimSequence > Additive Settings > Additive Anim Type
    # 2. Choose Mesh Space or Local Space additive
    # 3. Set Base Pose Type (usually Reference Pose)
    # 4. Use Layered Blend Per Bone in AnimGraph
    
    # Avatar Masks (critical for additives):
    # - Upper body mask for weapon handling
    # - Spine-only mask for breathing
    # - Head mask for look-at
    # Without masks, additives affect entire body
    
    # Common additive problems:
    # - Joints hyperextending (clamp rotation in blend)
    # - Additive + additive compounding (use maximum, not sum)
    # - Wrong reference pose (causes drift)
    # - Mesh space vs local space confusion
    

## Anti-Patterns


---
  #### **Name**
Non-zeroed Transforms
  #### **Description**
Binding mesh to skeleton without freezing transforms
  #### **Why**
Export will bake in offsets. Different DCCs interpret transforms differently. FBX will have "ghost" transforms. Animations will be offset.
  #### **Instead**
Always Freeze Transforms (Maya) or Apply All Transforms (Blender) on both skeleton and mesh before binding. The bind pose should show all zeros in channel box.

---
  #### **Name**
Binding in Wrong Pose
  #### **Description**
Binding mesh when character is in animation pose instead of bind pose
  #### **Why**
Weight painting assumes bind pose. Deformation will be wrong at rest. Can't share animation with other characters. Export breaks.
  #### **Instead**
Always return to T-pose or A-pose before binding. Create a "bind pose" button/script that resets skeleton. Verify pose before every bind.

---
  #### **Name**
Single Influence Joints
  #### **Description**
Joints that only one vertex is weighted to, or very low influence
  #### **Why**
Single vertices create hard edges in deformation. Low influences get culled on export. Creates popping artifacts.
  #### **Instead**
Ensure minimum 3-4 vertices per joint influence. Use weight hammer to smooth isolated weights. Remove joints that don't contribute.

---
  #### **Name**
Weight Islands
  #### **Description**
Groups of vertices with weights disconnected from their neighbors
  #### **Why**
Creates tears in mesh during deformation. Often invisible until animation plays. Very hard to debug.
  #### **Instead**
Use "Select Influenced" to visualize per-joint weights. Smooth weights at boundaries. Use topology-aware weight transfer.

---
  #### **Name**
Joint Limits in DCC
  #### **Description**
Relying on joint limits set in Maya/Blender for runtime
  #### **Why**
Most game engines ignore DCC joint limits completely. Maya IK joint limits export but don't constrain. Behavior differs between DCCs.
  #### **Instead**
Implement limits in engine (Unity Constraints, Unreal Control Rig). Or use post-process in animation system. Never rely on DCC limits for runtime.

---
  #### **Name**
Excessive Bone Count
  #### **Description**
Creating detailed skeleton without considering target platform
  #### **Why**
Mobile GPUs have hard bone limits (often 75 per draw call). Each bone costs CPU for transform updates. Skinning cost scales with bone count.
  #### **Instead**
Mobile characters 30-50 bones. PC characters 75-120 bones. Split mesh by bone count for LOD. Use bone LOD systems.

---
  #### **Name**
Floating Root Bone
  #### **Description**
Root bone not at world origin or floating in space
  #### **Why**
Root motion calculations assume origin. Retargeting breaks with offset roots. Export may compound transforms wrong.
  #### **Instead**
Root bone at (0,0,0) with no rotation. Place at ground level. Only move root for root motion data.

---
  #### **Name**
Inconsistent Joint Orientations
  #### **Description**
Joint X-axis pointing random directions, orientations not mirrored properly
  #### **Why**
Animation retargeting fails. Mirror animation fails. IK solving becomes unpredictable. Rotation interpolation glitches.
  #### **Instead**
X-axis always aims down bone. Y-axis consistent (pick forward or up, stick with it). Mirror orientations properly for symmetry.

---
  #### **Name**
Skinning Before Rig Completion
  #### **Description**
Weight painting before the skeleton hierarchy is finalized
  #### **Why**
Adding/removing joints invalidates weight data. Reparenting joints changes weight behavior. Multiple rebind cycles waste days.
  #### **Instead**
Complete skeleton hierarchy first. Add ALL helper and twist bones. Test full range of motion with proxy geo. THEN bind final mesh.

---
  #### **Name**
Over-relying on Corrective Shapes
  #### **Description**
Using corrective blend shapes for problems that proper weights would solve
  #### **Why**
Correctives cost memory and performance. Hard to maintain across LODs. Don't retarget. Compound complexity.
  #### **Instead**
Fix weight painting first. Add helper bones second. Use correctives only for impossible deformation (shoulder at 180 degrees).