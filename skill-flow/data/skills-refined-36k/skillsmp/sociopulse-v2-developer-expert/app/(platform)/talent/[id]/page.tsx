'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';
import {
    ArrowLeft,
    Shield,
    ShieldCheck,
    BadgeCheck,
    FileCheck,
    Heart,
    Share2,
    MessageCircle,
    Calendar,
    Clock,
    Users,
    MapPin,
    Video,
    Euro,
    Loader2,
    AlertCircle,
    Star,
    Briefcase,
    GraduationCap,
    CheckCircle2,
} from 'lucide-react';
import { Card, CardContent, Button, Badge } from '@/components/ui';
import { cn } from '@/lib/utils';
import { getApiUrl } from '@/lib/config';

// =============================================================================
// TYPES
// =============================================================================

interface TrustBadge {
    key: 'identity' | 'diploma' | 'insurance';
    label: string;
    verified: boolean;
    icon: React.ElementType;
}

interface PublishedService {
    id: string;
    name: string;
    slug: string;
    description?: string;
    shortDescription?: string;
    type: 'WORKSHOP' | 'COACHING_VIDEO';
    category?: string;
    basePrice?: number;
    imageUrl?: string;
    minParticipants: number;
    maxParticipants: number;
    totalBookings: number;
    averageRating: number;
}

interface TalentProfile {
    id: string;
    email: string;
    phone?: string;
    status: string;
    isVerified: boolean;
    isAvailableForSOS: boolean; // Key field for dual availability
    profile: {
        firstName: string;
        lastName: string;
        avatarUrl?: string;
        coverUrl?: string;
        bio?: string;
        headline?: string;
        specialties: string[];
        diplomas: Array<{ name: string; year?: number }>;
        hourlyRate?: number;
        city?: string;
        radiusKm: number;
        isVideoEnabled: boolean;
        totalMissions: number;
        totalBookings: number;
        averageRating: number;
        totalReviews: number;
    };
    // Trust verification fields
    hasVerifiedIdentity: boolean;
    hasVerifiedDiploma: boolean;
    hasVerifiedInsurance: boolean;
    // Services
    services: PublishedService[];
}

// =============================================================================
// MOCK DATA (Replace with API fetch)
// =============================================================================

const MOCK_TALENT: TalentProfile = {
    id: 'talent_123',
    email: 'thomas.martin@email.com',
    phone: '06 12 34 56 78',
    status: 'VERIFIED',
    isVerified: true,
    isAvailableForSOS: true,
    hasVerifiedIdentity: true,
    hasVerifiedDiploma: true,
    hasVerifiedInsurance: true,
    profile: {
        firstName: 'Thomas',
        lastName: 'Martin',
        avatarUrl: undefined,
        coverUrl: undefined,
        bio: 'Éducateur spécialisé passionné avec plus de 8 ans d\'expérience en MECS et ITEP. Spécialisé dans l\'accompagnement des adolescents en difficulté et la médiation par le sport.',
        headline: 'Éducateur Spécialisé • Spécialiste Autisme & Troubles du Comportement',
        specialties: ['Autisme', 'Troubles du comportement', 'Boxe éducative', 'Médiation animale'],
        diplomas: [
            { name: 'DEES - Diplôme d\'État d\'Éducateur Spécialisé', year: 2016 },
            { name: 'Certificat Boxe Éducative', year: 2019 },
        ],
        hourlyRate: 35,
        city: 'Lyon 3e',
        radiusKm: 30,
        isVideoEnabled: true,
        totalMissions: 47,
        totalBookings: 23,
        averageRating: 4.9,
        totalReviews: 34,
    },
    services: [
        {
            id: 'svc_1',
            name: 'Atelier Boxe Éducative',
            slug: 'atelier-boxe-educative',
            shortDescription: 'Canaliser l\'énergie par le noble art. Développement de la confiance et du respect.',
            type: 'WORKSHOP',
            category: 'Sport adapté',
            basePrice: 250,
            imageUrl: undefined,
            minParticipants: 4,
            maxParticipants: 12,
            totalBookings: 15,
            averageRating: 4.8,
        },
        {
            id: 'svc_2',
            name: 'Coaching Parental - Gestion des Crises',
            slug: 'coaching-parental-crises',
            shortDescription: 'Accompagnement personnalisé pour parents face aux comportements difficiles.',
            type: 'COACHING_VIDEO',
            category: 'Coaching',
            basePrice: 60,
            imageUrl: undefined,
            minParticipants: 1,
            maxParticipants: 2,
            totalBookings: 8,
            averageRating: 5.0,
        },
        {
            id: 'svc_3',
            name: 'Médiation Animale - Séance Découverte',
            slug: 'mediation-animale-decouverte',
            shortDescription: 'Créer du lien avec les animaux pour favoriser l\'expression émotionnelle.',
            type: 'WORKSHOP',
            category: 'Bien-être',
            basePrice: 180,
            imageUrl: undefined,
            minParticipants: 2,
            maxParticipants: 8,
            totalBookings: 6,
            averageRating: 4.9,
        },
    ],
};

