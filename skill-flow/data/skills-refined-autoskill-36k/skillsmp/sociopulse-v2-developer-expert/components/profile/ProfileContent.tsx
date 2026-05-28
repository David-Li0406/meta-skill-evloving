'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
    User, 
    History, 
    Star,
    Award,
    MapPin,
    Briefcase,
    GraduationCap,
    Clock,
    Gift
} from 'lucide-react';
import { ProfileTabs, TabPanel, Tab } from './ProfileTabs';
import { MissionHistory, MissionHistoryItem } from './MissionHistory';
import { ReviewsList, ReviewItem } from './ReviewsList';
import { EmptyState } from './EmptyState';
import { SkillsTags, parseSkills, Skill } from './SkillsTags';
import { AmenitiesList, Amenity, parseAmenities } from './AmenitiesList';

export interface ProfileAboutData {
    bio?: string | null;
    /** For TALENT: skills/specialties as colored pills */
    specialties?: string[];
    /** For CLIENT: amenities/advantages with icons */
    amenities?: string[];
    diplomas?: Array<{ name: string; year?: number }>;
    yearsExperience?: string;
    hourlyRate?: number;
    radiusKm?: number;
    isVideoEnabled?: boolean;
    /** Establishment description (for CLIENT) */
    establishmentType?: string;
    /** Number of employees (for CLIENT) */
    employeeCount?: number;
}

export interface ProfileContentProps {
    /** User role */
    role: 'TALENT' | 'CLIENT' | 'ADMIN';
    /** User's first name for empty states */
    userName?: string;
    /** Whether viewing own profile */
    isOwnProfile?: boolean;
    /** About section data */
    about: ProfileAboutData;
    /** Mission history */
    missions: MissionHistoryItem[];
    /** Reviews list */
    reviews: ReviewItem[];
    /** Average rating */
    averageRating?: number;
    /** Total reviews count */
    totalReviews?: number;
    /** Callback for empty state actions */
    onEmptyAction?: (type: 'missions' | 'reviews') => void;
}

const TABS: Tab[] = [
    { id: 'about', label: 'Profil', icon: <User className="w-4 h-4" /> },
    { id: 'history', label: 'Historique', icon: <History className="w-4 h-4" /> },
    { id: 'reviews', label: 'Avis', icon: <Star className="w-4 h-4" /> },
];

interface AboutSectionProps {
    about: ProfileAboutData;
    role: 'TALENT' | 'CLIENT' | 'ADMIN';
    isOwnProfile?: boolean;
}

