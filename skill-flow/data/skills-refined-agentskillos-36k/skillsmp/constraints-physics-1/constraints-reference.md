# Roblox Constraints API Reference

Complete property reference for all mechanical constraints.

---

## BallSocketConstraint

Forces two attachments into the same position, allows free rotation about all axes.

### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `LimitsEnabled` | boolean | false | Restricts tilt within cone |
| `UpperAngle` | number | 45 | Max tilt angle (degrees) when limits enabled |
| `TwistLimitsEnabled` | boolean | false | Restricts twist rotation |
| `TwistLowerAngle` | number | -45 | Min twist (degrees) |
| `TwistUpperAngle` | number | 45 | Max twist (degrees) |
| `MaxFrictionTorque` | number | 0 | Resistance to rotation (stiffness) |
| `Restitution` | number | 0 | Elasticity at limits (0-1) |
| `Radius` | number | 0.15 | Visual radius |

### Typical Values

| Use Case | MaxFrictionTorque | UpperAngle |
|----------|-------------------|------------|
| Ragdoll joint | 0-100 | 30-60 |
| Stiff joint | 500-1000 | 15-30 |
| Free rotation | 0 | 180 |

---

## HingeConstraint

Single-axis rotation like a door hinge.

### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `ActuatorType` | Enum | None | None, Motor, or Servo |
| `AngularVelocity` | number | 0 | Target speed for Motor (rad/s) |
| `MotorMaxTorque` | number | 0 | Max torque for Motor |
| `MotorMaxAcceleration` | number | inf | Max acceleration for Motor |
| `TargetAngle` | number | 0 | Target for Servo (degrees) |
| `ServoMaxTorque` | number | 0 | Max torque for Servo |
| `AngularSpeed` | number | 0 | Servo rotation speed (rad/s) |
| `AngularResponsiveness` | number | 45 | Servo sharpness |
| `LimitsEnabled` | boolean | false | Enable rotation limits |
| `LowerAngle` | number | -45 | Min angle (degrees) |
| `UpperAngle` | number | 45 | Max angle (degrees) |
| `Restitution` | number | 0 | Bounce at limits (0-1) |
| `CurrentAngle` | number | - | Read-only current angle |

### Typical Values

| Use Case | ActuatorType | Torque | Speed |
|----------|--------------|--------|-------|
| Door | Servo | 10000 | 2 |
| Vehicle wheel | Motor | 500-2000 | varies |
| Propeller | Motor | math.huge | 50+ |
| Turret | Servo | 50000 | 3 |

---

## PrismaticConstraint

Linear sliding along one axis. Inherits from SlidingBallConstraint.

### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `ActuatorType` | Enum | None | None, Motor, or Servo |
| `Velocity` | number | 0 | Speed for Motor (studs/s) |
| `MotorMaxForce` | number | 0 | Max force for Motor |
| `TargetPosition` | number | 0 | Target for Servo (studs) |
| `ServoMaxForce` | number | 0 | Max force for Servo |
| `Speed` | number | 0 | Servo movement speed |
| `LinearResponsiveness` | number | 45 | Servo sharpness |
| `LimitsEnabled` | boolean | false | Enable position limits |
| `LowerLimit` | number | 0 | Min position (studs) |
| `UpperLimit` | number | 0 | Max position (studs) |
| `Restitution` | number | 0 | Bounce at limits (0-1) |
| `CurrentPosition` | number | - | Read-only current position |

### Typical Values

| Use Case | ActuatorType | Force | Speed |
|----------|--------------|-------|-------|
| Sliding door | Servo | 10000 | 3 |
| Elevator | Servo | mass * g * 2 | 5 |
| Train | Motor | math.huge | varies |

---

## CylindricalConstraint

Combined sliding + rotation. Ideal for vehicle wheels with suspension.

### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `ActuatorType` | Enum | None | Linear: None/Motor/Servo |
| `AngularActuatorType` | Enum | None | Rotation: None/Motor/Servo |
| `AngularVelocity` | number | 0 | Wheel spin (rad/s) |
| `MotorMaxTorque` | number | 0 | Rotation motor torque |
| `MotorMaxAngularAcceleration` | number | inf | Rotation acceleration |
| `TargetAngle` | number | 0 | Steering target (degrees) |
| `ServoMaxTorque` | number | 0 | Steering servo torque |
| `AngularSpeed` | number | 0 | Steering speed (rad/s) |
| `AngularResponsiveness` | number | 45 | Steering sharpness |
| `InclinationAngle` | number | 0 | Rotation axis tilt (-180 to 180) |
| `LimitsEnabled` | boolean | false | Linear limits |
| `AngularLimitsEnabled` | boolean | false | Rotation limits |
| `LowerAngle` / `UpperAngle` | number | ±45 | Steering range |
| `CurrentAngle` | number | - | Read-only current angle |
| `CurrentPosition` | number | - | Read-only current position |

### Typical Values

| Use Case | Angular Type | Torque | Velocity |
|----------|--------------|--------|----------|
| Drive wheel | Motor | 500-2000 | speed/radius |
| Steering | Servo | 10000 | - |
| Suspension travel | limits | - | - |

---

## SpringConstraint

