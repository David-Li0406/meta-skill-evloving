'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import {
    Siren,
    Calendar,
    AlertTriangle,
    ChevronRight,
    Clock,
    FileSignature,
    Users,
    Sparkles,
    FolderKanban,
    ArrowRight,
    Heart,
    Star,
    CheckCircle2,
    MessageCircle,
    TrendingUp,
    Shield,
    Eye,
    Award,
    Wallet,
} from 'lucide-react';
import { ActionCard, Badge } from '@/components/ui';
import { ObjectiveWizard } from '@/components/publish';
import { DashboardAlert } from '@/components/dashboard';
import { getTerm, isFeatureEnabled } from '@/lib/domain-config';
import { cn } from '@/lib/utils';
import type { DashboardUser } from '../DashboardResolver';

// =============================================================================
// TYPES — Instagram/Portfolio Style
// =============================================================================

interface SocialClientDashboardProps {
    user?: DashboardUser;
}

interface TalentSpotlight {
    id: string;
    name: string;
    role: string;
    avatar: string;
    rating: number;
    savoirEtre: string[];
    available: boolean;
    favorited: boolean;
    verified: boolean;
    lastMission?: string;
}

interface ProjectCard {
    id: string;
    name: string;
    type: 'mission' | 'workshop';
    status: 'active' | 'upcoming' | 'completed';
    cover?: string;
    talentAvatars: string[];
    nextDate?: string;
    progress?: number;
    description: string;
}

interface TeamStability {
    score: number;
    trend: 'up' | 'down' | 'stable';
    returnRate: number;
    avgRating: number;
}

// =============================================================================
// ANIMATION VARIANTS — Soft & Friendly
// =============================================================================

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: { staggerChildren: 0.1 }
    }
} as const;

const itemVariants = {
    hidden: { opacity: 0, y: 14 },
    visible: { 
        opacity: 1, 
        y: 0,
        transition: { type: 'spring' as const, stiffness: 100, damping: 15 }
    }
} as const;

const cardHover = {
    rest: { scale: 1, y: 0 },
    hover: { scale: 1.02, y: -4, transition: { duration: 0.25 } }
} as const;

// =============================================================================
// MOCK DATA — Human-Centered, Story-Driven
// =============================================================================

const mockTalentSpotlights: TalentSpotlight[] = [
    {
        id: '1',
        name: 'Marie Lambert',
        role: 'Éducatrice Spécialisée',
        avatar: '/images/avatars/avatar-1.jpg',
        rating: 4.9,
        savoirEtre: ['Patiente', 'Créative', 'Bienveillante'],
        available: true,
        favorited: true,
        verified: true,
        lastMission: 'Il y a 3 jours',
    },
    {
        id: '2',
        name: 'Thomas Durand',
        role: 'Moniteur-Éducateur',
        avatar: '/images/avatars/avatar-2.jpg',
        rating: 4.7,
        savoirEtre: ['Dynamique', 'Sport', 'Autonome'],
        available: true,
        favorited: false,
        verified: true,
    },
    {
        id: '3',
        name: 'Sophie Martin',
        role: 'Animatrice Socio-culturelle',
        avatar: '/images/avatars/avatar-3.jpg',
        rating: 5.0,
        savoirEtre: ['Artistique', 'Empathique', 'Innovante'],
        available: false,
        favorited: true,
        verified: false,
        lastMission: 'En mission actuellement',
    },
];

const mockProjects: ProjectCard[] = [
    {
        id: '1',
        name: 'Renfort Éducatif - Groupe Ados',
        type: 'mission',
        status: 'active',
        cover: '/images/projects/education.jpg',
        talentAvatars: ['/images/avatars/avatar-1.jpg', '/images/avatars/avatar-2.jpg'],
        nextDate: 'Aujourd\'hui 14h00',
        progress: 65,
        description: 'Accompagnement du groupe adolescents 12-16 ans',
    },
    {
        id: '2',
        name: 'Atelier Gestion du Stress',
        type: 'workshop',
        status: 'upcoming',
        cover: '/images/projects/workshop.jpg',
        talentAvatars: ['/images/avatars/avatar-3.jpg'],
        nextDate: 'Vendredi 10h00',
        description: 'Formation relaxation pour les résidents',
    },
    {
        id: '3',
        name: 'Accompagnement Vacances Été',
        type: 'mission',
        status: 'active',
        talentAvatars: ['/images/avatars/avatar-1.jpg', '/images/avatars/avatar-2.jpg', '/images/avatars/avatar-3.jpg'],
        progress: 40,
        description: 'Séjour adapté montagne - 3 semaines',
    },
];

