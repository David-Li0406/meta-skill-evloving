# Remotion Kinetic Typography Template

## Composition Structure

```tsx
import { AbsoluteFill, Audio, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

// Types
interface Word {
  word: string;
  start: number;
  end: number;
}

interface Segment {
  name: string;
  time_range: [number, number];
  style: string;
  background: string;
  word_treatment: string;
  emphasis_words: string[];
  transition_out: string;
}

interface Props {
  words: Word[];
  segments: Segment[];
  audioFile: string;
}

// Main Composition
export const KineticTypography: React.FC<Props> = ({ words, segments, audioFile }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentTime = frame / fps;

  // Find current segment
  const currentSegment = segments.find(
    seg => currentTime >= seg.time_range[0] && currentTime < seg.time_range[1]
  ) || segments[0];

  return (
    <AbsoluteFill>
      {/* Dynamic Background */}
      <SegmentBackground segment={currentSegment} frame={frame} fps={fps} />

      {/* Words Layer */}
      <WordsLayer
        words={words}
        currentTime={currentTime}
        segment={currentSegment}
        frame={frame}
        fps={fps}
      />

      {/* Audio */}
      <Audio src={audioFile} />
    </AbsoluteFill>
  );
};
```

## Dynamic Backgrounds

```tsx
const SegmentBackground: React.FC<{segment: Segment; frame: number; fps: number}> = ({
  segment, frame, fps
}) => {
  const backgrounds: Record<string, React.ReactNode> = {
    'dark-gradient': (
      <AbsoluteFill style={{
        background: 'linear-gradient(180deg, #0a0a0a 0%, #1a1a2e 100%)'
      }} />
    ),

    'animated-particles': (
      <AbsoluteFill style={{
        background: '#0a0a0a'
      }}>
        {/* Add particle animation here */}
        <ParticleField frame={frame} />
      </AbsoluteFill>
    ),

    'radial-glow': (
      <AbsoluteFill style={{
        background: `radial-gradient(circle at 50% 50%,
          rgba(99, 102, 241, ${0.3 + Math.sin(frame / 30) * 0.1}) 0%,
          #0a0a0a 70%)`
      }} />
    ),

    'soft-gradient': (
      <AbsoluteFill style={{
        background: 'linear-gradient(180deg, #1a1a2e 0%, #2d1b4e 50%, #1a1a2e 100%)'
      }} />
    ),
  };

  return backgrounds[segment.background] || backgrounds['dark-gradient'];
};
```

## Word Treatment Animations

```tsx
const getWordAnimation = (
  treatment: string,
  frame: number,
  fps: number,
  wordStart: number,
  wordEnd: number,
  isEmphasis: boolean
) => {
  const wordStartFrame = wordStart * fps;
  const wordEndFrame = wordEnd * fps;
  const wordDuration = wordEndFrame - wordStartFrame;

  // Entrance animation (first 10 frames of word)
  const entranceProgress = interpolate(
    frame,
    [wordStartFrame, wordStartFrame + 10],
    [0, 1],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  // Exit animation (last 8 frames of word visibility window)
  const exitProgress = interpolate(
    frame,
    [wordEndFrame + 15, wordEndFrame + 23],
    [1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  const treatments: Record<string, React.CSSProperties> = {
    'fade-in-center': {
      opacity: entranceProgress * exitProgress,
      transform: `scale(${0.9 + entranceProgress * 0.1})`,
    },

    'slide-from-sides': {
      opacity: entranceProgress * exitProgress,
      transform: `translateX(${(1 - entranceProgress) * 100}px)`,
    },

    'scale-bounce': {
      opacity: entranceProgress * exitProgress,
      transform: `scale(${spring({
        frame: frame - wordStartFrame,
        fps,
        config: { damping: 12, stiffness: 200 },
        durationInFrames: 15,
      }) * (isEmphasis ? 1.3 : 1)})`,
    },

    'rotate-in': {
      opacity: entranceProgress * exitProgress,
      transform: `rotate(${(1 - entranceProgress) * 15}deg)`,
    },

    'blur-reveal': {
      opacity: entranceProgress * exitProgress,
      filter: `blur(${(1 - entranceProgress) * 10}px)`,
    },

    'color-shift': {
      opacity: entranceProgress * exitProgress,
      color: interpolateColors(
        entranceProgress,
        [0, 1],
        ['#666666', isEmphasis ? '#6366f1' : '#ffffff']
      ),
    },
  };

  return treatments[treatment] || treatments['fade-in-center'];
};
```

## Words Layer with Segment-Based Styling

```tsx
const WordsLayer: React.FC<{
  words: Word[];
  currentTime: number;
  segment: Segment;
  frame: number;
  fps: number;
}> = ({ words, currentTime, segment, frame, fps }) => {

  // Get visible words (current + recent for context)
  const visibleWords = words.filter(w => {
    const wordEnd = w.end;
    const visibilityWindow = currentTime - w.start;
    return visibilityWindow >= -0.1 && visibilityWindow < 2; // Show for 2 seconds after start
  });

  // Layout varies by segment style
  const getLayout = (style: string) => {
    switch (style) {
      case 'minimal-dramatic':
        return {
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          flexWrap: 'wrap' as const,
          gap: '20px',
          padding: '0 100px'
        };
      case 'dynamic-stack':
        return {
          display: 'flex',
          flexDirection: 'column' as const,
          justifyContent: 'center',
          alignItems: 'center',
          gap: '15px'
        };
      case 'explosive-center':
        return {
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          flexWrap: 'wrap' as const,
          gap: '25px',
          padding: '0 50px'
        };
      default:
        return {
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          flexWrap: 'wrap' as const,
          gap: '20px'
        };
    }
  };

  const getFontSize = (style: string, isEmphasis: boolean) => {
    const baseSizes: Record<string, number> = {
      'minimal-dramatic': 120,
      'dynamic-stack': 80,
      'explosive-center': 140,
      'slide-cascade': 70,
      'calm-elegant': 90,
    };
    const base = baseSizes[style] || 80;
    return isEmphasis ? base * 1.3 : base;
  };

  return (
    <AbsoluteFill style={getLayout(segment.style)}>
      {visibleWords.map((word, i) => {
        const isEmphasis = segment.emphasis_words.includes(word.word);
        const animation = getWordAnimation(
          segment.word_treatment,
          frame,
          fps,
          word.start,
          word.end,
          isEmphasis
        );

        return (
          <span
            key={`${word.word}-${i}`}
            style={{
              fontSize: getFontSize(segment.style, isEmphasis),
              fontWeight: isEmphasis ? 900 : 700,
              color: isEmphasis ? '#6366f1' : '#ffffff',
              textShadow: isEmphasis
                ? '0 0 40px rgba(99, 102, 241, 0.5)'
                : 'none',
              fontFamily: 'Inter, sans-serif',
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
              ...animation,
            }}
          >
            {word.word}
          </span>
        );
      })}
    </AbsoluteFill>
  );
};
```

## Particle Field Background (Optional)

```tsx
const ParticleField: React.FC<{frame: number}> = ({ frame }) => {
  const particles = useMemo(() =>
    Array.from({ length: 50 }, (_, i) => ({
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: 2 + Math.random() * 4,
      speed: 0.5 + Math.random() * 1,
      offset: Math.random() * 1000,
    })), []
  );

  return (
    <>
      {particles.map((p, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            left: `${p.x}%`,
            top: `${(p.y + (frame * p.speed * 0.1) + p.offset) % 120 - 10}%`,
            width: p.size,
            height: p.size,
            borderRadius: '50%',
            background: `rgba(99, 102, 241, ${0.3 + Math.sin((frame + p.offset) / 20) * 0.2})`,
          }}
        />
      ))}
    </>
  );
};
```

## Segment Transitions

```tsx
const SegmentTransition: React.FC<{
  type: string;
  progress: number;
}> = ({ type, progress }) => {
  const transitions: Record<string, React.CSSProperties> = {
    'fade-to-black': {
      position: 'absolute',
      inset: 0,
      background: '#000',
      opacity: progress,
    },
    'zoom-blur': {
      position: 'absolute',
      inset: 0,
      background: '#000',
      opacity: progress,
      filter: `blur(${progress * 20}px)`,
      transform: `scale(${1 + progress * 0.2})`,
    },
    'flash-white': {
      position: 'absolute',
      inset: 0,
      background: '#fff',
      opacity: progress > 0.5 ? (1 - progress) * 2 : progress * 2,
    },
  };

  return <div style={transitions[type] || transitions['fade-to-black']} />;
};
```

## Usage in Root.tsx

```tsx
import { Composition } from 'remotion';
import { KineticTypography } from './compositions/KineticTypography';

export const RemotionRoot = () => {
  return (
    <Composition
      id="KineticTypography"
      component={KineticTypography}
      durationInFrames={3600} // Adjust based on audio length
      fps={30}
      width={1080}
      height={1920} // 9:16 vertical for social
      defaultProps={{
        words: [], // Loaded from transcript.json
        segments: [], // Loaded from storyboard.json
        audioFile: 'speech_with_music.mp3',
      }}
    />
  );
};
```

## Key Principles

1. **Storyboard-Driven**: Segment determines style, not hardcoded
2. **Word-Level Sync**: Each word appears at exact timestamp
3. **Spring Animations**: Natural, bouncy motion over linear
4. **Emphasis Detection**: Special words get extra treatment
5. **Varied Layouts**: Different segments = different visual approaches
6. **Smooth Transitions**: Segment changes feel intentional
