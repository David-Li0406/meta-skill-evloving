/**
 * Hero Section Example
 *
 * Demonstrates the frontend-vibes aesthetic with:
 * - Figlet ASCII art display type
 * - Spring-based entrance animations
 * - Warm dark color palette (#131313, #d97757)
 * - Technical grid background
 * - Expressive motion physics
 *
 * Dependencies:
 * npm install framer-motion figlet @types/figlet
 */

import { motion, useInView } from "framer-motion";
import { useEffect, useState, useRef } from "react";
import figlet from "figlet";
import standard from "figlet/importable-fonts/Standard";

// Spring configurations (from motion-physics-guide.md)
const springs = {
  expressive: { type: "spring" as const, stiffness: 300, damping: 20 },
  gentle: { type: "spring" as const, stiffness: 250, damping: 28 },
};

interface HeroSectionProps {
  title: string;
  subtitle: string;
  ctaPrimary: {
    text: string;
    href: string;
  };
  ctaSecondary?: {
    text: string;
    href: string;
  };
}

export function HeroSection({
  title,
  subtitle,
  ctaPrimary,
  ctaSecondary,
}: HeroSectionProps) {
  const [asciiTitle, setAsciiTitle] = useState<string>("");
  const ref = useRef<HTMLElement>(null);
  const isInView = useInView(ref, { once: true, amount: 0.3 });

  // Generate figlet ASCII art
  useEffect(() => {
    figlet.parseFont("Standard", standard);
    figlet.text(
      title,
      {
        font: "Standard",
        horizontalLayout: "default",
        verticalLayout: "default",
      },
      (err, data) => {
        if (err) {
          console.error("Figlet error:", err);
          setAsciiTitle(title);
          return;
        }
        setAsciiTitle(data || title);
      }
    );
  }, [title]);

  return (
    <section
      ref={ref}
      className="relative min-h-screen flex items-center justify-center overflow-hidden bg-[#131313]"
    >
      {/* Technical grid background */}
      <div className="absolute inset-0 opacity-30">
        <div
          className="absolute inset-0"
          style={{
            backgroundImage: `
              radial-gradient(circle at center, #1a1a1a 1px, transparent 1px)
            `,
            backgroundSize: "32px 32px",
          }}
        />
      </div>

      {/* Subtle glow accent in background */}
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={isInView ? { opacity: 0.15, scale: 1 } : {}}
        transition={{ ...springs.gentle, delay: 0.2 }}
        className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-[#d97757] rounded-full blur-[120px] pointer-events-none"
      />

      {/* Content container */}
      <div className="relative z-10 max-w-5xl mx-auto px-8 py-20 text-center">
        {/* ASCII art title */}
        <motion.pre
          initial={{ opacity: 0, y: 40 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={springs.expressive}
          className="font-mono text-[#d97757] text-xs sm:text-sm md:text-base leading-tight mb-8 overflow-x-auto whitespace-pre"
          style={{
            textShadow: "0 0 20px rgba(217, 119, 87, 0.5)",
          }}
        >
          {asciiTitle}
        </motion.pre>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ ...springs.expressive, delay: 0.2 }}
          className="text-[#faf9f5] text-lg md:text-xl max-w-2xl mx-auto mb-12 leading-relaxed"
        >
          {subtitle}
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ ...springs.expressive, delay: 0.4 }}
          className="flex flex-col sm:flex-row gap-4 justify-center items-center"
        >
          {/* Primary CTA */}
          <motion.a
            href={ctaPrimary.href}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.98 }}
            transition={springs.expressive}
            className="group relative px-8 py-4 bg-[#d97757] text-[#131313] rounded-lg font-semibold text-lg overflow-hidden"
            style={{
              boxShadow: "0 4px 16px rgba(217, 119, 87, 0.3)",
            }}
          >
            {/* Animated glow on hover */}
            <motion.div
              className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-0 group-hover:opacity-20"
              initial={{ x: "-100%" }}
              whileHover={{ x: "100%" }}
              transition={{ duration: 0.6, ease: "easeInOut" }}
            />
            <span className="relative z-10">{ctaPrimary.text}</span>
          </motion.a>

          {/* Secondary CTA */}
          {ctaSecondary && (
            <motion.a
              href={ctaSecondary.href}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.98 }}
              transition={springs.expressive}
              className="px-8 py-4 border-2 border-[#d97757] text-[#d97757] rounded-lg font-semibold text-lg hover:bg-[#d97757]/10"
            >
              {ctaSecondary.text}
            </motion.a>
          )}
        </motion.div>

        {/* Decorative scanline effect */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={isInView ? { opacity: 0.1 } : {}}
          transition={{ ...springs.gentle, delay: 0.6 }}
          className="absolute inset-0 pointer-events-none"
          style={{
            backgroundImage: `repeating-linear-gradient(
              0deg,
              transparent,
              transparent 2px,
              #d97757 2px,
              #d97757 3px
            )`,
          }}
        />
      </div>

      {/* Scroll indicator */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={isInView ? { opacity: 0.6, y: 0 } : {}}
        transition={{ ...springs.gentle, delay: 0.8 }}
        className="absolute bottom-12 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-[#faf9f5]/60"
      >
        <span className="text-sm font-mono">SCROLL</span>
        <motion.div
          animate={{ y: [0, 8, 0] }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        >
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M12 5v14M19 12l-7 7-7-7" />
          </svg>
        </motion.div>
      </motion.div>
    </section>
  );
}

// Usage Example
export default function HeroExample() {
  return (
    <HeroSection
      title="VIBES"
      subtitle="Create distinctive frontend interfaces that balance technical precision with organic imperfection. Where constraint becomes style."
      ctaPrimary={{
        text: "Get Started",
        href: "#start",
      }}
      ctaSecondary={{
        text: "View Examples",
        href: "#examples",
      }}
    />
  );
}
