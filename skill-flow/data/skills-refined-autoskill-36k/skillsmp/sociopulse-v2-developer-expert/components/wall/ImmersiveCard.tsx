'use client';

import type { ReactNode } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';

export interface ImmersiveCardProps {
    title: string;
    subtitle?: string;
    priceLabel?: string;
    imageUrl?: string | null;
    avatarUrl?: string | null;
    badge?: ReactNode;
    href?: string;
    onClick?: () => void;
}

const cardMotion = {
    whileHover: { scale: 1.015, y: -2 },
    whileTap: { scale: 0.985 },
    transition: { type: 'spring' as const, stiffness: 220, damping: 18 },
};

export function ImmersiveCard({
    title,
    subtitle,
    priceLabel,
    imageUrl,
    avatarUrl,
    badge,
    href,
    onClick,
}: ImmersiveCardProps) {
    const card = (
        <motion.article
            {...cardMotion}
            onClick={onClick}
            className="group relative h-full overflow-hidden rounded-3xl shadow-soft"
        >
            <div className="absolute inset-0">
                {imageUrl ? (
                    <img
                        src={imageUrl}
                        alt={subtitle || title}
                        className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-[1.06]"
                        loading="lazy"
                        decoding="async"
                    />
                ) : (
                    <div className="h-full w-full bg-gradient-to-br from-indigo-500/20 via-white/5 to-teal-500/20" />
                )}
                <div className="absolute inset-0 bg-gradient-to-t from-black/55 via-black/15 to-transparent" />
            </div>

            {badge ? (
                <div className="absolute top-4 right-4">{badge}</div>
            ) : null}

            <div className="absolute bottom-4 left-4 right-4">
                <div className="bg-white/14 backdrop-blur-md border border-white/20 rounded-2xl px-4 py-4">
                    <div className="flex items-start justify-between gap-4">
                        <div className="min-w-0">
                            <p className="text-sm font-semibold text-white tracking-tight truncate">
                                {title}
                            </p>
                            {subtitle ? (
                                <p className="mt-1 text-xs text-white/75 line-clamp-1">
                                    {subtitle}
                                </p>
                            ) : null}
                        </div>
                        {priceLabel ? (
                            <div className="flex-shrink-0 rounded-xl bg-white/12 border border-white/20 px-3 py-1.5">
                                <span className="text-sm font-semibold text-white">{priceLabel}</span>
                            </div>
                        ) : null}
                    </div>

                    {avatarUrl ? (
                        <div className="mt-4 flex items-center gap-2">
                            <img
                                src={avatarUrl}
                                alt={title}
                                className="h-8 w-8 rounded-full object-cover ring-1 ring-white/30"
                                loading="lazy"
                                decoding="async"
                            />
                            <span className="text-xs text-white/70">Voir le profil</span>
                        </div>
                    ) : null}
                </div>
            </div>

            <div className="pointer-events-none absolute inset-0 rounded-3xl ring-1 ring-white/15" />
        </motion.article>
    );

    return href ? (
        <Link href={href} className="block h-full">
            {card}
        </Link>
    ) : (
        card
    );
}
