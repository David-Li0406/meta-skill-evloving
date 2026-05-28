---
name: ui-ux-system
description: Use this skill when implementing UI/UX systems for games, including responsive design, animations, input handling, and menu systems.
---

# UI/UX Systems

When implementing UI systems, follow these patterns for responsive and polished interfaces.

## Responsive Design

### Aspect Ratio and Size Constraints
```lua
-- Maintain aspect ratio regardless of screen size
local frame = Instance.new("Frame")
frame.Size = UDim2.new(0.5, 0, 0.5, 0)  -- Will be adjusted

local aspectRatio = Instance.new("UIAspectRatioConstraint")
aspectRatio.AspectRatio = 16/9
aspectRatio.AspectType = Enum.AspectType.FitWithinMaxSize
aspectRatio.DominantAxis = Enum.DominantAxis.Width
aspectRatio.Parent = frame

-- Limit min/max size
local sizeConstraint = Instance.new("UISizeConstraint")
sizeConstraint.MinSize = Vector2.new(100, 50)
sizeConstraint.MaxSize = Vector2.new(500, 300)
sizeConstraint.Parent = frame
```

### Screen Size Detection
```lua
local camera = workspace.CurrentCamera

local function getScreenCategory()
    local viewportSize = camera.ViewportSize

    if viewportSize.X < 600 then
        return "mobile"
    elseif viewportSize.X < 1200 then
        return "tablet"
    else
        return "desktop"
    end
end

local function updateLayout()
    local category = getScreenCategory()

    if category == "mobile" then
        mainFrame.Size = UDim2.new(0.95, 0, 0.9, 0)
        fontSize = 14
    elseif category == "tablet" then
        mainFrame.Size = UDim2.new(0.8, 0, 0.8, 0)
        fontSize = 16
    else
        mainFrame.Size = UDim2.new(0.6, 0, 0.7, 0)
        fontSize = 18
    end
end

camera:GetPropertyChangedSignal("ViewportSize"):Connect(updateLayout)
```

### Safe Area Handling
```lua
local GuiService = game:GetService("GuiService")

local function getSafeInsets()
    local insets = GuiService:GetGuiInset()
    return insets
end

-- Apply safe area padding
local topInset = getSafeInsets()
mainFrame.Position = UDim2.new(0.5, 0, 0, topInset.Y + 10)
```

## UI Animation

### TweenService for UI
```lua
local TweenService = game:GetService("TweenService")

local function animateIn(frame)
    frame.Position = UDim2.new(0.5, 0, 1.5, 0)  -- Start below screen
    frame.Visible = true

    local tween = TweenService:Create(
        frame,
        TweenInfo.new(0.5, Enum.EasingStyle.Back, Enum.EasingDirection.Out),
        {Position = UDim2.new(0.5, 0, 0.5, 0)}
    )
    tween:Play()
    return tween
end

local function animateOut(frame)
    local tween = TweenService:Create(
        frame,
        TweenInfo.new(0.3, Enum.EasingStyle.Back, Enum.EasingDirection.In),
        {Position = UDim2.new(0.5, 0, 1.5, 0)}
    )
    tween:Play()
    tween.Completed:Connect(function()
        frame.Visible = false
    end)
    return tween
end
```

### Button Interactions
```lua
local function setupButton(button)
    local originalSize = button.Size
    local originalColor = button.BackgroundColor3

    -- Hover
    button.MouseEnter:Connect(function()
        TweenService:Create(button, TweenInfo.new(0.1), {
            Size = originalSize + UDim2.new(0.02, 0, 0.02, 0),
            BackgroundColor3 = originalColor:Lerp(Color3.new(1, 1, 1), 0.1)
        }):Play()
    end)

    button.MouseLeave:Connect(function()
        TweenService:Create(button, TweenInfo.new(0.1), {
            Size = originalSize,
            BackgroundColor3 = originalColor
        }):Play()
    end)

    -- Click
    button.MouseButton1Down:Connect(function()
        TweenService:Create(button, TweenInfo.new(0.05), {
            Size = originalSize - UDim2.new(0.01, 0, 0.01, 0)
        }):Play()
    end)

    button.MouseButton1Up:Connect(function()
        TweenService:Create(button, TweenInfo.new(0.1), {
            Size = originalSize
        }):Play()
    end)
end
```

## Input Handling

