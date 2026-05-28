'use client';

import { useState } from 'react';
import { UserProfile, UserProfileData, ProfileContent, ProfileAboutData, MissionHistoryItem, ReviewItem } from '@/components/profile';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/useAuth';
import { Loader2 } from 'lucide-react';
import { Button } from '@/components/ui';

export default function ProfilePage() {
    const router = useRouter();
    const { user, isLoading, isAuthenticated } = useAuth();
    const [isFavorite, setIsFavorite] = useState(false);

    // Show loading state
    if (isLoading) {
        return (
            <div className="min-h-screen bg-canvas flex items-center justify-center">
                <div className="text-center space-y-4">
                    <Loader2 className="w-8 h-8 animate-spin text-primary-600 mx-auto" />
                    <p className="text-slate-500">Chargement du profil...</p>
                </div>
            </div>
        );
    }

    // Redirect if not authenticated
    if (!isAuthenticated || !user) {
        router.push('/auth/login');
        return null;
    }

    const isOwnProfile = true; // This is the current user's profile page

    // Build profile data from API response
    const profileData: UserProfileData = {
        id: user.id,
        firstName: user.profile?.firstName || user.email.split('@')[0],
        lastName: user.profile?.lastName || '',
        email: user.email,
        phone: user.phone || '',
        avatarUrl: user.profile?.avatarUrl || null,
        coverUrl: user.profile?.coverUrl || null,
        headline: user.profile?.headline || `${user.role === 'TALENT' ? 'Professionnel' : user.role === 'CLIENT' ? 'Établissement' : 'Administrateur'} Les TALENTs`,
        bio: user.profile?.bio || null,
        city: user.profile?.city || '',
        memberSince: new Date(user.createdAt),
        isVerified: user.status === 'VERIFIED',
        role: user.role,
        stats: {
            averageRating: 0, // TODO: fetch from reviews
            totalReviews: 0,
            totalMissions: 0,
            reliabilityRate: 100,
            isAvailable: true,
        },
    };

    // About section data from API
    const aboutData: ProfileAboutData = {
        bio: user.profile?.bio || 'Aucune bio renseignée. Modifiez votre profil pour en ajouter une.',
        specialties: user.profile?.specialties || [],
        diplomas: user.profile?.diplomas || [],
        yearsExperience: '',
        hourlyRate: user.profile?.hourlyRate || 0,
        radiusKm: user.profile?.radiusKm || 0,
        isVideoEnabled: user.profile?.isVideoEnabled || false,
    };

    // Mission history - TODO: fetch from API
    const missionsHistory: MissionHistoryItem[] = [];

    // Reviews - TODO: fetch from API
    const reviewsData: ReviewItem[] = [];

    const handlePrimaryAction = () => {
        router.push('/dashboard/relief');
    };

    const handleMessage = () => {
        router.push('/messages');
    };

    const handleShare = async () => {
        if (navigator.share) {
            try {
                await navigator.share({
                    title: `${profileData.firstName} ${profileData.lastName} - Les TALENTs`,
                    url: window.location.href,
                });
            } catch (err) {
                // User cancelled share
            }
        } else {
            await navigator.clipboard.writeText(window.location.href);
            alert('Lien copié dans le presse-papier');
        }
    };

    const handleEditCover = () => {
        console.log('Edit cover');
    };

    const handleEditAvatar = () => {
        console.log('Edit avatar');
    };

    return (
        <div className="min-h-screen bg-canvas py-8 px-4 sm:px-6 lg:px-8 pb-24 md:pb-8">
            <div className="max-w-3xl mx-auto space-y-6">
                {/* Profile Header Card */}
                <UserProfile
                    profile={profileData}
                    isOwnProfile={isOwnProfile}
                    isFavorite={isFavorite}
                    onPrimaryAction={handlePrimaryAction}
                    onMessage={handleMessage}
                    onFavoriteToggle={() => setIsFavorite(!isFavorite)}
                    onShare={handleShare}
                    onEditCover={handleEditCover}
                    onEditAvatar={handleEditAvatar}
                />

                {/* Profile Content Tabs */}
                <ProfileContent
                    role={profileData.role}
                    userName={profileData.firstName}
                    isOwnProfile={isOwnProfile}
                    about={aboutData}
                    missions={missionsHistory}
                    reviews={reviewsData}
                    averageRating={profileData.stats.averageRating}
                    totalReviews={profileData.stats.totalReviews}
                    onEmptyAction={(type) => {
                        if (type === 'missions') router.push('/dashboard/relief');
                        if (type === 'reviews') router.push('/profile');
                    }}
                />

                {/* Additional Sections for Own Profile */}
                {isOwnProfile && (
                    <div className="bg-white rounded-theme-xl shadow-soft p-6 border border-slate-100">
                        <h3 className="font-semibold text-slate-900 mb-4">
                            Actions rapides
                        </h3>
                        <div className="grid grid-cols-2 gap-3">
                            <Button
                                variant="default"
                                onClick={() => router.push('/dashboard/relief')}
                                className="justify-start"
                            >
                                Trouver une mission
                            </Button>
                            <Button
                                variant="secondary"
                                onClick={() => router.push('/messages')}
                                className="justify-start"
                            >
                                Voir mes messages
                            </Button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
