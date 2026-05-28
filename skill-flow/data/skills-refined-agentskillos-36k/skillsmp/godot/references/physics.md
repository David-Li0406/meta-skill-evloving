# Godot - Physics

**Pages:** 29

---

## Physics — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/physics/index.html

**Contents:**
- Physics

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Using NavigationLayers — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationlayers.html

**Contents:**
- Using NavigationLayers
- User-contributed notes

NavigationLayers are an optional feature to further control which navigation meshes are considered in a path query. They work similar to how physics layers control collision between collision objects or how visual layers control what is rendered to the Viewport.

NavigationLayers can be named in the ProjectSettings the same as physics layers or visual layers.

If a region has not a single compatible navigation layer with the navigation_layers parameter of a path query this regions navigation mesh will be skipped in pathfinding. See Using NavigationPaths for more information on querying the NavigationServer for paths.

NavigationLayers are a single int value that is used as a bitmask. Many navigation related nodes have set_navigation_layer_value() and get_navigation_layer_value() functions to set and get a layer number directly without the need for more complex bitwise operations.

In scripts the following helper functions can be used to work with the navigation_layers bitmask.

Changing navigation layers for path queries is a performance friendly alternative to enabling / disabling entire navigation regions. Compared to region changes a navigation path query with different navigation layers does not trigger large scale updates on the NavigationServer.

Changing the navigation layers of NavigationAgent nodes will have an immediate effect on the next path query. Changing the navigation layers of regions will have an effect after the next NavigationServer sync.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (swift):
```swift
func change_layers():
    var region: NavigationRegion2D = get_node("NavigationRegion2D")
    # enables 4-th layer for this region
    region.navigation_layers = enable_bitmask_inx(region.navigation_layers, 4)
    # disables 1-rst layer for this region
    region.navigation_layers = disable_bitmask_inx(region.navigation_layers, 1)

    var agent: NavigationAgent2D = get_node("NavigationAgent2D")
    # make future path queries of this agent ignore regions with 4-th layer
    agent.navigation_layers = disable_bitmask_inx(agent.navigation_layers, 4)

    var path_query_navigation_layers: int = 0
    path_query_navigation_layers = enable_bitmask_inx(path_query_navigation_layers, 2)
    # get a path that only considers 2-nd layer regions
    var path: PackedVector2Array = NavigationServer2D.map_get_path(
        map,
        start_position,
        target_position,
        true,
        path_query_navigation_layers
        )

static func is_bitmask_inx_enabled(_bitmask: int, _index: int) -> bool:
    return _bitmask & (1 << _index) != 0

static func enable_bitmask_inx(_bitmask: int, _index: int) -> int:
    return _bitmask | (1 << _index)

static func disable_bitmask_inx(_bitmask: int, _index: int) -> int:
    return _bitmask & ~(1 << _index)
```

Example 2 (csharp):
```csharp
using Godot;

public partial class MyNode2D : Node2D
{
    private Rid _map;
    private Vector2 _startPosition;
    private Vector2 _targetPosition;

    private void ChangeLayers()
    {
        NavigationRegion2D region = GetNode<NavigationRegion2D>("NavigationRegion2D");
        // Enables the 4th layer for this region.
        region.NavigationLayers = EnableBitmaskInx(region.NavigationLayers, 4);
        // Disables the 1st layer for this region.
        region.NavigationLayers = DisableBitmaskInx(region.NavigationLayers, 1);

        NavigationAgent2D agent = GetNode<NavigationAgent2D>("NavigationAgent2D");
        // Make future path queries of this agent ignore regions with the 4th layer.
        agent.NavigationLayers = DisableBitmaskInx(agent.NavigationLayers, 4);

        uint pathQueryNavigationLayers = 0;
        pathQueryNavigationLayers = EnableBitmaskInx(pathQueryNavigationLayers, 2);
        // Get a path that only considers 2nd layer regions.
        Vector2[] path = NavigationServer2D.MapGetPath(
            _map,
            _startPosition,
            _targetPosition,
            true,
            pathQueryNavigationLayers
        );
    }

    private static bool IsBitmaskInxEnabled(uint bitmask, int index)
    {
        return (bitmask & (1 << index)) != 0;
    }

    private static uint EnableBitmaskInx(uint bitmask, int index)
    {
        return bitmask | (1u << index);
    }

    private static uint DisableBitmaskInx(uint bitmask, int index)
    {
        return bitmask & ~(1u << index);
    }
}
```

Example 3 (swift):
```swift
func change_layers():
    var region: NavigationRegion3D = get_node("NavigationRegion3D")
    # enables 4-th layer for this region
    region.navigation_layers = enable_bitmask_inx(region.navigation_layers, 4)
    # disables 1-rst layer for this region
    region.navigation_layers = disable_bitmask_inx(region.navigation_layers, 1)

    var agent: NavigationAgent3D = get_node("NavigationAgent3D")
    # make future path queries of this agent ignore regions with 4-th layer
    agent.navigation_layers = disable_bitmask_inx(agent.navigation_layers, 4)

    var path_query_navigation_layers: int = 0
    path_query_navigation_layers = enable_bitmask_inx(path_query_navigation_layers, 2)
    # get a path that only considers 2-nd layer regions
    var path: PackedVector3Array = NavigationServer3D.map_get_path(
        map,
        start_position,
        target_position,
        true,
        path_query_navigation_layers
        )

static func is_bitmask_inx_enabled(_bitmask: int, _index: int) -> bool:
    return _bitmask & (1 << _index) != 0

static func enable_bitmask_inx(_bitmask: int, _index: int) -> int:
    return _bitmask | (1 << _index)

static func disable_bitmask_inx(_bitmask: int, _index: int) -> int:
    return _bitmask & ~(1 << _index)
```

Example 4 (csharp):
```csharp
using Godot;

public partial class MyNode3D : Node3D
{
    private Rid _map;
    private Vector3 _startPosition;
    private Vector3 _targetPosition;

    private void ChangeLayers()
    {
        NavigationRegion3D region = GetNode<NavigationRegion3D>("NavigationRegion3D");
        // Enables the 4th layer for this region.
        region.NavigationLayers = EnableBitmaskInx(region.NavigationLayers, 4);
        // Disables the 1st layer for this region.
        region.NavigationLayers = DisableBitmaskInx(region.NavigationLayers, 1);

        NavigationAgent3D agent = GetNode<NavigationAgent3D>("NavigationAgent2D");
        // Make future path queries of this agent ignore regions with the 4th layer.
        agent.NavigationLayers = DisableBitmaskInx(agent.NavigationLayers, 4);

        uint pathQueryNavigationLayers = 0;
        pathQueryNavigationLayers = EnableBitmaskInx(pathQueryNavigationLayers, 2);
        // Get a path that only considers 2nd layer regions.
        Vector3[] path = NavigationServer3D.MapGetPath(
            _map,
            _startPosition,
            _targetPosition,
            true,
            pathQueryNavigationLayers
        );
    }

    private static bool IsBitmaskInxEnabled(uint bitmask, int index)
    {
        return (bitmask & (1 << index)) != 0;
    }

    private static uint EnableBitmaskInx(uint bitmask, int index)
    {
        return bitmask | (1u << index);
    }

    private static uint DisableBitmaskInx(uint bitmask, int index)
    {
        return bitmask & ~(1u << index);
    }
}
```

---

## Using RigidBody — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/physics/rigid_body.html

**Contents:**
- Using RigidBody
- What is a rigid body?
- How to control a rigid body
- The "look at" method
- User-contributed notes

A rigid body is one that is directly controlled by the physics engine in order to simulate the behavior of physical objects. In order to define the shape of the body, it must have one or more Shape3D objects assigned. Note that setting the position of these shapes will affect the body's center of mass.

A rigid body's behavior can be altered by setting its properties, such as mass and weight. A physics material needs to be added to the rigid body to adjust its friction and bounce, and set if it's absorbent and/or rough. These properties can be set in the Inspector or via code. See RigidBody3D and PhysicsMaterial for the full list of properties and their effects.

There are several ways to control a rigid body's movement, depending on your desired application.

If you only need to place a rigid body once, for example to set its initial location, you can use the methods provided by the Node3D node, such as set_global_transform() or look_at(). However, these methods cannot be called every frame or the physics engine will not be able to correctly simulate the body's state. As an example, consider a rigid body that you want to rotate so that it points towards another object. A common mistake when implementing this kind of behavior is to use look_at() every frame, which breaks the physics simulation. Below, we'll demonstrate how to implement this correctly.

The fact that you can't use set_global_transform() or look_at() methods doesn't mean that you can't have full control of a rigid body. Instead, you can control it by using the _integrate_forces() callback. In this method, you can add forces, apply impulses, or set the velocity in order to achieve any movement you desire.

As described above, using the Node3D's look_at() method can't be used each frame to follow a target. Here is a custom look_at() method called look_follow() that will work with rigid bodies:

This method uses the rigid body's angular_velocity property to rotate the body. The axis to rotate around is given by the cross product between the current forward direction and the direction one wants to look in. The clamp is a simple method used to prevent the amount of rotation from going past the direction which is wanted to be looked in, as the total amount of rotation needed is given by the arccosine of the dot product. This method can be used with axis_lock_angular_* as well. If more precise control is needed, solutions such as ones relying on Quaternion may be required, as discussed in Using 3D transforms.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends RigidBody3D

var speed: float = 0.1

func look_follow(state: PhysicsDirectBodyState3D, current_transform: Transform3D, target_position: Vector3) -> void:
    var forward_local_axis: Vector3 = Vector3(1, 0, 0)
    var forward_dir: Vector3 = (current_transform.basis * forward_local_axis).normalized()
    var target_dir: Vector3 = (target_position - current_transform.origin).normalized()
    var local_speed: float = clampf(speed, 0, acos(forward_dir.dot(target_dir)))
    if forward_dir.dot(target_dir) > 1e-4:
        state.angular_velocity = local_speed * forward_dir.cross(target_dir) / state.step

func _integrate_forces(state):
    var target_position = $my_target_node3d_node.global_transform.origin
    look_follow(state, global_transform, target_position)
```

Example 2 (swift):
```swift
using Godot;

public partial class MyRigidBody3D : RigidBody3D
{
    private float _speed = 0.1f;
    private void LookFollow(PhysicsDirectBodyState3D state, Transform3D currentTransform, Vector3 targetPosition)
    {
        Vector3 forwardLocalAxis = new Vector3(1, 0, 0);
        Vector3 forwardDir = (currentTransform.Basis * forwardLocalAxis).Normalized();
        Vector3 targetDir = (targetPosition - currentTransform.Origin).Normalized();
        float localSpeed = Mathf.Clamp(_speed, 0.0f, Mathf.Acos(forwardDir.Dot(targetDir)));
        if (forwardDir.Dot(targetDir) > 1e-4)
        {
            state.AngularVelocity = forwardDir.Cross(targetDir) * localSpeed / state.Step;
        }
    }

    public override void _IntegrateForces(PhysicsDirectBodyState3D state)
    {
        Vector3 targetPosition = GetNode<Node3D>("MyTargetNode3DNode").GlobalTransform.Origin;
        LookFollow(state, GlobalTransform, targetPosition);
    }
}
```

---

## Using Jolt Physics — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/physics/using_jolt_physics.html

**Contents:**
- Using Jolt Physics
- Introduction
- Notable differences to Godot Physics
  - Joint properties
  - Single-body joints
  - Collision margins
  - Baumgarte stabilization
  - Ghost collisions
  - Memory usage
  - Ray-cast face index

The Jolt physics engine was added as an alternative to the existing Godot Physics physics engine in 4.4. Jolt is developed by Jorrit Rouwe with a focus on games and VR applications. Previously it was available as an extension but is now built into Godot.

It is important to note that the built-in Jolt Physics module is considered not finished, experimental, and lacks feature parity with both Godot Physics and the Godot Jolt extension. Behavior may change as it is developed further. Please keep that in mind when choosing what to use for your project.

The existing extension is now considered in maintenance mode. That means bug fixes will be merged, and it will be kept compatible with new versions of Godot until the built-in module has feature parity with the extension. The extension can be found here on GitHub and in Godot's asset library.

To change the 3D physics engine to be Jolt Physics, set Project Settings > Physics > 3D > Physics Engine to Jolt Physics. Once you've done that, click the Save & Restart button. When the editor opens again, 3D scenes should now be using Jolt for physics.

There are many differences between the existing Godot Physics engine and Jolt.

The current interfaces for the 3D joint nodes don't quite line up with the interface of Jolt's own joints. As such, there are a number of joint properties that are not supported, mainly ones related to configuring the joint's soft limits.

The unsupported properties are:

PinJoint3D: bias, damping, impulse_clamp

HingeJoint3D: bias, softness, relaxation

SliderJoint3D: angular_\*, \*_limit/softness, \*_limit/restitution, \*_limit/damping

ConeTwistJoint3D: bias, relaxation, softness

Generic6DOFJoint3D: *_limit_*/softness, *_limit_*/restitution, *_limit_*/damping, *_limit_*/erp

Currently a warning is emitted if you set these properties to anything but their default values.

You can, in Godot, omit one of the joint bodies for a two-body joint and effectively have "the world" be the other body. However, the node path that you assign your body to (node_a vs node_b) is ignored. Godot Physics will always behave as if you assigned it to node_a, and since node_a is also what defines the frame of reference for the joint limits, you end up with inverted limits and a potentially strange limit shape, especially if your limits allow both linear and angular degrees of freedom.

Jolt will behave as if you assigned the body to node_b instead, with node_a representing "the world". There is a project setting called Physics > Jolt Physics 3D > Joints > World Node that lets you toggle this behavior, if you need compatibility for an existing project.

Jolt (and other similar physics engines) uses something that Jolt refers to as "convex radius" to help improve the performance and behavior of the types of collision detection that Jolt relies on for convex shapes. Other physics engines (Godot included) might refer to these as "collision margins" instead. Godot exposes these as the margin property on every Shape3D-derived class, but Godot Physics itself does not use them for anything.

What these collision margins sometimes do in other engines (as described in Godot's documentation) is effectively add a "shell" around the shape, slightly increasing its size while also rounding off any edges/corners. In Jolt however, these margins are first used to shrink the shape, and then the "shell" is applied, resulting in edges/corners being similarly rounded off, but without increasing the size of the shape.

To prevent having to tweak this margin property manually, since its default value can be problematic for smaller shapes, the Jolt module exposes a project setting called Physics > Jolt Physics 3D > Collisions > Collision Margin Fraction which is multiplied with the smallest axis of the shape's AABB to calculate the actual margin. The margin property of the shape is then instead used as an upper bound.

These margins should, for most use-cases, be more or less transparent, but can sometimes result in odd collision normals when performing shape queries. You can lower the above mentioned project setting to mitigate some of this, including setting it to 0.0, but too small of a margin can also cause odd collision results, so is generally not recommended.

Baumgarte stabilization is a method to resolve penetrating bodies and push them to a state where they are just touching. In Godot Physics this works like a spring. This means that bodies can accelerate and may cause the bodies to overshoot and separate completely. With Jolt, the stabilization is only applied to the position and not to the velocity of the body. This means it cannot overshoot but it may take longer to resolve the penetration.

The strength of this stabilization can be tweaked using the project setting Physics > Jolt Physics 3D > Simulation > Baumgarte Stabilization Factor. Setting this project setting to 0.0 will turn Baumgarte stabilization off. Setting it to 1.0 will resolve penetration in 1 simulation step. This is fast but often also unstable.

Jolt employs two techniques to mitigate ghost collisions, meaning collisions with internal edges of shapes/bodies that result in collision normals that oppose the direction of movement.

The first technique, called "active edge detection", marks edges of triangles in ConcavePolygonShape3D or HeightMapShape3D as either "active" or "inactive", based on the angle to the neighboring triangle. When a collision happens with an inactive edge the collision normal will be replaced with the triangle's normal instead, to lessen the effect of ghost collisions.

The angle threshold for this active edge detection is configurable through the project setting Physics >Jolt Physics 3D > Collisions > Active Edge Threshold.

The second technique, called "enhanced internal edge removal", instead adds runtime checks to detect whether an edge is active or inactive, based on the contact points of the two bodies. This has the benefit of applying not only to collisions with ConcavePolygonShape3D and HeightMapShape3D, but also edges between any shapes within the same body.

Enhanced internal edge removal can be toggled on and off for the various contexts to which it's applied, using the Physics >Jolt Physics 3D > Simulation > Use Enhanced Internal Edge Removal, project setting, and the similar settings for queries and motion queries.

Note that neither the active edge detection nor enhanced internal edge removal apply when dealing with ghost collisions between two different bodies.

Jolt uses a stack allocator for temporary allocations within its simulation step. This stack allocator requires allocating a set amount of memory up front, which can be configured using the Physics > Jolt Physics 3D > Limits > Temporary Memory Buffer Size project setting.

The face_index property returned in the results of intersect_ray() and RayCast3D will by default always be -1 with Jolt. The project setting Physics > Jolt Physics 3D > Queries > Enable Ray Cast Face Index will enable them.

Note that enabling this setting will increase the memory requirement of ConcavePolygonShape3D with about 25%.

When using Jolt, a RigidBody3D frozen with FREEZE_MODE_KINEMATIC will by default not report contacts from collisions with other static/kinematic bodies, for performance reasons, even when setting a non-zero max_contacts_reported. If you have many/large kinematic bodies overlapping with complex static geometry, such as ConcavePolygonShape3D or HeightMapShape3D, you can end up wasting a significant amount of CPU performance and memory without realizing it.

For this reason this behavior is opt-in through the project setting Physics > Jolt Physics 3D > Simulation > Generate All Kinematic Contacts.

Due to limitations internal to Jolt, the contact impulses provided by PhysicsDirectBodyState3D.get_contact_impulse() are estimated ahead of time based on things like the contact manifold and velocities of the colliding bodies. This means that the reported impulses will only be accurate in cases where the two bodies in question are not colliding with any other bodies.

Jolt does not currently support any interactions between SoftBody3D and Area3D, such as overlap events, or the wind properties found on Area3D.

WorldBoundaryShape3D, which is meant to represent an infinite plane, is implemented a bit differently in Jolt compared to Godot Physics. Both engines have an upper limit for how big the effective size of this plane can be, but this size is much smaller when using Jolt, in order to avoid precision issues.

You can configure this size using the Physics > Jolt Physics 3D > Limits > World Boundary Shape Size project setting.

While the built-in Jolt module is largely a straight port of the Godot Jolt extension, there are a few things that are different.

All project settings have been moved from the physics/jolt_3d category to physics/jolt_physics_3d.

On top of that, there's been some renaming and refactoring of the individual project settings as well. These include:

sleep/enabled is now simulation/allow_sleep.

sleep/velocity_threshold is now simulation/sleep_velocity_threshold.

sleep/time_threshold is now simulation/sleep_time_threshold.

collisions/use_shape_margins is now collisions/collision_margin_fraction, where a value of 0 is equivalent to disabling it.

collisions/use_enhanced_internal_edge_removal is now simulation/use_enhanced_internal_edge_removal.

collisions/areas_detect_static_bodies is now simulation/areas_detect_static_bodies.

collisions/report_all_kinematic_contacts is now simulation/generate_all_kinematic_contacts.

collisions/soft_body_point_margin is now simulation/soft_body_point_radius.

collisions/body_pair_cache_enabled is now simulation/body_pair_contact_cache_enabled.

collisions/body_pair_cache_distance_threshold is now simulation/body_pair_contact_cache_distance_threshold.

collisions/body_pair_cache_angle_threshold is now simulation/body_pair_contact_cache_angle_threshold.

continuous_cd/movement_threshold is now simulation/continuous_cd_movement_threshold, but expressed as a fraction instead of a percentage.

continuous_cd/max_penetration is now simulation/continuous_cd_max_penetration, but expressed as a fraction instead of a percentage.

kinematics/use_enhanced_internal_edge_removal is now motion_queries/use_enhanced_internal_edge_removal.

kinematics/recovery_iterations is now motion_queries/recovery_iterations, but expressed as a fraction instead of a percentage.

kinematics/recovery_amount is now motion_queries/recovery_amount.

queries/use_legacy_ray_casting has been removed.

solver/position_iterations is now simulation/position_steps.

solver/velocity_iterations is now simulation/velocity_steps.

solver/position_correction is now simulation/baumgarte_stabilization_factor, but expressed as a fraction instead of a percentage.

solver/active_edge_threshold is now collisions/active_edge_threshold.

solver/bounce_velocity_threshold is now simulation/bounce_velocity_threshold.

solver/contact_speculative_distance is now simulation/speculative_contact_distance.

solver/contact_allowed_penetration is now simulation/penetration_slop.

limits/max_angular_velocity is now stored as radians instead.

limits/max_temporary_memory is now limits/temporary_memory_buffer_size.

The joint nodes that are exposed in the Godot Jolt extension (JoltPinJoint3D, JoltHingeJoint3D, JoltSliderJoint3D, JoltConeTwistJoint3D, and JoltGeneric6DOFJoint) have not been included in the Jolt module.

Unlike the Godot Jolt extension, the Jolt module does have thread-safety, including support for the Physics > 3D > Run On Separate Thread project setting. However this has not been tested very thoroughly, so it should be considered experimental.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Ragdoll system — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/physics/ragdoll_system.html

**Contents:**
- Ragdoll system
- Introduction
- Setting up the ragdoll
  - Creating physical bones
  - Cleaning up the skeleton
  - Collision shape adjustment
  - Joints adjustment
- Simulating the ragdoll
  - Collision layer and mask
- User-contributed notes

Since version 3.1, Godot supports ragdoll physics. Ragdolls rely on physics simulation to create realistic procedural animation. They are used for death animations in many games.

In this tutorial, we will be using the Platformer3D demo to set up a ragdoll.

You can download the Platformer3D demo on GitHub or using the Asset Library.

Like many other features in the engine, there is a node to set up a ragdoll: the PhysicalBone3D node. To simplify the setup, you can generate PhysicalBone nodes with the "Create physical skeleton" feature in the skeleton node.

Open the platformer demo in Godot, and then the Robi scene. Select the Skeleton node. A skeleton button appears on the top bar menu:

Click it and select the Create physical skeleton option. Godot will generate PhysicalBone nodes and collision shapes for each bone in the skeleton and pin joints to connect them together:

Some of the generated bones aren't necessary: the MASTER bone for example. So we're going to clean up the skeleton by removing them.

Each PhysicalBone the engine needs to simulate has a performance cost, so you want to remove every bone that is too small to make a difference in the simulation, as well as all utility bones.

For example, if we take a humanoid, you do not want to have physical bones for each finger. You can use a single bone for the entire hand instead, or one for the palm, one for the thumb, and a last one for the other four fingers.

Remove these physical bones: MASTER, waist, neck, headtracker. This gives us an optimized skeleton and makes it easier to control the ragdoll.

The next task is adjusting the collision shape and the size of physical bones to match the part of the body that each bone should simulate.

Once you adjusted the collision shapes, your ragdoll is almost ready. You just want to adjust the pin joints to get a better simulation. PhysicalBone nodes have an unconstrained pin joint assigned to them by default. To change the pin joint, select the PhysicalBone and change the constraint type in the Joint section. There, you can change the constraint's orientation and its limits.

This is the final result:

The ragdoll is now ready to use. To start the simulation and play the ragdoll animation, you need to call the physical_bones_start_simulation method. Attach a script to the skeleton node and call the method in the _ready method:

To stop the simulation, call the physical_bones_stop_simulation() method.

You can also limit the simulation to only a few bones. To do so, pass the bone names as a parameter. Here's an example of partial ragdoll simulation:

Make sure to set up your collision layers and masks properly so the CharacterBody3D's capsule doesn't get in the way of the physics simulation:

For more information, read Collision layers and masks.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
func _ready():
    physical_bones_start_simulation()
```

