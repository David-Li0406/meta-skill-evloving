'use client';

import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import {
    Building2,
    User,
    Heart,
    ArrowRight,
    Clock,
    Shield,
    CreditCard,
    MessageSquare,
    Lock,
    FileSignature,
    Wallet,
    CheckCircle2,
    Zap,
    BarChart3
} from 'lucide-react';
import { isMedical } from '@/lib/brand';

// ===========================================
// BENTO GRIDS - Univers & Power
// MOBILE-OPTIMIZED: Horizontal carousels, simplified visuals
// ===========================================

// ========== UNIVERS BENTO (Target Segmentation) ==========

const UNIVERS_CARDS = [
    {
        id: 'establishments',
        icon: Building2,
        title: 'Établissements',
        subtitle: 'EHPAD, MECS, IME, Cliniques...',
        features: ['Continuité de service garantie', 'Profils vérifiés & conformes', 'Facturation simplifiée'],
        cta: 'Publier un besoin',
        gradient: 'from-indigo-500 to-violet-600',
        lightBg: 'bg-indigo-50',
    },
    {
        id: 'freelancers',
        icon: User,
        title: 'Professionnels',
        subtitle: 'Indépendants & Remplaçants',
        features: ['Choisissez vos missions', 'Paiement sous 48h garanti', 'Contrats automatisés'],
        cta: 'Créer mon profil',
        gradient: 'from-emerald-500 to-teal-600',
        lightBg: 'bg-emerald-50',
    },
    {
        id: 'families',
        icon: Heart,
        title: 'Familles',
        subtitle: 'Particuliers employeurs',
        features: ['Intervenants de confiance', 'Accompagnement personnalisé', "Tranquillité d'esprit"],
        cta: 'Trouver un intervenant',
        gradient: 'from-rose-500 to-pink-600',
        lightBg: 'bg-rose-50',
    },
];

