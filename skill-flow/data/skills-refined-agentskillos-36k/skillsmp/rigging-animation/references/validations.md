# Rigging Animation - Validations

## Hardcoded Joint Names

### **Id**
rig-maya-hardcoded-joint-names
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - cmds\.joint\([^)]*name\s*=\s*["'](?!.*{)[^"']+["']
  - pm\.joint\([^)]*name\s*=\s*["'](?!.*{)[^"']+["']
### **Message**
Hardcoded joint names make rigs inflexible. Use naming convention variables or template strings.
### **Fix Action**
Create naming convention constants: SIDE_PREFIX, JOINT_SUFFIX, etc. Use f-strings or format().
### **Applies To**
  - *.py
  - *.mel

## Bind Skin Without Max Influences

### **Id**
rig-maya-bind-without-max-influences
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - skinCluster\([^)]*(?!.*maximumInfluences)[^)]*\)
  - bindSkin\([^)]*(?!.*tsb)[^)]*\)
### **Message**
Binding without max influences limit may exceed engine bone limits. Mobile: 4, PC: 8 max.
### **Fix Action**
Add maximumInfluences=4 parameter for mobile, maximumInfluences=8 for PC targets.
### **Applies To**
  - *.py
  - *.mel

## Joint Orient Check Missing

### **Id**
rig-maya-joint-orient-not-zeroed
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - makeIdentity\([^)]*apply\s*=\s*(?:True|1)[^)]*\)(?![\s\S]*?jointOrient)
### **Message**
Freezing transforms without checking joint orient may cause animation issues.
### **Fix Action**
After freezeTransformations, verify jointOrient values are as expected for the rig.
### **Applies To**
  - *.py
  - *.mel

## Parent Constraint Without Maintain Offset

### **Id**
rig-maya-parent-constraint-no-maintain-offset
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - parentConstraint\([^)]*(?!.*mo=|.*maintainOffset)[^)]*\)
### **Message**
Parent constraint without maintainOffset can cause unexpected snapping.
### **Fix Action**
Add mo=True or maintainOffset=True to preserve relative positioning.
### **Applies To**
  - *.py
  - *.mel

## IK Handle Without Solver Specification

### **Id**
rig-maya-ikhandle-no-solver-type
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ikHandle\([^)]*(?!.*solver|.*sol)[^)]*\)
### **Message**
IK handle without explicit solver type may default unexpectedly (SC vs RP).
### **Fix Action**
Specify solver='ikRPsolver' for limbs or solver='ikSCsolver' for simple chains.
### **Applies To**
  - *.py
  - *.mel

## Bone Roll Not Explicitly Set

### **Id**
rig-blender-bone-roll-not-set
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - edit_bones\.new\([^)]*\)(?![\s\S]{0,100}\.roll\s*=)
### **Message**
Bone created without setting roll. Inconsistent rolls cause IK and retargeting issues.
### **Fix Action**
Set bone.roll explicitly after creation. Use bpy.ops.armature.calculate_roll() for consistency.
### **Applies To**
  - *.py

## Bone Constraint Missing Subtarget