Example 2 (gdscript):
```gdscript
public override void _Ready()
{
    PhysicalBonesStartSimulation();
}
```

---

## Ray-casting — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/physics/ray-casting.html

**Contents:**
- Ray-casting
- Introduction
- Space
- Accessing space
- Raycast query
- Collision exceptions
- Collision Mask
- 3D ray casting from screen
- User-contributed notes

One of the most common tasks in game development is casting a ray (or custom shaped object) and checking what it hits. This enables complex behaviors, AI, etc. to take place. This tutorial will explain how to do this in 2D and 3D.

Godot stores all the low-level game information in servers, while the scene is only a frontend. As such, ray casting is generally a lower-level task. For simple raycasts, nodes like RayCast3D and RayCast2D will work, as they return every frame what the result of a raycast is.

Many times, though, ray-casting needs to be a more interactive process so a way to do this by code must exist.

In the physics world, Godot stores all the low-level collision and physics information in a space. The current 2d space (for 2D Physics) can be obtained by accessing CanvasItem.get_world_2d().space. For 3D, it's Node3D.get_world_3d().space.

The resulting space RID can be used in PhysicsServer3D and PhysicsServer2D respectively for 3D and 2D.

Godot physics runs by default in the same thread as game logic, but may be set to run on a separate thread to work more efficiently. Due to this, the only time accessing space is safe is during the Node._physics_process() callback. Accessing it from outside this function may result in an error due to space being locked.

To perform queries into physics space, the PhysicsDirectSpaceState2D and PhysicsDirectSpaceState3D must be used.

Use the following code in 2D:

For performing a 2D raycast query, the method PhysicsDirectSpaceState2D.intersect_ray() may be used. For example:

The result is a dictionary. If the ray didn't hit anything, the dictionary will be empty. If it did hit something, it will contain collision information:

The result dictionary when a collision occurs contains the following data:

The data is similar in 3D space, using Vector3 coordinates. Note that to enable collisions with Area3D, the boolean parameter collide_with_areas must be set to true.

A common use case for ray casting is to enable a character to gather data about the world around it. One problem with this is that the same character has a collider, so the ray will only detect its parent's collider, as shown in the following image:

To avoid self-intersection, the intersect_ray() parameters object can take an array of exceptions via its exclude property. This is an example of how to use it from a CharacterBody2D or any other collision object node:

The exceptions array can contain objects or RIDs.

While the exceptions method works fine for excluding the parent body, it becomes very inconvenient if you need a large and/or dynamic list of exceptions. In this case, it is much more efficient to use the collision layer/mask system.

The intersect_ray() parameters object can also be supplied a collision mask. For example, to use the same mask as the parent body, use the collision_mask member variable. The array of exceptions can be supplied as the last argument as well:

See Code example for details on how to set the collision mask.

Casting a ray from screen to 3D physics space is useful for object picking. There is not much need to do this because CollisionObject3D has an "input_event" signal that will let you know when it was clicked, but in case there is any desire to do it manually, here's how.

To cast a ray from the screen, you need a Camera3D node. A Camera3D can be in two projection modes: perspective and orthogonal. Because of this, both the ray origin and direction must be obtained. This is because origin changes in orthogonal mode, while normal changes in perspective mode:

To obtain it using a camera, the following code can be used:

Remember that during _input(), the space may be locked, so in practice this query should be run in _physics_process().

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
func _physics_process(delta):
    var space_rid = get_world_2d().space
    var space_state = PhysicsServer2D.space_get_direct_state(space_rid)
```

Example 2 (gdscript):
```gdscript
public override void _PhysicsProcess(double delta)
{
    var spaceRid = GetWorld2D().Space;
    var spaceState = PhysicsServer2D.SpaceGetDirectState(spaceRid);
}
```

Example 3 (gdscript):
```gdscript
func _physics_process(delta):
    var space_state = get_world_2d().direct_space_state
```

Example 4 (gdscript):
```gdscript
public override void _PhysicsProcess(double delta)
{
    var spaceState = GetWorld2D().DirectSpaceState;
}
```

---

## Using CharacterBody2D/3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.html

**Contents:**
- Using CharacterBody2D/3D
- Introduction
- What is a character body?
- Movement and collision
  - move_and_collide
  - move_and_slide
- Detecting collisions
- Which movement method to use?
- Examples
  - Movement and walls

Godot offers several collision objects to provide both collision detection and response. Trying to decide which one to use for your project can be confusing. You can avoid problems and simplify development if you understand how each of them works and what their pros and cons are. In this tutorial, we'll look at the CharacterBody2D node and show some examples of how to use it.

While this document uses CharacterBody2D in its examples, the same concepts apply in 3D as well.

CharacterBody2D is for implementing bodies that are controlled via code. Character bodies detect collisions with other bodies when moving, but are not affected by engine physics properties, like gravity or friction. While this means that you have to write some code to create their behavior, it also means you have more precise control over how they move and react.

This document assumes you're familiar with Godot's various physics bodies. Please read Physics introduction first, for an overview of the physics options.

A CharacterBody2D can be affected by gravity and other forces, but you must calculate the movement in code. The physics engine will not move a CharacterBody2D.

When moving a CharacterBody2D, you should not set its position property directly. Instead, you use the move_and_collide() or move_and_slide() methods. These methods move the body along a given vector and detect collisions.

You should handle physics body movement in the _physics_process() callback.

The two movement methods serve different purposes, and later in this tutorial, you'll see examples of how they work.

This method takes one required parameter: a Vector2 indicating the body's relative movement. Typically, this is your velocity vector multiplied by the frame timestep (delta). If the engine detects a collision anywhere along this vector, the body will immediately stop moving. If this happens, the method will return a KinematicCollision2D object.

KinematicCollision2D is an object containing data about the collision and the colliding object. Using this data, you can calculate your collision response.

move_and_collide is most useful when you just want to move the body and detect collision, but don't need any automatic collision response. For example, if you need a bullet that ricochets off a wall, you can directly change the angle of the velocity when you detect a collision. See below for an example.

The move_and_slide() method is intended to simplify the collision response in the common case where you want one body to slide along the other. It is especially useful in platformers or top-down games, for example.

When calling move_and_slide(), the function uses a number of node properties to calculate its slide behavior. These properties can be found in the Inspector, or set in code.

velocity - default value: Vector2( 0, 0 )

This property represents the body's velocity vector in pixels per second. move_and_slide() will modify this value automatically when colliding.

motion_mode - default value: MOTION_MODE_GROUNDED

This property is typically used to distinguish between side-scrolling and top-down movement. When using the default value, you can use the is_on_floor(), is_on_wall(), and is_on_ceiling() methods to detect what type of surface the body is in contact with, and the body will interact with slopes. When using MOTION_MODE_FLOATING, all collisions will be considered "walls".

up_direction - default value: Vector2( 0, -1 )

This property allows you to define what surfaces the engine should consider being the floor. Its value lets you use the is_on_floor(), is_on_wall(), and is_on_ceiling() methods to detect what type of surface the body is in contact with. The default value means that the top side of horizontal surfaces will be considered "ground".

floor_stop_on_slope - default value: true

This parameter prevents a body from sliding down slopes when standing still.

wall_min_slide_angle - default value: 0.261799 (in radians, equivalent to 15 degrees)

This is the minimum angle where the body is allowed to slide when it hits a slope.

floor_max_angle - default value: 0.785398 (in radians, equivalent to 45 degrees)

This parameter is the maximum angle before a surface is no longer considered a "floor."

There are many other properties that can be used to modify the body's behavior under specific circumstances. See the CharacterBody2D docs for full details.

When using move_and_collide() the function returns a KinematicCollision2D directly, and you can use this in your code.

When using move_and_slide() it's possible to have multiple collisions occur, as the slide response is calculated. To process these collisions, use get_slide_collision_count() and get_slide_collision():

get_slide_collision_count() only counts times the body has collided and changed direction.

See KinematicCollision2D for details on what collision data is returned.

A common question from new Godot users is: "How do you decide which movement function to use?" Often, the response is to use move_and_slide() because it seems simpler, but this is not necessarily the case. One way to think of it is that move_and_slide() is a special case, and move_and_collide() is more general. For example, the following two code snippets result in the same collision response:

Anything you do with move_and_slide() can also be done with move_and_collide(), but it might take a little more code. However, as we'll see in the examples below, there are cases where move_and_slide() doesn't provide the response you want.

In the example above, move_and_slide() automatically alters the velocity variable. This is because when the character collides with the environment, the function recalculates the speed internally to reflect the slowdown.

For example, if your character fell on the floor, you don't want it to accumulate vertical speed due to the effect of gravity. Instead, you want its vertical speed to reset to zero.

move_and_slide() may also recalculate the kinematic body's velocity several times in a loop as, to produce a smooth motion, it moves the character and collides up to five times by default. At the end of the process, the character's new velocity is available for use on the next frame.

To see these examples in action, download the sample project: character_body_2d_starter.zip

If you've downloaded the sample project, this example is in "basic_movement.tscn".

For this example, add a CharacterBody2D with two children: a Sprite2D and a CollisionShape2D. Use the Godot "icon.svg" as the Sprite2D's texture (drag it from the Filesystem dock to the Texture property of the Sprite2D). In the CollisionShape2D's Shape property, select "New RectangleShape2D" and size the rectangle to fit over the sprite image.

See 2D movement overview for examples of implementing 2D movement schemes.

Attach a script to the CharacterBody2D and add the following code:

Run this scene and you'll see that move_and_collide() works as expected, moving the body along the velocity vector. Now let's see what happens when you add some obstacles. Add a StaticBody2D with a rectangular collision shape. For visibility, you can use a Sprite2D, a Polygon2D, or turn on "Visible Collision Shapes" from the "Debug" menu.

Run the scene again and try moving into the obstacle. You'll see that the CharacterBody2D can't penetrate the obstacle. However, try moving into the obstacle at an angle and you'll find that the obstacle acts like glue - it feels like the body gets stuck.

This happens because there is no collision response. move_and_collide() stops the body's movement when a collision occurs. We need to code whatever response we want from the collision.

Try changing the function to move_and_slide() and running again.

move_and_slide() provides a default collision response of sliding the body along the collision object. This is useful for a great many game types, and may be all you need to get the behavior you want.

What if you don't want a sliding collision response? For this example ("bounce_and_collide.tscn" in the sample project), we have a character shooting bullets and we want the bullets to bounce off the walls.

This example uses three scenes. The main scene contains the Player and Walls. The Bullet and Wall are separate scenes so that they can be instanced.

The Player is controlled by the w and s keys for forward and back. Aiming uses the mouse pointer. Here is the code for the Player, using move_and_slide():

And the code for the Bullet:

The action happens in _physics_process(). After using move_and_collide(), if a collision occurs, a KinematicCollision2D object is returned (otherwise, the return is null).

If there is a returned collision, we use the normal of the collision to reflect the bullet's velocity with the Vector2.bounce() method.

If the colliding object (collider) has a hit method, we also call it. In the example project, we've added a flashing color effect to the Wall to demonstrate this.

Let's try one more popular example: the 2D platformer. move_and_slide() is ideal for quickly getting a functional character controller up and running. If you've downloaded the sample project, you can find this in "platformer.tscn".

For this example, we'll assume you have a level made of one or more StaticBody2D objects. They can be any shape and size. In the sample project, we're using Polygon2D to create the platform shapes.

Here's the code for the player body:

In this code we're using move_and_slide() as described above - to move the body along its velocity vector, sliding along any collision surfaces such as the ground or a platform. We're also using is_on_floor() to check if a jump should be allowed. Without this, you'd be able to "jump" in midair; great if you're making Flappy Bird, but not for a platformer game.

There is a lot more that goes into a complete platformer character: acceleration, double-jumps, coyote-time, and many more. The code above is just a starting point. You can use it as a base to expand into whatever movement behavior you need for your own projects.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (julia):
```julia
# Using move_and_collide.
var collision = move_and_collide(velocity * delta)
if collision:
    print("I collided with ", collision.get_collider().name)

# Using move_and_slide.
move_and_slide()
for i in get_slide_collision_count():
    var collision = get_slide_collision(i)
    print("I collided with ", collision.get_collider().name)
```

Example 2 (julia):
```julia
// Using MoveAndCollide.
var collision = MoveAndCollide(Velocity * (float)delta);
if (collision != null)
{
    GD.Print("I collided with ", ((Node)collision.GetCollider()).Name);
}

// Using MoveAndSlide.
MoveAndSlide();
for (int i = 0; i < GetSlideCollisionCount(); i++)
{
    var collision = GetSlideCollision(i);
    GD.Print("I collided with ", ((Node)collision.GetCollider()).Name);
}
```

Example 3 (typescript):
```typescript
# using move_and_collide
var collision = move_and_collide(velocity * delta)
if collision:
    velocity = velocity.slide(collision.get_normal())

# using move_and_slide
move_and_slide()
```

Example 4 (julia):
```julia
// using MoveAndCollide
var collision = MoveAndCollide(Velocity * (float)delta);
if (collision != null)
{
    Velocity = Velocity.Slide(collision.GetNormal());
}

