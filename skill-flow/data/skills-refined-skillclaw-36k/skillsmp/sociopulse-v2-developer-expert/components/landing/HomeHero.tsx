'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence, useInView } from 'framer-motion';
import { Search, ArrowRight, Sparkles, Building2, Users, Briefcase } from 'lucide-react';
import { isMedical, currentBrand } from '@/lib/brand';

// ===========================================
// HOME HERO - Masterpiece 2026
// INK REVEAL Progressive Effect
// Artistic, readable, industry-standard animation
// ===========================================

// EXACT content from user prompt
const SLIDE_CONTENT = {
    SOCIAL: [
        {
            title: "L'ÉTINCELLE",
            punch: "Parce que chaque rencontre est une aventure.",
            desc: "SOS Renfort : Que vous cherchiez une épaule solide ou une mission de cœur, on crée le lien parfait. Curieux de voir qui vous attend ?"
        },
        {
            title: "LE PARTAGE",
            punch: "Réinventons l'accompagnement, ensemble.",
            desc: "SocioLive : Des ateliers qui font du bien et des visios qui connectent. Découvrez une nouvelle façon de transmettre vos talents..."
        },
        {
            title: "LA TRIBU",
            punch: "Plus qu'un réseau, une famille de métier.",
            desc: "Le Wall : Un espace pour s'inspirer, échanger et grandir. Plongez dans le fil d'actualité pour voir ce qui fait vibrer le secteur."
        },
        {
            title: "L'ESPRIT LIBRE",
            punch: "On s'occupe de tout, pour vous.",
            desc: "Paiement & Contrats : On retire les épines de votre pied. Tout est fluide pour vous laisser vous concentrer sur l'essentiel : l'Humain."
        }
    ],
    MEDICAL: [
        {
            title: "L'HORIZON",
            punch: "Retrouvez le calme au cœur de vos plannings.",
            desc: "SOS Renfort : Un besoin urgent ? Une solution douce et efficace apparaît. Le soin reste votre priorité, nous gérons le reste."
        },
        {
            title: "L'ÉQUILIBRE",
            punch: "Votre métier, votre rythme, votre paix.",
            desc: "Espace Soignant : Choisissez vos interventions en toute clarté. Nous valorisons votre engagement avec la liberté que vous méritez."
        },
        {
            title: "LA CLARTÉ",
            punch: "La sécurité d'un cadre bienveillant.",
            desc: "Profils Vérifiés : Ici, chaque dossier est une promesse tenue. Nous veillons sur la qualité pour que vous puissiez veiller sur les autres."
        },
        {
            title: "LA FLUIDITÉ",
            punch: "Des solutions simples pour un quotidien apaisé.",
            desc: "Paiement & Admin : De la signature au paiement garanti, tout coule de source. Moins de gestion, plus de temps pour l'essentiel."
        }
    ]
};

// Counter hook
function useCountUp(target: number, duration = 2000, start = false) {
    const [count, setCount] = useState(0);
    useEffect(() => {
        if (!start) return;
        let startTime: number;
        const animate = (timestamp: number) => {
            if (!startTime) startTime = timestamp;
            const progress = Math.min((timestamp - startTime) / duration, 1);
            setCount(Math.floor(progress * target));
            if (progress < 1) requestAnimationFrame(animate);
        };
        requestAnimationFrame(animate);
    }, [target, duration, start]);
    return count;
}

// ===========================================
// INK REVEAL ANIMATION SYSTEM
// Inspired by premium editorial transitions
// ===========================================

// Custom easing for organic ink-like movement (cubic-bezier)
const inkEasing: [number, number, number, number] = [0.25, 0.1, 0.25, 1.0];

// Container variants - controls the overall slide transition
const slideContainerVariants = {
    enter: {
        opacity: 0,
    },
    center: {
        opacity: 1,
        transition: {
            duration: 0.5,
            ease: inkEasing,
            staggerChildren: 0.15,
            delayChildren: 0.1,
        }
    },
    exit: {
        opacity: 0,
        transition: {
            duration: 0.8,
            ease: inkEasing,
            staggerChildren: 0.08,
            staggerDirection: -1,
        }
    }
};

