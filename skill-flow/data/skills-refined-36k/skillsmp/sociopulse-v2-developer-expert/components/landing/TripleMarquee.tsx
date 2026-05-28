'use client';

import { useState, useRef, useEffect, useCallback } from 'react';
import { motion, useInView } from 'framer-motion';
import {
    Briefcase,
    Users,
    Radio,
    Zap,
    Clock,
    MapPin,
    Star,
    CheckCircle2,
    BadgeCheck,
    Calendar
} from 'lucide-react';
import { isMedical } from '@/lib/brand';
import {
    getMissions,
    getTalents,
    getAteliers,
    type MissionItem,
    type TalentItem,
    type AtelierItem
} from './data/MockData';

// ===========================================
// TRIPLE MARQUEE - The Pulse Explorer
// MOBILE-OPTIMIZED: Reduced rows, slower speed, touch-friendly
// ===========================================

type TabType = 'missions' | 'talents' | 'ateliers';

// ========== MARQUEE ROW COMPONENT ==========

interface MarqueeRowProps {
    children: React.ReactNode;
    speed?: number;
    mobileSpeed?: number;
    direction?: 'left' | 'right';
    paused?: boolean;
}

function MarqueeRow({
    children,
    speed = 40,
    mobileSpeed = 25, // 20% slower on mobile
    direction = 'left',
    paused = false
}: MarqueeRowProps) {
    const containerRef = useRef<HTMLDivElement>(null);
    const [contentWidth, setContentWidth] = useState(0);
    const [isMobile, setIsMobile] = useState(false);

    useEffect(() => {
        // Check if mobile on mount and resize
        const checkMobile = () => setIsMobile(window.innerWidth < 768);
        checkMobile();
        window.addEventListener('resize', checkMobile);
        return () => window.removeEventListener('resize', checkMobile);
    }, []);

    useEffect(() => {
        if (containerRef.current) {
            const firstChild = containerRef.current.firstElementChild as HTMLElement;
            if (firstChild) {
                setContentWidth(firstChild.offsetWidth);
            }
        }
    }, [children]);

    const actualSpeed = isMobile ? mobileSpeed : speed;
    const duration = contentWidth / actualSpeed;

    return (
        <div
            className="relative overflow-hidden group marquee-fade-edges"
        >
            <motion.div
                ref={containerRef}
                className="flex gap-3 md:gap-4"
                animate={{
                    x: direction === 'left' ? [-contentWidth, 0] : [0, -contentWidth]
                }}
                transition={{
                    x: {
                        duration: duration || 40,
                        repeat: Infinity,
                        ease: 'linear',
                        repeatType: 'loop'
                    }
                }}
                style={{
                    willChange: 'transform',
                    transform: 'translate3d(0, 0, 0)',
                    animationPlayState: paused ? 'paused' : 'running'
                }}
            >
                {children}
                {children}
            </motion.div>
        </div>
    );
}

// ========== CARD COMPONENTS ==========

function MissionCard({ mission }: { mission: MissionItem }) {
    const medical = isMedical();

    return (
        <div className="flex-shrink-0 w-[240px] md:w-[260px] bg-white rounded-2xl p-4 md:p-5 shadow-sm border border-slate-100 hover:shadow-xl hover:border-slate-200 hover:-translate-y-1 transition-all duration-300 cursor-pointer group">
            <div className="flex items-start justify-between mb-2 md:mb-3">
                <div className={`px-2 py-0.5 md:px-2.5 md:py-1 rounded-full text-[10px] font-bold uppercase tracking-wide ${mission.urgent
                        ? 'bg-red-100 text-red-600'
                        : medical
                            ? 'bg-rose-50 text-rose-600'
                            : 'bg-teal-50 text-teal-600'
                    }`}>
                    {mission.urgent ? '🔥 Urgent' : mission.duration}
                </div>
                {mission.urgent && <Zap className="h-4 w-4 text-amber-500" />}
            </div>

            <h4 className={`font-bold text-slate-900 text-sm md:text-base mb-1 transition-colors line-clamp-1 ${medical ? 'group-hover:text-rose-600' : 'group-hover:text-teal-600'
                }`}>
                {mission.title}
            </h4>

            <p className="text-xs md:text-sm text-slate-500 mb-2 md:mb-3 line-clamp-1">{mission.establishment}</p>

            <div className="flex items-center gap-2 md:gap-3 text-slate-500 text-xs md:text-sm mb-3 md:mb-4">
                <div className="flex items-center gap-1">
                    <MapPin className="h-3 md:h-3.5 w-3 md:w-3.5" />
                    <span className="truncate max-w-[60px] md:max-w-none">{mission.location}</span>
                </div>
                <div className="flex items-center gap-1">
                    <Calendar className="h-3 md:h-3.5 w-3 md:w-3.5" />
                    <span>{mission.date}</span>
                </div>
            </div>

            <div className="flex items-center justify-between pt-2 md:pt-3 border-t border-slate-100">
                <span className={`text-base md:text-lg font-bold ${medical ? 'text-rose-600' : 'text-teal-600'}`}>
                    {mission.price}
                </span>
                <span className={`text-xs font-medium ${medical ? 'text-rose-500' : 'text-teal-500'}`}>
                    Voir →
                </span>
            </div>
        </div>
    );
}