const mockTeamStability: TeamStability = {
    score: 87,
    trend: 'up',
    returnRate: 78,
    avgRating: 4.8,
};

// =============================================================================
// SUB-COMPONENTS — Human-Centered, Warm UI
// =============================================================================

/** Talent spotlight card - Instagram profile style */
function TalentCard({ talent, onFavorite }: { talent: TalentSpotlight; onFavorite?: () => void }) {
    return (
        <motion.div
            variants={cardHover}
            initial="rest"
            whileHover="hover"
            className="relative bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm hover:shadow-xl transition-shadow"
        >
            {/* Availability indicator */}
            {talent.available && (
                <div className="absolute top-3 right-3 z-10 flex items-center gap-1 px-2 py-1 bg-emerald-500 text-white text-[10px] font-bold rounded-full shadow-lg">
                    <span className="w-1.5 h-1.5 bg-white rounded-full animate-pulse" />
                    Disponible
                </div>
            )}
            
            {/* Avatar & Identity */}
            <div className="p-5 text-center">
                <div className="relative w-20 h-20 mx-auto mb-3">
                    <div className="w-full h-full rounded-full bg-gradient-to-br from-primary-400 to-secondary-500 p-0.5">
                        <div className="w-full h-full rounded-full bg-white p-0.5">
                            <div className="w-full h-full rounded-full bg-gradient-to-br from-slate-200 to-slate-300 flex items-center justify-center text-2xl font-bold text-slate-600">
                                {talent.name.split(' ').map(n => n[0]).join('')}
                            </div>
                        </div>
                    </div>
                    {talent.verified && (
                        <div className="absolute -bottom-1 -right-1 bg-white rounded-full p-0.5">
                            <Shield className="w-5 h-5 text-blue-500 fill-blue-100" />
                        </div>
                    )}
                </div>
                
                <h3 className="font-bold text-slate-900">{talent.name}</h3>
                <p className="text-sm text-slate-500">{talent.role}</p>
                
                {/* Rating */}
                <div className="flex items-center justify-center gap-1 mt-2">
                    <Star className="w-4 h-4 text-amber-400 fill-amber-400" />
                    <span className="font-semibold text-slate-900">{talent.rating}</span>
                </div>
            </div>
            
            {/* Savoir-être tags */}
            <div className="px-4 pb-4">
                <div className="flex flex-wrap justify-center gap-1.5">
                    {talent.savoirEtre.map((trait) => (
                        <span 
                            key={trait}
                            className="px-2 py-0.5 bg-gradient-to-r from-primary-50 to-secondary-50 text-primary-700 text-[11px] font-medium rounded-full border border-primary-100"
                        >
                            {trait}
                        </span>
                    ))}
                </div>
            </div>
            
            {/* Action bar */}
            <div className="flex border-t border-slate-100">
                <button 
                    onClick={onFavorite}
                    className="flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium text-slate-600 hover:bg-slate-50 transition-colors"
                >
                    <Heart className={cn('w-4 h-4', talent.favorited && 'fill-rose-500 text-rose-500')} />
                    {talent.favorited ? 'Favori' : 'Ajouter'}
                </button>
                <div className="w-px bg-slate-100" />
                <Link 
                    href={`/talent/${talent.id}`}
                    className="flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium text-primary-600 hover:bg-primary-50 transition-colors"
                >
                    <Eye className="w-4 h-4" />
                    Voir profil
                </Link>
            </div>
        </motion.div>
    );
}