### **Id**
rig-blender-constraint-no-subtarget
### **Severity**
error
### **Type**
regex
### **Pattern**
  - constraints\.new\([^)]*(?:'COPY_|'IK'|'DAMPED_TRACK')[^)]*\)[\s\S]{0,200}(?!.*subtarget)
### **Message**
Bone constraint without subtarget will likely fail. Target bone not specified.
### **Fix Action**
Set constraint.subtarget = 'bone_name' after adding the constraint.
### **Applies To**
  - *.py

## Using Only Automatic Weights

### **Id**
rig-blender-auto-weights-only
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - bpy\.ops\.object\.parent_set\([^)]*type\s*=\s*['"]ARMATURE_AUTO['"]
### **Message**
Automatic weights alone often need cleanup. Add weight normalization and limit total.
### **Fix Action**
Follow up with bpy.ops.object.vertex_group_limit_total(limit=4) and clean weights.
### **Applies To**
  - *.py

## Armature Scale Not Applied

### **Id**
rig-blender-armature-scale-not-applied
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - bpy\.data\.armatures\.new\([^)]*\)(?![\s\S]{0,500}bpy\.ops\.object\.transform_apply)
### **Message**
Armature created without applying transforms. Scale issues will cause export problems.
### **Fix Action**
After armature creation, use bpy.ops.object.transform_apply(location=True, rotation=True, scale=True).
### **Applies To**
  - *.py

## HumanBodyBones Magic String Usage

### **Id**
rig-unity-animator-getbone-magic-string
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - GetBoneTransform\([^)]*HumanBodyBones\.\w+
### **Message**
Using HumanBodyBones directly. Consider caching bone transforms for performance.
### **Fix Action**
Cache bone transforms in Awake() instead of calling GetBoneTransform every frame.
### **Applies To**
  - *.cs

## Animation Rigging Without Weight Control

### **Id**
rig-unity-animation-rigging-no-weight
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - TwoBoneIKConstraint|MultiAimConstraint|DampedTransform
### **Message**
Animation Rigging constraint detected. Ensure weight property is exposed for blending.
### **Fix Action**
Add [Range(0,1)] public float constraintWeight and control via RigBuilder.layers.
### **Applies To**
  - *.cs

## Root Motion Without Delta Check

### **Id**
rig-unity-root-motion-direct-access
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - animator\.rootPosition|animator\.rootRotation(?![\s\S]{0,50}delta)
### **Message**
Accessing root position/rotation directly. Consider using deltaPosition/deltaRotation for movement.
### **Fix Action**
Use animator.deltaPosition and animator.deltaRotation for frame-based root motion.
### **Applies To**
  - *.cs

## Avatar Mask Without Null Check

### **Id**
rig-unity-avatar-mask-null-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \.avatarMask\s*=\s*\w+(?![\s\S]{0,50}null)
### **Message**
Setting avatar mask without null check. Missing masks cause layer to affect all bones.
### **Fix Action**
Add null check: if (mask != null) layer.avatarMask = mask;
### **Applies To**
  - *.cs

## IK Weight Not Animated

### **Id**
rig-unity-ik-no-weight
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - SetIKPositionWeight\([^,]+,\s*1(?:\.0)?f?\s*\)
  - SetIKRotationWeight\([^,]+,\s*1(?:\.0)?f?\s*\)
### **Message**
IK weight set to 1 without transition. This causes snapping. Lerp weights for smooth IK.
### **Fix Action**
Lerp IK weight over time: ikWeight = Mathf.Lerp(ikWeight, targetWeight, Time.deltaTime * speed);
### **Applies To**
  - *.cs

## Skeletal Mesh Without LOD Setup

### **Id**
rig-unreal-skeletal-mesh-no-lod
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - USkeletalMesh\*(?![\s\S]{0,200}LOD|GetNumLODs)
### **Message**
Skeletal mesh referenced without LOD consideration. Performance issue on complex characters.
### **Fix Action**
Implement LOD switching. Use GetNumLODs() and SetForcedLOD() for distance-based quality.
### **Applies To**
  - *.cpp
  - *.h

## Unsafe Animation Instance Cast

### **Id**
rig-unreal-animation-instance-cast
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - Cast<U\w*AnimInstance>\s*\([^)]*GetAnimInstance\(\)
### **Message**
Direct cast of AnimInstance may return null. Check before using.
### **Fix Action**
Use if (UMyAnimInstance* Anim = Cast<UMyAnimInstance>(Mesh->GetAnimInstance())) { ... }
### **Applies To**
  - *.cpp

## Control Rig Element Without Weight

### **Id**
rig-unreal-control-rig-no-weight
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - FRigUnit_\w+(?![\s\S]{0,100}Weight)
### **Message**
Control Rig unit detected. Ensure Weight parameter is exposed for blending.
### **Fix Action**
Add UPROPERTY Weight float to rig unit and use for procedural blending.
### **Applies To**
  - *.cpp
  - *.h

## FBX Export Without Animation Bake

### **Id**
rig-fbx-python-no-bake
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - FBXExport[^;]*(?!.*[Bb]ake)
  - export_scene_fbx\([^)]*(?!.*bake_anim)
### **Message**
FBX export without baking may not include all animation data correctly.
### **Fix Action**
Enable bake_anim=True in Blender, or 'Bake Animation' in Maya FBX export settings.
### **Applies To**
  - *.py
  - *.mel

## Magic Numbers for Bone Limits

### **Id**
rig-script-magic-bone-numbers
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - bone.*(?:count|limit|max)\s*[=<>]\s*(?:75|128|256|4|8)\b
  - influence.*(?:count|limit|max)\s*[=<>]\s*[0-9]+
### **Message**
Magic numbers for bone/influence limits. Define constants for platform targets.
### **Fix Action**
Create constants: MOBILE_MAX_BONES = 75, PC_MAX_BONES = 128, MOBILE_INFLUENCES = 4
### **Applies To**
  - *.py
  - *.cs
  - *.cpp

## Hardcoded Twist Percentages

### **Id**
rig-script-twist-hardcoded-percentage
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - twist.*(?:weight|influence|factor)\s*=\s*0\.[0-9]+
### **Message**
Hardcoded twist bone percentages. Make configurable for different character proportions.
### **Fix Action**
Create twist_distribution list or calculate based on bone chain position.
### **Applies To**
  - *.py
  - *.cs
  - *.cpp

## Weight Assignment Without Normalization

### **Id**
rig-script-weight-no-normalize
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - setAttr.*\.weightList|vertex_group.*add\([^)]*\)(?![\s\S]{0,200}normaliz)
### **Message**
Weight assignment without normalization step. Weights may not sum to 1.0.
### **Fix Action**
After weight changes, call normalize weights function or verify total = 1.0 per vertex.
### **Applies To**
  - *.py
  - *.mel

