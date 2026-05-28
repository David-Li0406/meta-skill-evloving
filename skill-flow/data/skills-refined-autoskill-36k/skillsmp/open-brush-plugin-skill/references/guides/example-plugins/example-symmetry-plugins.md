# Example Symmetry Plugins

### AutoLathe

<div align="left"><figure><img src="../../../.gitbook/assets/symmetry-autolathe_compressed.gif" alt="" width="375"><figcaption></figcaption></figure></div>

Like spinning the mirror by hand but with precise control

#### Parameters

* **Speed:** How fast to spin
* **Angle X:** The axis tilt in the X direction
* **Angle Y:** The axis tilt in the Y direction

### Boids

A flock of pointers follows your hand using simple rules to control how they fly

<div align="left"><figure><img src="../../../.gitbook/assets/symmetry-boids_compressed.gif" alt="" width="375"><figcaption></figcaption></figure></div>

#### Parameters

* **Number of copies:** How many boids in the flock
* **Separation Amount:** How strongly each boid tries to stay away from others
* **Alignment Amount:** How closely the boids try and follow the flocks path
* **Pointer Attraction:** How strongly each boid is attracted to your brush position

### Ducklings

{% embed url="https://www.youtube.com/watch?v=WkGY_nXPehc" %}

The pointers follow your brush position but each one moves towards a point where your hand was further back in time

#### Parameters

* **Copies:** The number of strokes to draw at once
* **Delay per copy:** How far back in time (in frames) for each copy
* **Amount:** How far between the current and past position to move towards. 0.5 is the midpoint between past and current

### EllipseAround

{% embed url="https://www.youtube.com/watch?v=e3JXcvarGkI" %}

Copies of your stroke forming an ellipse - with optional color shifts

#### Parameters

* **Copies:** The number of strokes to draw at once
* **Eccentricity:** How elliptical the shape is
* **Axis Consistency:** Controls how much the elliptical axis follows your brush position

### Frame

<div align="left"><figure><img src="../../../.gitbook/assets/symmetry-frame_compressed.gif" alt="" width="375"><figcaption></figcaption></figure></div>

A simple frame of points following your brush position

### HoldFirstClick

{% embed url="https://www.youtube.com/watch?v=JS06ssbbCi0" %}

Like [Many Around](example-symmetry-plugins.md#manyaround) except the widget always moves to where you start drawing

#### Parameters

* **Copies:** The number of strokes to draw at once

### ManyAlong

<div align="left"><figure><img src="../../../.gitbook/assets/symmetry-manyalong_compressed.gif" alt="" width="375"><figcaption></figcaption></figure></div>

Linear copies of your stroke with optional color shifts

#### Parameters

* **Copies:** The number of strokes to draw at once
* **Distance:** How far each copy is from the next

### ManyAround

<div align="left"><figure><img src="../../../.gitbook/assets/symmetry-manyaround_compressed.gif" alt="" width="375"><figcaption></figcaption></figure></div>

Radial copies of your stroke with optional color shifts

#### Parameters

* **Copies:** The number of strokes to draw at once

### PointSymSpin

Works like activating Multimirror but the extra pointers spin around your brush position

#### Parameters

(todo)

### Pole

{% embed url="https://www.youtube.com/watch?v=7YxjNvCY8ak" %}

Multiple copies of your brush spaced between your left and right hand positions

#### Parameters

* **Copies:** The number of strokes to draw at once

### PolygonAround

<div align="left"><figure><img src="../../../.gitbook/assets/symmetry-polygonaround_compressed.gif" alt="" width="375"><figcaption></figcaption></figure></div>

Copies of your stroke forming an polygon

#### Parameters

* **Copies:** The number of strokes to draw at once
* **Sides:** The number of sides of the polygon

### RectangleAround

<div align="left"><figure><img src="../../../.gitbook/assets/symmetry-rectanglearound_compressed.gif" alt="" width="375"><figcaption></figcaption></figure></div>

Copies of your stroke forming an rectangle

#### Parameters

* **Number of points along width:** How many points along the sides
* **Number of points along height:** How many points along the top and bottom
* **Spacing:** The distance between each point
* **Exterior Only:** Whether to create copies just around the perimeter or also fill in the middle

### Spin

<div align="left"><figure><img src="../../../.gitbook/assets/symmetry-spin_compressed.gif" alt="" width="375"><figcaption></figcaption></figure></div>

Multiple copies of your brush spinning around your actual brush position

#### Parameters

* **Copies:** The number of strokes to draw at once
* **Speed:** How fast the extra pointers are rotating
* **Radius:** The radius of the circle they are rotating around

### StrokePoints

<div align="left"><figure><img src="../../../.gitbook/assets/symmetry-alongstroke_compressed.gif" alt="" width="375"><figcaption></figcaption></figure></div>

The previous stroke you drew is used as a template and multiple copies of the pointer are spread along it as you draw

#### Parameters

* **Point Spacing:** The distance to space out the copies along the stroke

### SuperEllipseAround

<div align="left"><figure><img src="../../../.gitbook/assets/symmetry-superellipsearound_compressed.gif" alt="" width="375"><figcaption></figcaption></figure></div>

Copies of your stroke forming a [superellipse](https://en.wikipedia.org/wiki/Superellipse)

#### Parameters

* **Copies:** The number of strokes to draw at once
* **n:** The parameter that controls the overall shape of the superellipse
* **Eccentricity:** How elliptical to make the shape
* **Axis Consistency:** Controls how much the elliptical axis follows your brush position

### Svg

<div align="left"><figure><img src="../../../.gitbook/assets/symmetry-svg_compressed.gif" alt="" width="375"><figcaption></figcaption></figure></div>

An example of using an SVG file as a template for symmetry patterns

### SvgAround

<div align="left"><figure><img src="../../../.gitbook/assets/symmetry-svgaround_compressed.gif" alt="" width="375"><figcaption></figcaption></figure></div>

Similar to [SVG](example-symmetry-plugins.md#svg) but centered around the Symmetry Widget

#### Parameters

* **Point Spacing:** The distance between each pointer around the shape

###