Spring/damper force between attachments.

### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `FreeLength` | number | 1 | Natural resting length (studs) |
| `Stiffness` | number | 0 | Spring force strength |
| `Damping` | number | 0 | Oscillation reduction |
| `MaxForce` | number | inf | Force cap |
| `LimitsEnabled` | boolean | false | Min/Max length limits |
| `MinLength` | number | 0 | Minimum length |
| `MaxLength` | number | 0 | Maximum length |
| `CurrentLength` | number | - | Read-only current length |
| `Coils` | number | 8 | Visual coil count (0-8) |
| `Radius` | number | 0.4 | Visual coil radius |
| `Thickness` | number | 0.1 | Visual coil thickness |

### Typical Values

| Vehicle Type | Stiffness | Damping | MaxForce |
|--------------|-----------|---------|----------|
| Light car | 500-1000 | 50-100 | 3000-5000 |
| Heavy truck | 2000-5000 | 200-500 | 15000+ |
| Off-road | 1000-2000 | 100-200 | 8000-12000 |
| Racing | 3000-6000 | 300-600 | 20000+ |

### Formulas

```lua
-- Critical damping (no oscillation)
damping = 2 * math.sqrt(stiffness * mass)

-- Stiffness from target force
stiffness = targetForce / expectedDisplacement
```

---

## RopeConstraint

Prevents separation beyond defined length. Optional winch motor.

### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Length` | number | 5 | Maximum separation (studs) |
| `Restitution` | number | 0 | Bounce when taut (0-1) |
| `Thickness` | number | 0.1 | Visual thickness |
| `WinchEnabled` | boolean | false | Enable motorized control |
| `WinchTarget` | number | 0 | Target length for winch |
| `WinchSpeed` | number | 0 | Retraction/extension speed |
| `WinchForce` | number | 0 | Motor strength |
| `WinchResponsiveness` | number | 45 | Winch servo sharpness |
| `CurrentDistance` | number | - | Read-only current distance |

### Typical Values

| Use Case | Length | WinchSpeed | WinchForce |
|----------|--------|------------|------------|
| Grapple | varies | 20 | 5000 |
| Leash | 10-20 | - | - |
| Fishing line | 50+ | reelSpeed | 1000 |

---

## RodConstraint

Fixed distance between attachments. Like a rigid bar.

### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Length` | number | 5 | Fixed separation (studs) |
| `LimitsEnabled` | boolean | false | Enable angle limits |
| `LimitAngle0` | number | 90 | Rotation limit at Attachment0 |
| `LimitAngle1` | number | 90 | Rotation limit at Attachment1 |
| `Thickness` | number | 0.1 | Visual thickness |
| `CurrentDistance` | number | - | Read-only (equals Length) |

### Typical Values

| Use Case | LimitAngle0 | LimitAngle1 |
|----------|-------------|-------------|
| Rigid bar | 0 | 0 |
| Lantern | 45 | 15 |
| Steering linkage | 90 | 90 |

---

## TorsionSpringConstraint

Angular spring that applies torque to align axes.

### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Stiffness` | number | 0 | Rotational spring strength |
| `Damping` | number | 0 | Angular oscillation reduction |
| `MaxTorque` | number | inf | Force cap |
| `LimitsEnabled` | boolean | false | Enable angle limits |
| `MaxAngle` | number | 45 | Max deviation (degrees) |
| `CurrentAngle` | number | - | Read-only current angle |
| `Coils` | number | 8 | Visual coil count |
| `Radius` | number | 0.4 | Visual radius |

**Note:** Not visible even when `Visible = true`.

### Typical Values

| Use Case | Stiffness | Damping |
|----------|-----------|---------|
| Self-centering door | 100 | 50 |
| Basketball rim | 500 | 20 |
| Stabilizer | 1000 | 200 |

---

## UniversalConstraint

Ensures two axes remain perpendicular.

### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `LimitsEnabled` | boolean | false | Enable cone limit |
| `MaxAngle` | number | 45 | Cone angle limit (degrees) |
| `Restitution` | number | 0 | Bounce at limits (0-1) |
| `Radius` | number | 0.2 | Visual radius |

---

## WeldConstraint

Rigid connection between two parts. No Attachments required.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `Part0` | BasePart | First part |
| `Part1` | BasePart | Second part |
| `Enabled` | boolean | Whether active |

---

## RigidConstraint

Rigid connection using Attachments. Can connect to Bones.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `Attachment0` | Attachment | First attachment |
| `Attachment1` | Attachment | Second attachment |

---

## NoCollisionConstraint

Prevents collision between two specific parts.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `Part0` | BasePart | First part |
| `Part1` | BasePart | Second part |
| `Enabled` | boolean | Whether active |

---

## PlaneConstraint

Constrains attachments to move along a plane.

### Properties

(Inherits standard Constraint properties)

---

## Base Constraint Properties

All constraints inherit:

| Property | Type | Description |
|----------|------|-------------|
| `Attachment0` | Attachment | First attachment |
| `Attachment1` | Attachment | Second attachment |
| `Enabled` | boolean | Whether active |
| `Visible` | boolean | Show visualization |
| `Color` | BrickColor | Visualization color |
