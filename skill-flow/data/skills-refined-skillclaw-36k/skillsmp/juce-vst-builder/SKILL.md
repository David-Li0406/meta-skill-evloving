---
name: juce-vst-builder
description: >
  Generate complete JUCE VST3/AU audio plugins from natural language descriptions.
  Use when the user wants to create a synthesizer, audio effect, or audio plugin.
  Triggers: "create a VST", "build a plugin", "make a synth", "audio effect",
  "JUCE plugin", "VST3", "AU plugin", "Ableton plugin", "DAW plugin".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# JUCE VST3 Plugin Builder

## Overview

This skill generates production-ready JUCE VST3/AU audio plugins. It creates complete, buildable projects with proper CMake configuration, DSP architecture, parameter management, and UI.

## When to Use

- User asks to create a VST, AU, or audio plugin
- User describes a synthesizer or audio effect they want to build
- User mentions JUCE, audio processing, or DAW plugins
- User wants to generate sound/audio software

## Environment Requirements

- **JUCE**: Version 8.0.3+ (auto-fetched via CMake FetchContent)
- **CMake**: Version 3.22+
- **C++ Compiler**: Clang (macOS) or GCC (Linux) with C++17 support
- **Build Generator**: Ninja recommended (`brew install ninja`)

## Project Generation Workflow

### Step 1: Understand the Plugin Type

Ask clarifying questions if needed:

1. **Plugin Category**:
   - Synthesizer (generates sound from MIDI)
   - Audio Effect (processes incoming audio)
   - Generator (produces audio without MIDI input)
   - MIDI Effect (transforms MIDI data)

2. **DSP Requirements**:
   - Oscillators (sine, saw, square, triangle, wavetable, FM)
   - Filters (LP, HP, BP, state-variable, ladder, Moog-style)
   - Effects (reverb, delay, chorus, distortion, wavefolder)
   - Modulation (LFOs, envelopes, ADSR)
   - Spatial (stereo width, panning, Haas effect)

3. **UI Style**:
   - Minimal (basic knobs and labels)
   - Standard (organized panels with visualizers)
   - Vintage/Skeuomorphic (hardware-inspired)

### Step 2: Generate Project Structure

Create this directory structure:

```
{plugin-name}/
├── CMakeLists.txt              # Build configuration
├── CLAUDE.md                   # Development guidelines
├── Source/
│   ├── PluginProcessor.h       # Audio engine interface
│   ├── PluginProcessor.cpp     # Audio processing implementation
│   ├── PluginEditor.h          # UI interface
│   ├── PluginEditor.cpp        # UI implementation
│   ├── Parameters/
│   │   ├── ParameterIDs.h      # Parameter constants
│   │   └── ParameterLayout.h/cpp
│   ├── DSP/
│   │   ├── {EngineClass}.h/cpp # Main DSP coordinator
│   │   ├── Oscillators/        # Sound generators
│   │   ├── Filters/            # Audio filters
│   │   ├── Effects/            # Audio effects
│   │   ├── Envelopes/          # ADSR, AR envelopes
│   │   └── Modulation/         # LFOs, modulators
│   ├── UI/
│   │   ├── {Name}LookAndFeel.h/cpp  # Custom styling
│   │   └── Components/         # Custom UI components
│   └── MIDI/                   # MIDI handling (if needed)
│       └── MIDIHandler.h/cpp
└── Resources/
    └── {Name}.icns             # App icon (optional)
```

### Step 3: Generate Files in Order

1. **CMakeLists.txt** - Build configuration first
2. **ParameterIDs.h** - Define all parameters
3. **ParameterLayout.cpp** - APVTS configuration
4. **DSP modules** - Oscillators, filters, effects
5. **Main DSP Engine** - Coordinates all DSP
6. **PluginProcessor** - Connects APVTS to DSP
7. **UI components** - Custom knobs, visualizers
8. **LookAndFeel** - Visual styling
9. **PluginEditor** - Assembles the UI

### Step 4: Build the Plugin

