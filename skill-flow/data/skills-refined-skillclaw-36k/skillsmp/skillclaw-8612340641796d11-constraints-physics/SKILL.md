---
name: constraints-physics
description: Use this skill when implementing constraint-based physics systems, including ragdolls, mechanical systems, and rope physics in your gameplay.
---

# Skill body

When implementing physics systems, use these constraint patterns for realistic and performant mechanics.

## Constraint Reference

### WeldConstraint
```lua
-- Rigid connection between two parts (no relative movement)
local weld = Instance.new("WeldConstraint")
weld.Part0 = part1
weld.Part1 = part2
weld.Parent = part1

-- Use for: Static connections, attaching accessories
-- Note: More efficient than Motor6D for non-animated joints
```

### Motor6D
```lua
-- Animated joint with C0/C1 transforms
local motor = Instance.new("Motor6D")
motor.Part0 = torso
motor.Part1 = arm
motor.C0 = CFrame.new(1.5, 0.5, 0)  -- Offset from Part0
motor.C1 = CFrame.new(0, 0.5, 0)    -- Offset from Part1
motor.Parent = torso

-- Animate by changing Transform property
motor.Transform = CFrame.Angles(0, 0, math.rad(45))

-- Use for: Character rigs, animated machinery
```

### HingeConstraint
```lua
-- Single-axis rotation (doors, wheels)
local hinge = Instance.new("HingeConstraint")
hinge.Attachment0 = attachment0  -- On Part0
hinge.Attachment1 = attachment1  -- On Part1

-- Limits
hinge.LimitsEnabled = true
hinge.LowerAngle = -90
hinge.UpperAngle = 90

-- Motor mode (powered rotation)
hinge.ActuatorType = Enum.ActuatorType.Motor
hinge.MotorMaxTorque = 10000
hinge.AngularVelocity = 10  -- Target velocity (rad/s)

-- Servo mode (target angle)
hinge.ActuatorType = Enum.ActuatorType.Servo
hinge.TargetAngle = 45
hinge.AngularSpeed = 5
hinge.ServoMaxTorque = 10000

hinge.Parent = part1

-- Read current angle
local currentAngle = hinge.CurrentAngle
```

### BallSocketConstraint
```lua
-- Three-axis rotation (ragdoll joints)
local ballSocket = Instance.new("BallSocketConstraint")
ballSocket.Attachment0 = attachment0
ballSocket.Attachment1 = attachment1

-- Twist limits (rotation around axis)
ballSocket.TwistLimitsEnabled = true
ballSocket.TwistLowerAngle = -45
ballSocket.TwistUpperAngle = 45

-- Cone limits (swing angle)
ballSocket.LimitsEnabled = true
ballSocket.UpperAngle = 60  -- Max angle from axis

ballSocket.Parent = part1
```

### RopeConstraint
```lua
-- Flexible connection with max length
local rope = Instance.new("RopeConstraint")
rope.Length = 10  -- Set the maximum length of the rope
rope.Attachment0 = attachment0
rope.Attachment1 = attachment1
rope.Parent = part1
```