// =============================================================================
// COMPONENTS
// =============================================================================

function SOSStatusBadge({ isAvailable }: { isAvailable: boolean }) {
    if (isAvailable) {
        return (
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-50 border-2 border-emerald-200 rounded-full">
                <span className="relative flex h-3 w-3">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
                </span>
                <span className="font-bold text-emerald-700">DISPONIBLE RENFORT</span>
            </div>
        );
    }

    return (
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-amber-50 border-2 border-amber-200 rounded-full">
            <span className="relative flex h-3 w-3">
                <span className="relative inline-flex rounded-full h-3 w-3 bg-amber-500"></span>
            </span>
            <span className="font-bold text-amber-700">INDISPONIBLE RENFORT</span>
        </div>
    );
}

function SOSActionButton({ 
    isAvailable, 
    onClick 
}: { 
    isAvailable: boolean; 
    onClick: () => void;
}) {
    if (isAvailable) {
        return (
            <Button
                onClick={onClick}
                className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-3 rounded-xl"
            >
                <Briefcase size={18} className="mr-2" />
                Proposer une Mission SOS
            </Button>
        );
    }

    return (
        <div className="space-y-2">
            <Button
                disabled
                className="bg-slate-200 text-slate-500 font-bold px-6 py-3 rounded-xl cursor-not-allowed"
            >
                <Briefcase size={18} className="mr-2" />
                Mission SOS non disponible
            </Button>
            <p className="text-sm text-slate-500 italic">
                Ce talent n'accepte pas de missions d'urgence pour le moment.
            </p>
        </div>
    );
}

function TrustBar({ badges }: { badges: TrustBadge[] }) {
    const allVerified = badges.every(b => b.verified);
    const verifiedCount = badges.filter(b => b.verified).length;

    return (
        <div className="space-y-4">
            {/* Shield Badge if all verified */}
            {allVerified && (
                <div className="flex items-center justify-center gap-2 p-3 bg-gradient-to-r from-emerald-50 to-teal-50 border-2 border-emerald-200 rounded-xl">
                    <ShieldCheck size={24} className="text-emerald-600" />
                    <span className="font-bold text-emerald-700 text-lg">PROFIL VÉRIFIÉ</span>
                </div>
            )}

            {/* Individual Badges */}
            <div className="flex flex-wrap justify-center gap-3">
                {badges.map((badge) => {
                    const Icon = badge.icon;
                    return (
                        <div
                            key={badge.key}
                            className={cn(
                                'flex items-center gap-2 px-4 py-2 rounded-xl border-2 transition-all',
                                badge.verified
                                    ? 'bg-slate-50 border-slate-200 text-slate-700'
                                    : 'bg-slate-100 border-slate-100 text-slate-400'
                            )}
                        >
                            <Icon size={18} className={badge.verified ? 'text-emerald-600' : 'text-slate-400'} />
                            <span className="text-sm font-medium">{badge.label}</span>
                            {badge.verified && <CheckCircle2 size={14} className="text-emerald-600" />}
                        </div>
                    );
                })}
            </div>

            {/* Progress hint if not all verified */}
            {!allVerified && (
                <p className="text-center text-sm text-slate-500">
                    {verifiedCount}/3 vérifications complétées
                </p>
            )}
        </div>
    );
}

