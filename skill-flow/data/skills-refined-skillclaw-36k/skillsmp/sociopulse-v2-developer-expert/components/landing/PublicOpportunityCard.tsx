'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import Image from 'next/image';
import {
    MapPin, Clock, Siren, Video, User, ArrowUpRight,
    Star, Zap, Sparkles
} from 'lucide-react';
import { isMedical } from '@/lib/brand';

// ===========================================
// PUBLIC OPPORTUNITY CARD - SEO Power Cards
// Schema.org JobPosting microdata
// Twin Design: Social (Image) vs Medical (Typo)
// ===========================================

export type OpportunityType = 'mission' | 'profile' | 'service';

export interface PublicOpportunityItem {
    id: string;
    type: OpportunityType;
    title: string;
    subtitle?: string;
    location?: string;
    price?: number;
    priceLabel?: string;
    imageUrl?: string;
    avatarUrl?: string;
    isUrgent?: boolean;
    isAvailable?: boolean;
    tags?: string[];
    category?: string;
    expiresAt?: string;
    rating?: number;
    createdAt?: string;
    organizationName?: string;
}

interface PublicOpportunityCardProps {
    item: PublicOpportunityItem;
}

// Extract initials from name
const getInitials = (name: string): string => {
    const words = name.split(/[\s\-']+/).filter(w => w.length > 0);
    if (words.length >= 2) {
        return (words[0][0] + words[1][0]).toUpperCase();
    }
    return name.substring(0, 2).toUpperCase();
};

// Format relative time
const formatRelativeTime = (dateStr?: string): string => {
    if (!dateStr) return 'Récent';
    const diff = Date.now() - new Date(dateStr).getTime();
    const hours = Math.floor(diff / (1000 * 60 * 60));
    if (hours < 1) return 'À l\'instant';
    if (hours < 24) return `Il y a ${hours}h`;
    const days = Math.floor(hours / 24);
    if (days < 7) return `Il y a ${days}j`;
    return `Il y a ${Math.floor(days / 7)} sem`;
};

// Format ISO date for Schema.org
const formatISODate = (dateStr?: string): string => {
    if (!dateStr) return new Date().toISOString();
    return new Date(dateStr).toISOString();
};

// High-quality placeholder images
const SOCIAL_IMAGES = [
    'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=400&h=300&fit=crop&q=80',
    'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400&h=300&fit=crop&q=80',
    'https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?w=400&h=300&fit=crop&q=80',
    'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=400&h=300&fit=crop&q=80',
    'https://images.unsplash.com/photo-1552664730-d307ca884978?w=400&h=300&fit=crop&q=80',
    'https://images.unsplash.com/photo-1531545514256-b1400bc00f31?w=400&h=300&fit=crop&q=80',
    'https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=400&h=300&fit=crop&q=80',
    'https://images.unsplash.com/photo-1582213782179-e0d53f98f2ca?w=400&h=300&fit=crop&q=80',
];

const getRandomImage = (id: string): string => {
    const index = id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0) % SOCIAL_IMAGES.length;
    return SOCIAL_IMAGES[index];
};

// Badge config
const getBadgeConfig = (type: OpportunityType, isUrgent: boolean) => {
    const medical = isMedical();
    switch (type) {
        case 'mission':
            return {
                icon: isUrgent ? Zap : Siren,
                label: 'Renfort',
                bgClass: isUrgent
                    ? 'bg-gradient-to-r from-red-500 to-orange-500'
                    : 'bg-gradient-to-r from-orange-500 to-amber-500',
                shadowClass: isUrgent ? 'shadow-red-500/40' : 'shadow-orange-500/40',
            };
        case 'service':
            return {
                icon: Video,
                label: medical ? 'Service' : 'SocioLive',
                bgClass: 'bg-gradient-to-r from-violet-500 to-purple-600',
                shadowClass: 'shadow-violet-500/40',
            };
        case 'profile':
            return {
                icon: Sparkles,
                label: medical ? 'Soignant' : 'Talent',
                bgClass: medical
                    ? 'bg-gradient-to-r from-rose-500 to-pink-500'
                    : 'bg-gradient-to-r from-teal-500 to-emerald-500',
                shadowClass: medical ? 'shadow-rose-500/40' : 'shadow-teal-500/40',
            };
    }
};

// ============================================
// SOCIAL MODE CARD - Instagram Story Style
// Full-bleed image with gradient overlay
// ============================================
function SocialCard({ item, href }: { item: PublicOpportunityItem; href: string }) {
    const badge = getBadgeConfig(item.type, item.isUrgent ?? false);
    const BadgeIcon = badge.icon;
    const imageUrl = item.imageUrl || item.avatarUrl || getRandomImage(item.id);
    const orgName = item.organizationName || item.subtitle || 'Établissement';

    return (
        <Link href={href} className="block">
            <motion.article
                itemScope
                itemType="https://schema.org/JobPosting"
                whileHover={{ y: -8, scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                transition={{ type: 'spring', stiffness: 400, damping: 25 }}
                className="group relative h-72 overflow-hidden rounded-3xl shadow-xl hover:shadow-2xl transition-shadow duration-500"
            >
                {/* Full Background Image */}
                <div className="absolute inset-0 overflow-hidden">
                    <img
                        src={imageUrl}
                        alt={`Offre ${item.title} à ${item.location || 'France'}`}
                        loading="lazy"
                        className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105"
                    />
                </div>

                {/* Gradient Overlay - WCAG compliant for text contrast */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent" />
                <div className="absolute inset-0 bg-gradient-to-br from-transparent via-transparent to-black/30" />

                {/* Badge - Top Left */}
                <div className="absolute top-4 left-4 z-10">
                    <span className={`inline-flex items-center gap-1.5 px-3.5 py-2 rounded-full text-xs font-bold text-white shadow-lg ${badge.bgClass} ${badge.shadowClass}`}>
                        <BadgeIcon className="h-3.5 w-3.5" />
                        {badge.label}
                    </span>
                </div>

                {/* Price Badge - Top Right */}
                {item.price && (
                    <div className="absolute top-4 right-4 z-10">
                        <span
                            itemProp="baseSalary"
                            className="px-4 py-2 rounded-full bg-white/95 backdrop-blur-sm text-sm font-black text-slate-900 shadow-lg"
                        >
                            {item.priceLabel || `${item.price}€/h`}
                        </span>
                    </div>
                )}

                {/* Content - Bottom with SEO structure */}
                <div className="absolute bottom-0 left-0 right-0 p-5 z-10">
                    {/* Organization Name - Hidden for SEO */}
                    <meta itemProp="hiringOrganization" content={orgName} />

                    {/* Date Posted */}
                    <time
                        itemProp="datePosted"
                        dateTime={formatISODate(item.createdAt)}
                        className="text-xs text-white/70 font-medium mb-1 block"
                    >
                        {formatRelativeTime(item.createdAt)}
                    </time>

                    {/* Title - SEO H2 */}
                    <h2
                        itemProp="title"
                        className="text-xl font-bold text-white line-clamp-2 mb-2 drop-shadow-lg"
                    >
                        {item.title}
                    </h2>

                    {/* Location */}
                    <div className="flex items-center justify-between gap-4">
                        {item.location && (
                            <div
                                itemProp="jobLocation"
                                itemScope
                                itemType="https://schema.org/Place"
                                className="flex items-center gap-1.5 text-sm text-white/90"
                            >
                                <MapPin className="h-4 w-4 text-teal-400" />
                                <span itemProp="name" className="truncate max-w-[160px] font-medium">
                                    {item.location}
                                </span>
                            </div>
                        )}

                        {item.rating && (
                            <div className="flex items-center gap-1.5 bg-white/20 backdrop-blur-md px-2.5 py-1 rounded-full">
                                <Star className="h-4 w-4 fill-amber-400 text-amber-400" />
                                <span className="text-sm font-bold text-white">{item.rating.toFixed(1)}</span>
                            </div>
                        )}
                    </div>

                    {/* Tags */}
                    {item.tags && item.tags.length > 0 && (
                        <div className="flex flex-wrap gap-2 mt-3">
                            {item.tags.slice(0, 3).map((tag) => (
                                <span
                                    key={tag}
                                    className="px-2.5 py-1 rounded-lg bg-white/15 backdrop-blur-sm text-xs font-semibold text-white border border-white/20"
                                >
                                    {tag}
                                </span>
                            ))}
                        </div>
                    )}
                </div>

                {/* Hover Arrow */}
                <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity z-20">
                    <div className="p-2.5 rounded-xl bg-white shadow-xl">
                        <ArrowUpRight className="h-5 w-5 text-slate-900" />
                    </div>
                </div>
            </motion.article>
        </Link>
    );
}

// ============================================
// MEDICAL MODE CARD - Swiss Corporate Style
// Typography focused, monogram initials
// ============================================
function MedicalCard({ item, href }: { item: PublicOpportunityItem; href: string }) {
    const badge = getBadgeConfig(item.type, item.isUrgent ?? false);
    const BadgeIcon = badge.icon;
    const initials = getInitials(item.title);
    const isUrgent = item.isUrgent ?? false;
    const orgName = item.organizationName || item.subtitle || 'Établissement';

    // Pastel monogram colors
    const monogramStyles = [
        { bg: 'bg-rose-50', text: 'text-rose-600', border: 'border-rose-200' },
        { bg: 'bg-violet-50', text: 'text-violet-600', border: 'border-violet-200' },
        { bg: 'bg-sky-50', text: 'text-sky-600', border: 'border-sky-200' },
        { bg: 'bg-amber-50', text: 'text-amber-600', border: 'border-amber-200' },
        { bg: 'bg-emerald-50', text: 'text-emerald-600', border: 'border-emerald-200' },
    ];
    const colorIndex = item.id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0) % monogramStyles.length;
    const monogram = monogramStyles[colorIndex];

    return (
        <Link href={href} className="block">
            <motion.article
                itemScope
                itemType="https://schema.org/JobPosting"
                whileHover={{ y: -6, scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
                transition={{ type: 'spring', stiffness: 300, damping: 25 }}
                className={`
                    group relative h-full overflow-hidden
                    rounded-2xl bg-white p-6
                    border-l-[5px] ${isUrgent ? 'border-l-red-500' : 'border-l-rose-400'}
                    border border-slate-200 hover:border-slate-300
                    shadow-lg shadow-slate-200/60 hover:shadow-xl hover:shadow-slate-300/60
                    transition-all duration-300
                `}
            >
                {/* Header: Monogram + Badge + Time */}
                <div className="flex items-start justify-between gap-3 mb-5">
                    {/* Monogram - Decorative, aria-hidden */}
                    <div
                        aria-hidden="true"
                        className={`h-16 w-16 rounded-2xl flex items-center justify-center border-2 ${monogram.bg} ${monogram.text} ${monogram.border}`}
                    >
                        <span className="text-2xl font-black tracking-tight">{initials}</span>
                    </div>

                    <div className="flex flex-col items-end gap-2">
                        {/* Badge */}
                        <span className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold text-white ${badge.bgClass} shadow-md ${badge.shadowClass}`}>
                            <BadgeIcon className="h-3.5 w-3.5" />
                            {badge.label}
                        </span>

                        {/* Date Posted */}
                        <time
                            itemProp="datePosted"
                            dateTime={formatISODate(item.createdAt)}
                            className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-slate-100 text-xs font-semibold text-slate-600"
                        >
                            <Clock className="h-3.5 w-3.5" />
                            {formatRelativeTime(item.createdAt)}
                        </time>
                    </div>
                </div>

                {/* Organization Name - SEO */}
                <p
                    itemProp="hiringOrganization"
                    className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1"
                >
                    {orgName}
                </p>

                {/* Title - SEO H2 */}
                <h2
                    itemProp="title"
                    className="text-lg font-bold text-slate-900 line-clamp-2 mb-4"
                >
                    {item.title}
                </h2>

                {/* Footer: Price + Location */}
                <div className="flex items-end justify-between mt-auto pt-4 border-t border-slate-100">
                    {/* Price */}
                    {item.price && (
                        <span
                            itemProp="baseSalary"
                            className="text-2xl font-black text-rose-600 tracking-tight"
                        >
                            {item.priceLabel || `${item.price}€/h`}
                        </span>
                    )}

                    {/* Location */}
                    {item.location && (
                        <div
                            itemProp="jobLocation"
                            itemScope
                            itemType="https://schema.org/Place"
                            className="flex items-center gap-1.5 text-sm text-slate-500 font-medium"
                        >
                            <MapPin className="h-4 w-4 text-rose-400" />
                            <span itemProp="name" className="truncate max-w-[120px]">
                                {item.location}
                            </span>
                        </div>
                    )}
                </div>

                {/* Tags */}
                {item.tags && item.tags.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-4">
                        {item.tags.slice(0, 4).map((tag) => (
                            <span
                                key={tag}
                                className="px-2.5 py-1 rounded-lg bg-slate-100 text-xs font-semibold text-slate-600 hover:bg-slate-200 transition-colors"
                            >
                                {tag}
                            </span>
                        ))}
                    </div>
                )}

                {/* Hover Arrow */}
                <div className="absolute bottom-5 right-5 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    <ArrowUpRight className="h-5 w-5 text-rose-500" />
                </div>

                {/* Urgent Pulse */}
                {isUrgent && (
                    <div className="absolute top-0 right-0 -mt-1 -mr-1">
                        <span className="flex h-4 w-4">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-4 w-4 bg-red-500"></span>
                        </span>
                    </div>
                )}
            </motion.article>
        </Link>
    );
}

// ============================================
// MAIN COMPONENT - Polymorphic Router
// ============================================
export function PublicOpportunityCard({ item }: PublicOpportunityCardProps) {
    const href = item.type === 'mission'
        ? `/need/${item.id}`
        : item.type === 'profile'
            ? `/profile/${item.id}`
            : `/offer/${item.id}`;

    if (isMedical()) {
        return <MedicalCard item={item} href={href} />;
    }

    return <SocialCard item={item} href={href} />;
}