```bash
# Configure
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release

# Build
cmake --build build --config Release

# Output location
# VST3: build/{Name}_artefacts/Release/VST3/{Name}.vst3
# AU:   build/{Name}_artefacts/Release/AU/{Name}.component
```

---

## Template Reference

### CMakeLists.txt Template

```cmake
cmake_minimum_required(VERSION 3.22)
project({PLUGIN_NAME} VERSION 1.0.0 LANGUAGES C CXX OBJC OBJCXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Fetch JUCE
include(FetchContent)
FetchContent_Declare(
    JUCE
    GIT_REPOSITORY https://github.com/juce-framework/JUCE.git
    GIT_TAG 8.0.3
    GIT_SHALLOW TRUE
)
FetchContent_MakeAvailable(JUCE)

# Plugin configuration
juce_add_plugin({PLUGIN_NAME}
    COMPANY_NAME "{COMPANY_NAME}"
    BUNDLE_ID "com.{company}.{pluginname}"
    IS_SYNTH {IS_SYNTH}                    # TRUE for synths
    NEEDS_MIDI_INPUT {NEEDS_MIDI}          # TRUE for synths/MIDI effects
    NEEDS_MIDI_OUTPUT FALSE
    IS_MIDI_EFFECT FALSE
    EDITOR_WANTS_KEYBOARD_FOCUS TRUE
    COPY_PLUGIN_AFTER_BUILD TRUE
    PLUGIN_MANUFACTURER_CODE {MFRC}        # 4-char code
    PLUGIN_CODE {PLGC}                     # 4-char code
    FORMATS AU VST3 Standalone
    PRODUCT_NAME "{PRODUCT_NAME}"
)

# Source files
target_sources({PLUGIN_NAME} PRIVATE
    Source/PluginProcessor.cpp
    Source/PluginEditor.cpp
    Source/Parameters/ParameterLayout.cpp
    Source/DSP/{ENGINE_NAME}.cpp
    Source/UI/{NAME}LookAndFeel.cpp
    # Add more source files as needed
)

target_include_directories({PLUGIN_NAME} PRIVATE Source)

target_compile_definitions({PLUGIN_NAME} PUBLIC
    JUCE_WEB_BROWSER=0
    JUCE_USE_CURL=0
    JUCE_VST3_CAN_REPLACE_VST2=0
    JUCE_DISPLAY_SPLASH_SCREEN=0
)

target_link_libraries({PLUGIN_NAME} PRIVATE
    juce::juce_audio_utils
    juce::juce_audio_processors
    juce::juce_dsp
    juce::juce_gui_basics
    juce::juce_recommended_config_flags
    juce::juce_recommended_lto_flags
    juce::juce_recommended_warning_flags
)
```

### PluginProcessor Template Pattern

```cpp
class {Name}AudioProcessor : public juce::AudioProcessor
{
public:
    {Name}AudioProcessor();
    ~{Name}AudioProcessor() override;

    void prepareToPlay(double sampleRate, int samplesPerBlock) override;
    void releaseResources() override;
    void processBlock(juce::AudioBuffer<float>&, juce::MidiBuffer&) override;

    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override { return true; }

    const juce::String getName() const override;
    bool acceptsMidi() const override;
    bool producesMidi() const override;
    double getTailLengthSeconds() const override;

    int getNumPrograms() override;
    int getCurrentProgram() override;
    void setCurrentProgram(int) override;
    const juce::String getProgramName(int) override;
    void changeProgramName(int, const juce::String&) override;

    void getStateInformation(juce::MemoryBlock&) override;
    void setStateInformation(const void*, int) override;

    juce::AudioProcessorValueTreeState apvts;

private:
    // DSP engine
    {Engine}Engine engine;

    // Atomic parameter pointers for real-time access
    std::atomic<float>* param1 = nullptr;
    // ... more parameters

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR({Name}AudioProcessor)
};
```

### Parameter System Pattern