// using MoveAndSlide
MoveAndSlide();
```

---

## Using SoftBody3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/physics/soft_body.html

**Contents:**
- Using SoftBody3D
- Basic set-up
- Cloak simulation
- Using Imported Meshes
- User-contributed notes

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

Soft bodies (or soft-body dynamics) simulate movement, changing shape and other physical properties of deformable objects. This can for example be used to simulate cloth or to create more realistic characters.

A SoftBody3D node is used for soft body simulations.

We will create a bouncy cube to demonstrate the setup of a soft body.

Create a new scene with a Node3D node as root. Then, create a SoftBody3D node. Add a CubeMesh in the mesh property of the node in the inspector and increase the subdivision of the mesh for simulation.

Set the parameters to obtain the type of soft body you aim for. Try to keep the Simulation Precision above 5, otherwise, the soft body may collapse.

Handle some parameters with care, as some value can lead to strange results. For example, if the shape is not completely closed and you set pressure to more than 0, the softbody will fly around like a plastic bag under strong wind.

Play the scene to view the simulation.

To improve the simulation's result, increase the Simulation Precision, this will give significant improvement at the cost of performance.

Let's make a cloak in the Platformer3D demo.

You can download the Platformer3D demo on GitHub or the Asset Library.

Open the Player scene, add a SoftBody3D node and assign a PlaneMesh to it.

Open the PlaneMesh properties and set the size(x: 0.5 y: 1) then set Subdivide Width and Subdivide Depth to 5. Adjust the SoftBody3D's position. You should end up with something like this:

Subdivision generates a more tessellated mesh for better simulations.

Add a BoneAttachment3D node under the skeleton node and select the Neck bone to attach the cloak to the character skeleton.

BoneAttachment3D node is to attach objects to a bone of an armature. The attached object will follow the bone's movement, weapon of a character can be attached this way.

To create pinned joints, select the upper vertices in the SoftBody3D node:

The pinned joints can be found in SoftBody3D's Attachments property, choose the BoneAttachment as the SpatialAttachment for each pinned joints, the pinned joints are now attached to the neck.

Last step is to avoid clipping by adding the Kinematic Body Player to Parent Collision Ignore of the SoftBody3D.

Play the scene and the cloak should simulate correctly.

This covers the basic settings of softbody, experiment with the parameters to achieve the effect you are aiming for when making your game.

The Save to File option in the Advanced Import Settings dialog allows you to save a mesh to a standalone resource file that you can then attach to SoftBody3D nodes.

You may also want to disable LOD generation or change the LOD generation options when importing a mesh for use with SoftBody3D. The default import settings will produce an LOD that merges adjacent faces that are nearly flat with respect to each other, even at very close render distances. This works well for static meshes, but is often undesirable for use with SoftBody3D if you want these faces to be able to bend and move with respect to each other, instead of being rendered as a single plane.

See Import configuration and Mesh level of detail (LOD) for more details.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Kinematic character (2D) — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/physics/kinematic_character_2d.html

**Contents:**
- Kinematic character (2D)
- Introduction
- Physics process
- Scene setup
- Moving the kinematic character
- User-contributed notes

Yes, the name sounds strange. "Kinematic Character". What is that? The reason for the name is that, when physics engines came out, they were called "Dynamics" engines (because they dealt mainly with collision responses). Many attempts were made to create a character controller using the dynamics engines, but it wasn't as easy as it seemed. Godot has one of the best implementations of dynamic character controller you can find (as it can be seen in the 2d/platformer demo), but using it requires a considerable level of skill and understanding of physics engines (or a lot of patience with trial and error).

Some physics engines, such as Havok seem to swear by dynamic character controllers as the best option, while others (PhysX) would rather promote the kinematic one.

So, what is the difference?:

A dynamic character controller uses a rigid body with an infinite inertia tensor. It's a rigid body that can't rotate. Physics engines always let objects move and collide, then solve their collisions all together. This makes dynamic character controllers able to interact with other physics objects seamlessly, as seen in the platformer demo. However, these interactions are not always predictable. Collisions can take more than one frame to be solved, so a few collisions may seem to displace a tiny bit. Those problems can be fixed, but require a certain amount of skill.

A kinematic character controller is assumed to always begin in a non-colliding state, and will always move to a non-colliding state. If it starts in a colliding state, it will try to free itself like rigid bodies do, but this is the exception, not the rule. This makes their control and motion a lot more predictable and easier to program. However, as a downside, they can't directly interact with other physics objects, unless done by hand in code.

This short tutorial focuses on the kinematic character controller. It uses the old-school way of handling collisions, which is not necessarily simpler under the hood, but well hidden and presented as an API.

To manage the logic of a kinematic body or character, it is always advised to use physics process, because it's called before physics step and its execution is in sync with physics server, also it is called the same amount of times per second, always. This makes physics and motion calculation work in a more predictable way than using regular process, which might have spikes or lose precision if the frame rate is too high or too low.

To have something to test, here's the scene (from the tilemap tutorial): kinematic_character_2d_starter.zip. We'll be creating a new scene for the character. Use the robot sprite and create a scene like this:

You'll notice that there's a warning icon next to our CollisionShape2D node; that's because we haven't defined a shape for it. Create a new CircleShape2D in the shape property of CollisionShape2D. Click on <CircleShape2D> to go to the options for it, and set the radius to 30:

Note: As mentioned before in the physics tutorial, the physics engine can't handle scale on most types of shapes (only collision polygons, planes and segments work), so always change the parameters (such as radius) of the shape instead of scaling it. The same is also true for the kinematic/rigid/static bodies themselves, as their scale affects the shape scale.

Now, create a script for the character, the one used as an example above should work as a base.

Finally, instance that character scene in the tilemap, and make the map scene the main one, so it runs when pressing play.

Go back to the character scene, and open the script, the magic begins now! Kinematic body will do nothing by default, but it has a useful function called CharacterBody2D.move_and_collide(). This function takes a Vector2 as an argument, and tries to apply that motion to the kinematic body. If a collision happens, it stops right at the moment of the collision.

So, let's move our sprite downwards until it hits the floor:

The result is that the character will move, but stop right when hitting the floor. Pretty cool, huh?

The next step will be adding gravity to the mix, this way it behaves a little more like a regular game character:

Now the character falls smoothly. Let's make it walk to the sides, left and right when touching the directional keys. Remember that the values being used (for speed at least) are pixels/second.

This adds basic support for walking when pressing left and right:

This is a good starting point for a platformer. A more complete demo can be found in the demo zip distributed with the engine, or in the https://github.com/godotengine/godot-demo-projects/tree/master/2d/kinematic_character.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends CharacterBody2D

func _physics_process(delta):
    pass
```

Example 2 (swift):
```swift
using Godot;

public partial class MyCharacterBody2D : CharacterBody2D
{
    public override void _PhysicsProcess(double delta)
    {
    }
}
```

Example 3 (gdscript):
```gdscript
extends CharacterBody2D

func _physics_process(delta):
    move_and_collide(Vector2(0, 1)) # Move down 1 pixel per physics frame
```

Example 4 (swift):
```swift
using Godot;

public partial class MyCharacterBody2D : CharacterBody2D
{
    public override void _PhysicsProcess(double delta)
    {
        // Move down 1 pixel per physics frame
        MoveAndCollide(new Vector2(0, 1));
    }
}
```

---

## Large world coordinates — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/physics/large_world_coordinates.html

**Contents:**
- Large world coordinates
- Why use large world coordinates?
- How large world coordinates work
- Who are large world coordinates for?
- Enabling large world coordinates
- Compatibility between single-precision and double-precision builds
  - Known incompatibilities
- Limitations
- User-contributed notes

Large world coordinates are mainly useful in 3D projects; they are rarely required in 2D projects. Also, unlike 3D rendering, 2D rendering currently doesn't benefit from increased precision when large world coordinates are enabled.

In Godot, physics simulation and rendering both rely on floating-point numbers. However, in computing, floating-point numbers have limited precision and range. This can be a problem for games with huge worlds, such as space or planetary-scale simulation games.

Precision is the greatest when the value is close to 0.0. Precision becomes gradually lower as the value increases or decreases away from 0.0. This occurs every time the floating-point number's exponent increases, which happens when the floating-point number surpasses a power of 2 value (2, 4, 8, 16, …). Every time this occurs, the number's minimum step will increase, resulting in a loss of precision.

In practice, this means that as the player moves away from the world origin (Vector2(0, 0) in 2D games or Vector3(0, 0, 0) in 3D games), precision will decrease.

This loss of precision can result in objects appearing to "vibrate" when far away from the world origin, as the model's position will snap to the nearest value that can be represented in a floating-point number. This can also result in physics glitches that only occur when the player is far from the world origin.

The range determines the minimum and maximum values that can be stored in the number. If the player tries to move past this range, they will simply not be able to. However, in practice, floating-point precision almost always becomes a problem before the range does.

The range and precision (minimum step between two exponent intervals) are determined by the floating-point number type. The theoretical range allows extremely high values to be stored in single-precision floats, but with very low precision. In practice, a floating-point type that cannot represent all integer values is not very useful. At extreme values, precision becomes so low that the number cannot even distinguish two separate integer values from each other.

This is the range where individual integer values can be represented in a floating-point number:

Single-precision float range (represent all integers): Between -16,777,216 and 16,777,216

Double-precision float range (represent all integers): Between -9 quadrillion and 9 quadrillion

Precision becomes greater near 0.0 (this table is abbreviated).

Maximum recommended single-precision range for a first-person 3D game without rendering artifacts or physics glitches.

Maximum recommended single-precision range for a third-person 3D game without rendering artifacts or physics glitches.

Maximum recommended single-precision range for a top-down 3D game without rendering artifacts or physics glitches.

Maximum recommended single-precision range for any 3D game. Double precision (large world coordinates) is usually required past this point.

~1e-10 (0.0000000001)

Double-precision remains far more precise than single-precision past this value.

When using single-precision floats, it is possible to go past the suggested ranges, but more visible artifacting will occur and physics glitches will be more common (such as the player not walking straight in certain directions).

See the Demystifying Floating Point Precision article for more information.

Large world coordinates (also known as double-precision physics) increase the precision level of all floating-point computations within the engine.

By default, float is 64-bit in GDScript, but Vector2, Vector3 and Vector4 are 32-bit. This means that the precision of vector types is much more limited. To resolve this, we can increase the number of bits used to represent a floating-point number in a Vector type. This results in an exponential increase in precision, which means the final value is not just twice as precise, but potentially thousands of times more precise at high values. The maximum value that can be represented is also greatly increased by going from a single-precision float to a double-precision float.

To avoid model snapping issues when far away from the world origin, Godot's 3D rendering engine will increase its precision for rendering operations when large world coordinates are enabled. The shaders do not use double-precision floats for performance reasons, but an alternative solution is used to emulate double precision for rendering using single-precision floats.

Enabling large world coordinates comes with a performance and memory usage penalty, especially on 32-bit CPUs. Only enable large world coordinates if you actually need them.

This feature is tailored towards mid-range/high-end desktop platforms. Large world coordinates may not perform well on low-end mobile devices, unless you take steps to reduce CPU usage with other means (such as decreasing the number of physics ticks per second).

On low-end platforms, an origin shifting approach can be used instead to allow for large worlds without using double-precision physics and rendering. Origin shifting works with single-precision floats, but it introduces more complexity to game logic, especially in multiplayer games. Therefore, origin shifting is not detailed on this page.

Large world coordinates are typically required for 3D space or planetary-scale simulation games. This extends to games that require supporting very fast movement speeds, but also very slow and precise movements at times.

On the other hand, it's important to only use large world coordinates when actually required (for performance reasons). Large world coordinates are usually not required for:

2D games, as precision issues are usually less noticeable.

Games with small-scale or medium-scale worlds.

Games with large worlds, but split into different levels with loading sequences in between. You can center each level portion around the world origin to avoid precision issues without a performance penalty.

Open world games with a playable on-foot area not exceeding 8192×8192 meters (centered around the world origin). As shown in the above table, the level of precision remains acceptable within that range, even for a first-person game.

If in doubt, you probably don't need to use large world coordinates in your project. For reference, most modern AAA open world titles don't use a large world coordinates system and still rely on single-precision floats for both rendering and physics.

This process requires recompiling the editor and all export template binaries you intend to use. If you only intend to export your project in release mode, you can skip the compilation of debug export templates. In any case, you'll need to compile an editor build so you can test your large precision world without having to export the project every time.

See the Compiling section for compiling instructions for each target platform. You will need to add the precision=double SCons option when compiling the editor and export templates.

The resulting binaries will be named with a .double suffix to distinguish them from single-precision binaries (which lack any precision suffix). You can then specify the binaries as custom export templates in your project's export presets in the Export dialog.

When saving a binary resource using the ResourceSaver singleton, a special flag is stored in the file if the resource was saved using a build that uses double-precision numbers. As a result, all binary resources will change on disk when you switch to a double-precision build and save over them.

Both single-precision and double-precision builds support using the ResourceLoader singleton on resources that use this special flag. This means single-precision builds can load resources saved using double-precision builds and vice versa. Text-based resources don't store a double-precision flag, as they don't require such a flag for correct reading.

In a networked multiplayer game, the server and all clients should be using the same build type to ensure precision remains consistent across clients. Using different build types may work, but various issues can occur.

The GDExtension API changes in an incompatible way in double-precision builds. This means extensions must be rebuilt to work with double-precision builds. On the extension developer's end, the REAL_T_IS_DOUBLE define is enabled when building a GDExtension with precision=double. real_t can be used as an alias for float in single-precision builds, and double in double-precision builds.

Since 3D rendering shaders don't actually use double-precision floats, there are some limitations when it comes to 3D rendering precision:

Shaders using the skip_vertex_transform or world_vertex_coords don't benefit from increased precision.

Triplanar mapping doesn't benefit from increased precision. Materials using triplanar mapping will exhibit visible jittering when far away from the world origin.

In double-precision builds, world space coordinates in a shader fragment() function can't be reconstructed from view space, for example:

Instead, calculate the world space coordinates in the vertex() function and pass them using a varying, for example:

2D rendering currently doesn't benefit from increased precision when large world coordinates are enabled. This can cause visible model snapping to occur when far away from the world origin (starting from a few million pixels at typical zoom levels). 2D physics calculations will still benefit from increased precision though.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
vec3 world = (INV_VIEW_MATRIX * vec4(VERTEX, 1.0)).xyz;
```

Example 2 (cpp):
```cpp
varying vec3 world;
void vertex() {
    world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
}
```

---

## Advanced physics interpolation — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/physics/interpolation/advanced_physics_interpolation.html

**Contents:**
- Advanced physics interpolation
- Exceptions to automatic physics interpolation
  - Cameras
  - Manual camera interpolation
    - Ensure the camera is using global coordinate space
    - Typical example
    - get_global_transform_interpolated()
    - Example manual camera script
    - Mouse look
  - Disabling interpolation on other nodes

Although the previous instructions will give satisfactory results in a lot of games, in some cases you will want to go a stage further to get the best possible results and the smoothest possible experience.

Even with physics interpolation active, there may be some local situations where you would benefit from disabling automatic interpolation for a Node (or branch of the SceneTree), and have the finer control of performing interpolation manually.

This is possible using the Node.physics_interpolation_mode property which is present in all Nodes. If you for example, turn off interpolation for a Node, the children will recursively also be affected (as they default to inheriting the parent setting). This means you can easily disable interpolation for an entire subscene.

The most common situation where you may want to perform your own interpolation is Cameras.

In many cases, a Camera3D can use automatic interpolation just like any other node. However, for best results, especially at low physics tick rates, it is recommended that you take a manual approach to camera interpolation.

This is because viewers are very sensitive to camera movement. For instance, a Camera3D that realigns slightly every 1/10th of a second (at 10tps tick rate) will often be noticeable. You can get a much smoother result by moving the camera each frame in _process, and following an interpolated target manually.

The very first step when performing manual camera interpolation is to make sure the Camera3D transform is specified in global space rather than inheriting the transform of a moving parent. This is because feedback can occur between the movement of a parent node of a Camera3D and the movement of the camera Node itself, which can mess up the interpolation.

There are two ways of doing this:

Move the Camera3D so it is independent on its own branch, rather than being a child of a moving object.

Call Node3D.top_level and set this to true, which will make the Camera ignore the transform of its parent.

A typical example of a custom approach is to use the look_at function in the Camera3D every frame in _process() to look at a target node (such as the player).

But there is a problem. If we use the traditional get_global_transform() on a Camera3D "target" node, this transform will only focus the Camera3D on the target at the current physics tick. This is not what we want, as the camera will jump about on each physics tick as the target moves. Even though the camera may be updated each frame, this does not help give smooth motion if the target is only changing each physics tick.

What we really want to focus the camera on, is not the position of the target on the physics tick, but the interpolated position, i.e. the position at which the target will be rendered.

We can do this using the Node3D.get_global_transform_interpolated function. This acts exactly like getting Node3D.global_transform but it gives you the interpolated transform (during a _process() call).

get_global_transform_interpolated() should only be used once or twice for special cases such as cameras. It should not be used all over the place in your code (both for performance reasons, and to give correct gameplay).

Aside from exceptions like the camera, in most cases, your game logic should be in _physics_process(). In game logic you should be calling get_global_transform() or get_transform(), which will give the current physics transform (in global or local space respectively), which is usually what you will want for gameplay code.

Here is an example of a simple fixed camera which follows an interpolated target:

Mouse look is a very common way of controlling cameras. But there is a problem. Unlike keyboard input which can be sampled periodically on the physics tick, mouse move events can come in continuously. The camera will be expected to react and follow these mouse movements on the next frame, rather than waiting until the next physics tick.

In this situation, it can be better to disable physics interpolation for the camera node (using Node.physics_interpolation_mode) and directly apply the mouse input to the camera rotation, rather than apply it in _physics_process.

Sometimes, especially with cameras, you will want to use a combination of interpolation and non-interpolation:

A first person camera may position the camera at a player location (perhaps using Node3D.get_global_transform_interpolated), but control the Camera rotation from mouse look without interpolation.

A third person camera may similarly determine the look at (target location) of the camera using Node3D.get_global_transform_interpolated, but position the camera using mouse look without interpolation.

There are many permutations and variations of camera types, but it should be clear that in many cases, disabling automatic physics interpolation and handling this yourself can give a better result.

Although cameras are the most common example, there are a number of cases when you may wish other nodes to control their own interpolation, or be non-interpolated. Consider for example, a player in a top view game whose rotation is controlled by mouse look. Disabling physics rotation allows the player rotation to match the mouse in real-time.

Although most visual Nodes follow the single Node single visual instance paradigm, MultiMeshes can control several instances from the same Node. Therefore, they have some extra functions for controlling interpolation functionality on a per-instance basis. You should explore these functions if you are using interpolated MultiMeshes.

MultiMesh.reset_instance_physics_interpolation

MultiMesh.set_buffer_interpolated

Full details are in the MultiMesh documentation.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends Camera3D

# Node that the camera will follow
var _target

# We will smoothly lerp to follow the target
# rather than follow exactly
var _target_pos : Vector3 = Vector3()

func _ready() -> void:
    # Find the target node
    _target = get_node("../Player")

    # Turn off automatic physics interpolation for the Camera3D,
    # we will be doing this manually
    set_physics_interpolation_mode(Node.PHYSICS_INTERPOLATION_MODE_OFF)

func _process(delta: float) -> void:
    # Find the current interpolated transform of the target
    var tr : Transform = _target.get_global_transform_interpolated()

    # Provide some delayed smoothed lerping towards the target position
    _target_pos = lerp(_target_pos, tr.origin, min(delta, 1.0))

    # Fixed camera position, but it will follow the target
    look_at(_target_pos, Vector3(0, 1, 0))
```

---

## Troubleshooting physics issues — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/physics/troubleshooting_physics_issues.html

**Contents:**
- Troubleshooting physics issues
- Objects are passing through each other at high speeds
- Stacked objects are unstable and wobbly
- Scaled physics bodies or collision shapes do not collide correctly
- Thin objects are wobbly when resting on the floor
- Cylinder collision shapes are unstable
- VehicleBody simulation is unstable, especially at high speeds
- Collision results in bumps when an object moves across tiles
- Framerate drops when an object touches another object
- Framerate suddenly drops to a very low value beyond a certain amount of physics simulation

