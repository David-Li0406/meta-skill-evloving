'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { Sparkles, Video, Palette, Star, MapPin, ArrowRight } from 'lucide-react';

// ===========================================
// FEATURED OFFERS - 4 Services Grid
// Premium display for top services/ateliers
// ===========================================

interface ServiceItem {
    id: string;
    name?: string;
    title?: string;
    description?: string;
    shortDescription?: string;
    basePrice?: number;
    category?: string;
    serviceType?: string;
    imageUrl?: string;
    profile?: {
        firstName?: string;
        lastName?: string;
        avatarUrl?: string;
        city?: string;
        averageRating?: number;
    };
}

interface FeaturedOffersProps {
    items: ServiceItem[];
}

const getInitials = (value?: string) => {
    if (!value) return 'SP';
    const parts = value.split(' ').filter(Boolean);
    if (parts.length === 0) return 'SP';
    return parts.map((part) => part[0]?.toUpperCase()).join('').slice(0, 2);
};

function FeaturedServiceCard({ item }: { item: ServiceItem }) {
    const title = item.name || item.title || 'Service';
    const description = item.shortDescription || item.description || '';
    const basePrice = item.basePrice;
    const category = item.category;
    const providerName = item.profile
        ? `${item.profile.firstName || ''} ${item.profile.lastName || ''}`.trim() || 'Expert'
        : 'Expert';
    const providerAvatar = item.profile?.avatarUrl;
    const city = item.profile?.city;
    const rating = item.profile?.averageRating;
    const isSocioLive = item.serviceType === 'COACHING_VIDEO' || item.serviceType === 'SOCIOLIVE';
    const imageUrl = item.imageUrl;

    return (
        <Link href={`/offer/${item.id}`} className="block h-full">
            <motion.article
                whileHover={{ y: -6 }}
                className="group relative bg-white rounded-2xl overflow-hidden shadow-soft hover:shadow-xl transition-all duration-300 h-full flex flex-col"
            >
                {/* Image/Gradient Header */}
                <div className="relative h-32 overflow-hidden">
                    {imageUrl ? (
                        <img
                            src={imageUrl}
                            alt={title}
                            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                            loading="lazy"
                        />
                    ) : (
                        <div className={`w-full h-full ${isSocioLive ? 'bg-gradient-to-br from-teal-400 to-teal-600' : 'bg-gradient-to-br from-indigo-400 to-indigo-600'}`} />
                    )}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />

                    {/* Badge */}
                    <div className="absolute top-3 left-3">
                        <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-[10px] font-bold text-white shadow-lg ${isSocioLive ? 'bg-teal-500' : 'bg-indigo-600'}`}>
                            {isSocioLive ? <Video className="w-3 h-3" /> : <Palette className="w-3 h-3" />}
                            {isSocioLive ? 'SocioLive' : 'Atelier'}
                        </span>
                    </div>

                    {/* Provider Avatar */}
                    <div className="absolute bottom-0 left-3 translate-y-1/2">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-teal-400 to-indigo-500 flex items-center justify-center overflow-hidden ring-2 ring-white shadow-md">
                            {providerAvatar ? (
                                <img src={providerAvatar} alt={providerName} className="w-full h-full object-cover" />
                            ) : (
                                <span className="text-xs font-bold text-white">{getInitials(providerName)}</span>
                            )}
                        </div>
                    </div>
                </div>

                {/* Content */}
                <div className="p-4 pt-7 flex-1 flex flex-col">
                    <div className="flex items-start justify-between gap-2 mb-1">
                        <p className="text-xs text-slate-500 font-medium truncate">{providerName}</p>
                        {rating && rating > 0 && (
                            <span className="flex items-center gap-0.5 text-xs">
                                <Star className="w-3 h-3 text-amber-400 fill-amber-400" />
                                <span className="font-semibold text-slate-700">{rating.toFixed(1)}</span>
                            </span>
                        )}
                    </div>

                    <h3 className="text-sm font-bold text-slate-900 line-clamp-2 leading-snug group-hover:text-indigo-600 transition-colors flex-1">
                        {title}
                    </h3>

                    {city && (
                        <p className="text-xs text-slate-400 flex items-center gap-1 mt-1">
                            <MapPin className="w-3 h-3" />
                            {city}
                        </p>
                    )}

                    {/* Footer */}
                    <div className="flex items-center justify-between mt-3 pt-3 border-t border-slate-100">
                        {basePrice ? (
                            <div className="flex items-baseline gap-0.5">
                                <span className="text-base font-bold text-indigo-600">{basePrice}€</span>
                                <span className="text-xs text-slate-400">/séance</span>
                            </div>
                        ) : (
                            <span className="text-xs text-slate-400">Sur devis</span>
                        )}
                        <span className="text-xs font-medium text-indigo-600 group-hover:underline">
                            Voir →
                        </span>
                    </div>
                </div>
            </motion.article>
        </Link>
    );
}

export function FeaturedOffers({ items }: FeaturedOffersProps) {
    if (items.length === 0) return null;

    // Take only first 4 items
    const featured = items.slice(0, 4);

    return (
        <section className="mb-10">
            {/* Header */}
            <div className="flex items-center justify-between gap-4 mb-4">
                <div className="flex items-center gap-3">
                    <div className="h-10 w-10 rounded-xl bg-teal-50 border border-teal-100 grid place-items-center">
                        <Sparkles className="h-5 w-5 text-teal-600" />
                    </div>
                    <div>
                        <p className="text-[10px] uppercase tracking-[0.2em] text-teal-600 font-semibold">
                            ✨ Offres à la une
                        </p>
                        <h2 className="text-base font-bold tracking-tight text-slate-900">
                            SocioLive & Ateliers
                        </h2>
                    </div>
                </div>
                <Link
                    href="/services"
                    className="inline-flex items-center gap-1 text-sm font-medium text-teal-600 hover:text-teal-700 transition-colors"
                >
                    Voir tout
                    <ArrowRight className="w-4 h-4" />
                </Link>
            </div>

            {/* MOBILE: Horizontal Carousel */}
            <div className="sm:hidden -mx-4 px-4">
                <div className="mobile-carousel gap-4">
                    {featured.map((item, index) => (
                        <motion.div
                            key={item.id || index}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.3, delay: index * 0.05 }}
                            className="w-[70vw] max-w-[260px] flex-shrink-0"
                        >
                            <FeaturedServiceCard item={item} />
                        </motion.div>
                    ))}
                </div>
            </div>

            {/* TABLET+: Grid */}
            <div className="hidden sm:grid grid-cols-2 lg:grid-cols-4 gap-4">
                {featured.map((item, index) => (
                    <motion.div
                        key={item.id || index}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: index * 0.05 }}
                    >
                        <FeaturedServiceCard item={item} />
                    </motion.div>
                ))}
            </div>
        </section>
    );
}
