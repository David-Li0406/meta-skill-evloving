# Godot - Audio

**Pages:** 13

---

## Importing audio samples — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_audio_samples.html

**Contents:**
- Importing audio samples
- Supported audio formats
- Importing audio samples
- Import options (WAV)
- Force > 8 Bit
- Force > Mono
- Force > Max Rate
- Edit > Trim
- Edit > Normalize
- Edit > Loop Mode

Godot provides 3 options to import your audio data: WAV, Ogg Vorbis and MP3.

Each format has different advantages:

WAV files use raw data or light compression (IMA ADPCM or Quite OK Audio). Currently they can only be imported in raw format, but Godot allows compression after import. They are lightweight to play back on the CPU (hundreds of simultaneous voices in this format are fine). The downside is that they take up a lot of disk space.

Ogg Vorbis files use a stronger compression that results in much smaller file size, but require significantly more processing power to play back.

MP3 files use better compression than WAV with IMA ADPCM or Quite OK Audio, but worse than Ogg Vorbis. This means that an MP3 file with roughly equal quality to Ogg Vorbis will be significantly larger. On the bright side, MP3 requires less CPU usage to play back compared to Ogg Vorbis.

If you've compiled the Godot editor from source with specific modules disabled, some formats may not be available.

Here is a comparative chart representing the file size of 1 second of audio with each format:

WAV 24-bit, 96 kHz, stereo

WAV 16-bit, 44 kHz, mono

WAV IMA ADPCM, 44 kHz, mono

Quite OK Audio, 44 kHz, mono

Ogg Vorbis 128 Kb/s, stereo

Ogg Vorbis 96 Kb/s, stereo

Note that the MP3 and Ogg Vorbis figures can vary depending on the encoding type. The above figures use CBR encoding for simplicity, but most Ogg Vorbis and MP3 files you can find online are encoded with VBR encoding which is more efficient. VBR encoding makes the effective audio file size depend on how "complex" the source audio is.

Consider using WAV for short and repetitive sound effects, and Ogg Vorbis for music, speech, and long sound effects. MP3 is useful for mobile and web projects where CPU resources are limited, especially when playing multiple compressed sounds at the same time (such as long ambient sounds).

Several options are available in the Import dock after selecting a WAV file in the FileSystem dock:

Import options in the Import dock after selecting a WAV file in the FileSystem dock

The set of options available after selecting an Ogg Vorbis or MP3 file is different:

Import options in the Import dock after selecting an MP3 file in the FileSystem dock. Options are identical for Ogg Vorbis files.

After importing a sound, you can play it back using the AudioStreamPlayer, AudioStreamPlayer2D or AudioStreamPlayer3D nodes. See Audio streams for more information.

If enabled, forces the imported audio to use 8-bit quantization if the source file is 16-bit or higher.

Enabling this is generally not recommended, as 8-bit quantization decreases audio quality significantly. If you need smaller file sizes, consider using Ogg Vorbis or MP3 audio instead.

If enabled, forces the imported audio to be mono if the source file is stereo. This decreases the file size by 50% by merging the two channels into one.

If set to a value greater than 0, forces the audio's sample rate to be reduced to a value lower than or equal to the value specified here.

This can decrease file size noticeably on certain sounds, without impacting quality depending on the actual sound's contents. See Best practices for more information.

The source audio file may contain long silences at the beginning and/or the end. These silences are inserted by DAWs when saving to a waveform, which increases their size unnecessarily and add latency to the moment they are played back.

Enabling Trim will automatically trim the beginning and end of the audio if it's lower than -50 dB after normalization (see Edit > Normalize below). A fade-in/fade-out period of 500 samples is also used during trimming to avoid audible pops.

If enabled, audio volume will be normalized so that its peak volume is equal to 0 dB. When enabled, normalization will make audio sound louder depending on its original peak volume.

Unlike Ogg Vorbis and MP3, WAV files can contain metadata to indicate whether they're looping (in addition to loop points). By default, Godot will follow this metadata, but you can choose to apply a specific loop mode:

Detect from WAV: Uses loop information from the WAV metadata.

Disabled: Don't loop audio, even if metadata indicates the file should be played back looping.

Forward: Standard audio looping. Plays the audio forward from the beginning to the loop end, then returns to the loop beginning and repeats.

Ping-Pong: Plays the audio forward until the loop end, then backwards to the loop beginning, repeating this cycle.

Backward: Plays the audio backwards from the loop end to the loop beginning, then repeats.

When choosing one of the Forward, Ping-Pong or Backward loop modes, loop points can also be defined to make only a specific part of the sound loop. Loop Begin is set in samples after the beginning of the audio file. Loop End is also set in samples after the beginning of the audio file, but will use the end of the audio file if set to -1.

In AudioStreamPlayer, the finished signal won't be emitted for looping audio when it reaches the end of the audio file, as the audio will keep playing indefinitely.

Three compression modes can be chosen from for WAV files: PCM (Uncompressed), IMA ADPCM, or Quite OK Audio (default). IMA ADPCM reduces file size and memory usage a little, at the cost of decreasing quality in an audible manner. Quite OK Audio reduces file size a bit more than IMA ADPCM and the quality decrease is much less noticeable, at the cost of slightly higher CPU usage (still much lower than MP3).

Ogg Vorbis and MP3 don't decrease quality as much and can provide greater file size reductions, at the cost of higher CPU usage during playback. This higher CPU usage is usually not a problem (especially with MP3), unless playing dozens of compressed sounds at the same time on mobile/web platforms.

If enabled, the audio will begin playing at the beginning after playback ends by reaching the end of the audio.

In AudioStreamPlayer, the finished signal won't be emitted for looping audio when it reaches the end of the audio file, as the audio will keep playing indefinitely.

The loop offset determines where audio will start to loop after playback reaches the end of the audio. This can be used to only loop a part of the audio file, which is useful for some ambient sounds or music. The value is determined in seconds relative to the beginning of the audio, so 0 will loop the entire audio file.

Only has an effect if Loop is enabled.

A more convenient editor for Loop Offset is provided in the Advanced import settings dialog, as it lets you preview your changes without having to reimport the audio.

The Beats Per Minute of the audio track. This should match the BPM measure that was used to compose the track. This is only relevant for music that wishes to make use of interactive music functionality, not sound effects.

A more convenient editor for BPM is provided in the Advanced import settings dialog, as it lets you preview your changes without having to reimport the audio.

The beat count of the audio track. This is only relevant for music that wishes to make use of interactive music functionality, not sound effects.

A more convenient editor for Beat Count is provided in the Advanced import settings dialog, as it lets you preview your changes without having to reimport the audio.

The number of bars within a single beat in the audio track. This is only relevant for music that wishes to make use of interactive music functionality , not sound effects.

A more convenient editor for Bar Beats is provided in the Advanced import settings dialog, as it lets you preview your changes without having to reimport the audio.

