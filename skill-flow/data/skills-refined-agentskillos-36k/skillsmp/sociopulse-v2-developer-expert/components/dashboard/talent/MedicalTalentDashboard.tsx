'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import {
    Siren,
    Calendar,
    Clock,
    MapPin,
    Euro,
    ChevronRight,
    Wallet,
    ArrowRight,
    RefreshCw,
    Filter,
    Bell,
    CheckCircle2,
    Zap,
    Activity,
    TrendingUp,
    Timer,
    Navigation,
    Shield,
    Star,
} from 'lucide-react';
import { Card, CardContent } from '@/components/ui';
import { DashboardAlert } from '@/components/dashboard';
import { getTerm } from '@/lib/domain-config';
import { cn } from '@/lib/utils';
import type { DashboardUser } from '../DashboardResolver';

// =============================================================================
// TYPES — Stock Ticker Data Structures
// =============================================================================

interface MedicalTalentDashboardProps {
    user?: DashboardUser;
}

interface ShiftItem {
    id: string;
    title: string;
    establishment: string;
    unit: string;
    date: string;
    time: string;
    duration: string;
    hourlyRate: number;
    totalPay: number;
    distance: number;
    urgency: 'critical' | 'high' | 'medium';
    type: 'IDE' | 'AS' | 'AES';
    verified: boolean;
    expiresIn?: string;
}

interface EarningsData {
    today: number;
    week: number;
    month: number;
    pending: number;
}

// =============================================================================
// ANIMATION VARIANTS — Fast, Snappy, Trading Floor
// =============================================================================

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: { staggerChildren: 0.04, delayChildren: 0.1 }
    }
} as const;

const itemVariants = {
    hidden: { opacity: 0, x: -10 },
    visible: { opacity: 1, x: 0, transition: { duration: 0.2 } }
} as const;

const tickerVariants = {
    hidden: { opacity: 0, y: 20, scale: 0.95 },
    visible: { 
        opacity: 1, 
        y: 0, 
        scale: 1,
        transition: { type: 'spring' as const, stiffness: 300, damping: 25 }
    },
    exit: { opacity: 0, y: -20, scale: 0.95, transition: { duration: 0.15 } }
} as const;

// =============================================================================
// MOCK DATA — Real-time Shift Opportunities
// =============================================================================

const mockShifts: ShiftItem[] = [
    {
        id: '1',
        title: 'Vacation IDE - Soins',
        establishment: 'EHPAD Les Tilleuls',
        unit: 'Étage 2 - Unité Alzheimer',
        date: "Aujourd'hui",
        time: '14:00 - 21:00',
        duration: '7h',
        hourlyRate: 42,
        totalPay: 294,
        distance: 8,
        urgency: 'critical',
        type: 'IDE',
        verified: true,
        expiresIn: '45 min',
    },
    {
        id: '2',
        title: 'Vacation AS - Nursing',
        establishment: 'Clinique Saint-Jean',
        unit: 'Service Gériatrie',
        date: "Aujourd'hui",
        time: '21:00 - 07:00',
        duration: '10h',
        hourlyRate: 28,
        totalPay: 280,
        distance: 12,
        urgency: 'critical',
        type: 'AS',
        verified: true,
        expiresIn: '1h 20min',
    },
    {
        id: '3',
        title: 'Vacation IDE - HAD',
        establishment: 'HAD Rhône-Alpes',
        unit: 'Tournée secteur Nord',
        date: 'Demain',
        time: '07:00 - 14:00',
        duration: '7h',
        hourlyRate: 45,
        totalPay: 315,
        distance: 5,
        urgency: 'high',
        type: 'IDE',
        verified: false,
    },
    {
        id: '4',
        title: 'Vacation AES - Accompagnement',
        establishment: 'MAS Les Oliviers',
        unit: 'Unité de vie',
        date: 'Demain',
        time: '14:00 - 21:00',
        duration: '7h',
        hourlyRate: 24,
        totalPay: 168,
        distance: 15,
        urgency: 'medium',
        type: 'AES',
        verified: true,
    },
    {
        id: '5',
        title: 'Vacation AS - Nuit',
        establishment: 'EHPAD Beauséjour',
        unit: 'Service complet',
        date: 'Vendredi',
        time: '21:00 - 07:00',
        duration: '10h',
        hourlyRate: 30,
        totalPay: 300,
        distance: 20,
        urgency: 'medium',
        type: 'AS',
        verified: true,
    },
];