### Drag and Drop
```lua
local function makeDraggable(frame)
    local dragging = false
    local dragStart
    local startPos

    frame.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 or
           input.UserInputType == Enum.UserInputType.Touch then
            dragging = true
            dragStart = input.Position
            startPos = frame.Position

            input.Changed:Connect(function()
                if input.UserInputState == Enum.UserInputState.End then
                    dragging = false
                end
            end)
        end
    end)

    frame.InputChanged:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseMovement or
           input.UserInputType == Enum.UserInputType.Touch then
            if dragging then
                local delta = input.Position - dragStart
                frame.Position = UDim2.new(
                    startPos.X.Scale,
                    startPos.X.Offset + delta.X,
                    startPos.Y.Scale,
                    startPos.Y.Offset + delta.Y
                )
            end
        end
    end)
end
```

## HUD Systems

### Health Bar
```lua
local function createHealthBar(parent)
    local container = Instance.new("Frame")
    container.Size = UDim2.new(0.3, 0, 0, 30)
    container.Position = UDim2.new(0.02, 0, 0.05, 0)
    container.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
    container.Parent = parent

    local fill = Instance.new("Frame")
    fill.Size = UDim2.new(1, 0, 1, 0)
    fill.BackgroundColor3 = Color3.fromRGB(0, 200, 0)
    fill.Parent = container

    local function updateHealth(current, max)
        local ratio = current / max
        fill.Size = UDim2.new(ratio, 0, 1, 0)
    end

    return {container = container, update = updateHealth}
end
```

## Menu Systems

### Page Navigation
```lua
local MenuController = {}
MenuController.pageStack = {}

function MenuController.pushPage(pageName)
    local currentPage = MenuController.pageStack[#MenuController.pageStack]
    if currentPage then
        currentPage.Visible = false
    end

    local newPage = Pages[pageName]
    newPage.Visible = true
    table.insert(MenuController.pageStack, newPage)
end

function MenuController.popPage()
    if #MenuController.pageStack <= 1 then return end

    local currentPage = table.remove(MenuController.pageStack)
    currentPage.Visible = false

    local previousPage = MenuController.pageStack[#MenuController.pageStack]
    previousPage.Visible = true
end
```

### Modal Dialog
```lua
local function showModal(title, message, buttons)
    local backdrop = Instance.new("Frame")
    backdrop.Size = UDim2.new(1, 0, 1, 0)
    backdrop.BackgroundColor3 = Color3.new(0, 0, 0)
    backdrop.BackgroundTransparency = 0.5
    backdrop.ZIndex = 100
    backdrop.Parent = ScreenGui

    local modal = Instance.new("Frame")
    modal.Size = UDim2.new(0.4, 0, 0.3, 0)
    modal.Position = UDim2.new(0.5, 0, 0.5, 0)
    modal.AnchorPoint = Vector2.new(0.5, 0.5)
    modal.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
    modal.ZIndex = 101
    modal.Parent = backdrop

    local titleLabel = Instance.new("TextLabel")
    titleLabel.Text = title
    titleLabel.Size = UDim2.new(1, 0, 0.2, 0)
    titleLabel.BackgroundTransparency = 1
    titleLabel.TextColor3 = Color3.new(1, 1, 1)
    titleLabel.TextScaled = true
    titleLabel.Parent = modal

    local messageLabel = Instance.new("TextLabel")
    messageLabel.Text = message
    messageLabel.Size = UDim2.new(0.9, 0, 0.4, 0)
    messageLabel.Position = UDim2.new(0.05, 0, 0.25, 0)
    messageLabel.BackgroundTransparency = 1
    messageLabel.TextColor3 = Color3.new(0.8, 0.8, 0.8)
    messageLabel.TextWrapped = true
    messageLabel.Parent = modal

    local buttonContainer = Instance.new("Frame")
    buttonContainer.Size = UDim2.new(0.9, 0, 0.25, 0)
    buttonContainer.Position = UDim2.new(0.05, 0, 0.7, 0)
    buttonContainer.BackgroundTransparency = 1
    buttonContainer.Parent = modal

    for _, buttonData in ipairs(buttons) do
        local btn = Instance.new("TextButton")
        btn.Size = UDim2.new(0, 100, 1, 0)
        btn.Text = buttonData.text
        btn.BackgroundColor3 = buttonData.color or Color3.fromRGB(60, 60, 60)
        btn.TextColor3 = Color3.new(1, 1, 1)
        btn.Parent = buttonContainer

        btn.MouseButton1Click:Connect(function()
            backdrop:Destroy()
        end)
    end
end
```