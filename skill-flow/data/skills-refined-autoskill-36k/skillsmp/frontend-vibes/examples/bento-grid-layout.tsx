/**
 * Bento Grid Layout Example
 *
 * Demonstrates the frontend-vibes aesthetic with:
 * - Asymmetric grid with varied card sizes
 * - Spring animations on hover
 * - Warm color palette with subtle accents
 * - Technical details and visual hierarchy
 * - Glassmorphism and depth effects
 *
 * Dependencies:
 * npm install framer-motion
 */

import { motion, useInView } from "framer-motion";
import { useRef } from "react";

const springs = {
  expressive: { type: "spring" as const, stiffness: 300, damping: 20 },
  gentle: { type: "spring" as const, stiffness: 250, damping: 28 },
};

interface BentoCardProps {
  title: string;
  description: string;
  icon?: React.ReactNode;
  size: "small" | "medium" | "large";
  accent?: boolean;
  children?: React.ReactNode;
  delay?: number;
}

function BentoCard({
  title,
  description,
  icon,
  size,
  accent = false,
  children,
  delay = 0,
}: BentoCardProps) {
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true, amount: 0.3 });

  const sizeClasses = {
    small: "col-span-1 row-span-1",
    medium: "col-span-1 md:col-span-2 row-span-1",
    large: "col-span-1 md:col-span-2 row-span-2",
  };

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 40 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ ...springs.expressive, delay }}
      whileHover={{ scale: 1.02, y: -4 }}
      className={`
        ${sizeClasses[size]}
        group relative p-6 md:p-8
        rounded-2xl
        ${accent ? "bg-[#d97757]" : "bg-[#1a1a1a]"}
        border border-[#2a2a2a]
        overflow-hidden
        cursor-pointer
      `}
      style={{
        boxShadow: accent
          ? "0 4px 24px rgba(217, 119, 87, 0.2)"
          : "0 4px 16px rgba(0, 0, 0, 0.3)",
      }}
    >
      {/* Subtle dot grid background */}
      <div
        className="absolute inset-0 opacity-20 pointer-events-none"
        style={{
          backgroundImage: `radial-gradient(circle at center, ${accent ? "#ffffff" : "#2a2a2a"} 1px, transparent 1px)`,
          backgroundSize: "24px 24px",
        }}
      />

      {/* Glow effect on hover */}
      <motion.div
        className="absolute inset-0 opacity-0 group-hover:opacity-100 pointer-events-none"
        style={{
          background: accent
            ? "radial-gradient(circle at top left, rgba(255,255,255,0.1), transparent)"
            : "radial-gradient(circle at top left, rgba(217, 119, 87, 0.1), transparent)",
        }}
        transition={springs.gentle}
      />

      <div className="relative z-10 h-full flex flex-col">
        {/* Icon */}
        {icon && (
          <div
            className={`mb-4 ${accent ? "text-[#131313]" : "text-[#d97757]"}`}
          >
            {icon}
          </div>
        )}

        {/* Title */}
        <h3
          className={`
            text-xl md:text-2xl font-bold mb-3
            ${accent ? "text-[#131313]" : "text-[#faf9f5]"}
          `}
        >
          {title}
        </h3>

        {/* Description */}
        <p
          className={`
            text-sm md:text-base leading-relaxed mb-4
            ${accent ? "text-[#131313]/80" : "text-[#faf9f5]/70"}
          `}
        >
          {description}
        </p>

        {/* Custom content */}
        {children && <div className="mt-auto">{children}</div>}

        {/* Border beam effect (subtle animation) */}
        <motion.div
          className="absolute bottom-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-[#d97757] to-transparent opacity-0 group-hover:opacity-100"
          initial={{ x: "-100%" }}
          whileHover={{ x: "100%" }}
          transition={{ duration: 1.5, ease: "easeInOut" }}
        />
      </div>
    </motion.div>
  );
}

interface BentoGridProps {
  title?: string;
  subtitle?: string;
}

