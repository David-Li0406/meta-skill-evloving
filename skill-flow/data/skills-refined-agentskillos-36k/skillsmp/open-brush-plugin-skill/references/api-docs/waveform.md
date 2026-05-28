
# Waveform

## Summary
Functions to generate a variety of waveforms



## Class Methods

        
### Waveform:Sine(time, frequency)

Returns the value of a sine wave at the given time

**Returns:** number  (The value of the wave sampled at the given time)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to sample the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Waveform.Sine(0, 6)</strong></code></pre>




### Waveform:Cosine(time, frequency)

Returns the value of a cosine wave at the given time

**Returns:** number  (The value of the wave sampled at the given time)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to sample the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Waveform.Cosine(0, 6)</strong></code></pre>




### Waveform:Triangle(time, frequency)

Returns the value of a triangle wave at the given time

**Returns:** number  (The value of the wave sampled at the given time)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to sample the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Waveform.Triangle(0, 6)</strong></code></pre>




### Waveform:Sawtooth(time, frequency)

Returns the value of a sawtooth wave at the given time

**Returns:** number  (The value of the wave sampled at the given time)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to sample the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Waveform.Sawtooth(0, 6)</strong></code></pre>




### Waveform:Square(time, frequency)

Returns the value of a square wave at the given time

**Returns:** number  (The value of the wave sampled at the given time)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to sample the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Waveform.Square(0, 6)</strong></code></pre>




### Waveform:Pulse(time, frequency, pulseWidth)

Returns the value of a pulse wave with a specified pulse width at the given time, frequency

**Returns:** number  (The value of the wave sampled at the given time)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to sample the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr>
<tr><td>pulseWidth</td><td>number</td><td></td><td>The width of the pulse</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Waveform.Pulse(0, 6, 0.2)</strong></code></pre>




### Waveform:Exponent(time, frequency)

Returns the value of an exponential wave at the given time

**Returns:** number  (The value of the wave sampled at the given time)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to sample the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Waveform.Exponent(0, 6)</strong></code></pre>




### Waveform:Power(time, frequency, power)

Returns the value of a power wave at the given time, frequency, and power

**Returns:** number  (The value of the wave sampled at the given time)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to sample the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr>
<tr><td>power</td><td>number</td><td></td><td>The power exponent of the wave</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Waveform.Power(0, 6, 2)</strong></code></pre>




### Waveform:Parabolic(time, frequency)

Returns the value of a parabolic wave at the given time

**Returns:** number  (The value of the wave sampled at the given time)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to sample the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Waveform.Parabolic(0, 6)</strong></code></pre>




### Waveform:ExponentialSawtooth(time, frequency, exponent)

Returns the value of an exponential sawtooth wave with the specified exponent at the given time, frequency

**Returns:** number  (The value of the wave sampled at the given time)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to sample the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr>
<tr><td>exponent</td><td>number</td><td></td><td>The exponent of the wave</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Waveform.ExponentialSawtooth(0, 6, 2)</strong></code></pre>




### Waveform:PerlinNoise(time, frequency)

Returns the value of a perlin noise function at the given time

**Returns:** number  (The value of the wave sampled at the given time)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to sample the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Waveform.PerlinNoise(0, 6)</strong></code></pre>




### Waveform:WhiteNoise()

Returns the value of a white noise function

**Returns:** number  (The value of the wave sampled at the given time)




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Waveform.WhiteNoise()</strong></code></pre>




### Waveform:BrownNoise(previous)

Returns the value of a brown noise function

**Returns:** number  (The value of the wave sampled at the given time)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>previous</td><td>number</td><td></td><td>The previous calculated value to feed back into the function</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Waveform.BrownNoise(previousValue)</strong></code></pre>




### Waveform:BlueNoise(previous)

Returns the value of a blue noise function

**Returns:** number  (The value of the wave sampled at the given time)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>previous</td><td>number</td><td></td><td>The previous calculated value to feed back into the function</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>value = Waveform.BlueNoise(previousValue)</strong></code></pre>




### Waveform:Sine(time, frequency, duration, sampleRate, amplitude)

Returns a sine wave with the given frequency, duration, and sample rate

**Returns:** number[]  (An array of float values)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to start sampling the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr>
<tr><td>duration</td><td>number</td><td></td><td>The duration of samples to generate</td></tr>
<tr><td>sampleRate</td><td>number</td><td></td><td>The sample rate of the generated waveform</td></tr>
<tr><td>amplitude</td><td>number</td><td>1</td><td>The amplitude of the generated waveform</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>wave = Waveform:Sine(0, 440, 1, 44100, 0.5)</strong></code></pre>




