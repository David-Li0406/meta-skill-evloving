/**
 * ASCII Text Effect Component
 *
 * Reusable component for rendering text as ASCII art using figlet.
 * Demonstrates the frontend-vibes aesthetic with:
 * - Multiple font options
 * - Animated character-by-character reveal
 * - Scanline overlay effect
 * - Warm color palette
 * - Spring-based animations
 *
 * Dependencies:
 * npm install framer-motion figlet @types/figlet
 */

import { motion } from "framer-motion";
import { useEffect, useState } from "react";
import figlet from "figlet";
import standard from "figlet/importable-fonts/Standard";
import slant from "figlet/importable-fonts/Slant";
import banner from "figlet/importable-fonts/Banner";

export type FigletFont = "Standard" | "Slant" | "Banner";

interface ASCIITextEffectProps {
  text: string;
  font?: FigletFont;
  color?: string;
  animate?: boolean;
  scanlines?: boolean;
  glow?: boolean;
  className?: string;
}

// Font imports mapping
const fontImports = {
  Standard: standard,
  Slant: slant,
  Banner: banner,
};

export function ASCIITextEffect({
  text,
  font = "Standard",
  color = "#d97757", // Terracotta accent
  animate = true,
  scanlines = false,
  glow = false,
  className = "",
}: ASCIITextEffectProps) {
  const [asciiArt, setAsciiArt] = useState<string>("");
  const [lines, setLines] = useState<string[]>([]);

  useEffect(() => {
    // Load the selected font
    figlet.parseFont(font, fontImports[font]);

    // Generate ASCII art
    figlet.text(
      text,
      {
        font,
        horizontalLayout: "default",
        verticalLayout: "default",
      },
      (err, data) => {
        if (err) {
          console.error("Figlet error:", err);
          setAsciiArt(text);
          setLines([text]);
          return;
        }

        const artLines = data?.split("\n") || [text];
        setAsciiArt(data || text);
        setLines(artLines);
      }
    );
  }, [text, font]);

  if (!asciiArt) {
    return (
      <div className={`font-mono text-sm ${className}`}>
        <span style={{ color }}>Loading...</span>
      </div>
    );
  }

  return (
    <div className={`relative ${className}`}>
      {/* ASCII art container */}
      <pre
        className="font-mono text-xs sm:text-sm md:text-base leading-tight overflow-x-auto whitespace-pre"
        style={{
          color,
          textShadow: glow ? `0 0 20px ${color}80` : "none",
        }}
      >
        {animate ? (
          // Animated line-by-line reveal
          lines.map((line, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{
                type: "spring",
                stiffness: 300,
                damping: 20,
                delay: index * 0.05, // Stagger each line
              }}
            >
              {line}
            </motion.div>
          ))
        ) : (
          // Static rendering
          asciiArt
        )}
      </pre>

      {/* Scanline overlay effect */}
      {scanlines && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.15 }}
          transition={{ duration: 0.5 }}
          className="absolute inset-0 pointer-events-none"
          style={{
            backgroundImage: `repeating-linear-gradient(
              0deg,
              transparent,
              transparent 2px,
              ${color} 2px,
              ${color} 3px
            )`,
          }}
        />
      )}
    </div>
  );
}

/**
 * Typewriter ASCII Effect
 *
 * Character-by-character reveal with blinking cursor
 */
interface TypewriterASCIIProps {
  text: string;
  font?: FigletFont;
  color?: string;
  typingSpeed?: number; // milliseconds per character
  className?: string;
}

export function TypewriterASCII({
  text,
  font = "Standard",
  color = "#d97757",
  typingSpeed = 30,
  className = "",
}: TypewriterASCIIProps) {
  const [asciiArt, setAsciiArt] = useState<string>("");
  const [displayedText, setDisplayedText] = useState<string>("");
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isComplete, setIsComplete] = useState(false);

  // Generate ASCII art
  useEffect(() => {
    figlet.parseFont(font, fontImports[font]);
    figlet.text(
      text,
      { font, horizontalLayout: "default", verticalLayout: "default" },
      (err, data) => {
        if (!err && data) {
          setAsciiArt(data);
        }
      }
    );
  }, [text, font]);

  // Typewriter effect
  useEffect(() => {
    if (!asciiArt) return;

    if (currentIndex < asciiArt.length) {
      const timeout = setTimeout(() => {
        setDisplayedText((prev) => prev + asciiArt[currentIndex]);
        setCurrentIndex((prev) => prev + 1);
      }, typingSpeed);

      return () => clearTimeout(timeout);
    } else {
      setIsComplete(true);
    }
  }, [asciiArt, currentIndex, typingSpeed]);

  return (
    <div className={`relative ${className}`}>
      <pre
        className="font-mono text-xs sm:text-sm md:text-base leading-tight overflow-x-auto whitespace-pre"
        style={{ color }}
      >
        {displayedText}
        {!isComplete && (
          <motion.span
            animate={{ opacity: [1, 0, 1] }}
            transition={{ duration: 0.8, repeat: Infinity }}
            className="inline-block w-2 h-4 bg-current ml-1"
          />
        )}
      </pre>
    </div>
  );
}