export function BentoGrid({ title, subtitle }: BentoGridProps) {
  return (
    <section className="py-20 px-8 bg-[#131313] min-h-screen">
      <div className="max-w-7xl mx-auto">
        {/* Section header */}
        {(title || subtitle) && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={springs.expressive}
            viewport={{ once: true }}
            className="mb-16 text-center"
          >
            {title && (
              <h2 className="text-4xl md:text-5xl font-bold text-[#faf9f5] mb-4">
                {title}
              </h2>
            )}
            {subtitle && (
              <p className="text-lg md:text-xl text-[#faf9f5]/70 max-w-2xl mx-auto">
                {subtitle}
              </p>
            )}
          </motion.div>
        )}

        {/* Bento grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 auto-rows-[240px] gap-6">
          <BentoCard
            title="Faux-ASCII Aesthetic"
            description="Typography and imagery rendered through lo-fi filters—pixelated figures, halftone worlds, characters built from blocks."
            size="medium"
            icon={
              <svg
                width="48"
                height="48"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <rect x="3" y="3" width="18" height="18" />
                <path d="M3 9h18M3 15h18M9 3v18M15 3v18" />
              </svg>
            }
            delay={0}
          />

          <BentoCard
            title="Warm Palettes"
            description="Dark foundations with olive undertones. Terracotta accents that cut through. The 90/10 rule."
            size="small"
            icon={
              <svg
                width="48"
                height="48"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <circle cx="12" cy="12" r="10" />
                <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20" />
              </svg>
            }
            delay={0.1}
          />

          <BentoCard
            title="Expressive Motion"
            description="Replace easing curves with spring physics. Stiffness and damping create motion that feels alive—interruptible, contextual, natural."
            size="large"
            accent={true}
            icon={
              <svg
                width="48"
                height="48"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <path d="M21 12a9 9 0 1 1-6.219-8.56" />
                <path d="M12 3v9l3 3" />
              </svg>
            }
            delay={0.2}
          >
            <div className="mt-6">
              <code className="block text-xs md:text-sm font-mono bg-[#131313] px-4 py-3 rounded-lg">
                <span className="text-[#d97757]">transition</span>: &#123;
                <br />
                &nbsp;&nbsp;stiffness: <span className="text-[#faf9f5]">300</span>,
                <br />
                &nbsp;&nbsp;damping: <span className="text-[#faf9f5]">20</span>
                <br />
                &#125;
              </code>
            </div>
          </BentoCard>

          <BentoCard
            title="Technical Romance"
            description="Line art, isometric views, pixel compositions. Smart enough to feel credible, warm enough to feel approachable."
            size="small"
            icon={
              <svg
                width="48"
                height="48"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <polygon points="12 2 2 7 12 12 22 7 12 2" />
                <polyline points="2 17 12 22 22 17" />
                <polyline points="2 12 12 17 22 12" />
              </svg>
            }
            delay={0.3}
          />

          <BentoCard
            title="Confident Space"
            description="60-120px section padding. Asymmetric layouts. Full-bleed moments that create rhythm through alternation."
            size="medium"
            icon={
              <svg
                width="48"
                height="48"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <rect x="3" y="3" width="7" height="7" />
                <rect x="14" y="3" width="7" height="7" />
                <rect x="14" y="14" width="7" height="7" />
                <rect x="3" y="14" width="7" height="7" />
              </svg>
            }
            delay={0.4}
          />

          <BentoCard
            title="Context Matters"
            description="Creative portfolios allow flourish. Financial tools need restraint. Think of expressiveness as a dial, not a binary switch."
            size="medium"
            icon={
              <svg
                width="48"
                height="48"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <circle cx="12" cy="12" r="10" />
                <polyline points="12 6 12 12 16 14" />
              </svg>
            }
            delay={0.5}
          />
        </div>
      </div>
    </section>
  );
}

// Usage Example
export default function BentoExample() {
  return (
    <BentoGrid
      title="Design Philosophy"
      subtitle="Technical precision meets organic imperfection. Where constraint becomes style."
    />
  );
}
