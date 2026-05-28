
# Vector2

## Summary
A position or offset in 2D space. See https://docs.unity3d.com/ScriptReference/Vector2.html for more detail on many of these methods or properties

## Class Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>down</td><td><a href="vector2.md">Vector2</a><br>Read-only</td><td>A vector of -1 in the y axis</td></tr>
<tr><td>left</td><td><a href="vector2.md">Vector2</a><br>Read-only</td><td>A vector of -1 in the x axis</td></tr>
<tr><td>negativeInfinity</td><td><a href="vector2.md">Vector2</a><br>Read-only</td><td>A vector of negative infinity in all axes</td></tr>
<tr><td>one</td><td><a href="vector2.md">Vector2</a><br>Read-only</td><td>A vector of 1 in all axes</td></tr>
<tr><td>positiveInfinity</td><td><a href="vector2.md">Vector2</a><br>Read-only</td><td>A vector of positive infinity in all axes</td></tr>
<tr><td>right</td><td><a href="vector2.md">Vector2</a><br>Read-only</td><td>A vector of 1 in the x axis</td></tr>
<tr><td>up</td><td><a href="vector2.md">Vector2</a><br>Read-only</td><td>A vector of 1 in the y axis</td></tr>
<tr><td>zero</td><td><a href="vector2.md">Vector2</a><br>Read-only</td><td>A vector of 0 in all axes</td></tr>
</tbody></table>



