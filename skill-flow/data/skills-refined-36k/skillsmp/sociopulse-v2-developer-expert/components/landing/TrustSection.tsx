'use client';

import { useRef, useState, useEffect } from 'react';
import { motion, useInView } from 'framer-motion';
import { ArrowRight, Clock } from 'lucide-react';
import Link from 'next/link';
import { isMedical } from '@/lib/brand';
import { getBlogArticles, getImpactStats, type BlogArticle, type ImpactStat } from './data/MockData';

// ===========================================
// TRUST SECTION - Logos, Stats, Blog
// MOBILE-OPTIMIZED: Tighter padding, horizontal blog carousel
// ===========================================

// ========== LOGO MARQUEE ==========

const LOGO_PLACEHOLDERS = [
    { id: 1, name: 'FEHAP' },
    { id: 2, name: 'ARS' },
    { id: 3, name: 'Croix-Rouge' },
    { id: 4, name: 'URIOPSS' },
    { id: 5, name: 'CNSA' },
    { id: 6, name: 'Korian' },
    { id: 7, name: 'DomusVi' },
    { id: 8, name: 'Colisée' },
];

function LogoMarquee() {
    return (
        <div className="relative overflow-hidden py-4 md:py-8 bg-slate-50">
            {/* Fade edges */}
            <div className="absolute inset-y-0 left-0 w-16 md:w-32 bg-gradient-to-r from-slate-50 to-transparent z-10" />
            <div className="absolute inset-y-0 right-0 w-16 md:w-32 bg-gradient-to-l from-slate-50 to-transparent z-10" />

            <motion.div
                className="flex gap-8 md:gap-16 items-center"
                animate={{ x: [0, -1000] }}
                transition={{
                    x: {
                        duration: 30,
                        repeat: Infinity,
                        ease: 'linear',
                        repeatType: 'loop'
                    }
                }}
                style={{
                    willChange: 'transform',
                    transform: 'translate3d(0, 0, 0)'
                }}
            >
                {/* Duplicate logos for seamless loop */}
                {[...LOGO_PLACEHOLDERS, ...LOGO_PLACEHOLDERS, ...LOGO_PLACEHOLDERS].map((logo, index) => (
                    <div
                        key={`${logo.id}-${index}`}
                        className="flex-shrink-0 h-10 md:h-12 px-4 md:px-6 flex items-center justify-center rounded-lg bg-white border border-slate-200 shadow-sm"
                    >
                        <span className="text-slate-400 font-semibold text-xs md:text-sm tracking-wide">
                            {logo.name}
                        </span>
                    </div>
                ))}
            </motion.div>
        </div>
    );
}

// ========== IMPACT COUNTERS ==========

function useCountUp(target: number, duration = 2000, start = false) {
    const [count, setCount] = useState(0);

    useEffect(() => {
        if (!start) return;
        let startTime: number;
        const animate = (timestamp: number) => {
            if (!startTime) startTime = timestamp;
            const progress = Math.min((timestamp - startTime) / duration, 1);
            // Easing function for smooth animation
            const eased = 1 - Math.pow(1 - progress, 3);
            setCount(Math.floor(eased * target));
            if (progress < 1) requestAnimationFrame(animate);
        };
        requestAnimationFrame(animate);
    }, [target, duration, start]);

    return count;
}

