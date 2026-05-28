'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import {
    Siren,
    Calendar,
    AlertTriangle,
    Wallet,
    ChevronRight,
    Clock,
    FileSignature,
    Users,
    CalendarClock,
    Plus,
    Filter,
    ChevronLeft,
    Activity,
    RefreshCw,
    Bell,
    Shield,
    CheckCircle2,
    Zap,
    Radio,
} from 'lucide-react';
import { Badge } from '@/components/ui';
import { DashboardAlert } from '@/components/dashboard';
import { getTerm } from '@/lib/domain-config';
import { cn } from '@/lib/utils';
import type { DashboardUser } from '../DashboardResolver';

// =============================================================================
// TYPES — Air Traffic Control Data Structures
// =============================================================================

interface MedicalClientDashboardProps {
    user?: DashboardUser;
}

interface ShiftSlot {
    id: string;
    time: string;
    endTime: string;
    talentName?: string;
    talentRole: 'IDE' | 'AS' | 'AES' | 'AIDE_SOIGNANT';
    status: 'filled' | 'open' | 'urgent' | 'critical';
    unit: string;
    verified: boolean;
}

interface DayColumn {
    date: Date;
    dayName: string;
    dayNumber: number;
    monthShort: string;
    isToday: boolean;
    shifts: ShiftSlot[];
}

interface AlertItem {
    id: string;
    type: 'critical' | 'warning' | 'info';
    message: string;
    time: string;
    action?: string;
    actionHref?: string;
}

// =============================================================================
// ANIMATION VARIANTS — Bloomberg Terminal Feel
// =============================================================================

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: { staggerChildren: 0.05, delayChildren: 0.1 }
    }
} as const;

const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.4 } }
} as const;

// =============================================================================
// MOCK DATA — Simulating Real-time Hospital Operations
// =============================================================================

const generateWeekData = (): DayColumn[] => {
    const today = new Date();
    const days: DayColumn[] = [];
    const dayNames = ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'];
    const monthNames = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'];
    
    const mockShifts: Omit<ShiftSlot, 'id'>[][] = [
        // Today - some critical
        [
            { time: '07:00', endTime: '14:00', talentName: 'Marie L.', talentRole: 'IDE', status: 'filled', unit: 'Étage 1', verified: true },
            { time: '14:00', endTime: '21:00', talentRole: 'AS', status: 'critical', unit: 'Étage 2', verified: false },
            { time: '21:00', endTime: '07:00', talentName: 'Thomas D.', talentRole: 'IDE', status: 'filled', unit: 'Nuit', verified: true },
        ],
        // Tomorrow
        [
            { time: '07:00', endTime: '14:00', talentRole: 'IDE', status: 'urgent', unit: 'Étage 1', verified: false },
            { time: '14:00', endTime: '21:00', talentName: 'Sophie M.', talentRole: 'AS', status: 'filled', unit: 'Étage 1', verified: true },
        ],
        // Day 3
        [
            { time: '07:00', endTime: '14:00', talentName: 'Pierre R.', talentRole: 'AES', status: 'filled', unit: 'Étage 2', verified: true },
            { time: '14:00', endTime: '21:00', talentRole: 'IDE', status: 'open', unit: 'Urgences', verified: false },
        ],
        // Day 4
        [
            { time: '07:00', endTime: '14:00', talentRole: 'AS', status: 'open', unit: 'Étage 1', verified: false },
            { time: '14:00', endTime: '21:00', talentName: 'Léa B.', talentRole: 'IDE', status: 'filled', unit: 'Étage 2', verified: true },
        ],
        // Day 5
        [
            { time: '07:00', endTime: '14:00', talentName: 'Julie B.', talentRole: 'IDE', status: 'filled', unit: 'Étage 1', verified: true },
            { time: '14:00', endTime: '21:00', talentName: 'Marc T.', talentRole: 'AS', status: 'filled', unit: 'Étage 2', verified: false },
        ],
        // Day 6
        [
            { time: '07:00', endTime: '19:00', talentRole: 'IDE', status: 'open', unit: 'Week-end', verified: false },
        ],
        // Day 7
        [
            { time: '07:00', endTime: '19:00', talentRole: 'AS', status: 'open', unit: 'Week-end', verified: false },
        ],
    ];

    for (let i = 0; i < 7; i++) {
        const date = new Date(today);
        date.setDate(today.getDate() + i);
        
        days.push({
            date,
            dayName: dayNames[date.getDay()],
            dayNumber: date.getDate(),
            monthShort: monthNames[date.getMonth()],
            isToday: i === 0,
            shifts: mockShifts[i].map((s, j) => ({ ...s, id: `${i}-${j}` })),
        });
    }
    
    return days;
};

