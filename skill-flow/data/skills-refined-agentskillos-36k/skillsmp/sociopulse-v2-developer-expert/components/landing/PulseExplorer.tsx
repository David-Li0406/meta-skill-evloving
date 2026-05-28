'use client';

import { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
    Briefcase,
    Users,
    Radio,
    Zap,
    Clock,
    MapPin,
    Star,
    CheckCircle2
} from 'lucide-react';

// ===========================================
// PULSE EXPLORER - Triple Marquee "Fourmilière Active"
// Shows platform density with infinite scroll lanes
// ===========================================

// ========== MOCK DATA ==========

const MISSIONS_DATA = [
    { id: 1, title: 'IDE Nuit', location: 'Lyon 3', price: '35€/h', urgent: true, type: 'medical' },
    { id: 2, title: 'Éducateur MECS', location: 'Paris 15', price: '28€/h', urgent: false, type: 'social' },
    { id: 3, title: 'AS Week-end', location: 'Bordeaux', price: '22€/h', urgent: true, type: 'medical' },
    { id: 4, title: 'Moniteur Éducateur', location: 'Nantes', price: '25€/h', urgent: false, type: 'social' },
    { id: 5, title: 'Infirmier EHPAD', location: 'Marseille', price: '32€/h', urgent: true, type: 'medical' },
    { id: 6, title: 'AES Foyer', location: 'Toulouse', price: '20€/h', urgent: false, type: 'social' },
    { id: 7, title: 'Kiné Domicile', location: 'Nice', price: '45€/h', urgent: false, type: 'medical' },
    { id: 8, title: 'ES Internat', location: 'Lille', price: '27€/h', urgent: true, type: 'social' },
    { id: 9, title: 'Aide-Soignant', location: 'Strasbourg', price: '21€/h', urgent: false, type: 'medical' },
    { id: 10, title: 'TISF Famille', location: 'Rennes', price: '23€/h', urgent: false, type: 'social' },
];

const TALENTS_DATA = [
    { id: 1, name: 'Marie L.', role: 'Infirmière DE', available: true, rating: 4.9, avatar: 'https://i.pravatar.cc/80?img=1' },
    { id: 2, name: 'Thomas D.', role: 'Éducateur Spé.', available: true, rating: 4.8, avatar: 'https://i.pravatar.cc/80?img=3' },
    { id: 3, name: 'Sophie M.', role: 'Aide-Soignante', available: false, rating: 5.0, avatar: 'https://i.pravatar.cc/80?img=5' },
    { id: 4, name: 'Lucas B.', role: 'Moniteur Éduc.', available: true, rating: 4.7, avatar: 'https://i.pravatar.cc/80?img=8' },
    { id: 5, name: 'Emma R.', role: 'IDE Bloc', available: true, rating: 4.9, avatar: 'https://i.pravatar.cc/80?img=9' },
    { id: 6, name: 'Hugo P.', role: 'ES MECS', available: false, rating: 4.6, avatar: 'https://i.pravatar.cc/80?img=11' },
    { id: 7, name: 'Léa C.', role: 'Psychomotricienne', available: true, rating: 4.8, avatar: 'https://i.pravatar.cc/80?img=16' },
    { id: 8, name: 'Nathan V.', role: 'AMP', available: true, rating: 4.7, avatar: 'https://i.pravatar.cc/80?img=12' },
    { id: 9, name: 'Camille G.', role: 'Orthophoniste', available: true, rating: 5.0, avatar: 'https://i.pravatar.cc/80?img=20' },
    { id: 10, name: 'Julien F.', role: 'CESF', available: false, rating: 4.5, avatar: 'https://i.pravatar.cc/80?img=14' },
];