/** Project card with visual storytelling */
function ProjectCardComponent({ project }: { project: ProjectCard }) {
    const statusConfig = {
        active: { label: 'En cours', color: 'bg-emerald-100 text-emerald-700', dot: 'bg-emerald-500' },
        upcoming: { label: 'À venir', color: 'bg-blue-100 text-blue-700', dot: 'bg-blue-500' },
        completed: { label: 'Terminé', color: 'bg-slate-100 text-slate-600', dot: 'bg-slate-400' },
    };
    
    const typeConfig = {
        mission: { icon: Siren, gradient: 'from-rose-500 to-orange-500' },
        workshop: { icon: Sparkles, gradient: 'from-teal-500 to-emerald-500' },
    };

    return (
        <motion.div
            variants={cardHover}
            initial="rest"
            whileHover="hover"
        >
            <Link
                href={`/dashboard/client/projects/${project.id}`}
                className="block bg-white border border-slate-200 rounded-2xl overflow-hidden hover:shadow-xl transition-all"
            >
                {/* Cover / Pattern */}
                <div className={cn(
                    'h-24 bg-gradient-to-br relative overflow-hidden',
                    typeConfig[project.type].gradient
                )}>
                    {/* Decorative pattern */}
                    <div className="absolute inset-0 opacity-20">
                        <div className="absolute top-0 right-0 w-32 h-32 bg-white/20 rounded-full -translate-y-1/2 translate-x-1/2" />
                        <div className="absolute bottom-0 left-0 w-24 h-24 bg-white/10 rounded-full translate-y-1/2 -translate-x-1/2" />
                    </div>
                    
                    {/* Type icon */}
                    <div className="absolute top-3 left-3 p-2 bg-white/20 backdrop-blur-sm rounded-xl">
                        {project.type === 'mission' ? (
                            <Siren className="w-5 h-5 text-white" />
                        ) : (
                            <Sparkles className="w-5 h-5 text-white" />
                        )}
                    </div>
                    
                    {/* Status badge */}
                    <div className="absolute top-3 right-3">
                        <Badge className={statusConfig[project.status].color}>
                            <span className={cn('w-1.5 h-1.5 rounded-full mr-1.5', statusConfig[project.status].dot)} />
                            {statusConfig[project.status].label}
                        </Badge>
                    </div>
                    
                    {/* Talent avatars stack */}
                    <div className="absolute bottom-3 right-3 flex -space-x-2">
                        {project.talentAvatars.slice(0, 3).map((_, i) => (
                            <div 
                                key={i}
                                className="w-8 h-8 rounded-full border-2 border-white bg-slate-200 flex items-center justify-center text-xs font-bold text-slate-600"
                            >
                                {String.fromCharCode(65 + i)}
                            </div>
                        ))}
                        {project.talentAvatars.length > 3 && (
                            <div className="w-8 h-8 rounded-full border-2 border-white bg-slate-800 text-white flex items-center justify-center text-[10px] font-bold">
                                +{project.talentAvatars.length - 3}
                            </div>
                        )}
                    </div>
                </div>
                
                {/* Content */}
                <div className="p-4">
                    <h3 className="font-bold text-slate-900 mb-1">{project.name}</h3>
                    <p className="text-sm text-slate-500 line-clamp-2 mb-3">{project.description}</p>
                    
                    {/* Meta */}
                    <div className="flex items-center justify-between">
                        {project.nextDate && (
                            <span className="flex items-center gap-1.5 text-xs text-slate-500">
                                <Clock size={12} />
                                {project.nextDate}
                            </span>
                        )}
                        
                        {project.progress !== undefined && (
                            <div className="flex items-center gap-2">
                                <div className="w-16 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                                    <div 
                                        className="h-full bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full"
                                        style={{ width: `${project.progress}%` }}
                                    />
                                </div>
                                <span className="text-xs font-semibold text-slate-600">{project.progress}%</span>
                            </div>
                        )}
                    </div>
                </div>
            </Link>
        </motion.div>
    );
}

