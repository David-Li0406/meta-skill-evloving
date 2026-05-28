# Physics Reference

## Contents
- [Adaptive timestepping](#adaptive-timestepping)
- [Assemblies](#assemblies)
- [Character controllers](#character-controllers)
- [AlignOrientation](#alignorientation)
- [AlignPosition](#alignposition)
- [AngularVelocity](#angularvelocity)
- [BallSocket](#ballsocket)
- [Cylindrical](#cylindrical)
- [Hinge](#hinge)
- [LineForce](#lineforce)
- [LinearVelocity](#linearvelocity)
- [NoCollision](#nocollision)
- [Plane](#plane)
- [Prismatic](#prismatic)
- [Rigid](#rigid)
- [Rod](#rod)
- [Rope](#rope)
- [Spring](#spring)
- [Torque](#torque)
- [TorsionSpring](#torsionspring)
- [Universal](#universal)
- [VectorForce](#vectorforce)
- [Weld](#weld)
- [Physics](#physics)
- [Mechanical constraints](#mechanical-constraints)
- [Mover constraints](#mover-constraints)
- [Network ownership](#network-ownership)
- [Sleep system](#sleep-system)
- [Roblox units](#roblox-units)

---

## Adaptive timestepping

The Roblox physics engine simulates all parts inside the 3D workspace through Newton's second law of motion. This law of motion is solved over time via **timesteps** and a single timestep is done within a **worldstep** in Roblox.

By default, Roblox simulates physics at 240&nbsp;Hz. Given cycles of approximately 60 frames per second, around 4&nbsp;worldsteps are advanced per frame. With **adaptive timestepping**, the physics engine automatically assigns parts to three "solver&nbsp;islands" by varying their simulation timestep, with an emphasis on 60&nbsp;Hz for best performance. However, parts that are "harder" to solve will use a faster timestep like 240&nbsp;Hz to ensure physical stability.

<img src="../assets/physics/adaptive-timestepping/Diagram-Labels.png" alt="" width="100%" />

Assignment criterions are subject to change, but parts assigned to the 240&nbsp;Hz island include [assemblies](../physics/assemblies.md) with high velocity values, high acceleration values, and complex mechanisms that are hard to solve.

## Enable adaptive mode

To enable adaptive timestepping in Studio:

1. In the **Explorer** window, select the **Workspace** object.

   <img src="../assets/studio/explorer/Workspace.png" alt="" width="320" />

2. In the **Properties** window, locate **PhysicsSteppingMethod** and select **Adaptive**.

   <img src="../assets/physics/adaptive-timestepping/PhysicsSteppingMethod-Adaptive.png" alt="" width="320" />

To observe the timestepping process in action, you can open the Studio **Microprofiler** (<kbd>Ctrl</kbd><kbd>F6</kbd>; <kbd>⌘</kbd><kbd>F6</kbd>). Once the experience is running, press <kbd>Ctrl</kbd><kbd>P</kbd> (<kbd>⌘</kbd><kbd>P</kbd>) to pause at the current frame.

Under the scope named **physicsStepped**, observe that the scope name of **worldStep** now reads **worldStep&nbsp;-&nbsp;Adaptive**.

<img src="../assets/physics/adaptive-timestepping/Adaptive-Timestepping-Microprofiler-A.png" alt="" width="80%" />

Hovering your cursor above 

[Content truncated - see full docs]

---

## Assemblies

An **assembly** is one or more [parts](../parts/index.md) welded by a rigid `Class.WeldConstraint|WeldConstraint` or connected through moveable joints, like `Class.Motor6D|Motor6Ds`. You can group an assembly of parts in a [model](../parts/models.md) container to quickly organize the parts and related objects as a single asset.

<Grid container spacing={0}>
  <Grid item XSmall={6} XLarge={3}>
    <img src="../assets/physics/assemblies/Assembly-Example-Block.png" alt="A light blue cube against a dark blue background that represents an assembly of 1 part." width="100%" />
    <figcaption>1&nbsp;assembly; 1&nbsp;part</figcaption>
  </Grid>
  <Grid item XSmall={6} XLarge={3}>
    <img src="../assets/physics/assemblies/Assembly-Example-Avatar.png" alt="A humanoid character model against a dark blue background that represents an assembly of 18 parts." width="100%" />
    <figcaption>1&nbsp;assembly; 18&nbsp;parts</figcaption>
  </Grid>
  <Grid item XSmall={12} XLarge={6}>
    <img src="../assets/physics/assemblies/Assembly-Example-Ship.png" alt="A pirate that represents an assemble of 179 parts." width="100%" />
    <figcaption>1&nbsp;assembly; 179&nbsp;parts</figcaption>
  </Grid>
</Grid>
<br />

From a physics perspective, an assembly is considered a single **rigid&nbsp;body**, meaning no force can push or pull the connected parts from each other, and they will move as a single unit. All forces applied to a specific `Class.BasePart` are applied to its assembly&nbsp;&mdash; for instance, `Class.BasePart:ApplyImpulse()` applies impulse to the assembly at `Class.BasePart.AssemblyCenterOfMass`.

<Alert severity="info">
The joints that combine multiple parts into assemblies are only active in the `Class.Workspace` or another `Class.WorldModel` instance. If the parts are stored elsewhere, all of the welds/connections that combine parts into assemblies will be non-functional.
</Alert>

<Alert severity="success">
To view colored outlines around parts in order to visualize singl

[Content truncated - see full docs]

---

## Character controllers

The `Class.ControllerManager` instance manages simulated motion control for its assigned `Class.ControllerManager.RootPart|RootPart`. Along with `Class.ControllerPartSensor|ControllerPartSensors`, it can be used to build a physics‑based character controller.

## Core setup

`Class.ControllerManager` requires a `Class.BasePart` to use as its root. Movement forces and part sensing will be on this part.

1. Choose a `Class.Part` or `Class.MeshPart` and name it **RootPart**.
2. Group the part as a `Class.Model` instance for organization along with the other components.
3. Add a `Class.ControllerManager` instance to the model. If **ControllerManager** doesn't initially appear in the object insertion menu, **uncheck** "Show only recommended objects" in the menu's [insertion settings](../studio/explorer.md#insert-and-parent).

	 <img src="../assets/physics/character-controller/Explorer-Core-Setup.png" width="320" alt="ControllerManager and RootPart inside a model." />

### Sensor setup

A `Class.ControllerPartSensor` detects parts with the same code the `Class.Humanoid` uses for detecting floors and ladders.

1. Insert a `Class.ControllerPartSensor` as a child of **RootPart** and rename it **GroundSensor** for easier identification of its purpose. Then, in the [Properties](../studio/properties.md) window, set its `Class.ControllerPartSensor.SearchDistance|SearchDistance` property to **2** but leave its `Class.ControllerPartSensor.SensorMode|SensorMode` as **Floor**.

   <img src="../assets/physics/character-controller/Explorer-RootPart-GroundSensor.png" width="320" alt="GroundSensor as child of RootPart" /><br />
	 <img src="../assets/physics/character-controller/Properties-GroundSensor.png" width="320" alt="" />

2. Insert another `Class.ControllerPartSensor` as a child of **RootPart** and rename it **ClimbSensor**. Then, in the [Properties](../studio/properties.md) window, set its `Class.ControllerPartSensor.SearchDistance|SearchDistance` property to **1** and its `Class

[Content truncated - see full docs]

---

## AlignOrientation

<Alert severity="info">
For an overview on creating, visualizing, and simulating mover constraints, including `Class.AlignOrientation`, see [Mover constraints](../../physics/mover-constraints.md). Also see [Roblox&nbsp;units](../../physics/units.md) to understand how Roblox units compare to metric units.
</Alert>

The `Class.AlignOrientation` constraint applies torque to align two attachments, or to align one attachment with a goal orientation. As indicated by the name, it only affects the **orientation** of the attachments, not their position (to align attachments **positionally**, see [AlignPosition](../../physics/constraints/align-position.md)).

<video controls src="../../assets/physics/constraints/AlignOrientation-Demo.mp4" width="90%" alt="Demo video of AlignOrientation constraint"></video>

<Alert severity="warning">
By default, the constraint only applies torque to `Class.Constraint.Attachment0|Attachment0`, although this behavior can be controlled through `Class.AlignOrientation.ReactionTorqueEnabled|ReactionTorqueEnabled`.
</Alert>

## Affected axes

The axes affected by torque are controlled through the constraint's `Class.AlignOrientation.AlignType|AlignType` property. When set to `Enum.AlignType|PrimaryAxisParallel`, `Enum.AlignType|PrimaryAxisPerpendicular` or `Enum.AlignType|PrimaryAxisLookAt`, torque will only occur when the primary axes become misaligned. Otherwise, the constraint will apply torque about all 3 axes to achieve alignment.

<GridContainer numColumns="2">
  <figure>
    <video controls src="../../assets/physics/constraints/AlignOrientation-AlignType-AllAxes.mp4" alt="Video showing AlignType set to AllAxes"></video>
    <figcaption>AlignType = **AllAxes**</figcaption>
  </figure>
  <figure>
    <video controls src="../../assets/physics/constraints/AlignOrientation-AlignType-PrimaryAxisParallel.mp4" alt="Video showing AlignType set to PrimaryAxisParallel"></video>
    <figcaption>AlignType = **PrimaryAxisParallel**</figcaption>
  </figure

[Content truncated - see full docs]

---

## AlignPosition

<Alert severity="info">
For an overview on creating, visualizing, and simulating mover constraints, including `Class.AlignPosition`, see [Mover constraints](../../physics/mover-constraints.md). Also see [Roblox&nbsp;units](../../physics/units.md) to understand how Roblox units compare to metric units.
</Alert>

An `Class.AlignPosition` constraint applies force to move two attachments together, or to move one attachment to a goal position. As indicated by the name, it only affects the **position** of the attachments, not their orientation (to align attachments by **orientation**, see [AlignOrientation](../../physics/constraints/align-orientation.md)).

<video controls src="../../assets/physics/constraints/AlignPosition-Demo.mp4" width="90%" alt="Demo video of AlignPosition constraint"></video>

<Alert severity="warning">
By default, the constraint only applies force to `Class.Constraint.Attachment0|Attachment0`, although this behavior can be controlled through `Class.AlignPosition.ReactionForceEnabled|ReactionForceEnabled`.
</Alert>

## Force location

By default, force is applied to the parent of `Class.Constraint.Attachment0|Attachment0` at that attachment's location, meaning that if the parent's center of mass is not aligned with the direction of the force, torque will be applied as well as force. Alternatively, force can be applied to the parents' center of mass by toggling on `Class.AlignPosition.ApplyAtCenterOfMass|ApplyAtCenterOfMass`.

<GridContainer numColumns="2">
  <figure>
    <video controls src="../../assets/physics/constraints/AlignPosition-ApplyAtCenterOfMass-False.mp4" alt="Video showing ApplyAtCenterOfMass set to false"></video>
    <figcaption>ApplyAtCenterOfMass = **false**</figcaption>
  </figure>
  <figure>
    <video controls src="../../assets/physics/constraints/AlignPosition-ApplyAtCenterOfMass-True.mp4" alt="Video showing ApplyAtCenterOfMass set to true"></video>
    <figcaption>ApplyAtCenterOfMass = **true**</figcaption>
  </figure>
</GridC

[Content truncated - see full docs]

---

## AngularVelocity

<Alert severity="info">
For an overview on creating, visualizing, and simulating mover constraints, including `Class.AngularVelocity`, see [Mover constraints](../../physics/mover-constraints.md). Also see [Roblox&nbsp;units](../../physics/units.md) to understand how Roblox units compare to metric units.
</Alert>

An `Class.AngularVelocity` constraint applies torque on an assembly to maintain a constant angular velocity.

<video controls src="../../assets/physics/constraints/AngularVelocity-Demo.mp4" width="90%" alt="Demo video of AngularVelocity constraint"></video>

<Alert severity="warning">
The `Class.AngularVelocity` constraint applies torque that attempts to maintain a **constant** angular velocity. If you want to control the amount of torque applied, use a [Torque](../../physics/constraints/torque.md) constraint. Alternatively, if you only need **initial** angular velocity, set the `Class.BasePart.AssemblyAngularVelocity|AssemblyAngularVelocity` method directly on the assembly.
</Alert>

## Relativity

Application of velocity can be controlled through the constraint's `Class.AngularVelocity.RelativeTo|RelativeTo` property. If set to `Enum.ActuatorRelativeTo|World`, the angular velocity vector is used as is. If set to `Enum.ActuatorRelativeTo|Attachment1` and the constraint's `Class.Constraint.Attachment1|Attachment1` property is set to another attachment, the angular velocity will be affected by that of the other attachment as seen by how the upper-left red part's velocity affects the attached blue part's velocity.

<GridContainer numColumns="2">
  <figure>
    <video controls src="../../assets/physics/constraints/AngularVelocity-RelativeTo-World.mp4" alt="Video showing relative behavior set to world space"></video>
    <figcaption>RelativeTo = **World**</figcaption>
  </figure>
  <figure>
    <video controls src="../../assets/physics/constraints/AngularVelocity-RelativeTo-Attachment1.mp4" alt="Video showing relative behavior set to Attachment1"></video>
    <

[Content truncated - see full docs]

---

## BallSocket

<Alert severity="info">
For an overview on creating, visualizing, and simulating mechanical constraints, including `Class.BallSocketConstraint`, see [Mechanical constraints](../../physics/mechanical-constraints.md). Also see [Roblox&nbsp;units](../../physics/units.md) to understand how Roblox units compare to metric units.
</Alert>

A `Class.BallSocketConstraint` forces its two attachments into the same position and allows them to freely rotate about all three axes. However, you can enable limits to restrict both tilt and twist.

<video controls src="../../assets/physics/constraints/BallInSocket-Demo.mp4" width="90%" alt="Demo video of BallSocketConstraint"></video>

## Limits

You can set limits to restrict both **tilt** and **twist** of a ball socket, similar to how a human's head can tilt and turn within a limited axial range. Enabling the `Class.BallSocketConstraint.LimitsEnabled|LimitsEnabled` property exposes the `Class.BallSocketConstraint.UpperAngle|UpperAngle` value to restrict **tilt** within a cone; it also exposes the `Class.BallSocketConstraint.TwistLimitsEnabled|TwistLimitsEnabled` property which, when enabled, lets you restrict **twist** rotation through the `Class.BallSocketConstraint.TwistLowerAngle|TwistLowerAngle` and `Class.BallSocketConstraint.TwistUpperAngle|TwistUpperAngle` limits.

<GridContainer numColumns="2">
  <figure>
    <video controls src="../../assets/physics/constraints/BallInSocket-Limits-Tilt.mp4" alt="Video showing limits when UpperAngle is set to 30 degrees"></video>
    <figcaption>UpperAngle = **30**</figcaption>
  </figure>
  <figure>
    <video controls src="../../assets/physics/constraints/BallInSocket-Limits-Twist.mp4" alt="Video showing limits when TwistLimitsEnabled is set to true"></video>
    <figcaption>TwistLimitsEnabled = **true**</figcaption>
  </figure>
</GridContainer>

Enabling `Class.BallSocketConstraint.LimitsEnabled|LimitsEnabled` also exposes the `Class.BallSocketConstraint.Restitution|Restitution` value whi

[Content truncated - see full docs]

---

## Cylindrical

<Alert severity="info">
For an overview on creating, visualizing, and simulating mechanical constraints, including `Class.CylindricalConstraint`, see [Mechanical constraints](../../physics/mechanical-constraints.md). Also see [Roblox&nbsp;units](../../physics/units.md) to understand how Roblox units compare to metric units.
</Alert>

A `Class.CylindricalConstraint` allows its attachments to slide along one axis and rotate about another axis. This constraint, along with a
[SpringConstraint](../../physics/constraints/spring.md), is ideal for building vehicle suspensions where the wheel shock can slide up and down while the wheel itself spins. This constraint can also be powered in both an [angular](#angular-power) and [linear](#linear-power) manner.

<video controls src="../../assets/physics/constraints/Cylindrical-Demo.mp4" width="90%" alt="Demo video of CylindricalConstraint"></video>

<Alert severity="info">
Orientation of the attachments affects how the cylindrical aspect will rotate. To ensure rotation occurs around the desired axis, each attachment's `Class.Attachment.Axis|Axis` and `Class.Attachment.SecondaryAxis|SecondaryAxis`, visualized by the yellow and orange arrows, should point in the same direction.
</Alert>

## Angular power

If a cylindrical's `Class.CylindricalConstraint.AngularActuatorType|AngularActuatorType` is set to `Enum.ActuatorType|Motor`, it attempts to rotate the attachments with the goal of reaching its `Class.CylindricalConstraint.AngularVelocity|AngularVelocity`. You can further control this rotation through both `Class.CylindricalConstraint.MotorMaxAngularAcceleration|MotorMaxAngularAcceleration` and `Class.CylindricalConstraint.MotorMaxTorque|MotorMaxTorque`.

If a cylindrical's `Class.CylindricalConstraint.AngularActuatorType|AngularActuatorType` is set to `Enum.ActuatorType|Servo`, it attempts to rotate to an angle specified by `Class.CylindricalConstraint.TargetAngle|TargetAngle`. This rotation is controlled by `Class.CylindricalCon

[Content truncated - see full docs]

---

## Hinge

<Alert severity="info">
For an overview on creating, visualizing, and simulating mechanical constraints, including `Class.HingeConstraint`, see [Mechanical constraints](../../physics/mechanical-constraints.md). Also see [Roblox&nbsp;units](../../physics/units.md) to understand how Roblox units compare to metric units.
</Alert>

A `Class.HingeConstraint`
allows its two attachments to rotate about one axis, forcing them into
the same position and **X** axis alignment. This constraint can also be
powered to behave like a [motor](#angular-power) or [servo](#angular-power), and you can set limits to restrict the hinge's rotational range.

<video controls src="../../assets/physics/constraints/Hinge-Demo.mp4" width="90%" alt="Demo video of HingeConstraint"></video>

<Alert severity="info">
Orientation of a hinge's attachments affects how it rotates. To ensure rotation occurs around the desired axis, each attachment's `Class.Attachment.Axis|Axis`, visualized by the yellow arrow, should point in the same direction.
</Alert>

### Angular power

If a hinge's `Class.HingeConstraint.ActuatorType|ActuatorType` is set to `Enum.ActuatorType|Motor`, it attempts to rotate the attachments with the goal of reaching its `Class.HingeConstraint.AngularVelocity|AngularVelocity`. You can further control this rotation through both `Class.HingeConstraint.MotorMaxAcceleration|MotorMaxAcceleration` and `Class.HingeConstraint.MotorMaxTorque|MotorMaxTorque`.

If a hinge's `Class.HingeConstraint.ActuatorType|ActuatorType` is set to `Enum.ActuatorType|Servo`, it attempts to rotate to an angle specified by `Class.HingeConstraint.TargetAngle|TargetAngle`. This rotation is controlled by both `Class.HingeConstraint.AngularSpeed|AngularSpeed` and `Class.HingeConstraint.ServoMaxTorque|ServoMaxTorque`.

<GridContainer numColumns="2">
  <figure>
    <video controls src="../../assets/physics/constraints/Hinge-ActuatorType-Motor.mp4" alt="Video showing angular power configured for motor behavior"></video>
  

[Content truncated - see full docs]

---

## LineForce

<Alert severity="info">
For an overview on creating, visualizing, and simulating mover constraints, including `Class.LineForce`, see [Mover constraints](../../physics/mover-constraints.md). Also see [Roblox&nbsp;units](../../physics/units.md) to understand how Roblox units compare to metric units.
</Alert>

The `Class.LineForce` constraint applies force along the theoretical line connecting its two `Class.Attachment|Attachments`. As the end points (attachments) move, the direction of force will change accordingly.

<video controls src="../../assets/physics/constraints/LineForce-Demo.mp4" width="90%" alt="Demo video of LineForce constraint"></video>

## Force location

By default, force is applied to either parent at its attachment location. If desired, force can be focused at each parent's center of mass by toggling on `Class.LineForce.ApplyAtCenterOfMass|ApplyAtCenterOfMass`.

<GridContainer numColumns="2">
  <figure>
    <video controls src="../../assets/physics/constraints/LineForce-ApplyAtCenterOfMass-False.mp4" alt="Video showing ApplyAtCenterOfMass set to false"></video>
    <figcaption>ApplyAtCenterOfMass = **false**</figcaption>
  </figure>
  <figure>
    <video controls src="../../assets/physics/constraints/LineForce-ApplyAtCenterOfMass-True.mp4" alt="Video showing ApplyAtCenterOfMass set to true"></video>
    <figcaption>ApplyAtCenterOfMass = **true**</figcaption>
  </figure>
</GridContainer>

## Inverse square law

When `Class.LineForce.InverseSquareLaw|InverseSquareLaw` is true, the force magnitude is multiplied by the inverse square of the distance, meaning the force will increase exponentially as the two attachments get closer together, like magnets. When using this setting, it's recommended that you set a `Class.LineForce.MaxForce|MaxForce` threshold to prevent infinite force if the attachments align precisely.

<GridContainer numColumns="2">
  <figure>
    <video controls src="../../assets/physics/constraints/LineForce-InverseSquareLaw-False.mp4" alt

[Content truncated - see full docs]

---

## LinearVelocity

<Alert severity="info">
For an overview on creating, visualizing, and simulating mover constraints, including `Class.LinearVelocity`, see [Mover constraints](../../physics/mover-constraints.md). Also see [Roblox&nbsp;units](../../physics/units.md) to understand how Roblox units compare to metric units.
</Alert>

A `Class.LinearVelocity` constraint applies force on an assembly to maintain a constant velocity. It can be set to apply force along a `Datatype.Vector3`, line, or 2D&nbsp;plane.

<video controls src="../../assets/physics/constraints/LinearVelocity-Demo.mp4" width="90%" alt="Demo video of LinearVelocity constraint"></video>

<Alert severity="warning">
The `Class.LinearVelocity` constraint applies a force that attempts to maintain a **constant** linear velocity. If you want to control the amount of force applied, use a [VectorForce](../../physics/constraints/vector-force.md) constraint. Alternatively, if you only need **initial** linear velocity, set the `Class.BasePart.AssemblyLinearVelocity|AssemblyLinearVelocity` property directly on the assembly.
</Alert>

## Relativity

Application of velocity can be controlled through the constraint's `Class.LinearVelocity.RelativeTo|RelativeTo` property. If set to `Enum.ActuatorRelativeTo|World`, force will be applied in world coordinates, independent of the parent or attachment orientations. If set to `Enum.ActuatorRelativeTo|Attachment0` or `Enum.ActuatorRelativeTo|Attachment1`, force will be applied relative to `Class.Constraint.Attachment0|Attachment0` or `Class.Constraint.Attachment1|Attachment1` respectively.

<GridContainer numColumns="2">
  <figure>
    <video controls src="../../assets/physics/constraints/LinearVelocity-RelativeTo-World.mp4" alt="Video showing relative behavior set to world space"></video>
    <figcaption>RelativeTo = **World**</figcaption>
  </figure>
  <figure>
    <video controls src="../../assets/physics/constraints/LinearVelocity-RelativeTo-Attachment0.mp4" alt="Video showing relative beh

[Content truncated - see full docs]

---

## NoCollision

The `Class.NoCollisionConstraint` prevents collisions between two specific parts, but those parts may still register collisions with the rest of the world. Compared to [collision groups](../../workspace/collisions.md#collision-groups), it provides a direct way to disable specific collisions, such as the wheel of a car scraping against the car's body.

---

## Plane

<Alert severity="info">
For an overview on creating, visualizing, and simulating mechanical constraints, including `Class.PlaneConstraint`, see [Mechanical constraints](../../physics/mechanical-constraints.md). Also see [Roblox&nbsp;units](../../physics/units.md) to understand how Roblox units compare to metric units.
</Alert>

A `Class.PlaneConstraint` moves its `Class.Constraint.Attachment0|Attachment0` and `Class.Constraint.Attachment1|Attachment1` into a position/orientation along a plane whose normal vector is the primary axis of `Class.Constraint.Attachment0|Attachment0`. Both parent assemblies remain free to translate and rotate unless otherwise constrained.

<video controls src="../../assets/physics/constraints/Plane-Demo.mp4" width="90%" alt="Demo video of PlaneConstraint"></video>

Compare the following examples for how the orientation of `Class.Constraint.Attachment0|Attachment0` defines the plane, while the orientation of `Class.Constraint.Attachment1|Attachment1` has no bearing.

<Tabs>
  <TabItem label="Orientation = (0, 0, 90)">
    <img src="../../assets/physics/constraints/Plane-Attachment0-1.jpg" width="672" height="378" alt="Attachment0 oriented to (0, 0, 90)" />
  </TabItem>
  <TabItem label="Orientation = (-45, 0, 90)">
    <img src="../../assets/physics/constraints/Plane-Attachment0-2.jpg" width="672" height="378" alt="Attachment0 oriented to (-45, 0, 90)" />
  </TabItem>
</Tabs>

---

## Prismatic

<Alert severity="info">
For an overview on creating, visualizing, and simulating mechanical constraints, including `Class.PrismaticConstraint`, see [Mechanical constraints](../../physics/mechanical-constraints.md). Also see [Roblox&nbsp;units](../../physics/units.md) to understand how Roblox units compare to metric units.
</Alert>

A `Class.PrismaticConstraint` creates a rigid joint between two attachments, allowing them to slide along one axis but not rotate. The constraint can also be [powered](#linear-power) for mechanisms like sliding doors and elevator platforms.

<video controls src="../../assets/physics/constraints/Prismatic-Demo.mp4" width="90%" alt="Demo video of PrismaticConstraint"></video>

<Alert severity="info">
Orientation of a prismatic's attachments affects how it will move. To ensure movement occurs along the desired axis, each attachment's `Class.Attachment.Axis|Axis`, visualized by the yellow arrow, should point in the same direction.
</Alert>

## Linear power

If a prismatic's `Class.PrismaticConstraint|ActuatorType` is set to `Enum.ActuatorType|Motor`, it attempts to translate the attachments with the goal of reaching `Class.PrismaticConstraint|Velocity`. You can further control this translation through both `Class.PrismaticConstraint|MotorMaxAcceleration` and `Class.PrismaticConstraint|MotorMaxForce`.

If a prismatic's `Class.PrismaticConstraint|ActuatorType` is set to `Enum.ActuatorType|Servo`, it attempts to translate the attachments to a set separation specified by `Class.PrismaticConstraint|TargetPosition`. This translation is controlled by `Class.PrismaticConstraint|Speed`, `Class.PrismaticConstraint|LinearResponsiveness`, and `Class.PrismaticConstraint|ServoMaxForce`.

<GridContainer numColumns="2">
  <figure>
    <video controls src="../../assets/physics/constraints/Prismatic-ActuatorType-Motor.mp4" alt="Video showing linear power configured for motor behavior"></video>
    <figcaption>ActuatorType = **Motor**</figcaption>
  </figure>
 

[Content truncated - see full docs]

---

## Rigid

A `Class.RigidConstraint` connects two `Class.Attachment|Attachments` or `Class.Bone|Bones` and ensures they stay in the same relative position/orientation to each other. This flexibility gives it additional functionality beyond `Class.WeldConstraint`, such as attaching accessories to `Class.Attachment|Attachments` on a character rig.

<Alert severity="info">
To attach two `Class.BasePart|BaseParts` together, versus two `Class.Attachment|Attachments` or `Class.Bone|Bones`, see [WeldConstraint](../../physics/constraints/weld.md).
</Alert>

When creating a `Class.RigidConstraint` using Studio's [Constraint](../mechanical-constraints.md#create-constraints) button, the tool behaves differently depending on whether you click on existing `Class.BasePart|BaseParts`, `Class.Attachment|Attachments`, or `Class.Bone|Bones` after the tool is activated:

- Clicking on an existing `Class.BasePart` creates a new `Class.Attachment` upon it as the intended `Class.RigidConstraint.Attachment0` or `Class.RigidConstraint.Attachment1`.
- Clicking on an existing `Class.Attachment` or `Class.Bone` uses that instance as the intended `Class.RigidConstraint.Attachment0` or `Class.RigidConstraint.Attachment1`.

Following the second valid click, a new `Class.RigidConstraint` is created to connect the two new attachments. If either the first or second click is **not** made on a `Class.BasePart`, `Class.Attachment`, or `Class.Bone`, the workflow is canceled and no constraint is created.

---

## Rod

<Alert severity="info">
For an overview on creating, visualizing, and simulating mechanical constraints, including `Class.RodConstraint`, see [Mechanical constraints](../../physics/mechanical-constraints.md). Also see [Roblox&nbsp;units](../../physics/units.md) to understand how Roblox units compare to metric units.
</Alert>

A `Class.RodConstraint` keeps two attachments separated by its defined `Class.RodConstraint.Length|Length`. By default, both attachments can rotate freely, although you can enable limits to restrict rotational tilt.

<video controls src="../../assets/physics/constraints/Rod-Demo.mp4" width="90%" alt="Demo video of RodConstraint"></video>

## Limits

You can limit rotation of the attachments within a cone, independently of each other, by enabling the `Class.RodConstraint.LimitsEnabled|LimitsEnabled` property and setting `Class.RodConstraint.LimitAngle0|LimitAngle0` and `Class.RodConstraint.LimitAngle1|LimitAngle1` respectively.

---

## Rope

<Alert severity="info">
For an overview on creating, visualizing, and simulating mechanical constraints, including `Class.RopeConstraint`, see [Mechanical constraints](../../physics/mechanical-constraints.md). Also see [Roblox&nbsp;units](../../physics/units.md) to understand how Roblox units compare to metric units.
</Alert>

A `Class.RopeConstraint` prevents two attachments from separating further than a defined `Class.RopeConstraint.Length|Length`. The attachments can move closer together than this length and both can freely rotate. `Class.RopeConstraint.Restitution|Restitution` defines the elasticity of the attachments when they reach the separation limit specified by `Class.RopeConstraint.Length|Length`.

This constraint can also be powered to behave as a [motorized winch](#winch).

<video controls src="../../assets/physics/constraints/Rope-Demo.mp4" width="90%" alt="Demo video of RopeConstraint"></video>

## Winch

If a rope's `Class.RopeConstraint.WinchEnabled|WinchEnabled` property is enabled, it attempts to translate the attachments to a set separation specified by `Class.RopeConstraint.WinchTarget|WinchTarget`, effectively the target length of the rope in studs. This translation is controlled by `Class.RopeConstraint.WinchSpeed|WinchSpeed`, `Class.RopeConstraint.WinchResponsiveness|WinchResponsiveness`, and `Class.RopeConstraint.WinchForce|WinchForce`.

<Alert severity="info">
`Class.RopeConstraint.WinchSpeed|WinchSpeed` must be a **positive** value, used to either contract or extend the rope length to `Class.RopeConstraint.WinchTarget|WinchTarget`. Setting a negative speed will revert to&nbsp;0, not reverse the winch servo direction.
</Alert>

---

## Spring

<Alert severity="info">
For an overview on creating, visualizing, and simulating mechanical constraints, including `Class.SpringConstraint`, see [Mechanical constraints](../../physics/mechanical-constraints.md). Also see [Roblox&nbsp;units](../../physics/units.md) to understand how Roblox units compare to metric units.
</Alert>

A `Class.SpringConstraint` applies a force on its attachments based on spring and damper behavior. You can customize a spring's [damping](#damping) and [stiffness](#stiffness), as well as set minimum and maximum [limits](#limits) on the spring's length.

<video controls src="../../assets/physics/constraints/Spring-Demo.mp4" width="90%" alt="Demo video of SpringConstraint"></video>

## Free length

`Class.SpringConstraint.FreeLength|FreeLength` defines the natural resting length of the spring. If the attachments are further apart than the free length, they are forced together; if the attachments are closer together than the free length, they are forced apart.

## Damping

The `Class.SpringConstraint.Damping|Damping` value controls how fast the spring's oscillation dies down. A value of 0 allows the spring to oscillate endlessly, while higher values bring the spring to a rest more quickly.

## Stiffness

`Class.SpringConstraint.Stiffness|Stiffness` sets the strength of the spring. Higher values create a spring that responds with more force when its attachments are closer together or further apart than `Class.SpringConstraint.FreeLength|FreeLength`.

<GridContainer numColumns="2">
  <figure>
    <video controls src="../../assets/physics/constraints/Spring-Stiffness-25.mp4" alt="Video showing Stiffness set to 25"></video>
    <figcaption>Stiffness = **25**</figcaption>
  </figure>
  <figure>
    <video controls src="../../assets/physics/constraints/Spring-Stiffness-500.mp4" alt="Video showing Stiffness set to 500"></video>
    <figcaption>Stiffness = **500**</figcaption>
  </figure>
</GridContainer>

## Limits

Enabling the `Class.SpringConstrai

[Content truncated - see full docs]

---

## Torque

<Alert severity="info">
For an overview on creating, visualizing, and simulating mover constraints, including `Class.Torque`, see [Mover constraints](../../physics/mover-constraints.md). Also see [Roblox&nbsp;units](../../physics/units.md) to understand how Roblox units compare to metric units.
</Alert>

A `Class.Torque` constraint applies constant torque on an assembly from its center of mass.

<video controls src="../../assets/physics/constraints/Torque-Demo.mp4" width="90%" alt="Demo video of Torque constraint"></video>

<Alert severity="warning">
Because the `Class.Torque` constraint applies **constant** torque and angular acceleration, very high speeds may result if no other forces are involved. If you want to maintain a more steady velocity over time, use an [AngularVelocity](../../physics/constraints/angular-velocity.md) constraint. Alternatively, if you only need **initial** velocity, set the `Class.BasePart.AssemblyAngularVelocity|AssemblyAngularVelocity` property directly on the assembly.
</Alert>

## Relativity

By default, torque is applied relative to `Class.Constraint.Attachment0|Attachment0`. If the parent assembly rotates, the torque will change direction to match the adjusted orientation of the attachment.

If `Class.Torque.RelativeTo|RelativeTo` is set to **World**, torque will be applied in world coordinates, independent of the parent or attachment orientations.

If `Class.Torque.RelativeTo|RelativeTo` is set to **Attachment1**, torque will be applied relative to `Class.Constraint.Attachment1|Attachment1` and, if the attachment rotates, change to match its orientation.

<GridContainer numColumns="2">
  <figure>
    <video controls src="../../assets/physics/constraints/Torque-RelativeTo-Attachment0.mp4" alt="Video showing RelativeTo set to Attachment0"></video>
    <figcaption>RelativeTo = **Attachment0**</figcaption>
  </figure>
  <figure>
    <video controls src="../../assets/physics/constraints/Torque-RelativeTo-World.mp4" alt="Video showing Rel

[Content truncated - see full docs]

---

## TorsionSpring

<Alert severity="info">
For an overview on creating, visualizing, and simulating mechanical constraints, including `Class.TorsionSpringConstraint`, see [Mechanical constraints](../../physics/mechanical-constraints.md). Also see [Roblox&nbsp;units](../../physics/units.md) to understand how Roblox units compare to metric units.
</Alert>

A `Class.TorsionSpringConstraint` applies torque based on a relative angle and relative angular velocity. It attempts to bring two axes from two parts together and is useful for [hinged](../../physics/constraints/hinge.md) swinging doors with a spring-back effect.

<video controls src="../../assets/physics/constraints/TorsionSpring-Demo.mp4" width="90%" alt="Demo video of TorsionSpringConstraint"></video>

<Alert severity="info">
Correct orientation of a torsion spring's attachments is important. The constraint will attempt to bring the `Class.Attachment.SecondaryAxis|SecondaryAxis` of each attachment, visualized by the orange arrows, into alignment. When building mechanisms like swinging doors, ensure that the secondary axes are **perpendicular** to the intended axis of rotation.
</Alert>

## Damping

The `Class.TorsionSpringConstraint.Damping|Damping` value controls how fast the spring's oscillation dies down. A value of 0 allows the spring to oscillate endlessly, while higher values bring the spring to a rest more quickly.

<GridContainer numColumns="2">
  <figure>
    <video controls src="../../assets/physics/constraints/TorsionSpring-Damping-0.mp4" alt="Video showing Damping set to 0"></video>
    <figcaption>Damping = **0**</figcaption>
  </figure>
  <figure>
    <video controls src="../../assets/physics/constraints/TorsionSpring-Damping-50.mp4" alt="Video showing Damping set to 50"></video>
    <figcaption>Damping = **50**</figcaption>
  </figure>
</GridContainer>

## Stiffness

`Class.TorsionSpringConstraint.Stiffness|Stiffness` sets the torsional strength of the spring. Higher values create a spring that responds with more fo

[Content truncated - see full docs]

---

## Universal

<Alert severity="info">
For an overview on creating, visualizing, and simulating mechanical constraints, including `Class.UniversalConstraint`, see [Mechanical constraints](../../physics/mechanical-constraints.md). Also see [Roblox&nbsp;units](../../physics/units.md) to understand how Roblox units compare to metric units.
</Alert>

A `Class.UniversalConstraint` ensures two axes on two assemblies remain perpendicular. Example applications include vehicle power transmission to the rear drive shafts, robotics, and more.

<video controls src="../../assets/physics/constraints/Universal-Demo.mp4" width="90%" alt="Demo video of UniversalConstraint"></video>

## Orientations

Orientation of a universal's two attachments affects how it will move. To ensure it behaves correctly, the `Class.Attachment.SecondaryAxis|SecondaryAxis` of the attachments, visualized by the orange arrows, should be **perpendicular** to each other. Note that a green L-shaped indicator appears when the axes are properly oriented.

<Tabs>
  <TabItem label="Axes Perpendicular">
    <img src="../../assets/physics/constraints/Universal-Attachments-Correct.jpg" width="672" height="378" alt="Secondary axes perpendicular for correct behavior" />
  </TabItem>
  <TabItem label="Axes Misoriented">
    <img src="../../assets/physics/constraints/Universal-Attachments-Incorrect.jpg" width="672" height="378" alt="Secondary axes misoriented" />
  </TabItem>
</Tabs>

## Limits

Enabling the `Class.UniversalConstraint.LimitsEnabled|LimitsEnabled` property exposes the `Class.UniversalConstraint.MaxAngle|MaxAngle` limit to restrict tilt within a cone, as well as `Class.UniversalConstraint.Restitution|Restitution` which defines the elasticity of the attachments when they reach the limit.

---

## VectorForce

<Alert severity="info">
For an overview on creating, visualizing, and simulating mover constraints, including `Class.VectorForce`, see [Mover constraints](../../physics/mover-constraints.md). Also see [Roblox&nbsp;units](../../physics/units.md) to understand how Roblox units compare to metric units.
</Alert>

The `Class.VectorForce` constraint applies constant linear force on an assembly. The direction and strength of the force is determined by a `Datatype.Vector3` and can be relative to an attachment on the part, another attachment, or the world coordinate system.

<video controls src="../../assets/physics/constraints/VectorForce-Demo.mp4" width="90%" alt="Demo video of VectorForce constraint"></video>

<Alert severity="warning">
Because the `Class.VectorForce` constraint applies **constant** force and acceleration, very high speeds may result if no other forces are involved. If you want to maintain a more steady velocity over time, use a [LinearVelocity](../../physics/constraints/linear-velocity.md) constraint. Alternatively, if you only need **initial** velocity, set the `Class.BasePart.AssemblyLinearVelocity|AssemblyLinearVelocity` property directly on the assembly.
</Alert>

## Force location

By default, force is applied to the assembly at the location of `Class.Constraint.Attachment0|Attachment0`. Thus, if its center of mass is not aligned with the direction/point of force, torque will be applied as well. If desired, force can be focused at the center of mass by toggling on `Class.VectorForce.ApplyAtCenterOfMass|ApplyAtCenterOfMass`.

<GridContainer numColumns="2">
  <figure>
    <video controls src="../../assets/physics/constraints/VectorForce-ApplyAtCenterOfMass-False.mp4" alt="Video showing ApplyAtCenterOfMass set to false"></video>
    <figcaption>ApplyAtCenterOfMass = **false**</figcaption>
  </figure>
  <figure>
    <video controls src="../../assets/physics/constraints/VectorForce-ApplyAtCenterOfMass-True.mp4" alt="Video showing ApplyAtCenterOfMass set 

[Content truncated - see full docs]

---

## Weld

A `Class.WeldConstraint` connects two `Class.BasePart|BaseParts` and ensures they stay in the same relative position and orientation to each other. Even if the two parts are not touching, you can weld them together.

<Alert severity="info">
To attach two `Class.Attachment|Attachments` or `Class.Bone|Bones`, versus two `Class.BasePart|BaseParts`, see [RigidConstraint](../../physics/constraints/rigid.md).
</Alert>

Unique to `Class.WeldConstraint` are slight behavioral differences in how Studio handles creation and repositioning of welded parts.

<Tabs>
<TabItem label="Weld Creation">
When creating a `Class.WeldConstraint` using Studio's [Constraint](../mechanical-constraints.md#create-constraints) button, the tool behaves differently depending on how many `Class.BasePart|BaseParts` are selected when the tool is activated:

- If no `Class.BasePart|BaseParts` are selected, the next two `Class.BasePart|BaseParts` clicked will be connected by a new `Class.WeldConstraint`. If the same `Class.BasePart` is clicked twice, no constraint will be created.
- If one `Class.BasePart` is already selected, the next `Class.BasePart` clicked will be connected to the selected one with a new `Class.WeldConstraint`.
- If multiple `Class.BasePart|BaseParts` are selected, those which are touching or overlapping will be automatically welded together by new `Class.WeldConstraint|WeldConstraints`.
</TabItem>
<TabItem label="Repositioning Welded Parts">
Roblox handles moving a welded part differently depending on whether the part
was moved through its `Class.BasePart.Position|Position` or through its
`Datatype.CFrame`.

- If a welded part's `Class.BasePart.Position|Position` is updated, that part
  will move but none of the connected parts will move with it. The weld will
  recalculate the offset from the other parts based on the moved part's new
  position.

- If a welded part's `Datatype.CFrame` is updated, that part will move **and**
  all of the connected parts will also move, ensuring the

[Content truncated - see full docs]

---

## Physics

Roblox uses a rigid body physics engine. Parts are subject to physical forces as long as they are not `Class.BasePart.Anchored|anchored`. You can create physical [assemblies](#assemblies) using attachments and constraints, and you can detect and control [collisions](#collisions) between objects using events and collision filtering.

## Assemblies

An [assembly](../physics/assemblies.md) is one or more `Class.BasePart|BaseParts` connected by rigid constraints or motors (animated rigid joints). Assemblies can be set to an initial linear or angular velocity, or their behavior can be affected through [constraints](#constraints).

<Grid container spacing={0}>
  <Grid item XSmall={6} XLarge={3}>
    <img src="../assets/physics/assemblies/Assembly-Example-Block.png" alt="A light blue cube against a dark blue background that represents an assembly of 1 part." width="100%" />
    <figcaption>1&nbsp;assembly; 1&nbsp;part</figcaption>
  </Grid>
  <Grid item XSmall={6} XLarge={3}>
    <img src="../assets/physics/assemblies/Assembly-Example-Avatar.png" alt="A humanoid character model against a dark blue background that represents an assembly of 18 parts." width="100%" />
    <figcaption>1&nbsp;assembly; 18&nbsp;parts</figcaption>
  </Grid>
  <Grid item XSmall={12} XLarge={6}>
    <img src="../assets/physics/assemblies/Assembly-Example-Ship.png" alt="A pirate that represents an assemble of 179 parts." width="100%" />
    <figcaption>1&nbsp;assembly; 179&nbsp;parts</figcaption>
  </Grid>
</Grid>

## Constraints

Non-anchored assemblies react to force from gravity and collisions, but physical force can also be applied through **mechanical constraints** or **mover constraints**.

### Mechanical constraints

Mechanical constraints include familiar objects like hinges, springs, and ropes which can be used to build mechanisms. Each is covered in [Mechanical&nbsp;constraints](../physics/mechanical-constraints.md).

<video src="../assets/physics/constraints/Spring-Demo.mp4" controls widt

[Content truncated - see full docs]

---

## Mechanical constraints

import ConstraintVisualization from '../includes/studio/constraint-visualization.md'
import ConstraintSimulation from '../includes/studio/constraint-simulation.md'

The physics engine includes the following `Class.Constraint|Constraints` that behave as conceptual mechanical connections, including hinges, springs, ropes, and more. In addition, various [mover constraints](../physics/mover-constraints.md) are available to exert directional or rotational force upon [assemblies](../physics/assemblies.md).

<Grid container spacing={4}>

<Grid item XSmall={12} Small={6} Medium={6} Large={6}>
<Card variant="outlined" style={{height: '100%'}}>
<CardContent>
<Button href="../physics/constraints/ball-socket.md" size="large" variant="contained" fullWidth>Ball Socket</Button>
<p></p>
<CardMedia component="video" controls src="../assets/physics/constraints/BallInSocket-Demo.mp4" />
<p></p>
<figcaption>[BallSocketConstraint](../physics/constraints/ball-socket.md) forces its two attachments into the same position and allows them to freely rotate about all three axes, with optional limits to restrict both tilt and twist</figcaption>
</CardContent>
</Card>
</Grid>

<Grid item XSmall={12} Small={6} Medium={6} Large={6}>
<Card variant="outlined" style={{height: '100%'}}>
<CardContent>
<Button href="../physics/constraints/hinge.md" size="large" variant="contained" fullWidth>Hinge</Button>
<p></p>
<CardMedia component="video" controls src="../assets/physics/constraints/Hinge-Demo.mp4" />
<p></p>
<figcaption>[HingeConstraint](../physics/constraints/hinge.md) allows its two attachments to rotate about one axis, with optional assigned power for motor or servo behavior</figcaption>
</CardContent>
</Card>
</Grid>

<Grid item XSmall={12} Small={6} Medium={6} Large={6}>
<Card variant="outlined" style={{height: '100%'}}>
<CardContent>
<Button href="../physics/constraints/prismatic.md" size="large" variant="contained" fullWidth>Prismatic</Button>
<p></p>
<CardMedia component="video" controls src=

[Content truncated - see full docs]

---

## Mover constraints

import ConstraintVisualization from '../includes/studio/constraint-visualization.md'
import ConstraintSimulation from '../includes/studio/constraint-simulation.md'

The physics engine includes the following `Class.Constraint|Constraints` that apply force or torque to move one or more assemblies. In addition, various [mechanical constraints](../physics/mechanical-constraints.md) are available which behave as conceptual mechanical connections, including hinges, springs, ropes, and more.

<Grid container spacing={4}>

<Grid item XSmall={12} Small={6} Medium={6} Large={6}>
<Card variant="outlined" style={{height: '100%'}}>
<CardContent>
<Button href="../physics/constraints/linear-velocity.md" size="large"  variant="contained" fullWidth>Linear Velocity</Button>
<p></p>
<CardMedia component="video" controls src="../assets/physics/constraints/LinearVelocity-Demo.mp4" />
<p></p>
<figcaption>[LinearVelocity](../physics/constraints/linear-velocity.md) applies force on an assembly to maintain a constant velocity along a 3D vector, line, or 2D plane</figcaption>
</CardContent>
</Card>
</Grid>

<Grid item XSmall={12} Small={6} Medium={6} Large={6}>
<Card variant="outlined" style={{height: '100%'}}>
<CardContent>
<Button href="../physics/constraints/angular-velocity.md" size="large" variant="contained" fullWidth>Angular Velocity</Button>
<p></p>
<CardMedia component="video" controls src="../assets/physics/constraints/AngularVelocity-Demo.mp4" />
<p></p>
<figcaption>[AngularVelocity](../physics/constraints/angular-velocity.md) applies torque on an assembly to maintain a constant angular velocity</figcaption>
</CardContent>
</Card>
</Grid>

<Grid item XSmall={12} Small={6} Medium={6} Large={6}>
<Card variant="outlined" style={{height: '100%'}}>
<CardContent>
<Button href="../physics/constraints/align-position.md" size="large" variant="contained" fullWidth>Align Position</Button>
<p></p>
<CardMedia component="video" controls src="../assets/physics/constraints/AlignPosition-Demo.mp4"

[Content truncated - see full docs]

---

## Network ownership

In order to support complex physical mechanisms while also aiming for a smooth and responsive experience for players, the Roblox [physics](../physics/index.md) engine utilizes a **distributed physics** system in which computations are distributed between the server and all connected clients. Within this system, the engine assigns **network ownership** of physically simulated `Class.BasePart|BaseParts` to either a client or server to divide the work of calculating physics.

Clients experience **more responsive** physics interactions with parts that they own, since there's no latency from communication with the server. Network ownership also improves server performance because physics computations can be split up among individual clients, allowing the server to prioritize other tasks.

## BasePart ownership

By default, the server retains ownership of any `Class.BasePart`. Additionally, the server **always** owns anchored `Class.BasePart|BaseParts` and you cannot manually change their ownership.

Based on a client's hardware capacity and the player's `Class.Player.Character` proximity to an unanchored `Class.BasePart`, the engine automatically assigns ownership of that part to the client. Thus, parts close to a player's character are more likely to become player-owned.

## Assembly ownership

If a physics-based mechanism has no anchored parts, [setting ownership](#setting-ownership) on an [assembly](../physics/assemblies.md) within that mechanism sets the same ownership for **every assembly** in the mechanism.

If you anchor a lone assembly that is **not** part of a broader mechanism, its ownership goes to the server, since the server always owns anchored `Class.BasePart|BaseParts`. Upon unanchoring the same assembly, its previous ownership state is lost and it reverts to automatic handling by the engine.

If you anchor one assembly within a broader mechanism of assemblies, its ownership goes to the server, but ownership of the other assemblies remains unchanged. Unan

[Content truncated - see full docs]

---

## Sleep system

Each [assembly](../physics/assemblies.md) in the Roblox Engine corresponds to a single **rigid body**. The position and velocity of each rigid body describe where it's located and how fast it's moving, and one of the primary engine tasks is to update the positions and velocities of each assembly.

Assemblies can be connected together with [mechanical constraints](../physics/mechanical-constraints.md) and [mover constraints](../physics/mover-constraints.md) to form mechanisms such as cars or airplanes. As the number of assemblies and constraints in a mechanism increases, the time required to simulate the mechanism also increases. Fortunately, this increase is offset when the **sleep system** determines that the engine can skip simulation of non‑moving assemblies.

## Sleep states

Each assembly can be in one of three states: [awake](#awake), [sleeping](#sleeping), or [sleep‑checking](#sleep-checking).

### Awake

An **awake** assembly is moving or accelerating, and is therefore simulated. Assemblies enter this state from situations outlined in [sleeping](#sleeping) and [sleep‑checking](#sleep-checking), as well as [additional wake situations](#additional-wake-situations).

### Sleeping

A **sleeping** assembly is neither moving nor accelerating, and is therefore not simulated.

An assembly is determined to be non-moving by checking its **linear velocity** and **rotational velocity**. If its linear velocity is less than the [Linear&nbsp;Velocity](#threshold-reference) threshold and its rotational velocity is less than the [Rotational&nbsp;Velocity](#threshold-reference) threshold, the assembly is considered to be non-moving.

In some cases, simply checking for non-movement would cause an assembly to incorrectly enter the sleeping state. For example, if a ball is thrown straight up, its velocity approaches zero as it reaches its maximum height, making it a candidate to sleep and never fall back down. To handle such cases, the engine considers an assembly to be accelera

[Content truncated - see full docs]

---

## Roblox units

This article outlines Roblox physical units and how they convert to metric units. Understanding units is useful whenever you work with physics, as in the following examples:

- Customizing your experience's gravity, jump height/power, and walk speed in the **World** tab of Studio's **File**&nbsp;⟩ **Game Settings** window.
- Tuning linear/angular velocities, forces, torques, stiffness, and damping of [mechanical constraints](../physics/mechanical-constraints.md) and [mover constraints](../physics/mover-constraints.md).
- Adjusting the density of [custom materials](../parts/materials.md#custom-materials).

## Unit conversions

<Tabs>
<TabItem label="Primary Units">

In general, you can use the conversions in the following table to relate Roblox's primary units for time, length, and mass to their metric counterparts.
<table size="small">
<thead>
	<tr>
		<th>Unit</th>
		<th>Roblox</th>
		<th>Metric</th>
	</tr>
</thead>
<tbody>
	<tr>
		<td>**Time**</td>
		<td>1 second</td>
		<td>1 second</td>
	</tr>
	<tr>
		<td>**Length**</td>
		<td>1 stud</td>
		<td>28 cm</td>
	</tr>
	<tr>
		<td>**Mass**</td>
		<td>1 RMU*</td>
		<td>21.952 kg</td>
	</tr>
</tbody>
</table>
<figcaption>\* RMU = Roblox Mass Unit</figcaption>
</TabItem>
<TabItem label="Derived units">

The primary units are used to generate conversions for **derived** units such as water density and air pressure at standard conditions. The following physical properties are expressed in metric units and Roblox units, with primary unit equivalents provided in brackets. All conversions have been rounded to three significant figures.

<table size="small">
<thead>
	<tr>
		<th>Unit</th>
		<th>Metric</th>
		<th>Roblox</th>
	</tr>
</thead>
<tbody>
	<tr>
		<td>**Water Density**</td>
		<td>1 g/cm&sup3;</td>
		<td>1 RMU/stud&sup3;</td>
	</tr>
	<tr>
		<td>**Air Density** (sea&nbsp;level)</td>
		<td>0.00129 g/cm&sup3;</td>
		<td>0.00129 RMU/stud&sup3;</td>
	</tr>
	<tr>
		<td>**1 atmosphere**</td>
		<td>101,325 Pa *[kg/(m s&sup2;)]*</td

[Content truncated - see full docs]

---

