'use client';

import { useState } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Siren,
    Calendar,
    Clock,
    CheckCircle2,
    ArrowRight,
    Star,
    MapPin,
    Wallet,
    ChevronRight,
    Briefcase,
    BookOpen,
    Sparkles,
    Heart,
    Users,
    Quote,
    Edit3,
    Share2,
    Shield,
    MessageCircle,
    Lightbulb,
} from 'lucide-react';
import { Card, CardContent, Badge } from '@/components/ui';
import { DashboardAlert } from '@/components/dashboard';
import { getTerm, isFeatureEnabled, domainConfig } from '@/lib/domain-config';
import { cn } from '@/lib/utils';
import type { DashboardUser } from '../DashboardResolver';

// =============================================================================
// ANIMATION VARIANTS — Behance Portfolio Style
// =============================================================================

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: { staggerChildren: 0.1, delayChildren: 0.1 }
    }
} as const;

const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.4 } }
} as const;

const cardHover = {
    rest: { scale: 1, y: 0 },
    hover: { scale: 1.02, y: -4, transition: { duration: 0.3 } }
} as const;

// =============================================================================
// TYPES — Portfolio & Meaningful Missions
// =============================================================================

interface SocialTalentDashboardProps {
    user?: DashboardUser;
}

interface PortfolioSkill {
    id: string;
    name: string;
    level: 'junior' | 'confirmé' | 'expert';
    endorsements: number;
    icon: React.ElementType;
    color: string;
}

interface SavoirEtre {
    id: string;
    trait: string;
    emoji: string;
    votedBy: number;
}

interface MeaningfulMission {
    id: string;
    title: string;
    establishment: string;
    establishmentAvatar: string;
    description: string;
    impact: string; // "12 familles accompagnées"
    distance: string;
    duration: string;
    values: string[]; // matching values
    urgency: 'normal' | 'soon' | 'urgent';
    matchScore: number; // 0-100
}

interface PortfolioStats {
    missionsCompleted: number;
    hoursWorked: number;
    avgRating: number;
    familiesHelped: number;
    endorsements: number;
}

interface TestimonialItem {
    id: string;
    text: string;
    author: string;
    role: string;
    avatar: string;
    rating: number;
}

// =============================================================================
// MOCK DATA — Behance Portfolio Style
// =============================================================================

const mockPortfolioSkills: PortfolioSkill[] = [
    { id: '1', name: 'Éducation spécialisée', level: 'expert', endorsements: 24, icon: BookOpen, color: 'teal' },
    { id: '2', name: 'Animation de groupe', level: 'expert', endorsements: 18, icon: Users, color: 'violet' },
    { id: '3', name: 'Accompagnement familial', level: 'confirmé', endorsements: 12, icon: Heart, color: 'rose' },
    { id: '4', name: 'Médiation', level: 'confirmé', endorsements: 9, icon: MessageCircle, color: 'blue' },
];

const mockSavoirEtre: SavoirEtre[] = [
    { id: '1', trait: 'Patient·e', emoji: '🧘', votedBy: 15 },
    { id: '2', trait: 'Créatif·ve', emoji: '🎨', votedBy: 12 },
    { id: '3', trait: 'À l\'écoute', emoji: '👂', votedBy: 18 },
    { id: '4', trait: 'Dynamique', emoji: '⚡', votedBy: 9 },
    { id: '5', trait: 'Bienveillant·e', emoji: '💚', votedBy: 21 },
];

