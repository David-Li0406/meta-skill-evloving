# Gui Classes

## Contents
- [ScreenGui](#screengui)
- [Frame](#frame)
- [TextLabel](#textlabel)
- [TextButton](#textbutton)
- [TextBox](#textbox)
- [ImageLabel](#imagelabel)
- [ImageButton](#imagebutton)
- [ScrollingFrame](#scrollingframe)
- [ViewportFrame](#viewportframe)
- [UIListLayout](#uilistlayout)
- [UIGridLayout](#uigridlayout)
- [UIPadding](#uipadding)
- [UICorner](#uicorner)
- [UIStroke](#uistroke)
- [UIGradient](#uigradient)
- [UIScale](#uiscale)
- [UIAspectRatioConstraint](#uiaspectratioconstraint)
- [BillboardGui](#billboardgui)
- [SurfaceGui](#surfacegui)
- [CanvasGroup](#canvasgroup)

---

## ScreenGui

Primary container of on-screen 2D user interface elements.

**Properties:**
- `ScreenGui.ClipToDeviceSafeArea`: boolean - Whether to clip the contents of this `Class.ScreenGui` to the device's
- `ScreenGui.DisplayOrder`: int - Controls the Z-index order in which multiple `Class.ScreenGui` containers
- `ScreenGui.IgnoreGuiInset`: boolean - Determines whether the `Class.ScreenGui` overflows into the range of
- `ScreenGui.SafeAreaCompatibility`: SafeAreaCompatibility - Specifies whether automatic UI compatibility transformations are applied
- `ScreenGui.ScreenInsets`: ScreenInsets - Controls the safe area insets that are applied to the contents of the

---

## Frame

A `Class.GuiObject` that renders as a plain rectangle, generally used as a
container.

**Properties:**
- `Frame.Style`: FrameStyle - Sets what the frame looks like from a selection of pre-determined styles.

---

## TextLabel

A 2D user interface element that displays non-interactive text.

**Properties:**
- `TextLabel.ContentText`: string - A copy of `Class.TextLabel.Text` that contains exactly what is being
- `TextLabel.Font`: Enum.Font - Determines the font used to render text.
- `TextLabel.FontFace`: Datatype.Font - Determines the font used to render text.
- `TextLabel.FontSize`: FontSize - Determines the font size to be used.
- `TextLabel.LineHeight`: float - Scales the spacing between lines of text in the `Class.TextLabel`.
- `TextLabel.LocalizedText`: string - Sets whether a `Class.TextLabel` should be `Class.GuiBase2d.Localize` or
- `TextLabel.MaxVisibleGraphemes`: int - The maximum number of graphemes the `Class.TextLabel` can show.
- `TextLabel.OpenTypeFeatures`: string
- `TextLabel.OpenTypeFeaturesError`: string
- `TextLabel.RichText`: boolean - Determines whether the `Class.TextLabel` renders its text using rich text
- ...and 16 more

---

## TextButton

A 2D user interface element that displays interactive text.

**Properties:**
- `TextButton.ContentText`: string - A copy of `Class.TextButton.Text` that contains exactly what is being
- `TextButton.Font`: Enum.Font - Determines the font used to render text.
- `TextButton.FontFace`: Datatype.Font - Determines the font used to render text.
- `TextButton.FontSize`: FontSize - Determines the font size to be used.
- `TextButton.LineHeight`: float - Scales the spacing between lines of text in the `Class.TextButton`.
- `TextButton.LocalizedText`: string - Sets whether a `Class.TextButton` should be `Class.GuiBase2d.Localize` or
- `TextButton.MaxVisibleGraphemes`: int - The maximum number of graphemes the `Class.TextButton` can show.
- `TextButton.OpenTypeFeatures`: string
- `TextButton.OpenTypeFeaturesError`: string
- `TextButton.RichText`: boolean - Determines whether the `Class.TextButton` renders its text using rich text
- ...and 16 more

---

## TextBox

A 2D user interface element that displays player-editable text.

**Properties:**
- `TextBox.ClearTextOnFocus`: boolean - Determines whether clicking on the `TextBox` will clear its
- `TextBox.ContentText`: string
- `TextBox.CursorPosition`: int - Determines the offset of the text cursor in bytes, or `-1` if there is no
- `TextBox.Font`: Enum.Font - Determines the font used to render text.
- `TextBox.FontFace`: Datatype.Font - Determines the font used to render text.
- `TextBox.FontSize`: FontSize - Determines the font size of a `Class.TextBox` object.
- `TextBox.LineHeight`: float - Scales the spacing between lines of text in the `Class.TextBox`.
- `TextBox.MaxVisibleGraphemes`: int - The maximum number of graphemes the `Class.TextBox` can show.
- `TextBox.MultiLine`: boolean - When set to `true`, text inside a `TextBox` is able to move onto multiple
- `TextBox.OpenTypeFeatures`: string
- ...and 23 more

**Methods:**
- `TextBox:CaptureFocus` - Forces the client to focus on the TextBox.
- `TextBox:IsFocused` - Returns `true` if the `TextBox` is focused or `false` if it is not.
- `TextBox:ReleaseFocus` - Forces the client to unfocus the TextBox.

**Events:**
- `TextBox.Focused` - Fires when the `Class.TextBox` gains focus.
- `TextBox.FocusLost` - Fires when the client lets their focus leave the `Class.TextBox`.
- `TextBox.ReturnPressedFromOnScreenKeyboard`

---

## ImageLabel

A 2D user interface element that displays a single non-interactive image.

**Properties:**
- `ImageLabel.Image`: ContentId - The image content displayed by the UI element. Reads and writes to
- `ImageLabel.ImageColor3`: Color3 - Determines how a rendered image will be colorized.
- `ImageLabel.ImageContent`: Content - The image content displayed by the UI element. Supports
- `ImageLabel.ImageRectOffset`: Vector2 - The offset in pixels of the sub-area of an image to be displayed.
- `ImageLabel.ImageRectSize`: Vector2 - Determines the size in pixels of the sub-area of an image to be displayed.
- `ImageLabel.ImageTransparency`: float - Determines the transparency of the rendered image.
- `ImageLabel.IsLoaded`: boolean - Indicates whether the image has finished loading from Roblox.
- `ImageLabel.ResampleMode`: ResamplerMode - Selects the image resampling mode for the label.
- `ImageLabel.ScaleType`: ScaleType - Determines how an image will scale if displayed in a UI element whose size
- `ImageLabel.SliceCenter`: Rect - Sets the slice boundaries of a 9-sliced image.
- ...and 2 more

---

## ImageButton

A 2D user interface element that displays an interactive image.

**Properties:**
- `ImageButton.HoverImage`: ContentId - A texture ID that will be used when the `Class.ImageButton` is being
- `ImageButton.HoverImageContent`: Content - The image content that will be used when the `Class.ImageButton` is being
- `ImageButton.Image`: ContentId - The image content displayed by the `Class.ImageButton` element. Reads and
- `ImageButton.ImageColor3`: Color3 - Determines how a rendered image will be colorized.
- `ImageButton.ImageContent`: Content - The image content displayed by the UI element. Supports asset URIs and
- `ImageButton.ImageRectOffset`: Vector2 - The offset in pixels of the sub-area of an image to be displayed.
- `ImageButton.ImageRectSize`: Vector2 - Determines the size in pixels of the sub-area of an image to be displayed.
- `ImageButton.ImageTransparency`: float - Determines the transparency of the rendered image.
- `ImageButton.IsLoaded`: boolean - Indicates whether the Image has finished loading from the Roblox website.
- `ImageButton.PressedImage`: ContentId - A texture ID that will be used when an `Class.ImageButton` is being
- ...and 6 more

---

## ScrollingFrame

`ScrollingFrame` is a special `Class.Frame` type with built-in scrolling
interactivity and different ways to customize how the scrolling works.

**Properties:**
- `ScrollingFrame.AbsoluteCanvasSize`: Vector2 - The size of the area that is scrollable, in offsets.
- `ScrollingFrame.AbsoluteWindowSize`: Vector2 - The size of the frame, in offsets, without the scroll bars.
- `ScrollingFrame.AutomaticCanvasSize`: AutomaticSize - Determines whether `Class.ScrollingFrame.CanvasSize` is resized based on
- `ScrollingFrame.BottomImage`: ContentId - Image that displays on the bottom of a vertical scroll bar, or the right
- `ScrollingFrame.BottomImageContent`: Content - Image that displays on the bottom of a vertical scroll bar, or the right
- `ScrollingFrame.CanvasPosition`: Vector2 - Reflects the **current** positional offset of the canvas within the frame,
- `ScrollingFrame.CanvasSize`: UDim2 - Determines the size of the scrollable area.
- `ScrollingFrame.ElasticBehavior`: ElasticBehavior - Determines if and when elastic scrolling is allowed on touch‑enabled
- `ScrollingFrame.HorizontalScrollBarInset`: ScrollBarInset - Indicates whether `Class.ScrollingFrame.CanvasSize|CanvasSize` is inset by
- `ScrollingFrame.MidImage`: ContentId - Image which spans the area between
- ...and 10 more

---

## ViewportFrame

`Class.GuiObject` that renders 3D objects inside its bounds.

**Properties:**
- `ViewportFrame.Ambient`: Color3 - The lighting hue applied to the area within the `ViewportFrame`.
- `ViewportFrame.CurrentCamera`: Camera - `Class.Camera` that is used to render children objects.
- `ViewportFrame.ImageColor3`: Color3 - Determines how the rendered viewport image will be colorized.
- `ViewportFrame.ImageTransparency`: float - Determines the transparency of the rendered viewport image.
- `ViewportFrame.LightColor`: Color3 - The color of the emitted light.
- `ViewportFrame.LightDirection`: Vector3 - A `Datatype.Vector3` representing the direction of the light source.

---

## UIListLayout

Positions sibling UI elements in rows or columns within the parent UI
container.

**Properties:**
- `UIListLayout.HorizontalFlex`: UIFlexAlignment - Controls how to distribute extra horizontal space.
- `UIListLayout.ItemLineAlignment`: ItemLineAlignment - In a flex layout, defines the **cross-directional** alignment of siblings
- `UIListLayout.Padding`: UDim - Amount of free space between each element.
- `UIListLayout.VerticalFlex`: UIFlexAlignment - Controls how to distribute extra vertical space.
- `UIListLayout.Wraps`: boolean - Controls whether siblings within the parent container wrap.

---

## UIGridLayout

Positions sibling UI elements by filling rows using the space of the parent UI
element.

**Properties:**
- `UIGridLayout.AbsoluteCellCount`: Vector2 - The number of elements in the grid.
- `UIGridLayout.AbsoluteCellSize`: Vector2 - The absolute size of each element in the grid.
- `UIGridLayout.CellPadding`: UDim2 - Determines how much space there is between elements in the grid.
- `UIGridLayout.CellSize`: UDim2 - Determines the size of each element in the grid.
- `UIGridLayout.FillDirectionMaxCells`: int - Determines the maximum number of cells that may be used in a row or column
- `UIGridLayout.StartCorner`: StartCorner - Determines from which corner the grid starts laying out UI elements.

---

## UIPadding

Applies padding to the borders of the parent `Class.GuiObject`.

**Properties:**
- `UIPadding.PaddingBottom`: UDim - Padding to apply on the bottom side, relative to the parent's normal size.
- `UIPadding.PaddingLeft`: UDim - Padding to apply on the left side, relative to the parent's normal size.
- `UIPadding.PaddingRight`: UDim - Padding to apply on the right side, relative to the parent's normal size.
- `UIPadding.PaddingTop`: UDim - Padding to apply on the top side, relative to the parent's normal size.

---

## UICorner

UI modifier which applies deformation to corners of its parent
`Class.GuiObject`.

**Properties:**
- `UICorner.CornerRadius`: UDim - Determines the radius of the component.

---

## UIStroke

Applies an outline to text or a UI border.

**Properties:**
- `UIStroke.ApplyStrokeMode`: ApplyStrokeMode - Determines whether to apply the stroke to the object's border instead of
- `UIStroke.BorderOffset`: UDim - Specifies an additional offset to the stroke's position, relative to the
- `UIStroke.BorderStrokePosition`: BorderStrokePosition - Determines the stroke's position on its parent's border.
- `UIStroke.Color`: Color3 - Determines the stroke color.
- `UIStroke.Enabled`: boolean - Determines whether the stroke in visible.
- `UIStroke.LineJoinMode`: LineJoinMode - Determines how corners are interpreted.
- `UIStroke.StrokeSizingMode`: StrokeSizingMode - Determines whether the stroke's `Class.UIStroke.Thickness|Thickness` will
- `UIStroke.Thickness`: float - Determines the stroke's thickness.
- `UIStroke.Transparency`: float - Sets the stroke opacity independently of the parent object's
- `UIStroke.ZIndex`: int - Determines the order in which the stroke renders relative to sibling

---

## UIGradient

Applies a color and transparency gradient to the UI elements rendered by the
parent `Class.GuiObject`.

**Properties:**
- `UIGradient.Color`: ColorSequence - Determines the color blended with the parent GuiObject along the length of
- `UIGradient.Enabled`: boolean - Whether the gradient is enabled or not.
- `UIGradient.Offset`: Vector2 - Determines the scalar translation of the gradient from the center of the
- `UIGradient.Rotation`: float - Determines the clockwise rotation in degrees of the gradient starting from
- `UIGradient.Transparency`: NumberSequence - Determines how much the parent GuiObject can be seen through along the

---

## UIScale

An object that acts as a multiplier for the size of the parent UI element's
scale.

**Properties:**
- `UIScale.Scale`: float - Determines the multiplier to apply to the parent UI element's size.

---

## UIAspectRatioConstraint

Ensures the parent UI element maintains a particular aspect ratio.

**Properties:**
- `UIAspectRatioConstraint.AspectRatio`: float - Determines the width-to-height ratio to maintain.
- `UIAspectRatioConstraint.AspectType`: AspectType - Determines how the maximum size of the object is limited.
- `UIAspectRatioConstraint.DominantAxis`: DominantAxis - Determines the axis to use when setting the new size of the object.

---

## BillboardGui

A container for `Class.GuiObject|GuiObjects` that renders in 3D space facing
the camera.

**Properties:**
- `BillboardGui.Active`: boolean - Controls whether the descendants will receive input events.
- `BillboardGui.Adornee`: Instance - Sets the target part or attachment that the `Class.BillboardGui` is
- `BillboardGui.AlwaysOnTop`: boolean - Determines whether the `Class.BillboardGui` will always be rendered on top
- `BillboardGui.Brightness`: float - Determines the factor by which the `Class.BillboardGui` container's light
- `BillboardGui.ClipsDescendants`: boolean - Whether portions of `Class.GuiObject|GuiObjects` that fall outside of the
- `BillboardGui.CurrentDistance`: float - The current distance in studs that the `Class.BillboardGui` is from the
- `BillboardGui.DistanceLowerLimit`: float - Determines the distance in studs at which the `Class.BillboardGui` will
- `BillboardGui.DistanceStep`: float - Determines the size `Class.BillboardGui.CurrentDistance|CurrentDistance`
- `BillboardGui.DistanceUpperLimit`: float - Determines the distance in studs at which the `Class.BillboardGui` will
- `BillboardGui.ExtentsOffset`: Vector3 - Determines how the `Class.BillboardGui` is offset from its
- ...and 8 more

---

## SurfaceGui

Container for GuiObjects that are rendered on the surface of a part.

**Properties:**
- `SurfaceGui.AlwaysOnTop`: boolean - Determines whether the `Class.SurfaceGui` will always be rendered on top
- `SurfaceGui.Brightness`: float - Determines the factor by which the `Class.SurfaceGui` container's light is
- `SurfaceGui.CanvasSize`: Vector2 - The size of a "virtual screen" in "virtual pixels" which makes
- `SurfaceGui.ClipsDescendants`: boolean - Whether portions of `Class.GuiObject|GuiObjects` that fall outside of the
- `SurfaceGui.LightInfluence`: float - Controls how much the `Class.SurfaceGui` is influenced by environmental
- `SurfaceGui.MaxDistance`: float - Controls how far away the `Class.SurfaceGui` can be displayed before it
- `SurfaceGui.PixelsPerStud`: float - Determines the density of pixels used for each world-space stud to render
- `SurfaceGui.SizingMode`: SurfaceGuiSizingMode - Determines whether the `Class.SurfaceGui` will render at a fixed size or
- `SurfaceGui.ToolPunchThroughDistance`: float - Sets the distance in which left clicking starts acting on the
- `SurfaceGui.ZOffset`: float - Layers this `Class.SurfaceGui` in relation to other

---

## CanvasGroup

Blends descendants as a group with color/transparency.

**Properties:**
- `CanvasGroup.GroupColor3`: Color3 - Color tint that applies to all descendants.
- `CanvasGroup.GroupTransparency`: float - Transparency that applies to all descendants.

---

