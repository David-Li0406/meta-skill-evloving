'use client';

import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { FileEdit, Target, ShieldCheck, ArrowRight, ChevronLeft, ChevronRight } from 'lucide-react';
import { isMedical } from '@/lib/brand';

// ===========================================
// HOW IT WORKS - 3-Step Carousel
// Horizontal scroll with icons and animations
// ===========================================

const STEPS = [
    {
        icon: FileEdit,
        title: 'Publiez en 2 min',
        description: 'Décrivez votre besoin, définissez vos critères et publiez votre annonce en quelques clics.',
        color: 'from-violet-500 to-purple-600',
        bgColor: 'bg-violet-50',
    },
    {
        icon: Target,
        title: 'Recevez des candidatures',
        description: 'Les professionnels qualifiés correspondant à vos critères vous contactent directement.',
        color: 'from-amber-500 to-orange-500',
        bgColor: 'bg-amber-50',
    },
    {
        icon: ShieldCheck,
        title: 'Recrutez en sécurité',
        description: 'Vérifiez les profils, échangez et finalisez en toute confiance sur la plateforme.',
        color: 'from-emerald-500 to-teal-500',
        bgColor: 'bg-emerald-50',
    },
];

export function HowItWorks() {
    const containerRef = useRef<HTMLDivElement>(null);
    const ref = useRef(null);
    const isInView = useInView(ref, { once: true, amount: 0.3 });

    const scroll = (direction: 'left' | 'right') => {
        if (containerRef.current) {
            const scrollAmount = 320;
            containerRef.current.scrollBy({
                left: direction === 'left' ? -scrollAmount : scrollAmount,
                behavior: 'smooth',
            });
        }
    };

    return (
        <section ref={ref} className="py-20 px-4 sm:px-6 bg-white relative overflow-hidden">
            {/* Background Pattern */}
            <div className="absolute inset-0 opacity-5">
                <div className="absolute inset-0" style={{
                    backgroundImage: `radial-gradient(circle at 1px 1px, currentColor 1px, transparent 0)`,
                    backgroundSize: '32px 32px',
                }} />
            </div>

            <div className="max-w-6xl mx-auto relative z-10">
                {/* Section Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={isInView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-12"
                >
                    <span className={`inline-block px-4 py-1.5 rounded-full text-sm font-semibold mb-4 ${isMedical()
                            ? 'bg-rose-100 text-rose-700'
                            : 'bg-teal-100 text-teal-700'
                        }`}>
                        Comment ça marche ?
                    </span>
                    <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-slate-900">
                        Simple. Rapide.{' '}
                        <span className={`bg-clip-text text-transparent bg-gradient-to-r ${isMedical() ? 'from-rose-600 to-violet-600' : 'from-teal-600 to-indigo-600'
                            }`}>
                            Efficace.
                        </span>
                    </h2>
                </motion.div>

                {/* Desktop Grid */}
                <div className="hidden md:grid md:grid-cols-3 gap-8">
                    {STEPS.map((step, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 30 }}
                            animate={isInView ? { opacity: 1, y: 0 } : {}}
                            transition={{ duration: 0.6, delay: index * 0.15 }}
                            className="group card-shine"
                        >
                            <div className={`relative p-8 rounded-3xl ${step.bgColor} border border-slate-100 hover:shadow-xl transition-all duration-300`}>
                                {/* Step Number */}
                                <div className="absolute -top-4 -left-2 h-10 w-10 rounded-full bg-slate-900 text-white flex items-center justify-center font-bold text-lg shadow-lg">
                                    {index + 1}
                                </div>

                                {/* Icon */}
                                <div className={`inline-flex p-4 rounded-2xl bg-gradient-to-br ${step.color} text-white mb-6 shadow-lg`}>
                                    <step.icon className="h-8 w-8" />
                                </div>

                                {/* Content */}
                                <h3 className="text-xl font-bold text-slate-900 mb-3">
                                    {step.title}
                                </h3>
                                <p className="text-slate-600 leading-relaxed">
                                    {step.description}
                                </p>

                                {/* Arrow Connector (except last) */}
                                {index < STEPS.length - 1 && (
                                    <div className="hidden lg:block absolute top-1/2 -right-4 transform -translate-y-1/2 z-10">
                                        <ArrowRight className="h-8 w-8 text-slate-300" />
                                    </div>
                                )}
                            </div>
                        </motion.div>
                    ))}
                </div>

                {/* Mobile Carousel */}
                <div className="md:hidden relative">
                    {/* Scroll Buttons */}
                    <button
                        onClick={() => scroll('left')}
                        className="absolute left-0 top-1/2 -translate-y-1/2 z-20 p-2 rounded-full bg-white shadow-lg text-slate-600 hover:text-slate-900 transition-colors"
                    >
                        <ChevronLeft className="h-5 w-5" />
                    </button>
                    <button
                        onClick={() => scroll('right')}
                        className="absolute right-0 top-1/2 -translate-y-1/2 z-20 p-2 rounded-full bg-white shadow-lg text-slate-600 hover:text-slate-900 transition-colors"
                    >
                        <ChevronRight className="h-5 w-5" />
                    </button>

                    {/* Carousel */}
                    <div
                        ref={containerRef}
                        className="flex gap-4 overflow-x-auto carousel-container pb-4 px-8"
                        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
                    >
                        {STEPS.map((step, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, x: 30 }}
                                animate={isInView ? { opacity: 1, x: 0 } : {}}
                                transition={{ duration: 0.5, delay: index * 0.1 }}
                                className="carousel-item w-72"
                            >
                                <div className={`relative p-6 rounded-2xl ${step.bgColor} border border-slate-100 h-full`}>
                                    {/* Step Number */}
                                    <div className="absolute -top-3 -left-1 h-8 w-8 rounded-full bg-slate-900 text-white flex items-center justify-center font-bold text-sm shadow-lg">
                                        {index + 1}
                                    </div>

                                    {/* Icon */}
                                    <div className={`inline-flex p-3 rounded-xl bg-gradient-to-br ${step.color} text-white mb-4 shadow-md`}>
                                        <step.icon className="h-6 w-6" />
                                    </div>

                                    <h3 className="text-lg font-bold text-slate-900 mb-2">
                                        {step.title}
                                    </h3>
                                    <p className="text-sm text-slate-600">
                                        {step.description}
                                    </p>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}