const mockMissions: MeaningfulMission[] = [
    {
        id: '1',
        title: 'Accompagnement éducatif weekend',
        establishment: 'MECS Les Jardins',
        establishmentAvatar: '/images/establishments/mecs-jardins.jpg',
        description: 'Animation et soutien pour groupe d\'adolescents en difficulté sociale',
        impact: '8 jeunes accompagnés',
        distance: '5 km',
        duration: 'Sam-Dim • 8h-18h',
        values: ['Bienveillance', 'Écoute'],
        urgency: 'soon',
        matchScore: 94,
    },
    {
        id: '2',
        title: 'Atelier d\'expression artistique',
        establishment: 'Foyer de Vie Harmonie',
        establishmentAvatar: '/images/establishments/foyer-harmonie.jpg',
        description: 'Animez des séances de peinture et expression créative pour adultes en situation de handicap',
        impact: '12 résidents par atelier',
        distance: '8 km',
        duration: 'Mer • 14h-17h',
        values: ['Créativité', 'Patience'],
        urgency: 'normal',
        matchScore: 87,
    },
    {
        id: '3',
        title: 'Soutien scolaire adolescents',
        establishment: 'IME Horizon',
        establishmentAvatar: '/images/establishments/ime-horizon.jpg',
        description: 'Aide aux devoirs et accompagnement pédagogique personnalisé',
        impact: '5 familles soutenues',
        distance: '3 km',
        duration: 'Lun-Jeu • 17h-19h',
        values: ['Pédagogie', 'Patience'],
        urgency: 'normal',
        matchScore: 82,
    },
];

const mockStats: PortfolioStats = {
    missionsCompleted: 47,
    hoursWorked: 312,
    avgRating: 4.9,
    familiesHelped: 89,
    endorsements: 73,
};

const mockTestimonials: TestimonialItem[] = [
    {
        id: '1',
        text: 'Thomas a su créer un lien de confiance remarquable avec nos résidents. Son approche bienveillante fait toute la différence.',
        author: 'Marie Dupont',
        role: 'Directrice, MECS Les Jardins',
        avatar: '/images/avatars/marie.jpg',
        rating: 5,
    },
    {
        id: '2',
        text: 'Professionnel, patient et toujours de bonne humeur. Les enfants l\'adorent !',
        author: 'Philippe Martin',
        role: 'Éducateur Chef, IME Horizon',
        avatar: '/images/avatars/philippe.jpg',
        rating: 5,
    },
];

const userName = 'Thomas';
const userPhilosophy = 'Chaque accompagnement est une rencontre unique. Je crois en la force du lien humain pour permettre à chacun de révéler son potentiel.';

// =============================================================================
// SUB-COMPONENTS — Behance Portfolio Style (Light Mode)
// =============================================================================

