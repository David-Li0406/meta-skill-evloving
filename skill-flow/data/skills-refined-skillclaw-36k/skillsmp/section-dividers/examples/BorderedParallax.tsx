"use client";

import { useEffect, useRef, useState } from "react";

type DividerVariant =
	| "wave-teal-indigo"
	| "diagonal-indigo-blue"
	| "blob-emerald-teal";

type BorderStyle = "crystal" | "gem";

interface BorderedParallaxProps {
	variant: DividerVariant;
	height?: number;
	className?: string;
	borderStyle?: BorderStyle;
}

const imagePaths: Record<DividerVariant, string> = {
	"wave-teal-indigo": "/dividers/wave-teal-indigo.png",
	"diagonal-indigo-blue": "/dividers/diagonal-indigo-blue.png",
	"blob-emerald-teal": "/dividers/blob-emerald-teal.png",
};

const borderImages = {
	crystal: {
		top: "/borders/divider-top-final.png",
		bottom: "/borders/divider-bottom-final.png",
	},
	gem: {
		top: "/borders/gem-divider.png",
		bottom: "/borders/gem-divider.png",
	},
};

/**
 * Parallax divider sandwiched between organic transparent border images.
 *
 * Structure:
 * - Top border overlays top edge of parallax (crystals hanging down / gems)
 * - Parallax image in the middle
 * - Bottom border overlays bottom edge of parallax (crystals growing up / gems)
 *
 * The borders use the same image (generated with double-sided jagged edges)
 * positioned at translateY(-50%) for top and translateY(50%) for bottom.
 */
export function BorderedParallax({
	variant,
	height = 200,
	className = "",
	borderStyle = "crystal",
}: BorderedParallaxProps) {
	const containerRef = useRef<HTMLDivElement>(null);
	const [offset, setOffset] = useState(0);
	const [isVisible, setIsVisible] = useState(false);

	const borders = borderImages[borderStyle];
	const imageSrc = imagePaths[variant];

	// Intersection Observer for performance
	useEffect(() => {
		if (!containerRef.current) return;

		const observer = new IntersectionObserver(
			([entry]) => setIsVisible(entry.isIntersecting),
			{ rootMargin: "200px" }
		);

		observer.observe(containerRef.current);
		return () => observer.disconnect();
	}, []);

	// Parallax scroll effect
	useEffect(() => {
		if (!isVisible) return;

		const handleScroll = () => {
			if (!containerRef.current) return;
			const rect = containerRef.current.getBoundingClientRect();
			const viewportCenter = window.innerHeight / 2;
			const elementCenter = rect.top + rect.height / 2;
			const distanceFromCenter = elementCenter - viewportCenter;
			setOffset(distanceFromCenter * 0.3 * -1);
		};

		handleScroll();
		window.addEventListener("scroll", handleScroll, { passive: true });
		return () => window.removeEventListener("scroll", handleScroll);
	}, [isVisible]);

	return (
		<div
			ref={containerRef}
			className={`relative ${className}`}
			style={{ overflow: "visible" }}
		>
			{/* Top divider - floats at top edge of parallax */}
			<div
				className="absolute left-0 right-0 z-50 pointer-events-none"
				style={{ top: 0, transform: "translateY(-50%)" }}
			>
				<img
					src={borders.top}
					alt=""
					className="w-full h-auto"
				/>
			</div>

			{/* Parallax background image */}
			<div
				className="relative w-full overflow-hidden"
				style={{ height: `${height}px` }}
			>
				<div
					className="absolute inset-0 w-full h-full"
					style={{
						backgroundImage: `url(${imageSrc})`,
						backgroundSize: "cover",
						backgroundPosition: "center",
						backgroundRepeat: "no-repeat",
						transform: `translateY(${offset}px)`,
						willChange: isVisible ? "transform" : "auto",
					}}
				/>
			</div>

			{/* Bottom divider - floats at bottom edge of parallax */}
			<div
				className="absolute left-0 right-0 z-50 pointer-events-none"
				style={{ bottom: 0, transform: "translateY(50%)" }}
			>
				<img
					src={borders.bottom}
					alt=""
					className="w-full h-auto"
				/>
			</div>
		</div>
	);
}
