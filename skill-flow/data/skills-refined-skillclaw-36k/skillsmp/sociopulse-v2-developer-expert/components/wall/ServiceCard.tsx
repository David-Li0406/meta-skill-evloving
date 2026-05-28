'use client';

import type { MouseEvent } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Video, Palette, Star, MapPin, MessageCircle, Play, Clock, Users } from 'lucide-react';
import { getCardStyle } from '@/lib/categoryStyles';
import { CourseJsonLd, EventJsonLd } from './JsonLdSchema';

// ===========================================
// SERVICE CARD - Design "Airbnb Experience"
// TYPE B : Immersif & Inspirant
// Grande image Cover (60%+) + Avatar overlap
// Badge : "🎥 SocioLive" (Teal) ou "🎨 Atelier" (Indigo)
// ===========================================

export interface ServiceCardProps {
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

const serviceTypeBadge = {
    COACHING_VIDEO: { label: 'SocioLive', icon: Video, bgColor: 'bg-teal-500', textColor: 'text-white', emoji: '🎥', gradient: 'from-teal-500 to-teal-600' },
    SOCIOLIVE: { label: 'SocioLive', icon: Video, bgColor: 'bg-teal-500', textColor: 'text-white', emoji: '🎥', gradient: 'from-teal-500 to-teal-600' },
    WORKSHOP: { label: 'Atelier', icon: Palette, bgColor: 'bg-indigo-600', textColor: 'text-white', emoji: '🎨', gradient: 'from-indigo-600 to-indigo-700' },
    ATELIER: { label: 'Atelier', icon: Palette, bgColor: 'bg-indigo-600', textColor: 'text-white', emoji: '🎨', gradient: 'from-indigo-600 to-indigo-700' },
    DEFAULT: { label: 'Service', icon: Palette, bgColor: 'bg-slate-700', textColor: 'text-white', emoji: '✨', gradient: 'from-slate-600 to-slate-700' },
};

// Category gradient fallback replaces static images

export function ServiceCard({ data, currentUserId, onClick, onSelfContact }: ServiceCardProps) {
    const service = data || {};
    const authorId = service?.profile?.userId || service?.authorId || service?.author?.id;
    const title = service?.name || service?.title || 'Service';
    const providerFirstName = service?.profile?.firstName || '';
    const providerLastName = service?.profile?.lastName || '';
    const providerName = service?.profile
        ? `${providerFirstName} ${providerLastName}`.trim() || service.profile.displayName || service.authorName || 'Expert'
        : service?.authorName || service?.providerName || 'Expert';
    const providerAvatar = service?.profile?.avatarUrl || service?.authorAvatar || service?.providerAvatar;
    const providerRating = Number(service?.providerRating ?? service?.profile?.averageRating ?? 0);
    const providerReviews = Number(service?.providerReviews ?? service?.profile?.totalReviews ?? 0);
    const city = service?.city || service?.profile?.city || '';
    const description = service?.content || service?.description || service?.bio || '';
    const serviceType = (service?.serviceType || service?.type || 'WORKSHOP') as keyof typeof serviceTypeBadge;
    const category = service?.category;
    const basePriceRaw = service?.basePrice ?? service?.hourlyRate ?? null;
    const basePrice = basePriceRaw !== null && basePriceRaw !== undefined ? Number(basePriceRaw) : null;
    const showBasePrice = basePrice !== null && !Number.isNaN(basePrice);
    const duration = service?.duration || service?.durationMinutes;
    const maxParticipants = service?.maxParticipants;
    const cardId = service?.id || service?.serviceId;
    const detailHref = cardId ? `/offer/${cardId}` : undefined;

    // Get actual image URL (no fallback to placeholder images)
    const actualImageUrl = service?.imageUrl || (Array.isArray(service?.imageUrls) ? service.imageUrls[0] : undefined) ||
        (Array.isArray(service?.galleryUrls) ? service.galleryUrls[0] : undefined) || service?.coverImage || null;
    const hasImage = Boolean(actualImageUrl);
    const categoryStyle = getCardStyle(category || serviceType);

    const badgeConfig = serviceTypeBadge[serviceType] || serviceTypeBadge.DEFAULT;
    const BadgeIcon = badgeConfig.icon;
    const isSocioLive = serviceType === 'COACHING_VIDEO' || serviceType === 'SOCIOLIVE';
    const router = useRouter();
    const imageAlt = `${title} par ${providerName}${city ? ` à ${city}` : ''}`;

    const handleContact = (event: MouseEvent<HTMLButtonElement>) => {
        event.stopPropagation();
        event.preventDefault();
        if (!authorId) return;
        if (currentUserId && authorId === currentUserId) { onSelfContact?.(); return; }
        router.push(`/messages?recipientId=${encodeURIComponent(authorId)}`);
    };

    const handleBook = (event: MouseEvent<HTMLButtonElement>) => {
        event.stopPropagation();
        event.preventDefault();
        if (detailHref) router.push(detailHref);
    };

    const card = (
        <motion.article
            whileHover={{ y: -6, transition: { duration: 0.25 } }}
            whileTap={{ scale: 0.98 }}
            onClick={onClick}
            className="group relative bg-white rounded-3xl overflow-hidden cursor-pointer shadow-soft hover:shadow-xl transition-all duration-300 h-full flex flex-col"
            itemScope itemType="https://schema.org/Service"
        >
            {/* IMAGE HERO or CATEGORY GRADIENT */}
            <div className="relative h-48 overflow-hidden">
                {hasImage ? (
                    <img src={actualImageUrl!} alt={imageAlt} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" loading="lazy" itemProp="image" />
                ) : (
                    <div className={`w-full h-full ${categoryStyle.gradientClass}`} aria-hidden="true" />
                )}
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent" />

                <div className="absolute top-4 left-4 right-4 flex items-start justify-between">
                    <motion.span whileHover={{ scale: 1.05 }} className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold ${badgeConfig.bgColor} ${badgeConfig.textColor} shadow-lg backdrop-blur-sm`}>
                        <span>{badgeConfig.emoji}</span>
                        <BadgeIcon className="w-3.5 h-3.5" />
                        {badgeConfig.label}
                    </motion.span>
                    {category && <span className="px-3 py-1.5 rounded-full bg-white/95 backdrop-blur-sm text-xs font-medium text-slate-700 shadow-lg">{category}</span>}
                </div>

                {isSocioLive && (
                    <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                        <motion.div whileHover={{ scale: 1.1 }} className="w-16 h-16 rounded-full bg-white/90 backdrop-blur-sm flex items-center justify-center shadow-xl">
                            <Play className="w-7 h-7 text-teal-600 ml-1" />
                        </motion.div>
                    </div>
                )}

                <div className="absolute bottom-0 left-0 right-0 p-4">
                    <div className="flex items-end justify-between gap-3">
                        <div className="flex items-center gap-3">
                            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-teal-400 to-indigo-500 flex items-center justify-center overflow-hidden ring-3 ring-white shadow-lg">
                                {providerAvatar ? <img src={providerAvatar} alt={providerName} className="w-full h-full object-cover" loading="lazy" /> : <span className="text-sm font-bold text-white">{getInitials(providerName)}</span>}
                            </div>
                            <div>
                                <p className="text-white font-semibold text-sm drop-shadow-sm" itemProp="provider">{providerName}</p>
                                {city && <p className="text-white/80 text-xs flex items-center gap-1"><MapPin className="w-3 h-3" /><span itemProp="areaServed">{city}</span></p>}
                            </div>
                        </div>
                        {providerRating > 0 && (
                            <div className="flex items-center gap-1 bg-white/90 backdrop-blur-sm px-2.5 py-1.5 rounded-lg shadow-lg">
                                <Star className="w-4 h-4 text-amber-400 fill-amber-400" />
                                <span className="text-sm font-bold text-slate-900">{providerRating.toFixed(1)}</span>
                                <span className="text-xs text-slate-500">({providerReviews})</span>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* CONTENT */}
            <div className="p-5 flex-1 flex flex-col">
                <h3 className="text-lg font-bold text-slate-900 leading-snug line-clamp-2 group-hover:text-indigo-600 transition-colors" itemProp="name">{title}</h3>
                {description && <p className="text-sm text-slate-600 mt-2 line-clamp-2 leading-relaxed flex-1" itemProp="description">{description}</p>}

                <div className="flex items-center gap-4 mt-3 text-xs text-slate-500">
                    {duration && <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" />{duration} min</span>}
                    {maxParticipants && <span className="flex items-center gap-1"><Users className="w-3.5 h-3.5" />Max {maxParticipants} pers.</span>}
                </div>

                {/* FOOTER */}
                <div className="flex items-center justify-between pt-4 mt-auto border-t border-slate-100">
                    {showBasePrice ? (
                        <div className="flex items-baseline gap-1" itemProp="offers" itemScope itemType="https://schema.org/Offer">
                            <span className="text-xl font-bold text-indigo-600" itemProp="price">{basePrice}</span>
                            <span className="text-sm text-slate-500">€</span>
                            <span className="text-xs text-slate-400">/ séance</span>
                            <meta itemProp="priceCurrency" content="EUR" />
                        </div>
                    ) : <span className="text-sm text-slate-400">Sur devis</span>}

                    <div className="flex items-center gap-2">
                        <button type="button" onClick={handleContact} className="p-2.5 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-50 hover:border-slate-300 active:scale-95 transition-all touch-target">
                            <MessageCircle className="w-5 h-5 md:w-4 md:h-4" />
                        </button>
                        <button type="button" onClick={handleBook} className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r ${badgeConfig.gradient} text-white text-sm font-semibold shadow-md hover:shadow-lg active:scale-[0.98] transition-all touch-target`}>
                            {isSocioLive ? 'Rejoindre' : 'Réserver'}
                        </button>
                    </div>
                </div>
            </div>
        </motion.article>
    );

    // JSON-LD data for SEO
    const jsonLdData = {
        id: cardId ?? '',
        title: title,
        description: description || undefined,
        createdAt: service?.createdAt,
        providerName: providerName,
        city: city || undefined,
        basePrice: basePrice,
        serviceType: serviceType,
        duration: typeof duration === 'number' ? duration : undefined,
        category: category || undefined,
    };

    // Use EventJsonLd for SocioLive, CourseJsonLd for Workshop/Atelier
    const JsonLdComponent = isSocioLive ? EventJsonLd : CourseJsonLd;

    const wrappedCard = (
        <>
            <JsonLdComponent data={jsonLdData} />
            {card}
        </>
    );

    return detailHref
        ? <Link href={detailHref} className="block h-full">{wrappedCard}</Link>
        : wrappedCard;
}