// Title - Large ink blob reveal from center
const titleVariants = {
    enter: {
        opacity: 0,
        scale: 0.8,
        y: 40,
        filter: 'blur(20px)',
    },
    center: {
        opacity: 1,
        scale: 1,
        y: 0,
        filter: 'blur(0px)',
        transition: {
            duration: 1.2,
            ease: inkEasing,
        }
    },
    exit: {
        opacity: 0,
        scale: 1.1,
        y: -30,
        filter: 'blur(15px)',
        transition: {
            duration: 0.6,
            ease: inkEasing,
        }
    }
};

// Punchline - Flows in like ink spreading
const punchVariants = {
    enter: {
        opacity: 0,
        y: 30,
        clipPath: 'inset(100% 0% 0% 0%)',
    },
    center: {
        opacity: 1,
        y: 0,
        clipPath: 'inset(0% 0% 0% 0%)',
        transition: {
            duration: 1.0,
            ease: inkEasing,
            clipPath: { duration: 0.8, ease: [0.33, 1, 0.68, 1] }
        }
    },
    exit: {
        opacity: 0,
        y: -20,
        clipPath: 'inset(0% 0% 100% 0%)',
        transition: {
            duration: 0.5,
            ease: inkEasing,
        }
    }
};

// Description - Word by word ink reveal effect
const descVariants = {
    enter: {
        opacity: 0,
        y: 25,
    },
    center: {
        opacity: 1,
        y: 0,
        transition: {
            duration: 0.9,
            ease: inkEasing,
        }
    },
    exit: {
        opacity: 0,
        y: -15,
        transition: {
            duration: 0.4,
            ease: inkEasing,
        }
    }
};

// Ink splash decoration element
const InkSplash = ({ color, delay = 0 }: { color: string; delay?: number }) => (
    <motion.div
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 0.15 }}
        exit={{ scale: 0.8, opacity: 0 }}
        transition={{ duration: 1.5, delay, ease: inkEasing }}
        className={`absolute rounded-full blur-3xl ${color}`}
        style={{
            width: '120%',
            height: '120%',
            left: '-10%',
            top: '-10%',
        }}
    />
);

// Slide duration in ms (7 seconds - faster pace)
const SLIDE_DURATION = 7000;