```cpp
// ParameterIDs.h
namespace ParameterIDs
{
    // Use inline const juce::String for each parameter
    inline const juce::String masterVolume { "masterVolume" };
    inline const juce::String filterCutoff { "filterCutoff" };
    // etc.
}

// ParameterLayout.cpp
juce::AudioProcessorValueTreeState::ParameterLayout createParameterLayout()
{
    std::vector<std::unique_ptr<juce::RangedAudioParameter>> params;

    // Float parameter with skew
    params.push_back(std::make_unique<juce::AudioParameterFloat>(
        juce::ParameterID { ParameterIDs::filterCutoff, 1 },
        "Filter Cutoff",
        juce::NormalisableRange<float>(20.0f, 20000.0f, 0.1f, 0.3f), // skew 0.3 = logarithmic
        1000.0f,
        juce::String(),
        juce::AudioProcessorParameter::genericParameter,
        [](float value, int) { return juce::String(value, 1) + " Hz"; }
    ));

    // Choice parameter
    params.push_back(std::make_unique<juce::AudioParameterChoice>(
        juce::ParameterID { ParameterIDs::waveform, 1 },
        "Waveform",
        juce::StringArray { "Sine", "Triangle", "Saw", "Square" },
        0  // default index
    ));

    // Bool parameter
    params.push_back(std::make_unique<juce::AudioParameterBool>(
        juce::ParameterID { ParameterIDs::bypassEnabled, 1 },
        "Bypass",
        false
    ));

    return { params.begin(), params.end() };
}
```

---

## DSP Building Blocks

### Oscillators

**Basic Wavetable Oscillator:**
```cpp
class Oscillator
{
public:
    enum class Waveform { Sine, Triangle, Saw, Square };

    void prepare(double sampleRate) { this->sampleRate = sampleRate; }
    void setFrequency(float freq) { phaseIncrement = freq / sampleRate; }
    void setWaveform(Waveform w) { waveform = w; }

    float getNextSample()
    {
        float sample = 0.0f;
        switch (waveform)
        {
            case Waveform::Sine:     sample = std::sin(phase * juce::MathConstants<float>::twoPi); break;
            case Waveform::Triangle: sample = 2.0f * std::abs(2.0f * phase - 1.0f) - 1.0f; break;
            case Waveform::Saw:      sample = 2.0f * phase - 1.0f; break;
            case Waveform::Square:   sample = phase < 0.5f ? 1.0f : -1.0f; break;
        }
        phase += phaseIncrement;
        if (phase >= 1.0f) phase -= 1.0f;
        return sample;
    }

private:
    double sampleRate = 44100.0;
    float phase = 0.0f;
    float phaseIncrement = 0.0f;
    Waveform waveform = Waveform::Sine;
};
```

**PolyBLEP Anti-Aliased Oscillator:**
```cpp
static float polyBlep(float t, float dt)
{
    if (t < dt)
    {
        t /= dt;
        return t + t - t * t - 1.0f;
    }
    else if (t > 1.0f - dt)
    {
        t = (t - 1.0f) / dt;
        return t * t + t + t + 1.0f;
    }
    return 0.0f;
}

float getSawSample()
{
    float sample = 2.0f * phase - 1.0f;
    sample -= polyBlep(phase, phaseIncrement);
    return sample;
}
```

### Filters

**State Variable TPT Filter (Topology-Preserving Transform):**
```cpp
class SVTFilter
{
public:
    enum class Mode { LowPass, HighPass, BandPass };

    void prepare(double sampleRate) { this->sampleRate = sampleRate; }

    void setParameters(float cutoffHz, float resonance, Mode mode)
    {
        this->mode = mode;
        float g = std::tan(juce::MathConstants<float>::pi * cutoffHz / sampleRate);
        k = 1.0f / resonance;
        a1 = 1.0f / (1.0f + g * (g + k));
        a2 = g * a1;
        a3 = g * a2;
    }

    float process(float input)
    {
        float v3 = input - ic2eq;
        float v1 = a1 * ic1eq + a2 * v3;
        float v2 = ic2eq + a2 * ic1eq + a3 * v3;
        ic1eq = 2.0f * v1 - ic1eq;
        ic2eq = 2.0f * v2 - ic2eq;

        switch (mode)
        {
            case Mode::LowPass:  return v2;
            case Mode::HighPass: return input - k * v1 - v2;
            case Mode::BandPass: return v1;
        }
        return v2;
    }

private:
    double sampleRate = 44100.0;
    Mode mode = Mode::LowPass;
    float k = 1.0f, a1 = 0.0f, a2 = 0.0f, a3 = 0.0f;
    float ic1eq = 0.0f, ic2eq = 0.0f;
};
```

