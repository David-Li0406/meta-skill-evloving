
# Timer

## Summary
Timers can be used to call functions at a predetermined time (or multiple times)



## Class Methods

        
### Timer:Set(fn, interval, delay, repeats)

Sets up a function to be called in the future

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>fn</td><td>function</td><td></td><td>The function to call</td></tr>
<tr><td>interval</td><td>number</td><td></td><td>How long to wait inbetween repeated calls</td></tr>
<tr><td>delay</td><td>number</td><td>0</td><td>How long to wait until the first call</td></tr>
<tr><td>repeats</td><td>number</td><td>-1</td><td>The number of times to call the function. A value of -1 means "run forever"</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Timer:Set(myFunction, 1, 0, 5)</strong></code></pre>




### Timer:Unset(fn)

Removes a future function timer

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>fn</td><td>function</td><td></td><td>The function to remove</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Timer:Unset(myFunction)</strong></code></pre>



    

