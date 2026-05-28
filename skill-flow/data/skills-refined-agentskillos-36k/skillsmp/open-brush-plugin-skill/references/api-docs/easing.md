
# Easing

## Summary
Each easing function takes a value between 0 and 1 and modifies it to speed up or slow down at either end



## Class Methods

        
### Easing:Linear(t)

Linear easing function

**Returns:** number  (The input is returned unchanged)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:Linear(value)</strong></code></pre>




### Easing:InQuad(t)

InQuad easing function

**Returns:** number  (The value smoothed in the in direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InQuad(value)</strong></code></pre>




### Easing:OutQuad(t)

OutQuad easing function

**Returns:** number  (The value smoothed in the out direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:OutQuad(value)</strong></code></pre>




### Easing:InOutQuad(t)

InOutQuad easing function

**Returns:** number  (The value smoothed in and out)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InOutQuad(value)</strong></code></pre>




### Easing:InCubic(t)

InCubic easing function

**Returns:** number  (The value smoothed in the in direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InCubic(value)</strong></code></pre>




### Easing:OutCubic(t)

OutCubic easing function

**Returns:** number  (The value smoothed in the out direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:OutCubic(value)</strong></code></pre>




### Easing:InOutCubic(t)

InOutCubic easing function

**Returns:** number  (The value smoothed in and out)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InOutCubic(value)</strong></code></pre>




### Easing:InQuart(t)

InQuart easing function

**Returns:** number  (The value smoothed in the in direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InQuart(value)</strong></code></pre>




### Easing:OutQuart(t)

OutQuart easing function

**Returns:** number  (The value smoothed in the out direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:OutQuart(value)</strong></code></pre>




### Easing:InOutQuart(t)

InQuart easing function

**Returns:** number  (The value smoothed in and out)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InQuart(value)</strong></code></pre>




### Easing:InQuint(t)

InQuint easing function

**Returns:** number  (The value smoothed in the in direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InQuint(value)</strong></code></pre>




### Easing:OutQuint(t)

OutQuint easing function

**Returns:** number  (The value smoothed in the out direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:OutQuint(value)</strong></code></pre>




### Easing:InOutQuint(t)

InOutQuint easing function

**Returns:** number  (The value smoothed in and out)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InOutQuint(value)</strong></code></pre>




### Easing:InSine(t)

InSine easing function

**Returns:** number  (The value smoothed in the in direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InSine(value)</strong></code></pre>




### Easing:OutSine(t)

OutSine easing function

**Returns:** number  (The value smoothed in the out direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:OutSine(value)</strong></code></pre>




### Easing:InOutSine(t)

InOutSine easing function

**Returns:** number  (The value smoothed in and out)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InOutSine(value)</strong></code></pre>




### Easing:InExpo(t)

InExpo easing function

**Returns:** number  (The value smoothed in the in direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InExpo(value)</strong></code></pre>




### Easing:OutExpo(t)

OutExpo easing function

**Returns:** number  (The value smoothed in the out direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:OutExpo(value)</strong></code></pre>




### Easing:InOutExpo(t)

InOutExpo easing function

**Returns:** number  (The value smoothed in and out)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InOutExpo(value)</strong></code></pre>




### Easing:InCirc(t)

InCirc easing function

**Returns:** number  (The value smoothed in the in direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InCirc(value)</strong></code></pre>




### Easing:OutCirc(t)

OutCirc easing function

**Returns:** number  (The value smoothed in the out direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:OutCirc(value)</strong></code></pre>




### Easing:InOutCirc(t)

InOutCirc easing function

**Returns:** number  (The value smoothed in and out)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InOutCirc(value)</strong></code></pre>




### Easing:InElastic(t)

InElastic easing function

**Returns:** number  (The value smoothed in the in direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InElastic(value)</strong></code></pre>




### Easing:OutElastic(t)

OutElastic easing function

**Returns:** number  (The value smoothed in the out direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:OutElastic(value)</strong></code></pre>




### Easing:InOutElastic(t)

InOutElastic easing function

**Returns:** number  (The value smoothed in and out)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InOutElastic(value)</strong></code></pre>




### Easing:InBack(t)

InBack easing function

**Returns:** number  (The value smoothed in the in direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InBack(value)</strong></code></pre>




### Easing:OutBack(t)

OutBack easing function

**Returns:** number  (The value smoothed in the out direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:OutBack(value)</strong></code></pre>




### Easing:InOutBack(t)

InOutBack easing function

**Returns:** number  (The value smoothed in and out)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InOutBack(value)</strong></code></pre>




### Easing:InBounce(t)

InBounce easing function

**Returns:** number  (The value smoothed in the in direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InBounce(value)</strong></code></pre>




### Easing:OutBounce(t)

OutBounce easing function

**Returns:** number  (The value smoothed in the out direction only)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:OutBounce(value)</strong></code></pre>




### Easing:InOutBounce(t)

InOutBounce easing function

**Returns:** number  (The value smoothed in and out)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>t</td><td>number</td><td></td><td>The input value between 0 and 1</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Easing:InOutBounce(value)</strong></code></pre>



    