const mockEarnings: EarningsData = {
    today: 294,
    week: 1547,
    month: 4892,
    pending: 847,
};

const userName = 'Marie';

// =============================================================================
// SUB-COMPONENTS — Bloomberg/Trading Terminal Style
// =============================================================================

/** Animated earnings counter - Light mode */
function EarningsCounter({ value, label, trend }: { value: number; label: string; trend?: 'up' | 'down' }) {
    const [displayValue, setDisplayValue] = useState(0);
    
    useEffect(() => {
        const duration = 1000;
        const steps = 30;
        const increment = value / steps;
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= value) {
                setDisplayValue(value);
                clearInterval(timer);
            } else {
                setDisplayValue(Math.floor(current));
            }
        }, duration / steps);
        
        return () => clearInterval(timer);
    }, [value]);
    
    return (
        <div className="text-center">
            <div className="flex items-center justify-center gap-1">
                <span className="text-2xl lg:text-3xl font-bold font-mono tabular-nums text-rose-600">
                    {displayValue.toLocaleString('fr-FR')}
                </span>
                <span className="text-rose-600 text-lg">€</span>
                {trend && (
                    <TrendingUp className={cn(
                        'w-4 h-4 ml-1',
                        trend === 'up' ? 'text-emerald-500' : 'text-rose-500 rotate-180'
                    )} />
                )}
            </div>
            <p className="text-[10px] text-slate-500 uppercase tracking-wider mt-0.5">{label}</p>
        </div>
    );
}

/** Availability toggle - Light mode */
function AvailabilityToggle({ isOn, onToggle }: { isOn: boolean; onToggle: () => void }) {
    return (
        <button
            onClick={onToggle}
            className={cn(
                'relative flex items-center gap-3 px-4 py-2.5 rounded-xl transition-all duration-300 shadow-md',
                isOn
                    ? 'bg-gradient-to-r from-emerald-500 to-teal-500 text-white shadow-emerald-200'
                    : 'bg-white text-slate-600 border border-slate-200 shadow-slate-100'
            )}
        >
            {isOn && (
                <span className="absolute -top-1 -right-1 flex h-3 w-3">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                    <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-300" />
                </span>
            )}

            <Activity size={18} className={isOn ? 'text-white' : 'text-slate-400'} />
            
            <div className="flex flex-col items-start text-left">
                <span className="text-[9px] font-bold uppercase tracking-wider opacity-80">
                    {isOn ? 'EN LIGNE' : 'HORS LIGNE'}
                </span>
                <span className="font-semibold text-xs">
                    {isOn ? 'Prêt vacations' : 'Mode repos'}
                </span>
            </div>

            <div className={cn(
                'w-9 h-5 rounded-full relative transition-colors ml-2',
                isOn ? 'bg-emerald-700' : 'bg-slate-300'
            )}>
                <span className={cn(
                    'absolute top-0.5 w-4 h-4 rounded-full bg-white shadow transition-all duration-300',
                    isOn ? 'left-4' : 'left-0.5'
                )} />
            </div>
        </button>
    );
}

/** Wallet display - Light mode */
function WalletDisplay({ balance }: { balance: number }) {
    return (
        <Link
            href="/dashboard/talent/admin"
            className="flex items-center gap-3 px-4 py-2.5 bg-white border border-slate-200 rounded-xl hover:border-rose-300 hover:shadow-md transition-all group"
        >
            <div className="p-2 bg-gradient-to-br from-amber-100 to-amber-50 rounded-lg">
                <Wallet size={18} className="text-amber-600" />
            </div>
            <div>
                <p className="text-[9px] text-slate-500 font-bold uppercase tracking-wider">Solde</p>
                <p className="font-bold font-mono text-slate-900 tabular-nums">
                    {balance.toLocaleString('fr-FR')} €
                </p>
            </div>
            <ChevronRight size={14} className="text-slate-400 group-hover:translate-x-1 group-hover:text-rose-500 transition-all" />
        </Link>
    );
}