export function HomeHero() {
    const router = useRouter();
    const [searchQuery, setSearchQuery] = useState('');
    const [isFocused, setIsFocused] = useState(false);
    const [currentSlide, setCurrentSlide] = useState(0);

    const statsRef = useRef(null);
    const statsInView = useInView(statsRef, { once: true, amount: 0.5 });

    const medical = isMedical();
    const slides = medical ? SLIDE_CONTENT.MEDICAL : SLIDE_CONTENT.SOCIAL;

    // Counters
    const missionsCount = useCountUp(2500, 2000, statsInView);
    const establishmentsCount = useCountUp(850, 2000, statsInView);
    const professionalsCount = useCountUp(3200, 2000, statsInView);

    // Auto-advance slides
    const nextSlide = useCallback(() => {
        setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, [slides.length]);

    useEffect(() => {
        const timer = setInterval(nextSlide, SLIDE_DURATION);
        return () => clearInterval(timer);
    }, [nextSlide]);

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        router.push(searchQuery.trim() ? `/fil-pro?q=${encodeURIComponent(searchQuery)}` : '/fil-pro');
    };

    // Colors
    const brandGradient = medical
        ? 'from-rose-500 via-pink-500 to-violet-600'
        : 'from-teal-400 via-teal-500 to-indigo-600';

    return (
        <section className="relative w-full min-h-[90vh] flex flex-col overflow-hidden">
            {/* ========== ANIMATED DEPTH BACKGROUND ========== */}
            <div className={`absolute inset-0 bg-gradient-to-br ${medical
                ? 'from-rose-50 via-pink-50/80 to-violet-50'
                : 'from-teal-50 via-cyan-50/80 to-indigo-50'
                }`} />

            {/* Animated mesh for depth */}
            <div className="absolute inset-0 opacity-30">
                <motion.div
                    animate={{ backgroundPosition: ['0% 0%', '100% 100%'] }}
                    transition={{ duration: 30, repeat: Infinity, repeatType: 'reverse', ease: 'linear' }}
                    className="absolute inset-0"
                    style={{
                        backgroundImage: `radial-gradient(circle at 20% 50%, ${medical ? 'rgba(244, 63, 94, 0.15)' : 'rgba(20, 184, 166, 0.15)'} 0%, transparent 50%),
                                          radial-gradient(circle at 80% 50%, ${medical ? 'rgba(139, 92, 246, 0.1)' : 'rgba(99, 102, 241, 0.1)'} 0%, transparent 50%)`,
                        backgroundSize: '100% 100%',
                    }}
                />
            </div>

            {/* Floating soft orbs */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
                <motion.div
                    animate={{ x: [0, 30, 0], y: [0, -20, 0], opacity: [0.3, 0.5, 0.3] }}
                    transition={{ duration: 15, repeat: Infinity, ease: 'easeInOut' }}
                    className={`absolute -top-32 -left-32 w-[500px] h-[500px] rounded-full blur-[100px] ${medical ? 'bg-rose-200' : 'bg-teal-200'}`}
                />
                <motion.div
                    animate={{ x: [0, -25, 0], y: [0, 25, 0], opacity: [0.2, 0.4, 0.2] }}
                    transition={{ duration: 18, repeat: Infinity, ease: 'easeInOut' }}
                    className={`absolute top-1/4 -right-32 w-[400px] h-[400px] rounded-full blur-[80px] ${medical ? 'bg-violet-200' : 'bg-indigo-200'}`}
                />
                <motion.div
                    animate={{ x: [0, 20, 0], y: [0, -15, 0], opacity: [0.25, 0.35, 0.25] }}
                    transition={{ duration: 20, repeat: Infinity, ease: 'easeInOut' }}
                    className={`absolute bottom-32 left-1/3 w-[350px] h-[350px] rounded-full blur-[70px] ${medical ? 'bg-pink-200' : 'bg-cyan-200'}`}
                />
            </div>

            {/* ========== MAIN CONTENT ========== */}
            <div className="relative z-10 flex-1 flex flex-col items-center justify-center px-4 sm:px-6 pt-24 pb-12">
                <div className="max-w-5xl mx-auto text-center w-full">

                    {/* Preheader Teaser */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                        className="mb-6"
                    >
                        <span className={`text-lg sm:text-xl md:text-2xl font-bold tracking-wide uppercase ${medical
                            ? 'text-rose-500'
                            : 'text-teal-600'
                            }`}>
                            {medical ? "VOS RENFORTS, EN UN BATTEMENT." : "L'HUMAIN AU CŒUR DU LIEN."}
                        </span>
                    </motion.div>

                    {/* ========== INK REVEAL SLIDER ========== */}
                    <div className="relative min-h-[320px] sm:min-h-[350px] flex flex-col items-center justify-center overflow-hidden">

                        <AnimatePresence mode="wait">
                            <motion.div
                                key={currentSlide}
                                variants={slideContainerVariants}
                                initial="enter"
                                animate="center"
                                exit="exit"
                                className="absolute inset-0 flex flex-col items-center justify-center"
                            >
                                {/* Title - Main ink blob reveal */}
                                <motion.h1
                                    variants={titleVariants}
                                    className="relative text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-black tracking-tighter leading-[0.95] mb-4"
                                >
                                    <span className={`bg-clip-text text-transparent bg-gradient-to-r ${brandGradient}`}>
                                        {slides[currentSlide].title}
                                    </span>
                                </motion.h1>

                                {/* Punchline - Ink spread effect */}
                                <motion.p
                                    variants={punchVariants}
                                    className={`text-xl sm:text-2xl md:text-3xl font-medium italic mb-6 ${medical ? 'text-rose-500/80' : 'text-teal-500/80'
                                        }`}
                                >
                                    {slides[currentSlide].punch}
                                </motion.p>

                                {/* Description - Gentle fade in */}
                                <motion.p
                                    variants={descVariants}
                                    className="text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed px-4"
                                >
                                    {slides[currentSlide].desc}
                                </motion.p>
                            </motion.div>
                        </AnimatePresence>

                        {/* Minimal Progress Bars - Bottom */}
                        <div className="absolute bottom-0 left-1/2 -translate-x-1/2 flex gap-2 z-20">
                            {slides.map((_, idx) => (
                                <div
                                    key={idx}
                                    className="relative w-8 h-1 rounded-full overflow-hidden bg-slate-300/80"
                                >
                                    {currentSlide === idx && (
                                        <motion.div
                                            className={`absolute inset-0 ${medical ? 'bg-rose-500' : 'bg-teal-500'}`}
                                            initial={{ scaleX: 0 }}
                                            animate={{ scaleX: 1 }}
                                            transition={{ duration: SLIDE_DURATION / 1000, ease: 'linear' }}
                                            style={{ transformOrigin: 'left' }}
                                        />
                                    )}
                                    {currentSlide > idx && (
                                        <div className={`absolute inset-0 ${medical ? 'bg-rose-500' : 'bg-teal-500'}`} />
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* ========== SEARCH BAR ========== */}
                    <motion.form
                        onSubmit={handleSearch}
                        initial={{ opacity: 0, y: 30, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        transition={{ duration: 0.8, delay: 0.3 }}
                        className="max-w-2xl mx-auto relative mt-8"
                    >
                        <div className={`absolute inset-0 -m-2 rounded-3xl blur-2xl transition-opacity duration-500 ${isFocused ? 'opacity-50' : 'opacity-20'
                            } ${medical ? 'bg-rose-400' : 'bg-teal-400'}`} />

                        <div className={`
                            relative rounded-2xl overflow-hidden
                            bg-white/80 backdrop-blur-xl border border-white/60
                            shadow-2xl transition-all duration-300
                            ${isFocused ? 'scale-[1.02]' : ''}
                            ${medical ? 'shadow-rose-500/20' : 'shadow-teal-500/20'}
                        `}>
                            <div className="flex items-center">
                                <div className="flex items-center gap-4 flex-1 pl-6 pr-4 py-5">
                                    <Search className={`h-6 w-6 flex-shrink-0 transition-colors duration-300 ${isFocused ? (medical ? 'text-rose-500' : 'text-teal-500') : 'text-slate-400'
                                        }`} />
                                    <input
                                        type="text"
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                        onFocus={() => setIsFocused(true)}
                                        onBlur={() => setIsFocused(false)}
                                        placeholder={medical
                                            ? 'IDE, Aide-Soignant, Kiné, AES...'
                                            : 'Éducateur, Animateur, SocioLive...'
                                        }
                                        className="flex-1 bg-transparent text-slate-900 placeholder:text-slate-400 text-lg font-medium focus:outline-none"
                                    />
                                </div>
                                <div className="pr-2">
                                    <motion.button
                                        type="submit"
                                        whileHover={{ scale: 1.05 }}
                                        whileTap={{ scale: 0.95 }}
                                        className={`
                                            h-14 px-8 rounded-xl flex items-center justify-center gap-2
                                            text-white font-bold shadow-lg transition-all
                                            ${medical
                                                ? 'bg-gradient-to-r from-rose-500 to-rose-600 shadow-rose-500/40'
                                                : 'bg-gradient-to-r from-teal-500 to-teal-600 shadow-teal-500/40'
                                            }
                                        `}
                                    >
                                        <span className="hidden sm:inline">Rechercher</span>
                                        <ArrowRight className="h-5 w-5" />
                                    </motion.button>
                                </div>
                            </div>
                        </div>
                    </motion.form>

                    {/* ========== VALUE PROPOSITION TAGLINE ========== */}
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: 0.4 }}
                        className="mt-6 mb-2"
                    >
                        <p className={`text-sm sm:text-base font-medium ${medical ? 'text-rose-600/80' : 'text-teal-600/80'}`}>
                            {medical
                                ? "EHPAD, Cliniques, Hôpitaux : Sécurisez vos plannings avec des IDE et AS qualifiés, disponibles immédiatement."
                                : "La référence RH du Secteur Social & Éducatif"
                            }
                        </p>
                    </motion.div>

                    {/* ========== QUICK TAGS ========== */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.6, delay: 0.5 }}
                        className="mt-4 flex flex-wrap items-center justify-center gap-3"
                    >
                        <span className="text-sm text-slate-500 mr-1">Populaires :</span>
                        {(medical
                            ? ['IDE', 'Aide-Soignant', 'AES', 'Kiné']
                            : ['Éducateur Spécialisé', 'Moniteur-Éducateur', 'Animateur', 'SocioLive']
                        ).map((tag, i) => (
                            <motion.button
                                key={i}
                                whileHover={{ scale: 1.08 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={() => setSearchQuery(tag)}
                                className={`
                                    px-4 py-2 rounded-full text-sm font-semibold
                                    bg-white/80 backdrop-blur-sm border border-white/60
                                    text-slate-700 shadow-sm hover:shadow-md transition-all duration-200
                                    ${medical
                                        ? 'hover:text-rose-600 hover:border-rose-200 hover:bg-rose-50'
                                        : 'hover:text-teal-600 hover:border-teal-200 hover:bg-teal-50'
                                    }
                                `}
                            >
                                {tag}
                            </motion.button>
                        ))}
                    </motion.div>
                </div>
            </div>

            {/* ========== STATS COUNTER BAR ========== */}
            <motion.div
                ref={statsRef}
                initial={{ opacity: 0, y: 30 }}
                animate={statsInView ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.6 }}
                className="relative z-10 py-8 bg-white/60 backdrop-blur-xl border-t border-white/40"
            >
                <div className="max-w-5xl mx-auto px-4 sm:px-6">
                    <div className="grid grid-cols-3 gap-4 sm:gap-8">
                        <div className="text-center">
                            <div className="flex items-center justify-center gap-2 mb-1">
                                <Briefcase className={`h-5 w-5 ${medical ? 'text-rose-500' : 'text-teal-500'}`} />
                                <span className={`text-2xl sm:text-4xl font-black ${medical ? 'text-rose-600' : 'text-teal-600'}`}>
                                    +{missionsCount.toLocaleString()}
                                </span>
                            </div>
                            <p className="text-xs sm:text-sm text-slate-600 font-medium">Missions publiées</p>
                        </div>
                        <div className="text-center">
                            <div className="flex items-center justify-center gap-2 mb-1">
                                <Building2 className={`h-5 w-5 ${medical ? 'text-violet-500' : 'text-indigo-500'}`} />
                                <span className={`text-2xl sm:text-4xl font-black ${medical ? 'text-violet-600' : 'text-indigo-600'}`}>
                                    +{establishmentsCount.toLocaleString()}
                                </span>
                            </div>
                            <p className="text-xs sm:text-sm text-slate-600 font-medium">Établissements actifs</p>
                        </div>
                        <div className="text-center">
                            <div className="flex items-center justify-center gap-2 mb-1">
                                <Users className={`h-5 w-5 ${medical ? 'text-pink-500' : 'text-emerald-500'}`} />
                                <span className={`text-2xl sm:text-4xl font-black ${medical ? 'text-pink-600' : 'text-emerald-600'}`}>
                                    +{professionalsCount.toLocaleString()}
                                </span>
                            </div>
                            <p className="text-xs sm:text-sm text-slate-600 font-medium">Professionnels inscrits</p>
                        </div>
                    </div>
                </div>
            </motion.div>

            {/* Bottom fade */}
            <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-white to-transparent pointer-events-none z-0" />
        </section>
    );
}
