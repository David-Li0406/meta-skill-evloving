
# Color

## Summary
An RGB color

## Class Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>black</td><td><a href="color.md">Color</a><br>Read-only</td><td>The color black</td></tr>
<tr><td>blue</td><td><a href="color.md">Color</a><br>Read-only</td><td>The color blue</td></tr>
<tr><td>cyan</td><td><a href="color.md">Color</a><br>Read-only</td><td>The color cyan</td></tr>
<tr><td>gray</td><td><a href="color.md">Color</a><br>Read-only</td><td>The color gray</td></tr>
<tr><td>green</td><td><a href="color.md">Color</a><br>Read-only</td><td>The color green</td></tr>
<tr><td>grey</td><td><a href="color.md">Color</a><br>Read-only</td><td>The color grey</td></tr>
<tr><td>magenta</td><td><a href="color.md">Color</a><br>Read-only</td><td>The color magenta</td></tr>
<tr><td>red</td><td><a href="color.md">Color</a><br>Read-only</td><td>The color red</td></tr>
<tr><td>white</td><td><a href="color.md">Color</a><br>Read-only</td><td>The color white</td></tr>
<tr><td>yellow</td><td><a href="color.md">Color</a><br>Read-only</td><td>The color yellow</td></tr>
</tbody></table>



## Instance Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>this[index]</td><td>number<br>Read/Write</td><td>The color component at the specified index</td></tr>
<tr><td>r</td><td>number<br>Read-only</td><td>The red component</td></tr>
<tr><td>g</td><td>number<br>Read-only</td><td>The green component</td></tr>
<tr><td>b</td><td>number<br>Read-only</td><td>The blue component</td></tr>
<tr><td>a</td><td>number<br>Read-only</td><td>The alpha component</td></tr>
<tr><td>grayscale</td><td>number<br>Read-only</td><td>The grayscale value</td></tr>
<tr><td>gamma</td><td><a href="color.md">Color</a><br>Read-only</td><td>The gamma color space representation</td></tr>
<tr><td>linear</td><td><a href="color.md">Color</a><br>Read-only</td><td>The linear color space representation</td></tr>
<tr><td>maxColorComponent</td><td>number<br>Read-only</td><td>The maximum color component value</td></tr>
<tr><td>html</td><td>string<br>Read-only</td><td>The HTML hex string of the color (for example "A4D0FF")</td></tr>
<tr><td>greyscale</td><td>number<br>Read-only</td><td>The grayscale value</td></tr>
<tr><td>hsv</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>The hue, saturation and brightess</td></tr>
</tbody></table>



## Class Methods

        
### Color:New(r, g, b)

Creates a new instance of a color with the specified RGB values

**Returns:** <a href="color.md">Color</a>  (instance of the Color)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>r</td><td>number</td><td>0</td><td>The red component of the color. Default is 0</td></tr>
<tr><td>g</td><td>number</td><td>0</td><td>The green component of the color. Default is 0</td></tr>
<tr><td>b</td><td>number</td><td>0</td><td>The blue component of the color. Default is 0</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myColor = Color:New(0.5, 0, 1)</strong></code></pre>




### Color:New(html)

Creates a new instance of the Color with the color parsed from the specified HTML string

**Returns:** <a href="color.md">Color</a>  (Returns the color. Invalid html inputs return bright magenta (r=1, g=0, b=1))


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>html</td><td>string</td><td></td><td>The HTML string representing the color</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myColor = Color:New("D3B322")</strong></code></pre>




### Color:Lerp(a, b, t)

Performs a linear interpolation between two colors

**Returns:** <a href="color.md">Color</a>  (The interpolated color)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="color.md">Color</a></td><td></td><td>The start color</td></tr>
<tr><td>b</td><td><a href="color.md">Color</a></td><td></td><td>The end color</td></tr>
<tr><td>t</td><td>number</td><td></td><td>The interpolation value. Should be between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newColor = Color:Lerp(color1, color2, 0.5)</strong></code></pre>




### Color:LerpUnclamped(a, b, t)

Performs a linear interpolation between two colors without clamping the interpolation parameter

**Returns:** <a href="color.md">Color</a>  (color)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="color.md">Color</a></td><td></td><td>The start color</td></tr>
<tr><td>b</td><td><a href="color.md">Color</a></td><td></td><td>The end color</td></tr>
<tr><td>t</td><td>number</td><td></td><td>The interpolation value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newColor = Color:Lerp(color1, color2, 1.5)</strong></code></pre>