// Profile Hero Card (Instagram-style)
function ProfileHeroCard({ stats }: { stats: PortfolioStats }) {
    return (
        <motion.div
            variants={itemVariants}
            className="relative overflow-hidden bg-gradient-to-br from-teal-500 via-teal-600 to-emerald-600 rounded-3xl p-6 text-white"
        >
            {/* Background Pattern */}
            <div className="absolute inset-0 opacity-10">
                <div className="absolute top-0 right-0 w-64 h-64 bg-white rounded-full blur-3xl transform translate-x-1/2 -translate-y-1/2" />
                <div className="absolute bottom-0 left-0 w-48 h-48 bg-white rounded-full blur-3xl transform -translate-x-1/2 translate-y-1/2" />
            </div>

            <div className="relative flex flex-col md:flex-row items-center gap-6">
                {/* Avatar */}
                <div className="relative">
                    <div className="w-24 h-24 rounded-full bg-white/20 backdrop-blur-sm border-4 border-white/30 flex items-center justify-center text-4xl font-bold">
                        T
                    </div>
                    <div className="absolute -bottom-1 -right-1 w-8 h-8 bg-emerald-400 rounded-full flex items-center justify-center border-3 border-white">
                        <Shield className="w-4 h-4 text-white" />
                    </div>
                </div>

                {/* Info */}
                <div className="flex-1 text-center md:text-left">
                    <div className="flex items-center justify-center md:justify-start gap-2 mb-1">
                        <h1 className="text-2xl font-bold">{userName}</h1>
                        <span className="px-2 py-0.5 bg-white/20 rounded-full text-xs font-medium">Profil Vérifié ✓</span>
                    </div>
                    <p className="text-teal-100 text-sm">Éducateur Spécialisé • DEES</p>
                    <div className="flex items-center justify-center md:justify-start gap-1 mt-2">
                        {[...Array(5)].map((_, i) => (
                            <Star key={i} className="w-4 h-4 fill-amber-300 text-amber-300" />
                        ))}
                        <span className="ml-1 text-sm font-medium">{stats.avgRating}</span>
                        <span className="text-teal-200 text-sm">• {stats.endorsements} recommandations</span>
                    </div>
                </div>

                {/* Quick Actions */}
                <div className="flex gap-2">
                    <Link
                        href="/dashboard/talent/profile/edit"
                        className="p-3 bg-white/20 hover:bg-white/30 rounded-xl transition-colors backdrop-blur-sm"
                    >
                        <Edit3 className="w-5 h-5" />
                    </Link>
                    <button className="p-3 bg-white/20 hover:bg-white/30 rounded-xl transition-colors backdrop-blur-sm" title="Partager mon profil" aria-label="Partager mon profil">
                        <Share2 className="w-5 h-5" />
                    </button>
                </div>
            </div>

            {/* Stats Row */}
            <div className="relative grid grid-cols-4 gap-4 mt-6 pt-6 border-t border-white/20">
                <div className="text-center">
                    <p className="text-2xl font-bold">{stats.missionsCompleted}</p>
                    <p className="text-teal-200 text-xs">{getTerm('missionPlural')}</p>
                </div>
                <div className="text-center">
                    <p className="text-2xl font-bold">{stats.hoursWorked}h</p>
                    <p className="text-teal-200 text-xs">d'intervention</p>
                </div>
                <div className="text-center">
                    <p className="text-2xl font-bold">{stats.familiesHelped}</p>
                    <p className="text-teal-200 text-xs">familles aidées</p>
                </div>
                <div className="text-center">
                    <p className="text-2xl font-bold">{stats.endorsements}</p>
                    <p className="text-teal-200 text-xs">👏 endorsements</p>
                </div>
            </div>
        </motion.div>
    );
}

// Philosophy Quote Block
function PhilosophyBlock({ quote }: { quote: string }) {
    return (
        <motion.div
            variants={itemVariants}
            className="relative p-6 bg-gradient-to-br from-slate-50 to-teal-50 rounded-2xl border border-teal-100"
        >
            <Quote className="absolute top-4 left-4 w-8 h-8 text-teal-200" />
            <p className="text-slate-700 italic pl-10 pr-4 leading-relaxed">{quote}</p>
            <div className="mt-4 flex items-center justify-end gap-2">
                <Lightbulb className="w-4 h-4 text-amber-500" />
                <span className="text-xs text-slate-500">Ma philosophie d'accompagnement</span>
            </div>
        </motion.div>
    );
}

// Savoir-Être Badges (voted by clients)
function SavoirEtreBadges({ items }: { items: SavoirEtre[] }) {
    return (
        <motion.div variants={itemVariants} className="space-y-3">
            <div className="flex items-center justify-between">
                <h3 className="font-bold text-slate-900 flex items-center gap-2">
                    <Heart className="w-5 h-5 text-rose-500" />
                    Savoir-être reconnus
                </h3>
                <span className="text-xs text-slate-500">Votés par les établissements</span>
            </div>
            <div className="flex flex-wrap gap-2">
                {items.map((item) => (
                    <motion.span
                        key={item.id}
                        whileHover={{ scale: 1.05 }}
                        className="inline-flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 rounded-full shadow-sm hover:shadow-md hover:border-teal-300 transition-all cursor-default"
                    >
                        <span className="text-lg">{item.emoji}</span>
                        <span className="font-medium text-slate-700">{item.trait}</span>
                        <span className="text-xs text-teal-600 font-semibold bg-teal-50 px-2 py-0.5 rounded-full">+{item.votedBy}</span>
                    </motion.span>
                ))}
            </div>
        </motion.div>
    );
}

