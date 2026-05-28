# Physics Classes

## Contents
- [Weld](#weld)
- [WeldConstraint](#weldconstraint)
- [Motor6D](#motor6d)
- [HingeConstraint](#hingeconstraint)
- [SpringConstraint](#springconstraint)
- [RopeConstraint](#ropeconstraint)
- [RodConstraint](#rodconstraint)
- [AlignPosition](#alignposition)
- [AlignOrientation](#alignorientation)
- [BodyPosition](#bodyposition)
- [BodyVelocity](#bodyvelocity)
- [BodyForce](#bodyforce)
- [BodyGyro](#bodygyro)
- [VectorForce](#vectorforce)

---

## Weld

---

## WeldConstraint

Connects two `Class.BasePart|BaseParts` together such that their relative
position and orientation remain the same.

**Properties:**
- `WeldConstraint.Active`: boolean - Indicates if the WeldConstraint is currently active in the world.
- `WeldConstraint.Enabled`: boolean - Toggles the constraint on and off.
- `WeldConstraint.Part0`: BasePart - The first part connected by the constraint.
- `WeldConstraint.Part1`: BasePart - The second part connected by the constraint.

---

## Motor6D

Creates an animatable joint between two `Class.BasePart|BaseParts`.

**Properties:**
- `Motor6D.ChildName`: string
- `Motor6D.ParentName`: string
- `Motor6D.Transform`: CFrame - Describes the current animation offset of the `Class.Motor6D` joint.

---

## HingeConstraint

Constrains its attachments to rotate about a single axis.

**Properties:**
- `HingeConstraint.ActuatorType`: ActuatorType - Sets whether the rotation of the `Class.HingeConstraint` is actuated and,
- `HingeConstraint.AngularResponsiveness`: float - Specifies the sharpness of the servo motor in reaching the
- `HingeConstraint.AngularSpeed`: float - The desired angular speed a `Class.HingeConstraint` with
- `HingeConstraint.AngularVelocity`: float - The angular velocity a `Class.HingeConstraint` with
- `HingeConstraint.CurrentAngle`: float - The current angle of the `Class.HingeConstraint`.
- `HingeConstraint.LimitsEnabled`: boolean - Sets whether the `Class.HingeConstraint` will limit the range of rotation.
- `HingeConstraint.LowerAngle`: float - The minimum rotation angle the `Class.HingeConstraint` will allow if
- `HingeConstraint.MotorMaxAcceleration`: float - The maximum angular acceleration a `Class.HingeConstraint` with
- `HingeConstraint.MotorMaxTorque`: float - The maximum torque a `Class.HingeConstraint` with
- `HingeConstraint.Radius`: float - The visualized radius of the `Class.HingeConstraint`.
- ...and 5 more

---

## SpringConstraint

Simulates spring and damper behavior between two attachments.

**Properties:**
- `SpringConstraint.Coils`: float - The number of coils visualized on the `Class.SpringConstraint`.
- `SpringConstraint.CurrentLength`: float - The current distance between the constraint's
- `SpringConstraint.Damping`: float - Damping constant for the `Class.SpringConstraint`. Multiplied to the
- `SpringConstraint.FreeLength`: float - Natural resting length of the spring.
- `SpringConstraint.LimitsEnabled`: boolean - Sets whether the `Class.SpringConstraint` enforces a minimum and maximum
- `SpringConstraint.MaxForce`: float - The maximum force the `Class.SpringConstraint` can apply on its
- `SpringConstraint.MaxLength`: float - The maximum separation the SpringConstraint will allow if
- `SpringConstraint.MinLength`: float - The minimum separation the SpringConstraint will allow if
- `SpringConstraint.Radius`: float - The visualized radius of the spring's coils.
- `SpringConstraint.Stiffness`: float - The strength of the spring. The higher this value the more force will be
- ...and 1 more

---

## RopeConstraint

Simulates rope dynamics, preventing two attachments from separating further
than a defined length.

**Properties:**
- `RopeConstraint.CurrentDistance`: float - The current distance between the constraint's
- `RopeConstraint.Length`: float - The maximum distance apart the two `Class.Attachment|Attachments` can be.
- `RopeConstraint.Restitution`: float - Elasticity of the `Class.Attachment|Attachments` connected by the
- `RopeConstraint.Thickness`: float - The visualized thickness of the `Class.RopeConstraint`.
- `RopeConstraint.WinchEnabled`: boolean - Enables the winch motor.
- `RopeConstraint.WinchForce`: float - The maximum force that the winch motor can apply.
- `RopeConstraint.WinchResponsiveness`: float - The sharpness of the winch motor in reaching the
- `RopeConstraint.WinchSpeed`: float - A positive desired velocity at which the winch motor changes the rope
- `RopeConstraint.WinchTarget`: float - The target length for the winch motor.

---

## RodConstraint

Keeps two attachments separated by its defined
`Class.RodConstraint.Length|Length`.

**Properties:**
- `RodConstraint.CurrentDistance`: float - The current distance between the constraint's
- `RodConstraint.Length`: float - The distance apart at which the constraint attempts to keep its
- `RodConstraint.LimitAngle0`: float - The maximum angle between the rod and
- `RodConstraint.LimitAngle1`: float - The maximum angle between the rod and
- `RodConstraint.LimitsEnabled`: boolean - Determines whether `Class.RodConstraint.LimitAngle0|LimitAngle0` and
- `RodConstraint.Thickness`: float - The visualized thickness of the `Class.RodConstraint`.

---

## AlignPosition

Constraint which applies force to move two attachments together, or to move
one attachment to a goal position.

**Properties:**
- `AlignPosition.ApplyAtCenterOfMass`: boolean - Whether force is applied to the parent of
- `AlignPosition.ForceLimitMode`: ForceLimitMode - Determines how the constraint force will be limited. Only used if
- `AlignPosition.ForceRelativeTo`: ActuatorRelativeTo - Determines the axes that the constraint uses to limit the force. Only
- `AlignPosition.MaxAxesForce`: Vector3 - Maximum force along each axis that the constraint can apply to achieve its
- `AlignPosition.MaxForce`: float - Maximum force magnitude the constraint can apply to achieve its goal.
- `AlignPosition.MaxVelocity`: float - Maximum speed the attachments can move when converging.
- `AlignPosition.Mode`: PositionAlignmentMode - Whether the constraint uses one or two attachments in calculating its
- `AlignPosition.Position`: Vector3 - The position to which the constraint should move its
- `AlignPosition.ReactionForceEnabled`: boolean - Whether the constraint applies force only to
- `AlignPosition.Responsiveness`: float - Controls how quickly the constraint reaches its goal. Higher values cause
- ...and 1 more

---

## AlignOrientation

Constraint which applies torque to align two attachments, or to align one
attachment with a goal orientation.

**Properties:**
- `AlignOrientation.AlignType`: AlignType - The constraint's axis alignment type.
- `AlignOrientation.CFrame`: CFrame - The `Datatype.CFrame` orientation with which the constraint will attempt
- `AlignOrientation.LookAtPosition`: Vector3 - A `Datatype.Vector3` world space location toward which the primary axis
- `AlignOrientation.MaxAngularVelocity`: float - Maximum angular velocity the constraint can use to reach its goal.
- `AlignOrientation.MaxTorque`: float - Maximum torque the constraint can use to reach its goal.
- `AlignOrientation.Mode`: OrientationAlignmentMode - Whether the constraint uses one or two attachments in calculating its
- `AlignOrientation.PrimaryAxis`: Vector3 - The direction of the goal's **X** axis, represented as a unit
- `AlignOrientation.PrimaryAxisOnly`: boolean - Determines how the constraint's axes are affected by torque.
- `AlignOrientation.ReactionTorqueEnabled`: boolean - Whether the constraint applies torque only to
- `AlignOrientation.Responsiveness`: float - Controls how quickly the constraint reaches its goal. Higher values cause
- ...and 2 more

---

## BodyPosition

Applies a force to maintain a constant position.

**Properties:**
- `BodyPosition.D`: float - Determines the amount of dampening to use in reaching the goal
- `BodyPosition.MaxForce`: Vector3 - Determines the limit on how much force that may be applied to each axis.
- `BodyPosition.maxForce`: Vector3
- `BodyPosition.P`: float - Determines how aggressive of a force is applied in reaching the goal
- `BodyPosition.Position`: Vector3 - Determines the goal position towards which force will be applied.
- `BodyPosition.position`: Vector3

**Methods:**
- `BodyPosition:GetLastForce` - Returns the last force in the object.
- `BodyPosition:lastForce` - Returns the last force in the object.

**Events:**
- `BodyPosition.ReachedTarget` - Fired when the Parent of the BodyPosition reaches the desired

---

## BodyVelocity

Applies a force to maintain a constant velocity.

**Properties:**
- `BodyVelocity.MaxForce`: Vector3 - Determines the limit on how much force that may be applied to each axis.
- `BodyVelocity.maxForce`: Vector3
- `BodyVelocity.P`: float - Determines how aggressive of a force is applied in reaching the goal
- `BodyVelocity.Velocity`: Vector3 - Determines the goal velocity.
- `BodyVelocity.velocity`: Vector3

**Methods:**
- `BodyVelocity:GetLastForce` - Not implemented and will always return the `0` vector.
- `BodyVelocity:lastForce` - Returns the last force in the object.

---

## BodyForce

Applies a constant force to an object.

**Properties:**
- `BodyForce.Force`: Vector3 - Determines the force exerted on each axis.
- `BodyForce.force`: Vector3 - Determines the amount of force applied on each axis.

---

## BodyGyro

Applies a torque to maintain a constant orientation.

**Properties:**
- `BodyGyro.CFrame`: CFrame - Determines the target orientation (translational component ignored).
- `BodyGyro.cframe`: CFrame
- `BodyGyro.D`: float - Determines the amount of dampening to use in reaching the goal
- `BodyGyro.MaxTorque`: Vector3 - Determines the limit on how much torque that may be applied to each axis.
- `BodyGyro.maxTorque`: Vector3
- `BodyGyro.P`: float - Determines how aggressive of a torque is applied in reaching the goal

---

## VectorForce

Applies constant force to an assembly.

**Properties:**
- `VectorForce.ApplyAtCenterOfMass`: boolean - Whether force is applied at the center of mass of the parent assembly.
- `VectorForce.Force`: Vector3 - The strength and direction of the force.
- `VectorForce.RelativeTo`: ActuatorRelativeTo - The `Datatype.CFrame` in which the force is expressed.

---

