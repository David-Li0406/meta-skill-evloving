'use client';

import { useState } from 'react';
import {
    UserCircle,
    Camera,
    Edit2,
    Save,
    MapPin,
    Briefcase,
    GraduationCap,
    Star,
    Award,
    Link as LinkIcon,
    Plus,
    X,
    Eye,
    Image,
    Video,
    FileText,
    CheckCircle2,
    ExternalLink,
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, Button, Badge, Input } from '@/components/ui';
import { cn } from '@/lib/utils';

// =============================================================================
// TYPES
// =============================================================================

interface TalentProfile {
    firstName: string;
    lastName: string;
    title: string;
    bio: string;
    avatarUrl?: string;
    coverUrl?: string;
    location: {
        city: string;
        postalCode: string;
        radius: number;
    };
    experience: number;
    certifications: string[];
    skills: string[];
    languages: string[];
    socialLinks: {
        linkedin?: string;
        website?: string;
    };
    stats: {
        rating: number;
        reviewsCount: number;
        completedMissions: number;
        responseRate: number;
    };
    badges: {
        id: string;
        label: string;
        icon: string;
    }[];
    media: {
        id: string;
        type: 'image' | 'video' | 'document';
        url: string;
        title: string;
    }[];
}

// =============================================================================
// MOCK DATA
// =============================================================================

const mockProfile: TalentProfile = {
    firstName: 'Marie',
    lastName: 'Laurent',
    title: 'Éducatrice Spécialisée & Formatrice',
    bio: 'Passionnée par l\'accompagnement des jeunes en difficulté depuis plus de 10 ans. Spécialisée en gestion des émotions et communication non-violente. J\'interviens également en formation auprès des équipes éducatives.',
    avatarUrl: undefined,
    coverUrl: undefined,
    location: {
        city: 'Lyon',
        postalCode: '69003',
        radius: 30,
    },
    experience: 12,
    certifications: ['DEES', 'DU Médiation', 'Certification CNV'],
    skills: ['Gestion de groupe', 'Communication Non-Violente', 'Animation d\'ateliers', 'Accompagnement individuel', 'Supervision'],
    languages: ['Français (natif)', 'Anglais (B2)'],
    socialLinks: {
        linkedin: 'https://linkedin.com/in/marie-laurent',
        website: 'https://marie-laurent-educ.fr',
    },
    stats: {
        rating: 4.9,
        reviewsCount: 32,
        completedMissions: 47,
        responseRate: 98,
    },
    badges: [
        { id: '1', label: 'Top Performer', icon: '🏆' },
        { id: '2', label: 'Réponse rapide', icon: '⚡' },
        { id: '3', label: 'Super hôte', icon: '🌟' },
    ],
    media: [
        { id: '1', type: 'image', url: '/images/workshop1.jpg', title: 'Atelier gestion du stress' },
        { id: '2', type: 'video', url: '/videos/intro.mp4', title: 'Vidéo de présentation' },
        { id: '3', type: 'document', url: '/docs/cv.pdf', title: 'CV détaillé' },
    ],
};

// =============================================================================
// COMPONENTS
// =============================================================================