If you double-click an Ogg Vorbis or MP3 file in the FileSystem dock (or choose Advanced… in the Import dock), you will see a dialog appear:

Advanced dialog when double-clicking an Ogg Vorbis or MP3 file in the FileSystem dock

This dialog allows you to edit the audio's loop point with a real-time preview, in addition to the BPM, beat count and bar beats. These 3 settings are currently unused, but they will be used in the future for interactive music support (which allows smoothly transitioning between different music tracks).

Unlike WAV files, Ogg Vorbis and MP3 only support a "loop begin" loop point, not a "loop end" point. Looping can also be only be standard forward looping, not ping-pong or backward.

While keeping pristine-quality audio sources is important if you're performing editing, using the same quality in the exported project is not necessary. For WAV files, Godot offers several import options to reduce the final file size without modifying the source file on disk.

To reduce memory usage and file size, choose an appropriate quantization, sample rate and number of channels for your audio:

There's no audible benefit to using 24-bit audio, especially in a game where several sounds are often playing at the same time (which makes it harder to appreciate individual sounds).

Unless you are slowing down the audio at runtime, there's no audible benefit to using a sample rate greater than 48 kHz. If you wish to keep a source with a higher sample rate for editing, use the Force > Max Rate import option to limit the sample rate of the imported sound (only available for WAV files).

Many sound effects can generally be converted to mono as opposed to stereo. If you wish to keep a source with stereo for editing, use the Force > Mono import option to convert the imported sound to mono (only available for WAV files).

Voices can generally be converted to mono, but can also have their sample rate reduced to 22 kHz without a noticeable loss in quality (unless the voice is very high-pitched). This is because most human voices never go past 11 kHz.

Godot has an extensive bus system with built-in effects. This saves SFX artists the need to add reverb to the sound effects, reducing their size greatly and ensuring correct trimming.

As you can see above, sound effects become much larger in file size with reverb added.

Audio samples can be loaded and saved at runtime using runtime file loading and saving, including from an exported project.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Audio buses — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/audio/audio_buses.html

**Contents:**
- Audio buses
- Introduction
- Decibel scale
- Audio buses
- Playback of audio through a bus
- Adding effects
- Automatic bus disabling
- Bus rearrangement
- Default bus layout
- User-contributed notes

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

Godot's audio processing code has been written with games in mind, with the aim of achieving an optimal balance between performance and sound quality.

Godot's audio engine allows any number of audio buses to be created and any number of effect processors can be added to each bus. Only the hardware of the device running your game will limit the number of buses and effects that can be used before performance starts to suffer.

Godot's sound interface is designed to meet the expectations of sound design professionals. To this end, it primarily uses the decibel scale.

For those unfamiliar with it, it can be explained with a few facts:

The decibel (dB) scale is a relative scale. It represents the ratio of sound power by using 20 times the base 10 logarithm of the ratio (20 × log10(P/P0)).

For every 6 dB, sound amplitude doubles or halves. 12 dB represents a factor of 4, 18 dB a factor of 8, 20 dB a factor of 10, 40 dB a factor of 100, etc.

Since the scale is logarithmic, true zero (no audio) can't be represented.

0 dB is the maximum amplitude possible in a digital audio system. This limit is not the human limit, but a limit from the sound hardware. Audio with amplitudes that are too high to be represented properly below 0 dB create a kind of distortion called clipping.

To avoid clipping, your sound mix should be arranged so that the output of the master bus (more on that later) never exceeds 0 dB.

Every 6 dB below the 0 dB limit, sound energy is halved. It means the sound volume at -6 dB is half as loud as 0dB. -12 dB is half as loud as -6 dB and so on.

When working with decibels, sound is considered no longer audible between -60 dB and -80 dB. This makes your working range generally between -60 dB and 0 dB.

This can take a bit getting used to, but it's friendlier in the end and will allow you to communicate better with audio professionals.

Audio buses can be found in the bottom panel of the Godot editor:

An audio bus (also called an audio channel) can be considered a place that audio is channeled through on the way to playback through a device's speakers. Audio data can be modified and re-routed by an audio bus. An audio bus has a VU meter (the bars that light up when sound is played) which indicates the amplitude of the signal passing through.

The leftmost bus is the master bus. This bus outputs the mix to your speakers so, as mentioned in the Decibel scale section above, make sure that your mix level doesn't reach 0 dB in this bus. The rest of the audio buses can be flexibly routed. After modifying the sound, they send it to another bus to the left. The destination bus can be specified for each of the non-master audio buses. Routing always passes audio from buses on the right to buses further to the left. This avoids infinite routing loops.

In the above image, the output of Bus 2 has been routed to the Master bus.

To test passing audio to a bus, create an AudioStreamPlayer node, load an AudioStream and select a target bus for playback:

Finally, toggle the Playing property to On and sound will flow.

You may also be interested in reading about Audio streams now.

This feature is not supported on the web platform if the AudioStreamPlayer's playback mode is set to Sample, which is the default. It will only work if the playback mode is set to Stream, at the cost of increased latency if threads are not enabled.

See Audio playback in the Exporting for the Web documentation for details.

Audio buses can contain all sorts of effects. These effects modify the sound in one way or another and are applied in order.

For information on what each effect does, see Audio effects.

There is no need to disable buses manually when not in use. Godot detects that the bus has been silent for a few seconds and disables it (including all effects).

Disabled buses have a blue VU meter instead of a red-green one.

Stream Players use bus names to identify a bus, which allows adding, removing and moving buses around while the reference to them is kept. However, if a bus is renamed, the reference will be lost and the Stream Player will output to Master. This system was chosen because rearranging buses is a more common process than renaming them.

The default bus layout is automatically saved to the res://default_bus_layout.tres file. Custom bus arrangements can be saved and loaded from disk.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Sync the gameplay with audio and music — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/audio/sync_with_audio.html

**Contents:**
- Sync the gameplay with audio and music
- Introduction
- Using the system clock to sync
- Using the sound hardware clock to sync
- User-contributed notes

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

In any application or game, sound and music playback will have a slight delay. For games, this delay is often so small that it is negligible. Sound effects will come out a few milliseconds after any play() function is called. For music this does not matter as in most games it does not interact with the gameplay.

Still, for some games (mainly, rhythm games), it may be required to synchronize player actions with something happening in a song (usually in sync with the BPM). For this, having more precise timing information for an exact playback position is useful.

Achieving very low playback timing precision is difficult. This is because many factors are at play during audio playback:

Audio is mixed in chunks (not continuously), depending on the size of audio buffers used (check latency in project settings).

Mixed chunks of audio are not played immediately.

Graphics APIs display two or three frames late.

When playing on TVs, some delay may be added due to image processing.

The most common way to reduce latency is to shrink the audio buffers (again, by editing the latency setting in the project settings). The problem is that when latency is too small, sound mixing will require considerably more CPU. This increases the risk of skipping (a crack in sound because a mix callback was lost).

This is a common tradeoff, so Godot ships with sensible defaults that should not need to be altered.

