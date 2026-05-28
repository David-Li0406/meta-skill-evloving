# Constraint Code Samples

Copy-paste ready code snippets for common constraint operations.

---

## Creating Constraints Programmatically

### Basic Constraint Creation

```lua
-- Create attachment pair
local function createAttachmentPair(part0, part1, cf0, cf1)
    local a0 = Instance.new("Attachment")
    a0.CFrame = cf0 or CFrame.new()
    a0.Parent = part0

    local a1 = Instance.new("Attachment")
    a1.CFrame = cf1 or CFrame.new()
    a1.Parent = part1

    return a0, a1
end

-- Create any constraint
local function createConstraint(constraintType, a0, a1, properties)
    local constraint = Instance.new(constraintType)
    constraint.Attachment0 = a0
    constraint.Attachment1 = a1

    for prop, value in pairs(properties or {}) do
        constraint[prop] = value
    end

    constraint.Parent = a0.Parent
    return constraint
end
```

### HingeConstraint

```lua
-- Motor hinge (continuous rotation)
local function createMotorHinge(part0, part1, velocity, torque)
    local a0, a1 = createAttachmentPair(part0, part1)

    local hinge = Instance.new("HingeConstraint")
    hinge.Attachment0 = a0
    hinge.Attachment1 = a1
    hinge.ActuatorType = Enum.ActuatorType.Motor
    hinge.AngularVelocity = velocity or 10
    hinge.MotorMaxTorque = torque or 1000
    hinge.Parent = part0

    return hinge
end

-- Servo hinge (target angle)
local function createServoHinge(part0, part1, targetAngle, speed)
    local a0, a1 = createAttachmentPair(part0, part1)

    local hinge = Instance.new("HingeConstraint")
    hinge.Attachment0 = a0
    hinge.Attachment1 = a1
    hinge.ActuatorType = Enum.ActuatorType.Servo
    hinge.TargetAngle = targetAngle or 0
    hinge.AngularSpeed = speed or 2
    hinge.ServoMaxTorque = 10000
    hinge.Parent = part0

    return hinge
end
```

### SpringConstraint

```lua
-- Vehicle suspension spring
local function createSuspensionSpring(chassisAttachment, wheelAttachment, vehicleMass, numWheels)
    local spring = Instance.new("SpringConstraint")
    spring.Attachment0 = chassisAttachment
    spring.Attachment1 = wheelAttachment

    local forcePerWheel = vehicleMass * workspace.Gravity / numWheels
    spring.FreeLength = 2
    spring.Stiffness = forcePerWheel / 0.5
    spring.Damping = 2 * math.sqrt(spring.Stiffness * (vehicleMass / numWheels))
    spring.MaxForce = forcePerWheel * 3
    spring.LimitsEnabled = true
    spring.MinLength = 1
    spring.MaxLength = 3

    spring.Parent = chassisAttachment.Parent
    return spring
end
```

### RopeConstraint

```lua
-- Grapple rope with winch
local function createGrappleRope(playerAttachment, targetAttachment)
    local rope = Instance.new("RopeConstraint")
    rope.Attachment0 = playerAttachment
    rope.Attachment1 = targetAttachment
    rope.Length = (playerAttachment.WorldPosition - targetAttachment.WorldPosition).Magnitude
    rope.Visible = true
    rope.Thickness = 0.1
    rope.WinchEnabled = true
    rope.WinchSpeed = 30
    rope.WinchForce = 10000
    rope.WinchTarget = 5
    rope.Parent = playerAttachment.Parent

    return rope
end
```

### BallSocketConstraint

```lua
-- Ragdoll joint
local function createRagdollJoint(motor6d)
    local a0 = Instance.new("Attachment")
    local a1 = Instance.new("Attachment")
    a0.CFrame = motor6d.C0
    a1.CFrame = motor6d.C1
    a0.Parent = motor6d.Part0
    a1.Parent = motor6d.Part1

    local socket = Instance.new("BallSocketConstraint")
    socket.Attachment0 = a0
    socket.Attachment1 = a1
    socket.LimitsEnabled = true
    socket.TwistLimitsEnabled = true
    socket.UpperAngle = 45
    socket.TwistLowerAngle = -30
    socket.TwistUpperAngle = 30
    socket.MaxFrictionTorque = 50
    socket.Parent = motor6d.Part0

    motor6d.Enabled = false
    return socket
end
```

---

## Network Ownership

