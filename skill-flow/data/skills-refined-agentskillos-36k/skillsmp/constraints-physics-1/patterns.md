# Constraint Implementation Patterns

Ready-to-use patterns for common game mechanics.

---

## Vehicle Chassis Pattern

### Structure

```
VehicleModel
├── Body (PrimaryPart, contains VehicleSeat)
│   ├── Attachment_FL, Attachment_FR (front)
│   └── Attachment_BL, Attachment_BR (rear)
├── Wheel_FL
│   ├── Attachment
│   ├── SpringConstraint → Body.Attachment_FL
│   └── CylindricalConstraint → Body.Attachment_FL
├── Wheel_FR (mirror of FL)
├── Wheel_BL (rear drive only)
│   ├── Attachment
│   └── CylindricalConstraint → Body.Attachment_BL
└── Wheel_BR (mirror of BL)
```

### Setup Script

```lua
local function setupVehicle(vehicle)
    local body = vehicle.Body
    local seat = body.VehicleSeat

    -- Calculate mass for spring tuning
    local totalMass = 0
    for _, part in pairs(vehicle:GetDescendants()) do
        if part:IsA("BasePart") then
            totalMass = totalMass + part:GetMass()
        end
    end

    local gravity = workspace.Gravity
    local numWheels = 4
    local suspensionForce = totalMass * gravity / numWheels

    for _, wheel in pairs(vehicle:GetChildren()) do
        if wheel.Name:match("^Wheel_") then
            local spring = wheel:FindFirstChildOfClass("SpringConstraint")
            local cylindrical = wheel:FindFirstChildOfClass("CylindricalConstraint")

            if spring then
                spring.Stiffness = suspensionForce / 0.5 -- 0.5 stud travel
                spring.Damping = 2 * math.sqrt(spring.Stiffness * wheel:GetMass())
                spring.MaxForce = suspensionForce * 3
            end

            if cylindrical then
                cylindrical.AngularActuatorType = Enum.ActuatorType.Motor
                cylindrical.MotorMaxTorque = 500
            end
        end
    end
end
```

### Drive Script

```lua
local function driveVehicle(vehicle, throttle, steer)
    local wheels = {}
    for _, child in pairs(vehicle:GetChildren()) do
        if child.Name:match("^Wheel_") then
            wheels[child.Name] = child:FindFirstChildOfClass("CylindricalConstraint")
        end
    end

    local maxSpeed = 50
    local wheelRadius = vehicle.Wheel_FL.Size.Y / 2
    local angularVelocity = (throttle * maxSpeed) / wheelRadius
    local maxSteerAngle = 35

    -- Drive wheels
    for name, constraint in pairs(wheels) do
        if constraint then
            constraint.AngularVelocity = angularVelocity
        end
    end

    -- Steering (front wheels only)
    if wheels.Wheel_FL then
        wheels.Wheel_FL.AngularActuatorType = Enum.ActuatorType.Servo
        wheels.Wheel_FL.TargetAngle = steer * maxSteerAngle
    end
    if wheels.Wheel_FR then
        wheels.Wheel_FR.AngularActuatorType = Enum.ActuatorType.Servo
        wheels.Wheel_FR.TargetAngle = steer * maxSteerAngle
    end
end
```

---

## Ragdoll Pattern

### Structure

```
Character
├── HumanoidRootPart
├── LowerTorso
│   ├── Root (Motor6D → HumanoidRootPart) [KEEP ENABLED]
│   └── BallSocketConstraint → each limb
├── UpperTorso
│   └── BallSocketConstraint → LowerTorso
├── Head
│   └── BallSocketConstraint → UpperTorso
├── LeftUpperArm → LeftLowerArm → LeftHand
└── RightUpperArm → RightLowerArm → RightHand
```

### Ragdoll Module