/** Shift ticker card - Light mode */
function ShiftTickerCard({ shift, index }: { shift: ShiftItem; index: number }) {
    const urgencyConfig = {
        critical: { 
            label: 'URGENT', 
            border: 'border-rose-300',
            bg: 'bg-gradient-to-r from-rose-50 to-white',
            badge: 'bg-rose-500 text-white',
            glow: 'shadow-lg shadow-rose-100'
        },
        high: { 
            label: 'PRIORITAIRE', 
            border: 'border-amber-300',
            bg: 'bg-gradient-to-r from-amber-50 to-white',
            badge: 'bg-amber-100 text-amber-700 border border-amber-300',
            glow: 'shadow-md shadow-amber-50'
        },
        medium: { 
            label: 'STANDARD', 
            border: 'border-slate-200',
            bg: 'bg-white',
            badge: 'bg-slate-100 text-slate-600',
            glow: ''
        },
    };

    const config = urgencyConfig[shift.urgency];
    const typeColors = {
        IDE: 'bg-rose-100 text-rose-700 border-rose-300',
        AS: 'bg-blue-100 text-blue-700 border-blue-300',
        AES: 'bg-violet-100 text-violet-700 border-violet-300',
    };

    return (
        <motion.div
            variants={tickerVariants}
            initial="hidden"
            animate="visible"
            exit="exit"
            layout
            className={cn(
                'relative border-2 rounded-xl overflow-hidden transition-all hover:scale-[1.01] cursor-pointer group',
                config.border,
                config.bg,
                config.glow && `shadow-lg ${config.glow}`
            )}
        >
            {/* Urgency scanning line for critical */}
            {shift.urgency === 'critical' && (
                <motion.div
                    className="absolute inset-0 bg-gradient-to-r from-transparent via-rose-200/40 to-transparent pointer-events-none"
                    animate={{ x: ['-100%', '100%'] }}
                    transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                />
            )}
            
            <Link href={`/sos/${shift.id}`} className="relative block p-4">
                <div className="flex items-start gap-3">
                    {/* Left: Type + Pay Stack */}
                    <div className="flex flex-col items-center gap-2">
                        <span className={cn('px-2 py-1 rounded-lg text-[10px] font-bold border', typeColors[shift.type])}>
                            {shift.type}
                        </span>
                        <div className="text-center">
                            <p className="text-lg font-bold font-mono text-rose-600 tabular-nums">
                                {shift.totalPay}€
                            </p>
                            <p className="text-[9px] text-slate-500">{shift.hourlyRate}€/h</p>
                        </div>
                    </div>
                    
                    {/* Center: Info */}
                    <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1.5">
                            <span className={cn(
                                'px-2 py-0.5 text-[9px] font-bold rounded-full uppercase tracking-wider',
                                config.badge,
                                shift.urgency === 'critical' && 'animate-pulse'
                            )}>
                                {config.label}
                            </span>
                            {shift.expiresIn && (
                                <span className="flex items-center gap-1 text-[10px] text-rose-500">
                                    <Timer size={10} />
                                    Expire: {shift.expiresIn}
                                </span>
                            )}
                            {shift.verified && (
                                <Shield className="w-3.5 h-3.5 text-emerald-500" />
                            )}
                        </div>
                        <h3 className="font-bold text-slate-900 truncate group-hover:text-rose-600 transition-colors">
                            {shift.establishment}
                        </h3>
                        <p className="text-sm text-slate-500 truncate">{shift.unit}</p>
                        
                        {/* Meta row */}
                        <div className="flex items-center gap-4 mt-2">
                            <span className="flex items-center gap-1.5 text-xs text-slate-600">
                                <Clock size={12} className="text-slate-400" />
                                <span className="font-mono">{shift.time}</span>
                            </span>
                            <span className="flex items-center gap-1.5 text-xs text-slate-600">
                                <Navigation size={12} className="text-slate-400" />
                                <span className="font-mono">{shift.distance} km</span>
                            </span>
                            <span className="text-xs text-slate-500">
                                {shift.date}
                            </span>
                        </div>
                    </div>
                    
                    {/* Right: CTA */}
                    <div className="flex flex-col items-center justify-between self-stretch">
                        <span className="text-xs font-bold text-slate-500 font-mono">{shift.duration}</span>
                        <button className="flex items-center gap-1 px-3 py-1.5 bg-rose-500 text-white text-xs font-bold rounded-lg hover:bg-rose-400 transition-colors shadow-lg shadow-rose-200">
                            <Zap size={12} />
                            ACCEPTER
                        </button>
                    </div>
                </div>
            </Link>
        </motion.div>
    );
}

