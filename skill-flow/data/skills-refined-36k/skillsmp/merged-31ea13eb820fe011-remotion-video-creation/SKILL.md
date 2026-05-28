---
name: remotion-video-creation
description: Use this skill when you need to create programmatic videos in React using Remotion, including animations, compositions, and media handling.
---

# Remotion - Video Creation in React

This skill set provides comprehensive guidance for creating programmatic videos using Remotion, a framework for video creation in React.

## When to use

Use this skill whenever you are working with Remotion code to gain domain-specific knowledge about:

- Creating video compositions with React components
- Animating elements using frame-based animations
- Working with audio, video, and image assets
- Building charts and data visualizations
- Implementing text animations and captions
- Using 3D content with Three.js
- Applying transitions and sequencing
- Integrating Tailwind CSS and Lottie animations

## Core Concepts

Remotion allows you to create videos using:
- **React Components**: Build video content with familiar React syntax
- **Frame-based Animations**: All animations driven by `useCurrentFrame()` hook
- **Compositions**: Define video compositions with duration, dimensions, and props
- **Assets**: Import and manipulate images, videos, audio, and fonts
- **Rendering**: Export videos programmatically with customizable settings

## Key Features

- Frame-by-frame control over animations
- Dynamic metadata calculation
- Media processing (trimming, volume, speed, pitch)
- Caption generation and display
- Data visualization with charts
- 3D content integration
- Professional text animations
- Scene transitions and sequencing

## How to use

Read individual rule files for detailed explanations and code examples:

- **3D Content**: [3d.md](rules/3d.md) - Using Three.js and React Three Fiber
- **Animations**: [animations.md](rules/animations.md) - Fundamental animation techniques
- **Assets**: [assets.md](rules/assets.md) - Importing images, videos, audio, and fonts
- **Audio**: [audio.md](rules/audio.md) - Using audio and sound, including trimming and volume
- **Metadata**: [calculate-metadata.md](rules/calculate-metadata.md) - Dynamically set composition properties
- **Decoding**: [can-decode.md](rules/can-decode.md) - Check if a video can be decoded by the browser
- **Charts**: [charts.md](rules/charts.md) - Data visualization patterns
- **Compositions**: [compositions.md](rules/compositions.md) - Defining compositions and dynamic metadata
- **Captions**: [display-captions.md](rules/display-captions.md) - Displaying captions with TikTok-style pages
- **Frame Extraction**: [extract-frames.md](rules/extract-frames.md) - Extract frames from videos
- **Fonts**: [fonts.md](rules/fonts.md) - Loading Google Fonts and local fonts
- **Duration**: [get-audio-duration.md](rules/get-audio-duration.md) - Getting audio file duration
- **Video Dimensions**: [get-video-dimensions.md](rules/get-video-dimensions.md) - Getting video file dimensions
- **Video Duration**: [get-video-duration.md](rules/get-video-duration.md) - Getting video file duration
- **GIFs**: [gifs.md](rules/gifs.md) - Displaying GIFs synchronized with the timeline
- **Images**: [images.md](rules/images.md) - Embedding images using the Img component
- **SRT Captions**: [import-srt-captions.md](rules/import-srt-captions.md) - Importing .srt subtitle files
- **Lottie**: [lottie.md](rules/lottie.md) - Embedding Lottie animations
- **DOM Measurement**: [measuring-dom-nodes.md](rules/measuring-dom-nodes.md) - Measuring DOM element dimensions
- **Text Measurement**: [measuring-text.md](rules/measuring-text.md) - Measuring text dimensions and overflow
- **Sequencing**: [sequencing.md](rules/sequencing.md) - Sequencing patterns for animations
- **Tailwind**: [tailwind.md](rules/tailwind.md) - Using TailwindCSS in Remotion
- **Text Animations**: [text-animations.md](rules/text-animations.md) - Typography and text animation patterns
- **Timing**: [timing.md](rules/timing.md) - Interpolation curves for animations
- **Transcribing Captions**: [transcribe-captions.md](rules/transcribe-captions.md) - Generating captions from audio
- **Transitions**: [transitions.md](rules/transitions.md) - Scene transition patterns
- **Trimming**: [trimming.md](rules/trimming.md) - Trimming patterns for animations
- **Videos**: [videos.md](rules/videos.md) - Embedding videos with various properties

## Quick Start Example

```tsx
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";

export const MyComposition = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 2 * fps], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <div style={{ opacity }}>
      <h1>Hello Remotion!</h1>
    </div>
  );
};
```

## Best Practices

1. **Always use `useCurrentFrame()`** - Drive all animations from the current frame.
2. **Avoid CSS animations** - They won't render correctly in videos.
3. **Think in seconds** - Multiply time in seconds by `fps` for frame calculations.
4. **Use interpolate for smooth animations** - Built-in interpolation with easing functions.
5. **Clamp extrapolation** - Prevent values from exceeding intended ranges.
6. **Test frequently** - Preview in Remotion Studio before rendering.

## Resources

- **Documentation**: [Remotion Documentation](https://www.remotion.dev/docs)
- **Repository**: [Remotion GitHub](https://github.com/remotion-dev/remotion)
- **Skills Repository**: [Remotion Skills GitHub](https://github.com/remotion-dev/skills)
- **Community**: Discord and GitHub Discussions
- **License**: MIT