### Effects

**Stereo Delay with Feedback:**
```cpp
class StereoDelay
{
public:
    void prepare(double sampleRate, int maxDelayMs = 2000)
    {
        int maxSamples = static_cast<int>(sampleRate * maxDelayMs / 1000.0);
        delayLineL.resize(maxSamples);
        delayLineR.resize(maxSamples);
        this->sampleRate = sampleRate;
    }

    void setParameters(float timeMs, float feedback, float mix)
    {
        delaySamples = static_cast<int>(sampleRate * timeMs / 1000.0f);
        this->feedback = juce::jlimit(0.0f, 0.95f, feedback);
        this->mix = mix;
    }

    void process(float& left, float& right)
    {
        float delayedL = delayLineL[writePos];
        float delayedR = delayLineR[writePos];

        delayLineL[writePos] = left + delayedR * feedback;  // Cross-feedback
        delayLineR[writePos] = right + delayedL * feedback;

        left = left * (1.0f - mix) + delayedL * mix;
        right = right * (1.0f - mix) + delayedR * mix;

        writePos = (writePos + 1) % delaySamples;
    }

private:
    std::vector<float> delayLineL, delayLineR;
    double sampleRate = 44100.0;
    int delaySamples = 0, writePos = 0;
    float feedback = 0.3f, mix = 0.5f;
};
```

**Reverb using JUCE DSP:**
```cpp
class StereoReverb
{
public:
    void prepare(const juce::dsp::ProcessSpec& spec)
    {
        reverb.prepare(spec);
    }

    void setParameters(float roomSize, float damping, float wetLevel, float width)
    {
        juce::Reverb::Parameters params;
        params.roomSize = roomSize;
        params.damping = damping;
        params.wetLevel = wetLevel;
        params.dryLevel = 1.0f - wetLevel;
        params.width = width;
        reverb.setParameters(params);
    }

    void process(juce::AudioBuffer<float>& buffer)
    {
        juce::dsp::AudioBlock<float> block(buffer);
        juce::dsp::ProcessContextReplacing<float> context(block);
        reverb.process(context);
    }

private:
    juce::dsp::Reverb reverb;
};
```

### Modulation

**LFO with Multiple Shapes:**
```cpp
class LFO
{
public:
    enum class Shape { Sine, Triangle, Square, SawUp, SawDown };

    void prepare(double sampleRate) { this->sampleRate = sampleRate; }
    void setRate(float hz) { phaseIncrement = hz / sampleRate; }
    void setShape(Shape s) { shape = s; }

    float process()
    {
        float value = 0.0f;
        switch (shape)
        {
            case Shape::Sine:    value = std::sin(phase * juce::MathConstants<float>::twoPi); break;
            case Shape::Triangle: value = 2.0f * std::abs(2.0f * phase - 1.0f) - 1.0f; break;
            case Shape::Square:  value = phase < 0.5f ? 1.0f : -1.0f; break;
            case Shape::SawUp:   value = 2.0f * phase - 1.0f; break;
            case Shape::SawDown: value = 1.0f - 2.0f * phase; break;
        }
        phase += phaseIncrement;
        if (phase >= 1.0f) phase -= 1.0f;
        return value;
    }

private:
    double sampleRate = 44100.0;
    float phase = 0.0f, phaseIncrement = 0.0f;
    Shape shape = Shape::Sine;
};
```

