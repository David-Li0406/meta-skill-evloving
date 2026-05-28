
# Random

## Summary
Various functions for generating random data

## Class Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>insideUnitCircle</td><td><a href="vector2.md">Vector2</a><br>Read-only</td><td>Returns a random 2d point inside a circle of radius 1</td></tr>
<tr><td>insideUnitSphere</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>Returns a random 3d point inside a sphere of radius 1</td></tr>
<tr><td>onUnitSphere</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>Returns a random 3d point on the surface of a sphere of radius 1</td></tr>
<tr><td>rotation</td><td><a href="rotation.md">Rotation</a><br>Read-only</td><td>Returns a random rotation</td></tr>
<tr><td>rotationUniform</td><td><a href="rotation.md">Rotation</a><br>Read-only</td><td>Returns a random rotation with uniform distribution</td></tr>
<tr><td>value</td><td>number<br>Read-only</td><td>Returns a random number between 0 and 1</td></tr>
<tr><td>color</td><td><a href="color.md">Color</a><br>Read-only</td><td>Returns a random color</td></tr>
</tbody></table>




## Class Methods

        
### Random:ColorHSV(hueMin, hueMax, saturationMin, saturationMax, valueMin, valueMax)

Returns a random color within given ranges

**Returns:** <a href="color.md">Color</a>  (The new random color)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>hueMin</td><td>number</td><td></td><td>Minimum hue</td></tr>
<tr><td>hueMax</td><td>number</td><td></td><td>Maximum hue</td></tr>
<tr><td>saturationMin</td><td>number</td><td></td><td>Minimum saturation</td></tr>
<tr><td>saturationMax</td><td>number</td><td></td><td>Maximum saturation</td></tr>
<tr><td>valueMin</td><td>number</td><td></td><td>Minimum brightness</td></tr>
<tr><td>valueMax</td><td>number</td><td></td><td>Maximum brightness</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myColor = Random:ColorHSV(0, 1, 0.8, 1, 0.5, 1)</strong></code></pre>




### Random:InitState(seed)

Initializes the random number generator with a specified seed

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>seed</td><td>number</td><td></td><td>The seed for the random number generator</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Random:InitState(seed)</strong></code></pre>




### Random:Range(min, max)

Returns a random float number between min and max (inclusive

**Returns:** number  (A random whole number >= min and <= max)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>min</td><td>number</td><td></td><td>Minimum value</td></tr>
<tr><td>max</td><td>number</td><td></td><td>Maximum value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Random:Range(1, 6)</strong></code></pre>




### Random:Range(min, max)

Returns a random float number between min and max

**Returns:** number  (The random number  >= min and <= max)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>min</td><td>number</td><td></td><td>Minimum value</td></tr>
<tr><td>max</td><td>number</td><td></td><td>Maximum value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Random:Range(-1, 1)</strong></code></pre>



    