```lua
-- Set vehicle to player ownership
local function setVehicleOwner(vehicle, player)
    for _, part in pairs(vehicle:GetDescendants()) do
        if part:IsA("BasePart") then
            if part:CanSetNetworkOwnership() then
                part:SetNetworkOwner(player)
            end
        end
    end
end

-- Set to server ownership
local function setServerOwner(model)
    for _, part in pairs(model:GetDescendants()) do
        if part:IsA("BasePart") then
            if part:CanSetNetworkOwnership() then
                part:SetNetworkOwner(nil)
            end
        end
    end
end

-- Auto-set on seat occupancy
seat:GetPropertyChangedSignal("Occupant"):Connect(function()
    local occupant = seat.Occupant
    if occupant then
        local player = game.Players:GetPlayerFromCharacter(occupant.Parent)
        if player then
            setVehicleOwner(vehicle, player)
        end
    else
        setServerOwner(vehicle)
    end
end)
```

---

## Collision Groups for Ragdolls

```lua
local PhysicsService = game:GetService("PhysicsService")

-- Setup once
local function setupRagdollCollisionGroup()
    PhysicsService:RegisterCollisionGroup("Ragdoll")
    PhysicsService:CollisionGroupSetCollidable("Ragdoll", "Ragdoll", false)
end

-- Apply to character
local function setRagdollCollisionGroup(character)
    for _, part in pairs(character:GetDescendants()) do
        if part:IsA("BasePart") then
            part.CollisionGroup = "Ragdoll"
        end
    end
end

-- Reset to default
local function resetCollisionGroup(character)
    for _, part in pairs(character:GetDescendants()) do
        if part:IsA("BasePart") then
            part.CollisionGroup = "Default"
        end
    end
end
```

---

## Utility Functions

### Calculate Vehicle Mass

```lua
local function getModelMass(model)
    local mass = 0
    for _, part in pairs(model:GetDescendants()) do
        if part:IsA("BasePart") then
            mass = mass + part:GetMass()
        end
    end
    return mass
end
```

### Aim Angle Calculations

```lua
-- Calculate yaw angle (horizontal)
local function calculateYaw(origin, target)
    local direction = (target - origin).Unit
    return math.deg(math.atan2(direction.X, direction.Z))
end

-- Calculate pitch angle (vertical)
local function calculatePitch(origin, target)
    local direction = (target - origin).Unit
    local horizontalDist = math.sqrt(direction.X^2 + direction.Z^2)
    return math.deg(math.atan2(direction.Y, horizontalDist))
end

-- Both angles
local function calculateAimAngles(origin, target)
    local direction = (target - origin).Unit
    local yaw = math.deg(math.atan2(direction.X, direction.Z))
    local horizontalDist = math.sqrt(direction.X^2 + direction.Z^2)
    local pitch = math.deg(math.atan2(direction.Y, horizontalDist))
    return yaw, pitch
end
```

### Angular Velocity from Speed

```lua
local function speedToAngularVelocity(linearSpeed, wheelRadius)
    return linearSpeed / wheelRadius
end

local function angularVelocityToSpeed(angularVelocity, wheelRadius)
    return angularVelocity * wheelRadius
end
```

### Spring Calculations

```lua
-- Critical damping (no oscillation)
local function criticalDamping(stiffness, mass)
    return 2 * math.sqrt(stiffness * mass)
end

-- Spring stiffness for target force
local function stiffnessForForce(targetForce, expectedDisplacement)
    return targetForce / expectedDisplacement
end

-- Full suspension config
local function calculateSuspensionProperties(vehicleMass, numWheels, rideHeight, travel)
    local forcePerWheel = vehicleMass * workspace.Gravity / numWheels
    local stiffness = forcePerWheel / travel
    local damping = criticalDamping(stiffness, vehicleMass / numWheels)

    return {
        FreeLength = rideHeight,
        Stiffness = stiffness,
        Damping = damping,
        MaxForce = forcePerWheel * 3,
        MinLength = rideHeight - travel,
        MaxLength = rideHeight + travel
    }
end
```

---

## Common Constraint Configurations

### Door Configurations

```lua
local DOOR_CONFIGS = {
    SwingingDoor = {
        ActuatorType = Enum.ActuatorType.Servo,
        ServoMaxTorque = 10000,
        AngularSpeed = 2,
        LimitsEnabled = true,
        LowerAngle = 0,
        UpperAngle = 90
    },
    HeavyDoor = {
        ActuatorType = Enum.ActuatorType.Servo,
        ServoMaxTorque = 50000,
        AngularSpeed = 1,
        LimitsEnabled = true,
        LowerAngle = 0,
        UpperAngle = 90
    },
    SlidingDoor = {
        ActuatorType = Enum.ActuatorType.Servo,
        ServoMaxForce = 10000,
        Speed = 3,
        LimitsEnabled = true,
        LowerLimit = 0,
        UpperLimit = 5
    }
}
```