The problem, in the end, is not this slight delay but synchronizing graphics and audio for games that require it. Some helpers are available to obtain more precise playback timing.

As mentioned before, If you call AudioStreamPlayer.play(), sound will not begin immediately, but when the audio thread processes the next chunk.

This delay can't be avoided but it can be estimated by calling AudioServer.get_time_to_next_mix().

The output latency (what happens after the mix) can also be estimated by calling AudioServer.get_output_latency().

Add these two and it's possible to guess almost exactly when sound or music will begin playing in the speakers during _process():

In the long run, though, as the sound hardware clock is never exactly in sync with the system clock, the timing information will slowly drift away.

For a rhythm game where a song begins and ends after a few minutes, this approach is fine (and it's the recommended approach). For a game where playback can last a much longer time, the game will eventually go out of sync and a different approach is needed.

Using AudioStreamPlayer.get_playback_position() to obtain the current position for the song sounds ideal, but it's not that useful as-is. This value will increment in chunks (every time the audio callback mixed a block of sound), so many calls can return the same value. Added to this, the value will be out of sync with the speakers too because of the previously mentioned reasons.

To compensate for the "chunked" output, there is a function that can help: AudioServer.get_time_since_last_mix().

Adding the return value from this function to get_playback_position() increases precision:

To increase precision, subtract the latency information (how much it takes for the audio to be heard after it was mixed):

The result may be a bit jittery due how multiple threads work. Just check that the value is not less than in the previous frame (discard it if so). This is also a less precise approach than the one before, but it will work for songs of any length, or synchronizing anything (sound effects, as an example) to music.

Here is the same code as before using this approach:

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
var time_begin
var time_delay


func _ready():
    time_begin = Time.get_ticks_usec()
    time_delay = AudioServer.get_time_to_next_mix() + AudioServer.get_output_latency()
    $Player.play()


func _process(delta):
    # Obtain from ticks.
    var time = (Time.get_ticks_usec() - time_begin) / 1000000.0
    # Compensate for latency.
    time -= time_delay
    # May be below 0 (did not begin yet).
    time = max(0, time)
    print("Time is: ", time)
```

Example 2 (gdscript):
```gdscript
private double _timeBegin;
private double _timeDelay;

public override void _Ready()
{
    _timeBegin = Time.GetTicksUsec();
    _timeDelay = AudioServer.GetTimeToNextMix() + AudioServer.GetOutputLatency();
    GetNode<AudioStreamPlayer>("Player").Play();
}

public override void _Process(double delta)
{
    double time = (Time.GetTicksUsec() - _timeBegin) / 1000000.0d;
    time = Math.Max(0.0d, time - _timeDelay);
    GD.Print(string.Format("Time is: {0}", time));
}
```

Example 3 (gdscript):
```gdscript
var time = $Player.get_playback_position() + AudioServer.get_time_since_last_mix()
```

Example 4 (typescript):
```typescript
double time = GetNode<AudioStreamPlayer>("Player").GetPlaybackPosition() + AudioServer.GetTimeSinceLastMix();
```

---

## Text to speech — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/audio/text_to_speech.html

**Contents:**
- Text to speech
- Basic Usage
- Requirements for functionality
  - Distro-specific one-liners
- Troubleshooting
- Best practices
- Caveats and Other Information
- User-contributed notes

Basic usage of text-to-speech involves the following one-time steps:

Enable TTS in the Godot editor for your project

Query the system for a list of usable voices

Store the ID of the voice you want to use

By default, the Godot project-level setting for text-to-speech is disabled, to avoid unnecessary overhead. To enable it:

Go to Project > Project Settings

Make sure the Advanced Settings toggle is enabled

Click on Audio > General

Ensure the Text to Speech option is checked

Restart Godot if prompted to do so.

Text-to-speech uses a specific voice. Depending on the user's system, they might have multiple voices installed. Once you have the voice ID, you can use it to speak some text:

Godot includes text-to-speech functionality. You can find these under the DisplayServer class.

Godot depends on system libraries for text-to-speech functionality. These libraries are installed by default on Windows, macOS, Web, Android and iOS, but not on all Linux distributions. If they are not present, text-to-speech functionality will not work. Specifically, the tts_get_voices() method will return an empty list, indicating that there are no usable voices.

Both Godot users on Linux and end-users on Linux running Godot games need to ensure that their system includes the system libraries for text-to-speech to work. Please consult the table below or your own distribution's documentation to determine what libraries you need to install.

If you get the error Invalid get index '0' (on base: 'PackedStringArray'). for the line var voice_id = voices[0], check if there are any items in voices. If not:

All users: make sure you enabled Text to Speech in project settings

Linux users: ensure you installed the system-specific libraries for text to speech

The best practices for text-to-speech, in terms of the ideal player experience for blind players, is to send output to the player's screen reader. This preserves the choice of language, speed, pitch, etc. that the user set, as well as allows advanced features like allowing players to scroll backward and forward through text. As of now, Godot doesn't provide this level of integration.

With the current state of the Godot text-to-speech APIs, best practices include:

Develop the game with text-to-speech enabled, and ensure that everything sounds correct

Allow players to control which voice to use, and save/persist that selection across game sessions

Allow players to control the speech rate, and save/persist that selection across game sessions

This provides your blind players with the most flexibility and comfort available when not using a screen reader, and minimizes the chance of frustrating and alienating them.

Expect delays when you call tts_speak and tts_stop. The actual delay time varies depending on both the OS and on your machine's specifications. This is especially critical on Android and Web, where some of the voices depend on web services, and the actual time to playback depends on server load, network latency, and other factors.

Non-English text works if the correct voices are installed and used. On Windows, you can consult the instructions in this article to enable additional language voices on Windows.

Non-ASCII characters, such as umlaut, are pronounced correctly if you select the correct voice.

Blind players use a number of screen readers, including JAWS, NVDA, VoiceOver, Narrator, and more.

Windows text-to-speech APIs generally perform better than their equivalents on other systems (e.g. tts_stop followed by tts_speak immediately speaks the new message).

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
# One-time steps.
# Pick a voice. Here, we arbitrarily pick the first English voice.
var voices = DisplayServer.tts_get_voices_for_language("en")
var voice_id = voices[0]

# Say "Hello, world!".
DisplayServer.tts_speak("Hello, world!", voice_id)

# Say a longer sentence, and then interrupt it.
# Note that this method is asynchronous: execution proceeds to the next line immediately,
# before the voice finishes speaking.
var long_message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur"
DisplayServer.tts_speak(long_message, voice_id)

# Immediately stop the current text mid-sentence and say goodbye instead.
DisplayServer.tts_stop()
DisplayServer.tts_speak("Goodbye!", voice_id)
```

Example 2 (csharp):
```csharp
// One-time steps.
// Pick a voice. Here, we arbitrarily pick the first English voice.
string[] voices = DisplayServer.TtsGetVoicesForLanguage("en");
string voiceId = voices[0];

// Say "Hello, world!".
DisplayServer.TtsSpeak("Hello, world!", voiceId);

// Say a longer sentence, and then interrupt it.
// Note that this method is asynchronous: execution proceeds to the next line immediately,
// before the voice finishes speaking.
string longMessage = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur";
DisplayServer.TtsSpeak(longMessage, voiceId);

// Immediately stop the current text mid-sentence and say goodbye instead.
DisplayServer.TtsStop();
DisplayServer.TtsSpeak("Goodbye!", voiceId);
```

Example 3 (unknown):
```unknown
pacman -S speech-dispatcher festival espeakup
```

---

## Audio — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/audio/index.html

**Contents:**
- Audio

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Recording with microphone — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/audio/recording_with_microphone.html

**Contents:**
- Recording with microphone
- The structure of the demo
- User-contributed notes

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

Godot supports in-game audio recording for Windows, macOS, Linux, Android and iOS.

A simple demo is included in the official demo projects and will be used as support for this tutorial: https://github.com/godotengine/godot-demo-projects/tree/master/audio/mic_record.

You will need to enable audio input in the Audio > Driver > Enable Input project setting, or you'll just get empty audio files.

The demo consists of a single scene. This scene includes two major parts: the GUI and the audio.

We will focus on the audio part. In this demo, a bus named Record with the effect Record is created to handle the audio recording. An AudioStreamPlayer named AudioStreamRecord is used for recording.

The audio recording is handled by the AudioEffectRecord resource which has three methods: get_recording(), is_recording_active(), and set_recording_active().

At the start of the demo, the recording effect is not active. When the user presses the RecordButton, the effect is enabled with set_recording_active(true).

On the next button press, as effect.is_recording_active() is true, the recorded stream can be stored into the recording variable by calling effect.get_recording().

To playback the recording, you assign the recording as the stream of the AudioStreamPlayer and call play().

To save the recording, you call save_to_wav() with the path to a file. In this demo, the path is defined by the user via a LineEdit input box.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
var effect
var recording


func _ready():
    # We get the index of the "Record" bus.
    var idx = AudioServer.get_bus_index("Record")
    # And use it to retrieve its first effect, which has been defined
    # as an "AudioEffectRecord" resource.
    effect = AudioServer.get_bus_effect(idx, 0)
```

Example 2 (gdscript):
```gdscript
private AudioEffectRecord _effect;
private AudioStreamSample _recording;

public override void _Ready()
{
    // We get the index of the "Record" bus.
    int idx = AudioServer.GetBusIndex("Record");
    // And use it to retrieve its first effect, which has been defined
    // as an "AudioEffectRecord" resource.
    _effect = (AudioEffectRecord)AudioServer.GetBusEffect(idx, 0);
}
```

Example 3 (typescript):
```typescript
func _on_record_button_pressed():
    if effect.is_recording_active():
        recording = effect.get_recording()
        $PlayButton.disabled = false
        $SaveButton.disabled = false
        effect.set_recording_active(false)
        $RecordButton.text = "Record"
        $Status.text = ""
    else:
        $PlayButton.disabled = true
        $SaveButton.disabled = true
        effect.set_recording_active(true)
        $RecordButton.text = "Stop"
        $Status.text = "Recording..."
```

Example 4 (json):
```json
private void OnRecordButtonPressed()
{
    if (_effect.IsRecordingActive())
    {
        _recording = _effect.GetRecording();
        GetNode<Button>("PlayButton").Disabled = false;
        GetNode<Button>("SaveButton").Disabled = false;
        _effect.SetRecordingActive(false);
        GetNode<Button>("RecordButton").Text = "Record";
        GetNode<Label>("Status").Text = "";
    }
    else
    {
        GetNode<Button>("PlayButton").Disabled = true;
        GetNode<Button>("SaveButton").Disabled = true;
        _effect.SetRecordingActive(true);
        GetNode<Button>("RecordButton").Text = "Stop";
        GetNode<Label>("Status").Text = "Recording...";
    }
}
```

---

## Audio streams — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/audio/audio_streams.html

**Contents:**
- Audio streams
- Introduction
- AudioStream
- AudioStreamPlayer
- AudioStreamPlayer2D
- AudioStreamPlayer3D
  - Reverb buses
  - Doppler
- User-contributed notes

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

As you might have already read in Audio buses, sound is sent to each bus via an AudioStreamPlayer node. There are different kinds of AudioStreamPlayers. Each one loads an AudioStream and plays it back.

An audio stream is an abstract object that emits sound. The sound can come from many places, but is most commonly loaded from the filesystem. Audio files can be loaded as AudioStreams and placed inside an AudioStreamPlayer. You can find information on supported formats and differences in Importing audio samples.

There are other types of AudioStreams, such as AudioStreamRandomizer. This one picks a different audio stream from a list of streams each time it's played back, and applies random pitch and volume shifting. This can be helpful for adding variation to sounds that are played back often.

This is the standard, non-positional stream player. It can play to any bus. In 5.1 sound setups, it can send audio to stereo mix or front speakers.

Playback Type is an experimental setting, and could change in future versions of Godot. It exists so Web exports use Web Audio-API based samples instead of streaming all sounds to the browser, unlike most platforms. This prevents the audio from being garbled in single-threaded Web exports. By default, only the Web platform will use samples. Changing this setting is not recommended, unless you have an explicit reason to. You can change the default playback type for the web and other platforms in the project settings under Audio > General (advanced settings must be turned on to see the setting).

This is a variant of AudioStreamPlayer, but emits sound in a 2D positional environment. When close to the left of the screen, the panning will go left. When close to the right side, it will go right.

Area2Ds can be used to divert sound from any AudioStreamPlayer2Ds they contain to specific buses. This makes it possible to create buses with different reverb or sound qualities to handle action happening in a particular parts of your game world.

This is a variant of AudioStreamPlayer, but emits sound in a 3D positional environment. Depending on the location of the player relative to the screen, it can position sound in stereo, 5.1 or 7.1 depending on the chosen audio setup.

Similar to AudioStreamPlayer2D, an Area3D can divert the sound to an audio bus.

Unlike for 2D, the 3D version of AudioStreamPlayer has a few more advanced options:

This feature is not supported on the web platform if the AudioStreamPlayer's playback mode is set to Sample, which is the default. It will only work if the playback mode is set to Stream, at the cost of increased latency if threads are not enabled.

See Audio playback in the Exporting for the Web documentation for details.

Godot allows for 3D audio streams that enter a specific Area3D node to send dry and wet audio to separate buses. This is useful when you have several reverb configurations for different types of rooms. This is done by enabling this type of reverb in the Reverb Bus section of the Area3D's properties:

At the same time, a special bus layout is created where each Area3D receives the reverb info from each Area3D. A Reverb effect needs to be created and configured in each reverb bus to complete the setup for the desired effect:

The Area3D's Reverb Bus section also has a parameter named Uniformity. Some types of rooms bounce sounds more than others (like a warehouse), so reverberation can be heard almost uniformly across the room even though the source may be far away. Playing around with this parameter can simulate that effect.

This feature is not supported on the web platform if the AudioStreamPlayer's playback mode is set to Sample, which is the default. It will only work if the playback mode is set to Stream, at the cost of increased latency if threads are not enabled.

See Audio playback in the Exporting for the Web documentation for details.

When the relative velocity between an emitter and listener changes, this is perceived as an increase or decrease in the pitch of the emitted sound. Godot can track velocity changes in the AudioStreamPlayer3D and Camera nodes. Both nodes have this property, which must be enabled manually:

Enable it by setting it depending on how objects will be moved: use Idle for objects moved using _process, or Physics for objects moved using _physics_process. The tracking will happen automatically.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Audio effects — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/audio/audio_effects.html

**Contents:**
- Audio effects
- Amplify
- BandLimit and BandPass
- Capture
- Chorus
- Compressor
- Delay
- Distortion
- EQ
- EQ6, EQ10, EQ21

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

Godot includes several audio effects that can be added to an audio bus to alter every sound file that goes through that bus.

Try them all out to get a sense of how they alter sound. Here follows a short description of the available effects:

Amplify changes the volume of the signal. Some care needs to be taken, though: setting the level too high can make the sound digitally clip, which can produce unpleasant crackles and pops.

These are resonant filters which block frequencies around the Cutoff point. BandPass can be used to simulate sound passing through an old telephone line or megaphone. Modulating the BandPass frequency can simulate the sound of a wah-wah guitar pedal, think of the guitar in Jimi Hendrix's Voodoo Child (Slight Return).

The Capture effect copies the audio frames of the audio bus that it is on into an internal buffer. This can be used to capture data from the microphone or to transmit audio over the network in real-time.

As the name of the effect implies, the Chorus effect makes a single audio sample sound like an entire chorus. It does this by duplicating a signal and very slightly altering the timing and pitch of each duplicate, and varying that over time via an LFO (low frequency oscillator). The duplicate(s) are then mixed back together with the original signal, producing a lush, wide, and large sound. Although chorus is traditionally used for voices, it can be desirable with almost any type of sound.

A dynamic range compressor automatically attenuates (ducks) the level of the incoming signal when its amplitude exceeds a certain threshold. The level of attenuation applied is proportional to how far the incoming audio exceeds the threshold. The compressor's Ratio parameter controls the degree of attenuation. One of the main uses of a compressor is to reduce the dynamic range of signals with very loud and quiet parts. Reducing the dynamic range of a signal can make it fit more comfortably in a mix.

The compressor has many uses. For example:

It can be used in the Master bus to compress the whole output prior to being hit by a limiter, making the effect of the limiter much more subtle.

It can be used in voice channels to ensure they sound as even as possible.

It can be sidechained by another sound source. This means it can reduce the sound level of one signal using the level of another audio bus for threshold detection. This technique is very common in video game mixing to "duck" the level of music or sound effects when in-game or multiplayer voices need to be fully audible.

It can accentuate transients by using a slower attack. This can make sound effects more punchy.

If your goal is to prevent a signal from exceeding a given amplitude altogether, rather than to reduce the dynamic range of the signal, a limiter is likely a better choice than a compressor for this purpose. However, applying compression before a limiter is still good practice.

Digital delay essentially duplicates a signal and repeats it at a specified speed with a volume level that decays for each repeat. Delay is great for simulating the acoustic space of a canyon or large room, where sound bounces have a lot of delay between their repeats. This is in contrast to reverb, which has a more natural and blurred sound to it. Using this in conjunction with reverb can create very natural sounding environments!

Makes the sound distorted. Godot offers several types of distortion:

Overdrive sounds like a guitar distortion pedal or megaphone. Sounds distorted with this sound like they're coming through a low-quality speaker or device.

Tan sounds like another interesting flavor of overdrive.

Bit crushing clamps the amplitude of the signal, making it sound flat and crunchy.

All three types of distortion can add higher frequency sounds to an original sound, making it stand out better in a mix.

EQ is what all other equalizers inherit from. It can be extended with Custom scripts to create an equalizer with a custom number of bands.

Godot provides three equalizers with different numbers of bands, which are represented in the title (6, 10, and 21 bands, respectively). An equalizer on the Master bus can be useful for cutting low and high frequencies that the device's speakers can't reproduce well. For example, phone or tablet speakers usually don't reproduce low frequency sounds well, and could make a limiter or compressor attenuate sounds that aren't even audible to the user anyway.

Note: The equalizer effect can be disabled when headphones are plugged in, giving the user the best of both worlds.

Filter is what all other filters inherit from and should not be used directly.

A limiter is similar to a compressor, but it's less flexible and designed to prevent a signal's amplitude exceeding a given dB threshold. Adding a limiter to the final point of the Master bus is good practice, as it offers an easy safeguard against clipping.

Cuts frequencies below a specific Cutoff frequency. HighPassFilter is used to reduce the bass content of a signal.

Reduces all frequencies above a specific Cutoff frequency.

This is the old limiter effect, and it is recommended to use the new HardLimiter effect instead.

Here is an example of how this effect works, if the ceiling is set to -12 dB, and the threshold is 0 dB, all samples going through get reduced by 12dB. This changes the waveform of the sound and introduces distortion.

This effect is being kept to preserve compatibility, however it should be considered deprecated.

Cuts frequencies above a specific Cutoff frequency and can also resonate (boost frequencies close to the Cutoff frequency). Low pass filters can be used to simulate "muffled" sound. For instance, underwater sounds, sounds blocked by walls, or distant sounds.

Reduces all frequencies below a specific Cutoff frequency.

The opposite of the BandPassFilter, it removes a band of sound from the frequency spectrum at a given Cutoff frequency.

The Panner allows the stereo balance of a signal to be adjusted between the left and right channels. Headphones are recommended when configuring in this effect.

This effect is formed by de-phasing two duplicates of the same sound so they cancel each other out in an interesting way. Phaser produces a pleasant whooshing sound that moves back and forth through the audio spectrum, and can be a great way to create sci-fi effects or Darth Vader-like voices.

This effect allows the adjustment of the signal's pitch independently of its speed. All frequencies can be increased/decreased with minimal effect on transients. PitchShift can be useful to create unusually high or deep voices. Do note that altering pitch can sound unnatural when pushed outside of a narrow window.

The Record effect allows the user to record sound from a microphone.

Reverb simulates rooms of different sizes. It has adjustable parameters that can be tweaked to obtain the sound of a specific room. Reverb is commonly outputted from Area3Ds (see Reverb buses), or to apply a "chamber" feel to all sounds.

This effect doesn't alter audio, instead, you add this effect to buses you want a spectrum analysis of. This would typically be used for audio visualization. Visualizing voices can be a great way to draw attention to them without just increasing their volume. A demo project using this can be found here.

This effect uses a few algorithms to enhance a signal's stereo width.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## AudioListener3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_audiolistener3d.html

**Contents:**
- AudioListener3D
- Description
- Properties
- Methods
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: Node3D < Node < Object

Overrides the location sounds are heard from.

Once added to the scene tree and enabled using make_current(), this node will override the location sounds are heard from. This can be used to listen from a location different from the Camera3D.

get_listener_transform() const

enum DopplerTracking: 🔗

DopplerTracking DOPPLER_TRACKING_DISABLED = 0

Disables Doppler effect simulation (default).

DopplerTracking DOPPLER_TRACKING_IDLE_STEP = 1

Simulate Doppler effect by tracking positions of objects that are changed in _process. Changes in the relative velocity of this listener compared to those objects affect how audio is perceived (changing the audio's AudioStreamPlayer3D.pitch_scale).

DopplerTracking DOPPLER_TRACKING_PHYSICS_STEP = 2

Simulate Doppler effect by tracking positions of objects that are changed in _physics_process. Changes in the relative velocity of this listener compared to those objects affect how audio is perceived (changing the audio's AudioStreamPlayer3D.pitch_scale).

DopplerTracking doppler_tracking = 0 🔗

void set_doppler_tracking(value: DopplerTracking)

DopplerTracking get_doppler_tracking()

If not DOPPLER_TRACKING_DISABLED, this listener will simulate the Doppler effect for objects changed in particular _process methods.

Note: The Doppler effect will only be heard on AudioStreamPlayer3Ds if AudioStreamPlayer3D.doppler_tracking is not set to AudioStreamPlayer3D.DOPPLER_TRACKING_DISABLED.

void clear_current() 🔗

Disables the listener to use the current camera's listener instead.

Transform3D get_listener_transform() const 🔗

Returns the listener's global orthonormalized Transform3D.

bool is_current() const 🔗

Returns true if the listener was made current using make_current(), false otherwise.

Note: There may be more than one AudioListener3D marked as "current" in the scene tree, but only the one that was made current last will be used.

void make_current() 🔗

Enables the listener. This will override the current camera's listener.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## AudioListener2D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_audiolistener2d.html

**Contents:**
- AudioListener2D
- Description
- Methods
- Method Descriptions
- User-contributed notes

Inherits: Node2D < CanvasItem < Node < Object

Overrides the location sounds are heard from.

Once added to the scene tree and enabled using make_current(), this node will override the location sounds are heard from. Only one AudioListener2D can be current. Using make_current() will disable the previous AudioListener2D.

If there is no active AudioListener2D in the current Viewport, center of the screen will be used as a hearing point for the audio. AudioListener2D needs to be inside SceneTree to function.

void clear_current() 🔗

Disables the AudioListener2D. If it's not set as current, this method will have no effect.

bool is_current() const 🔗

Returns true if this AudioListener2D is currently active.

void make_current() 🔗

Makes the AudioListener2D active, setting it as the hearing point for the sounds. If there is already another active AudioListener2D, it will be disabled.

This method will have no effect if the AudioListener2D is not added to SceneTree.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## AudioStreamPlayer — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer.html

**Contents:**
- AudioStreamPlayer
- Description
- Tutorials
- Properties
- Methods
- Signals
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: Node < Object

A node for audio playback.

The AudioStreamPlayer node plays an audio stream non-positionally. It is ideal for user interfaces, menus, or background music.

To use this node, stream needs to be set to a valid AudioStream resource. Playing more than one sound at the same time is also supported, see max_polyphony.

If you need to play audio at a specific position, use AudioStreamPlayer2D or AudioStreamPlayer3D instead.

2D Dodge The Creeps Demo

Audio Device Changer Demo

Audio Microphone Record Demo

Audio Spectrum Visualizer Demo

get_playback_position()

get_stream_playback()

has_stream_playback()

play(from_position: float = 0.0)

seek(to_position: float)

Emitted when a sound finishes playing without interruptions. This signal is not emitted when calling stop(), or when exiting the tree while sounds are playing.

MixTarget MIX_TARGET_STEREO = 0

The audio will be played only on the first channel. This is the default.

MixTarget MIX_TARGET_SURROUND = 1

The audio will be played on all surround channels.

MixTarget MIX_TARGET_CENTER = 2

The audio will be played on the second channel, which is usually the center.

bool autoplay = false 🔗

void set_autoplay(value: bool)

bool is_autoplay_enabled()

If true, this node calls play() when entering the tree.

StringName bus = &"Master" 🔗

void set_bus(value: StringName)

The target bus name. All sounds from this node will be playing on this bus.

Note: At runtime, if no bus with the given name exists, all sounds will fall back on "Master". See also AudioServer.get_bus_name().

int max_polyphony = 1 🔗

void set_max_polyphony(value: int)

int get_max_polyphony()

The maximum number of sounds this node can play at the same time. Calling play() after this value is reached will cut off the oldest sounds.

MixTarget mix_target = 0 🔗

void set_mix_target(value: MixTarget)

MixTarget get_mix_target()

The mix target channels. Has no effect when two speakers or less are detected (see SpeakerMode).

float pitch_scale = 1.0 🔗

void set_pitch_scale(value: float)

float get_pitch_scale()

The audio's pitch and tempo, as a multiplier of the stream's sample rate. A value of 2.0 doubles the audio's pitch, while a value of 0.5 halves the pitch.

PlaybackType playback_type = 0 🔗

void set_playback_type(value: PlaybackType)

PlaybackType get_playback_type()

Experimental: This property may be changed or removed in future versions.

The playback type of the stream player. If set other than to the default value, it will force that playback type.

bool playing = false 🔗

void set_playing(value: bool)

If true, this node is playing sounds. Setting this property has the same effect as play() and stop().

void set_stream(value: AudioStream)

AudioStream get_stream()

The AudioStream resource to be played. Setting this property stops all currently playing sounds. If left empty, the AudioStreamPlayer does not work.

bool stream_paused = false 🔗

void set_stream_paused(value: bool)

bool get_stream_paused()

If true, the sounds are paused. Setting stream_paused to false resumes all sounds.

Note: This property is automatically changed when exiting or entering the tree, or this node is paused (see Node.process_mode).

float volume_db = 0.0 🔗

void set_volume_db(value: float)

float get_volume_db()

Volume of sound, in decibels. This is an offset of the stream's volume.

Note: To convert between decibel and linear energy (like most volume sliders do), use volume_linear, or @GlobalScope.db_to_linear() and @GlobalScope.linear_to_db().

float volume_linear 🔗

void set_volume_linear(value: float)

float get_volume_linear()

Volume of sound, as a linear value.

Note: This member modifies volume_db for convenience. The returned value is equivalent to the result of @GlobalScope.db_to_linear() on volume_db. Setting this member is equivalent to setting volume_db to the result of @GlobalScope.linear_to_db() on a value.

float get_playback_position() 🔗

Returns the position in the AudioStream of the latest sound, in seconds. Returns 0.0 if no sounds are playing.

Note: The position is not always accurate, as the AudioServer does not mix audio every processed frame. To get more accurate results, add AudioServer.get_time_since_last_mix() to the returned position.

Note: This method always returns 0.0 if the stream is an AudioStreamInteractive, since it can have multiple clips playing at once.

AudioStreamPlayback get_stream_playback() 🔗

Returns the latest AudioStreamPlayback of this node, usually the most recently created by play(). If no sounds are playing, this method fails and returns an empty playback.

bool has_stream_playback() 🔗

Returns true if any sound is active, even if stream_paused is set to true. See also playing and get_stream_playback().

void play(from_position: float = 0.0) 🔗

Plays a sound from the beginning, or the given from_position in seconds.

void seek(to_position: float) 🔗

Restarts all sounds to be played from the given to_position, in seconds. Does nothing if no sounds are playing.

Stops all sounds from this node.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## AudioStreamPlayer2D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer2d.html

**Contents:**
- AudioStreamPlayer2D
- Description
- Tutorials
- Properties
- Methods
- Signals
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: Node2D < CanvasItem < Node < Object

Plays positional sound in 2D space.

Plays audio that is attenuated with distance to the listener.

By default, audio is heard from the screen center. This can be changed by adding an AudioListener2D node to the scene and enabling it by calling AudioListener2D.make_current() on it.

See also AudioStreamPlayer to play a sound non-positionally.

Note: Hiding an AudioStreamPlayer2D node does not disable its audio output. To temporarily disable an AudioStreamPlayer2D's audio output, set volume_db to a very low value like -100 (which isn't audible to human hearing).

get_playback_position()

get_stream_playback()

has_stream_playback()

play(from_position: float = 0.0)

seek(to_position: float)

Emitted when the audio stops playing.

void set_area_mask(value: int)

Determines which Area2D layers affect the sound for reverb and audio bus effects. Areas can be used to redirect AudioStreams so that they play in a certain audio bus. An example of how you might use this is making a "water" area so that sounds played in the water are redirected through an audio bus to make them sound like they are being played underwater.

float attenuation = 1.0 🔗

void set_attenuation(value: float)

float get_attenuation()

The volume is attenuated over distance with this as an exponent.

bool autoplay = false 🔗

void set_autoplay(value: bool)

bool is_autoplay_enabled()

If true, audio plays when added to scene tree.

StringName bus = &"Master" 🔗

void set_bus(value: StringName)

Bus on which this audio is playing.

Note: When setting this property, keep in mind that no validation is performed to see if the given name matches an existing bus. This is because audio bus layouts might be loaded after this property is set. If this given name can't be resolved at runtime, it will fall back to "Master".

float max_distance = 2000.0 🔗

void set_max_distance(value: float)

float get_max_distance()

Maximum distance from which audio is still hearable.

int max_polyphony = 1 🔗

void set_max_polyphony(value: int)

int get_max_polyphony()

The maximum number of sounds this node can play at the same time. Playing additional sounds after this value is reached will cut off the oldest sounds.

float panning_strength = 1.0 🔗

void set_panning_strength(value: float)

float get_panning_strength()

Scales the panning strength for this node by multiplying the base ProjectSettings.audio/general/2d_panning_strength with this factor. Higher values will pan audio from left to right more dramatically than lower values.

float pitch_scale = 1.0 🔗

void set_pitch_scale(value: float)

float get_pitch_scale()

The pitch and the tempo of the audio, as a multiplier of the audio sample's sample rate.

PlaybackType playback_type = 0 🔗

void set_playback_type(value: PlaybackType)

PlaybackType get_playback_type()

Experimental: This property may be changed or removed in future versions.

The playback type of the stream player. If set other than to the default value, it will force that playback type.

bool playing = false 🔗

void set_playing(value: bool)

If true, audio is playing or is queued to be played (see play()).

void set_stream(value: AudioStream)

AudioStream get_stream()

The AudioStream object to be played.

bool stream_paused = false 🔗

void set_stream_paused(value: bool)

bool get_stream_paused()

If true, the playback is paused. You can resume it by setting stream_paused to false.

float volume_db = 0.0 🔗

void set_volume_db(value: float)

float get_volume_db()

Base volume before attenuation, in decibels.

float volume_linear 🔗

void set_volume_linear(value: float)

float get_volume_linear()

Base volume before attenuation, as a linear value.

Note: This member modifies volume_db for convenience. The returned value is equivalent to the result of @GlobalScope.db_to_linear() on volume_db. Setting this member is equivalent to setting volume_db to the result of @GlobalScope.linear_to_db() on a value.

float get_playback_position() 🔗

Returns the position in the AudioStream.

AudioStreamPlayback get_stream_playback() 🔗

Returns the AudioStreamPlayback object associated with this AudioStreamPlayer2D.

bool has_stream_playback() 🔗

Returns whether the AudioStreamPlayer can return the AudioStreamPlayback object or not.

void play(from_position: float = 0.0) 🔗

Queues the audio to play on the next physics frame, from the given position from_position, in seconds.

void seek(to_position: float) 🔗

Sets the position from which audio will be played, in seconds.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## AudioStreamPlayer3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer3d.html

**Contents:**
- AudioStreamPlayer3D
- Description
- Tutorials
- Properties
- Methods
- Signals
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: Node3D < Node < Object

Plays positional sound in 3D space.

Plays audio with positional sound effects, based on the relative position of the audio listener. Positional effects include distance attenuation, directionality, and the Doppler effect. For greater realism, a low-pass filter is applied to distant sounds. This can be disabled by setting attenuation_filter_cutoff_hz to 20500.

By default, audio is heard from the camera position. This can be changed by adding an AudioListener3D node to the scene and enabling it by calling AudioListener3D.make_current() on it.

See also AudioStreamPlayer to play a sound non-positionally.

Note: Hiding an AudioStreamPlayer3D node does not disable its audio output. To temporarily disable an AudioStreamPlayer3D's audio output, set volume_db to a very low value like -100 (which isn't audible to human hearing).

attenuation_filter_cutoff_hz

attenuation_filter_db

emission_angle_degrees

emission_angle_enabled

emission_angle_filter_attenuation_db

get_playback_position()

get_stream_playback()

has_stream_playback()

play(from_position: float = 0.0)

seek(to_position: float)

Emitted when the audio stops playing.

enum AttenuationModel: 🔗

AttenuationModel ATTENUATION_INVERSE_DISTANCE = 0

Attenuation of loudness according to linear distance.

AttenuationModel ATTENUATION_INVERSE_SQUARE_DISTANCE = 1

Attenuation of loudness according to squared distance.

AttenuationModel ATTENUATION_LOGARITHMIC = 2

Attenuation of loudness according to logarithmic distance.

AttenuationModel ATTENUATION_DISABLED = 3

No attenuation of loudness according to distance. The sound will still be heard positionally, unlike an AudioStreamPlayer. ATTENUATION_DISABLED can be combined with a max_distance value greater than 0.0 to achieve linear attenuation clamped to a sphere of a defined size.

enum DopplerTracking: 🔗

DopplerTracking DOPPLER_TRACKING_DISABLED = 0

Disables doppler tracking.

DopplerTracking DOPPLER_TRACKING_IDLE_STEP = 1

Executes doppler tracking during process frames (see Node.NOTIFICATION_INTERNAL_PROCESS).

DopplerTracking DOPPLER_TRACKING_PHYSICS_STEP = 2

Executes doppler tracking during physics frames (see Node.NOTIFICATION_INTERNAL_PHYSICS_PROCESS).

void set_area_mask(value: int)

Determines which Area3D layers affect the sound for reverb and audio bus effects. Areas can be used to redirect AudioStreams so that they play in a certain audio bus. An example of how you might use this is making a "water" area so that sounds played in the water are redirected through an audio bus to make them sound like they are being played underwater.

float attenuation_filter_cutoff_hz = 5000.0 🔗

void set_attenuation_filter_cutoff_hz(value: float)

float get_attenuation_filter_cutoff_hz()

The cutoff frequency of the attenuation low-pass filter, in Hz. A sound above this frequency is attenuated more than a sound below this frequency. To disable this effect, set this to 20500 as this frequency is above the human hearing limit.

float attenuation_filter_db = -24.0 🔗

void set_attenuation_filter_db(value: float)

float get_attenuation_filter_db()

Amount how much the filter affects the loudness, in decibels.

AttenuationModel attenuation_model = 0 🔗

void set_attenuation_model(value: AttenuationModel)

AttenuationModel get_attenuation_model()

Decides if audio should get quieter with distance linearly, quadratically, logarithmically, or not be affected by distance, effectively disabling attenuation.

bool autoplay = false 🔗

void set_autoplay(value: bool)

bool is_autoplay_enabled()

If true, audio plays when the AudioStreamPlayer3D node is added to scene tree.

StringName bus = &"Master" 🔗

void set_bus(value: StringName)

The bus on which this audio is playing.

Note: When setting this property, keep in mind that no validation is performed to see if the given name matches an existing bus. This is because audio bus layouts might be loaded after this property is set. If this given name can't be resolved at runtime, it will fall back to "Master".

DopplerTracking doppler_tracking = 0 🔗

void set_doppler_tracking(value: DopplerTracking)

DopplerTracking get_doppler_tracking()

Decides in which step the Doppler effect should be calculated.

Note: If doppler_tracking is not DOPPLER_TRACKING_DISABLED but the current Camera3D/AudioListener3D has doppler tracking disabled, the Doppler effect will be heard but will not take the movement of the current listener into account. If accurate Doppler effect is desired, doppler tracking should be enabled on both the AudioStreamPlayer3D and the current Camera3D/AudioListener3D.

float emission_angle_degrees = 45.0 🔗

void set_emission_angle(value: float)

float get_emission_angle()

The angle in which the audio reaches a listener unattenuated.

bool emission_angle_enabled = false 🔗

void set_emission_angle_enabled(value: bool)

bool is_emission_angle_enabled()

If true, the audio should be attenuated according to the direction of the sound.

float emission_angle_filter_attenuation_db = -12.0 🔗

void set_emission_angle_filter_attenuation_db(value: float)

float get_emission_angle_filter_attenuation_db()

Attenuation factor used if listener is outside of emission_angle_degrees and emission_angle_enabled is set, in decibels.

void set_max_db(value: float)

Sets the absolute maximum of the sound level, in decibels.

float max_distance = 0.0 🔗

void set_max_distance(value: float)

float get_max_distance()

The distance past which the sound can no longer be heard at all. Only has an effect if set to a value greater than 0.0. max_distance works in tandem with unit_size. However, unlike unit_size whose behavior depends on the attenuation_model, max_distance always works in a linear fashion. This can be used to prevent the AudioStreamPlayer3D from requiring audio mixing when the listener is far away, which saves CPU resources.

int max_polyphony = 1 🔗

void set_max_polyphony(value: int)

int get_max_polyphony()

The maximum number of sounds this node can play at the same time. Playing additional sounds after this value is reached will cut off the oldest sounds.

float panning_strength = 1.0 🔗

void set_panning_strength(value: float)

float get_panning_strength()

Scales the panning strength for this node by multiplying the base ProjectSettings.audio/general/3d_panning_strength by this factor. If the product is 0.0 then stereo panning is disabled and the volume is the same for all channels. If the product is 1.0 then one of the channels will be muted when the sound is located exactly to the left (or right) of the listener.

Two speaker stereo arrangements implement the WebAudio standard for StereoPannerNode Panning where the volume is cosine of half the azimuth angle to the ear.

For other speaker arrangements such as the 5.1 and 7.1 the SPCAP (Speaker-Placement Correction Amplitude) algorithm is implemented.

float pitch_scale = 1.0 🔗

void set_pitch_scale(value: float)

float get_pitch_scale()

The pitch and the tempo of the audio, as a multiplier of the audio sample's sample rate.

PlaybackType playback_type = 0 🔗

void set_playback_type(value: PlaybackType)

PlaybackType get_playback_type()

Experimental: This property may be changed or removed in future versions.

The playback type of the stream player. If set other than to the default value, it will force that playback type.

bool playing = false 🔗

void set_playing(value: bool)

If true, audio is playing or is queued to be played (see play()).

void set_stream(value: AudioStream)

AudioStream get_stream()

The AudioStream resource to be played.

bool stream_paused = false 🔗

void set_stream_paused(value: bool)

bool get_stream_paused()

If true, the playback is paused. You can resume it by setting stream_paused to false.

float unit_size = 10.0 🔗

void set_unit_size(value: float)

float get_unit_size()

The factor for the attenuation effect. Higher values make the sound audible over a larger distance.

float volume_db = 0.0 🔗

void set_volume_db(value: float)

float get_volume_db()

The base sound level before attenuation, in decibels.

float volume_linear 🔗

void set_volume_linear(value: float)

float get_volume_linear()

The base sound level before attenuation, as a linear value.

Note: This member modifies volume_db for convenience. The returned value is equivalent to the result of @GlobalScope.db_to_linear() on volume_db. Setting this member is equivalent to setting volume_db to the result of @GlobalScope.linear_to_db() on a value.

float get_playback_position() 🔗

Returns the position in the AudioStream.

AudioStreamPlayback get_stream_playback() 🔗

Returns the AudioStreamPlayback object associated with this AudioStreamPlayer3D.

bool has_stream_playback() 🔗

Returns whether the AudioStreamPlayer can return the AudioStreamPlayback object or not.

void play(from_position: float = 0.0) 🔗

Queues the audio to play on the next physics frame, from the given position from_position, in seconds.

void seek(to_position: float) 🔗

Sets the position from which audio will be played, in seconds.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---