### Waveform:Cosine(time, frequency, duration, sampleRate, amplitude)

Returns a cosine wave with the given frequency, duration, and sample rate

**Returns:** number[]  (An array of float values)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to start sampling the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr>
<tr><td>duration</td><td>number</td><td></td><td>The duration of samples to generate</td></tr>
<tr><td>sampleRate</td><td>number</td><td></td><td>The sample rate of the generated waveform</td></tr>
<tr><td>amplitude</td><td>number</td><td>1</td><td>The amplitude of the generated waveform</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>wave = Waveform:Cosine(0, 440, 1, 44100, 0.5)</strong></code></pre>




### Waveform:Triangle(time, frequency, duration, sampleRate, amplitude)

Returns a triangle wave with the given frequency, duration, and sample rate

**Returns:** number[]  (An array of float values)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to start sampling the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr>
<tr><td>duration</td><td>number</td><td></td><td>The duration of samples to generate</td></tr>
<tr><td>sampleRate</td><td>number</td><td></td><td>The sample rate of the generated waveform</td></tr>
<tr><td>amplitude</td><td>number</td><td>1</td><td>The amplitude of the generated waveform</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>wave = Waveform:Triangle(0, 440, 1, 44100, 0.5)</strong></code></pre>




### Waveform:Sawtooth(time, frequency, duration, sampleRate, amplitude)

Returns a sawtooth wave with the given frequency, duration, and sample rate

**Returns:** number[]  (An array of float values)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to start sampling the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr>
<tr><td>duration</td><td>number</td><td></td><td>The duration of samples to generate</td></tr>
<tr><td>sampleRate</td><td>number</td><td></td><td>The sample rate of the generated waveform</td></tr>
<tr><td>amplitude</td><td>number</td><td>1</td><td>The amplitude of the generated waveform</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>wave = Waveform:Sawtooth(0, 440, 1, 44100, 0.5)</strong></code></pre>




### Waveform:Square(time, frequency, duration, sampleRate, amplitude)

Returns a square wave with the given frequency, duration, and sample rate

**Returns:** number[]  (An array of float values)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to start sampling the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr>
<tr><td>duration</td><td>number</td><td></td><td>The duration of samples to generate</td></tr>
<tr><td>sampleRate</td><td>number</td><td></td><td>The sample rate of the generated waveform</td></tr>
<tr><td>amplitude</td><td>number</td><td>1</td><td>The amplitude of the generated waveform</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>wave = Waveform:Square(0, 440, 1, 44100, 0.5)</strong></code></pre>




### Waveform:Exponent(time, frequency, duration, sampleRate, amplitude)

Returns an exponential wave with the given frequency, duration, and sample rate

**Returns:** number[]  (An array of float values)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to start sampling the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr>
<tr><td>duration</td><td>number</td><td></td><td>The duration of samples to generate</td></tr>
<tr><td>sampleRate</td><td>number</td><td></td><td>The sample rate of the generated waveform</td></tr>
<tr><td>amplitude</td><td>number</td><td>1</td><td>The amplitude of the generated waveform</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>wave = Waveform:Exponent(0, 440, 1, 44100, 0.5)</strong></code></pre>




### Waveform:Parabolic(time, frequency, duration, sampleRate, amplitude)

Returns a parabolic wave with the given frequency, duration, and sample rate

**Returns:** number[]  (An array of float values)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to start sampling the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr>
<tr><td>duration</td><td>number</td><td></td><td>The duration of samples to generate</td></tr>
<tr><td>sampleRate</td><td>number</td><td></td><td>The sample rate of the generated waveform</td></tr>
<tr><td>amplitude</td><td>number</td><td>1</td><td>The amplitude of the generated waveform</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>wave = Waveform:Parabolic(0, 440, 1, 44100, 0.5)</strong></code></pre>




### Waveform:Pulse(time, frequency, pulseWidth, duration, sampleRate, amplitude)

Returns a pulse wave with the given frequency, pulse width, duration, and sample rate