function ServiceCard({ 
    service, 
    onBook 
}: { 
    service: PublishedService; 
    onBook: () => void;
}) {
    const isWorkshop = service.type === 'WORKSHOP';

    return (
        <Card className="overflow-hidden border-2 border-slate-100 hover:border-slate-200 hover:shadow-lg transition-all group">
            {/* Image */}
            <div className={cn(
                'aspect-[16/10] relative',
                service.imageUrl 
                    ? 'bg-slate-200' 
                    : isWorkshop 
                        ? 'bg-gradient-to-br from-indigo-100 to-indigo-200' 
                        : 'bg-gradient-to-br from-teal-100 to-teal-200'
            )}>
                {service.imageUrl ? (
                    <img src={service.imageUrl} alt={service.name} className="w-full h-full object-cover" />
                ) : (
                    <div className="absolute inset-0 flex items-center justify-center">
                        {isWorkshop ? (
                            <Users size={48} className="text-indigo-300" />
                        ) : (
                            <Video size={48} className="text-teal-300" />
                        )}
                    </div>
                )}
                
                {/* Type Badge */}
                <div className="absolute top-3 left-3">
                    <span className={cn(
                        'px-3 py-1 text-xs font-bold rounded-full',
                        isWorkshop ? 'bg-indigo-600 text-white' : 'bg-teal-600 text-white'
                    )}>
                        {isWorkshop ? '👥 Atelier' : '📹 Visio'}
                    </span>
                </div>

                {/* Category */}
                {service.category && (
                    <div className="absolute top-3 right-3">
                        <span className="px-2 py-1 text-xs font-medium bg-white/90 text-slate-700 rounded-full">
                            {service.category}
                        </span>
                    </div>
                )}
            </div>

            {/* Content */}
            <CardContent className="p-4">
                <h3 className="font-bold text-lg text-slate-900 line-clamp-1 group-hover:text-primary-600 transition-colors">
                    {service.name}
                </h3>

                {service.shortDescription && (
                    <p className="text-sm text-slate-600 mt-2 line-clamp-2">
                        {service.shortDescription}
                    </p>
                )}

                {/* Meta */}
                <div className="flex items-center gap-3 mt-3 text-xs text-slate-500">
                    <span className="flex items-center gap-1">
                        <Users size={12} />
                        {service.minParticipants}-{service.maxParticipants} pers.
                    </span>
                    {service.totalBookings > 0 && (
                        <span className="flex items-center gap-1">
                            <Calendar size={12} />
                            {service.totalBookings} réservations
                        </span>
                    )}
                </div>

                {/* Price & Action */}
                <div className="flex items-center justify-between mt-4 pt-4 border-t border-slate-100">
                    <div>
                        <p className="text-2xl font-bold text-slate-900">
                            {service.basePrice}€
                        </p>
                        <p className="text-xs text-slate-500">par session</p>
                    </div>
                    <Button 
                        onClick={onBook}
                        className={cn(
                            'text-white font-semibold',
                            isWorkshop 
                                ? 'bg-indigo-600 hover:bg-indigo-700' 
                                : 'bg-teal-600 hover:bg-teal-700'
                        )}
                    >
                        <Calendar size={16} className="mr-2" />
                        Réserver
                    </Button>
                </div>
            </CardContent>
        </Card>
    );
}