function TalentCard({ talent }: { talent: TalentItem }) {
    const medical = isMedical();

    return (
        <div className="flex-shrink-0 w-[160px] md:w-[200px] bg-white rounded-2xl p-4 md:p-5 shadow-sm border border-slate-100 hover:shadow-xl hover:border-slate-200 hover:-translate-y-1 transition-all duration-300 cursor-pointer group text-center">
            <div className="relative mx-auto w-12 h-12 md:w-16 md:h-16 mb-2 md:mb-3">
                <img
                    src={talent.avatar}
                    alt={talent.name}
                    className="w-full h-full rounded-full object-cover ring-2 ring-white shadow-md"
                />
                {talent.available && (
                    <span className="absolute -bottom-1 -right-1 h-4 w-4 md:h-5 md:w-5 bg-emerald-500 rounded-full border-2 border-white flex items-center justify-center">
                        <CheckCircle2 className="h-2.5 w-2.5 md:h-3 md:w-3 text-white" />
                    </span>
                )}
                {talent.verified && (
                    <span className={`absolute -top-1 -right-1 h-4 w-4 md:h-5 md:w-5 rounded-full border-2 border-white flex items-center justify-center ${medical ? 'bg-rose-500' : 'bg-teal-500'
                        }`}>
                        <BadgeCheck className="h-2.5 w-2.5 md:h-3 md:w-3 text-white" />
                    </span>
                )}
            </div>

            <h4 className={`font-bold text-slate-900 text-xs md:text-sm transition-colors ${medical ? 'group-hover:text-rose-600' : 'group-hover:text-teal-600'
                }`}>
                {talent.name}
            </h4>
            <p className="text-[10px] md:text-xs text-slate-500 mb-1 line-clamp-1">{talent.role}</p>

            <div className="flex items-center justify-center gap-1 mb-1 md:mb-2">
                <Star className="h-3 md:h-3.5 w-3 md:w-3.5 text-amber-400 fill-amber-400" />
                <span className="text-[10px] md:text-xs font-semibold text-slate-700">{talent.rating}</span>
            </div>

            <div className={`text-[9px] md:text-[10px] font-medium uppercase tracking-wider ${talent.available ? 'text-emerald-600' : 'text-slate-400'
                }`}>
                {talent.available ? '🟢 Dispo' : '⚪ Occupé'}
            </div>
        </div>
    );
}

function AtelierCard({ atelier }: { atelier: AtelierItem }) {
    return (
        <div className="flex-shrink-0 w-[180px] md:w-[220px] bg-white rounded-2xl overflow-hidden shadow-sm border border-slate-100 hover:shadow-xl hover:border-slate-200 hover:-translate-y-1 transition-all duration-300 cursor-pointer group">
            <div className="relative h-24 md:h-28 overflow-hidden">
                <img
                    src={atelier.image}
                    alt={atelier.title}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />
                <div className="absolute top-2 left-2 px-2 py-0.5 rounded-full bg-teal-500 text-white text-[9px] md:text-[10px] font-bold flex items-center gap-1">
                    <Radio className="h-2.5 w-2.5 md:h-3 md:w-3" />
                    LIVE
                </div>
            </div>
            <div className="p-3 md:p-4">
                <h4 className="font-bold text-slate-900 text-xs md:text-sm mb-1 line-clamp-1 group-hover:text-teal-600 transition-colors">
                    {atelier.title}
                </h4>
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-1 text-slate-500 text-[10px] md:text-xs">
                        <Clock className="h-2.5 w-2.5 md:h-3 md:w-3" />
                        <span>{atelier.date}</span>
                    </div>
                    <span className="text-xs md:text-sm font-bold text-teal-600">{atelier.price}</span>
                </div>
            </div>
        </div>
    );
}

// ========== MAIN COMPONENT ==========

