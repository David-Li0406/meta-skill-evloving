
# Vector3

## Summary
A position or offset in 3D space. See https://docs.unity3d.com/ScriptReference/Vector3.html for more detail on many of these methods or properties

## Class Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>back</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>A vector of -1 in the z axis</td></tr>
<tr><td>down</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>A vector of -1 in the y axis</td></tr>
<tr><td>forward</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>A vector of 1 in the z axis</td></tr>
<tr><td>left</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>A vector of -1 in the x axis</td></tr>
<tr><td>negativeInfinity</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>A vector of -infinity in all axes</td></tr>
<tr><td>one</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>A vector of 1 in all axes</td></tr>
<tr><td>positiveInfinity</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>A vector of infinity in all axes</td></tr>
<tr><td>right</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>A vector of 1 in the x axis</td></tr>
<tr><td>up</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>A vector of 1 in the y axis</td></tr>
<tr><td>zero</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>A vector of 0 in all axes</td></tr>
</tbody></table>



## Instance Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>this[index]</td><td>number<br>Read/Write</td><td>The component at the specified index</td></tr>
<tr><td>x</td><td>number<br>Read/Write</td><td>The x coordinate</td></tr>
<tr><td>y</td><td>number<br>Read/Write</td><td>The y coordinate</td></tr>
<tr><td>z</td><td>number<br>Read/Write</td><td>The z coordinate</td></tr>
<tr><td>magnitude</td><td>number<br>Read/Write</td><td>Returns the length of this vector</td></tr>
<tr><td>sqrMagnitude</td><td>number<br>Read/Write</td><td>Returns the squared length of this vector</td></tr>
<tr><td>normalized</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>Returns a vector with the same direction but with a length of 1</td></tr>
</tbody></table>



## Class Methods

        
### Vector3:New(x, y, z)

Creates a new vector based on x, y and z position

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The x coordinate</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The y coordinate</td></tr>
<tr><td>z</td><td>number</td><td></td><td>The z coordinate</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newVector = Vector3:New(1, 2, 3)</strong></code></pre>




### Vector3:Cross(a, b)

Returns the cross product of two vectors

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The first vector</td></tr>
<tr><td>b</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The second vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>crossProduct = Vector3:Cross(firstVector, secondVector)</strong></code></pre>




### Vector3:Lerp(a, b, t)

Linearly interpolates between two points

**Returns:** <a href="vector3.md">Vector3</a>  (A point somewhere between a and b based on the value of t)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The first point</td></tr>
<tr><td>b</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The second point</td></tr>
<tr><td>t</td><td>number</td><td></td><td>The value between 0 and 1 that controls how far between a and b the new point is</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newPoint = Vector3:Lerp(pointA, PointB, 0.25)</strong></code></pre>




### Vector3:LerpUnclamped(a, b, t)

Linearly interpolates (or extrapolates) between two points

**Returns:** <a href="vector3.md">Vector3</a>  (A point somewhere between a and b based on the value of t)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The first point</td></tr>
<tr><td>b</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The second point</td></tr>
<tr><td>t</td><td>number</td><td></td><td>The value that controls how far between (or beyond) a and b the new point is</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newPoint = Vector3:Lerp(pointA, PointB, 0.25)</strong></code></pre>




### Vector3:Max(a, b)