/** Team stability widget - "Wellness gauge" */
function TeamStabilityWidget({ data }: { data: TeamStability }) {
    return (
        <div className="bg-gradient-to-br from-primary-50 via-white to-secondary-50 rounded-2xl border border-primary-100 p-5">
            <div className="flex items-center justify-between mb-4">
                <h3 className="font-bold text-slate-900 flex items-center gap-2">
                    <Award className="w-5 h-5 text-primary-600" />
                    Stabilité Équipe
                </h3>
                <div className={cn(
                    'flex items-center gap-1 text-sm font-semibold',
                    data.trend === 'up' ? 'text-emerald-600' : data.trend === 'down' ? 'text-rose-600' : 'text-slate-600'
                )}>
                    <TrendingUp className={cn('w-4 h-4', data.trend === 'down' && 'rotate-180')} />
                    {data.trend === 'up' ? '+5%' : data.trend === 'down' ? '-3%' : '0%'}
                </div>
            </div>
            
            {/* Big score */}
            <div className="text-center mb-4">
                <div className="relative w-24 h-24 mx-auto">
                    <svg className="w-full h-full -rotate-90" viewBox="0 0 36 36">
                        <path
                            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            fill="none"
                            stroke="#e2e8f0"
                            strokeWidth="3"
                        />
                        <path
                            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            fill="none"
                            stroke="url(#gradient)"
                            strokeWidth="3"
                            strokeDasharray={`${data.score}, 100`}
                            strokeLinecap="round"
                        />
                        <defs>
                            <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stopColor="#14b8a6" />
                                <stop offset="100%" stopColor="#6366f1" />
                            </linearGradient>
                        </defs>
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                        <span className="text-2xl font-bold text-slate-900">{data.score}%</span>
                    </div>
                </div>
            </div>
            
            {/* Mini stats */}
            <div className="grid grid-cols-2 gap-3">
                <div className="text-center p-2 bg-white rounded-xl">
                    <p className="text-lg font-bold text-slate-900">{data.returnRate}%</p>
                    <p className="text-[10px] text-slate-500">Taux de retour</p>
                </div>
                <div className="text-center p-2 bg-white rounded-xl">
                    <div className="flex items-center justify-center gap-1">
                        <Star className="w-4 h-4 text-amber-400 fill-amber-400" />
                        <span className="text-lg font-bold text-slate-900">{data.avgRating}</span>
                    </div>
                    <p className="text-[10px] text-slate-500">Note moyenne</p>
                </div>
            </div>
        </div>
    );
}

/** Quick stat card */
function StatCard({ label, value, icon: Icon, color }: {
    label: string;
    value: number | string;
    icon: React.ElementType;
    color: 'rose' | 'purple' | 'teal' | 'amber';
}) {
    const colorClasses = {
        rose: 'bg-rose-50 text-rose-600 border-rose-100',
        purple: 'bg-purple-50 text-purple-600 border-purple-100',
        teal: 'bg-teal-50 text-teal-600 border-teal-100',
        amber: 'bg-amber-50 text-amber-600 border-amber-100',
    };

    return (
        <div className="rounded-2xl border bg-white p-4 shadow-sm hover:shadow-md transition-shadow">
            <div className={cn('mb-2 inline-flex rounded-xl p-2 border', colorClasses[color])}>
                <Icon className="h-5 w-5" />
            </div>
            <p className="text-2xl font-bold text-slate-900">{value}</p>
            <p className="text-sm text-slate-500">{label}</p>
        </div>
    );
}

// =============================================================================
// MAIN COMPONENT — Instagram-Style Light Dashboard
// =============================================================================

