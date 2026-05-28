
# Transform

## Summary
Represents a position, rotation and scale in one object

## Class Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>identity</td><td><a href="transform.md">Transform</a><br>Read-only</td><td>A transform that does nothing. No translation, rotation or scaling</td></tr>
</tbody></table>



## Instance Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>inverse</td><td><a href="transform.md">Transform</a><br>Read-only</td><td>The inverse of this transform</td></tr>
<tr><td>up</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>A translation of 1 in the y axis</td></tr>
<tr><td>down</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>A translation of -1 in the y axis</td></tr>
<tr><td>right</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>A translation of 1 in the x axis</td></tr>
<tr><td>left</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>A translation of -1 in the x axis</td></tr>
<tr><td>forward</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>A translation of 1 in the z axis</td></tr>
<tr><td>back</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>A translation of -1 in the z axis</td></tr>
<tr><td>position</td><td><a href="vector3.md">Vector3</a><br>Read/Write</td><td>Get or set the position of this transform</td></tr>
<tr><td>rotation</td><td><a href="rotation.md">Rotation</a><br>Read/Write</td><td>Get or set the rotation of this transform</td></tr>
<tr><td>scale</td><td>number<br>Read/Write</td><td>Get or set the scale of this transform</td></tr>
</tbody></table>



## Class Methods

        
### Transform:New(translation, rotation, scale)

Creates a new translation, rotation and scale transform

**Returns:** <a href="transform.md">Transform</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>translation</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The translation amount</td></tr>
<tr><td>rotation</td><td><a href="rotation.md">Rotation</a></td><td></td><td>The rotation amount</td></tr>
<tr><td>scale</td><td>number</td><td></td><td>The scale amount</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myTransform = Transform:New(Vector3(1, 2, 3), Rotation.identity, 2)</strong></code></pre>




### Transform:New(translation, rotation)

Creates a new translation and rotation transform

**Returns:** <a href="transform.md">Transform</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>translation</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The translation amount</td></tr>
<tr><td>rotation</td><td><a href="rotation.md">Rotation</a></td><td></td><td>The rotation amount</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myTransform = Transform:New(Vector3(1, 2, 3), Rotation.identity)</strong></code></pre>




### Transform:New(translation)

Creates a new translation transform

**Returns:** <a href="transform.md">Transform</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>translation</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The translation amount</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myTransform = Transform:New(Vector3(1, 2, 3))</strong></code></pre>




### Transform:New(translation, scale)

Creates a new translation and scale transform

**Returns:** <a href="transform.md">Transform</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>translation</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The translation amount</td></tr>
<tr><td>scale</td><td>number</td><td></td><td>The scale amount</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myTransform = Transform:New(Vector3(1, 2, 3), 2)</strong></code></pre>




### Transform:Position(x, y, z)

Creates a new translation transform

**Returns:** <a href="transform.md">Transform</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The x translation amount</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The y translation amount</td></tr>
<tr><td>z</td><td>number</td><td></td><td>The z translation amount</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myTransform = Transform:Position(1, 2, 3)</strong></code></pre>




### Transform:Position(position)

Creates a new translation transform

**Returns:** <a href="transform.md">Transform</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>position</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The Vector3 position</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myTransform = Transform:Position(myVector3)</strong></code></pre>




### Transform:Rotation(x, y, z)

Creates a new rotation transform

**Returns:** <a href="transform.md">Transform</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The x rotation amount</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The y rotation amount</td></tr>
<tr><td>z</td><td>number</td><td></td><td>The z rotation amount</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myTransform = Transform:Rotation(1, 2, 3)</strong></code></pre>




### Transform:Rotation(rotation)

Creates a new rotation transform

**Returns:** <a href="transform.md">Transform</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>rotation</td><td><a href="rotation.md">Rotation</a></td><td></td><td>The rotation</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myTransform = Transform:Rotation(myRotation)</strong></code></pre>




### Transform:Scale(amount)

Creates a new scale transform

**Returns:** <a href="transform.md">Transform</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>amount</td><td>number</td><td></td><td>The scale amount</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myTransform = Transform:Scale(2)</strong></code></pre>




### Transform:Lerp(a, b, t)

Interpolates between two transforms

**Returns:** <a href="transform.md">Transform</a>  (A transform that blends between a and b based on the value of t)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="transform.md">Transform</a></td><td></td><td>The first transform</td></tr>
<tr><td>b</td><td><a href="transform.md">Transform</a></td><td></td><td>The second transform</td></tr>
<tr><td>t</td><td>number</td><td></td><td>The value between 0 and 1 that controls how far between a and b the new transform is</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newTransform = Transform:Lerp(transformA, transformB, 0.25)</strong></code></pre>



    

## Instance Methods

        
### transform:TransformBy(transform)

Applies another transform to this transform

**Returns:** <a href="transform.md">Transform</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>transform</td><td><a href="transform.md">Transform</a></td><td></td><td>The transform to apply</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newTransform = myTransform:TransformBy(myOtherTransform)</strong></code></pre>




### transform:TranslateBy(translation)

Applies a translation to this transform

**Returns:** <a href="transform.md">Transform</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>translation</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The translation to apply</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newTransform = myTransform:TranslateBy(Vector3.up * 3)</strong></code></pre>




### transform:TranslateBy(x, y, z)

Applies a translation to this transform

**Returns:** <a href="transform.md">Transform</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The x translation to apply</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The y translation to apply</td></tr>
<tr><td>z</td><td>number</td><td></td><td>The z translation to apply</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newTransform = myTransform:TranslateBy(1, 2, 3)</strong></code></pre>




### transform:RotateBy(rotation)

Applies a rotation to this transform

**Returns:** <a href="transform.md">Transform</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>rotation</td><td><a href="rotation.md">Rotation</a></td><td></td><td>The rotation to apply</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newTransform = myTransform:RotateBy(Rotation.left)</strong></code></pre>




### transform:RotateBy(x, y, z)

Applies a rotation to this transform

**Returns:** <a href="transform.md">Transform</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The x rotation to apply</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The y rotation to apply</td></tr>
<tr><td>z</td><td>number</td><td></td><td>The z rotation to apply</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newTransform = myTransform:RotateBy(45, 0, 0)</strong></code></pre>




### transform:ScaleBy(scale)

Applies a scale to this transform

**Returns:** <a href="transform.md">Transform</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>scale</td><td>number</td><td></td><td>The scale value to apply</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newTransform = myTransform:ScaleBy(2)</strong></code></pre>




### transform:Multiply(other)

Combines another transform with this one (Does the same as "TransformBy")

**Returns:** <a href="transform.md">Transform</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="transform.md">Transform</a></td><td></td><td>The Transform to apply to this one</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newTransform = myTransform:Multiply(Transform.up)</strong></code></pre>



    