const LIVE_DATA = [
    { id: 1, title: 'Atelier Sophrologie', date: '22 Jan', time: '14h', image: 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=200&h=200&fit=crop' },
    { id: 2, title: 'Gestion du Stress', date: '23 Jan', time: '10h', image: 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=200&h=200&fit=crop' },
    { id: 3, title: 'Écrits Pro', date: '24 Jan', time: '18h', image: 'https://images.unsplash.com/photo-1456324504439-367cee3b3c32?w=200&h=200&fit=crop' },
    { id: 4, title: 'Bientraitance', date: '25 Jan', time: '9h', image: 'https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?w=200&h=200&fit=crop' },
    { id: 5, title: 'Yoga Doux', date: '26 Jan', time: '12h', image: 'https://images.unsplash.com/photo-1599901860904-17e6ed7083a0?w=200&h=200&fit=crop' },
    { id: 6, title: 'Communication NV', date: '27 Jan', time: '15h', image: 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=200&h=200&fit=crop' },
    { id: 7, title: 'Méditation Guidée', date: '28 Jan', time: '8h', image: 'https://images.unsplash.com/photo-1508672019048-805c876b67e2?w=200&h=200&fit=crop' },
    { id: 8, title: 'Prévention TMS', date: '29 Jan', time: '11h', image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=200&h=200&fit=crop' },
];

// ========== FILTER TYPES ==========

type FilterType = 'all' | 'missions' | 'talents' | 'live';

// ========== MARQUEE COMPONENT ==========

interface MarqueeRowProps {
    children: React.ReactNode;
    speed?: number;
    direction?: 'left' | 'right';
    dimmed?: boolean;
}

function MarqueeRow({ children, speed = 30, direction = 'left', dimmed = false }: MarqueeRowProps) {
    const containerRef = useRef<HTMLDivElement>(null);
    const [contentWidth, setContentWidth] = useState(0);

    useEffect(() => {
        if (containerRef.current) {
            const firstChild = containerRef.current.firstElementChild as HTMLElement;
            if (firstChild) {
                setContentWidth(firstChild.offsetWidth);
            }
        }
    }, [children]);

    const duration = contentWidth / speed;

    return (
        <div
            className={`relative overflow-hidden transition-all duration-500 ${dimmed ? 'opacity-30 blur-sm' : 'opacity-100 blur-0'
                }`}
        >
            <motion.div
                ref={containerRef}
                className="flex gap-4"
                animate={{
                    x: direction === 'left' ? [-contentWidth, 0] : [0, -contentWidth]
                }}
                transition={{
                    x: {
                        duration: duration || 30,
                        repeat: Infinity,
                        ease: 'linear',
                        repeatType: 'loop'
                    }
                }}
                style={{
                    willChange: 'transform',
                    transform: 'translate3d(0, 0, 0)' // Force GPU acceleration
                }}
            >
                {children}
                {children}
            </motion.div>
        </div>
    );
}

// ========== CARD COMPONENTS ==========

function MissionCard({ mission }: { mission: typeof MISSIONS_DATA[0] }) {
    return (
        <div className="flex-shrink-0 w-[220px] bg-white rounded-2xl p-4 shadow-sm border border-slate-100 hover:shadow-md hover:border-slate-200 transition-all cursor-pointer group">
            <div className="flex items-start justify-between mb-3">
                <div className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wide ${mission.urgent
                        ? 'bg-red-100 text-red-600'
                        : 'bg-slate-100 text-slate-500'
                    }`}>
                    {mission.urgent ? '🔥 Urgent' : mission.type === 'medical' ? 'Médical' : 'Social'}
                </div>
                <Zap className={`h-4 w-4 ${mission.urgent ? 'text-amber-500' : 'text-slate-300'}`} />
            </div>
            <h4 className="font-bold text-slate-900 text-base mb-1 group-hover:text-brand-600 transition-colors">
                {mission.title}
            </h4>
            <div className="flex items-center gap-1.5 text-slate-500 text-sm mb-3">
                <MapPin className="h-3.5 w-3.5" />
                <span>{mission.location}</span>
            </div>
            <div className="flex items-center justify-between pt-3 border-t border-slate-100">
                <span className="text-lg font-bold text-brand-600">{mission.price}</span>
                <span className="text-xs text-slate-400">Voir →</span>
            </div>
        </div>
    );
}

function TalentCard({ talent }: { talent: typeof TALENTS_DATA[0] }) {
    return (
        <div className="flex-shrink-0 w-[180px] bg-white rounded-2xl p-4 shadow-sm border border-slate-100 hover:shadow-md hover:border-slate-200 transition-all cursor-pointer group text-center">
            <div className="relative mx-auto w-16 h-16 mb-3">
                <img
                    src={talent.avatar}
                    alt={talent.name}
                    className="w-full h-full rounded-full object-cover ring-2 ring-white shadow-md"
                />
                {talent.available && (
                    <span className="absolute -bottom-1 -right-1 h-5 w-5 bg-emerald-500 rounded-full border-2 border-white flex items-center justify-center">
                        <CheckCircle2 className="h-3 w-3 text-white" />
                    </span>
                )}
            </div>
            <h4 className="font-bold text-slate-900 text-sm group-hover:text-brand-600 transition-colors">
                {talent.name}
            </h4>
            <p className="text-xs text-slate-500 mb-2">{talent.role}</p>
            <div className="flex items-center justify-center gap-1">
                <Star className="h-3.5 w-3.5 text-amber-400 fill-amber-400" />
                <span className="text-xs font-semibold text-slate-700">{talent.rating}</span>
            </div>
            <div className={`mt-2 text-[10px] font-medium uppercase tracking-wider ${talent.available ? 'text-emerald-600' : 'text-slate-400'
                }`}>
                {talent.available ? '🟢 Disponible' : 'Occupé'}
            </div>
        </div>
    );
}

function LiveCard({ live }: { live: typeof LIVE_DATA[0] }) {
    return (
        <div className="flex-shrink-0 w-[160px] bg-white rounded-2xl overflow-hidden shadow-sm border border-slate-100 hover:shadow-md hover:border-slate-200 transition-all cursor-pointer group">
            <div className="relative h-24 overflow-hidden">
                <img
                    src={live.image}
                    alt={live.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                <div className="absolute top-2 left-2 px-2 py-0.5 rounded-full bg-red-500 text-white text-[10px] font-bold flex items-center gap-1">
                    <Radio className="h-3 w-3" />
                    LIVE
                </div>
            </div>
            <div className="p-3">
                <h4 className="font-bold text-slate-900 text-sm mb-1 line-clamp-1 group-hover:text-brand-600 transition-colors">
                    {live.title}
                </h4>
                <div className="flex items-center gap-1.5 text-slate-500 text-xs">
                    <Clock className="h-3 w-3" />
                    <span>{live.date} • {live.time}</span>
                </div>
            </div>
        </div>
    );
}

// ========== MAIN COMPONENT ==========

export function PulseExplorer() {
    const [activeFilter, setActiveFilter] = useState<FilterType>('all');

    const filters: { key: FilterType; label: string; icon: React.ReactNode }[] = [
        { key: 'all', label: 'Tout voir', icon: null },
        { key: 'missions', label: 'Missions', icon: <Briefcase className="h-4 w-4" /> },
        { key: 'talents', label: 'Talents', icon: <Users className="h-4 w-4" /> },
        { key: 'live', label: 'Live', icon: <Radio className="h-4 w-4" /> },
    ];

    return (
        <section className="relative w-full py-16 bg-slate-50/50 overflow-hidden">
            {/* Section Header */}
            <div className="text-center mb-10 px-4">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6 }}
                >
                    <h2 className="text-3xl sm:text-4xl font-bold text-slate-900 mb-3">
                        La Fourmilière Active
                    </h2>
                    <p className="text-slate-600 text-lg max-w-2xl mx-auto">
                        Explorez en temps réel les opportunités, talents et ateliers de la communauté.
                    </p>
                </motion.div>
            </div>

            {/* Smart Switcher - Glassmorphism Pill */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: 0.1 }}
                className="flex justify-center mb-10 px-4"
            >
                <div className="inline-flex items-center gap-1 p-1.5 rounded-full bg-white/80 backdrop-blur-xl shadow-lg border border-slate-200/50">
                    {filters.map((filter) => (
                        <button
                            key={filter.key}
                            onClick={() => setActiveFilter(filter.key)}
                            className={`flex items-center gap-2 px-5 py-2.5 rounded-full text-sm font-medium transition-all ${activeFilter === filter.key
                                    ? 'bg-slate-900 text-white shadow-md'
                                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                                }`}
                        >
                            {filter.icon}
                            <span>{filter.label}</span>
                        </button>
                    ))}
                </div>
            </motion.div>

            {/* Triple Marquee Rows */}
            <div className="space-y-6">
                {/* Row 1: Missions - Slow, Left */}
                <MarqueeRow
                    speed={25}
                    direction="left"
                    dimmed={activeFilter !== 'all' && activeFilter !== 'missions'}
                >
                    <div className="flex gap-4 pl-4">
                        {MISSIONS_DATA.map((mission) => (
                            <MissionCard key={mission.id} mission={mission} />
                        ))}
                    </div>
                </MarqueeRow>

                {/* Row 2: Talents - Medium, Right */}
                <MarqueeRow
                    speed={35}
                    direction="right"
                    dimmed={activeFilter !== 'all' && activeFilter !== 'talents'}
                >
                    <div className="flex gap-4 pl-4">
                        {TALENTS_DATA.map((talent) => (
                            <TalentCard key={talent.id} talent={talent} />
                        ))}
                    </div>
                </MarqueeRow>

                {/* Row 3: SocioLive - Slow, Left */}
                <MarqueeRow
                    speed={25}
                    direction="left"
                    dimmed={activeFilter !== 'all' && activeFilter !== 'live'}
                >
                    <div className="flex gap-4 pl-4">
                        {LIVE_DATA.map((live) => (
                            <LiveCard key={live.id} live={live} />
                        ))}
                    </div>
                </MarqueeRow>
            </div>

            {/* Gradient Fades on Sides */}
            <div className="absolute top-0 left-0 bottom-0 w-24 bg-gradient-to-r from-slate-50/50 to-transparent pointer-events-none z-10" />
            <div className="absolute top-0 right-0 bottom-0 w-24 bg-gradient-to-l from-slate-50/50 to-transparent pointer-events-none z-10" />
        </section>
    );
}