/** Quick filters - Light mode */
function QuickFilters({ activeFilter, setActiveFilter }: { 
    activeFilter: string; 
    setActiveFilter: (f: string) => void;
}) {
    const filters = [
        { id: 'all', label: 'Toutes', count: 5 },
        { id: 'critical', label: '🚨 Urgentes', count: 2 },
        { id: 'IDE', label: 'IDE', count: 3 },
        { id: 'AS', label: 'AS', count: 2 },
        { id: 'night', label: '🌙 Nuit', count: 2 },
        { id: 'near', label: '📍 < 10km', count: 3 },
    ];
    
    return (
        <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-hide">
            {filters.map((filter) => (
                <button
                    key={filter.id}
                    onClick={() => setActiveFilter(filter.id)}
                    className={cn(
                        'flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-all border',
                        activeFilter === filter.id
                            ? 'bg-rose-50 text-rose-700 border-rose-300'
                            : 'bg-white text-slate-600 border-slate-200 hover:border-rose-200 hover:bg-rose-50/50'
                    )}
                >
                    {filter.label}
                    <span className={cn(
                        'px-1.5 py-0.5 rounded-full text-[10px] font-bold',
                        activeFilter === filter.id ? 'bg-rose-200 text-rose-800' : 'bg-slate-100 text-slate-500'
                    )}>
                        {filter.count}
                    </span>
                </button>
            ))}
        </div>
    );
}

/** Stats bar - Light mode */
function StatsBar({ earnings }: { earnings: EarningsData }) {
    return (
        <div className="grid grid-cols-4 gap-2 p-4 bg-white rounded-2xl border border-slate-200 shadow-sm">
            <EarningsCounter value={earnings.today} label="Aujourd'hui" trend="up" />
            <EarningsCounter value={earnings.week} label="Cette semaine" />
            <EarningsCounter value={earnings.month} label="Ce mois" />
            <div className="text-center">
                <div className="flex items-center justify-center gap-1">
                    <Star className="w-4 h-4 text-amber-400 fill-amber-400" />
                    <span className="text-2xl lg:text-3xl font-bold font-mono tabular-nums text-slate-900">4.9</span>
                </div>
                <p className="text-[10px] text-slate-500 uppercase tracking-wider mt-0.5">Note</p>
            </div>
        </div>
    );
}

// =============================================================================
// MAIN COMPONENT — Stock Ticker Dashboard (Light Mode)
// =============================================================================