## Instance Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>this[index]</td><td>number<br>Read/Write</td><td>The component at the specified index</td></tr>
<tr><td>x</td><td>number<br>Read/Write</td><td>The x coordinate</td></tr>
<tr><td>y</td><td>number<br>Read/Write</td><td>The y coordinate</td></tr>
<tr><td>magnitude</td><td>number<br>Read/Write</td><td>The length of this vector</td></tr>
<tr><td>sqrMagnitude</td><td>number<br>Read/Write</td><td>The square of the length of this vector (faster to calculate if you're just comparing two lengths)</td></tr>
<tr><td>normalized</td><td><a href="vector2.md">Vector2</a><br>Read-only</td><td>Returns a vector with the same distance but witha length of 1</td></tr>
</tbody></table>



## Class Methods

        
### Vector2:New(x, y)

Creates a new vector

**Returns:** <a href="vector2.md">Vector2</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td>0</td><td>The x coordinate</td></tr>
<tr><td>y</td><td>number</td><td>0</td><td>The y coordinate</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newVector = Vector2(1, 2)</strong></code></pre>




### Vector2:Dot(a, b)

The dot product of two vectors

**Returns:** number 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The first vector</td></tr>
<tr><td>b</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The second vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = Vector3:Dot(myVector, otherVector</strong></code></pre>




### Vector2:Lerp(a, b, t)

Linearly interpolates between two points

**Returns:** <a href="vector2.md">Vector2</a>  (A point somewhere between a and b based on the value of t)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The first point</td></tr>
<tr><td>b</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The second point</td></tr>
<tr><td>t</td><td>number</td><td></td><td>The value between 0 and 1 that controls how far between a and b the new point is</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newPoint = Vector2:Lerp(pointA, PointB, 0.25)</strong></code></pre>




### Vector2:LerpUnclamped(a, b, t)

Linearly interpolates (or extrapolates) between two points

**Returns:** <a href="vector2.md">Vector2</a>  (A point somewhere between a and b based on the value of t)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The first point</td></tr>
<tr><td>b</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The second point</td></tr>
<tr><td>t</td><td>number</td><td></td><td>The value that controls how far between (or beyond) a and b the new point is</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newPoint = Vector2:Lerp(pointA, PointB, 0.25)</strong></code></pre>




### Vector2:Max(a, b)

Creates a vector made from the largest components of the inputs

**Returns:** <a href="vector2.md">Vector2</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The first vector</td></tr>
<tr><td>b</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The second vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = Vector2:Max(firstVector, secondVector</strong></code></pre>




### Vector2:Min(a, b)

Creates a vector made from the largest components of the inputs

**Returns:** <a href="vector2.md">Vector2</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The first vector</td></tr>
<tr><td>b</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The second vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = Vector2:Min(firstVector, secondVector</strong></code></pre>




### Vector2:Slerp(a, b, t)

Spherically interpolates between two vectors

**Returns:** <a href="vector2.md">Vector2</a>  (A point somewhere between a and b based on the value of t)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The first point</td></tr>
<tr><td>b</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The second point</td></tr>
<tr><td>t</td><td>number</td><td></td><td>The value that controls how far between (or beyond) a and b the new point is</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newPoint = Vector3:Slerp(pointA, PointB, 0.25)</strong></code></pre>




### Vector2:SlerpUnclamped(a, b, t)

Spherically interpolates (or extrapolates) between two vectors

**Returns:** <a href="vector2.md">Vector2</a>  (A point somewhere between a and b based on the value of t)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The first point</td></tr>
<tr><td>b</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The second point</td></tr>
<tr><td>t</td><td>number</td><td></td><td>The value that controls how far between (or beyond) a and b the new point is</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newPoint = Vector3:SlerpUnclamped(pointA, PointB, 0.25)</strong></code></pre>




### Vector2:PointOnCircle(degrees)

Returns the point the given number of degrees around a circle with radius 1

**Returns:** <a href="vector2.md">Vector2</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>degrees</td><td>number</td><td></td><td>The angle in degrees</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = Vector2:PointOnCircle(45)</strong></code></pre>



    

## Instance Methods

        
### vector2:Angle(other)

The unsigned angle in degrees between this vector and another

**Returns:** number 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The other vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>angle = myVector:Angle(otherVector)</strong></code></pre>




### vector2:ClampMagnitude(maxLength)

Returns a vector with the same direction but with it's length clamped to a maximum

**Returns:** <a href="vector2.md">Vector2</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>maxLength</td><td>number</td><td></td><td>The maximum length of the new vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newVector = myVector:ClampMagnitude</strong></code></pre>




### vector2:Distance(other)

The distance between two points

**Returns:** number 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The other vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>distance = Vector2:Distance(firstPoint, secondPoint)</strong></code></pre>




### vector2:MoveTowards(target, maxDistanceDelta)

Moves a point towards a target point

**Returns:** <a href="vector2.md">Vector2</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>target</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The target point</td></tr>
<tr><td>maxDistanceDelta</td><td>number</td><td></td><td>The maximum distance to move</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newPoint = Vector2:MoveTowards(currentPoint, targetPoint, 0.25)</strong></code></pre>




### vector2:Reflect(normal)

Reflects a vector off the vector defined by a normal

**Returns:** <a href="vector2.md">Vector2</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>normal</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The normal vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newVector = myVector:Reflect(normalVector)</strong></code></pre>




### vector2:Scale(other)

Scales a vector by multiplying it's components by the components of another vector

**Returns:** <a href="vector2.md">Vector2</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The vector to scale by</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newVector = myVector:Scale(otherVector)</strong></code></pre>




### vector2:SignedAngle(other)

Returns the signed angle in degrees between this vector and another

**Returns:** number 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The other vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:SignedAngle(otherVector</strong></code></pre>




### vector2:OnX()

Converts this 2D vector to a 3D vector on the YZ plane)

**Returns:** <a href="vector3.md">Vector3</a>  (A 3D Vector based on the input but with x as 0: (0, inX, inY))




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myVector3 = myVector2:OnX()</strong></code></pre>




### vector2:OnY()

Converts this 2D vector to a 3D vector on the XZ plane (i.e. with all y values set to 0)

**Returns:** <a href="vector3.md">Vector3</a>  (A 3D Vector based on the input but with y as 0: (inX, 0, inY))




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myVector3 = myVector2:OnY()</strong></code></pre>




### vector2:OnZ()

Converts this 2D vector to a 3D vector on the XY plane (i.e. with all z values set to 0)

**Returns:** <a href="vector3.md">Vector3</a>  (A 3D Vector based on the input but with z as 0: (inX, inX, 0))




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myVector3 = myVector2:OnZ()</strong></code></pre>




### vector2:Add(other)

Adds this vector to another

**Returns:** <a href="vector2.md">Vector2</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The other vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Add(otherVector)</strong></code></pre>




### vector2:Add(x, y)

Adds the given x and y values to this vector

**Returns:** <a href="vector2.md">Vector2</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The x value</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The y value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Add(2, 3)</strong></code></pre>




### vector2:Subtract(other)

Subtracts another vector from this one

**Returns:** <a href="vector2.md">Vector2</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The other vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Subtract(otherVector)</strong></code></pre>




### vector2:Subtract(x, y)

Subtracts the given x and y values from this vector

**Returns:** <a href="vector2.md">Vector2</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The x value</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The y value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Subtract(2, 3)</strong></code></pre>




### vector2:Multiply(value)

Multiplies a vector by a scalar value

**Returns:** <a href="vector2.md">Vector2</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>value</td><td>number</td><td></td><td>The value to multiply by</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Multiply(2)</strong></code></pre>




### vector2:ScaleBy(other)

Multiplies this vector by another component-wise

**Returns:** <a href="vector2.md">Vector2</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The other vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:ScaleBy(Vector2:New(2, 3)))</strong></code></pre>




### vector2:ScaleBy(x, y)

Multiplies each component of this vector by the given x and y values

**Returns:** <a href="vector2.md">Vector2</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The x value</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The y value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:ScaleBy(2, 3)</strong></code></pre>




### vector2:Divide(value)

Divides this vector by another

**Returns:** <a href="vector2.md">Vector2</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>value</td><td>number</td><td></td><td>The value to divide by</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Divide(2)</strong></code></pre>




### vector2:NotEquals(other)

Is this vector not equal to another?

**Returns:** boolean 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The other vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>if myVector:NotEquals(Vector2.zero) then print("Vector is not zero") end</strong></code></pre>




### vector2:NotEquals(x, y)

Is this vector not equal to the given x and y values?

**Returns:** boolean 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The x value</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The y value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>if myVector:NotEquals(1, 2) then print("Vector is not 1,2") end</strong></code></pre>



    
