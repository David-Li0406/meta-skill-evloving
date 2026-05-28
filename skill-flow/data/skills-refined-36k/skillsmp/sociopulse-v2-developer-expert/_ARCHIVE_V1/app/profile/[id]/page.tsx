'use client';

import { useState, use } from 'react';
import { UserProfile, UserProfileData, ProfileContent, ProfileAboutData, ReviewItem } from '@/components/profile';
import { useRouter } from 'next/navigation';

// Mock Data Store
const MOCK_PROFILES: Record<string, Partial<UserProfileData>> = {
    '1': {
        firstName: 'Marie',
        lastName: 'Dupont',
        role: 'TALENT',
        headline: 'Éducatrice spécialisée • 10 ans d\'expérience',
        city: 'Lyon 3e'
    },
    '2': {
        firstName: 'Thomas',
        lastName: 'Martin',
        role: 'TALENT',
        headline: 'Coach Sportif Adapté',
        city: 'Toulouse'
    },
    '3': {
        firstName: 'Sophie',
        lastName: 'Laurent',
        role: 'TALENT',
        headline: 'Musicothérapeute certifiée',
        city: 'Paris 15e'
    }
};

export default function PublicProfilePage({ params }: { params: { id: string } }) {
    const { id } = params;
    const router = useRouter();
    const [isFavorite, setIsFavorite] = useState(false);

    // Get mock data or default
    const profileBase = MOCK_PROFILES[id] || {
        firstName: 'Utilisateur',
        lastName: 'Inconnu',
        role: 'TALENT',
        headline: 'Profil utilisateur',
        city: 'Non renseigné'
    };

    const mockProfile: UserProfileData = {
        id: id,
        firstName: profileBase.firstName!,
        lastName: profileBase.lastName!,
        email: 'contact@example.com',
        phone: '06 ** ** ** **',
        avatarUrl: null,
        coverUrl: null,
        headline: profileBase.headline,
        bio: null,
        city: profileBase.city,
        memberSince: new Date('2023-01-01'),
        isVerified: true,
        role: profileBase.role as 'TALENT' | 'CLIENT',
        stats: {
            averageRating: 4.8,
            totalReviews: 12,
            totalMissions: 24,
            reliabilityRate: 98,
            isAvailable: true,
        },
    };

    const aboutData: ProfileAboutData = {
        bio: `${profileBase.firstName} est un professionnel engagé sur Les TALENTs.`,
        specialties: ['Accompagnement', 'Soin', 'Animation'],
        diplomas: [
            { name: 'Diplôme certifié', year: 2020 }
        ],
        yearsExperience: '5+ ans',
        hourlyRate: 30,
        radiusKm: 20,
        isVideoEnabled: true,
    };

    const reviewsData: ReviewItem[] = [
        {
            id: 'r1',
            reviewerName: 'Client Vérifié',
            reviewerRole: 'Directeur EHPAD',
            rating: 5,
            comment: 'Excellent travail, très professionnel.',
            date: new Date('2024-11-15'),
            isVerifiedMission: true,
            missionTitle: 'Mission ponctuelle',
            helpfulCount: 2,
        }
    ];

    const handleMessage = () => {
        router.push(`/messages?recipientId=${id}`);
    };

    const handleShare = async () => {
        if (navigator.share) {
            try {
                await navigator.share({
                    title: `${mockProfile.firstName} ${mockProfile.lastName} - Les TALENTs`,
                    url: window.location.href,
                });
            } catch (err) { }
        } else {
            // fallback
        }
    };

    return (
        <div className="min-h-screen bg-slate-50 py-8 px-4 sm:px-6 lg:px-8 pb-24 md:pb-8">
            <div className="max-w-3xl mx-auto space-y-6">
                <UserProfile
                    profile={mockProfile}
                    isOwnProfile={false}
                    isFavorite={isFavorite}
                    onPrimaryAction={handleMessage}
                    onMessage={handleMessage}
                    onFavoriteToggle={() => setIsFavorite(!isFavorite)}
                    onShare={handleShare}
                />

                <ProfileContent
                    role={mockProfile.role}
                    userName={mockProfile.firstName}
                    isOwnProfile={false}
                    about={aboutData}
                    missions={[]} // Hide history for public/others for privacy or simplicity
                    reviews={reviewsData}
                    averageRating={mockProfile.stats.averageRating}
                    totalReviews={mockProfile.stats.totalReviews}
                />
            </div>
        </div>
    );
}