When working with a physics engine, you may encounter unexpected results.

While many of these issues can be resolved through configuration, some of them are the result of engine bugs. For known issues related to the physics engine, see open physics-related issues on GitHub. Looking through closed issues can also help answer questions related to physics engine behavior.

This is known as tunneling. Enabling Continuous CD in the RigidBody properties can sometimes resolve this issue. If this does not help, there are other solutions you can try:

Make your static collision shapes thicker. For example, if you have a thin floor that the player can't get below in some way, you can make the collider thicker than the floor's visual representation.

Modify your fast-moving object's collision shape depending on its movement speed. The faster the object moves, the larger the collision shape should extend outside of the object to ensure it can collide with thin walls more reliably.

Increase Physics Ticks per Second in the advanced Project Settings. While this has other benefits (such as more stable simulation and reduced input lag), this increases CPU utilization and may not be viable for mobile/web platforms. Multipliers of the default value of 60 (such as 120, 180 or 240) should be preferred for a smooth appearance on most displays.

Despite seeming like a simple problem, stable RigidBody simulation with stacked objects is difficult to implement in a physics engine. This is caused by integrating forces going against each other. The more stacked objects are present, the stronger the forces will be against each other. This eventually causes the simulation to become wobbly, making the objects unable to rest on top of each other without moving.

Increasing the physics simulation rate can help alleviate this issue. To do so, increase Physics Ticks per Second in the advanced Project Settings. Note that increases CPU utilization and may not be viable for mobile/web platforms. Multipliers of the default value of 60 (such as 120, 180 or 240) should be preferred for a smooth appearance on most displays.

In 3D, switching the physics engine from the default GodotPhysics to Jolt can also improve stability. See Using Jolt Physics for more information.

Godot does not currently support scaling of physics bodies or collision shapes. As a workaround, change the collision shape's extents instead of changing its scale. If you want the visual representation's scale to change as well, change the scale of the underlying visual representation (Sprite2D, MeshInstance3D, …) and change the collision shape's extents separately. Make sure the collision shape is not a child of the visual representation in this case.

Since resources are shared by default, you'll have to make the collision shape resource unique if you don't want the change to be applied to all nodes using the same collision shape resource in the scene. This can be done by calling duplicate() in a script on the collision shape resource before changing its size.

This can be due to one of two causes:

The floor's collision shape is too thin.

The RigidBody's collision shape is too thin.

In the first case, this can be alleviated by making the floor's collision shape thicker. For example, if you have a thin floor that the player can't get below in some way, you can make the collider thicker than the floor's visual representation.