// Skills Portfolio Grid
function SkillsGrid({ skills }: { skills: PortfolioSkill[] }) {
    const levelConfig = {
        junior: { label: 'Junior', width: '33%', color: 'bg-slate-300' },
        confirmé: { label: 'Confirmé', width: '66%', color: 'bg-teal-400' },
        expert: { label: 'Expert', width: '100%', color: 'bg-emerald-500' },
    };

    return (
        <motion.div variants={itemVariants} className="space-y-4">
            <div className="flex items-center justify-between">
                <h3 className="font-bold text-slate-900 flex items-center gap-2">
                    <Briefcase className="w-5 h-5 text-teal-600" />
                    Compétences clés
                </h3>
                <Link href="/dashboard/talent/profile" className="text-xs font-medium text-teal-600 hover:text-teal-700 flex items-center gap-1">
                    Modifier <Edit3 className="w-3 h-3" />
                </Link>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {skills.map((skill) => (
                    <motion.div
                        key={skill.id}
                        whileHover={{ y: -2 }}
                        className="p-4 bg-white border border-slate-200 rounded-xl hover:shadow-md transition-all"
                    >
                        <div className="flex items-center gap-3 mb-3">
                            <div className={cn(
                                'p-2 rounded-lg',
                                skill.color === 'teal' && 'bg-teal-100',
                                skill.color === 'violet' && 'bg-violet-100',
                                skill.color === 'rose' && 'bg-rose-100',
                                skill.color === 'blue' && 'bg-blue-100',
                            )}>
                                <skill.icon className={cn(
                                    'w-5 h-5',
                                    skill.color === 'teal' && 'text-teal-600',
                                    skill.color === 'violet' && 'text-violet-600',
                                    skill.color === 'rose' && 'text-rose-600',
                                    skill.color === 'blue' && 'text-blue-600',
                                )} />
                            </div>
                            <div className="flex-1">
                                <p className="font-semibold text-slate-900">{skill.name}</p>
                                <p className="text-xs text-slate-500">{levelConfig[skill.level].label} • {skill.endorsements} endorsements</p>
                            </div>
                        </div>
                        <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                            <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: levelConfig[skill.level].width }}
                                transition={{ duration: 0.8, ease: 'easeOut' }}
                                className={cn('h-full rounded-full', levelConfig[skill.level].color)}
                            />
                        </div>
                    </motion.div>
                ))}
            </div>
        </motion.div>
    );
}