export function MedicalTalentDashboard({ user }: MedicalTalentDashboardProps) {
    const [isAvailable, setIsAvailable] = useState(true);
    const [activeFilter, setActiveFilter] = useState('all');
    const criticalCount = mockShifts.filter(s => s.urgency === 'critical').length;

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-rose-50 dark:from-slate-950 dark:via-slate-900 dark:to-rose-950/30 transition-colors">
            {/* Top Control Bar */}
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="sticky top-0 z-40 bg-white/80 backdrop-blur-xl border-b border-slate-200"
            >
                <div className="px-4 py-3 flex flex-col lg:flex-row lg:items-center justify-between gap-3">
                    <div className="flex items-center gap-4">
                        <div>
                            <p className="text-slate-500 text-xs">Bonjour 👋</p>
                            <h1 className="text-lg font-bold text-slate-900">{user?.name || userName}</h1>
                        </div>
                        {criticalCount > 0 && (
                            <div className="flex items-center gap-2 px-3 py-1.5 bg-rose-100 border border-rose-200 rounded-full">
                                <Bell className="w-4 h-4 text-rose-500 animate-pulse" />
                                <span className="text-sm font-bold text-rose-600">{criticalCount} urgentes</span>
                            </div>
                        )}
                    </div>
                    
                    <div className="flex items-center gap-3">
                        <AvailabilityToggle isOn={isAvailable} onToggle={() => setIsAvailable(!isAvailable)} />
                        <WalletDisplay balance={mockEarnings.month} />
                    </div>
                </div>
            </motion.div>

            <motion.div
                variants={containerVariants}
                initial="hidden"
                animate="visible"
                className="p-4 space-y-4 max-w-4xl mx-auto"
            >
                {/* Profile Alert */}
                <DashboardAlert 
                    ctaLink="/dashboard/talent/profile"
                    ctaText="Compléter mon profil"
                />

                {/* Earnings Stats Bar */}
                <motion.div variants={itemVariants}>
                    <StatsBar earnings={mockEarnings} />
                </motion.div>

                {/* Job Ticker Section */}
                <div className="space-y-3">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                                <Activity className="w-4 h-4 text-rose-500" />
                                {getTerm('missionPlural')} disponibles
                            </h2>
                        </div>
                        <button 
                            className="p-2 hover:bg-slate-100 rounded-lg transition-colors border border-slate-200"
                            title="Actualiser"
                            aria-label="Actualiser la liste"
                        >
                            <RefreshCw size={16} className="text-slate-500" />
                        </button>
                    </div>

                    {/* Quick Filters */}
                    <QuickFilters activeFilter={activeFilter} setActiveFilter={setActiveFilter} />

                    {/* Shift Ticker List */}
                    <AnimatePresence mode="popLayout">
                        {isAvailable ? (
                            <motion.div className="space-y-3">
                                {mockShifts.map((shift, index) => (
                                    <ShiftTickerCard key={shift.id} shift={shift} index={index} />
                                ))}
                            </motion.div>
                        ) : (
                            <motion.div
                                initial={{ opacity: 0, scale: 0.95 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.95 }}
                            >
                                <Card className="border-2 border-dashed border-rose-200 bg-rose-50/50">
                                    <CardContent className="p-8 flex flex-col items-center text-center">
                                        <div className="p-4 bg-rose-100 rounded-2xl mb-4">
                                            <Siren size={32} className="text-rose-400" />
                                        </div>
                                        <h3 className="font-bold text-slate-700">Mode repos activé</h3>
                                        <p className="text-sm text-slate-500 mt-1 mb-4">
                                            Activez votre disponibilité pour voir les {getTerm('missionPlural').toLowerCase()} urgentes
                                        </p>
                                        <button
                                            onClick={() => setIsAvailable(true)}
                                            className="px-5 py-2.5 bg-gradient-to-r from-rose-500 to-rose-600 text-white font-semibold rounded-xl hover:from-rose-600 hover:to-rose-700 transition-colors shadow-lg shadow-rose-200"
                                        >
                                            Activer ma disponibilité
                                        </button>
                                    </CardContent>
                                </Card>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>

                {/* Quick Access */}
                <motion.div variants={itemVariants} className="grid grid-cols-2 gap-3">
                    <Link
                        href="/dashboard/talent/planning"
                        className="flex items-center gap-3 p-4 bg-white border border-slate-200 rounded-xl hover:border-blue-300 hover:shadow-md transition-all group"
                    >
                        <div className="p-2 bg-blue-100 rounded-lg">
                            <Calendar size={20} className="text-blue-600" />
                        </div>
                        <div className="flex-1">
                            <p className="font-semibold text-slate-900">Mon Planning</p>
                            <p className="text-[10px] text-slate-500">{getTerm('availability')}</p>
                        </div>
                        <ChevronRight size={16} className="text-slate-400 group-hover:translate-x-1 group-hover:text-blue-500 transition-all" />
                    </Link>

                    <Link
                        href="/dashboard/talent/missions"
                        className="flex items-center gap-3 p-4 bg-white border border-slate-200 rounded-xl hover:border-emerald-300 hover:shadow-md transition-all group"
                    >
                        <div className="p-2 bg-emerald-100 rounded-lg">
                            <CheckCircle2 size={20} className="text-emerald-600" />
                        </div>
                        <div className="flex-1">
                            <p className="font-semibold text-slate-900">Mes {getTerm('missionPlural')}</p>
                            <p className="text-[10px] text-slate-500">Historique</p>
                        </div>
                        <ChevronRight size={16} className="text-slate-400 group-hover:translate-x-1 group-hover:text-emerald-500 transition-all" />
                    </Link>
                </motion.div>
            </motion.div>
        </div>
    );
}

export default MedicalTalentDashboard;
