'use client';

import Image from 'next/image';
import Link from 'next/link';
import { MapPin, Euro } from 'lucide-react';
import type { SeedItem } from '@/lib/seedData';

// ===========================================
// UNIVERSE CARD - Card for Netflix Rails
// ===========================================

interface UniverseCardProps {
    item: SeedItem;
    accentColor: 'rose' | 'indigo' | 'teal';
}

// Category to image mapping for fallback
const categoryImages: Record<string, string> = {
    SOIN: 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=400&h=300&fit=crop',
    EDUC: 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=400&h=300&fit=crop',
    HANDICAP: 'https://images.unsplash.com/photo-1582213782179-e0d53f98f2ca?w=400&h=300&fit=crop',
    SOCIAL: 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&h=300&fit=crop',
    SOCIOLIVE: 'https://images.unsplash.com/photo-1545205597-3d9d02c29597?w=400&h=300&fit=crop',
    PETITE_ENFANCE: 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=300&fit=crop',
};

const accentColorClasses = {
    rose: {
        badge: 'bg-alert-100 text-alert-700',
        border: 'hover:border-alert-300',
        price: 'text-alert-600',
    },
    indigo: {
        badge: 'bg-brand-100 text-brand-700',
        border: 'hover:border-brand-300',
        price: 'text-brand-600',
    },
    teal: {
        badge: 'bg-live-100 text-live-700',
        border: 'hover:border-live-300',
        price: 'text-live-600',
    },
};

export function UniverseCard({ item, accentColor }: UniverseCardProps) {
    const colors = accentColorClasses[accentColor];
    const imageUrl = item.data.logoUrl || categoryImages[item.category] || categoryImages.SOIN;
    const displayTags = item.data.tags.slice(0, 2);

    return (
        <Link
            href="/fil-pro"
            className={`group flex-shrink-0 w-[280px] sm:w-[320px] snap-center bg-white rounded-2xl overflow-hidden border border-slate-100 ${colors.border} shadow-sm hover:shadow-soft-lg transition-all duration-300`}
        >
            {/* Image */}
            <div className="relative h-40 overflow-hidden">
                <Image
                    src={imageUrl}
                    alt={item.data.title}
                    fill
                    className="object-cover group-hover:scale-105 transition-transform duration-500"
                    sizes="320px"
                />
                {/* Availability Badge */}
                {item.data.isAvailable && (
                    <div className="absolute top-3 left-3 px-2 py-1 rounded-full bg-green-500 text-white text-xs font-semibold flex items-center gap-1">
                        <span className="w-1.5 h-1.5 rounded-full bg-white animate-pulse" />
                        Disponible
                    </div>
                )}
            </div>

            {/* Content */}
            <div className="p-5">
                {/* Title - Critical for SEO */}
                <h3 className="font-bold text-slate-900 text-sm leading-snug line-clamp-2 mb-3 group-hover:text-brand-600 transition-colors">
                    {item.data.title}
                </h3>

                {/* Tags */}
                <div className="flex flex-wrap gap-1.5 mb-3">
                    {displayTags.map((tag) => (
                        <span
                            key={tag}
                            className={`px-2 py-0.5 rounded-full text-xs font-medium ${colors.badge}`}
                        >
                            {tag}
                        </span>
                    ))}
                </div>

                {/* Footer: Price & Location */}
                <div className="flex items-center justify-between text-sm">
                    <div className={`flex items-center gap-1 font-bold ${colors.price}`}>
                        <Euro className="h-4 w-4" />
                        <span>{item.data.hourlyRate}€/h</span>
                    </div>
                    <div className="flex items-center gap-1 text-slate-500">
                        <MapPin className="h-3.5 w-3.5" />
                        <span className="text-xs">{item.city}</span>
                    </div>
                </div>
            </div>
        </Link>
    );
}