function ProfileHeader({ 
    talent, 
    onMessage, 
    onShare, 
    onFavorite,
    isFavorite 
}: { 
    talent: TalentProfile;
    onMessage: () => void;
    onShare: () => void;
    onFavorite: () => void;
    isFavorite: boolean;
}) {
    const { profile } = talent;
    const initials = `${profile.firstName[0]}${profile.lastName[0]}`.toUpperCase();

    return (
        <div className="relative">
            {/* Cover */}
            <div className={cn(
                'h-32 sm:h-48',
                profile.coverUrl 
                    ? 'bg-slate-200' 
                    : 'bg-gradient-to-r from-primary-100 via-primary-50 to-secondary-100'
            )}>
                {profile.coverUrl && (
                    <img src={profile.coverUrl} alt="" className="w-full h-full object-cover" />
                )}
            </div>

            {/* Avatar */}
            <div className="absolute left-6 -bottom-12 sm:-bottom-16">
                <div className="w-24 h-24 sm:w-32 sm:h-32 rounded-2xl bg-white border-4 border-white shadow-lg overflow-hidden">
                    {profile.avatarUrl ? (
                        <img src={profile.avatarUrl} alt={profile.firstName} className="w-full h-full object-cover" />
                    ) : (
                        <div className="w-full h-full bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center">
                            <span className="text-3xl sm:text-4xl font-bold text-white">{initials}</span>
                        </div>
                    )}
                </div>
                {talent.isVerified && (
                    <div className="absolute -bottom-1 -right-1 bg-white rounded-full p-1 shadow-md">
                        <BadgeCheck size={24} className="text-primary-600" />
                    </div>
                )}
            </div>

            {/* Action Buttons */}
            <div className="absolute top-4 right-4 flex items-center gap-2">
                <Button 
                    variant="outline" 
                    size="sm" 
                    onClick={onShare}
                    className="bg-white/90 backdrop-blur-sm"
                >
                    <Share2 size={16} />
                </Button>
                <Button 
                    variant="outline" 
                    size="sm" 
                    onClick={onFavorite}
                    className={cn(
                        'bg-white/90 backdrop-blur-sm',
                        isFavorite && 'text-rose-500 border-rose-200'
                    )}
                >
                    <Heart size={16} className={isFavorite ? 'fill-current' : ''} />
                </Button>
                <Button 
                    variant="outline" 
                    size="sm" 
                    onClick={onMessage}
                    className="bg-white/90 backdrop-blur-sm"
                >
                    <MessageCircle size={16} />
                </Button>
            </div>
        </div>
    );
}

// =============================================================================
// PAGE
// =============================================================================

