'use client';

import { motion } from 'framer-motion';
import { Target, Calendar, Zap } from 'lucide-react';
import { currentBrand, isMedical } from '@/lib/brand';

// ===========================================
// QUICK GUIDE - Brand-Aware Onboarding
// Adapts messaging to SOCIAL vs MEDICAL
// ===========================================

// Steps adapt based on brand mode
const getSteps = () => {
    if (isMedical()) {
        return [
            {
                icon: Target,
                title: 'Identifiez',
                description: 'Recherchez un soignant disponible selon vos critères : qualification, horaires, urgence.',
                color: 'bg-alert-100 text-alert-600',
                delay: 0.1,
            },
            {
                icon: Calendar,
                title: 'Réservez',
                description: 'Créneaux temps réel. Contrats et DPAE générés automatiquement.',
                color: 'bg-brand-100 text-brand-600',
                delay: 0.2,
            },
            {
                icon: Zap,
                title: 'Activez',
                description: 'Le soignant intervient dans votre établissement sous 24h.',
                color: 'bg-live-100 text-live-600',
                delay: 0.3,
            },
        ];
    }

    // SOCIAL mode (default)
    return [
        {
            icon: Target,
            title: 'Ciblez',
            description: 'Sélectionnez un profil expert ou un atelier clé en main.',
            color: 'bg-live-100 text-live-600',
            delay: 0.1,
        },
        {
            icon: Calendar,
            title: 'Réservez',
            description: 'Disponibilité temps réel. Contrats et DPAE automatisés.',
            color: 'bg-brand-100 text-brand-600',
            delay: 0.2,
        },
        {
            icon: Zap,
            title: 'Activez',
            description: 'Le talent intervient dans votre structure ou en visio.',
            color: 'bg-alert-100 text-alert-600',
            delay: 0.3,
        },
    ];
};

// Dynamic header label color
const labelColorClass = isMedical() ? 'text-alert-600' : 'text-live-600';

export function QuickGuide() {
    const steps = getSteps();

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
                    <p className={`text-sm font-semibold tracking-[0.2em] uppercase ${labelColorClass} mb-3`}>
                        Guide rapide
                    </p>
                    <h2 className="text-3xl sm:text-4xl font-bold text-slate-900">
                        Comment ça marche ?
                    </h2>
                </motion.div>

                {/* 3-Column Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
                    {steps.map((step, index) => (
                        <motion.div
                            key={step.title}
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.5, delay: step.delay }}
                            className="group relative bg-white rounded-2xl p-8 shadow-sm hover:shadow-soft-lg border border-slate-100 hover:border-slate-200 transition-all duration-300"
                        >
                            {/* Step Number */}
                            <div className={`absolute -top-3 -left-3 w-8 h-8 rounded-full text-white text-sm font-bold flex items-center justify-center shadow-lg ${isMedical() ? 'bg-alert-600' : 'bg-slate-900'
                                }`}>
                                {index + 1}
                            </div>

                            {/* Icon */}
                            <div className={`w-14 h-14 rounded-xl ${step.color} flex items-center justify-center mb-5 group-hover:scale-110 transition-transform duration-300`}>
                                <step.icon className="h-7 w-7" />
                            </div>

                            {/* Content */}
                            <h3 className="text-xl font-bold text-slate-900 mb-2">
                                {step.title}
                            </h3>
                            <p className="text-slate-600 leading-relaxed">
                                {step.description}
                            </p>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