```lua
local RagdollModule = {}

-- Attachment offsets for R15
local ATTACHMENT_CFRAMES = {
    ["LeftHip"] = {CFrame.new(-0.5, -1, 0), CFrame.new(0, 0.5, 0)},
    ["RightHip"] = {CFrame.new(0.5, -1, 0), CFrame.new(0, 0.5, 0)},
    ["Waist"] = {CFrame.new(0, 0.5, 0), CFrame.new(0, -0.5, 0)},
    ["Neck"] = {CFrame.new(0, 1, 0), CFrame.new(0, -0.5, 0)},
    ["LeftShoulder"] = {CFrame.new(-1, 0.5, 0), CFrame.new(0.5, 0.5, 0)},
    ["RightShoulder"] = {CFrame.new(1, 0.5, 0), CFrame.new(-0.5, 0.5, 0)},
    ["LeftElbow"] = {CFrame.new(0, -0.5, 0), CFrame.new(0, 0.5, 0)},
    ["RightElbow"] = {CFrame.new(0, -0.5, 0), CFrame.new(0, 0.5, 0)},
    ["LeftWrist"] = {CFrame.new(0, -0.5, 0), CFrame.new(0, 0.3, 0)},
    ["RightWrist"] = {CFrame.new(0, -0.5, 0), CFrame.new(0, 0.3, 0)},
    ["LeftKnee"] = {CFrame.new(0, -0.5, 0), CFrame.new(0, 0.5, 0)},
    ["RightKnee"] = {CFrame.new(0, -0.5, 0), CFrame.new(0, 0.5, 0)},
    ["LeftAnkle"] = {CFrame.new(0, -0.5, 0), CFrame.new(0, 0.5, 0)},
    ["RightAnkle"] = {CFrame.new(0, -0.5, 0), CFrame.new(0, 0.5, 0)},
}

function RagdollModule.createColliderPart(part)
    local collider = Instance.new("Part")
    collider.Name = "RagdollCollider"
    collider.Size = part.Size * 0.8
    collider.Transparency = 1
    collider.CanCollide = true
    collider.Massless = true

    local weld = Instance.new("WeldConstraint")
    weld.Part0 = collider
    weld.Part1 = part
    weld.Parent = collider

    collider.Parent = part
    return collider
end

function RagdollModule.enableRagdoll(character)
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    if not humanoid then return end

    humanoid.RequiresNeck = false
    humanoid.PlatformStand = true
    humanoid.AutoRotate = false

    for _, motor in pairs(character:GetDescendants()) do
        if motor:IsA("Motor6D") and motor.Name ~= "Root" then
            -- Create attachments
            local a0 = Instance.new("Attachment")
            local a1 = Instance.new("Attachment")

            local offsets = ATTACHMENT_CFRAMES[motor.Name]
            if offsets then
                a0.CFrame = offsets[1]
                a1.CFrame = offsets[2]
            else
                a0.CFrame = motor.C0
                a1.CFrame = motor.C1
            end

            a0.Name = "RagdollAttachment0"
            a1.Name = "RagdollAttachment1"
            a0.Parent = motor.Part0
            a1.Parent = motor.Part1

            -- Create ball socket
            local socket = Instance.new("BallSocketConstraint")
            socket.Name = "RagdollSocket"
            socket.Attachment0 = a0
            socket.Attachment1 = a1
            socket.LimitsEnabled = true
            socket.TwistLimitsEnabled = true
            socket.UpperAngle = 45
            socket.TwistLowerAngle = -45
            socket.TwistUpperAngle = 45
            socket.MaxFrictionTorque = 50
            socket.Parent = motor.Part0

            -- Create collider
            RagdollModule.createColliderPart(motor.Part1)

            -- Disable motor
            motor.Enabled = false
        end
    end

    humanoid:ChangeState(Enum.HumanoidStateType.Physics)
end

function RagdollModule.disableRagdoll(character)
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    if not humanoid then return end

    for _, obj in pairs(character:GetDescendants()) do
        if obj.Name == "RagdollSocket" or
           obj.Name == "RagdollAttachment0" or
           obj.Name == "RagdollAttachment1" or
           obj.Name == "RagdollCollider" then
            obj:Destroy()
        end

        if obj:IsA("Motor6D") then
            obj.Enabled = true
        end
    end

    humanoid.PlatformStand = false
    humanoid.AutoRotate = true
    humanoid:ChangeState(Enum.HumanoidStateType.GettingUp)
end

return RagdollModule
```

---

## Turret Pattern

### Structure

```
TurretAssembly
├── Base (anchored or welded to vehicle)
│   └── YawAttachment (points up, Y-axis)
├── TurretBody
│   ├── YawAttachment (matches Base)
│   ├── HingeConstraint (yaw, Servo)
│   └── PitchAttachment (points sideways)
└── Barrel
    ├── PitchAttachment (matches Body)
    └── HingeConstraint (pitch, Servo)
```

### Turret Controller