// Meaningful Mission Card (Instagram story-like)
function MissionCard({ mission }: { mission: MeaningfulMission }) {
    const urgencyConfig = {
        urgent: { label: 'Urgent', bg: 'bg-rose-100', text: 'text-rose-700', border: 'border-rose-300' },
        soon: { label: 'Cette semaine', bg: 'bg-amber-100', text: 'text-amber-700', border: 'border-amber-300' },
        normal: { label: 'Disponible', bg: 'bg-slate-100', text: 'text-slate-600', border: 'border-slate-200' },
    };

    const config = urgencyConfig[mission.urgency];

    return (
        <motion.div
            variants={cardHover}
            initial="rest"
            whileHover="hover"
        >
            <Link
                href={`/dashboard/talent/missions/${mission.id}`}
                className={cn(
                    'block p-5 bg-white border-2 rounded-2xl transition-all hover:shadow-lg',
                    config.border
                )}
            >
                {/* Header with Match Score */}
                <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-teal-100 to-teal-200 flex items-center justify-center text-teal-600 font-bold">
                            {mission.establishment.charAt(0)}
                        </div>
                        <div>
                            <p className="font-bold text-slate-900">{mission.establishment}</p>
                            <p className="text-xs text-slate-500 flex items-center gap-1">
                                <MapPin className="w-3 h-3" /> {mission.distance}
                            </p>
                        </div>
                    </div>
                    <div className="text-right">
                        <div className={cn('inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-semibold', config.bg, config.text)}>
                            {mission.urgency === 'urgent' && <Siren className="w-3 h-3" />}
                            {config.label}
                        </div>
                        <div className="mt-1 flex items-center justify-end gap-1">
                            <span className="text-xs text-slate-400">Match</span>
                            <span className={cn(
                                'text-sm font-bold',
                                mission.matchScore >= 90 ? 'text-emerald-600' : mission.matchScore >= 80 ? 'text-teal-600' : 'text-slate-600'
                            )}>
                                {mission.matchScore}%
                            </span>
                        </div>
                    </div>
                </div>

                {/* Mission Details */}
                <h3 className="font-bold text-lg text-slate-900 mb-2">{mission.title}</h3>
                <p className="text-sm text-slate-600 mb-3 line-clamp-2">{mission.description}</p>

                {/* Impact Badge */}
                <div className="flex items-center gap-2 mb-3 p-2 bg-emerald-50 rounded-lg">
                    <Heart className="w-4 h-4 text-emerald-600" />
                    <span className="text-sm font-medium text-emerald-700">{mission.impact}</span>
                </div>

                {/* Footer */}
                <div className="flex items-center justify-between pt-3 border-t border-slate-100">
                    <div className="flex items-center gap-2 text-sm text-slate-500">
                        <Clock className="w-4 h-4" />
                        {mission.duration}
                    </div>
                    <div className="flex gap-1">
                        {mission.values.map((value, i) => (
                            <span key={i} className="px-2 py-1 bg-teal-50 text-teal-700 text-xs rounded-full">
                                {value}
                            </span>
                        ))}
                    </div>
                </div>
            </Link>
        </motion.div>
    );
}

// Testimonial Carousel Card
function TestimonialCard({ testimonial }: { testimonial: TestimonialItem }) {
    return (
        <motion.div
            whileHover={{ y: -4 }}
            className="min-w-[300px] p-5 bg-white border border-slate-200 rounded-2xl shadow-sm"
        >
            <div className="flex items-center gap-1 mb-3">
                {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-4 h-4 fill-amber-400 text-amber-400" />
                ))}
            </div>
            <p className="text-slate-700 text-sm italic mb-4">"{testimonial.text}"</p>
            <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-teal-400 to-teal-600 flex items-center justify-center text-white font-bold text-sm">
                    {testimonial.author.charAt(0)}
                </div>
                <div>
                    <p className="font-semibold text-slate-900 text-sm">{testimonial.author}</p>
                    <p className="text-xs text-slate-500">{testimonial.role}</p>
                </div>
            </div>
        </motion.div>
    );
}

// Availability Toggle (Light theme)
function AvailabilityToggle({ isOn, onToggle }: { isOn: boolean; onToggle: () => void }) {
    return (
        <motion.button
            onClick={onToggle}
            whileTap={{ scale: 0.98 }}
            className={cn(
                'relative flex items-center gap-3 px-5 py-3 rounded-2xl transition-all duration-300 shadow-md',
                isOn
                    ? 'bg-gradient-to-r from-emerald-500 to-teal-500 text-white shadow-emerald-200'
                    : 'bg-white border border-slate-200 text-slate-600 shadow-slate-100'
            )}
        >
            {isOn && (
                <span className="absolute -top-1 -right-1 flex h-4 w-4">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                    <span className="relative inline-flex rounded-full h-4 w-4 bg-emerald-300" />
                </span>
            )}

            <Siren size={20} className={isOn ? 'text-white' : 'text-slate-400'} />
            
            <div className="flex flex-col items-start">
                <span className="text-xs font-medium opacity-80">
                    {isOn ? 'DISPONIBLE' : 'INDISPONIBLE'}
                </span>
                <span className="font-bold text-sm">
                    {isOn ? 'Je peux intervenir' : 'Mode repos'}
                </span>
            </div>

            <div className={cn(
                'w-11 h-6 rounded-full relative transition-colors ml-2',
                isOn ? 'bg-emerald-700' : 'bg-slate-300'
            )}>
                <span className={cn(
                    'absolute top-1 w-4 h-4 rounded-full bg-white shadow transition-all duration-300',
                    isOn ? 'left-6' : 'left-1'
                )} />
            </div>
        </motion.button>
    );
}

