---
name: ui-system
description: Use this skill when implementing user interfaces, including responsive layouts, animations, and interactive elements for games.
---

# Skill body

When implementing user interfaces, follow these patterns for responsive and polished UI.

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

### Tweening UI Elements
```lua
local TweenService = game:GetService("TweenService")

local function animateIn(frame)
    frame.Position = UDim2.new(0.5, 0, 1.5, 0)  -- Start below screen
    frame.Visible = true

    local tween = TweenService:Create(
        frame,
        TweenInfo.new(0.5, Enum.EasingStyle.Back, Enum.EasingDirection.Out),
        {Position = UDim2.new(0.5, 0, 0.5, 0)}  -- Animate to center
    )
    tween:Play()
end
```

## Layout Basics

### Container-Based Layout
```gdscript
# VBoxContainer - Vertical stack
# HBoxContainer - Horizontal stack
# GridContainer - Grid layout
# MarginContainer - Add margins
# CenterContainer - Center content

extends Control

func setup_menu() -> void:
    var vbox := VBoxContainer.new()
    vbox.add_theme_constant_override("separation", 10)

    for option in ["Start", "Options", "Quit"]:
        var button := Button.new()
        button.text = option
        button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        vbox.add_child(button)

    add_child(vbox)
```

### Anchors and Margins
```gdscript
extends Control

func setup_anchors() -> void:
    # Full screen
    anchor_left = 0
    anchor_top = 0
    anchor_right = 1
    anchor_bottom = 1

    # Top-right corner
    anchor_left = 1
    anchor_top = 0
    anchor_right = 1
    anchor_bottom = 0
    offset_left = -100
    offset_right = 0
    offset_top = 0
    offset_bottom = 50

    # Center
    anchor_left = 0.5
    anchor_top = 0.5
    anchor_right = 0.5
    anchor_bottom = 0.5
    offset_left = -50
    offset_right = 50
    offset_top = -25
    offset_bottom = 25

func set_full_rect() -> void:
    set_anchors_preset(Control.PRESET_FULL_RECT)

func set_center() -> void:
    set_anchors_preset(Control.PRESET_CENTER)
```

### Responsive Layout
```gdscript
@export var mobile_threshold := 600

func _ready() -> void:
    get_viewport().size_changed.connect(_on_viewport_resized)
    _on_viewport_resized()

func _on_viewport_resized() -> void:
    var viewport_size := get_viewport().get_visible_rect().size

    if viewport_size.x < mobile_threshold:
        apply_mobile_layout()
    else:
        apply_desktop_layout()

func apply_mobile_layout() -> void:
    # Stack vertically, larger touch targets
    $MainContainer.columns = 1
    for button in $MainContainer.get_children():
        button.custom_minimum_size.y = 60

func apply_desktop_layout() -> void:
    # Grid layout, normal sizes
    $MainContainer.columns = 3
    for button in $MainContainer.get_children():
        button.custom_minimum_size.y = 30
```