```lua
local TurretController = {}
TurretController.__index = TurretController

function TurretController.new(turretModel)
    local self = setmetatable({}, TurretController)

    self.model = turretModel
    self.base = turretModel.Base
    self.body = turretModel.TurretBody
    self.barrel = turretModel.Barrel

    self.yawHinge = self.body:FindFirstChildOfClass("HingeConstraint")
    self.pitchHinge = self.barrel:FindFirstChildOfClass("HingeConstraint")

    -- Configure hinges
    self.yawHinge.ActuatorType = Enum.ActuatorType.Servo
    self.yawHinge.ServoMaxTorque = 100000
    self.yawHinge.AngularSpeed = 3

    self.pitchHinge.ActuatorType = Enum.ActuatorType.Servo
    self.pitchHinge.ServoMaxTorque = 50000
    self.pitchHinge.AngularSpeed = 2
    self.pitchHinge.LimitsEnabled = true
    self.pitchHinge.LowerAngle = -10
    self.pitchHinge.UpperAngle = 60

    return self
end

function TurretController:aimAt(targetPosition)
    local turretPos = self.body.Position
    local direction = (targetPosition - turretPos).Unit

    -- Yaw (horizontal rotation)
    local yaw = math.deg(math.atan2(direction.X, direction.Z))

    -- Adjust for base orientation
    local baseYaw = math.deg(math.atan2(
        self.base.CFrame.LookVector.X,
        self.base.CFrame.LookVector.Z
    ))
    local relativeYaw = yaw - baseYaw

    -- Normalize to -180 to 180
    while relativeYaw > 180 do relativeYaw = relativeYaw - 360 end
    while relativeYaw < -180 do relativeYaw = relativeYaw + 360 end

    self.yawHinge.TargetAngle = relativeYaw

    -- Pitch (vertical rotation)
    local horizontalDist = math.sqrt(direction.X^2 + direction.Z^2)
    local pitch = math.deg(math.atan2(direction.Y, horizontalDist))

    self.pitchHinge.TargetAngle = math.clamp(pitch, -10, 60)
end

function TurretController:getCurrentAngles()
    return {
        yaw = self.yawHinge.CurrentAngle,
        pitch = self.pitchHinge.CurrentAngle
    }
end

return TurretController
```

---

## Grappling Hook Pattern

### Structure

```
GrapplingSystem
├── Tool
│   ├── Handle
│   └── MuzzleAttachment
└── Runtime (created when grappling)
    ├── HookPart
    │   └── HookAttachment
    └── RopeConstraint (MuzzleAttachment → HookAttachment)
```

### Grapple Controller

```lua
local GrappleController = {}
GrappleController.__index = GrappleController

function GrappleController.new(player, tool)
    local self = setmetatable({}, GrappleController)

    self.player = player
    self.tool = tool
    self.maxRange = 100
    self.pullSpeed = 30
    self.pullForce = 10000

    self.rope = nil
    self.hookAttachment = nil
    self.isGrappling = false

    return self
end

function GrappleController:fire(targetPosition)
    if self.isGrappling then return end

    local character = self.player.Character
    if not character then return end

    local rootPart = character:FindFirstChild("HumanoidRootPart")
    if not rootPart then return end

    -- Check range
    local distance = (targetPosition - rootPart.Position).Magnitude
    if distance > self.maxRange then return end

    -- Create hook attachment at target
    self.hookAttachment = Instance.new("Attachment")
    self.hookAttachment.WorldPosition = targetPosition
    self.hookAttachment.Parent = workspace.Terrain

    -- Get or create player attachment
    local playerAttachment = rootPart:FindFirstChild("GrappleAttachment")
    if not playerAttachment then
        playerAttachment = Instance.new("Attachment")
        playerAttachment.Name = "GrappleAttachment"
        playerAttachment.Parent = rootPart
    end

    -- Create rope
    self.rope = Instance.new("RopeConstraint")
    self.rope.Attachment0 = playerAttachment
    self.rope.Attachment1 = self.hookAttachment
    self.rope.Length = distance
    self.rope.Visible = true
    self.rope.Thickness = 0.1
    self.rope.Color = BrickColor.new("Really black")
    self.rope.WinchEnabled = true
    self.rope.WinchSpeed = self.pullSpeed
    self.rope.WinchForce = self.pullForce
    self.rope.WinchTarget = 5 -- Pull close
    self.rope.Parent = character

    self.isGrappling = true
end

function GrappleController:release()
    if not self.isGrappling then return end

    if self.rope then
        self.rope:Destroy()
        self.rope = nil
    end

    if self.hookAttachment then
        self.hookAttachment:Destroy()
        self.hookAttachment = nil
    end

    self.isGrappling = false
end

function GrappleController:adjustLength(delta)
    if self.rope and self.isGrappling then
        self.rope.WinchTarget = math.max(5, self.rope.WinchTarget + delta)
    end
end

return GrappleController
```