function ImpactCounters() {
    const ref = useRef(null);
    const isInView = useInView(ref, { once: true, amount: 0.5 });
    const stats = getImpactStats();
    const medical = isMedical();

    return (
        <div ref={ref} className="py-10 md:py-16 px-4 sm:px-6 bg-white">
            <div className="max-w-5xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={isInView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-8 md:mb-12"
                >
                    <span className={`inline-block px-3 md:px-4 py-1 md:py-1.5 rounded-full text-xs md:text-sm font-semibold mb-3 md:mb-4 ${medical ? 'bg-rose-100 text-rose-700' : 'bg-teal-100 text-teal-700'
                        }`}>
                        Notre Impact
                    </span>
                    <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold text-slate-900">
                        Des chiffres qui{' '}
                        <span className={`bg-clip-text text-transparent bg-gradient-to-r ${medical ? 'from-rose-600 to-pink-600' : 'from-teal-600 to-emerald-600'
                            }`}>
                            parlent
                        </span>
                    </h2>
                </motion.div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-6 lg:gap-8">
                    {stats.map((stat, index) => (
                        <ImpactCard
                            key={index}
                            stat={stat}
                            isInView={isInView}
                            delay={index * 0.1}
                            medical={medical}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
}

function ImpactCard({ stat, isInView, delay, medical }: {
    stat: ImpactStat;
    isInView: boolean;
    delay: number;
    medical: boolean;
}) {
    const count = useCountUp(stat.value, 2000, isInView);

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.6, delay }}
            className="text-center p-4 md:p-6 rounded-xl md:rounded-2xl bg-slate-50 border border-slate-100"
        >
            <div className={`text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-black mb-1 md:mb-2 ${medical ? 'text-rose-600' : 'text-teal-600'
                }`}>
                {stat.prefix}{count.toLocaleString()}{stat.suffix}
            </div>
            <p className="text-slate-600 text-[10px] sm:text-xs md:text-sm font-medium">{stat.label}</p>
        </motion.div>
    );
}

// ========== PULSE MAG (Blog Previews) ==========

function PulseMag() {
    const ref = useRef(null);
    const isInView = useInView(ref, { once: true, amount: 0.3 });
    const articles = getBlogArticles();
    const medical = isMedical();

    return (
        <div ref={ref} className="py-12 md:py-20 px-4 sm:px-6 bg-gradient-to-b from-white to-slate-50">
            <div className="max-w-6xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={isInView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.6 }}
                    className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-8 md:mb-12"
                >
                    <div>
                        <span className={`inline-block px-3 md:px-4 py-1 md:py-1.5 rounded-full text-xs md:text-sm font-semibold mb-3 md:mb-4 ${medical ? 'bg-rose-100 text-rose-700' : 'bg-teal-100 text-teal-700'
                            }`}>
                            Pulse Mag
                        </span>
                        <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold text-slate-900">
                            Actualités &{' '}
                            <span className={`bg-clip-text text-transparent bg-gradient-to-r ${medical ? 'from-rose-600 to-pink-600' : 'from-teal-600 to-emerald-600'
                                }`}>
                                Conseils
                            </span>
                        </h2>
                    </div>
                    <Link
                        href="/blog"
                        className={`inline-flex items-center gap-2 font-semibold text-sm md:text-base transition-colors touch-target ${medical ? 'text-rose-600 hover:text-rose-700' : 'text-teal-600 hover:text-teal-700'
                            }`}
                    >
                        Voir tout
                        <ArrowRight className="h-4 w-4" />
                    </Link>
                </motion.div>

                {/* MOBILE: Horizontal Scroll Carousel */}
                <div className="md:hidden -mx-4 px-4">
                    <div className="mobile-carousel gap-4">
                        {articles.map((article, index) => (
                            <motion.div
                                key={article.id}
                                initial={{ opacity: 0, y: 30 }}
                                animate={isInView ? { opacity: 1, y: 0 } : {}}
                                transition={{ duration: 0.6, delay: index * 0.1 }}
                                className="w-[75vw] max-w-[300px] flex-shrink-0"
                            >
                                <BlogCard article={article} medical={medical} />
                            </motion.div>
                        ))}
                    </div>
                </div>

                {/* DESKTOP: Grid Layout */}
                <div className="hidden md:grid md:grid-cols-3 gap-6 lg:gap-8">
                    {articles.map((article, index) => (
                        <motion.article
                            key={article.id}
                            initial={{ opacity: 0, y: 30 }}
                            animate={isInView ? { opacity: 1, y: 0 } : {}}
                            transition={{ duration: 0.6, delay: index * 0.1 }}
                            className="group"
                        >
                            <BlogCard article={article} medical={medical} />
                        </motion.article>
                    ))}
                </div>
            </div>
        </div>
    );
}

function BlogCard({ article, medical }: {
    article: BlogArticle;
    medical: boolean;
}) {
    return (
        <Link href={`/blog/${article.slug}`} className="block h-full group">
            <div className="h-full bg-white rounded-2xl md:rounded-3xl overflow-hidden border border-slate-200 shadow-lg hover:shadow-xl transition-all duration-300">
                {/* Image */}
                <div className="relative h-36 md:h-48 overflow-hidden">
                    <img
                        src={article.image}
                        alt={article.title}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                        loading="lazy"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
                    <span className={`absolute top-3 left-3 md:top-4 md:left-4 px-2.5 py-0.5 md:px-3 md:py-1 rounded-full text-[10px] md:text-xs font-bold text-white ${medical ? 'bg-rose-500' : 'bg-teal-500'
                        }`}>
                        {article.category}
                    </span>
                </div>

                {/* Content */}
                <div className="p-4 md:p-6">
                    <h3 className={`text-base md:text-lg font-bold text-slate-900 mb-1.5 md:mb-2 line-clamp-2 transition-colors ${medical ? 'group-hover:text-rose-600' : 'group-hover:text-teal-600'
                        }`}>
                        {article.title}
                    </h3>
                    <p className="text-slate-600 text-xs md:text-sm mb-3 md:mb-4 line-clamp-2">
                        {article.excerpt}
                    </p>
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-1 text-slate-400 text-[10px] md:text-xs">
                            <Clock className="h-3 md:h-3.5 w-3 md:w-3.5" />
                            <span>{article.readTime}</span>
                        </div>
                        <span className={`flex items-center gap-1 text-[10px] md:text-xs font-semibold transition-colors ${medical ? 'text-rose-500 group-hover:text-rose-600' : 'text-teal-500 group-hover:text-teal-600'
                            }`}>
                            Lire
                            <ArrowRight className="h-3 w-3 group-hover:translate-x-1 transition-transform" />
                        </span>
                    </div>
                </div>
            </div>
        </Link>
    );
}

// ========== MAIN EXPORT ==========

export function TrustSection() {
    return (
        <section className="relative">
            {/* Partners Logo Marquee */}
            <div className="border-y border-slate-200">
                <div className="max-w-6xl mx-auto px-4 py-4 md:py-8">
                    <p className="text-center text-xs md:text-sm text-slate-500 mb-4 md:mb-6 font-medium">
                        Ils nous font confiance
                    </p>
                    <LogoMarquee />
                </div>
            </div>

            {/* Impact Numbers */}
            <ImpactCounters />

            {/* Blog/Mag Section */}
            <PulseMag />
        </section>
    );
}
