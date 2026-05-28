
# Svg

## Summary
Functions related to SVG images



## Class Methods

        
### Svg:ParsePathString(svgPath)

Parses an SVG path string

**Returns:** <a href="pathlist.md">PathList</a>  (Returns a PathList representing the parsed SVG path)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>svgPath</td><td>string</td><td></td><td>The SVG path string to parse</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPaths = SVG:ParsePathString('M 100 100 L 200 200')</strong></code></pre>




### Svg:ParseDocument(svg, offsetPerPath, includeColors)

Parses an SVG document

**Returns:** <a href="pathlist.md">PathList</a>  (Returns a PathList representing the parsed SVG document)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>svg</td><td>string</td><td></td><td>A text string that is valid SVG document</td></tr>
<tr><td>offsetPerPath</td><td>number</td><td>0</td><td>Each path can be lifted to form a layered result</td></tr>
<tr><td>includeColors</td><td>boolean</td><td>false</td><td>Whether the colors from the SVG are used</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPaths = SVG:ParseDocument('<svg>...</svg>')</strong></code></pre>




### Svg:DrawPathString(svgPath, tr)

Draws an SVG path string

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>svgPath</td><td>string</td><td></td><td>The SVG path string to draw</td></tr>
<tr><td>tr</td><td><a href="transform.md">Transform</a></td><td></td><td>The transform to apply to the result</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Svg:DrawPathString('M 100 100 L 200 200')</strong></code></pre>




### Svg:DrawDocument(svg, tr, includeColors)

Draws an SVG document

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>svg</td><td>string</td><td></td><td>A text string that is a valid SVG document</td></tr>
<tr><td>tr</td><td><a href="transform.md">Transform</a></td><td></td><td>The transform (position, rotation and scale) to apply to the result</td></tr>
<tr><td>includeColors</td><td>boolean</td><td>false</td><td>Whether to use the colors from the SVG document</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Svg:Draw('<svg>...</svg>')</strong></code></pre>



    