---

## Door Pattern

### Swinging Door

```lua
local function createSwingingDoor(doorPart, hingePosition, maxAngle)
    -- Create frame attachment (anchored reference)
    local frameAttachment = Instance.new("Attachment")
    frameAttachment.WorldPosition = hingePosition
    frameAttachment.Parent = workspace.Terrain

    -- Create door attachment
    local doorAttachment = Instance.new("Attachment")
    doorAttachment.Position = doorPart.CFrame:PointToObjectSpace(hingePosition)
    doorAttachment.Parent = doorPart

    -- Create hinge
    local hinge = Instance.new("HingeConstraint")
    hinge.Attachment0 = frameAttachment
    hinge.Attachment1 = doorAttachment
    hinge.ActuatorType = Enum.ActuatorType.Servo
    hinge.ServoMaxTorque = 10000
    hinge.AngularSpeed = 2
    hinge.LimitsEnabled = true
    hinge.LowerAngle = 0
    hinge.UpperAngle = maxAngle
    hinge.TargetAngle = 0
    hinge.Parent = doorPart

    return hinge
end

-- Usage
local doorHinge = createSwingingDoor(door, Vector3.new(0, 5, 0), 90)
doorHinge.TargetAngle = 90 -- Open
doorHinge.TargetAngle = 0  -- Close
```

### Sliding Door

```lua
local function createSlidingDoor(doorPart, slideDirection, slideDistance)
    -- Create frame attachment (anchored)
    local frameAttachment = Instance.new("Attachment")
    frameAttachment.WorldPosition = doorPart.Position
    frameAttachment.WorldAxis = slideDirection
    frameAttachment.Parent = workspace.Terrain

    -- Create door attachment
    local doorAttachment = Instance.new("Attachment")
    doorAttachment.Parent = doorPart

    -- Create prismatic
    local prismatic = Instance.new("PrismaticConstraint")
    prismatic.Attachment0 = frameAttachment
    prismatic.Attachment1 = doorAttachment
    prismatic.ActuatorType = Enum.ActuatorType.Servo
    prismatic.ServoMaxForce = 10000
    prismatic.Speed = 3
    prismatic.LimitsEnabled = true
    prismatic.LowerLimit = 0
    prismatic.UpperLimit = slideDistance
    prismatic.TargetPosition = 0
    prismatic.Parent = doorPart

    return prismatic
end

-- Usage
local slidingDoor = createSlidingDoor(door, Vector3.new(1, 0, 0), 5)
slidingDoor.TargetPosition = 5 -- Open
slidingDoor.TargetPosition = 0 -- Close
```

---

## Train/Cart System Pattern

### Structure

```
TrainSystem
├── Track
│   ├── Rails (anchored parts)
│   └── PathAttachments (along track)
├── Locomotive
│   ├── Body
│   ├── PrismaticConstraint → Track
│   └── RearCoupler.Attachment
└── Carriage
    ├── Body
    ├── FrontCoupler.Attachment
    ├── RearCoupler.Attachment
    └── RopeConstraint (FrontCoupler → Locomotive.RearCoupler)
```

### Train Controller

```lua
local function setupTrain(locomotive, carriages, trackAttachment)
    -- Locomotive movement
    local locoPrismatic = Instance.new("PrismaticConstraint")
    locoPrismatic.Attachment0 = trackAttachment
    locoPrismatic.Attachment1 = locomotive.TrackAttachment
    locoPrismatic.ActuatorType = Enum.ActuatorType.Motor
    locoPrismatic.Parent = locomotive

    -- Connect carriages
    local previousCar = locomotive
    for i, carriage in ipairs(carriages) do
        -- Rope for distance
        local rope = Instance.new("RopeConstraint")
        rope.Attachment0 = previousCar.RearCoupler
        rope.Attachment1 = carriage.FrontCoupler
        rope.Length = 2
        rope.Restitution = 0.1
        rope.Parent = carriage

        -- Ball socket for rotation freedom
        local socket = Instance.new("BallSocketConstraint")
        socket.Attachment0 = previousCar.RearCoupler
        socket.Attachment1 = carriage.FrontCoupler
        socket.LimitsEnabled = true
        socket.UpperAngle = 15
        socket.Parent = carriage

        previousCar = carriage
    end

    return locoPrismatic
end

-- Control
local trainPrismatic = setupTrain(loco, cars, track.StartAttachment)
trainPrismatic.Velocity = 20 -- Move forward
trainPrismatic.Velocity = 0  -- Stop
trainPrismatic.Velocity = -10 -- Reverse
```