Creates a vector made from the largest components of the inputs

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The first vector</td></tr>
<tr><td>b</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The second vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = Vector3:Max(firstVector, secondVector</strong></code></pre>




### Vector3:Min(a, b)

Creates a vector made from the smallest components of the inputs

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The first vector</td></tr>
<tr><td>b</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The second vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = Vector3:Min(firstVector, secondVector</strong></code></pre>




### Vector3:Slerp(a, b, t)

Spherically interpolates between two vectors

**Returns:** <a href="vector3.md">Vector3</a>  (A point somewhere between a and b based on the value of t)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The first point</td></tr>
<tr><td>b</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The second point</td></tr>
<tr><td>t</td><td>number</td><td></td><td>The value that controls how far between (or beyond) a and b the new point is</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newPoint = Vector3:Lerp(pointA, PointB, 0.25)</strong></code></pre>




### Vector3:SlerpUnclamped(a, b, t)

Spherically interpolates (or extrapolates) between two vectors

**Returns:** <a href="vector3.md">Vector3</a>  (A point somewhere between a and b based on the value of t)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The first point</td></tr>
<tr><td>b</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The second point</td></tr>
<tr><td>t</td><td>number</td><td></td><td>The value that controls how far between (or beyond) a and b the new point is</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newPoint = Vector3:Lerp(pointA, PointB, 0.25)</strong></code></pre>



    

## Instance Methods

        
### vector3:Angle(other)

The unsigned angle in degrees between this vector and another

**Returns:** number 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The other vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>angle = myVector:Angle(otherVector)</strong></code></pre>




### vector3:ClampMagnitude(maxLength)

Returns a vector with the same direction but with it's length clamped to a maximum

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>maxLength</td><td>number</td><td></td><td>The maximum length of the returned vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>clampedVector = myVector:ClampMagnitude(5)</strong></code></pre>




### vector3:Distance(other)

Returns the distance between two points

**Returns:** number 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The other vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>distance = Vector3:Distance(firstPoint, secondPoint)</strong></code></pre>




### vector3:MoveTowards(target, maxDistanceDelta)

Moves a point towards a target point

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>target</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The target point</td></tr>
<tr><td>maxDistanceDelta</td><td>number</td><td></td><td>The maximum distance to move towards the target point</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>position = position:MoveTowards(PointB, 0.25)</strong></code></pre>




### vector3:Project(other)

Projects this vector onto another

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The other vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newVector = myVector:Project(otherVector)</strong></code></pre>




### vector3:ProjectOnPlane(planeNormal)

Projects this vector onto a plane defined by a normal orthogonal to the plane

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>planeNormal</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The normal vector of the plane</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newVector = myVector:ProjectOnPlane(planeNormal)</strong></code></pre>




### vector3:Reflect(normal)

Reflects a vector off the vector defined by a normal

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>normal</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The normal vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newVector = myVector:Reflect(normalVector)</strong></code></pre>




### vector3:RotateTowards(target, maxRadiansDelta, maxMagnitudeDelta)

Moves this vector towards another with a maximum change in angle

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>target</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The target vector</td></tr>
<tr><td>maxRadiansDelta</td><td>number</td><td></td><td>The maximum change in angle</td></tr>
<tr><td>maxMagnitudeDelta</td><td>number</td><td></td><td>The maximum allowed change in vector magnitude for this rotation</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newVector = myVector:RotateTowards(targetVector, Math.pi / 10, 0.25)</strong></code></pre>




### vector3:ScaleBy(other)

Multiplies two vectors component-wise

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The other vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Scale(secondVector</strong></code></pre>




### vector3:SignedAngle(other, axis)

Returns the signed angle in degrees between two points and the origin

**Returns:** number 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The other vector</td></tr>
<tr><td>axis</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The axis around which the vectors are rotated</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>angle = myVector:SignedAngle(otherVector, axis)</strong></code></pre>




### vector3:Add(other)

Adds two vectors

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The other vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Add(secondVector)</strong></code></pre>




### vector3:Add(x, y, z)

Adds x, y and z values to this vector

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The x value</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The y value</td></tr>
<tr><td>z</td><td>number</td><td></td><td>The z value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Add(1, 2, 3)</strong></code></pre>




### vector3:Subtract(other)

Subtracts a Vector3 from this vector

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The vector to subtract</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Subtract(otherVector)</strong></code></pre>




### vector3:Subtract(x, y, z)

Subtracts x, y and z values from this vector

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The x value</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The y value</td></tr>
<tr><td>z</td><td>number</td><td></td><td>The z value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Subtract(1, 2, 3)</strong></code></pre>




### vector3:Multiply(value)

Multiplies this vector by a scalar value

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>value</td><td>number</td><td></td><td>The scalar value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Multiply(2)</strong></code></pre>




### vector3:ScaleBy(x, y, z)

Multiplies this vector by x, y and z values component-wise

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The x value</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The y value</td></tr>
<tr><td>z</td><td>number</td><td></td><td>The z value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Multiply(2, 3, 4)</strong></code></pre>




### vector3:Divide(value)

Divides this vector by a scalar value

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>value</td><td>number</td><td></td><td>The scalar value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Divide(2)</strong></code></pre>




### vector3:NotEquals(other)

Is this vector not equal to another?

**Returns:** boolean 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The other vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>if myVector:NotEquals(Vector3.zero) then print("Vector is not zero") end</strong></code></pre>




### vector3:NotEquals(x, y, z)

Is this vector not equal to these x, y and z values?

**Returns:** boolean 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The x value</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The y value</td></tr>
<tr><td>z</td><td>number</td><td></td><td>The z value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>if myVector:NotEquals(1, 2, 3) then print("Vector is not 1,2,3") end</strong></code></pre>



    