**Returns:** number[]  (An array of float values)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to start sampling the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr>
<tr><td>pulseWidth</td><td>number</td><td></td><td>The width of the pulse</td></tr>
<tr><td>duration</td><td>number</td><td></td><td>The duration of samples to generate</td></tr>
<tr><td>sampleRate</td><td>number</td><td></td><td>The sample rate of the generated waveform</td></tr>
<tr><td>amplitude</td><td>number</td><td>1</td><td>The amplitude of the generated waveform</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>wave = Waveform:Pulse(0, 440, 0.5, 1, 44100, 0.5)</strong></code></pre>




### Waveform:Power(time, frequency, power, duration, sampleRate, amplitude)

Returns a power wave with the given frequency, power, duration, and sample rate

**Returns:** number[]  (An array of float values)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to start sampling the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr>
<tr><td>power</td><td>number</td><td></td><td>The power exponent of the wave</td></tr>
<tr><td>duration</td><td>number</td><td></td><td>The duration of samples to generate</td></tr>
<tr><td>sampleRate</td><td>number</td><td></td><td>The sample rate of the generated waveform</td></tr>
<tr><td>amplitude</td><td>number</td><td>1</td><td>The amplitude of the generated waveform</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>wave = Waveform:Power(0, 440, 0.5, 1, 44100, 0.5)</strong></code></pre>




### Waveform:ExponentialSawtoothWave(time, frequency, exponent, duration, sampleRate, amplitude)

Returns an exponential sawtooth wave with the given frequency, exponent, duration, and sample rate

**Returns:** number[]  (An array of float values)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to start sampling the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr>
<tr><td>exponent</td><td>number</td><td></td><td>The exponent of the wave</td></tr>
<tr><td>duration</td><td>number</td><td></td><td>The duration of samples to generate</td></tr>
<tr><td>sampleRate</td><td>number</td><td></td><td>The sample rate of the generated waveform</td></tr>
<tr><td>amplitude</td><td>number</td><td>1</td><td>The amplitude of the generated waveform</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>wave = Waveform:ExponentialSawtooth(0, 440, 0.5, 1, 44100, 0.5)</strong></code></pre>




### Waveform:PerlinNoise(time, frequency, duration, sampleRate, amplitude)

Returns a perlin noise wave with the given frequency, duration, and sample rate

**Returns:** number[]  (An array of float values)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>time</td><td>number</td><td></td><td>The time to start sampling the waveform at</td></tr>
<tr><td>frequency</td><td>number</td><td></td><td>The frequency of the wave</td></tr>
<tr><td>duration</td><td>number</td><td></td><td>The duration of samples to generate</td></tr>
<tr><td>sampleRate</td><td>number</td><td></td><td>The sample rate of the generated waveform</td></tr>
<tr><td>amplitude</td><td>number</td><td>1</td><td>The amplitude of the generated waveform</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>wave = Waveform:PerlinNoise(0, 440, 1, 44100, 0.5)</strong></code></pre>




### Waveform:WhiteNoise(duration, sampleRate, amplitude)

Returns a white noise wave with the given duration and sample rate

**Returns:** number[]  (An array of float values)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>duration</td><td>number</td><td></td><td>The duration of samples to generate</td></tr>
<tr><td>sampleRate</td><td>number</td><td></td><td>The sample rate of the generated waveform</td></tr>
<tr><td>amplitude</td><td>number</td><td>1</td><td>The amplitude of the generated waveform</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>wave = Waveform:WhiteNoise(1, 44100, 0.5)</strong></code></pre>




### Waveform:BrownNoise(duration, sampleRate, amplitude)

Returns a brown noise wave with the given duration and sample rate

**Returns:** number[]  (An array of float values)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>duration</td><td>number</td><td></td><td>The duration of samples to generate</td></tr>
<tr><td>sampleRate</td><td>number</td><td></td><td>The sample rate of the generated waveform</td></tr>
<tr><td>amplitude</td><td>number</td><td>1</td><td>The amplitude of the generated waveform</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>wave = Waveform:BrownNoise(1, 44100, 0.5)</strong></code></pre>




### Waveform:BlueNoise(duration, sampleRate, amplitude)

Returns a blue noise wave with the given duration and sample rate

**Returns:** number[]  (An array of float values)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>duration</td><td>number</td><td></td><td>The duration of samples to generate</td></tr>
<tr><td>sampleRate</td><td>number</td><td></td><td>The sample rate of the generated waveform</td></tr>
<tr><td>amplitude</td><td>number</td><td>1</td><td>The amplitude of the generated waveform</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>wave = Waveform:BlueNoise(1, 44100, 0.5)</strong></code></pre>



    