export default function PublicTalentProfilePage() {
    const params = useParams();
    const router = useRouter();
    const talentId = params.id as string;

    const [talent, setTalent] = useState<TalentProfile | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [isFavorite, setIsFavorite] = useState(false);
    const [bookingModalService, setBookingModalService] = useState<string | null>(null);

    // Fetch talent profile
    useEffect(() => {
        const fetchTalent = async () => {
            setIsLoading(true);
            try {
                // TODO: Replace with actual API call
                // const response = await fetch(`${getApiUrl()}/talents/${talentId}/public`);
                // const data = await response.json();
                // setTalent(data);
                
                // Using mock data for now
                await new Promise(resolve => setTimeout(resolve, 500));
                setTalent(MOCK_TALENT);
            } catch (err) {
                setError('Impossible de charger le profil');
            } finally {
                setIsLoading(false);
            }
        };

        fetchTalent();
    }, [talentId]);

    // Build trust badges
    const trustBadges: TrustBadge[] = talent ? [
        { key: 'identity', label: 'Identité Vérifiée', verified: talent.hasVerifiedIdentity, icon: BadgeCheck },
        { key: 'diploma', label: 'Diplôme Certifié', verified: talent.hasVerifiedDiploma, icon: GraduationCap },
        { key: 'insurance', label: 'Assurance Validée', verified: talent.hasVerifiedInsurance, icon: FileCheck },
    ] : [];

    // Handlers
    const handleProposeSOS = () => {
        router.push(`/sos/create?talentId=${talentId}`);
    };

    const handleBookService = (serviceId: string) => {
        // Open calendar modal or redirect to booking page
        router.push(`/services/${serviceId}/book`);
    };

    const handleMessage = () => {
        router.push(`/messages?userId=${talentId}`);
    };

    const handleShare = async () => {
        if (navigator.share) {
            await navigator.share({
                title: talent ? `${talent.profile.firstName} ${talent.profile.lastName}` : 'Profil Talent',
                url: window.location.href,
            });
        } else {
            navigator.clipboard.writeText(window.location.href);
            // TODO: Show toast
        }
    };

    // Loading state
    if (isLoading) {
        return (
            <div className="min-h-screen bg-slate-50 flex items-center justify-center">
                <div className="text-center space-y-4">
                    <Loader2 className="w-10 h-10 animate-spin text-primary-600 mx-auto" />
                    <p className="text-slate-500">Chargement du profil...</p>
                </div>
            </div>
        );
    }

    // Error state
    if (error || !talent) {
        return (
            <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
                <Card className="max-w-md w-full p-8 text-center">
                    <AlertCircle className="w-12 h-12 text-amber-500 mx-auto mb-4" />
                    <h2 className="text-xl font-bold text-slate-900 mb-2">Profil introuvable</h2>
                    <p className="text-slate-500 mb-6">{error || 'Ce talent n\'existe pas ou n\'est plus disponible.'}</p>
                    <Button onClick={() => router.back()}>
                        <ArrowLeft size={16} className="mr-2" />
                        Retour
                    </Button>
                </Card>
            </div>
        );
    }

    const { profile } = talent;

    return (
        <div className="min-h-screen bg-slate-50">
            {/* Back Button */}
            <div className="fixed top-4 left-4 z-50">
                <Button 
                    variant="outline" 
                    size="sm" 
                    onClick={() => router.back()}
                    className="bg-white/90 backdrop-blur-sm shadow-sm"
                >
                    <ArrowLeft size={16} className="mr-1" />
                    Retour
                </Button>
            </div>

            {/* Profile Header */}
            <Card className="overflow-hidden border-0 rounded-none sm:rounded-b-3xl shadow-sm">
                <ProfileHeader 
                    talent={talent}
                    onMessage={handleMessage}
                    onShare={handleShare}
                    onFavorite={() => setIsFavorite(!isFavorite)}
                    isFavorite={isFavorite}
                />

                {/* Profile Info */}
                <div className="pt-16 sm:pt-20 px-6 pb-6">
                    {/* Name & Headline */}
                    <div className="mb-4">
                        <h1 className="text-2xl sm:text-3xl font-bold text-slate-900">
                            {profile.firstName} {profile.lastName}
                        </h1>
                        {profile.headline && (
                            <p className="text-slate-600 mt-1">{profile.headline}</p>
                        )}
                        {profile.city && (
                            <p className="flex items-center gap-1 text-sm text-slate-500 mt-2">
                                <MapPin size={14} />
                                {profile.city} • Rayon {profile.radiusKm}km
                            </p>
                        )}
                    </div>

                    {/* SOS Status Section */}
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 p-4 bg-slate-50 rounded-2xl mb-6">
                        <SOSStatusBadge isAvailable={talent.isAvailableForSOS} />
                        <SOSActionButton 
                            isAvailable={talent.isAvailableForSOS} 
                            onClick={handleProposeSOS}
                        />
                    </div>

                    {/* Trust Badges */}
                    <TrustBar badges={trustBadges} />

                    {/* Bio */}
                    {profile.bio && (
                        <div className="mt-6 p-4 bg-slate-50 rounded-xl">
                            <h3 className="font-semibold text-slate-900 mb-2">À propos</h3>
                            <p className="text-slate-600 leading-relaxed">{profile.bio}</p>
                        </div>
                    )}

                    {/* Specialties */}
                    {profile.specialties.length > 0 && (
                        <div className="mt-4">
                            <h3 className="font-semibold text-slate-900 mb-2">Spécialités</h3>
                            <div className="flex flex-wrap gap-2">
                                {profile.specialties.map((specialty, i) => (
                                    <Badge key={i} variant="secondary" className="px-3 py-1">
                                        {specialty}
                                    </Badge>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Diplomas */}
                    {profile.diplomas.length > 0 && (
                        <div className="mt-4">
                            <h3 className="font-semibold text-slate-900 mb-2">Diplômes & Certifications</h3>
                            <ul className="space-y-2">
                                {profile.diplomas.map((diploma, i) => (
                                    <li key={i} className="flex items-center gap-2 text-slate-600">
                                        <GraduationCap size={16} className="text-primary-500" />
                                        <span>{diploma.name}</span>
                                        {diploma.year && (
                                            <span className="text-slate-400">({diploma.year})</span>
                                        )}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}

                    {/* Quick Stats */}
                    <div className="grid grid-cols-3 gap-4 mt-6 p-4 bg-gradient-to-r from-primary-50 to-secondary-50 rounded-xl">
                        <div className="text-center">
                            <p className="text-2xl font-bold text-slate-900">{profile.totalMissions}</p>
                            <p className="text-xs text-slate-500">Missions SOS</p>
                        </div>
                        <div className="text-center border-x border-slate-200">
                            <p className="text-2xl font-bold text-slate-900">{profile.totalBookings}</p>
                            <p className="text-xs text-slate-500">Réservations</p>
                        </div>
                        <div className="text-center">
                            <p className="text-2xl font-bold text-slate-900">{profile.totalReviews}</p>
                            <p className="text-xs text-slate-500">Avis vérifiés</p>
                        </div>
                    </div>
                </div>
            </Card>

            {/* Services Grid (Always Open) */}
            <div className="max-w-6xl mx-auto px-4 py-8">
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <h2 className="text-xl font-bold text-slate-900">Services proposés</h2>
                        <p className="text-slate-500 text-sm">Réservez un atelier ou une session de coaching</p>
                    </div>
                    {talent.services.length > 0 && (
                        <Badge className="bg-primary-100 text-primary-700">
                            {talent.services.length} service{talent.services.length > 1 ? 's' : ''}
                        </Badge>
                    )}
                </div>

                {talent.services.length > 0 ? (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                        {talent.services.map((service) => (
                            <ServiceCard
                                key={service.id}
                                service={service}
                                onBook={() => handleBookService(service.id)}
                            />
                        ))}
                    </div>
                ) : (
                    <Card className="p-8 text-center bg-slate-50 border-dashed">
                        <Users size={48} className="mx-auto text-slate-300 mb-4" />
                        <h3 className="font-semibold text-slate-700 mb-2">Aucun service publié</h3>
                        <p className="text-slate-500 text-sm">
                            Ce talent n'a pas encore publié de services sur la marketplace.
                        </p>
                    </Card>
                )}
            </div>

            {/* Mobile Sticky CTA */}
            <div className="fixed bottom-0 left-0 right-0 p-4 bg-white border-t border-slate-200 sm:hidden z-40">
                <div className="flex gap-2">
                    <Button 
                        variant="outline" 
                        className="flex-1"
                        onClick={handleMessage}
                    >
                        <MessageCircle size={18} className="mr-2" />
                        Message
                    </Button>
                    {talent.isAvailableForSOS ? (
                        <Button 
                            className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white"
                            onClick={handleProposeSOS}
                        >
                            <Briefcase size={18} className="mr-2" />
                            Mission SOS
                        </Button>
                    ) : (
                        <Button 
                            disabled
                            className="flex-1 bg-slate-200 text-slate-500"
                        >
                            SOS indisponible
                        </Button>
                    )}
                </div>
            </div>

            {/* Spacer for mobile sticky CTA */}
            <div className="h-20 sm:hidden" />
        </div>
    );
}