## Joint Creation in Loop Without Hierarchy Check

### **Id**
rig-script-joint-creation-loop
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for.*:[\s\S]{0,50}(?:joint\(|edit_bones\.new|AddBone)(?![\s\S]{0,100}parent)
### **Message**
Creating joints in loop without explicit parent assignment. Hierarchy may be wrong.
### **Fix Action**
Explicitly set parent joint/bone after creation in loop. Don't rely on selection.
### **Applies To**
  - *.py
  - *.mel

## IK Chain Length Not Validated

### **Id**
rig-script-ik-chain-length
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ikHandle|TwoBoneIK|FABRIK(?![\s\S]{0,200}(?:chain.*length|joint.*count|bone.*count))
### **Message**
IK chain created without validating joint count. Wrong chain length causes solve failures.
### **Fix Action**
Validate chain has expected joint count before creating IK. Log warning if mismatch.
### **Applies To**
  - *.py
  - *.cs
  - *.cpp

## Loop Animation Endpoint Mismatch Risk

### **Id**
rig-animation-loop-endpoint
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - loop.*anim|cycl.*anim|WrapMode\.Loop
### **Message**
Looping animation detected. Verify first and last keyframes match for seamless loop.
### **Fix Action**
Check that frame 0 and final frame have identical bone transforms. Use 'paste flipped' for walk cycles.
### **Applies To**
  - *.py
  - *.cs
  - *.cpp

## Additive Animation Without Reference Pose

### **Id**
rig-additive-no-reference
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - additive|AdditiveReferencePose|AnimationType\.Additive
### **Message**
Additive animation setup. Verify reference pose is correctly set or deltas will be wrong.
### **Fix Action**
Set reference pose to T-pose or idle base. Test additive at 100% to verify delta looks correct.
### **Applies To**
  - *.py
  - *.cs
  - *.cpp
  - *.asset

## Root Motion Loop May Drift

### **Id**
rig-root-motion-loop-drift
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - root.*motion.*loop|EnableRootMotion.*true[\s\S]{0,200}loop
### **Message**
Root motion with looping animation. Verify root returns to origin at loop point.
### **Fix Action**
At final frame, root position delta should equal 0. Extract and verify root motion curve endpoint.
### **Applies To**
  - *.py
  - *.cs
  - *.cpp