**ADSR Envelope:**
```cpp
class ADSREnvelope
{
public:
    enum class State { Idle, Attack, Decay, Sustain, Release };

    void prepare(double sampleRate) { this->sampleRate = sampleRate; }

    void setParameters(float attack, float decay, float sustain, float release)
    {
        attackRate = 1.0f / (attack * sampleRate);
        decayRate = 1.0f / (decay * sampleRate);
        sustainLevel = sustain;
        releaseRate = 1.0f / (release * sampleRate);
    }

    void noteOn() { state = State::Attack; }
    void noteOff() { state = State::Release; }

    float process()
    {
        switch (state)
        {
            case State::Idle: return 0.0f;
            case State::Attack:
                level += attackRate;
                if (level >= 1.0f) { level = 1.0f; state = State::Decay; }
                break;
            case State::Decay:
                level -= decayRate;
                if (level <= sustainLevel) { level = sustainLevel; state = State::Sustain; }
                break;
            case State::Sustain:
                break;
            case State::Release:
                level -= releaseRate;
                if (level <= 0.0f) { level = 0.0f; state = State::Idle; }
                break;
        }
        return level;
    }

    bool isActive() const { return state != State::Idle; }

private:
    double sampleRate = 44100.0;
    State state = State::Idle;
    float level = 0.0f;
    float attackRate = 0.0f, decayRate = 0.0f, sustainLevel = 0.5f, releaseRate = 0.0f;
};
```

---

## UI Patterns

### Custom LookAndFeel

```cpp
class {Name}LookAndFeel : public juce::LookAndFeel_V4
{
public:
    // Color palette
    static inline const juce::Colour background { 0xff1a1a1a };
    static inline const juce::Colour panelBg { 0xff252525 };
    static inline const juce::Colour accent { 0xffff6b35 };
    static inline const juce::Colour accentAlt { 0xff00ff88 };
    static inline const juce::Colour textPrimary { 0xffe0e0e0 };
    static inline const juce::Colour textSecondary { 0xff888888 };

    void drawRotarySlider(juce::Graphics& g, int x, int y, int width, int height,
                          float sliderPos, float startAngle, float endAngle,
                          juce::Slider& slider) override
    {
        auto bounds = juce::Rectangle<int>(x, y, width, height).toFloat().reduced(4.0f);
        auto radius = juce::jmin(bounds.getWidth(), bounds.getHeight()) / 2.0f;
        auto centreX = bounds.getCentreX();
        auto centreY = bounds.getCentreY();
        auto angle = startAngle + sliderPos * (endAngle - startAngle);

        // Background circle
        g.setColour(panelBg);
        g.fillEllipse(bounds);

        // Value arc
        juce::Path arc;
        arc.addCentredArc(centreX, centreY, radius - 4.0f, radius - 4.0f,
                          0.0f, startAngle, angle, true);
        g.setColour(accent);
        g.strokePath(arc, juce::PathStrokeType(3.0f));

        // Pointer
        juce::Path pointer;
        auto pointerLength = radius * 0.6f;
        pointer.addRectangle(-2.0f, -pointerLength, 4.0f, pointerLength);
        g.setColour(textPrimary);
        g.fillPath(pointer, juce::AffineTransform::rotation(angle)
                               .translated(centreX, centreY));
    }
};
```

### Waveform Visualizer