export function TripleMarquee() {
    const [activeTab, setActiveTab] = useState<TabType>('missions');
    const [isPaused, setIsPaused] = useState(false);
    const ref = useRef(null);
    const isInView = useInView(ref, { once: true, amount: 0.2 });

    const medical = isMedical();
    const missions = getMissions();
    const talents = getTalents();
    const ateliers = getAteliers();
    const showAteliers = !medical && ateliers.length > 0;

    const tabs: { key: TabType; label: string; icon: React.ReactNode }[] = [
        { key: 'missions', label: 'Missions', icon: <Briefcase className="h-4 w-4" /> },
        { key: 'talents', label: 'Talents', icon: <Users className="h-4 w-4" /> },
        ...(showAteliers ? [{ key: 'ateliers' as TabType, label: 'Live', icon: <Radio className="h-4 w-4" /> }] : []),
    ];

    const handleMouseEnter = useCallback(() => setIsPaused(true), []);
    const handleMouseLeave = useCallback(() => setIsPaused(false), []);

    return (
        <section
            ref={ref}
            className="relative w-full py-12 md:py-20 overflow-hidden bg-gradient-to-b from-white via-slate-50/50 to-white touch-scroll-y"
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
        >
            {/* Section Header */}
            <div className="text-center mb-8 md:mb-12 px-4">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={isInView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.6 }}
                >
                    <span className={`inline-block px-3 md:px-4 py-1 md:py-1.5 rounded-full text-xs md:text-sm font-semibold mb-3 md:mb-4 ${medical ? 'bg-rose-100 text-rose-700' : 'bg-teal-100 text-teal-700'
                        }`}>
                        L'Écosystème Vivant
                    </span>
                    <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-slate-900 mb-3 md:mb-4">
                        Explorez la{' '}
                        <span className={`bg-clip-text text-transparent bg-gradient-to-r ${medical ? 'from-rose-600 to-pink-600' : 'from-teal-600 to-emerald-600'
                            }`}>
                            Fourmilière
                        </span>
                    </h2>
                    <p className="text-slate-600 text-sm md:text-lg max-w-2xl mx-auto">
                        Des centaines d'opportunités en mouvement.
                    </p>
                </motion.div>
            </div>

            {/* Glassmorphism Tab Switcher - Touch Friendly */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={isInView ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.6, delay: 0.1 }}
                className="flex justify-center mb-6 md:mb-10 px-4"
            >
                <div className="inline-flex items-center gap-1 p-1 md:p-1.5 rounded-full bg-white/70 backdrop-blur-xl shadow-lg border border-white/30">
                    {tabs.map((tab) => (
                        <button
                            key={tab.key}
                            onClick={() => setActiveTab(tab.key)}
                            className={`flex items-center gap-1.5 md:gap-2 px-3 md:px-5 py-2 md:py-2.5 rounded-full text-xs md:text-sm font-medium transition-all duration-300 touch-target ${activeTab === tab.key
                                    ? medical
                                        ? 'bg-gradient-to-r from-rose-500 to-pink-500 text-white shadow-lg'
                                        : 'bg-gradient-to-r from-teal-500 to-emerald-500 text-white shadow-lg'
                                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
                                }`}
                        >
                            {tab.icon}
                            <span className="hidden sm:inline">{tab.label}</span>
                        </button>
                    ))}
                </div>
            </motion.div>

            {/* Marquee Rows - MOBILE: Show 2 rows, DESKTOP: Show all 3 */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={isInView ? { opacity: 1 } : {}}
                transition={{ duration: 0.8, delay: 0.2 }}
                className="space-y-4 md:space-y-6"
            >
                {/* Row 1: Missions - Always visible */}
                <div className={`transition-all duration-500 ${activeTab !== 'missions' ? 'opacity-30 blur-[2px]' : 'opacity-100'
                    }`}>
                    <MarqueeRow speed={30} mobileSpeed={20} direction="left" paused={isPaused}>
                        <div className="flex gap-3 md:gap-4 pl-4">
                            {missions.map((mission) => (
                                <MissionCard key={mission.id} mission={mission} />
                            ))}
                        </div>
                    </MarqueeRow>
                </div>

                {/* Row 2: Talents - HIDDEN on mobile to reduce GPU load */}
                <div className={`hidden md:block transition-all duration-500 ${activeTab !== 'talents' ? 'opacity-30 blur-[2px]' : 'opacity-100'
                    }`}>
                    <MarqueeRow speed={35} mobileSpeed={25} direction="right" paused={isPaused}>
                        <div className="flex gap-3 md:gap-4 pl-4">
                            {talents.map((talent) => (
                                <TalentCard key={talent.id} talent={talent} />
                            ))}
                        </div>
                    </MarqueeRow>
                </div>

                {/* Row 2 Mobile Alternative: Simple horizontal scroll */}
                <div className={`md:hidden transition-all duration-500 ${activeTab !== 'talents' ? 'opacity-30 blur-[2px]' : 'opacity-100'
                    }`}>
                    <div className="mobile-carousel px-4 gap-3">
                        {talents.slice(0, 6).map((talent) => (
                            <TalentCard key={talent.id} talent={talent} />
                        ))}
                    </div>
                </div>

                {/* Row 3: Ateliers/SocioLive - Only for Social mode */}
                {showAteliers && (
                    <div className={`transition-all duration-500 ${activeTab !== 'ateliers' ? 'opacity-30 blur-[2px]' : 'opacity-100'
                        }`}>
                        <MarqueeRow speed={25} mobileSpeed={18} direction="left" paused={isPaused}>
                            <div className="flex gap-3 md:gap-4 pl-4">
                                {ateliers.map((atelier) => (
                                    <AtelierCard key={atelier.id} atelier={atelier} />
                                ))}
                            </div>
                        </MarqueeRow>
                    </div>
                )}
            </motion.div>

            {/* Gradient Fades on Sides */}
            <div className="absolute top-0 left-0 bottom-0 w-8 sm:w-16 md:w-32 bg-gradient-to-r from-white to-transparent pointer-events-none z-10" />
            <div className="absolute top-0 right-0 bottom-0 w-8 sm:w-16 md:w-32 bg-gradient-to-l from-white to-transparent pointer-events-none z-10" />
        </section>
    );
}