/**
 * Glitch ASCII Effect
 *
 * Scramble/glitch effect before resolving to final text
 */
interface GlitchASCIIProps {
  text: string;
  font?: FigletFont;
  color?: string;
  glitchDuration?: number; // milliseconds
  className?: string;
}

const GLITCH_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`";

export function GlitchASCII({
  text,
  font = "Standard",
  color = "#d97757",
  glitchDuration = 800,
  className = "",
}: GlitchASCIIProps) {
  const [asciiArt, setAsciiArt] = useState<string>("");
  const [displayedText, setDisplayedText] = useState<string>("");
  const [isGlitching, setIsGlitching] = useState(true);

  // Generate ASCII art
  useEffect(() => {
    figlet.parseFont(font, fontImports[font]);
    figlet.text(
      text,
      { font, horizontalLayout: "default", verticalLayout: "default" },
      (err, data) => {
        if (!err && data) {
          setAsciiArt(data);
          setDisplayedText(data); // Initial glitched version
        }
      }
    );
  }, [text, font]);

  // Glitch effect
  useEffect(() => {
    if (!asciiArt || !isGlitching) return;

    const glitchInterval = setInterval(() => {
      // Randomly replace characters with glitch chars
      const glitched = asciiArt
        .split("")
        .map((char) => {
          if (char === " " || char === "\n") return char;
          return Math.random() > 0.7
            ? GLITCH_CHARS[Math.floor(Math.random() * GLITCH_CHARS.length)]
            : char;
        })
        .join("");

      setDisplayedText(glitched);
    }, 50);

    // Stop glitching after duration
    const stopTimeout = setTimeout(() => {
      setIsGlitching(false);
      setDisplayedText(asciiArt);
    }, glitchDuration);

    return () => {
      clearInterval(glitchInterval);
      clearTimeout(stopTimeout);
    };
  }, [asciiArt, isGlitching, glitchDuration]);

  return (
    <div className={`relative ${className}`}>
      <motion.pre
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="font-mono text-xs sm:text-sm md:text-base leading-tight overflow-x-auto whitespace-pre"
        style={{
          color,
          textShadow: isGlitching ? `0 0 10px ${color}` : "none",
        }}
      >
        {displayedText}
      </motion.pre>
    </div>
  );
}

// Usage Examples
export default function ASCIIExamples() {
  return (
    <div className="min-h-screen bg-[#131313] p-8 space-y-16">
      <div className="max-w-5xl mx-auto space-y-16">
        {/* Standard animated ASCII */}
        <section>
          <h2 className="text-2xl font-bold text-[#faf9f5] mb-6">
            Standard ASCII (Animated)
          </h2>
          <ASCIITextEffect
            text="FRONTEND"
            font="Standard"
            animate={true}
            glow={true}
            scanlines={false}
          />
        </section>

        {/* Slant font with scanlines */}
        <section>
          <h2 className="text-2xl font-bold text-[#faf9f5] mb-6">
            Slant Font (With Scanlines)
          </h2>
          <ASCIITextEffect
            text="VIBES"
            font="Slant"
            animate={true}
            glow={false}
            scanlines={true}
          />
        </section>

        {/* Typewriter effect */}
        <section>
          <h2 className="text-2xl font-bold text-[#faf9f5] mb-6">
            Typewriter Effect
          </h2>
          <TypewriterASCII
            text="CODE"
            font="Banner"
            typingSpeed={30}
          />
        </section>

        {/* Glitch effect */}
        <section>
          <h2 className="text-2xl font-bold text-[#faf9f5] mb-6">
            Glitch Effect
          </h2>
          <GlitchASCII
            text="TECH"
            font="Standard"
            glitchDuration={1200}
          />
        </section>
      </div>
    </div>
  );
}