function ProfileHeader({ profile, onEdit }: { profile: TalentProfile; onEdit: () => void }) {
    return (
        <Card className="border-slate-200 overflow-hidden">
            {/* Cover */}
            <div className="h-32 bg-gradient-to-r from-primary-500 via-primary-600 to-secondary-500 relative">
                <button className="absolute top-3 right-3 p-2 bg-white/20 backdrop-blur rounded-lg text-white hover:bg-white/30 transition-colors">
                    <Camera size={16} />
                </button>
            </div>

            {/* Avatar & Info */}
            <CardContent className="pt-0 relative">
                <div className="flex flex-col sm:flex-row sm:items-end gap-4 -mt-12">
                    <div className="relative">
                        <div className="w-24 h-24 rounded-2xl bg-white border-4 border-white shadow-lg overflow-hidden">
                            {profile.avatarUrl ? (
                                <img src={profile.avatarUrl} alt="" className="w-full h-full object-cover" />
                            ) : (
                                <div className="w-full h-full bg-gradient-to-br from-primary-100 to-primary-200 flex items-center justify-center">
                                    <span className="text-3xl font-bold text-primary-600">
                                        {profile.firstName[0]}{profile.lastName[0]}
                                    </span>
                                </div>
                            )}
                        </div>
                        <button className="absolute -bottom-1 -right-1 p-1.5 bg-primary-600 text-white rounded-full shadow-lg hover:bg-primary-700 transition-colors">
                            <Camera size={12} />
                        </button>
                    </div>
                    <div className="flex-1 pb-2">
                        <h1 className="text-2xl font-bold text-slate-900">{profile.firstName} {profile.lastName}</h1>
                        <p className="text-slate-600">{profile.title}</p>
                        <div className="flex items-center gap-3 mt-2 text-sm text-slate-500">
                            <span className="flex items-center gap-1">
                                <MapPin size={14} />
                                {profile.location.city} • {profile.location.radius}km
                            </span>
                            <span className="flex items-center gap-1">
                                <Briefcase size={14} />
                                {profile.experience} ans d'exp.
                            </span>
                        </div>
                    </div>
                    <div className="flex gap-2">
                        <Button variant="outline" className="gap-2">
                            <Eye size={16} /> Aperçu public
                        </Button>
                        <Button onClick={onEdit} className="gap-2 bg-primary-600 hover:bg-primary-700 text-white">
                            <Edit2 size={16} /> Modifier
                        </Button>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}

function StatsGrid({ stats }: { stats: TalentProfile['stats'] }) {
    return (
        <div className="grid grid-cols-4 gap-4">
            <Card className="border-slate-200">
                <CardContent className="p-4 text-center">
                    <div className="flex items-center justify-center gap-1 mb-1">
                        <Star size={18} className="text-amber-400 fill-amber-400" />
                        <span className="text-2xl font-bold text-slate-900">{stats.rating}</span>
                    </div>
                    <p className="text-xs text-slate-500">{stats.reviewsCount} avis</p>
                </CardContent>
            </Card>
            <Card className="border-slate-200">
                <CardContent className="p-4 text-center">
                    <p className="text-2xl font-bold text-slate-900">{stats.completedMissions}</p>
                    <p className="text-xs text-slate-500">Missions</p>
                </CardContent>
            </Card>
            <Card className="border-slate-200">
                <CardContent className="p-4 text-center">
                    <p className="text-2xl font-bold text-emerald-600">{stats.responseRate}%</p>
                    <p className="text-xs text-slate-500">Taux de réponse</p>
                </CardContent>
            </Card>
            <Card className="border-slate-200">
                <CardContent className="p-4 text-center">
                    <div className="flex items-center justify-center gap-1">
                        <CheckCircle2 size={18} className="text-emerald-500" />
                    </div>
                    <p className="text-xs text-slate-500 mt-1">Profil vérifié</p>
                </CardContent>
            </Card>
        </div>
    );
}

function BadgesSection({ badges }: { badges: TalentProfile['badges'] }) {
    return (
        <Card className="border-slate-200">
            <CardHeader className="pb-3">
                <CardTitle className="text-base font-semibold flex items-center gap-2">
                    <Award size={18} className="text-amber-500" />
                    Badges obtenus
                </CardTitle>
            </CardHeader>
            <CardContent>
                <div className="flex flex-wrap gap-2">
                    {badges.map((badge) => (
                        <div
                            key={badge.id}
                            className="flex items-center gap-2 px-3 py-2 bg-amber-50 border border-amber-200 rounded-xl"
                        >
                            <span className="text-lg">{badge.icon}</span>
                            <span className="text-sm font-medium text-amber-800">{badge.label}</span>
                        </div>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
}

function BioSection({ bio, onEdit }: { bio: string; onEdit: () => void }) {
    const [isEditing, setIsEditing] = useState(false);
    const [editedBio, setEditedBio] = useState(bio);

    return (
        <Card className="border-slate-200">
            <CardHeader className="pb-3 flex flex-row items-center justify-between">
                <CardTitle className="text-base font-semibold">À propos</CardTitle>
                <button
                    onClick={() => setIsEditing(!isEditing)}
                    className="p-1.5 hover:bg-slate-100 rounded-lg text-slate-400 hover:text-slate-600"
                >
                    <Edit2 size={14} />
                </button>
            </CardHeader>
            <CardContent>
                {isEditing ? (
                    <div className="space-y-3">
                        <textarea
                            value={editedBio}
                            onChange={(e) => setEditedBio(e.target.value)}
                            className="w-full h-32 px-3 py-2 border border-slate-200 rounded-xl resize-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                        />
                        <div className="flex justify-end gap-2">
                            <Button variant="outline" size="sm" onClick={() => setIsEditing(false)}>
                                Annuler
                            </Button>
                            <Button size="sm" className="bg-primary-600 hover:bg-primary-700 text-white gap-1">
                                <Save size={14} /> Enregistrer
                            </Button>
                        </div>
                    </div>
                ) : (
                    <p className="text-slate-600 leading-relaxed">{bio}</p>
                )}
            </CardContent>
        </Card>
    );
}

function SkillsSection({ title, items, icon: Icon, onAdd }: { title: string; items: string[]; icon: React.ElementType; onAdd?: () => void }) {
    return (
        <Card className="border-slate-200">
            <CardHeader className="pb-3 flex flex-row items-center justify-between">
                <CardTitle className="text-base font-semibold flex items-center gap-2">
                    <Icon size={18} className="text-primary-500" />
                    {title}
                </CardTitle>
                {onAdd && (
                    <button
                        onClick={onAdd}
                        className="p-1.5 hover:bg-slate-100 rounded-lg text-slate-400 hover:text-slate-600"
                    >
                        <Plus size={14} />
                    </button>
                )}
            </CardHeader>
            <CardContent>
                <div className="flex flex-wrap gap-2">
                    {items.map((item, i) => (
                        <span
                            key={i}
                            className="px-3 py-1.5 bg-slate-100 text-slate-700 rounded-lg text-sm font-medium group flex items-center gap-1"
                        >
                            {item}
                            <button className="opacity-0 group-hover:opacity-100 text-slate-400 hover:text-rose-500 transition-opacity">
                                <X size={12} />
                            </button>
                        </span>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
}

function MediaSection({ media }: { media: TalentProfile['media'] }) {
    const typeIcons = {
        image: Image,
        video: Video,
        document: FileText,
    };

    return (
        <Card className="border-slate-200">
            <CardHeader className="pb-3 flex flex-row items-center justify-between">
                <CardTitle className="text-base font-semibold flex items-center gap-2">
                    <Image size={18} className="text-primary-500" />
                    Médias & Portfolio
                </CardTitle>
                <Button variant="outline" size="sm" className="gap-1">
                    <Plus size={14} /> Ajouter
                </Button>
            </CardHeader>
            <CardContent>
                <div className="grid grid-cols-3 gap-3">
                    {media.map((item) => {
                        const Icon = typeIcons[item.type];
                        return (
                            <div
                                key={item.id}
                                className="aspect-video bg-slate-100 rounded-xl border border-slate-200 flex flex-col items-center justify-center hover:border-primary-300 transition-colors cursor-pointer group"
                            >
                                <Icon size={24} className="text-slate-400 group-hover:text-primary-500 mb-1" />
                                <span className="text-xs text-slate-500 text-center px-2 truncate max-w-full">
                                    {item.title}
                                </span>
                            </div>
                        );
                    })}
                    <div className="aspect-video bg-slate-50 rounded-xl border-2 border-dashed border-slate-300 flex flex-col items-center justify-center hover:border-primary-400 hover:bg-primary-50 transition-colors cursor-pointer">
                        <Plus size={24} className="text-slate-400" />
                        <span className="text-xs text-slate-500 mt-1">Ajouter</span>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}

function SocialLinksSection({ links }: { links: TalentProfile['socialLinks'] }) {
    return (
        <Card className="border-slate-200">
            <CardHeader className="pb-3">
                <CardTitle className="text-base font-semibold flex items-center gap-2">
                    <LinkIcon size={18} className="text-primary-500" />
                    Liens
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
                {links.linkedin && (
                    <a
                        href={links.linkedin}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-3 p-3 bg-slate-50 rounded-xl hover:bg-slate-100 transition-colors group"
                    >
                        <div className="p-2 bg-blue-100 rounded-lg">
                            <span className="text-blue-600 font-bold text-sm">in</span>
                        </div>
                        <div className="flex-1 min-w-0">
                            <p className="font-medium text-slate-900">LinkedIn</p>
                            <p className="text-sm text-slate-500 truncate">{links.linkedin}</p>
                        </div>
                        <ExternalLink size={16} className="text-slate-400 group-hover:text-slate-600" />
                    </a>
                )}
                {links.website && (
                    <a
                        href={links.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-3 p-3 bg-slate-50 rounded-xl hover:bg-slate-100 transition-colors group"
                    >
                        <div className="p-2 bg-emerald-100 rounded-lg">
                            <LinkIcon size={14} className="text-emerald-600" />
                        </div>
                        <div className="flex-1 min-w-0">
                            <p className="font-medium text-slate-900">Site web</p>
                            <p className="text-sm text-slate-500 truncate">{links.website}</p>
                        </div>
                        <ExternalLink size={16} className="text-slate-400 group-hover:text-slate-600" />
                    </a>
                )}
                <button className="w-full flex items-center justify-center gap-2 p-3 border-2 border-dashed border-slate-300 rounded-xl text-slate-500 hover:border-primary-400 hover:text-primary-600 transition-colors">
                    <Plus size={16} /> Ajouter un lien
                </button>
            </CardContent>
        </Card>
    );
}

// =============================================================================
// PAGE
// =============================================================================

export default function TalentProfilePage() {
    const [profile] = useState<TalentProfile>(mockProfile);

    return (
        <div className="space-y-6 max-w-4xl mx-auto">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
                    <UserCircle className="text-primary-500" />
                    Mon Profil Public
                </h1>
                <p className="text-slate-500 mt-1">Personnalisez votre profil visible par les clients</p>
            </div>

            {/* Profile Header Card */}
            <ProfileHeader profile={profile} onEdit={() => {}} />

            {/* Stats */}
            <StatsGrid stats={profile.stats} />

            {/* Two Column Layout */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 space-y-6">
                    <BioSection bio={profile.bio} onEdit={() => {}} />
                    <SkillsSection title="Compétences" items={profile.skills} icon={Briefcase} onAdd={() => {}} />
                    <MediaSection media={profile.media} />
                </div>
                <div className="space-y-6">
                    <BadgesSection badges={profile.badges} />
                    <SkillsSection title="Certifications" items={profile.certifications} icon={GraduationCap} onAdd={() => {}} />
                    <SkillsSection title="Langues" items={profile.languages} icon={GraduationCap} />
                    <SocialLinksSection links={profile.socialLinks} />
                </div>
            </div>
        </div>
    );
}
