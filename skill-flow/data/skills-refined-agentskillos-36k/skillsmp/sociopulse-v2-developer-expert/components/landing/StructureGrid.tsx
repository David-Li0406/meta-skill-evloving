'use client';

import Link from 'next/link';
import Image from 'next/image';
import { motion } from 'framer-motion';

// ===========================================
// STRUCTURE GRID - Bento Navigation
// ===========================================

const structures = [
    {
        id: 'ehpad',
        title: 'EHPAD',
        subtitle: 'Résidences pour personnes âgées',
        image: 'https://images.unsplash.com/photo-1576765608535-5f8040e7c02d?w=600&h=400&fit=crop',
        href: '/feed?structure=ehpad',
    },
    {
        id: 'protection-enfance',
        title: 'PROTECTION ENFANCE',
        subtitle: 'MECS, Foyers, ASE',
        image: 'https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=600&h=400&fit=crop',
        href: '/feed?structure=protection-enfance',
    },
    {
        id: 'handicap',
        title: 'HANDICAP',
        subtitle: 'IME, MAS, FAM, FH',
        image: 'https://images.unsplash.com/photo-1582213782179-e0d53f98f2ca?w=600&h=400&fit=crop',
        href: '/feed?structure=handicap',
    },
    {
        id: 'petite-enfance',
        title: 'PETITE ENFANCE',
        subtitle: 'Crèches, Micro-crèches',
        image: 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=600&h=400&fit=crop',
        href: '/feed?structure=petite-enfance',
    },
];

export function StructureGrid() {
    return (
        <section className="py-16 sm:py-20 px-4 sm:px-6 lg:px-8">
            <div className="max-w-6xl mx-auto">
                {/* Section Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-12"
                >
                    <p className="text-sm font-semibold tracking-[0.2em] uppercase text-brand-600 mb-3">
                        Par type de structure
                    </p>
                    <h2 className="text-3xl sm:text-4xl font-bold text-slate-900">
                        Trouvez par établissement
                    </h2>
                </motion.div>

                {/* Bento Grid */}
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
                    {structures.map((structure, index) => (
                        <motion.div
                            key={structure.id}
                            initial={{ opacity: 0, scale: 0.95 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.4, delay: index * 0.1 }}
                        >
                            <Link
                                href={structure.href}
                                className="group relative block aspect-square rounded-2xl overflow-hidden"
                            >
                                {/* Background Image */}
                                <Image
                                    src={structure.image}
                                    alt={structure.title}
                                    fill
                                    className="object-cover group-hover:scale-105 transition-transform duration-500"
                                    sizes="(max-width: 768px) 50vw, 25vw"
                                />

                                {/* Dark Overlay */}
                                <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/40 to-black/20 group-hover:from-black/80 group-hover:via-black/50 transition-colors" />

                                {/* Content */}
                                <div className="absolute inset-0 flex flex-col items-center justify-center p-4 text-center">
                                    <h3 className="text-lg sm:text-xl lg:text-2xl font-bold text-white tracking-wide">
                                        {structure.title}
                                    </h3>
                                    <p className="mt-2 text-xs sm:text-sm text-white/80 hidden sm:block">
                                        {structure.subtitle}
                                    </p>
                                </div>
                            </Link>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