export function UniversBento() {
    const ref = useRef(null);
    const isInView = useInView(ref, { once: true, amount: 0.3 });
    const medical = isMedical();

    return (
        <section ref={ref} className="py-16 md:py-24 px-4 sm:px-6 bg-white relative overflow-hidden">
            {/* Background Pattern */}
            <div className="absolute inset-0 opacity-[0.02] pointer-events-none">
                <div className="absolute inset-0 bg-dot-pattern" />
            </div>

            <div className="max-w-6xl mx-auto relative z-10">
                {/* Section Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={isInView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-10 md:mb-16"
                >
                    <span className={`inline-block px-3 md:px-4 py-1 md:py-1.5 rounded-full text-xs md:text-sm font-semibold mb-3 md:mb-4 ${medical ? 'bg-rose-100 text-rose-700' : 'bg-teal-100 text-teal-700'
                        }`}>
                        Pour qui ?
                    </span>
                    <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-slate-900 mb-3 md:mb-4">
                        Un écosystème pour{' '}
                        <span className={`bg-clip-text text-transparent bg-gradient-to-r ${medical ? 'from-rose-600 to-pink-600' : 'from-teal-600 to-emerald-600'
                            }`}>
                            chaque acteur
                        </span>
                    </h2>
                    <p className="text-slate-600 text-sm md:text-lg max-w-2xl mx-auto">
                        Que vous recrutiez, cherchiez des missions ou un accompagnement, nous avons la solution.
                    </p>
                </motion.div>

                {/* MOBILE: Horizontal Scroll Carousel */}
                <div className="md:hidden -mx-4 px-4">
                    <div className="mobile-carousel gap-4">
                        {UNIVERS_CARDS.map((card, index) => (
                            <motion.div
                                key={card.id}
                                initial={{ opacity: 0, y: 30 }}
                                animate={isInView ? { opacity: 1, y: 0 } : {}}
                                transition={{ duration: 0.6, delay: index * 0.1 }}
                                className="carousel-card-mobile group"
                            >
                                <UniversCard card={card} />
                            </motion.div>
                        ))}
                    </div>
                    {/* Scroll Hint */}
                    <p className="text-center text-xs text-slate-400 mt-2">← Swipez pour découvrir →</p>
                </div>

                {/* DESKTOP: Grid Layout */}
                <div className="hidden md:grid md:grid-cols-3 gap-6 lg:gap-8">
                    {UNIVERS_CARDS.map((card, index) => (
                        <motion.div
                            key={card.id}
                            initial={{ opacity: 0, y: 30 }}
                            animate={isInView ? { opacity: 1, y: 0 } : {}}
                            transition={{ duration: 0.6, delay: index * 0.1 }}
                            className="group"
                        >
                            <UniversCard card={card} />
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}

// Extracted card component for reuse
function UniversCard({ card }: { card: typeof UNIVERS_CARDS[0] }) {
    return (
        <div className="relative h-full p-6 md:p-8 rounded-2xl md:rounded-3xl bg-white border border-slate-200 shadow-lg hover:shadow-2xl hover:-translate-y-1 md:hover:-translate-y-2 transition-all duration-300">
            {/* Icon */}
            <div className={`inline-flex p-3 md:p-4 rounded-xl md:rounded-2xl bg-gradient-to-br ${card.gradient} text-white mb-4 md:mb-6 shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                <card.icon className="h-6 w-6 md:h-8 md:w-8" />
            </div>

            {/* Content */}
            <h3 className="text-xl md:text-2xl font-bold text-slate-900 mb-1 md:mb-2">
                {card.title}
            </h3>
            <p className="text-slate-500 text-sm md:text-base mb-4 md:mb-6">{card.subtitle}</p>

            {/* Features */}
            <ul className="space-y-2 md:space-y-3 mb-6 md:mb-8">
                {card.features.map((feature, i) => (
                    <li key={i} className="flex items-center gap-2 text-slate-600">
                        <CheckCircle2 className="h-3.5 w-3.5 md:h-4 md:w-4 text-emerald-500 flex-shrink-0" />
                        <span className="text-xs md:text-sm">{feature}</span>
                    </li>
                ))}
            </ul>

            {/* CTA */}
            <button className={`w-full flex items-center justify-center gap-2 px-4 md:px-6 py-2.5 md:py-3 rounded-xl font-semibold text-white bg-gradient-to-r ${card.gradient} shadow-lg hover:shadow-xl transition-all duration-300 group-hover:gap-3 touch-target`}>
                <span className="text-sm md:text-base">{card.cta}</span>
                <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
            </button>
        </div>
    );
}

// ========== POWER BENTO (SaaS Features) ==========

export function PowerBento() {
    const ref = useRef(null);
    const isInView = useInView(ref, { once: true, amount: 0.2 });
    const medical = isMedical();

    const brandGradient = medical
        ? 'from-rose-500 to-pink-600'
        : 'from-teal-500 to-emerald-600';

    return (
        <section ref={ref} className="py-16 md:py-24 px-4 sm:px-6 bg-gradient-to-b from-slate-50 to-white relative overflow-hidden">
            <div className="max-w-6xl mx-auto relative z-10">
                {/* Section Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={isInView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-10 md:mb-16"
                >
                    <span className={`inline-block px-3 md:px-4 py-1 md:py-1.5 rounded-full text-xs md:text-sm font-semibold mb-3 md:mb-4 ${medical ? 'bg-rose-100 text-rose-700' : 'bg-teal-100 text-teal-700'
                        }`}>
                        La Technologie
                    </span>
                    <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-slate-900 mb-3 md:mb-4">
                        Une plateforme{' '}
                        <span className={`bg-clip-text text-transparent bg-gradient-to-r ${brandGradient}`}>
                            à la pointe
                        </span>
                    </h2>
                    <p className="text-slate-600 text-sm md:text-lg max-w-2xl mx-auto">
                        Des outils puissants pour gérer vos missions, communications et paiements.
                    </p>
                </motion.div>

                {/* MOBILE: Simplified vertical stack */}
                <div className="md:hidden space-y-4">
                    {/* Mission Hub - Featured */}
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={isInView ? { opacity: 1, y: 0 } : {}}
                        transition={{ duration: 0.6, delay: 0.1 }}
                    >
                        <div className={`p-6 rounded-2xl bg-gradient-to-br ${brandGradient} text-white shadow-xl`}>
                            <div className="flex items-center gap-3 mb-4">
                                <div className="p-2.5 rounded-xl bg-white/20 backdrop-blur-sm">
                                    <BarChart3 className="h-5 w-5" />
                                </div>
                                <div>
                                    <h3 className="text-lg font-bold">Mission Hub 3.0</h3>
                                    <p className="text-white/80 text-xs">Suivi en temps réel</p>
                                </div>
                            </div>

                            {/* Simplified timeline for mobile */}
                            <div className="flex items-center gap-2 mb-4 overflow-x-auto pb-2">
                                {['Publiée', 'Candidatures', 'En cours', 'Terminée'].map((step, i) => (
                                    <div key={i} className={`flex-shrink-0 px-3 py-1.5 rounded-full text-xs font-medium ${i < 3 ? 'bg-white/20' : 'bg-white/10 text-white/60'
                                        }`}>
                                        {step}
                                    </div>
                                ))}
                            </div>

                            <div className="flex flex-wrap gap-2">
                                <span className="px-2 py-1 rounded-full bg-white/20 text-xs font-medium">Real-time</span>
                                <span className="px-2 py-1 rounded-full bg-white/20 text-xs font-medium">Push</span>
                                <span className="px-2 py-1 rounded-full bg-white/20 text-xs font-medium">Historique</span>
                            </div>
                        </div>
                    </motion.div>

                    {/* Horizontal scroll for smaller cards */}
                    <div className="-mx-4 px-4">
                        <div className="mobile-carousel gap-3">
                            {/* Chat Card */}
                            <motion.div
                                initial={{ opacity: 0, y: 30 }}
                                animate={isInView ? { opacity: 1, y: 0 } : {}}
                                transition={{ duration: 0.6, delay: 0.2 }}
                                className="w-[70vw] max-w-[280px] flex-shrink-0"
                            >
                                <div className="h-full p-5 rounded-2xl bg-white border border-slate-200 shadow-lg">
                                    <div className={`inline-flex p-2.5 rounded-xl mb-3 ${medical ? 'bg-rose-100 text-rose-600' : 'bg-teal-100 text-teal-600'}`}>
                                        <MessageSquare className="h-5 w-5" />
                                    </div>
                                    <h3 className="text-lg font-bold text-slate-900 mb-1">Chat Sécurisé</h3>
                                    <p className="text-slate-600 text-xs mb-3">Messagerie contextuelle liée à vos missions.</p>
                                    <div className="flex items-center gap-1.5 text-[10px] text-slate-500">
                                        <Lock className="h-3 w-3" />
                                        <span>Chiffrement E2E</span>
                                    </div>
                                </div>
                            </motion.div>

                            {/* Finance Card */}
                            <motion.div
                                initial={{ opacity: 0, y: 30 }}
                                animate={isInView ? { opacity: 1, y: 0 } : {}}
                                transition={{ duration: 0.6, delay: 0.3 }}
                                className="w-[70vw] max-w-[280px] flex-shrink-0"
                            >
                                <div className="h-full p-5 rounded-2xl bg-white border border-slate-200 shadow-lg">
                                    <div className="inline-flex p-2.5 rounded-xl bg-emerald-100 text-emerald-600 mb-3">
                                        <Wallet className="h-5 w-5" />
                                    </div>
                                    <h3 className="text-lg font-bold text-slate-900 mb-1">Finance Shield</h3>
                                    <p className="text-slate-600 text-xs mb-3">Paiements sécurisés, fonds en séquestre.</p>
                                    <div className="flex flex-wrap gap-1">
                                        <span className="px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 text-[10px] font-medium">Stripe</span>
                                        <span className="px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 text-[10px] font-medium">Escrow</span>
                                    </div>
                                </div>
                            </motion.div>

                            {/* Contracts Card */}
                            <motion.div
                                initial={{ opacity: 0, y: 30 }}
                                animate={isInView ? { opacity: 1, y: 0 } : {}}
                                transition={{ duration: 0.6, delay: 0.4 }}
                                className="w-[70vw] max-w-[280px] flex-shrink-0"
                            >
                                <div className="h-full p-5 rounded-2xl bg-slate-900 text-white shadow-lg">
                                    <div className={`inline-flex p-2.5 rounded-xl mb-3 ${medical ? 'bg-rose-500/20' : 'bg-teal-500/20'}`}>
                                        <FileSignature className={`h-5 w-5 ${medical ? 'text-rose-400' : 'text-teal-400'}`} />
                                    </div>
                                    <h3 className="text-lg font-bold mb-1">Smart Contracts</h3>
                                    <p className="text-slate-300 text-xs mb-3">Signature électronique légale, horodatage certifié.</p>
                                    <div className="flex flex-wrap gap-1">
                                        <span className={`px-2 py-0.5 rounded-full text-[10px] font-medium ${medical ? 'bg-rose-500/20 text-rose-300' : 'bg-teal-500/20 text-teal-300'}`}>Legal</span>
                                        <span className={`px-2 py-0.5 rounded-full text-[10px] font-medium ${medical ? 'bg-rose-500/20 text-rose-300' : 'bg-teal-500/20 text-teal-300'}`}>eIDAS</span>
                                    </div>
                                </div>
                            </motion.div>
                        </div>
                    </div>
                </div>

                {/* DESKTOP: Complex Bento Grid */}
                <div className="hidden md:grid md:grid-cols-3 gap-6">
                    {/* Card 1: Mission Hub (Large, spans 2 cols) */}
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={isInView ? { opacity: 1, y: 0 } : {}}
                        transition={{ duration: 0.6, delay: 0.1 }}
                        className="md:col-span-2 md:row-span-2"
                    >
                        <div className={`h-full p-8 rounded-3xl bg-gradient-to-br ${brandGradient} text-white shadow-xl relative overflow-hidden`}>
                            {/* Background Pattern */}
                            <div className="absolute inset-0 opacity-10 pointer-events-none">
                                <div className="absolute inset-0 bg-dot-pattern-light" />
                            </div>

                            <div className="relative z-10">
                                <div className="flex items-center gap-3 mb-6">
                                    <div className="p-3 rounded-xl bg-white/20 backdrop-blur-sm">
                                        <BarChart3 className="h-6 w-6" />
                                    </div>
                                    <div>
                                        <h3 className="text-2xl font-bold">Mission Hub 3.0</h3>
                                        <p className="text-white/80 text-sm">Suivi en temps réel</p>
                                    </div>
                                </div>

                                {/* Timeline Visual */}
                                <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 mb-6">
                                    <div className="space-y-4">
                                        {[
                                            { status: 'Publiée', icon: Zap, color: 'bg-amber-400', done: true },
                                            { status: 'Candidatures reçues', icon: User, color: 'bg-blue-400', done: true },
                                            { status: 'Profil sélectionné', icon: CheckCircle2, color: 'bg-emerald-400', done: true },
                                            { status: 'Mission en cours', icon: Clock, color: 'bg-violet-400', done: false, active: true },
                                            { status: 'Mission terminée', icon: Shield, color: 'bg-slate-300', done: false },
                                        ].map((step, i) => (
                                            <div key={i} className="flex items-center gap-4">
                                                <div className={`w-10 h-10 rounded-full ${step.done ? step.color : step.active ? 'bg-white animate-pulse' : 'bg-white/30'} flex items-center justify-center`}>
                                                    <step.icon className={`h-5 w-5 ${step.done || step.active ? 'text-slate-900' : 'text-white/50'}`} />
                                                </div>
                                                <div className={`flex-1 h-0.5 ${i < 4 ? (step.done ? step.color : 'bg-white/20') : 'hidden'}`} />
                                                <span className={`text-sm font-medium ${step.done || step.active ? 'text-white' : 'text-white/50'}`}>
                                                    {step.status}
                                                </span>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                <div className="flex flex-wrap gap-3">
                                    <span className="px-3 py-1 rounded-full bg-white/20 text-sm font-medium">Real-time Tracking</span>
                                    <span className="px-3 py-1 rounded-full bg-white/20 text-sm font-medium">Notifications Push</span>
                                    <span className="px-3 py-1 rounded-full bg-white/20 text-sm font-medium">Historique complet</span>
                                </div>
                            </div>
                        </div>
                    </motion.div>

                    {/* Card 2: Secure Chat (Square) */}
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={isInView ? { opacity: 1, y: 0 } : {}}
                        transition={{ duration: 0.6, delay: 0.2 }}
                    >
                        <div className="h-full p-6 rounded-3xl bg-white border border-slate-200 shadow-lg hover:shadow-xl transition-shadow">
                            <div className={`inline-flex p-3 rounded-xl mb-4 ${medical ? 'bg-rose-100 text-rose-600' : 'bg-teal-100 text-teal-600'}`}>
                                <MessageSquare className="h-6 w-6" />
                            </div>
                            <h3 className="text-xl font-bold text-slate-900 mb-2">Messagerie Sécurisée</h3>
                            <p className="text-slate-600 text-sm mb-4">Échangez en contexte, directement liés à vos missions.</p>

                            {/* Chat Bubbles Visual */}
                            <div className="space-y-2 mb-4">
                                <div className="flex justify-end">
                                    <div className={`px-3 py-2 rounded-2xl rounded-br-sm text-white text-xs max-w-[80%] ${medical ? 'bg-rose-500' : 'bg-teal-500'}`}>
                                        Bonjour, disponible demain ?
                                    </div>
                                </div>
                                <div className="flex justify-start">
                                    <div className="px-3 py-2 rounded-2xl rounded-bl-sm bg-slate-100 text-slate-700 text-xs max-w-[80%]">
                                        Oui, à partir de 14h ✓
                                    </div>
                                </div>
                            </div>

                            <div className="flex items-center gap-2 text-xs text-slate-500">
                                <Lock className="h-3.5 w-3.5" />
                                <span>Chiffrement de bout en bout</span>
                            </div>
                        </div>
                    </motion.div>

                    {/* Card 3: Finance Shield (Square) */}
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={isInView ? { opacity: 1, y: 0 } : {}}
                        transition={{ duration: 0.6, delay: 0.3 }}
                    >
                        <div className="h-full p-6 rounded-3xl bg-white border border-slate-200 shadow-lg hover:shadow-xl transition-shadow">
                            <div className="inline-flex p-3 rounded-xl bg-emerald-100 text-emerald-600 mb-4">
                                <Wallet className="h-6 w-6" />
                            </div>
                            <h3 className="text-xl font-bold text-slate-900 mb-2">Finance Shield</h3>
                            <p className="text-slate-600 text-sm mb-4">Paiements sécurisés, fonds en séquestre, zéro risque.</p>

                            {/* Wallet Visual */}
                            <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-xl p-4 mb-4 text-white">
                                <div className="flex items-center justify-between mb-3">
                                    <span className="text-xs text-slate-400">Solde disponible</span>
                                    <CreditCard className="h-4 w-4 text-slate-400" />
                                </div>
                                <div className="text-2xl font-bold mb-1">2 450,00 €</div>
                                <div className="text-xs text-emerald-400">+850€ ce mois</div>
                            </div>

                            <div className="flex flex-wrap gap-2">
                                <span className="px-2 py-1 rounded-full bg-slate-100 text-slate-600 text-[10px] font-medium">Stripe Connect</span>
                                <span className="px-2 py-1 rounded-full bg-slate-100 text-slate-600 text-[10px] font-medium">Escrow</span>
                            </div>
                        </div>
                    </motion.div>

                    {/* Card 4: Smart Contracts (Wide, spans full width) */}
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={isInView ? { opacity: 1, y: 0 } : {}}
                        transition={{ duration: 0.6, delay: 0.4 }}
                        className="md:col-span-3"
                    >
                        <div className="p-8 rounded-3xl bg-gradient-to-r from-slate-900 to-slate-800 text-white shadow-xl relative overflow-hidden">
                            {/* Background Glow */}
                            <div className={`absolute top-0 right-0 w-96 h-96 rounded-full blur-[100px] opacity-20 ${medical ? 'bg-rose-500' : 'bg-teal-500'}`} />

                            <div className="relative z-10 flex flex-col md:flex-row items-center gap-8">
                                <div className="flex-1">
                                    <div className="flex items-center gap-3 mb-4">
                                        <div className={`p-3 rounded-xl ${medical ? 'bg-rose-500/20' : 'bg-teal-500/20'}`}>
                                            <FileSignature className={`h-6 w-6 ${medical ? 'text-rose-400' : 'text-teal-400'}`} />
                                        </div>
                                        <h3 className="text-2xl font-bold">Smart Contracts</h3>
                                    </div>
                                    <p className="text-slate-300 mb-6 max-w-xl">
                                        Contrats générés automatiquement, signature électronique légale, horodatage certifié. Tout est archivé et conforme.
                                    </p>
                                    <div className="flex flex-wrap gap-3">
                                        <span className={`px-3 py-1.5 rounded-full text-sm font-medium ${medical ? 'bg-rose-500/20 text-rose-300' : 'bg-teal-500/20 text-teal-300'}`}>
                                            Legal Timestamping
                                        </span>
                                        <span className={`px-3 py-1.5 rounded-full text-sm font-medium ${medical ? 'bg-rose-500/20 text-rose-300' : 'bg-teal-500/20 text-teal-300'}`}>
                                            Auto-PDF Generation
                                        </span>
                                        <span className={`px-3 py-1.5 rounded-full text-sm font-medium ${medical ? 'bg-rose-500/20 text-rose-300' : 'bg-teal-500/20 text-teal-300'}`}>
                                            eIDAS Compliant
                                        </span>
                                    </div>
                                </div>

                                {/* Contract Visual - HIDDEN on tablet, visible on large desktop */}
                                <div className="hidden lg:block flex-shrink-0">
                                    <div className="w-48 h-64 bg-white rounded-xl shadow-2xl p-4 transform rotate-3 hover:rotate-0 transition-transform duration-300">
                                        <div className="h-3 w-24 bg-slate-200 rounded mb-3" />
                                        <div className="h-2 w-full bg-slate-100 rounded mb-2" />
                                        <div className="h-2 w-full bg-slate-100 rounded mb-2" />
                                        <div className="h-2 w-3/4 bg-slate-100 rounded mb-4" />
                                        <div className="h-2 w-full bg-slate-100 rounded mb-2" />
                                        <div className="h-2 w-full bg-slate-100 rounded mb-2" />
                                        <div className="h-2 w-1/2 bg-slate-100 rounded mb-6" />
                                        <div className="flex items-center gap-2 mt-auto">
                                            <div className={`h-8 w-24 rounded ${medical ? 'bg-rose-100' : 'bg-teal-100'}`} />
                                            <CheckCircle2 className={`h-5 w-5 ${medical ? 'text-rose-500' : 'text-teal-500'}`} />
                                        </div>
                                        <div className="mt-2 text-[8px] text-slate-400 text-center">
                                            Signé le 19/01/2026
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </div>
        </section>
    );
}
