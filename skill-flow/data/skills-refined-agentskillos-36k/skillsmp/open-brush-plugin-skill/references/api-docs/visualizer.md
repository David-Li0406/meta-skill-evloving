
# Visualizer

## Summary
Settings and controls for audio visualization mode

## Class Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>sampleRate</td><td>number<br>Read-only</td><td>The current audio sample rate</td></tr>
<tr><td>duration</td><td>number<br>Read-only</td><td>The current duration of the audio buffer</td></tr>
</tbody></table>




## Class Methods

        
### Visualizer:EnableScripting()

Enables scripted access to the audio visualization buffer

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Visualizer.EnableScripting()</strong></code></pre>




### Visualizer:DisableScripting()

Disables scripted access to the audio visualization buffer

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Visualizer.DisableScripting()</strong></code></pre>




### Visualizer:SetWaveform(data)

Passes the given waveform data to the audio visualizer

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>data</td><td>number[]</td><td></td><td>An array of numbers representing the waveform</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Visualizer.SetWaveform(data)</strong></code></pre>




### Visualizer:SetFft(data1, data2, data3, data4)

Passes the given FFT data to the audio visualizer

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>data1</td><td>number[]</td><td></td><td>An array of numbers representing first FFT band</td></tr>
<tr><td>data2</td><td>number[]</td><td></td><td>An array of numbers representing second FFT band</td></tr>
<tr><td>data3</td><td>number[]</td><td></td><td>An array of numbers representing third FFT band</td></tr>
<tr><td>data4</td><td>number[]</td><td></td><td>An array of numbers representing fourth FFT band</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Visualizer.SetFft(data1, data2, data3, data4)</strong></code></pre>




### Visualizer:SetBeats(x, y, z, w)

Passes the given beat data to the audio visualizer

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The first beat value</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The second beat value</td></tr>
<tr><td>z</td><td>number</td><td></td><td>The third beat value</td></tr>
<tr><td>w</td><td>number</td><td></td><td>The fourth beat value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Visualizer.SetBeats(x, y, z, w)</strong></code></pre>




### Visualizer:SetBeatAccumulators(x, y, z, w)

Passes the given beat accumulator data to the audio visualizer

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The first beat accumulator value</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The second beat accumulator value</td></tr>
<tr><td>z</td><td>number</td><td></td><td>The third beat accumulator value</td></tr>
<tr><td>w</td><td>number</td><td></td><td>The fourth beat accumulator value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Visualizer.SetBeatAccumulators(x, y, z, w)</strong></code></pre>




### Visualizer:SetBandPeak(peak)

Passes the given band peak data to the audio visualizer

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>peak</td><td>number</td><td></td><td>The peak value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Visualizer.SetBandPeak(0.5)</strong></code></pre>



    