```cpp
class WaveformVisualizer : public juce::Component, private juce::Timer
{
public:
    WaveformVisualizer() { startTimerHz(60); }

    void pushSample(float left, float right)
    {
        bufferL[writePos] = left;
        bufferR[writePos] = right;
        writePos = (writePos + 1) % BufferSize;
    }

    void paint(juce::Graphics& g) override
    {
        g.fillAll(juce::Colour(0xff1a1a2e));

        // Draw waveform paths
        juce::Path pathL, pathR;
        auto bounds = getLocalBounds().toFloat().reduced(4.0f);
        auto centreY = bounds.getCentreY();

        for (int i = 0; i < BufferSize; ++i)
        {
            float x = bounds.getX() + (i / (float)BufferSize) * bounds.getWidth();
            float yL = centreY - bufferL[i] * bounds.getHeight() * 0.4f;
            float yR = centreY - bufferR[i] * bounds.getHeight() * 0.4f;

            if (i == 0) { pathL.startNewSubPath(x, yL); pathR.startNewSubPath(x, yR); }
            else { pathL.lineTo(x, yL); pathR.lineTo(x, yR); }
        }

        g.setColour(juce::Colour(0xff00d9ff).withAlpha(0.8f));
        g.strokePath(pathL, juce::PathStrokeType(1.5f));
        g.setColour(juce::Colour(0xffe91e63).withAlpha(0.8f));
        g.strokePath(pathR, juce::PathStrokeType(1.5f));
    }

private:
    void timerCallback() override { repaint(); }

    static constexpr int BufferSize = 256;
    std::array<float, BufferSize> bufferL{}, bufferR{};
    int writePos = 0;
};
```

---

## Build Commands

After generating all files, build with:

```bash
# Navigate to plugin directory
cd /path/to/{plugin-name}

# Configure with Ninja (faster builds)
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release

# Build
cmake --build build --config Release

# Plugin output locations:
# VST3: build/{Name}_artefacts/Release/VST3/{Name}.vst3
# AU:   build/{Name}_artefacts/Release/AU/{Name}.component
# App:  build/{Name}_artefacts/Release/Standalone/{Name}.app
```

### Install to DAW

```bash
# Copy VST3 to system location
cp -r build/{Name}_artefacts/Release/VST3/{Name}.vst3 ~/Library/Audio/Plug-Ins/VST3/

# Copy AU to system location
cp -r build/{Name}_artefacts/Release/AU/{Name}.component ~/Library/Audio/Plug-Ins/Components/

# Rescan plugins in DAW
```

---

## Common Plugin Recipes

### 1. Simple Synthesizer
- 1-2 oscillators with waveform selection
- ADSR envelope for amplitude
- Low-pass filter with cutoff/resonance
- Master volume

### 2. Drone/Ambient Synth
- Multiple detuned oscillators
- Ultra-slow LFOs (0.01-1 Hz)
- Long attack/release envelopes
- Reverb and delay effects
- Stereo width processing

### 3. Distortion/Saturation Effect
- Input gain stage
- Waveshaping/clipping algorithms
- Tone control (EQ)
- Mix (dry/wet) control
- Output level

### 4. Delay Effect
- Tempo-syncable delay time
- Feedback with filtering
- Stereo ping-pong mode
- Modulation (chorus/flutter)
- Mix control

### 5. Filter Effect
- Multiple filter modes (LP, HP, BP, Notch)
- Cutoff and resonance
- LFO modulation
- Envelope follower
- Drive/saturation

---

## Important Guidelines

1. **Thread Safety**: Use `std::atomic<float>*` for real-time parameter access
2. **No Allocations**: Never allocate memory in `processBlock()`
3. **Denormals**: Use `juce::ScopedNoDenormals` in processing
4. **Smoothing**: Use `juce::SmoothedValue` for click-free parameter changes
5. **State Save/Load**: Implement `getStateInformation`/`setStateInformation`
6. **Anti-Aliasing**: Use PolyBLEP for digital oscillators
7. **DC Blocking**: Add DC blockers after nonlinear processing

## Example Session

**User**: Create a vintage tape delay effect plugin

**Assistant**: I'll create a tape delay VST with:
- Delay time (tempo-syncable)
- Feedback with low-pass filtering (tape warmth)
- Wow & flutter modulation
- Tape saturation
- Mix control

[Generates complete project...]

---

## Reference Files

For complete implementation examples, examine:
- `/Users/franciscokemeny/Code/modular/monolith-vst/` - Drone synth
- `/Users/franciscokemeny/Code/solardronemachine/` - Vintage synth emulator
- `/Users/franciscokemeny/Code/microdetuner/` - Simple generator

These provide real-world patterns for DSP, parameters, and UI.