In the second case, this can usually only be resolved by increasing the physics simulation rate (as making the shape thicker would cause a disconnect between the RigidBody's visual representation and its collision).

In both cases, increasing the physics simulation rate can also help alleviate this issue. To do so, increase Physics Ticks per Second in the advanced Project Settings. Note that this increases CPU utilization and may not be viable for mobile/web platforms. Multipliers of the default value of 60 (such as 120, 180 or 240) should be preferred for a smooth appearance on most displays.

Switching the physics engine from the default GodotPhysics to Jolt should make cylinder collision shapes more reliable. See Using Jolt Physics for more information.

During the transition from Bullet to GodotPhysics in Godot 4, cylinder collision shapes had to be reimplemented from scratch. However, cylinder collision shapes are one of the most difficult shapes to support, which is why many other physics engines don't provide any support for them. There are several known bugs with cylinder collision shapes currently.

If you are sticking to GodotPhysics, we recommend using box or capsule collision shapes for characters for now. Boxes generally provide the best reliability, but have the downside of making the character take more space diagonally. Capsule collision shapes do not have this downside, but their shape can make precision platforming more difficult.

When a physics body moves at a high speed, it travels a large distance between each physics step. For instance, when using the 1 unit = 1 meter convention in 3D, a vehicle moving at 360 km/h will travel 100 units per second. With the default physics simulation rate of 60 Hz, the vehicle moves by ~1.67 units each physics tick. This means that small objects may be ignored entirely by the vehicle (due to tunneling), but also that the simulation has little data to work with in general at such a high speed.

Fast-moving vehicles can benefit a lot from an increased physics simulation rate. To do so, increase Physics Ticks per Second in the advanced Project Settings. Note that this increases CPU utilization and may not be viable for mobile/web platforms. Multipliers of the default value of 60 (such as 120, 180 or 240) should be preferred for a smooth appearance on most displays.

This is a known issue in the physics engine caused by the object bumping on a shape's edges, even though that edge is covered by another shape. This can occur in both 2D and 3D.

The best way to work around this issue is to create a "composite" collider. This means that instead of individual tiles having their collision, you create a single collision shape representing the collision for a group of tiles. Typically, you should split composite colliders on a per-island basis (which means each group of touching tiles gets its own collider).

Using a composite collider can also improve physics simulation performance in certain cases. However, since the composite collision shape is much more complex, this may not be a net performance win in all cases.

In Godot 4.5 and later, creating a composite collider is automatically done when using a TileMapLayer node. The chunk size (16 tiles on each axis by default) can be set using the Physics Quadrant Size property in the TileMapLayer inspector. Larger values provide more reliable collision, at the cost of slower updates when the TileMap is changed.

This is likely due to one of the objects using a collision shape that is too complex. Convex collision shapes should use a number of shapes as low as possible for performance reasons. When relying on Godot's automatic generation, it's possible that you ended up with dozens if not hundreds of shapes created for a single convex shape collision resource.

In some cases, replacing a convex collider with a couple of primitive collision shapes (box, sphere, or capsule) can deliver better performance.

This issue can also occur with StaticBodies that use very detailed trimesh (concave) collisions. In this case, use a simplified representation of the level geometry as a collider. Not only this will improve physics simulation performance significantly, but this can also improve stability by letting you remove small fixtures and crevices from being considered by collision.

In 3D, switching the physics engine from the default GodotPhysics to Jolt can also improve performance. See Using Jolt Physics for more information.

This occurs because the physics engine can't keep up with the expected simulation rate. In this case, the framerate will start dropping, but the engine is only allowed to simulate a certain number of physics steps per rendered frame. This snowballs into a situation where framerate keeps dropping until it reaches a very low framerate (typically 1-2 FPS) and is called the physics spiral of death.

To avoid this, you should check for situations in your project that can cause excessive number of physics simulations to occur at the same time (or with excessively complex collision shapes). If these situations cannot be avoided, you can increase the Max Physics Steps per Frame project setting and/or reduce Physics Ticks per Second to alleviate this.

This is caused by floating-point precision errors, which become more pronounced as the physics simulation occurs further away from the world origin. This issue also affects rendering, which results in wobbly camera movement when far away from the world origin. See Large world coordinates for more information.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Physics Interpolation — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/physics/interpolation/index.html

**Contents:**
- Physics Interpolation

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Using physics interpolation — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/physics/interpolation/using_physics_interpolation.html

**Contents:**
- Using physics interpolation
- Turn on the physics interpolation setting
- Move (almost) all game logic from _process to _physics_process
- Ensure that all indirect movement happens during physics ticks
- Choose a physics tick rate
- Call reset_physics_interpolation() when teleporting objects
- Testing and debugging tips
- User-contributed notes

How do we incorporate physics interpolation into a Godot game? Are there any caveats?

We have tried to make the system as easy to use as possible, and many existing games will work with few changes. That said there are some situations which require special treatment, and these will be described.

The first step is to turn on physics interpolation in Project Settings > Physics > Common > Physics Interpolation You can now run your game.

It is likely that nothing looks hugely different, particularly if you are running physics at 60 TPS or a multiple of it. However, quite a bit more is happening behind the scenes.

To convert an existing game to use interpolation, it is highly recommended that you temporarily set Project Settings > Physics > Common > Physics Tick per Second to a low value such as 10, which will make interpolation problems more obvious.

The most fundamental requirement for physics interpolation (which you may be doing already) is that you should be moving and performing game logic on your objects within _physics_process (which runs at a physics tick) rather than _process (which runs on a rendered frame). This means your scripts should typically be doing the bulk of their processing within _physics_process, including responding to input and AI.

Setting the transform of objects only within physics ticks allows the automatic interpolation to deal with transforms between physics ticks, and ensures the game will run the same whatever machine it is run on. As a bonus, this also reduces CPU usage if the game is rendering at high FPS, since AI logic (for example) will no longer run on every rendered frame.

If you attempt to set the transform of interpolated objects outside the physics tick, the calculations for the interpolated position will be incorrect, and you will get jitter. This jitter may not be visible on your machine, but it will occur for some players. For this reason, setting the transform of interpolated objects should be avoided outside of the physics tick. Godot will attempt to produce warnings in the editor if this case is detected.

This is only a soft rule. There are some occasions where you might want to teleport objects outside of the physics tick (for instance when starting a level, or respawning objects). Still, in general, you should be applying transforms from the physics tick.

Consider that in Godot, nodes can be moved not just directly in your own scripts, but also by automatic methods such as tweening, animation, and navigation. All these methods should also have their timing set to operate on the physics tick rather than each frame ("idle"), if you are using them to move objects (these methods can also be used to control properties that are not interpolated).

Also consider that nodes can be moved not just by moving themselves, but also by moving parent nodes in the SceneTree. The movement of parents should therefore also only occur during physics ticks.

When using physics interpolation, the rendering is decoupled from physics, and you can choose any value that makes sense for your game. You are no longer limited to values that are multiples of the user's monitor refresh rate (for stutter-free gameplay if the target FPS is reached).

Low tick rates (10-30)

Medium tick rates (30-60)

High tick rates (60+)

Better CPU performance

Good physics behavior in complex scenes

Good with fast physics

Add some delay to input

Good for first person games

Good for racing games

Simple physics behaviour

You can always change the tick rate as you develop, it is as simple as changing the project setting.

Most of the time, interpolation is what you want between two physics ticks. However, there is one situation in which it may not be what you want. That is when you are initially placing objects, or moving them to a new location. Here, you don't want a smooth motion between where the object was (e.g. the origin) and the initial position - you want an instantaneous move.

The solution to this is to call the Node.reset_physics_interpolation function. What this function does under the hood is set the internally stored previous transform of the object to be equal to the current transform. This ensures that when interpolating between these two equal transforms, there will be no movement.

Even if you forget to call this, it will usually not be a problem in most situations (especially at high tick rates). This is something you can easily leave to the polishing phase of your game. The worst that will happen is seeing a streaking motion for a frame or so when you move them - you will know when you need it!

There are actually two ways to use reset_physics_interpolation():

Standing start (e.g. player)

Set the initial transform

Call reset_physics_interpolation()

The previous and current transforms will be identical, resulting in no initial movement.

Moving start (e.g. bullet)

Set the initial transform

Call reset_physics_interpolation()

Immediately set the transform expected after the first tick of motion

The previous transform will be the starting position, and the current transform will act as though a tick of simulation has already taken place. This will immediately start moving the object, instead of having a tick delay standing still.

Make sure you set the transform and call reset_physics_interpolation() in the correct order as shown above, otherwise you will see unwanted "streaking".

Even if you intend to run physics at 60 TPS, in order to thoroughly test your interpolation and get the smoothest gameplay, it is highly recommended to temporarily set the physics tick rate to a low value such as 10 TPS.

The gameplay may not work perfectly, but it should enable you to more easily see cases where you should be calling Node.reset_physics_interpolation, or where you should be using your own custom interpolation on e.g. a Camera3D. Once you have these cases fixed, you can set the physics tick rate back to the desired setting.

The other great advantage to testing at a low tick rate is you can often notice other game systems that are synchronized to the physics tick and creating glitches which you may want to work around. Typical examples include setting animation blend values, which you may decide to set in _process() and interpolate manually.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Collision shapes (2D) — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/physics/collision_shapes_2d.html

**Contents:**
- Collision shapes (2D)
- Primitive collision shapes
- Convex collision shapes
- Concave or trimesh collision shapes
- Performance caveats
- User-contributed notes

The types of collision shapes available in 2D in Godot.

Using an image converted to a polygon as a collision shape.

Performance considerations regarding 2D collisions.

Godot provides many kinds of collision shapes, with different performance and accuracy tradeoffs.

You can define the shape of a PhysicsBody2D by adding one or more CollisionShape2Ds or CollisionPolygon2Ds as direct child nodes. Indirect child nodes (i.e. children of child nodes) will be ignored and won't be used as collision shapes. Also, note that you must add a Shape2D resource to collision shape nodes in the Inspector dock.

When you add multiple collision shapes to a single PhysicsBody2D, you don't have to worry about them overlapping. They won't "collide" with each other.

Godot provides the following primitive collision shape types:

SeparationRayShape2D (designed for characters)

WorldBoundaryShape2D (infinite plane)

You can represent the collision of most smaller objects using one or more primitive shapes. However, for more complex objects, such as a large ship or a whole level, you may need convex or concave shapes instead. More on that below.

We recommend favoring primitive shapes for dynamic objects such as RigidBodies and CharacterBodies as their behavior is the most reliable. They often provide better performance as well.

Godot currently doesn't offer a built-in way to create 2D convex collision shapes. This section is mainly here for reference purposes.

Convex collision shapes are a compromise between primitive collision shapes and concave collision shapes. They can represent shapes of any complexity, but with an important caveat. As their name implies, an individual shape can only represent a convex shape. For instance, a pyramid is convex, but a hollow box is concave. To define a concave object with a single collision shape, you need to use a concave collision shape.

Depending on the object's complexity, you may get better performance by using multiple convex shapes instead of a concave collision shape. Godot lets you use convex decomposition to generate convex shapes that roughly match a hollow object. Note this performance advantage no longer applies after a certain amount of convex shapes. For large and complex objects such as a whole level, we recommend using concave shapes instead.

Concave collision shapes, also called trimesh collision shapes, can take any form, from a few triangles to thousands of triangles. Concave shapes are the slowest option but are also the most accurate in Godot. You can only use concave shapes within StaticBodies. They will not work with CharacterBodies or RigidBodies unless the RigidBody's mode is Static.

Even though concave shapes offer the most accurate collision, contact reporting can be less precise than primitive shapes.

When not using TileMaps for level design, concave shapes are the best approach for a level's collision.

You can configure the CollisionPolygon2D node's build mode in the inspector. If it is set to Solids (the default), collisions will include the polygon and its contained area. If it is set to Segments, collisions will only include the polygon edges.

You can generate a concave collision shape from the editor by selecting a Sprite2D and using the Sprite2D menu at the top of the 2D viewport. The Sprite2D menu dropdown exposes an option called Create CollisionPolygon2D Sibling. Once you click it, it displays a menu with 3 settings:

Simplification: Higher values will result in a less detailed shape, which improves performance at the cost of accuracy.

Shrink (Pixels): Higher values will shrink the generated collision polygon relative to the sprite's edges.

Grow (Pixels): Higher values will grow the generated collision polygon relative to the sprite's edges. Note that setting Grow and Shrink to equal values may yield different results than leaving both of them on 0.

If you have an image with many small details, it's recommended to create a simplified version and use it to generate the collision polygon. This can result in better performance and game feel, since the player won't be blocked by small, decorative details.

To use a separate image for collision polygon generation, create another Sprite2D, generate a collision polygon sibling from it then remove the Sprite2D node. This way, you can exclude small details from the generated collision.

You aren't limited to a single collision shape per PhysicsBody. Still, we recommend keeping the number of shapes as low as possible to improve performance, especially for dynamic objects like RigidBodies and CharacterBodies. On top of that, avoid translating, rotating, or scaling CollisionShapes to benefit from the physics engine's internal optimizations.

When using a single non-transformed collision shape in a StaticBody, the engine's broad phase algorithm can discard inactive PhysicsBodies. The narrow phase will then only have to take into account the active bodies' shapes. If a StaticBody has many collision shapes, the broad phase will fail. The narrow phase, which is slower, must then perform a collision check against each shape.

If you run into performance issues, you may have to make tradeoffs in terms of accuracy. Most games out there don't have a 100% accurate collision. They find creative ways to hide it or otherwise make it unnoticeable during normal gameplay.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Quick start guide — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/physics/interpolation/physics_interpolation_quick_start_guide.html

**Contents:**
- Quick start guide
- User-contributed notes

Turn on physics interpolation: Project Settings > Physics > Common > Physics Interpolation

Make sure you move objects and run your game logic in _physics_process() rather than _process(). This includes moving objects directly and indirectly (by e.g. moving a parent, or using another mechanism to automatically move nodes).

Be sure to call Node.reset_physics_interpolation on nodes after you first position or teleport them, to prevent "streaking".

Temporarily try setting Project Settings > Physics > Common > Physics Tick per Second to 10 to see the difference with and without interpolation.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Collision shapes (3D) — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/physics/collision_shapes_3d.html

**Contents:**
- Collision shapes (3D)
- Primitive collision shapes
- Convex collision shapes
- Concave or trimesh collision shapes
- Performance caveats
- User-contributed notes

The types of collision shapes available in 3D in Godot.

Using a convex or a concave mesh as a collision shape.

Performance considerations regarding 3D collisions.

Godot provides many kinds of collision shapes, with different performance and accuracy tradeoffs.

You can define the shape of a PhysicsBody3D by adding one or more CollisionShape3Ds as direct child nodes. Indirect child nodes (i.e. children of child nodes) will be ignored and won't be used as collision shapes. Also, note that you must add a Shape3D resource to collision shape nodes in the Inspector dock.

When you add multiple collision shapes to a single PhysicsBody, you don't have to worry about them overlapping. They won't "collide" with each other.

Godot provides the following primitive collision shape types:

You can represent the collision of most smaller objects using one or more primitive shapes. However, for more complex objects, such as a large ship or a whole level, you may need convex or concave shapes instead. More on that below.

We recommend favoring primitive shapes for dynamic objects such as RigidBodies and CharacterBodies as their behavior is the most reliable. They often provide better performance as well.

Convex collision shapes are a compromise between primitive collision shapes and concave collision shapes. They can represent shapes of any complexity, but with an important caveat. As their name implies, an individual shape can only represent a convex shape. For instance, a pyramid is convex, but a hollow box is concave. To define a concave object with a single collision shape, you need to use a concave collision shape.

Depending on the object's complexity, you may get better performance by using multiple convex shapes instead of a concave collision shape. Godot lets you use convex decomposition to generate convex shapes that roughly match a hollow object. Note this performance advantage no longer applies after a certain amount of convex shapes. For large and complex objects such as a whole level, we recommend using concave shapes instead.

You can generate one or several convex collision shapes from the editor by selecting a MeshInstance3D and using the Mesh menu at the top of the 3D viewport. The editor exposes two generation modes:

Create Single Convex Collision Sibling uses the Quickhull algorithm. It creates one CollisionShape node with an automatically generated convex collision shape. Since it only generates a single shape, it provides good performance and is ideal for small objects.

Create Multiple Convex Collision Siblings uses the V-HACD algorithm. It creates several CollisionShape nodes, each with a convex shape. Since it generates multiple shapes, it is more accurate for concave objects at the cost of performance. For objects with medium complexity, it will likely be faster than using a single concave collision shape.

Concave collision shapes, also called trimesh collision shapes, can take any form, from a few triangles to thousands of triangles. Concave shapes are the slowest option but are also the most accurate in Godot. You can only use concave shapes within StaticBodies. They will not work with CharacterBodies or RigidBodies unless the RigidBody's mode is Static.

Even though concave shapes offer the most accurate collision, contact reporting can be less precise than primitive shapes.

When not using GridMaps for level design, concave shapes are the best approach for a level's collision. That said, if your level has small details, you may want to exclude those from collision for performance and game feel. To do so, you can build a simplified collision mesh in a 3D modeler and have Godot generate a collision shape for it automatically. More on that below

Note that unlike primitive and convex shapes, a concave collision shape doesn't have an actual "volume". You can place objects both outside of the shape as well as inside.

You can generate a concave collision shape from the editor by selecting a MeshInstance3D and using the Mesh menu at the top of the 3D viewport. The editor exposes two options:

Create Trimesh Static Body is a convenient option. It creates a StaticBody containing a concave shape matching the mesh's geometry.

Create Trimesh Collision Sibling creates a CollisionShape node with a concave shape matching the mesh's geometry.

See Importing 3D scenes for information on how to export models for Godot and automatically generate collision shapes on import.

You aren't limited to a single collision shape per PhysicsBody. Still, we recommend keeping the number of shapes as low as possible to improve performance, especially for dynamic objects like RigidBodies and CharacterBodies. On top of that, avoid translating, rotating, or scaling CollisionShapes to benefit from the physics engine's internal optimizations.

When using a single non-transformed collision shape in a StaticBody, the engine's broad phase algorithm can discard inactive PhysicsBodies. The narrow phase will then only have to take into account the active bodies' shapes. If a StaticBody has many collision shapes, the broad phase will fail. The narrow phase, which is slower, must then perform a collision check against each shape.

If you run into performance issues, you may have to make tradeoffs in terms of accuracy. Most games out there don't have a 100% accurate collision. They find creative ways to hide it or otherwise make it unnoticeable during normal gameplay.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## AnimatableBody2D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_animatablebody2d.html

**Contents:**
- AnimatableBody2D
- Description
- Tutorials
- Properties
- Property Descriptions
- User-contributed notes

Inherits: StaticBody2D < PhysicsBody2D < CollisionObject2D < Node2D < CanvasItem < Node < Object

A 2D physics body that can't be moved by external forces. When moved manually, it affects other bodies in its path.

An animatable 2D physics body. It can't be moved by external forces or contacts, but can be moved manually by other means such as code, AnimationMixers (with AnimationMixer.callback_mode_process set to AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS), and RemoteTransform2D.

When AnimatableBody2D is moved, its linear and angular velocity are estimated and used to affect other physics bodies in its path. This makes it useful for moving platforms, doors, and other moving objects.

Troubleshooting physics issues

bool sync_to_physics = true 🔗

void set_sync_to_physics(value: bool)

bool is_sync_to_physics_enabled()

If true, the body's movement will be synchronized to the physics frame. This is useful when animating movement via AnimationPlayer, for example on moving platforms. Do not use together with PhysicsBody2D.move_and_collide().

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## AnimatableBody3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_animatablebody3d.html

**Contents:**
- AnimatableBody3D
- Description
- Tutorials
- Properties
- Property Descriptions
- User-contributed notes

Inherits: StaticBody3D < PhysicsBody3D < CollisionObject3D < Node3D < Node < Object

A 3D physics body that can't be moved by external forces. When moved manually, it affects other bodies in its path.

An animatable 3D physics body. It can't be moved by external forces or contacts, but can be moved manually by other means such as code, AnimationMixers (with AnimationMixer.callback_mode_process set to AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS), and RemoteTransform3D.

When AnimatableBody3D is moved, its linear and angular velocity are estimated and used to affect other physics bodies in its path. This makes it useful for moving platforms, doors, and other moving objects.

Troubleshooting physics issues

3D Physics Tests Demo

Third Person Shooter (TPS) Demo

bool sync_to_physics = true 🔗

void set_sync_to_physics(value: bool)

bool is_sync_to_physics_enabled()

If true, the body's movement will be synchronized to the physics frame. This is useful when animating movement via AnimationPlayer, for example on moving platforms. Do not use together with PhysicsBody3D.move_and_collide().

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Area2D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_area2d.html

**Contents:**
- Area2D
- Description
- Tutorials
- Properties
- Methods
- Signals
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: CollisionObject2D < Node2D < CanvasItem < Node < Object

A region of 2D space that detects other CollisionObject2Ds entering or exiting it.

Area2D is a region of 2D space defined by one or multiple CollisionShape2D or CollisionPolygon2D child nodes. It detects when other CollisionObject2Ds enter or exit it, and it also keeps track of which collision objects haven't exited it yet (i.e. which one are overlapping it).

This node can also locally alter or override physics parameters (gravity, damping) and route audio to custom audio buses.

Note: Areas and bodies created with PhysicsServer2D might not interact as expected with Area2Ds, and might not emit signals or track objects correctly.

2D Dodge The Creeps Demo

angular_damp_space_override

gravity_point_unit_distance

gravity_space_override

linear_damp_space_override

get_overlapping_areas() const

get_overlapping_bodies() const

has_overlapping_areas() const

has_overlapping_bodies() const

overlaps_area(area: Node) const

overlaps_body(body: Node) const

area_entered(area: Area2D) 🔗

Emitted when the received area enters this area. Requires monitoring to be set to true.

area_exited(area: Area2D) 🔗

Emitted when the received area exits this area. Requires monitoring to be set to true.

area_shape_entered(area_rid: RID, area: Area2D, area_shape_index: int, local_shape_index: int) 🔗

Emitted when a Shape2D of the received area enters a shape of this area. Requires monitoring to be set to true.

local_shape_index and area_shape_index contain indices of the interacting shapes from this area and the other area, respectively. area_rid contains the RID of the other area. These values can be used with the PhysicsServer2D.

Example: Get the CollisionShape2D node from the shape index:

area_shape_exited(area_rid: RID, area: Area2D, area_shape_index: int, local_shape_index: int) 🔗

Emitted when a Shape2D of the received area exits a shape of this area. Requires monitoring to be set to true.

See also area_shape_entered.

body_entered(body: Node2D) 🔗

Emitted when the received body enters this area. body can be a PhysicsBody2D or a TileMap. TileMaps are detected if their TileSet has collision shapes configured. Requires monitoring to be set to true.

body_exited(body: Node2D) 🔗

Emitted when the received body exits this area. body can be a PhysicsBody2D or a TileMap. TileMaps are detected if their TileSet has collision shapes configured. Requires monitoring to be set to true.

body_shape_entered(body_rid: RID, body: Node2D, body_shape_index: int, local_shape_index: int) 🔗

Emitted when a Shape2D of the received body enters a shape of this area. body can be a PhysicsBody2D or a TileMap. TileMaps are detected if their TileSet has collision shapes configured. Requires monitoring to be set to true.

local_shape_index and body_shape_index contain indices of the interacting shapes from this area and the interacting body, respectively. body_rid contains the RID of the body. These values can be used with the PhysicsServer2D.

Example: Get the CollisionShape2D node from the shape index:

body_shape_exited(body_rid: RID, body: Node2D, body_shape_index: int, local_shape_index: int) 🔗

Emitted when a Shape2D of the received body exits a shape of this area. body can be a PhysicsBody2D or a TileMap. TileMaps are detected if their TileSet has collision shapes configured. Requires monitoring to be set to true.

See also body_shape_entered.

enum SpaceOverride: 🔗

SpaceOverride SPACE_OVERRIDE_DISABLED = 0

This area does not affect gravity/damping.

SpaceOverride SPACE_OVERRIDE_COMBINE = 1

This area adds its gravity/damping values to whatever has been calculated so far (in priority order).

SpaceOverride SPACE_OVERRIDE_COMBINE_REPLACE = 2

This area adds its gravity/damping values to whatever has been calculated so far (in priority order), ignoring any lower priority areas.

SpaceOverride SPACE_OVERRIDE_REPLACE = 3

This area replaces any gravity/damping, even the defaults, ignoring any lower priority areas.

SpaceOverride SPACE_OVERRIDE_REPLACE_COMBINE = 4

This area replaces any gravity/damping calculated so far (in priority order), but keeps calculating the rest of the areas.

float angular_damp = 1.0 🔗

void set_angular_damp(value: float)

float get_angular_damp()

The rate at which objects stop spinning in this area. Represents the angular velocity lost per second.

See ProjectSettings.physics/2d/default_angular_damp for more details about damping.

SpaceOverride angular_damp_space_override = 0 🔗

void set_angular_damp_space_override_mode(value: SpaceOverride)

SpaceOverride get_angular_damp_space_override_mode()

Override mode for angular damping calculations within this area.

StringName audio_bus_name = &"Master" 🔗

void set_audio_bus_name(value: StringName)

StringName get_audio_bus_name()

The name of the area's audio bus.

bool audio_bus_override = false 🔗

void set_audio_bus_override(value: bool)

bool is_overriding_audio_bus()

If true, the area's audio bus overrides the default audio bus.

float gravity = 980.0 🔗

void set_gravity(value: float)

The area's gravity intensity (in pixels per second squared). This value multiplies the gravity direction. This is useful to alter the force of gravity without altering its direction.

Vector2 gravity_direction = Vector2(0, 1) 🔗

void set_gravity_direction(value: Vector2)

Vector2 get_gravity_direction()

The area's gravity vector (not normalized).

bool gravity_point = false 🔗

void set_gravity_is_point(value: bool)

bool is_gravity_a_point()

If true, gravity is calculated from a point (set via gravity_point_center). See also gravity_space_override.

Vector2 gravity_point_center = Vector2(0, 1) 🔗

void set_gravity_point_center(value: Vector2)

Vector2 get_gravity_point_center()

If gravity is a point (see gravity_point), this will be the point of attraction.

float gravity_point_unit_distance = 0.0 🔗

void set_gravity_point_unit_distance(value: float)

float get_gravity_point_unit_distance()

The distance at which the gravity strength is equal to gravity. For example, on a planet 100 pixels in radius with a surface gravity of 4.0 px/s², set the gravity to 4.0 and the unit distance to 100.0. The gravity will have falloff according to the inverse square law, so in the example, at 200 pixels from the center the gravity will be 1.0 px/s² (twice the distance, 1/4th the gravity), at 50 pixels it will be 16.0 px/s² (half the distance, 4x the gravity), and so on.

The above is true only when the unit distance is a positive number. When this is set to 0.0, the gravity will be constant regardless of distance.

SpaceOverride gravity_space_override = 0 🔗

void set_gravity_space_override_mode(value: SpaceOverride)

SpaceOverride get_gravity_space_override_mode()

Override mode for gravity calculations within this area.

float linear_damp = 0.1 🔗

void set_linear_damp(value: float)

float get_linear_damp()

The rate at which objects stop moving in this area. Represents the linear velocity lost per second.

See ProjectSettings.physics/2d/default_linear_damp for more details about damping.

SpaceOverride linear_damp_space_override = 0 🔗

void set_linear_damp_space_override_mode(value: SpaceOverride)

SpaceOverride get_linear_damp_space_override_mode()

Override mode for linear damping calculations within this area.

bool monitorable = true 🔗

void set_monitorable(value: bool)

bool is_monitorable()

If true, other monitoring areas can detect this area.

bool monitoring = true 🔗

void set_monitoring(value: bool)

If true, the area detects bodies or areas entering and exiting it.

void set_priority(value: int)

The area's priority. Higher priority areas are processed first. The World2D's physics is always processed last, after all areas.

Array[Area2D] get_overlapping_areas() const 🔗

Returns a list of intersecting Area2Ds. The overlapping area's CollisionObject2D.collision_layer must be part of this area's CollisionObject2D.collision_mask in order to be detected.

For performance reasons (collisions are all processed at the same time) this list is modified once during the physics step, not immediately after objects are moved. Consider using signals instead.

Array[Node2D] get_overlapping_bodies() const 🔗

Returns a list of intersecting PhysicsBody2Ds and TileMaps. The overlapping body's CollisionObject2D.collision_layer must be part of this area's CollisionObject2D.collision_mask in order to be detected.

For performance reasons (collisions are all processed at the same time) this list is modified once during the physics step, not immediately after objects are moved. Consider using signals instead.

bool has_overlapping_areas() const 🔗

Returns true if intersecting any Area2Ds, otherwise returns false. The overlapping area's CollisionObject2D.collision_layer must be part of this area's CollisionObject2D.collision_mask in order to be detected.

For performance reasons (collisions are all processed at the same time) the list of overlapping areas is modified once during the physics step, not immediately after objects are moved. Consider using signals instead.

bool has_overlapping_bodies() const 🔗

Returns true if intersecting any PhysicsBody2Ds or TileMaps, otherwise returns false. The overlapping body's CollisionObject2D.collision_layer must be part of this area's CollisionObject2D.collision_mask in order to be detected.

For performance reasons (collisions are all processed at the same time) the list of overlapping bodies is modified once during the physics step, not immediately after objects are moved. Consider using signals instead.

bool overlaps_area(area: Node) const 🔗

Returns true if the given Area2D intersects or overlaps this Area2D, false otherwise.

Note: The result of this test is not immediate after moving objects. For performance, the list of overlaps is updated once per frame and before the physics step. Consider using signals instead.

bool overlaps_body(body: Node) const 🔗

Returns true if the given physics body intersects or overlaps this Area2D, false otherwise.

Note: The result of this test is not immediate after moving objects. For performance, list of overlaps is updated once per frame and before the physics step. Consider using signals instead.

The body argument can either be a PhysicsBody2D or a TileMap instance. While TileMaps are not physics bodies themselves, they register their tiles with collision shapes as a virtual physics body.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
var other_shape_owner = area.shape_find_owner(area_shape_index)
var other_shape_node = area.shape_owner_get_owner(other_shape_owner)

var local_shape_owner = shape_find_owner(local_shape_index)
var local_shape_node = shape_owner_get_owner(local_shape_owner)
```

Example 2 (gdscript):
```gdscript
var body_shape_owner = body.shape_find_owner(body_shape_index)
var body_shape_node = body.shape_owner_get_owner(body_shape_owner)

var local_shape_owner = shape_find_owner(local_shape_index)
var local_shape_node = shape_owner_get_owner(local_shape_owner)
```

---

## Area3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_area3d.html

**Contents:**
- Area3D
- Description
- Tutorials
- Properties
- Methods
- Signals
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: CollisionObject3D < Node3D < Node < Object

A region of 3D space that detects other CollisionObject3Ds entering or exiting it.

Area3D is a region of 3D space defined by one or multiple CollisionShape3D or CollisionPolygon3D child nodes. It detects when other CollisionObject3Ds enter or exit it, and it also keeps track of which collision objects haven't exited it yet (i.e. which one are overlapping it).

This node can also locally alter or override physics parameters (gravity, damping) and route audio to custom audio buses.

Note: Areas and bodies created with PhysicsServer3D might not interact as expected with Area3Ds, and might not emit signals or track objects correctly.

Warning: Using a ConcavePolygonShape3D inside a CollisionShape3D child of this node (created e.g. by using the Create Trimesh Collision Sibling option in the Mesh menu that appears when selecting a MeshInstance3D node) may give unexpected results, since this collision shape is hollow. If this is not desired, it has to be split into multiple ConvexPolygonShape3Ds or primitive shapes like BoxShape3D, or in some cases it may be replaceable by a CollisionPolygon3D.

GUI in 3D Viewport Demo

angular_damp_space_override

gravity_point_unit_distance

gravity_space_override

linear_damp_space_override

reverb_bus_uniformity

wind_attenuation_factor

get_overlapping_areas() const

get_overlapping_bodies() const

has_overlapping_areas() const

has_overlapping_bodies() const

overlaps_area(area: Node) const

overlaps_body(body: Node) const

area_entered(area: Area3D) 🔗

Emitted when the received area enters this area. Requires monitoring to be set to true.

area_exited(area: Area3D) 🔗

Emitted when the received area exits this area. Requires monitoring to be set to true.

area_shape_entered(area_rid: RID, area: Area3D, area_shape_index: int, local_shape_index: int) 🔗

Emitted when a Shape3D of the received area enters a shape of this area. Requires monitoring to be set to true.

local_shape_index and area_shape_index contain indices of the interacting shapes from this area and the other area, respectively. area_rid contains the RID of the other area. These values can be used with the PhysicsServer3D.

Example: Get the CollisionShape3D node from the shape index:

area_shape_exited(area_rid: RID, area: Area3D, area_shape_index: int, local_shape_index: int) 🔗

Emitted when a Shape3D of the received area exits a shape of this area. Requires monitoring to be set to true.

See also area_shape_entered.

body_entered(body: Node3D) 🔗

Emitted when the received body enters this area. body can be a PhysicsBody3D or a GridMap. GridMaps are detected if their MeshLibrary has collision shapes configured. Requires monitoring to be set to true.

body_exited(body: Node3D) 🔗

Emitted when the received body exits this area. body can be a PhysicsBody3D or a GridMap. GridMaps are detected if their MeshLibrary has collision shapes configured. Requires monitoring to be set to true.

body_shape_entered(body_rid: RID, body: Node3D, body_shape_index: int, local_shape_index: int) 🔗

Emitted when a Shape3D of the received body enters a shape of this area. body can be a PhysicsBody3D or a GridMap. GridMaps are detected if their MeshLibrary has collision shapes configured. Requires monitoring to be set to true.

local_shape_index and body_shape_index contain indices of the interacting shapes from this area and the interacting body, respectively. body_rid contains the RID of the body. These values can be used with the PhysicsServer3D.

Example: Get the CollisionShape3D node from the shape index:

body_shape_exited(body_rid: RID, body: Node3D, body_shape_index: int, local_shape_index: int) 🔗

Emitted when a Shape3D of the received body exits a shape of this area. body can be a PhysicsBody3D or a GridMap. GridMaps are detected if their MeshLibrary has collision shapes configured. Requires monitoring to be set to true.

See also body_shape_entered.

enum SpaceOverride: 🔗

SpaceOverride SPACE_OVERRIDE_DISABLED = 0

This area does not affect gravity/damping.

SpaceOverride SPACE_OVERRIDE_COMBINE = 1

This area adds its gravity/damping values to whatever has been calculated so far (in priority order).

SpaceOverride SPACE_OVERRIDE_COMBINE_REPLACE = 2

This area adds its gravity/damping values to whatever has been calculated so far (in priority order), ignoring any lower priority areas.

SpaceOverride SPACE_OVERRIDE_REPLACE = 3

This area replaces any gravity/damping, even the defaults, ignoring any lower priority areas.

SpaceOverride SPACE_OVERRIDE_REPLACE_COMBINE = 4

This area replaces any gravity/damping calculated so far (in priority order), but keeps calculating the rest of the areas.

float angular_damp = 0.1 🔗

void set_angular_damp(value: float)

float get_angular_damp()

The rate at which objects stop spinning in this area. Represents the angular velocity lost per second.

See ProjectSettings.physics/3d/default_angular_damp for more details about damping.

SpaceOverride angular_damp_space_override = 0 🔗

void set_angular_damp_space_override_mode(value: SpaceOverride)

SpaceOverride get_angular_damp_space_override_mode()

Override mode for angular damping calculations within this area.

StringName audio_bus_name = &"Master" 🔗

void set_audio_bus_name(value: StringName)

StringName get_audio_bus_name()

The name of the area's audio bus.

bool audio_bus_override = false 🔗

void set_audio_bus_override(value: bool)

bool is_overriding_audio_bus()

If true, the area's audio bus overrides the default audio bus.

float gravity = 9.8 🔗

void set_gravity(value: float)

The area's gravity intensity (in meters per second squared). This value multiplies the gravity direction. This is useful to alter the force of gravity without altering its direction.

Vector3 gravity_direction = Vector3(0, -1, 0) 🔗

void set_gravity_direction(value: Vector3)

Vector3 get_gravity_direction()

The area's gravity vector (not normalized).

bool gravity_point = false 🔗

void set_gravity_is_point(value: bool)

bool is_gravity_a_point()

If true, gravity is calculated from a point (set via gravity_point_center). See also gravity_space_override.

Vector3 gravity_point_center = Vector3(0, -1, 0) 🔗

void set_gravity_point_center(value: Vector3)

Vector3 get_gravity_point_center()

If gravity is a point (see gravity_point), this will be the point of attraction.

float gravity_point_unit_distance = 0.0 🔗

void set_gravity_point_unit_distance(value: float)

float get_gravity_point_unit_distance()

The distance at which the gravity strength is equal to gravity. For example, on a planet 100 meters in radius with a surface gravity of 4.0 m/s², set the gravity to 4.0 and the unit distance to 100.0. The gravity will have falloff according to the inverse square law, so in the example, at 200 meters from the center the gravity will be 1.0 m/s² (twice the distance, 1/4th the gravity), at 50 meters it will be 16.0 m/s² (half the distance, 4x the gravity), and so on.

The above is true only when the unit distance is a positive number. When this is set to 0.0, the gravity will be constant regardless of distance.

SpaceOverride gravity_space_override = 0 🔗

void set_gravity_space_override_mode(value: SpaceOverride)

SpaceOverride get_gravity_space_override_mode()

Override mode for gravity calculations within this area.

float linear_damp = 0.1 🔗

void set_linear_damp(value: float)

float get_linear_damp()

The rate at which objects stop moving in this area. Represents the linear velocity lost per second.

See ProjectSettings.physics/3d/default_linear_damp for more details about damping.

SpaceOverride linear_damp_space_override = 0 🔗

void set_linear_damp_space_override_mode(value: SpaceOverride)

SpaceOverride get_linear_damp_space_override_mode()

Override mode for linear damping calculations within this area.

bool monitorable = true 🔗

void set_monitorable(value: bool)

bool is_monitorable()

If true, other monitoring areas can detect this area.

bool monitoring = true 🔗

void set_monitoring(value: bool)

If true, the area detects bodies or areas entering and exiting it.

void set_priority(value: int)

The area's priority. Higher priority areas are processed first. The World3D's physics is always processed last, after all areas.

float reverb_bus_amount = 0.0 🔗

void set_reverb_amount(value: float)

float get_reverb_amount()

The degree to which this area applies reverb to its associated audio. Ranges from 0 to 1 with 0.1 precision.

bool reverb_bus_enabled = false 🔗

void set_use_reverb_bus(value: bool)

bool is_using_reverb_bus()

If true, the area applies reverb to its associated audio.

StringName reverb_bus_name = &"Master" 🔗

void set_reverb_bus_name(value: StringName)

StringName get_reverb_bus_name()

The name of the reverb bus to use for this area's associated audio.

float reverb_bus_uniformity = 0.0 🔗

void set_reverb_uniformity(value: float)

float get_reverb_uniformity()

The degree to which this area's reverb is a uniform effect. Ranges from 0 to 1 with 0.1 precision.

float wind_attenuation_factor = 0.0 🔗

void set_wind_attenuation_factor(value: float)

float get_wind_attenuation_factor()

The exponential rate at which wind force decreases with distance from its origin.

Note: This wind force only applies to SoftBody3D nodes. Other physics bodies are currently not affected by wind.

float wind_force_magnitude = 0.0 🔗

void set_wind_force_magnitude(value: float)

float get_wind_force_magnitude()

The magnitude of area-specific wind force.

Note: This wind force only applies to SoftBody3D nodes. Other physics bodies are currently not affected by wind.

NodePath wind_source_path = NodePath("") 🔗

void set_wind_source_path(value: NodePath)

NodePath get_wind_source_path()

The Node3D which is used to specify the direction and origin of an area-specific wind force. The direction is opposite to the z-axis of the Node3D's local transform, and its origin is the origin of the Node3D's local transform.

Note: This wind force only applies to SoftBody3D nodes. Other physics bodies are currently not affected by wind.

Array[Area3D] get_overlapping_areas() const 🔗

Returns a list of intersecting Area3Ds. The overlapping area's CollisionObject3D.collision_layer must be part of this area's CollisionObject3D.collision_mask in order to be detected.

For performance reasons (collisions are all processed at the same time) this list is modified once during the physics step, not immediately after objects are moved. Consider using signals instead.

Array[Node3D] get_overlapping_bodies() const 🔗

Returns a list of intersecting PhysicsBody3Ds and GridMaps. The overlapping body's CollisionObject3D.collision_layer must be part of this area's CollisionObject3D.collision_mask in order to be detected.

For performance reasons (collisions are all processed at the same time) this list is modified once during the physics step, not immediately after objects are moved. Consider using signals instead.

bool has_overlapping_areas() const 🔗

Returns true if intersecting any Area3Ds, otherwise returns false. The overlapping area's CollisionObject3D.collision_layer must be part of this area's CollisionObject3D.collision_mask in order to be detected.

For performance reasons (collisions are all processed at the same time) the list of overlapping areas is modified once during the physics step, not immediately after objects are moved. Consider using signals instead.

bool has_overlapping_bodies() const 🔗

Returns true if intersecting any PhysicsBody3Ds or GridMaps, otherwise returns false. The overlapping body's CollisionObject3D.collision_layer must be part of this area's CollisionObject3D.collision_mask in order to be detected.

For performance reasons (collisions are all processed at the same time) the list of overlapping bodies is modified once during the physics step, not immediately after objects are moved. Consider using signals instead.

bool overlaps_area(area: Node) const 🔗

Returns true if the given Area3D intersects or overlaps this Area3D, false otherwise.

Note: The result of this test is not immediate after moving objects. For performance, list of overlaps is updated once per frame and before the physics step. Consider using signals instead.

bool overlaps_body(body: Node) const 🔗

Returns true if the given physics body intersects or overlaps this Area3D, false otherwise.

Note: The result of this test is not immediate after moving objects. For performance, list of overlaps is updated once per frame and before the physics step. Consider using signals instead.

The body argument can either be a PhysicsBody3D or a GridMap instance. While GridMaps are not physics body themselves, they register their tiles with collision shapes as a virtual physics body.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
var other_shape_owner = area.shape_find_owner(area_shape_index)
var other_shape_node = area.shape_owner_get_owner(other_shape_owner)

var local_shape_owner = shape_find_owner(local_shape_index)
var local_shape_node = shape_owner_get_owner(local_shape_owner)
```

Example 2 (gdscript):
```gdscript
var body_shape_owner = body.shape_find_owner(body_shape_index)
var body_shape_node = body.shape_owner_get_owner(body_shape_owner)

var local_shape_owner = shape_find_owner(local_shape_index)
var local_shape_node = shape_owner_get_owner(local_shape_owner)
```

---

## CollisionObject2D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_collisionobject2d.html

**Contents:**
- CollisionObject2D
- Description
- Properties
- Methods
- Signals
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: Node2D < CanvasItem < Node < Object

Inherited By: Area2D, PhysicsBody2D

Abstract base class for 2D physics objects.

Abstract base class for 2D physics objects. CollisionObject2D can hold any number of Shape2Ds for collision. Each shape must be assigned to a shape owner. Shape owners are not nodes and do not appear in the editor, but are accessible through code using the shape_owner_* methods.

Note: Only collisions between objects within the same canvas (Viewport canvas or CanvasLayer) are supported. The behavior of collisions between objects in different canvases is undefined.

_input_event(viewport: Viewport, event: InputEvent, shape_idx: int) virtual

_mouse_enter() virtual

_mouse_exit() virtual

_mouse_shape_enter(shape_idx: int) virtual

_mouse_shape_exit(shape_idx: int) virtual

create_shape_owner(owner: Object)

get_collision_layer_value(layer_number: int) const

get_collision_mask_value(layer_number: int) const

get_shape_owner_one_way_collision_margin(owner_id: int) const

is_shape_owner_disabled(owner_id: int) const

is_shape_owner_one_way_collision_enabled(owner_id: int) const

remove_shape_owner(owner_id: int)

set_collision_layer_value(layer_number: int, value: bool)

set_collision_mask_value(layer_number: int, value: bool)

shape_find_owner(shape_index: int) const

shape_owner_add_shape(owner_id: int, shape: Shape2D)

shape_owner_clear_shapes(owner_id: int)

shape_owner_get_owner(owner_id: int) const

shape_owner_get_shape(owner_id: int, shape_id: int) const

shape_owner_get_shape_count(owner_id: int) const

shape_owner_get_shape_index(owner_id: int, shape_id: int) const

shape_owner_get_transform(owner_id: int) const

shape_owner_remove_shape(owner_id: int, shape_id: int)

shape_owner_set_disabled(owner_id: int, disabled: bool)

shape_owner_set_one_way_collision(owner_id: int, enable: bool)

shape_owner_set_one_way_collision_margin(owner_id: int, margin: float)

shape_owner_set_transform(owner_id: int, transform: Transform2D)

input_event(viewport: Node, event: InputEvent, shape_idx: int) 🔗

Emitted when an input event occurs. Requires input_pickable to be true and at least one collision_layer bit to be set. See _input_event() for details.

Emitted when the mouse pointer enters any of this object's shapes. Requires input_pickable to be true and at least one collision_layer bit to be set. Note that moving between different shapes within a single CollisionObject2D won't cause this signal to be emitted.

Note: Due to the lack of continuous collision detection, this signal may not be emitted in the expected order if the mouse moves fast enough and the CollisionObject2D's area is small. This signal may also not be emitted if another CollisionObject2D is overlapping the CollisionObject2D in question.

Emitted when the mouse pointer exits all this object's shapes. Requires input_pickable to be true and at least one collision_layer bit to be set. Note that moving between different shapes within a single CollisionObject2D won't cause this signal to be emitted.

Note: Due to the lack of continuous collision detection, this signal may not be emitted in the expected order if the mouse moves fast enough and the CollisionObject2D's area is small. This signal may also not be emitted if another CollisionObject2D is overlapping the CollisionObject2D in question.

mouse_shape_entered(shape_idx: int) 🔗

Emitted when the mouse pointer enters any of this object's shapes or moves from one shape to another. shape_idx is the child index of the newly entered Shape2D. Requires input_pickable to be true and at least one collision_layer bit to be set.

mouse_shape_exited(shape_idx: int) 🔗

Emitted when the mouse pointer exits any of this object's shapes. shape_idx is the child index of the exited Shape2D. Requires input_pickable to be true and at least one collision_layer bit to be set.

DisableMode DISABLE_MODE_REMOVE = 0

When Node.process_mode is set to Node.PROCESS_MODE_DISABLED, remove from the physics simulation to stop all physics interactions with this CollisionObject2D.

Automatically re-added to the physics simulation when the Node is processed again.

DisableMode DISABLE_MODE_MAKE_STATIC = 1

When Node.process_mode is set to Node.PROCESS_MODE_DISABLED, make the body static. Doesn't affect Area2D. PhysicsBody2D can't be affected by forces or other bodies while static.

Automatically set PhysicsBody2D back to its original mode when the Node is processed again.

DisableMode DISABLE_MODE_KEEP_ACTIVE = 2

When Node.process_mode is set to Node.PROCESS_MODE_DISABLED, do not affect the physics simulation.

int collision_layer = 1 🔗

void set_collision_layer(value: int)

int get_collision_layer()

The physics layers this CollisionObject2D is in. Collision objects can exist in one or more of 32 different layers. See also collision_mask.

Note: Object A can detect a contact with object B only if object B is in any of the layers that object A scans. See Collision layers and masks in the documentation for more information.

int collision_mask = 1 🔗

void set_collision_mask(value: int)

int get_collision_mask()

The physics layers this CollisionObject2D scans. Collision objects can scan one or more of 32 different layers. See also collision_layer.

Note: Object A can detect a contact with object B only if object B is in any of the layers that object A scans. See Collision layers and masks in the documentation for more information.

float collision_priority = 1.0 🔗

void set_collision_priority(value: float)

float get_collision_priority()

The priority used to solve colliding when occurring penetration. The higher the priority is, the lower the penetration into the object will be. This can for example be used to prevent the player from breaking through the boundaries of a level.

DisableMode disable_mode = 0 🔗

void set_disable_mode(value: DisableMode)

DisableMode get_disable_mode()

Defines the behavior in physics when Node.process_mode is set to Node.PROCESS_MODE_DISABLED.

bool input_pickable = true 🔗

void set_pickable(value: bool)

If true, this object is pickable. A pickable object can detect the mouse pointer entering/leaving, and if the mouse is inside it, report input events. Requires at least one collision_layer bit to be set.

void _input_event(viewport: Viewport, event: InputEvent, shape_idx: int) virtual 🔗

Accepts unhandled InputEvents. shape_idx is the child index of the clicked Shape2D. Connect to input_event to easily pick up these events.

Note: _input_event() requires input_pickable to be true and at least one collision_layer bit to be set.

void _mouse_enter() virtual 🔗

Called when the mouse pointer enters any of this object's shapes. Requires input_pickable to be true and at least one collision_layer bit to be set. Note that moving between different shapes within a single CollisionObject2D won't cause this function to be called.

void _mouse_exit() virtual 🔗

Called when the mouse pointer exits all this object's shapes. Requires input_pickable to be true and at least one collision_layer bit to be set. Note that moving between different shapes within a single CollisionObject2D won't cause this function to be called.

void _mouse_shape_enter(shape_idx: int) virtual 🔗

Called when the mouse pointer enters any of this object's shapes or moves from one shape to another. shape_idx is the child index of the newly entered Shape2D. Requires input_pickable to be true and at least one collision_layer bit to be called.

void _mouse_shape_exit(shape_idx: int) virtual 🔗

Called when the mouse pointer exits any of this object's shapes. shape_idx is the child index of the exited Shape2D. Requires input_pickable to be true and at least one collision_layer bit to be called.

int create_shape_owner(owner: Object) 🔗

Creates a new shape owner for the given object. Returns owner_id of the new owner for future reference.

bool get_collision_layer_value(layer_number: int) const 🔗

Returns whether or not the specified layer of the collision_layer is enabled, given a layer_number between 1 and 32.

bool get_collision_mask_value(layer_number: int) const 🔗

Returns whether or not the specified layer of the collision_mask is enabled, given a layer_number between 1 and 32.

RID get_rid() const 🔗

Returns the object's RID.

float get_shape_owner_one_way_collision_margin(owner_id: int) const 🔗

Returns the one_way_collision_margin of the shape owner identified by given owner_id.

PackedInt32Array get_shape_owners() 🔗

Returns an Array of owner_id identifiers. You can use these ids in other methods that take owner_id as an argument.

bool is_shape_owner_disabled(owner_id: int) const 🔗

If true, the shape owner and its shapes are disabled.

bool is_shape_owner_one_way_collision_enabled(owner_id: int) const 🔗

Returns true if collisions for the shape owner originating from this CollisionObject2D will not be reported to collided with CollisionObject2Ds.

void remove_shape_owner(owner_id: int) 🔗

Removes the given shape owner.

void set_collision_layer_value(layer_number: int, value: bool) 🔗

Based on value, enables or disables the specified layer in the collision_layer, given a layer_number between 1 and 32.

void set_collision_mask_value(layer_number: int, value: bool) 🔗

Based on value, enables or disables the specified layer in the collision_mask, given a layer_number between 1 and 32.

int shape_find_owner(shape_index: int) const 🔗

Returns the owner_id of the given shape.

void shape_owner_add_shape(owner_id: int, shape: Shape2D) 🔗

Adds a Shape2D to the shape owner.

void shape_owner_clear_shapes(owner_id: int) 🔗

Removes all shapes from the shape owner.

Object shape_owner_get_owner(owner_id: int) const 🔗

Returns the parent object of the given shape owner.

Shape2D shape_owner_get_shape(owner_id: int, shape_id: int) const 🔗

Returns the Shape2D with the given ID from the given shape owner.

int shape_owner_get_shape_count(owner_id: int) const 🔗

Returns the number of shapes the given shape owner contains.

int shape_owner_get_shape_index(owner_id: int, shape_id: int) const 🔗

Returns the child index of the Shape2D with the given ID from the given shape owner.

Transform2D shape_owner_get_transform(owner_id: int) const 🔗

Returns the shape owner's Transform2D.

void shape_owner_remove_shape(owner_id: int, shape_id: int) 🔗

Removes a shape from the given shape owner.

void shape_owner_set_disabled(owner_id: int, disabled: bool) 🔗

If true, disables the given shape owner.

void shape_owner_set_one_way_collision(owner_id: int, enable: bool) 🔗

If enable is true, collisions for the shape owner originating from this CollisionObject2D will not be reported to collided with CollisionObject2Ds.

void shape_owner_set_one_way_collision_margin(owner_id: int, margin: float) 🔗

Sets the one_way_collision_margin of the shape owner identified by given owner_id to margin pixels.

void shape_owner_set_transform(owner_id: int, transform: Transform2D) 🔗

Sets the Transform2D of the given shape owner.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CharacterBody3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_characterbody3d.html

**Contents:**
- CharacterBody3D
- Description
- Tutorials
- Properties
- Methods
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: PhysicsBody3D < CollisionObject3D < Node3D < Node < Object

A 3D physics body specialized for characters moved by script.

CharacterBody3D is a specialized class for physics bodies that are meant to be user-controlled. They are not affected by physics at all, but they affect other physics bodies in their path. They are mainly used to provide high-level API to move objects with wall and slope detection (move_and_slide() method) in addition to the general collision detection provided by PhysicsBody3D.move_and_collide(). This makes it useful for highly configurable physics bodies that must move in specific ways and collide with the world, as is often the case with user-controlled characters.

For game objects that don't require complex movement or collision detection, such as moving platforms, AnimatableBody3D is simpler to configure.

Troubleshooting physics issues

Kinematic character (2D)

3D Kinematic Character Demo

Third Person Shooter (TPS) Demo

platform_floor_layers

get_floor_angle(up_direction: Vector3 = Vector3(0, 1, 0)) const

get_floor_normal() const

get_last_motion() const

get_last_slide_collision()

get_platform_angular_velocity() const

get_platform_velocity() const

get_position_delta() const

get_real_velocity() const

get_slide_collision(slide_idx: int)

get_slide_collision_count() const

get_wall_normal() const

is_on_ceiling() const

is_on_ceiling_only() const

is_on_floor_only() const

is_on_wall_only() const

MotionMode MOTION_MODE_GROUNDED = 0

Apply when notions of walls, ceiling and floor are relevant. In this mode the body motion will react to slopes (acceleration/slowdown). This mode is suitable for grounded games like platformers.

MotionMode MOTION_MODE_FLOATING = 1

Apply when there is no notion of floor or ceiling. All collisions will be reported as on_wall. In this mode, when you slide, the speed will always be constant. This mode is suitable for games without ground like space games.

enum PlatformOnLeave: 🔗

PlatformOnLeave PLATFORM_ON_LEAVE_ADD_VELOCITY = 0

Add the last platform velocity to the velocity when you leave a moving platform.

PlatformOnLeave PLATFORM_ON_LEAVE_ADD_UPWARD_VELOCITY = 1

Add the last platform velocity to the velocity when you leave a moving platform, but any downward motion is ignored. It's useful to keep full jump height even when the platform is moving down.

PlatformOnLeave PLATFORM_ON_LEAVE_DO_NOTHING = 2

Do nothing when leaving a platform.

bool floor_block_on_wall = true 🔗

void set_floor_block_on_wall_enabled(value: bool)

bool is_floor_block_on_wall_enabled()

If true, the body will be able to move on the floor only. This option avoids to be able to walk on walls, it will however allow to slide down along them.

bool floor_constant_speed = false 🔗

void set_floor_constant_speed_enabled(value: bool)

bool is_floor_constant_speed_enabled()

If false (by default), the body will move faster on downward slopes and slower on upward slopes.

If true, the body will always move at the same speed on the ground no matter the slope. Note that you need to use floor_snap_length to stick along a downward slope at constant speed.

float floor_max_angle = 0.7853982 🔗

void set_floor_max_angle(value: float)

float get_floor_max_angle()

Maximum angle (in radians) where a slope is still considered a floor (or a ceiling), rather than a wall, when calling move_and_slide(). The default value equals 45 degrees.

float floor_snap_length = 0.1 🔗

void set_floor_snap_length(value: float)

float get_floor_snap_length()

Sets a snapping distance. When set to a value different from 0.0, the body is kept attached to slopes when calling move_and_slide(). The snapping vector is determined by the given distance along the opposite direction of the up_direction.

As long as the snapping vector is in contact with the ground and the body moves against up_direction, the body will remain attached to the surface. Snapping is not applied if the body moves along up_direction, meaning it contains vertical rising velocity, so it will be able to detach from the ground when jumping or when the body is pushed up by something. If you want to apply a snap without taking into account the velocity, use apply_floor_snap().

bool floor_stop_on_slope = true 🔗

void set_floor_stop_on_slope_enabled(value: bool)

bool is_floor_stop_on_slope_enabled()

If true, the body will not slide on slopes when calling move_and_slide() when the body is standing still.

If false, the body will slide on floor's slopes when velocity applies a downward force.

void set_max_slides(value: int)

Maximum number of times the body can change direction before it stops when calling move_and_slide(). Must be greater than zero.

MotionMode motion_mode = 0 🔗

void set_motion_mode(value: MotionMode)

MotionMode get_motion_mode()

Sets the motion mode which defines the behavior of move_and_slide().

int platform_floor_layers = 4294967295 🔗

void set_platform_floor_layers(value: int)

int get_platform_floor_layers()

Collision layers that will be included for detecting floor bodies that will act as moving platforms to be followed by the CharacterBody3D. By default, all floor bodies are detected and propagate their velocity.

PlatformOnLeave platform_on_leave = 0 🔗

void set_platform_on_leave(value: PlatformOnLeave)

PlatformOnLeave get_platform_on_leave()

Sets the behavior to apply when you leave a moving platform. By default, to be physically accurate, when you leave the last platform velocity is applied.

int platform_wall_layers = 0 🔗

void set_platform_wall_layers(value: int)

int get_platform_wall_layers()

Collision layers that will be included for detecting wall bodies that will act as moving platforms to be followed by the CharacterBody3D. By default, all wall bodies are ignored.

float safe_margin = 0.001 🔗

void set_safe_margin(value: float)

float get_safe_margin()

Extra margin used for collision recovery when calling move_and_slide().

If the body is at least this close to another body, it will consider them to be colliding and will be pushed away before performing the actual motion.

A higher value means it's more flexible for detecting collision, which helps with consistently detecting walls and floors.

A lower value forces the collision algorithm to use more exact detection, so it can be used in cases that specifically require precision, e.g at very low scale to avoid visible jittering, or for stability with a stack of character bodies.

bool slide_on_ceiling = true 🔗

void set_slide_on_ceiling_enabled(value: bool)

bool is_slide_on_ceiling_enabled()

If true, during a jump against the ceiling, the body will slide, if false it will be stopped and will fall vertically.

Vector3 up_direction = Vector3(0, 1, 0) 🔗

void set_up_direction(value: Vector3)

Vector3 get_up_direction()

Vector pointing upwards, used to determine what is a wall and what is a floor (or a ceiling) when calling move_and_slide(). Defaults to Vector3.UP. As the vector will be normalized it can't be equal to Vector3.ZERO, if you want all collisions to be reported as walls, consider using MOTION_MODE_FLOATING as motion_mode.

Vector3 velocity = Vector3(0, 0, 0) 🔗

void set_velocity(value: Vector3)

Vector3 get_velocity()

Current velocity vector (typically meters per second), used and modified during calls to move_and_slide().

float wall_min_slide_angle = 0.2617994 🔗

void set_wall_min_slide_angle(value: float)

float get_wall_min_slide_angle()

Minimum angle (in radians) where the body is allowed to slide when it encounters a wall. The default value equals 15 degrees. When motion_mode is MOTION_MODE_GROUNDED, it only affects movement if floor_block_on_wall is true.

void apply_floor_snap() 🔗

Allows to manually apply a snap to the floor regardless of the body's velocity. This function does nothing when is_on_floor() returns true.

float get_floor_angle(up_direction: Vector3 = Vector3(0, 1, 0)) const 🔗

Returns the floor's collision angle at the last collision point according to up_direction, which is Vector3.UP by default. This value is always positive and only valid after calling move_and_slide() and when is_on_floor() returns true.

Vector3 get_floor_normal() const 🔗

Returns the collision normal of the floor at the last collision point. Only valid after calling move_and_slide() and when is_on_floor() returns true.

Warning: The collision normal is not always the same as the surface normal.

Vector3 get_last_motion() const 🔗

Returns the last motion applied to the CharacterBody3D during the last call to move_and_slide(). The movement can be split into multiple motions when sliding occurs, and this method return the last one, which is useful to retrieve the current direction of the movement.

KinematicCollision3D get_last_slide_collision() 🔗

Returns a KinematicCollision3D, which contains information about the latest collision that occurred during the last call to move_and_slide().

Vector3 get_platform_angular_velocity() const 🔗

Returns the angular velocity of the platform at the last collision point. Only valid after calling move_and_slide().

Vector3 get_platform_velocity() const 🔗

Returns the linear velocity of the platform at the last collision point. Only valid after calling move_and_slide().

Vector3 get_position_delta() const 🔗

Returns the travel (position delta) that occurred during the last call to move_and_slide().

Vector3 get_real_velocity() const 🔗

Returns the current real velocity since the last call to move_and_slide(). For example, when you climb a slope, you will move diagonally even though the velocity is horizontal. This method returns the diagonal movement, as opposed to velocity which returns the requested velocity.

KinematicCollision3D get_slide_collision(slide_idx: int) 🔗

Returns a KinematicCollision3D, which contains information about a collision that occurred during the last call to move_and_slide(). Since the body can collide several times in a single call to move_and_slide(), you must specify the index of the collision in the range 0 to (get_slide_collision_count() - 1).

int get_slide_collision_count() const 🔗

Returns the number of times the body collided and changed direction during the last call to move_and_slide().

Vector3 get_wall_normal() const 🔗

Returns the collision normal of the wall at the last collision point. Only valid after calling move_and_slide() and when is_on_wall() returns true.

Warning: The collision normal is not always the same as the surface normal.

bool is_on_ceiling() const 🔗

Returns true if the body collided with the ceiling on the last call of move_and_slide(). Otherwise, returns false. The up_direction and floor_max_angle are used to determine whether a surface is "ceiling" or not.

bool is_on_ceiling_only() const 🔗

Returns true if the body collided only with the ceiling on the last call of move_and_slide(). Otherwise, returns false. The up_direction and floor_max_angle are used to determine whether a surface is "ceiling" or not.

bool is_on_floor() const 🔗

Returns true if the body collided with the floor on the last call of move_and_slide(). Otherwise, returns false. The up_direction and floor_max_angle are used to determine whether a surface is "floor" or not.

bool is_on_floor_only() const 🔗

Returns true if the body collided only with the floor on the last call of move_and_slide(). Otherwise, returns false. The up_direction and floor_max_angle are used to determine whether a surface is "floor" or not.

bool is_on_wall() const 🔗

Returns true if the body collided with a wall on the last call of move_and_slide(). Otherwise, returns false. The up_direction and floor_max_angle are used to determine whether a surface is "wall" or not.

bool is_on_wall_only() const 🔗

Returns true if the body collided only with a wall on the last call of move_and_slide(). Otherwise, returns false. The up_direction and floor_max_angle are used to determine whether a surface is "wall" or not.

bool move_and_slide() 🔗

Moves the body based on velocity. If the body collides with another, it will slide along the other body rather than stop immediately. If the other body is a CharacterBody3D or RigidBody3D, it will also be affected by the motion of the other body. You can use this to make moving and rotating platforms, or to make nodes push other nodes.

Modifies velocity if a slide collision occurred. To get the latest collision call get_last_slide_collision(), for more detailed information about collisions that occurred, use get_slide_collision().

When the body touches a moving platform, the platform's velocity is automatically added to the body motion. If a collision occurs due to the platform's motion, it will always be first in the slide collisions.

Returns true if the body collided, otherwise, returns false.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CharacterBody2D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_characterbody2d.html

**Contents:**
- CharacterBody2D
- Description
- Tutorials
- Properties
- Methods
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: PhysicsBody2D < CollisionObject2D < Node2D < CanvasItem < Node < Object

A 2D physics body specialized for characters moved by script.

CharacterBody2D is a specialized class for physics bodies that are meant to be user-controlled. They are not affected by physics at all, but they affect other physics bodies in their path. They are mainly used to provide high-level API to move objects with wall and slope detection (move_and_slide() method) in addition to the general collision detection provided by PhysicsBody2D.move_and_collide(). This makes it useful for highly configurable physics bodies that must move in specific ways and collide with the world, as is often the case with user-controlled characters.

For game objects that don't require complex movement or collision detection, such as moving platforms, AnimatableBody2D is simpler to configure.

Troubleshooting physics issues

Kinematic character (2D)

Using CharacterBody2D

2D Kinematic Character Demo

platform_floor_layers

get_floor_angle(up_direction: Vector2 = Vector2(0, -1)) const

get_floor_normal() const

get_last_motion() const

get_last_slide_collision()

get_platform_velocity() const

get_position_delta() const

get_real_velocity() const

get_slide_collision(slide_idx: int)

get_slide_collision_count() const

get_wall_normal() const

is_on_ceiling() const

is_on_ceiling_only() const

is_on_floor_only() const

is_on_wall_only() const

MotionMode MOTION_MODE_GROUNDED = 0

Apply when notions of walls, ceiling and floor are relevant. In this mode the body motion will react to slopes (acceleration/slowdown). This mode is suitable for sided games like platformers.

MotionMode MOTION_MODE_FLOATING = 1

Apply when there is no notion of floor or ceiling. All collisions will be reported as on_wall. In this mode, when you slide, the speed will always be constant. This mode is suitable for top-down games.

enum PlatformOnLeave: 🔗

PlatformOnLeave PLATFORM_ON_LEAVE_ADD_VELOCITY = 0

Add the last platform velocity to the velocity when you leave a moving platform.

PlatformOnLeave PLATFORM_ON_LEAVE_ADD_UPWARD_VELOCITY = 1

Add the last platform velocity to the velocity when you leave a moving platform, but any downward motion is ignored. It's useful to keep full jump height even when the platform is moving down.

PlatformOnLeave PLATFORM_ON_LEAVE_DO_NOTHING = 2

Do nothing when leaving a platform.

bool floor_block_on_wall = true 🔗

void set_floor_block_on_wall_enabled(value: bool)

bool is_floor_block_on_wall_enabled()

If true, the body will be able to move on the floor only. This option avoids to be able to walk on walls, it will however allow to slide down along them.

bool floor_constant_speed = false 🔗

void set_floor_constant_speed_enabled(value: bool)

bool is_floor_constant_speed_enabled()

If false (by default), the body will move faster on downward slopes and slower on upward slopes.

If true, the body will always move at the same speed on the ground no matter the slope. Note that you need to use floor_snap_length to stick along a downward slope at constant speed.

float floor_max_angle = 0.7853982 🔗

void set_floor_max_angle(value: float)

float get_floor_max_angle()

Maximum angle (in radians) where a slope is still considered a floor (or a ceiling), rather than a wall, when calling move_and_slide(). The default value equals 45 degrees.

float floor_snap_length = 1.0 🔗

void set_floor_snap_length(value: float)

float get_floor_snap_length()

Sets a snapping distance. When set to a value different from 0.0, the body is kept attached to slopes when calling move_and_slide(). The snapping vector is determined by the given distance along the opposite direction of the up_direction.

As long as the snapping vector is in contact with the ground and the body moves against up_direction, the body will remain attached to the surface. Snapping is not applied if the body moves along up_direction, meaning it contains vertical rising velocity, so it will be able to detach from the ground when jumping or when the body is pushed up by something. If you want to apply a snap without taking into account the velocity, use apply_floor_snap().

bool floor_stop_on_slope = true 🔗

void set_floor_stop_on_slope_enabled(value: bool)

bool is_floor_stop_on_slope_enabled()

If true, the body will not slide on slopes when calling move_and_slide() when the body is standing still.

If false, the body will slide on floor's slopes when velocity applies a downward force.

void set_max_slides(value: int)

Maximum number of times the body can change direction before it stops when calling move_and_slide(). Must be greater than zero.

MotionMode motion_mode = 0 🔗

void set_motion_mode(value: MotionMode)

MotionMode get_motion_mode()

Sets the motion mode which defines the behavior of move_and_slide().

int platform_floor_layers = 4294967295 🔗

void set_platform_floor_layers(value: int)

int get_platform_floor_layers()

Collision layers that will be included for detecting floor bodies that will act as moving platforms to be followed by the CharacterBody2D. By default, all floor bodies are detected and propagate their velocity.

PlatformOnLeave platform_on_leave = 0 🔗

void set_platform_on_leave(value: PlatformOnLeave)

PlatformOnLeave get_platform_on_leave()

Sets the behavior to apply when you leave a moving platform. By default, to be physically accurate, when you leave the last platform velocity is applied.

int platform_wall_layers = 0 🔗

void set_platform_wall_layers(value: int)

int get_platform_wall_layers()

Collision layers that will be included for detecting wall bodies that will act as moving platforms to be followed by the CharacterBody2D. By default, all wall bodies are ignored.

float safe_margin = 0.08 🔗

void set_safe_margin(value: float)

float get_safe_margin()

Extra margin used for collision recovery when calling move_and_slide().

If the body is at least this close to another body, it will consider them to be colliding and will be pushed away before performing the actual motion.

A higher value means it's more flexible for detecting collision, which helps with consistently detecting walls and floors.

A lower value forces the collision algorithm to use more exact detection, so it can be used in cases that specifically require precision, e.g at very low scale to avoid visible jittering, or for stability with a stack of character bodies.

bool slide_on_ceiling = true 🔗

void set_slide_on_ceiling_enabled(value: bool)

bool is_slide_on_ceiling_enabled()

If true, during a jump against the ceiling, the body will slide, if false it will be stopped and will fall vertically.

Vector2 up_direction = Vector2(0, -1) 🔗

void set_up_direction(value: Vector2)

Vector2 get_up_direction()

Vector pointing upwards, used to determine what is a wall and what is a floor (or a ceiling) when calling move_and_slide(). Defaults to Vector2.UP. As the vector will be normalized it can't be equal to Vector2.ZERO, if you want all collisions to be reported as walls, consider using MOTION_MODE_FLOATING as motion_mode.

Vector2 velocity = Vector2(0, 0) 🔗

void set_velocity(value: Vector2)

Vector2 get_velocity()

Current velocity vector in pixels per second, used and modified during calls to move_and_slide().

float wall_min_slide_angle = 0.2617994 🔗

void set_wall_min_slide_angle(value: float)

float get_wall_min_slide_angle()

Minimum angle (in radians) where the body is allowed to slide when it encounters a wall. The default value equals 15 degrees. This property only affects movement when motion_mode is MOTION_MODE_FLOATING.

void apply_floor_snap() 🔗

Allows to manually apply a snap to the floor regardless of the body's velocity. This function does nothing when is_on_floor() returns true.

float get_floor_angle(up_direction: Vector2 = Vector2(0, -1)) const 🔗

Returns the floor's collision angle at the last collision point according to up_direction, which is Vector2.UP by default. This value is always positive and only valid after calling move_and_slide() and when is_on_floor() returns true.

Vector2 get_floor_normal() const 🔗

Returns the collision normal of the floor at the last collision point. Only valid after calling move_and_slide() and when is_on_floor() returns true.

Warning: The collision normal is not always the same as the surface normal.

Vector2 get_last_motion() const 🔗

Returns the last motion applied to the CharacterBody2D during the last call to move_and_slide(). The movement can be split into multiple motions when sliding occurs, and this method return the last one, which is useful to retrieve the current direction of the movement.

KinematicCollision2D get_last_slide_collision() 🔗

Returns a KinematicCollision2D, which contains information about the latest collision that occurred during the last call to move_and_slide().

Vector2 get_platform_velocity() const 🔗

Returns the linear velocity of the platform at the last collision point. Only valid after calling move_and_slide().

Vector2 get_position_delta() const 🔗

Returns the travel (position delta) that occurred during the last call to move_and_slide().

Vector2 get_real_velocity() const 🔗

Returns the current real velocity since the last call to move_and_slide(). For example, when you climb a slope, you will move diagonally even though the velocity is horizontal. This method returns the diagonal movement, as opposed to velocity which returns the requested velocity.

KinematicCollision2D get_slide_collision(slide_idx: int) 🔗

Returns a KinematicCollision2D, which contains information about a collision that occurred during the last call to move_and_slide(). Since the body can collide several times in a single call to move_and_slide(), you must specify the index of the collision in the range 0 to (get_slide_collision_count() - 1).

Example: Iterate through the collisions with a for loop:

int get_slide_collision_count() const 🔗

Returns the number of times the body collided and changed direction during the last call to move_and_slide().

Vector2 get_wall_normal() const 🔗

Returns the collision normal of the wall at the last collision point. Only valid after calling move_and_slide() and when is_on_wall() returns true.

Warning: The collision normal is not always the same as the surface normal.

bool is_on_ceiling() const 🔗

Returns true if the body collided with the ceiling on the last call of move_and_slide(). Otherwise, returns false. The up_direction and floor_max_angle are used to determine whether a surface is "ceiling" or not.

bool is_on_ceiling_only() const 🔗

Returns true if the body collided only with the ceiling on the last call of move_and_slide(). Otherwise, returns false. The up_direction and floor_max_angle are used to determine whether a surface is "ceiling" or not.

bool is_on_floor() const 🔗

Returns true if the body collided with the floor on the last call of move_and_slide(). Otherwise, returns false. The up_direction and floor_max_angle are used to determine whether a surface is "floor" or not.

bool is_on_floor_only() const 🔗

Returns true if the body collided only with the floor on the last call of move_and_slide(). Otherwise, returns false. The up_direction and floor_max_angle are used to determine whether a surface is "floor" or not.

bool is_on_wall() const 🔗

Returns true if the body collided with a wall on the last call of move_and_slide(). Otherwise, returns false. The up_direction and floor_max_angle are used to determine whether a surface is "wall" or not.

bool is_on_wall_only() const 🔗

Returns true if the body collided only with a wall on the last call of move_and_slide(). Otherwise, returns false. The up_direction and floor_max_angle are used to determine whether a surface is "wall" or not.

bool move_and_slide() 🔗

Moves the body based on velocity. If the body collides with another, it will slide along the other body (by default only on floor) rather than stop immediately. If the other body is a CharacterBody2D or RigidBody2D, it will also be affected by the motion of the other body. You can use this to make moving and rotating platforms, or to make nodes push other nodes.

Modifies velocity if a slide collision occurred. To get the latest collision call get_last_slide_collision(), for detailed information about collisions that occurred, use get_slide_collision().

When the body touches a moving platform, the platform's velocity is automatically added to the body motion. If a collision occurs due to the platform's motion, it will always be first in the slide collisions.

The general behavior and available properties change according to the motion_mode.

Returns true if the body collided, otherwise, returns false.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
for i in get_slide_collision_count():
    var collision = get_slide_collision(i)
    print("Collided with: ", collision.get_collider().name)
```

Example 2 (json):
```json
for (int i = 0; i < GetSlideCollisionCount(); i++)
{
    KinematicCollision2D collision = GetSlideCollision(i);
    GD.Print("Collided with: ", (collision.GetCollider() as Node).Name);
}
```

---

## CollisionObject3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_collisionobject3d.html

**Contents:**
- CollisionObject3D
- Description
- Properties
- Methods
- Signals
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: Node3D < Node < Object

Inherited By: Area3D, PhysicsBody3D

Abstract base class for 3D physics objects.

Abstract base class for 3D physics objects. CollisionObject3D can hold any number of Shape3Ds for collision. Each shape must be assigned to a shape owner. Shape owners are not nodes and do not appear in the editor, but are accessible through code using the shape_owner_* methods.

Warning: With a non-uniform scale, this node will likely not behave as expected. It is advised to keep its scale the same on all axes and adjust its collision shape(s) instead.

input_capture_on_drag

_input_event(camera: Camera3D, event: InputEvent, event_position: Vector3, normal: Vector3, shape_idx: int) virtual

_mouse_enter() virtual

_mouse_exit() virtual

create_shape_owner(owner: Object)

get_collision_layer_value(layer_number: int) const

get_collision_mask_value(layer_number: int) const

is_shape_owner_disabled(owner_id: int) const

remove_shape_owner(owner_id: int)

set_collision_layer_value(layer_number: int, value: bool)

set_collision_mask_value(layer_number: int, value: bool)

shape_find_owner(shape_index: int) const

shape_owner_add_shape(owner_id: int, shape: Shape3D)

shape_owner_clear_shapes(owner_id: int)

shape_owner_get_owner(owner_id: int) const

shape_owner_get_shape(owner_id: int, shape_id: int) const

shape_owner_get_shape_count(owner_id: int) const

shape_owner_get_shape_index(owner_id: int, shape_id: int) const

shape_owner_get_transform(owner_id: int) const

shape_owner_remove_shape(owner_id: int, shape_id: int)

shape_owner_set_disabled(owner_id: int, disabled: bool)

shape_owner_set_transform(owner_id: int, transform: Transform3D)

input_event(camera: Node, event: InputEvent, event_position: Vector3, normal: Vector3, shape_idx: int) 🔗

Emitted when the object receives an unhandled InputEvent. event_position is the location in world space of the mouse pointer on the surface of the shape with index shape_idx and normal is the normal vector of the surface at that point.

Emitted when the mouse pointer enters any of this object's shapes. Requires input_ray_pickable to be true and at least one collision_layer bit to be set.

Note: Due to the lack of continuous collision detection, this signal may not be emitted in the expected order if the mouse moves fast enough and the CollisionObject3D's area is small. This signal may also not be emitted if another CollisionObject3D is overlapping the CollisionObject3D in question.

Emitted when the mouse pointer exits all this object's shapes. Requires input_ray_pickable to be true and at least one collision_layer bit to be set.

Note: Due to the lack of continuous collision detection, this signal may not be emitted in the expected order if the mouse moves fast enough and the CollisionObject3D's area is small. This signal may also not be emitted if another CollisionObject3D is overlapping the CollisionObject3D in question.

DisableMode DISABLE_MODE_REMOVE = 0

When Node.process_mode is set to Node.PROCESS_MODE_DISABLED, remove from the physics simulation to stop all physics interactions with this CollisionObject3D.

Automatically re-added to the physics simulation when the Node is processed again.

DisableMode DISABLE_MODE_MAKE_STATIC = 1

When Node.process_mode is set to Node.PROCESS_MODE_DISABLED, make the body static. Doesn't affect Area3D. PhysicsBody3D can't be affected by forces or other bodies while static.

Automatically set PhysicsBody3D back to its original mode when the Node is processed again.

DisableMode DISABLE_MODE_KEEP_ACTIVE = 2

When Node.process_mode is set to Node.PROCESS_MODE_DISABLED, do not affect the physics simulation.

int collision_layer = 1 🔗

void set_collision_layer(value: int)

int get_collision_layer()

The physics layers this CollisionObject3D is in. Collision objects can exist in one or more of 32 different layers. See also collision_mask.

Note: Object A can detect a contact with object B only if object B is in any of the layers that object A scans. See Collision layers and masks in the documentation for more information.

int collision_mask = 1 🔗

void set_collision_mask(value: int)

int get_collision_mask()

The physics layers this CollisionObject3D scans. Collision objects can scan one or more of 32 different layers. See also collision_layer.

Note: Object A can detect a contact with object B only if object B is in any of the layers that object A scans. See Collision layers and masks in the documentation for more information.

float collision_priority = 1.0 🔗

void set_collision_priority(value: float)

float get_collision_priority()

The priority used to solve colliding when occurring penetration. The higher the priority is, the lower the penetration into the object will be. This can for example be used to prevent the player from breaking through the boundaries of a level.

DisableMode disable_mode = 0 🔗

void set_disable_mode(value: DisableMode)

DisableMode get_disable_mode()

Defines the behavior in physics when Node.process_mode is set to Node.PROCESS_MODE_DISABLED.

bool input_capture_on_drag = false 🔗

void set_capture_input_on_drag(value: bool)

bool get_capture_input_on_drag()

If true, the CollisionObject3D will continue to receive input events as the mouse is dragged across its shapes.

bool input_ray_pickable = true 🔗

void set_ray_pickable(value: bool)

bool is_ray_pickable()

If true, this object is pickable. A pickable object can detect the mouse pointer entering/leaving, and if the mouse is inside it, report input events. Requires at least one collision_layer bit to be set.

void _input_event(camera: Camera3D, event: InputEvent, event_position: Vector3, normal: Vector3, shape_idx: int) virtual 🔗

Receives unhandled InputEvents. event_position is the location in world space of the mouse pointer on the surface of the shape with index shape_idx and normal is the normal vector of the surface at that point. Connect to the input_event signal to easily pick up these events.

Note: _input_event() requires input_ray_pickable to be true and at least one collision_layer bit to be set.

void _mouse_enter() virtual 🔗

Called when the mouse pointer enters any of this object's shapes. Requires input_ray_pickable to be true and at least one collision_layer bit to be set. Note that moving between different shapes within a single CollisionObject3D won't cause this function to be called.

void _mouse_exit() virtual 🔗

Called when the mouse pointer exits all this object's shapes. Requires input_ray_pickable to be true and at least one collision_layer bit to be set. Note that moving between different shapes within a single CollisionObject3D won't cause this function to be called.

int create_shape_owner(owner: Object) 🔗

Creates a new shape owner for the given object. Returns owner_id of the new owner for future reference.

bool get_collision_layer_value(layer_number: int) const 🔗

Returns whether or not the specified layer of the collision_layer is enabled, given a layer_number between 1 and 32.

bool get_collision_mask_value(layer_number: int) const 🔗

Returns whether or not the specified layer of the collision_mask is enabled, given a layer_number between 1 and 32.

RID get_rid() const 🔗

Returns the object's RID.

PackedInt32Array get_shape_owners() 🔗

Returns an Array of owner_id identifiers. You can use these ids in other methods that take owner_id as an argument.

bool is_shape_owner_disabled(owner_id: int) const 🔗

If true, the shape owner and its shapes are disabled.

void remove_shape_owner(owner_id: int) 🔗

Removes the given shape owner.

void set_collision_layer_value(layer_number: int, value: bool) 🔗

Based on value, enables or disables the specified layer in the collision_layer, given a layer_number between 1 and 32.

void set_collision_mask_value(layer_number: int, value: bool) 🔗

Based on value, enables or disables the specified layer in the collision_mask, given a layer_number between 1 and 32.

int shape_find_owner(shape_index: int) const 🔗

Returns the owner_id of the given shape.

void shape_owner_add_shape(owner_id: int, shape: Shape3D) 🔗

Adds a Shape3D to the shape owner.

void shape_owner_clear_shapes(owner_id: int) 🔗

Removes all shapes from the shape owner.

Object shape_owner_get_owner(owner_id: int) const 🔗

Returns the parent object of the given shape owner.

Shape3D shape_owner_get_shape(owner_id: int, shape_id: int) const 🔗

Returns the Shape3D with the given ID from the given shape owner.

int shape_owner_get_shape_count(owner_id: int) const 🔗

Returns the number of shapes the given shape owner contains.

int shape_owner_get_shape_index(owner_id: int, shape_id: int) const 🔗

Returns the child index of the Shape3D with the given ID from the given shape owner.

Transform3D shape_owner_get_transform(owner_id: int) const 🔗

Returns the shape owner's Transform3D.

void shape_owner_remove_shape(owner_id: int, shape_id: int) 🔗

Removes a shape from the given shape owner.

void shape_owner_set_disabled(owner_id: int, disabled: bool) 🔗

If true, disables the given shape owner.

void shape_owner_set_transform(owner_id: int, transform: Transform3D) 🔗

Sets the Transform3D of the given shape owner.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CollisionShape2D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_collisionshape2d.html

**Contents:**
- CollisionShape2D
- Description
- Tutorials
- Properties
- Property Descriptions
- User-contributed notes

Inherits: Node2D < CanvasItem < Node < Object

A node that provides a Shape2D to a CollisionObject2D parent.

A node that provides a Shape2D to a CollisionObject2D parent and allows to edit it. This can give a detection shape to an Area2D or turn a PhysicsBody2D into a solid object.

2D Dodge The Creeps Demo

2D Kinematic Character Demo

one_way_collision_margin

Color debug_color = Color(0, 0, 0, 0) 🔗

void set_debug_color(value: Color)

Color get_debug_color()

The collision shape color that is displayed in the editor, or in the running project if Debug > Visible Collision Shapes is checked at the top of the editor.

Note: The default value is ProjectSettings.debug/shapes/collision/shape_color. The Color(0, 0, 0, 0) value documented here is a placeholder, and not the actual default debug color.

bool disabled = false 🔗

void set_disabled(value: bool)

A disabled collision shape has no effect in the world. This property should be changed with Object.set_deferred().

bool one_way_collision = false 🔗

void set_one_way_collision(value: bool)

bool is_one_way_collision_enabled()

Sets whether this collision shape should only detect collision on one side (top or bottom).

Note: This property has no effect if this CollisionShape2D is a child of an Area2D node.

float one_way_collision_margin = 1.0 🔗

void set_one_way_collision_margin(value: float)

float get_one_way_collision_margin()

The margin used for one-way collision (in pixels). Higher values will make the shape thicker, and work better for colliders that enter the shape at a high velocity.

void set_shape(value: Shape2D)

The actual shape owned by this collision shape.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CollisionPolygon2D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_collisionpolygon2d.html

**Contents:**
- CollisionPolygon2D
- Description
- Properties
- Enumerations
- Property Descriptions
- User-contributed notes

Inherits: Node2D < CanvasItem < Node < Object

A node that provides a polygon shape to a CollisionObject2D parent.

A node that provides a polygon shape to a CollisionObject2D parent and allows to edit it. The polygon can be concave or convex. This can give a detection shape to an Area2D, turn PhysicsBody2D into a solid object, or give a hollow shape to a StaticBody2D.

Warning: A non-uniformly scaled CollisionPolygon2D will likely not behave as expected. Make sure to keep its scale the same on all axes and adjust its polygon instead.

one_way_collision_margin

BuildMode BUILD_SOLIDS = 0

Collisions will include the polygon and its contained area. In this mode the node has the same effect as several ConvexPolygonShape2D nodes, one for each convex shape in the convex decomposition of the polygon (but without the overhead of multiple nodes).

BuildMode BUILD_SEGMENTS = 1

Collisions will only include the polygon edges. In this mode the node has the same effect as a single ConcavePolygonShape2D made of segments, with the restriction that each segment (after the first one) starts where the previous one ends, and the last one ends where the first one starts (forming a closed but hollow polygon).

BuildMode build_mode = 0 🔗

void set_build_mode(value: BuildMode)

BuildMode get_build_mode()

Collision build mode.

bool disabled = false 🔗

void set_disabled(value: bool)

If true, no collisions will be detected. This property should be changed with Object.set_deferred().

bool one_way_collision = false 🔗

void set_one_way_collision(value: bool)

bool is_one_way_collision_enabled()

If true, only edges that face up, relative to CollisionPolygon2D's rotation, will collide with other objects.

Note: This property has no effect if this CollisionPolygon2D is a child of an Area2D node.

float one_way_collision_margin = 1.0 🔗

void set_one_way_collision_margin(value: float)

float get_one_way_collision_margin()

The margin used for one-way collision (in pixels). Higher values will make the shape thicker, and work better for colliders that enter the polygon at a high velocity.

PackedVector2Array polygon = PackedVector2Array() 🔗

void set_polygon(value: PackedVector2Array)

PackedVector2Array get_polygon()

The polygon's list of vertices. Each point will be connected to the next, and the final point will be connected to the first.

Note: The returned vertices are in the local coordinate space of the given CollisionPolygon2D.

Note: The returned array is copied and any changes to it will not update the original property value. See PackedVector2Array for more details.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CollisionPolygon3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_collisionpolygon3d.html

**Contents:**
- CollisionPolygon3D
- Description
- Properties
- Property Descriptions
- User-contributed notes

Inherits: Node3D < Node < Object

A node that provides a thickened polygon shape (a prism) to a CollisionObject3D parent.

A node that provides a thickened polygon shape (a prism) to a CollisionObject3D parent and allows to edit it. The polygon can be concave or convex. This can give a detection shape to an Area3D or turn PhysicsBody3D into a solid object.

Warning: A non-uniformly scaled CollisionShape3D will likely not behave as expected. Make sure to keep its scale the same on all axes and adjust its shape resource instead.

Color debug_color = Color(0, 0, 0, 0) 🔗

void set_debug_color(value: Color)

Color get_debug_color()

The collision shape color that is displayed in the editor, or in the running project if Debug > Visible Collision Shapes is checked at the top of the editor.

Note: The default value is ProjectSettings.debug/shapes/collision/shape_color. The Color(0, 0, 0, 0) value documented here is a placeholder, and not the actual default debug color.

bool debug_fill = true 🔗

void set_enable_debug_fill(value: bool)

bool get_enable_debug_fill()

If true, when the shape is displayed, it will show a solid fill color in addition to its wireframe.

void set_depth(value: float)

Length that the resulting collision extends in either direction perpendicular to its 2D polygon.

bool disabled = false 🔗

void set_disabled(value: bool)

If true, no collision will be produced. This property should be changed with Object.set_deferred().

float margin = 0.04 🔗

void set_margin(value: float)

The collision margin for the generated Shape3D. See Shape3D.margin for more details.

PackedVector2Array polygon = PackedVector2Array() 🔗

void set_polygon(value: PackedVector2Array)

PackedVector2Array get_polygon()

Array of vertices which define the 2D polygon in the local XY plane.

Note: The returned array is copied and any changes to it will not update the original property value. See PackedVector2Array for more details.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CollisionShape3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_collisionshape3d.html

**Contents:**
- CollisionShape3D
- Description
- Tutorials
- Properties
- Methods
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: Node3D < Node < Object

A node that provides a Shape3D to a CollisionObject3D parent.

A node that provides a Shape3D to a CollisionObject3D parent and allows to edit it. This can give a detection shape to an Area3D or turn a PhysicsBody3D into a solid object.

Warning: A non-uniformly scaled CollisionShape3D will likely not behave as expected. Make sure to keep its scale the same on all axes and adjust its shape resource instead.

3D Kinematic Character Demo

Third Person Shooter (TPS) Demo

make_convex_from_siblings()

resource_changed(resource: Resource)

Color debug_color = Color(0, 0, 0, 0) 🔗

void set_debug_color(value: Color)

Color get_debug_color()

The collision shape color that is displayed in the editor, or in the running project if Debug > Visible Collision Shapes is checked at the top of the editor.

Note: The default value is ProjectSettings.debug/shapes/collision/shape_color. The Color(0, 0, 0, 0) value documented here is a placeholder, and not the actual default debug color.

bool debug_fill = true 🔗

void set_enable_debug_fill(value: bool)

bool get_enable_debug_fill()

If true, when the shape is displayed, it will show a solid fill color in addition to its wireframe.

bool disabled = false 🔗

void set_disabled(value: bool)

A disabled collision shape has no effect in the world. This property should be changed with Object.set_deferred().

void set_shape(value: Shape3D)

The actual shape owned by this collision shape.

void make_convex_from_siblings() 🔗

Sets the collision shape's shape to the addition of all its convexed MeshInstance3D siblings geometry.

void resource_changed(resource: Resource) 🔗

Deprecated: Use Resource.changed instead.

This method does nothing.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---