const mockAlerts: AlertItem[] = [
    { id: '1', type: 'critical', message: '1 poste IDE non pourvu pour ce soir 14h-21h', time: 'À l\'instant', action: 'SOS', actionHref: '/sos/new' },
    { id: '2', type: 'warning', message: 'ADELI Thomas D. expire dans 15j', time: 'Il y a 2h', action: 'Vérifier', actionHref: '/dashboard/client/team' },
    { id: '3', type: 'info', message: '3 soignants disponibles dans votre secteur', time: 'Il y a 5h' },
];

// =============================================================================
// SUB-COMPONENTS — Dense, Data-Rich Night Shift UI
// =============================================================================

/** Real-time clock for dispatch feel */
function LiveClock() {
    const [time, setTime] = useState(new Date());
    
    useEffect(() => {
        const interval = setInterval(() => setTime(new Date()), 1000);
        return () => clearInterval(interval);
    }, []);
    
    return (
        <div className="flex items-center gap-2 px-3 py-1.5 bg-white rounded-lg border border-slate-200 shadow-sm">
            <Radio className="h-3 w-3 text-rose-500 animate-pulse" />
            <span className="font-mono text-sm font-bold text-slate-900 tabular-nums">
                {time.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
            </span>
        </div>
    );
}

/** Critical alert banner with scanning animation */
function CriticalAlertBanner({ alerts }: { alerts: AlertItem[] }) {
    const critical = alerts.find(a => a.type === 'critical');
    if (!critical) return null;
    
    return (
        <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="relative overflow-hidden rounded-2xl border-2 border-rose-300 bg-gradient-to-r from-rose-50 via-white to-rose-50 shadow-lg shadow-rose-100"
        >
            {/* Scanning line animation */}
            <motion.div
                className="absolute inset-0 bg-gradient-to-r from-transparent via-rose-200/30 to-transparent"
                animate={{ x: ['-100%', '100%'] }}
                transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
            />
            
            <div className="relative flex items-center justify-between p-4">
                <div className="flex items-center gap-4">
                    <div className="flex items-center justify-center h-12 w-12 rounded-xl bg-rose-100 border border-rose-200">
                        <Siren className="h-6 w-6 text-rose-500 animate-pulse" />
                    </div>
                    <div>
                        <div className="flex items-center gap-2">
                            <span className="text-rose-600 text-[10px] font-bold uppercase tracking-widest">
                                ALERTE CRITIQUE
                            </span>
                            <span className="flex h-2 w-2 rounded-full bg-rose-500 animate-ping" />
                        </div>
                        <p className="text-slate-900 font-semibold mt-0.5">{critical.message}</p>
                    </div>
                </div>
                
                {critical.action && (
                    <Link
                        href={critical.actionHref || '#'}
                        className="flex items-center gap-2 px-5 py-2.5 bg-rose-500 text-white font-bold rounded-xl hover:bg-rose-400 transition-all shadow-lg shadow-rose-200 hover:shadow-rose-300"
                    >
                        <Zap className="h-4 w-4" />
                        Lancer {critical.action}
                    </Link>
                )}
            </div>
        </motion.div>
    );
}

/** Compact shift cell for week grid */
function ShiftCell({ shift }: { shift: ShiftSlot }) {
    const statusConfig = {
        filled: { 
            bg: 'bg-emerald-50 border-emerald-200 hover:border-emerald-300', 
            text: 'text-emerald-600',
            icon: CheckCircle2,
            label: 'Pourvu'
        },
        open: { 
            bg: 'bg-slate-50 border-slate-200 border-dashed hover:border-slate-300', 
            text: 'text-slate-500',
            icon: Clock,
            label: 'À pourvoir'
        },
        urgent: { 
            bg: 'bg-amber-50 border-amber-300 hover:border-amber-400', 
            text: 'text-amber-600',
            icon: AlertTriangle,
            label: 'Urgent'
        },
        critical: { 
            bg: 'bg-rose-50 border-rose-300 animate-pulse hover:border-rose-400', 
            text: 'text-rose-600',
            icon: Siren,
            label: 'Critique'
        },
    };
    
    const config = statusConfig[shift.status];
    const Icon = config.icon;
    
    const roleColors: Record<string, string> = {
        IDE: 'bg-rose-100 text-rose-700 border-rose-300',
        AS: 'bg-blue-100 text-blue-700 border-blue-300',
        AES: 'bg-violet-100 text-violet-700 border-violet-300',
        AIDE_SOIGNANT: 'bg-teal-100 text-teal-700 border-teal-300',
    };

    return (
        <motion.div
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className={cn(
                'relative p-2 rounded-lg border cursor-pointer transition-all bg-white shadow-sm',
                config.bg
            )}
        >
            {/* Time + Role header */}
            <div className="flex items-center justify-between mb-1.5">
                <span className="font-mono text-[11px] font-bold text-slate-700">{shift.time}</span>
                <span className={cn('px-1.5 py-0.5 rounded text-[9px] font-bold border', roleColors[shift.talentRole])}>
                    {shift.talentRole}
                </span>
            </div>
            
            {/* Status + Name */}
            <div className="flex items-center gap-1.5">
                <Icon className={cn('h-3 w-3 shrink-0', config.text)} />
                <span className={cn('text-[11px] font-medium truncate', config.text)}>
                    {shift.talentName || config.label}
                </span>
            </div>
            
            {/* Unit */}
            <p className="text-[9px] text-slate-500 mt-1 truncate">{shift.unit}</p>
            
            {/* Verified badge */}
            {shift.verified && (
                <div className="absolute top-1.5 right-1.5">
                    <Shield className="h-2.5 w-2.5 text-emerald-500" />
                </div>
            )}
            
            {/* Action button for open slots */}
            {(shift.status === 'open' || shift.status === 'urgent' || shift.status === 'critical') && (
                <button className="w-full mt-2 py-1 text-[9px] font-bold rounded bg-rose-100 text-rose-600 hover:bg-rose-200 transition-colors border border-rose-200">
                    + POURVOIR
                </button>
            )}
        </motion.div>
    );
}

/** Week calendar grid - responsive with mobile day view */
function WeekGrid({ data, selectedDay, setSelectedDay }: { 
    data: DayColumn[]; 
    selectedDay: number;
    setSelectedDay: (day: number) => void;
}) {
    return (
        <>
            {/* Mobile: Day selector + single day view */}
            <div className="lg:hidden">
                <div className="flex gap-1 mb-3 overflow-x-auto pb-2 scrollbar-hide">
                    {data.map((day, index) => (
                        <button
                            key={day.dayNumber}
                            onClick={() => setSelectedDay(index)}
                            className={cn(
                                'flex flex-col items-center min-w-[52px] px-3 py-2 rounded-lg border transition-all',
                                selectedDay === index
                                    ? 'bg-rose-500 text-white border-rose-400 shadow-lg shadow-rose-200'
                                    : day.isToday
                                        ? 'bg-rose-50 text-rose-700 border-rose-200'
                                        : 'bg-white text-slate-600 border-slate-200 hover:border-rose-200'
                            )}
                        >
                            <span className="text-[10px] font-medium uppercase">{day.dayName}</span>
                            <span className="text-lg font-bold">{day.dayNumber}</span>
                        </button>
                    ))}
                </div>
                
                {/* Single day shifts */}
                <div className="space-y-2 min-h-[200px]">
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={selectedDay}
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="space-y-2"
                        >
                            {data[selectedDay]?.shifts.map((shift) => (
                                <ShiftCell key={shift.id} shift={shift} />
                            ))}
                            {data[selectedDay]?.shifts.length === 0 && (
                                <div className="p-6 text-center text-slate-500 text-sm">
                                    Aucune vacation ce jour
                                </div>
                            )}
                        </motion.div>
                    </AnimatePresence>
                </div>
            </div>
            
            {/* Desktop: Full 7-column grid */}
            <div className="hidden lg:grid lg:grid-cols-7 gap-2">
                {data.map((day) => (
                    <div key={day.dayNumber} className="min-w-0">
                        {/* Day header */}
                        <div className={cn(
                            'text-center p-2 rounded-t-lg border-b-2',
                            day.isToday
                                ? 'bg-rose-500 text-white border-rose-400'
                                : 'bg-slate-100 text-slate-700 border-slate-200'
                        )}>
                            <p className="text-[10px] font-medium uppercase tracking-wider opacity-70">{day.dayName}</p>
                            <p className="text-lg font-bold font-mono">{day.dayNumber}</p>
                            <p className="text-[10px] opacity-50">{day.monthShort}</p>
                        </div>
                        
                        {/* Shifts column */}
                        <div className="space-y-1.5 p-1.5 bg-slate-50 rounded-b-lg min-h-[260px] border border-t-0 border-slate-200">
                            <AnimatePresence>
                                {day.shifts.map((shift) => (
                                    <motion.div
                                        key={shift.id}
                                        initial={{ opacity: 0, scale: 0.9 }}
                                        animate={{ opacity: 1, scale: 1 }}
                                        exit={{ opacity: 0, scale: 0.9 }}
                                    >
                                        <ShiftCell shift={shift} />
                                    </motion.div>
                                ))}
                            </AnimatePresence>
                            
                            {day.shifts.length === 0 && (
                                <div className="h-full flex items-center justify-center p-4">
                                    <p className="text-[10px] text-slate-400 text-center">Aucune vacation</p>
                                </div>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </>
    );
}

/** Quick stats bar - Light mode */
function QuickStats({ data }: { data: DayColumn[] }) {
    const totalShifts = data.reduce((acc, d) => acc + d.shifts.length, 0);
    const openShifts = data.reduce((acc, d) => acc + d.shifts.filter(s => s.status !== 'filled').length, 0);
    const filledShifts = totalShifts - openShifts;
    const coverageRate = totalShifts > 0 ? Math.round((filledShifts / totalShifts) * 100) : 0;
    const criticalCount = data.reduce((acc, d) => acc + d.shifts.filter(s => s.status === 'critical').length, 0);
    
    const stats = [
        { label: 'Total vacations', value: totalShifts, color: 'text-slate-900' },
        { label: 'À pourvoir', value: openShifts, color: openShifts > 3 ? 'text-rose-600' : 'text-amber-600', alert: openShifts > 3 },
        { label: 'Critiques', value: criticalCount, color: criticalCount > 0 ? 'text-rose-600' : 'text-emerald-600', alert: criticalCount > 0 },
        { label: 'Couverture', value: `${coverageRate}%`, color: coverageRate >= 80 ? 'text-emerald-600' : 'text-amber-600' },
    ];
    
    return (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-2">
            {stats.map((stat) => (
                <div 
                    key={stat.label} 
                    className={cn(
                        'p-4 bg-white rounded-xl border transition-all shadow-sm',
                        stat.alert ? 'border-rose-200' : 'border-slate-200'
                    )}
                >
                    <div className="flex items-baseline gap-1">
                        <span className={cn('text-2xl font-bold font-mono tabular-nums', stat.color)}>
                            {stat.value}
                        </span>
                        {stat.alert && <span className="flex h-2 w-2 rounded-full bg-rose-500 animate-pulse" />}
                    </div>
                    <p className="text-[10px] text-slate-500 mt-0.5 uppercase tracking-wider">{stat.label}</p>
                </div>
            ))}
        </div>
    );
}

/** Alerts sidebar - Light mode */
function AlertsSidebar({ alerts }: { alerts: AlertItem[] }) {
    const typeConfig = {
        critical: { bg: 'bg-rose-50 border-rose-200', icon: Siren, color: 'text-rose-600' },
        warning: { bg: 'bg-amber-50 border-amber-200', icon: AlertTriangle, color: 'text-amber-600' },
        info: { bg: 'bg-blue-50 border-blue-200', icon: Bell, color: 'text-blue-600' },
    };
    
    return (
        <div className="space-y-3">
            <div className="flex items-center justify-between">
                <h3 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest flex items-center gap-2">
                    <Activity className="h-3 w-3" /> Flux alertes
                </h3>
                <span className="text-[10px] text-slate-400">Live</span>
            </div>
            <div className="space-y-2">
                {alerts.map((alert) => {
                    const config = typeConfig[alert.type];
                    const Icon = config.icon;
                    return (
                        <motion.div 
                            key={alert.id} 
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            className={cn('p-3 rounded-lg border', config.bg)}
                        >
                            <div className="flex items-start gap-2">
                                <Icon className={cn('h-4 w-4 mt-0.5 shrink-0', config.color)} />
                                <div className="flex-1 min-w-0">
                                    <p className="text-[11px] text-slate-700 leading-snug">{alert.message}</p>
                                    <div className="flex items-center gap-2 mt-1">
                                        <span className="text-[9px] text-slate-500">{alert.time}</span>
                                        {alert.action && (
                                            <Link 
                                                href={alert.actionHref || '#'} 
                                                className={cn('text-[10px] font-semibold', config.color)}
                                            >
                                                {alert.action} →
                                            </Link>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    );
                })}
            </div>
        </div>
    );
}

// =============================================================================
// MAIN COMPONENT — Air Traffic Control Dashboard (Light Mode)
// =============================================================================

export function MedicalClientDashboard({ user }: MedicalClientDashboardProps) {
    const [weekData] = useState(generateWeekData);
    const [selectedDay, setSelectedDay] = useState(0);
    
    const openSlots = weekData.reduce((acc, day) => acc + day.shifts.filter(s => s.status !== 'filled').length, 0);

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-rose-50 dark:from-slate-950 dark:via-slate-900 dark:to-rose-950/30 transition-colors">
            {/* Top Control Bar - Sticky */}
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="sticky top-0 z-40 bg-white/80 backdrop-blur-xl border-b border-slate-200"
            >
                <div className="px-4 py-3 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <div>
                            <h1 className="text-base lg:text-lg font-bold text-slate-900">{getTerm('dashboardTitle')}</h1>
                            <p className="text-[10px] lg:text-xs text-slate-500 hidden sm:block">Centre de contrôle</p>
                        </div>
                        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-white rounded-lg border border-slate-200 shadow-sm">
                            <span className="text-[10px] text-slate-500">Postes ouverts:</span>
                            <span className={cn(
                                'font-mono font-bold text-sm tabular-nums',
                                openSlots > 5 ? 'text-rose-600' : 'text-emerald-600'
                            )}>
                                {openSlots}
                            </span>
                            {openSlots > 3 && <span className="flex h-2 w-2 rounded-full bg-rose-500 animate-pulse" />}
                        </div>
                    </div>
                    
                    <div className="flex items-center gap-2 lg:gap-3">
                        <LiveClock />
                        <button 
                            className="p-2 hover:bg-slate-100 rounded-lg transition-colors border border-slate-200"
                            title="Actualiser les données"
                            aria-label="Actualiser"
                        >
                            <RefreshCw className="h-4 w-4 text-slate-500" />
                        </button>
                        <Link
                            href="/sos/new"
                            className="flex items-center gap-2 px-3 lg:px-4 py-2 bg-rose-500 text-white font-semibold rounded-xl hover:bg-rose-400 transition-all shadow-lg shadow-rose-200"
                        >
                            <Siren className="h-4 w-4" />
                            <span className="hidden sm:inline">SOS Renfort</span>
                        </Link>
                    </div>
                </div>
            </motion.div>

            {/* Main Content */}
            <motion.div
                variants={containerVariants}
                initial="hidden"
                animate="visible"
                className="p-3 lg:p-4 space-y-4"
            >
                {/* Alert Banner */}
                <DashboardAlert ctaLink="/dashboard/client/settings" ctaText="Compléter le profil" />
                
                {/* Critical Alert */}
                <motion.div variants={itemVariants}>
                    <CriticalAlertBanner alerts={mockAlerts} />
                </motion.div>
                
                {/* Quick Stats */}
                <motion.div variants={itemVariants}>
                    <QuickStats data={weekData} />
                </motion.div>
                
                {/* Main Grid: Calendar + Alerts */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
                    {/* Calendar Panel */}
                    <motion.div variants={itemVariants} className="lg:col-span-9 bg-white rounded-2xl border border-slate-200 p-3 lg:p-4 shadow-sm">
                        <div className="flex items-center justify-between mb-4">
                            <div className="flex items-center gap-2">
                                <Calendar className="h-4 w-4 text-rose-500" />
                                <h2 className="font-semibold text-slate-900">Planning Semaine</h2>
                            </div>
                            <div className="hidden lg:flex items-center gap-2">
                                <button 
                                    className="p-1.5 hover:bg-slate-100 rounded-lg transition-colors"
                                    title="Semaine précédente"
                                    aria-label="Semaine précédente"
                                >
                                    <ChevronLeft className="h-4 w-4 text-slate-500" />
                                </button>
                                <button className="px-3 py-1 text-xs font-medium text-slate-700 hover:bg-slate-100 rounded-lg transition-colors">
                                    Cette semaine
                                </button>
                                <button 
                                    className="p-1.5 hover:bg-slate-100 rounded-lg transition-colors"
                                    title="Semaine suivante"
                                    aria-label="Semaine suivante"
                                >
                                    <ChevronRight className="h-4 w-4 text-slate-500" />
                                </button>
                                <div className="w-px h-4 bg-slate-200 mx-1" />
                                <button 
                                    className="p-1.5 hover:bg-slate-100 rounded-lg transition-colors"
                                    title="Filtrer"
                                    aria-label="Filtrer les vacations"
                                >
                                    <Filter className="h-4 w-4 text-slate-500" />
                                </button>
                            </div>
                        </div>
                        <WeekGrid data={weekData} selectedDay={selectedDay} setSelectedDay={setSelectedDay} />
                    </motion.div>
                    
                    {/* Right Sidebar: Alerts + Quick Actions */}
                    <motion.div variants={itemVariants} className="lg:col-span-3 space-y-4">
                        <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm">
                            <AlertsSidebar alerts={mockAlerts} />
                        </div>
                        
                        <div className="bg-white rounded-2xl border border-slate-200 p-4 space-y-2 shadow-sm">
                            <h3 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Actions rapides</h3>
                            <Link href="/sos/new" className="flex items-center gap-3 p-3 bg-rose-50 border border-rose-200 rounded-xl hover:bg-rose-100 transition-colors group">
                                <Siren className="h-5 w-5 text-rose-500" />
                                <div className="flex-1">
                                    <p className="text-sm font-semibold text-rose-700">Lancer SOS</p>
                                    <p className="text-[10px] text-slate-500">Renfort urgent</p>
                                </div>
                                <ChevronRight className="h-4 w-4 text-slate-400 group-hover:translate-x-1 transition-transform" />
                            </Link>
                            <Link href="/dashboard/client/team" className="flex items-center gap-3 p-3 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 transition-colors group">
                                <Users className="h-5 w-5 text-blue-500" />
                                <div className="flex-1">
                                    <p className="text-sm font-semibold text-slate-700">Mon Vivier</p>
                                    <p className="text-[10px] text-slate-500">18 soignants</p>
                                </div>
                                <ChevronRight className="h-4 w-4 text-slate-400 group-hover:translate-x-1 transition-transform" />
                            </Link>
                            <Link href="/dashboard/client/finance" className="flex items-center gap-3 p-3 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 transition-colors group">
                                <Wallet className="h-5 w-5 text-emerald-500" />
                                <div className="flex-1">
                                    <p className="text-sm font-semibold text-slate-700">Finance</p>
                                    <p className="text-[10px] text-slate-500">3 450 € ce mois</p>
                                </div>
                                <ChevronRight className="h-4 w-4 text-slate-400 group-hover:translate-x-1 transition-transform" />
                            </Link>
                            <Link href="/contracts" className="flex items-center gap-3 p-3 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 transition-colors group">
                                <FileSignature className="h-5 w-5 text-amber-500" />
                                <div className="flex-1">
                                    <p className="text-sm font-semibold text-slate-700">Contrats</p>
                                    <p className="text-[10px] text-slate-500">2 en attente</p>
                                </div>
                                <ChevronRight className="h-4 w-4 text-slate-400 group-hover:translate-x-1 transition-transform" />
                            </Link>
                        </div>
                    </motion.div>
                </div>
            </motion.div>
        </div>
    );
}

export default MedicalClientDashboard;