### Color:HsvToRgb(h, s, v)

Converts an HSV color to an RGB color

**Returns:** <a href="color.md">Color</a>  (color)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>h</td><td>number</td><td></td><td>The hue value. Should be between 0 and 1</td></tr>
<tr><td>s</td><td>number</td><td></td><td>The saturation value. Should be between 0 and 1</td></tr>
<tr><td>v</td><td>number</td><td></td><td>The value value. Should be between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newColor = Color:HsvToRgb(0.5, 0.9, 0.5)</strong></code></pre>




### Color:HsvToRgb(hsv)

Converts an HSV Vector3 to an RGB color

**Returns:** <a href="color.md">Color</a>  (color)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>hsv</td><td><a href="vector3.md">Vector3</a></td><td></td><td>A Vector3 with xyz representing hsv. All values between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newColor = Color:HsvToRgb(myHsv)</strong></code></pre>



    

## Instance Methods

        
### color:Add(other)

Adds the specified color to this color

**Returns:** <a href="color.md">Color</a>  (color)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="color.md">Color</a></td><td></td><td>The color to add</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newColor = color1:Add(color2)</strong></code></pre>




### color:Add(r, g, b)

Adds the specified RGB values to this color

**Returns:** <a href="color.md">Color</a>  (color)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>r</td><td>number</td><td></td><td>The red component value to add</td></tr>
<tr><td>g</td><td>number</td><td></td><td>The green component value to add</td></tr>
<tr><td>b</td><td>number</td><td></td><td>The blue component value to add</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newColor = color1:Add(0.5, 0, 0.1)</strong></code></pre>




### color:Subtract(other)

Subtracts the specified color from this color

**Returns:** <a href="color.md">Color</a>  (color)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="color.md">Color</a></td><td></td><td>The color to subtract</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newColor = color1:Subtract(color2)</strong></code></pre>




### color:Subtract(r, g, b)

Subtracts the specified RGB values from this color

**Returns:** <a href="color.md">Color</a>  (color)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>r</td><td>number</td><td></td><td>The red component value to subtract</td></tr>
<tr><td>g</td><td>number</td><td></td><td>The green component value to subtract</td></tr>
<tr><td>b</td><td>number</td><td></td><td>The blue component value to subtract</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newColor = color1:Subtract(0.5, 0.25, 0)</strong></code></pre>




### color:Multiply(value)

Multiplies this color by the specified value

**Returns:** <a href="color.md">Color</a>  (color)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>value</td><td>number</td><td></td><td>The value to multiply</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newColor = color1:Multiply(0.5)</strong></code></pre>




### color:Multiply(r, g, b)

Multiplies this color by the specified RGB values

**Returns:** <a href="color.md">Color</a>  (color)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>r</td><td>number</td><td></td><td>The red component value to multiply</td></tr>
<tr><td>g</td><td>number</td><td></td><td>The green component value to multiply</td></tr>
<tr><td>b</td><td>number</td><td></td><td>The blue component value to multiply</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newColor = color1:Multiply(0.85, 0, 0)</strong></code></pre>




### color:Divide(value)

Divides this color by the specified value

**Returns:** <a href="color.md">Color</a>  (color)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>value</td><td>number</td><td></td><td>The value to divide</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newColor = color1:Divide(0.5)</strong></code></pre>




### color:NotEquals(other)

Determines whether this color is not equal to the specified color

**Returns:** boolean  (true if this color is not equal to the specified color; otherwise, false)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="color.md">Color</a></td><td></td><td>The color to compare</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>if color1:NotEquals(color2) then print("colors are different") end</strong></code></pre>




### color:NotEquals(r, g, b)

Determines whether this color is not equal to the specified RGB values

**Returns:** boolean  (true if this color is not equal to the specified RGB values; otherwise, false)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>r</td><td>number</td><td></td><td>The red component value to compare</td></tr>
<tr><td>g</td><td>number</td><td></td><td>The green component value to compare</td></tr>
<tr><td>b</td><td>number</td><td></td><td>The blue component value to compare</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>if color1:NotEquals(0, 1, 0) then print("color is not green") end</strong></code></pre>



    
