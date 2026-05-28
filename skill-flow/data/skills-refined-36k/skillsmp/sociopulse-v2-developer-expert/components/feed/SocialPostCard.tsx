'use client';

import { useMemo, useState } from 'react';
import { ChevronLeft, ChevronRight, Image as ImageIcon } from 'lucide-react';
import { motion } from 'framer-motion';

export type SocialPostCategory = 'EXPERIENCE' | 'NEWS';

export interface SocialPostCardItem {
    id: string;
    type: 'POST';
    postType?: string;
    title?: string;
    content: string;
    category?: SocialPostCategory | string | null;
    mediaUrls?: string[];
    createdAt?: string | Date;
    authorName?: string;
    authorAvatar?: string | null;
    isOptimistic?: boolean;
}

const getInitials = (value?: string) => {
    if (!value) return 'LX';
    const parts = value.split(' ').filter(Boolean);
    if (parts.length === 0) return 'LX';
    return parts.map((part) => part[0]?.toUpperCase()).join('').slice(0, 2);
};

const formatDate = (value?: string | Date) => {
    if (!value) return '';
    const date = value instanceof Date ? value : new Date(value);
    if (Number.isNaN(date.getTime())) return '';
    return date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' });
};

const formatCategoryLabel = (category?: string | null) => {
    if (!category) return null;
    const upper = category.toUpperCase();
    if (upper === 'EXPERIENCE') return 'Expérience';
    if (upper === 'NEWS') return 'Actu';
    return category;
};

export function SocialPostCard({ item }: { item: SocialPostCardItem }) {
    const media = useMemo(() => (Array.isArray(item.mediaUrls) ? item.mediaUrls.filter(Boolean) : []), [item.mediaUrls]);
    const [activeIndex, setActiveIndex] = useState(0);

    const canPrev = activeIndex > 0;
    const canNext = activeIndex < media.length - 1;
    const categoryLabel = formatCategoryLabel(typeof item.category === 'string' ? item.category : null);
    const dateLabel = formatDate(item.createdAt);

    return (
        <motion.article
            whileHover={{ y: -2, scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
            transition={{ type: 'spring' as const, stiffness: 220, damping: 18 }}
            className="group relative overflow-hidden rounded-3xl bg-white/70 backdrop-blur-md border border-white/60 shadow-soft"
        >
            {media.length > 0 ? (
                <div className="relative h-52 bg-slate-100">
                    <img
                        src={media[Math.min(activeIndex, media.length - 1)]}
                        alt={item.title || 'Publication'}
                        className="h-full w-full object-cover"
                        loading="lazy"
                        decoding="async"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/35 via-black/10 to-transparent" />

                    {media.length > 1 ? (
                        <>
                            <button
                                type="button"
                                onClick={() => setActiveIndex((prev) => Math.max(0, prev - 1))}
                                disabled={!canPrev}
                                className="absolute left-3 top-1/2 -translate-y-1/2 h-9 w-9 rounded-full bg-white/85 backdrop-blur-sm flex items-center justify-center shadow disabled:opacity-50"
                                aria-label="Image précédente"
                            >
                                <ChevronLeft className="h-5 w-5 text-slate-800" />
                            </button>
                            <button
                                type="button"
                                onClick={() => setActiveIndex((prev) => Math.min(media.length - 1, prev + 1))}
                                disabled={!canNext}
                                className="absolute right-3 top-1/2 -translate-y-1/2 h-9 w-9 rounded-full bg-white/85 backdrop-blur-sm flex items-center justify-center shadow disabled:opacity-50"
                                aria-label="Image suivante"
                            >
                                <ChevronRight className="h-5 w-5 text-slate-800" />
                            </button>

                            <div className="absolute bottom-3 left-1/2 -translate-x-1/2 flex items-center gap-1.5">
                                {media.map((_, index) => (
                                    <span
                                        key={index}
                                        className={`h-1.5 w-1.5 rounded-full ${index === activeIndex ? 'bg-white' : 'bg-white/50'}`}
                                    />
                                ))}
                            </div>
                        </>
                    ) : null}
                </div>
            ) : (
                <div className="relative h-20 bg-gradient-to-r from-slate-50 to-white border-b border-white/60 flex items-center justify-center">
                    <ImageIcon className="h-5 w-5 text-slate-400" />
                </div>
            )}

            <div className="p-6 space-y-4">
                <header className="flex items-center justify-between gap-3">
                    <div className="flex items-center gap-3 min-w-0">
                        <div className="h-10 w-10 rounded-2xl bg-gradient-to-br from-brand-100 to-indigo-100 flex items-center justify-center overflow-hidden ring-2 ring-white shadow-sm flex-shrink-0">
                            {item.authorAvatar ? (
                                <img src={item.authorAvatar} alt={item.authorName || 'Auteur'} className="h-full w-full object-cover" loading="lazy" decoding="async" />
                            ) : (
                                <span className="text-sm font-semibold text-brand-700">
                                    {getInitials(item.authorName)}
                                </span>
                            )}
                        </div>

                        <div className="min-w-0">
                            <p className="text-sm font-semibold text-slate-900 truncate">
                                {item.authorName || 'Membre'}
                            </p>
                            <p className="text-xs text-slate-500">
                                {categoryLabel ? (
                                    <span className="inline-flex items-center gap-2">
                                        <span className="px-2 py-0.5 rounded-full bg-brand-50 text-brand-700 font-medium">
                                            {categoryLabel}
                                        </span>
                                        {dateLabel ? <span>{dateLabel}</span> : null}
                                    </span>
                                ) : (
                                    dateLabel
                                )}
                            </p>
                        </div>
                    </div>

                    {item.isOptimistic ? (
                        <span className="text-[11px] font-semibold text-slate-500 bg-slate-100 px-2.5 py-1 rounded-full">
                            Envoi…
                        </span>
                    ) : null}
                </header>

                <p className="text-sm text-slate-700 leading-relaxed whitespace-pre-wrap">
                    {item.content}
                </p>
            </div>
        </motion.article>
    );
}