// Wallet (Light theme)
function WalletCard({ balance }: { balance: number }) {
    return (
        <Link
            href="/dashboard/talent/admin"
            className="flex items-center gap-3 px-4 py-3 bg-white border border-slate-200 rounded-xl hover:border-teal-300 hover:shadow-md transition-all group"
        >
            <div className="p-2 bg-gradient-to-br from-amber-100 to-amber-50 rounded-lg">
                <Wallet size={18} className="text-amber-600" />
            </div>
            <div>
                <p className="text-xs text-slate-500">Solde</p>
                <p className="font-bold text-slate-900">
                    {balance.toLocaleString('fr-FR', { style: 'currency', currency: 'EUR' })}
                </p>
            </div>
            <ChevronRight size={14} className="text-slate-400 group-hover:translate-x-1 transition-transform" />
        </Link>
    );
}

// =============================================================================
// MAIN COMPONENT — Behance Portfolio Dashboard (Light Mode)
// =============================================================================

export function SocialTalentDashboard({ user }: SocialTalentDashboardProps) {
    const [isAvailable, setIsAvailable] = useState(false);
    const walletBalance = 1247.50;

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-teal-50 dark:from-slate-950 dark:via-slate-900 dark:to-teal-950/30 transition-colors">
            {/* Top Header */}
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="sticky top-0 z-40 bg-white/80 backdrop-blur-xl border-b border-slate-200"
            >
                <div className="px-4 py-3 flex items-center justify-between max-w-4xl mx-auto">
                    <div>
                        <p className="text-slate-500 text-xs">Bienvenue 👋</p>
                        <h1 className="text-lg font-bold text-slate-900">{user?.name || userName}</h1>
                    </div>
                    <div className="flex items-center gap-3">
                        <AvailabilityToggle isOn={isAvailable} onToggle={() => setIsAvailable(!isAvailable)} />
                        <WalletCard balance={walletBalance} />
                    </div>
                </div>
            </motion.div>

            <motion.div
                variants={containerVariants}
                initial="hidden"
                animate="visible"
                className="p-4 space-y-6 max-w-4xl mx-auto pb-8"
            >
                {/* Profile Completion Alert */}
                <DashboardAlert 
                    ctaLink="/dashboard/talent/profile"
                    ctaText="Compléter mon portfolio"
                />

                {/* Profile Hero Card */}
                <ProfileHeroCard stats={mockStats} />

                {/* Philosophy Quote */}
                <PhilosophyBlock quote={userPhilosophy} />

                {/* Savoir-Être Badges */}
                <SavoirEtreBadges items={mockSavoirEtre} />

                {/* Skills Portfolio */}
                <SkillsGrid skills={mockPortfolioSkills} />

                {/* Meaningful Missions Section */}
                <motion.div variants={itemVariants} className="space-y-4">
                    <div className="flex items-center justify-between">
                        <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                            <Heart className="w-5 h-5 text-rose-500" />
                            {getTerm('missionPlural')} qui vous correspondent
                        </h2>
                        <Link href="/dashboard/talent/missions" className="text-sm font-medium text-teal-600 hover:text-teal-700 flex items-center gap-1">
                            Voir tout <ArrowRight className="w-4 h-4" />
                        </Link>
                    </div>

                    {isAvailable ? (
                        <div className="space-y-4">
                            {mockMissions.map((mission) => (
                                <MissionCard key={mission.id} mission={mission} />
                            ))}
                        </div>
                    ) : (
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                        >
                            <Card className="border-2 border-dashed border-teal-200 bg-teal-50/50">
                                <CardContent className="p-8 flex flex-col items-center text-center">
                                    <div className="p-4 bg-teal-100 rounded-2xl mb-4">
                                        <Siren size={32} className="text-teal-500" />
                                    </div>
                                    <h3 className="font-bold text-slate-700">Activez votre disponibilité</h3>
                                    <p className="text-sm text-slate-500 mt-1 mb-4 max-w-md">
                                        Rendez-vous visible auprès des établissements qui recherchent des profils comme le vôtre
                                    </p>
                                    <button
                                        onClick={() => setIsAvailable(true)}
                                        className="px-6 py-3 bg-gradient-to-r from-teal-500 to-emerald-500 text-white font-semibold rounded-xl hover:from-teal-600 hover:to-emerald-600 transition-all shadow-lg shadow-teal-200"
                                    >
                                        Je suis disponible
                                    </button>
                                </CardContent>
                            </Card>
                        </motion.div>
                    )}
                </motion.div>

                {/* Testimonials */}
                {mockTestimonials.length > 0 && (
                    <motion.div variants={itemVariants} className="space-y-4">
                        <h3 className="font-bold text-slate-900 flex items-center gap-2">
                            <MessageCircle className="w-5 h-5 text-teal-600" />
                            Ce qu'ils disent de vous
                        </h3>
                        <div className="flex gap-4 overflow-x-auto pb-2 -mx-4 px-4 scrollbar-hide">
                            {mockTestimonials.map((testimonial) => (
                                <TestimonialCard key={testimonial.id} testimonial={testimonial} />
                            ))}
                        </div>
                    </motion.div>
                )}

                {/* Quick Access */}
                <motion.div variants={itemVariants} className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <Link
                        href="/dashboard/talent/missions"
                        className="flex items-center gap-3 p-4 bg-white border border-slate-200 rounded-xl hover:border-rose-300 hover:shadow-md transition-all group"
                    >
                        <div className="p-2 bg-rose-100 rounded-xl">
                            <Siren size={20} className="text-rose-600" />
                        </div>
                        <div className="flex-1">
                            <p className="font-semibold text-slate-900">{getTerm('missionPlural')}</p>
                            <p className="text-xs text-slate-500">Voir les opportunités</p>
                        </div>
                        <ArrowRight size={16} className="text-slate-400 group-hover:translate-x-1 group-hover:text-rose-500 transition-all" />
                    </Link>

                    {isFeatureEnabled('enableWorkshops') && (
                        <Link
                            href="/dashboard/talent/services/new"
                            className="flex items-center gap-3 p-4 bg-white border border-slate-200 rounded-xl hover:border-teal-300 hover:shadow-md transition-all group"
                        >
                            <div className="p-2 bg-teal-100 rounded-xl">
                                <Sparkles size={20} className="text-teal-600" />
                            </div>
                            <div className="flex-1">
                                <p className="font-semibold text-slate-900">Créer un atelier</p>
                                <p className="text-xs text-slate-500">SocioLive</p>
                            </div>
                            <ArrowRight size={16} className="text-slate-400 group-hover:translate-x-1 group-hover:text-teal-500 transition-all" />
                        </Link>
                    )}

                    <Link
                        href="/dashboard/talent/planning"
                        className="flex items-center gap-3 p-4 bg-white border border-slate-200 rounded-xl hover:border-violet-300 hover:shadow-md transition-all group"
                    >
                        <div className="p-2 bg-violet-100 rounded-xl">
                            <Calendar size={20} className="text-violet-600" />
                        </div>
                        <div className="flex-1">
                            <p className="font-semibold text-slate-900">Mon Planning</p>
                            <p className="text-xs text-slate-500">{getTerm('availability')}</p>
                        </div>
                        <ArrowRight size={16} className="text-slate-400 group-hover:translate-x-1 group-hover:text-violet-500 transition-all" />
                    </Link>
                </motion.div>
            </motion.div>
        </div>
    );
}

export default SocialTalentDashboard;