### Vehicle Wheel Configurations

```lua
local WHEEL_CONFIGS = {
    LightCar = {
        MotorMaxTorque = 500,
        MotorMaxAngularAcceleration = 50,
        MaxSteerAngle = 35
    },
    HeavyTruck = {
        MotorMaxTorque = 2000,
        MotorMaxAngularAcceleration = 30,
        MaxSteerAngle = 25
    },
    SportsCar = {
        MotorMaxTorque = 1000,
        MotorMaxAngularAcceleration = 100,
        MaxSteerAngle = 40
    }
}
```

### Ragdoll Joint Limits

```lua
local JOINT_LIMITS = {
    Neck = { UpperAngle = 30, TwistLower = -45, TwistUpper = 45 },
    Shoulder = { UpperAngle = 90, TwistLower = -90, TwistUpper = 90 },
    Elbow = { UpperAngle = 120, TwistLower = 0, TwistUpper = 0 },
    Wrist = { UpperAngle = 45, TwistLower = -30, TwistUpper = 30 },
    Hip = { UpperAngle = 60, TwistLower = -30, TwistUpper = 30 },
    Knee = { UpperAngle = 120, TwistLower = 0, TwistUpper = 0 },
    Ankle = { UpperAngle = 30, TwistLower = -15, TwistUpper = 15 }
}
```

---

## Event Handling

### Constraint Property Changes

```lua
-- Monitor hinge angle
hinge:GetPropertyChangedSignal("CurrentAngle"):Connect(function()
    local angle = hinge.CurrentAngle
    if angle >= 89 then
        print("Door fully open")
    elseif angle <= 1 then
        print("Door closed")
    end
end)

-- Monitor prismatic position
prismatic:GetPropertyChangedSignal("CurrentPosition"):Connect(function()
    local pos = prismatic.CurrentPosition
    if pos >= prismatic.UpperLimit - 0.1 then
        print("Reached top")
    elseif pos <= prismatic.LowerLimit + 0.1 then
        print("Reached bottom")
    end
end)

-- Monitor spring compression
RunService.Heartbeat:Connect(function()
    local compression = spring.FreeLength - spring.CurrentLength
    if compression > 0.5 then
        print("Spring compressed")
    end
end)
```

### Smooth Transitions

```lua
local TweenService = game:GetService("TweenService")

-- Smooth hinge movement
local function smoothHingeMove(hinge, targetAngle, duration)
    local tween = TweenService:Create(
        hinge,
        TweenInfo.new(duration, Enum.EasingStyle.Quad, Enum.EasingDirection.Out),
        { TargetAngle = targetAngle }
    )
    tween:Play()
    return tween
end

-- Smooth prismatic movement
local function smoothSlide(prismatic, targetPosition, duration)
    local tween = TweenService:Create(
        prismatic,
        TweenInfo.new(duration, Enum.EasingStyle.Quad, Enum.EasingDirection.InOut),
        { TargetPosition = targetPosition }
    )
    tween:Play()
    return tween
end
```

---

## Debugging

### Visualize Attachments

```lua
local function visualizeAttachment(attachment, color)
    local part = Instance.new("Part")
    part.Name = "AttachmentVisual"
    part.Size = Vector3.new(0.2, 0.2, 0.2)
    part.Shape = Enum.PartType.Ball
    part.Color = color or Color3.new(1, 0, 0)
    part.CanCollide = false
    part.Anchored = false
    part.Transparency = 0.5

    local weld = Instance.new("WeldConstraint")
    weld.Part0 = part
    weld.Part1 = attachment.Parent
    weld.Parent = part

    part.CFrame = attachment.WorldCFrame
    part.Parent = workspace
    return part
end
```

### Print Constraint State

```lua
local function printConstraintState(constraint)
    print("=== Constraint: " .. constraint.Name .. " ===")
    print("Type: " .. constraint.ClassName)
    print("Enabled: " .. tostring(constraint.Enabled))
    print("Active: " .. tostring(constraint.Active))

    if constraint:IsA("HingeConstraint") then
        print("CurrentAngle: " .. constraint.CurrentAngle)
        print("ActuatorType: " .. tostring(constraint.ActuatorType))
    elseif constraint:IsA("PrismaticConstraint") then
        print("CurrentPosition: " .. constraint.CurrentPosition)
    elseif constraint:IsA("SpringConstraint") then
        print("CurrentLength: " .. constraint.CurrentLength)
        print("FreeLength: " .. constraint.FreeLength)
    elseif constraint:IsA("RopeConstraint") then
        print("CurrentDistance: " .. constraint.CurrentDistance)
        print("Length: " .. constraint.Length)
    end
end
```
