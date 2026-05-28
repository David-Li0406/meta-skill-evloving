'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { ProfileHeader, ProfileHeaderProps } from './ProfileHeader';
import { StatsRow, TrustStats } from './StatsRow';
import { MobileActionBar, DesktopActions } from './MobileActionBar';

export interface UserProfileData extends Omit<ProfileHeaderProps, 'isOwnProfile' | 'onEditCover' | 'onEditAvatar'> {
    /** User ID */
    id: string;
    /** User email */
    email?: string;
    /** User phone */
    phone?: string;
    /** Bio / description */
    bio?: string | null;
    /** Trust statistics */
    stats: TrustStats;
}

export interface UserProfileProps {
    /** Profile data */
    profile: UserProfileData;
    /** Whether this is the current user's own profile */
    isOwnProfile?: boolean;
    /** Whether the current user has favorited this profile */
    isFavorite?: boolean;
    /** Callback when primary action is clicked */
    onPrimaryAction?: () => void;
    /** Callback when message is clicked */
    onMessage?: () => void;
    /** Callback when favorite is toggled */
    onFavoriteToggle?: () => void;
    /** Callback when share is clicked */
    onShare?: () => void;
    /** Callback when call is clicked (if phone available) */
    onCall?: () => void;
    /** Callback when edit cover is clicked */
    onEditCover?: () => void;
    /** Callback when edit avatar is clicked */
    onEditAvatar?: () => void;
}

export function UserProfile({
    profile,
    isOwnProfile = false,
    isFavorite = false,
    onPrimaryAction,
    onMessage,
    onFavoriteToggle,
    onShare,
    onCall,
    onEditCover,
    onEditAvatar,
}: UserProfileProps) {
    return (
        <div className="card-surface overflow-hidden border border-slate-100">
            {/* Profile Header (Cover + Avatar + Name) */}
            <ProfileHeader
                firstName={profile.firstName}
                lastName={profile.lastName}
                avatarUrl={profile.avatarUrl}
                coverUrl={profile.coverUrl}
                headline={profile.headline}
                city={profile.city}
                memberSince={profile.memberSince}
                isVerified={profile.isVerified}
                role={profile.role}
                isOwnProfile={isOwnProfile}
                onEditCover={onEditCover}
                onEditAvatar={onEditAvatar}
            />

            {/* Bio Section */}
            {profile.bio && (
                <div className="px-6 pb-4">
                    <p className="text-slate-600 leading-relaxed text-sm sm:text-base">
                        {profile.bio}
                    </p>
                </div>
            )}

            {/* Trust Stats Row */}
            <div className="border-t border-slate-100">
                <StatsRow
                    role={profile.role}
                    averageRating={profile.stats.averageRating}
                    totalReviews={profile.stats.totalReviews}
                    totalMissions={profile.stats.totalMissions}
                    reliabilityRate={profile.stats.reliabilityRate}
                    isAvailable={profile.stats.isAvailable}
                />
            </div>

            {/* Desktop Actions */}
            <div className="px-6 pb-6">
                <DesktopActions
                    role={profile.role}
                    isOwnProfile={isOwnProfile}
                    isFavorite={isFavorite}
                    onPrimaryAction={onPrimaryAction}
                    onMessageClick={onMessage}
                    onFavoriteToggle={onFavoriteToggle}
                    onShare={onShare}
                    onCall={profile.phone ? onCall : undefined}
                />
            </div>

            {/* Mobile Action Bar (Fixed Bottom) */}
            <MobileActionBar
                role={profile.role}
                isOwnProfile={isOwnProfile}
                isFavorite={isFavorite}
                onPrimaryAction={onPrimaryAction}
                onMessageClick={onMessage}
                onFavoriteToggle={onFavoriteToggle}
                onShare={onShare}
            />
        </div>
    );
}

// ============================================================
// DEMO: Example usage component for testing
// ============================================================

export function UserProfileDemo() {
    const [isFavorite, setIsFavorite] = useState(false);

    const mockProfile: UserProfileData = {
        id: 'usr_123',
        firstName: 'Marie',
        lastName: 'Dupont',
        email: 'marie.dupont@example.com',
        phone: '06 12 34 56 78',
        avatarUrl: null,
        coverUrl: null,
        headline: 'Éducatrice spécialisée • 10 ans d\'expérience en EHPAD et IME',
        bio: 'Passionnée par l\'accompagnement des personnes en situation de handicap. Spécialisée dans l\'autisme et les troubles du comportement. Diplômée DEES avec une certification en musicothérapie.',
        city: 'Lyon 3e',
        memberSince: new Date('2022-03-15'),
        isVerified: true,
        role: 'TALENT',
        stats: {
            averageRating: 4.9,
            totalReviews: 34,
            totalMissions: 47,
            reliabilityRate: 100,
            isAvailable: true,
        },
    };

    const mockClientProfile: UserProfileData = {
        id: 'usr_456',
        firstName: 'EHPAD',
        lastName: 'Les Jardins',
        email: 'contact@ehpad-jardins.fr',
        phone: '04 78 00 00 00',
        avatarUrl: null,
        coverUrl: null,
        headline: 'Établissement d\'hébergement pour personnes âgées dépendantes',
        bio: 'Notre EHPAD accueille 120 résidents dans un cadre verdoyant au cœur de Lyon. Nous recherchons régulièrement des professionnels qualifiés pour renforcer nos équipes.',
        city: 'Lyon 6e',
        memberSince: new Date('2021-09-01'),
        isVerified: true,
        role: 'CLIENT',
        stats: {
            averageRating: 4.7,
            totalReviews: 18,
            totalMissions: 156,
            reliabilityRate: 98,
            isAvailable: true,
        },
    };

    return (
        <div className="min-h-screen bg-slate-50 py-8 px-4">
            <div className="max-w-3xl mx-auto space-y-8">
                <h1 className="text-2xl font-bold text-slate-900 mb-6">
                    Démo Composants Profil
                </h1>

                {/* Freelancer Profile */}
                <div>
                    <h2 className="text-lg font-semibold text-slate-700 mb-4">
                        Profil Freelance (TALENT)
                    </h2>
                    <UserProfile
                        profile={mockProfile}
                        isFavorite={isFavorite}
                        onPrimaryAction={() => alert('Proposer une mission')}
                        onMessage={() => alert('Ouvrir messagerie')}
                        onFavoriteToggle={() => setIsFavorite(!isFavorite)}
                        onShare={() => alert('Partager le profil')}
                        onCall={() => alert('Appeler')}
                    />
                </div>

                {/* Client Profile */}
                <div>
                    <h2 className="text-lg font-semibold text-slate-700 mb-4">
                        Profil Établissement (Client)
                    </h2>
                    <UserProfile
                        profile={mockClientProfile}
                        onPrimaryAction={() => alert('Postuler')}
                        onMessage={() => alert('Ouvrir messagerie')}
                        onShare={() => alert('Partager le profil')}
                    />
                </div>

                {/* Own Profile */}
                <div>
                    <h2 className="text-lg font-semibold text-slate-700 mb-4">
                        Mon Profil (Vue propriétaire)
                    </h2>
                    <UserProfile
                        profile={mockProfile}
                        isOwnProfile={true}
                        onEditCover={() => alert('Modifier la couverture')}
                        onEditAvatar={() => alert('Modifier l\'avatar')}
                    />
                </div>
            </div>
        </div>
    );
}