export function SocialClientDashboard({ user }: SocialClientDashboardProps) {
    const [favorited, setFavorited] = useState<Record<string, boolean>>({});
    const contractsToSign = 2;
    const walletBalance = 1250;
    
    const toggleFavorite = (id: string) => {
        setFavorited(prev => ({ ...prev, [id]: !prev[id] }));
    };
    
    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-primary-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-primary-950/30 transition-colors">
            <motion.div
                variants={containerVariants}
                initial="hidden"
                animate="visible"
                className="p-4 lg:p-6 space-y-6 max-w-7xl mx-auto"
            >
                {/* Profile Completion Alert */}
                <DashboardAlert 
                    ctaLink="/dashboard/client/settings"
                    ctaText="Compléter maintenant"
                />

                {/* Zone A: Objective Wizard */}
                <motion.div variants={itemVariants}>
                    <ObjectiveWizard userName={user?.name || 'Jean'} />
                </motion.div>

                {/* Zone B: Compliance Widget */}
                {contractsToSign > 0 && (
                    <motion.div
                        variants={itemVariants}
                        className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 rounded-2xl border-2 border-amber-200 bg-gradient-to-r from-amber-50 to-orange-50 p-4"
                    >
                        <div className="flex items-center gap-3">
                            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-amber-100">
                                <AlertTriangle className="h-6 w-6 text-amber-600" />
                            </div>
                            <div>
                                <p className="font-bold text-amber-800">
                                    {contractsToSign} Contrat{contractsToSign > 1 ? 's' : ''} en attente
                                </p>
                                <p className="text-sm text-amber-600">
                                    Action requise avant démarrage des missions
                                </p>
                            </div>
                        </div>
                        <Link
                            href="/dashboard/client/admin"
                            className="inline-flex items-center justify-center gap-2 rounded-xl bg-amber-500 px-5 py-2.5 text-sm font-bold text-white shadow-lg shadow-amber-200 transition-all hover:bg-amber-600 hover:shadow-xl"
                        >
                            <FileSignature className="h-4 w-4" />
                            Signer maintenant
                        </Link>
                    </motion.div>
                )}

                {/* Talent Spotlights - Instagram Stories style */}
                <motion.div variants={itemVariants}>
                    <div className="flex items-center justify-between mb-4">
                        <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                            <Heart className="h-5 w-5 text-rose-500" />
                            Intervenants Favoris
                        </h2>
                        <Link
                            href="/search?type=talent"
                            className="text-sm font-medium text-primary-600 hover:text-primary-700 flex items-center gap-1"
                        >
                            Découvrir <ArrowRight size={14} />
                        </Link>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                        {mockTalentSpotlights.map((talent) => (
                            <TalentCard 
                                key={talent.id} 
                                talent={{ ...talent, favorited: favorited[talent.id] ?? talent.favorited }}
                                onFavorite={() => toggleFavorite(talent.id)}
                            />
                        ))}
                    </div>
                </motion.div>

                {/* Projects Section */}
                {isFeatureEnabled('enableProjects') && (
                    <motion.div variants={itemVariants}>
                        <div className="flex items-center justify-between mb-4">
                            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                                <FolderKanban className="h-5 w-5 text-primary-600" />
                                Mes Projets
                            </h2>
                            <Link
                                href="/dashboard/client/projects"
                                className="text-sm font-medium text-primary-600 hover:text-primary-700 flex items-center gap-1"
                            >
                                Voir tout <ArrowRight size={14} />
                            </Link>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {mockProjects.map((project) => (
                                <ProjectCardComponent key={project.id} project={project} />
                            ))}
                        </div>
                    </motion.div>
                )}

                {/* Bottom Grid: Stability + Wallet + Stats */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Team Stability */}
                    <motion.div variants={itemVariants}>
                        <TeamStabilityWidget data={mockTeamStability} />
                    </motion.div>
                    
                    {/* Wallet Card */}
                    <motion.div variants={itemVariants}>
                        <div className="h-full overflow-hidden rounded-2xl bg-gradient-to-br from-primary-500 via-primary-600 to-secondary-600 p-6 text-white shadow-xl shadow-primary-200">
                            <div className="flex items-center justify-between mb-4">
                                <div>
                                    <p className="text-sm text-primary-100 opacity-80">Solde disponible</p>
                                    <p className="text-3xl font-bold tracking-tight">
                                        {walletBalance.toLocaleString('fr-FR')} €
                                    </p>
                                </div>
                                <Wallet className="h-10 w-10 text-primary-200/40" />
                            </div>
                            <p className="text-sm text-primary-100 opacity-60 mb-4">
                                Gérez vos paiements et factures en toute simplicité
                            </p>
                            <Link
                                href="/dashboard/client/finance"
                                className="inline-flex items-center gap-2 rounded-xl bg-white/20 px-4 py-2.5 text-sm font-medium backdrop-blur-sm transition-all hover:bg-white/30"
                            >
                                Gérer mon portefeuille
                                <ChevronRight className="h-4 w-4" />
                            </Link>
                        </div>
                    </motion.div>
                    
                    {/* Quick Stats */}
                    <motion.div variants={itemVariants} className="grid grid-cols-2 gap-4 content-start">
                        <StatCard
                            label={`${getTerm('missionPlural')} actives`}
                            value={3}
                            icon={Siren}
                            color="rose"
                        />
                        <StatCard
                            label={`${getTerm('talentPlural')} favoris`}
                            value={12}
                            icon={Heart}
                            color="purple"
                        />
                        <StatCard
                            label="Messages"
                            value={5}
                            icon={MessageCircle}
                            color="teal"
                        />
                        <StatCard
                            label="Avis reçus"
                            value={24}
                            icon={Star}
                            color="amber"
                        />
                    </motion.div>
                </div>

                {/* Workshops CTA */}
                {isFeatureEnabled('enableWorkshops') && (
                    <motion.div
                        variants={itemVariants}
                        className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-teal-500 to-emerald-500 p-6 text-white shadow-xl shadow-teal-200"
                    >
                        {/* Decorative elements */}
                        <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2" />
                        <div className="absolute bottom-0 left-0 w-40 h-40 bg-white/5 rounded-full translate-y-1/2 -translate-x-1/2" />
                        
                        <div className="relative flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                            <div className="flex items-center gap-4">
                                <div className="p-3 bg-white/20 rounded-2xl backdrop-blur-sm">
                                    <Sparkles className="h-8 w-8 text-white" />
                                </div>
                                <div>
                                    <h3 className="text-xl font-bold">Ateliers SocioLive</h3>
                                    <p className="text-teal-100 opacity-80">
                                        Bien-être, art-thérapie, sophrologie... Pour vos équipes et résidents
                                    </p>
                                </div>
                            </div>
                            <Link
                                href="/search?type=workshop"
                                className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-white text-teal-600 rounded-xl font-bold hover:bg-teal-50 transition-colors shadow-lg"
                            >
                                Explorer les ateliers
                                <ArrowRight size={18} />
                            </Link>
                        </div>
                    </motion.div>
                )}

                {/* Quick Links */}
                <motion.div variants={itemVariants} className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <Link
                        href="/dashboard/client/admin"
                        className="group flex items-center gap-4 p-4 bg-white border border-slate-200 rounded-2xl hover:border-amber-300 hover:shadow-lg transition-all"
                    >
                        <div className="p-3 bg-amber-50 rounded-xl">
                            <FileSignature className="h-6 w-6 text-amber-600" />
                        </div>
                        <div className="flex-1">
                            <p className="font-semibold text-slate-900">Contrats</p>
                            <p className="text-sm text-slate-500">{contractsToSign} en attente</p>
                        </div>
                        <ChevronRight className="h-5 w-5 text-slate-400 group-hover:translate-x-1 transition-transform" />
                    </Link>
                    
                    <Link
                        href="/dashboard/client/bookings"
                        className="group flex items-center gap-4 p-4 bg-white border border-slate-200 rounded-2xl hover:border-primary-300 hover:shadow-lg transition-all"
                    >
                        <div className="p-3 bg-primary-50 rounded-xl">
                            <Calendar className="h-6 w-6 text-primary-600" />
                        </div>
                        <div className="flex-1">
                            <p className="font-semibold text-slate-900">{getTerm('bookingPlural')}</p>
                            <p className="text-sm text-slate-500">5 à venir</p>
                        </div>
                        <ChevronRight className="h-5 w-5 text-slate-400 group-hover:translate-x-1 transition-transform" />
                    </Link>
                    
                    <Link
                        href="/dashboard/client/team"
                        className="group flex items-center gap-4 p-4 bg-white border border-slate-200 rounded-2xl hover:border-purple-300 hover:shadow-lg transition-all"
                    >
                        <div className="p-3 bg-purple-50 rounded-xl">
                            <Users className="h-6 w-6 text-purple-600" />
                        </div>
                        <div className="flex-1">
                            <p className="font-semibold text-slate-900">Mon Équipe</p>
                            <p className="text-sm text-slate-500">12 intervenants</p>
                        </div>
                        <ChevronRight className="h-5 w-5 text-slate-400 group-hover:translate-x-1 transition-transform" />
                    </Link>
                </motion.div>
            </motion.div>
        </div>
    );
}

export default SocialClientDashboard;