function AboutSection({ about, role, isOwnProfile }: AboutSectionProps) {
    // Parse skills for freelancers
    const skills: Skill[] = about.specialties 
        ? parseSkills(about.specialties, 3) // Highlight first 3
        : [];

    // Parse amenities for clients
    const amenities: Amenity[] = about.amenities
        ? parseAmenities(about.amenities)
        : [];

    const hasContent = about.bio || skills.length > 0 || amenities.length > 0 || 
        (about.diplomas && about.diplomas.length > 0);

    if (!hasContent) {
        return (
            <EmptyState
                type="profile"
                isOwnProfile={isOwnProfile}
            />
        );
    }

    return (
        <div className="py-6 px-4 sm:px-6 space-y-6">
            {/* Bio */}
            {about.bio && (
                <div>
                    <h3 className="text-sm font-semibold text-slate-900 mb-2 flex items-center gap-2">
                        <User className="w-4 h-4 text-slate-400" />
                        À propos
                    </h3>
                    <p className="text-sm text-slate-600 leading-relaxed">
                        {about.bio}
                    </p>
                </div>
            )}

            {/* === FREELANCER VIEW: Skills/Specialties as colored pills === */}
            {role === 'TALENT' && skills.length > 0 && (
                <div>
                    <h3 className="text-sm font-semibold text-slate-900 mb-3 flex items-center gap-2">
                        <Briefcase className="w-4 h-4 text-slate-400" />
                        Compétences & Spécialités
                    </h3>
                    <SkillsTags 
                        skills={skills} 
                        variant="pills"
                        animated={true}
                    />
                </div>
            )}

            {/* === CLIENT VIEW: Amenities/Advantages with icons === */}
            {role === 'CLIENT' && amenities.length > 0 && (
                <div>
                    <h3 className="text-sm font-semibold text-slate-900 mb-3 flex items-center gap-2">
                        <Gift className="w-4 h-4 text-slate-400" />
                        Avantages de l'établissement
                    </h3>
                    <AmenitiesList 
                        amenities={amenities}
                        variant="grid"
                    />
                </div>
            )}

            {/* Establishment Info (Client only) */}
            {role === 'CLIENT' && (about.establishmentType || about.employeeCount) && (
                <div className="grid grid-cols-2 gap-4">
                    {about.establishmentType && (
                        <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                            <div className="text-xs text-slate-500 mb-1">Type d'établissement</div>
                            <div className="text-sm font-semibold text-slate-900">
                                {about.establishmentType}
                            </div>
                        </div>
                    )}
                    {about.employeeCount && (
                        <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                            <div className="text-xs text-slate-500 mb-1">Effectif</div>
                            <div className="text-sm font-semibold text-slate-900">
                                {about.employeeCount} employés
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* Diplomas (Freelance) */}
            {role === 'TALENT' && about.diplomas && about.diplomas.length > 0 && (
                <div>
                    <h3 className="text-sm font-semibold text-slate-900 mb-3 flex items-center gap-2">
                        <GraduationCap className="w-4 h-4 text-slate-400" />
                        Diplômes & Certifications
                    </h3>
                    <div className="space-y-2">
                        {about.diplomas.map((diploma, index) => (
                            <div
                                key={index}
                                className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-100"
                            >
                                <div className="flex items-center gap-3">
                                    <div className="w-8 h-8 rounded-lg bg-blue-100 flex items-center justify-center">
                                        <Award className="w-4 h-4 text-blue-600" />
                                    </div>
                                    <span className="text-sm font-medium text-slate-700">
                                        {diploma.name}
                                    </span>
                                </div>
                                {diploma.year && (
                                    <span className="text-xs text-slate-400">
                                        {diploma.year}
                                    </span>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Experience & Rate (Freelance only) */}
            {role === 'TALENT' && (about.yearsExperience || about.hourlyRate || about.radiusKm) && (
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                    {about.yearsExperience && (
                        <div className="p-4 rounded-xl bg-slate-50 border border-slate-100 text-center">
                            <Clock className="w-5 h-5 text-slate-400 mx-auto mb-2" />
                            <div className="text-lg font-bold text-slate-900">
                                {about.yearsExperience}
                            </div>
                            <div className="text-xs text-slate-500">d'expérience</div>
                        </div>
                    )}
                    {about.hourlyRate && (
                        <div className="p-4 rounded-xl bg-brand-50 border border-brand-100 text-center">
                            <div className="text-lg font-bold text-brand-600">
                                {about.hourlyRate}€/h
                            </div>
                            <div className="text-xs text-brand-500">Taux horaire</div>
                        </div>
                    )}
                    {about.radiusKm && (
                        <div className="p-4 rounded-xl bg-slate-50 border border-slate-100 text-center">
                            <MapPin className="w-5 h-5 text-slate-400 mx-auto mb-2" />
                            <div className="text-lg font-bold text-slate-900">
                                {about.radiusKm} km
                            </div>
                            <div className="text-xs text-slate-500">Rayon d'intervention</div>
                        </div>
                    )}
                </div>
            )}

            {/* Video Coaching Badge */}
            {role === 'TALENT' && about.isVideoEnabled && (
                <div className="flex items-center gap-3 p-4 rounded-xl bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-100">
                    <div className="w-10 h-10 rounded-xl bg-purple-100 flex items-center justify-center">
                        <svg className="w-5 h-5 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                        </svg>
                    </div>
                    <div>
                        <div className="text-sm font-semibold text-purple-900">
                            Coaching Vidéo Disponible
                        </div>
                        <div className="text-xs text-purple-600">
                            Sessions en visioconférence possibles
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export function ProfileContent({
    role,
    userName,
    isOwnProfile = false,
    about,
    missions,
    reviews,
    averageRating,
    totalReviews,
    onEmptyAction,
}: ProfileContentProps) {
    const [activeTab, setActiveTab] = useState('about');

    // Add badge count to reviews tab
    const tabsWithBadges = TABS.map(tab => {
        if (tab.id === 'reviews' && reviews.length > 0) {
            return {
                ...tab,
                label: `Avis (${reviews.length})`,
            };
        }
        if (tab.id === 'history' && missions.length > 0) {
            return {
                ...tab,
                label: `Historique (${missions.length})`,
            };
        }
        return tab;
    });

    return (
        <div className="bg-white rounded-2xl shadow-soft border border-slate-100 overflow-hidden">
            {/* Tab Navigation */}
            <ProfileTabs
                tabs={tabsWithBadges}
                activeTab={activeTab}
                onTabChange={setActiveTab}
            />

            {/* Tab Content */}
            <AnimatePresence mode="wait">
                <TabPanel key="about" isActive={activeTab === 'about'}>
                    <AboutSection about={about} role={role} />
                </TabPanel>

                <TabPanel key="history" isActive={activeTab === 'history'}>
                    <MissionHistory 
                        missions={missions} 
                        role={role}
                        userName={userName}
                        isOwnProfile={isOwnProfile}
                        onEmptyAction={onEmptyAction ? () => onEmptyAction('missions') : undefined}
                    />
                </TabPanel>

                <TabPanel key="reviews" isActive={activeTab === 'reviews'}>
                    <ReviewsList 
                        reviews={reviews}
                        averageRating={averageRating}
                        totalReviews={totalReviews}
                        userName={userName}
                        isOwnProfile={isOwnProfile}
                        onEmptyAction={onEmptyAction ? () => onEmptyAction('reviews') : undefined}
                    />
                </TabPanel>
            </AnimatePresence>
        </div>
    );
}

