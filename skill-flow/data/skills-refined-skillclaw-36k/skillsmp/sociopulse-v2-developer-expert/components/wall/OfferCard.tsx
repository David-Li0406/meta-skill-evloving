'use client';

import type { MouseEvent } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Star, MapPin, Video, Mail } from 'lucide-react';

export interface OfferCardProps {
    data: any;
    currentUserId?: string;
    onSelfContact?: () => void;
    onClick?: () => void;
}

const getInitials = (value?: string) => {
    if (!value) return 'LX';
    const parts = value.split(' ').filter(Boolean);
    if (parts.length === 0) return 'LX';
    return parts.map((part) => part[0]?.toUpperCase()).join('').slice(0, 2);
};

export function OfferCard({
    data,
    currentUserId,
    onClick,
    onSelfContact,
}: OfferCardProps) {
    const service = data || {};
    const authorId = service?.profile?.userId || service?.authorId || service?.author?.id;
    const title = service?.name || service?.title || 'Service';
    const providerName = service?.profile
        ? `${service.profile.firstName || ''} ${service.profile.lastName || ''}`.trim() || service.profile.displayName || service.authorName || 'Prestataire'
        : service?.authorName || service?.providerName || 'Prestataire';
    const providerAvatar = service?.profile?.avatarUrl || service?.authorAvatar || service?.providerAvatar;
    const providerRating = Number(service?.providerRating ?? service?.profile?.averageRating ?? 0);
    const providerReviews = Number(service?.providerReviews ?? service?.profile?.totalReviews ?? 0);
    const city = service?.city || service?.profile?.city || '';
    const description = service?.content || service?.description || '';
    const serviceType = (service?.serviceType || service?.type || 'WORKSHOP') as 'WORKSHOP' | 'COACHING_VIDEO';
    const category = service?.category;
    const basePriceRaw = service?.basePrice ?? service?.hourlyRate ?? null;
    const basePrice = basePriceRaw !== null && basePriceRaw !== undefined ? Number(basePriceRaw) : null;
    const showBasePrice = basePrice !== null && !Number.isNaN(basePrice);
    const cardId = service?.id || service?.serviceId;
    const detailHref = cardId ? `/offer/${cardId}` : undefined;
    const imageUrl =
        service?.imageUrl ||
        (Array.isArray(service?.imageUrls) ? service.imageUrls[0] : undefined) ||
        (Array.isArray(service?.galleryUrls) ? service.galleryUrls[0] : undefined);
    const rawTags = Array.isArray(service?.tags) ? service.tags : [];
    const tags: string[] = rawTags.filter((tag: unknown): tag is string => typeof tag === 'string' && tag.trim().length > 0);
    const isVideo = serviceType === 'COACHING_VIDEO';
    const router = useRouter();

    const handleContact = (event: MouseEvent<HTMLButtonElement>) => {
        event.stopPropagation();

        if (!authorId) return;
        if (currentUserId && authorId === currentUserId) {
            onSelfContact?.();
            return;
        }

        router.push(`/messages?recipientId=${encodeURIComponent(authorId)}`);
    };

    const card = (
        <motion.article
            whileHover={{ y: -4, transition: { duration: 0.2 } }}
            whileTap={{ scale: 0.98 }}
            onClick={onClick}
            className={`
        group relative bg-white rounded-2xl overflow-hidden cursor-pointer
        border-l-4 border-orange-500
        shadow-soft hover:shadow-soft-lg
        transition-shadow duration-300
      `}
        >
            {/* Image Header */}
            {imageUrl && (
                <div className="relative h-36 overflow-hidden">
                    <img
                        src={imageUrl}
                        alt={title}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent" />

                    {/* Video Badge */}
                    {isVideo && (
                        <div className="absolute top-3 right-3">
                            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-white/90 backdrop-blur-sm text-xs font-medium text-slate-700">
                                <Video className="w-3 h-3 text-orange-500" />
                                Visio
                            </span>
                        </div>
                    )}
                </div>
            )}

            <div className="p-5">
                {/* Provider Info */}
                <div className="flex items-center gap-3 mb-3">
                    {/* Avatar */}
                    <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-indigo-100 to-teal-100 flex items-center justify-center overflow-hidden ring-2 ring-white shadow-sm">
                        {providerAvatar ? (
                            <img src={providerAvatar} alt={providerName} className="w-full h-full object-cover" />
                        ) : (
                            <span className="text-sm font-semibold text-orange-600">
                                {getInitials(providerName)}
                            </span>
                        )}
                    </div>

                    <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-slate-900 truncate">{providerName}</p>
                        <div className="flex items-center gap-1.5">
                            {providerRating > 0 && (
                                <>
                                    <Star className="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
                                    <span className="text-xs font-medium text-slate-700">{providerRating.toFixed(1)}</span>
                                    <span className="text-xs text-slate-400">({providerReviews})</span>
                                </>
                            )}
                            {city && (
                                <span className="inline-flex items-center gap-0.5 text-xs text-slate-400 ml-1">
                                    <MapPin className="w-3 h-3" />
                                    {city}
                                </span>
                            )}
                        </div>
                    </div>
                </div>

                {/* Title */}
                <h3 className="font-semibold text-slate-900 text-base leading-tight line-clamp-2 group-hover:text-orange-600 transition-colors mb-2">
                    {title}
                </h3>

                {/* Category Badge */}
                {category && (
                    <span className="inline-block px-3 py-1 rounded-xl bg-teal-50 text-teal-700 text-xs font-medium mb-3">
                        {category}
                    </span>
                )}

                {/* Description */}
                <p className="text-sm text-slate-600 leading-relaxed line-clamp-2 mb-4">
                    {description}
                </p>

                {/* Footer */}
                <div className="flex items-center justify-between pt-3 border-t border-slate-100">
                    {/* Tags */}
                    <div className="flex flex-wrap gap-1">
                        {tags.slice(0, 2).map((tag, index) => (
                            <span
                                key={index}
                                className="px-2 py-0.5 rounded-md bg-slate-100 text-slate-600 text-xs"
                            >
                                {tag}
                            </span>
                        ))}
                    </div>

                    <div className="flex items-center gap-2">
                        {showBasePrice && (
                            <span className="inline-flex items-center gap-0.5 font-semibold text-slate-900">
                                <span className="text-lg">{basePrice} €</span>
                                <span className="text-xs text-slate-400 font-normal">/h</span>
                            </span>
                        )}
                        <button
                            type="button"
                            onClick={handleContact}
                            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-brand-600 text-white text-xs font-semibold hover:bg-brand-700 shadow-sm hover:shadow-md active:scale-95 transition-all"
                            aria-label={`Contacter ${providerName}`}
                        >
                            <Mail className="w-3.5 h-3.5" />
                            Contacter
                        </button>
                    </div>
                </div>
            </div>

            {/* Hover Effect Overlay */}
            <div className="absolute inset-0 rounded-2xl border-2 border-transparent group-hover:border-orange-200 transition-colors pointer-events-none" />
        </motion.article>
    );

    return detailHref ? (
        <Link href={detailHref} className="block h-full">
            {card}
        </Link>
    ) : (
        card
    );
}
