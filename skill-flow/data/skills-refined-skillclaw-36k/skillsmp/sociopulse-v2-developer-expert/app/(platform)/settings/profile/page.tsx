'use client';

import { useState, useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Save,
    Loader2,
    AlertCircle,
    CheckCircle,
    User,
    Briefcase,
    FileText,
} from 'lucide-react';
import { ImageUploader, SkillsTagInput, AmenitiesSelector } from '@/components/settings';
import { ToastContainer, useToasts } from '@/components/ui/Toast';

// ===========================================
// TYPES
// ===========================================

type UserRole = 'FREELANCE' | 'CLIENT';

interface ProfileFormData {
    firstName: string;
    lastName: string;
    title: string;
    bio: string;
    city: string;
    phone: string;
    skills: string[];      // For Freelancers
    amenities: string[];   // For Clients
}

// ===========================================
// MOCK DATA (will be replaced by API)
// ===========================================

const MOCK_USER: ProfileFormData & { role: UserRole; avatarUrl?: string } = {
    role: 'FREELANCE', // Toggle to 'CLIENT' to see different fields
    firstName: 'Marie',
    lastName: 'Dupont',
    title: 'Infirmière Diplômée',
    bio: 'Infirmière expérimentée avec 10 ans de pratique en milieu hospitalier et EHPAD.',
    city: 'Lyon',
    phone: '06 12 34 56 78',
    skills: ['Soins infirmiers', 'Gériatrie', 'Urgences'],
    amenities: ['parking', 'meals'],
    avatarUrl: undefined,
};

// ===========================================
// CHARACTER COUNTER
// ===========================================

function CharacterCounter({ current, max }: { current: number; max: number }) {
    const percentage = (current / max) * 100;
    const isNearLimit = percentage > 80;
    const isAtLimit = current >= max;

    return (
        <div className="flex items-center gap-2 text-xs">
            <div className="flex-1 h-1 bg-slate-200 rounded-full overflow-hidden">
                <motion.div
                    className={`h-full rounded-full ${isAtLimit ? 'bg-red-500' : isNearLimit ? 'bg-amber-500' : 'bg-brand-600'
                        }`}
                    initial={false}
                    animate={{ width: `${Math.min(percentage, 100)}%` }}
                />
            </div>
            <span className={`font-medium ${isAtLimit ? 'text-red-500' : 'text-slate-400'}`}>
                {current}/{max}
            </span>
        </div>
    );
}

// ===========================================
// FLOATING SAVE BAR
// ===========================================

interface FloatingSaveBarProps {
    isDirty: boolean;
    isSubmitting: boolean;
    onSave: () => void;
    onReset: () => void;
}

function FloatingSaveBar({ isDirty, isSubmitting, onSave, onReset }: FloatingSaveBarProps) {
    return (
        <AnimatePresence>
            {isDirty && (
                <motion.div
                    initial={{ y: 100, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    exit={{ y: 100, opacity: 0 }}
                    transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                    className="fixed bottom-0 left-0 right-0 z-50 lg:left-64"
                >
                    <div className="bg-white/90 backdrop-blur-xl border-t border-slate-200 shadow-2xl">
                        <div className="max-w-2xl mx-auto px-4 py-4">
                            <div className="flex items-center justify-between gap-4">
                                <div className="flex items-center gap-2 text-amber-600">
                                    <AlertCircle className="w-5 h-5" />
                                    <span className="text-sm font-medium">
                                        Modifications non enregistrées
                                    </span>
                                </div>
                                <div className="flex items-center gap-3">
                                    <button
                                        type="button"
                                        onClick={onReset}
                                        disabled={isSubmitting}
                                        className="btn-secondary"
                                    >
                                        Annuler
                                    </button>
                                    <button
                                        type="button"
                                        onClick={onSave}
                                        disabled={isSubmitting}
                                        className="btn-primary"
                                    >
                                        {isSubmitting ? (
                                            <>
                                                <Loader2 className="w-4 h-4 animate-spin" />
                                                Enregistrement...
                                            </>
                                        ) : (
                                            <>
                                                <Save className="w-4 h-4" />
                                                Enregistrer
                                            </>
                                        )}
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
}

// ===========================================
// MAIN PAGE COMPONENT
// ===========================================

export default function EditProfilePage() {
    const [userRole] = useState<UserRole>(MOCK_USER.role);
    const [avatarFile, setAvatarFile] = useState<File | null>(null);
    const { toasts, addToast, removeToast } = useToasts();

    // React Hook Form
    const {
        register,
        control,
        handleSubmit,
        reset,
        watch,
        formState: { isDirty, isSubmitting, errors },
    } = useForm<ProfileFormData>({
        defaultValues: {
            firstName: MOCK_USER.firstName,
            lastName: MOCK_USER.lastName,
            title: MOCK_USER.title,
            bio: MOCK_USER.bio,
            city: MOCK_USER.city,
            phone: MOCK_USER.phone,
            skills: MOCK_USER.skills,
            amenities: MOCK_USER.amenities,
        },
    });

    const bioValue = watch('bio') || '';
    const BIO_MAX_LENGTH = 300;

    // Handle form submission
    const onSubmit = async (data: ProfileFormData) => {
        try {
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 1500));

            console.log('Saving profile:', data);
            console.log('Avatar file:', avatarFile);

            addToast({
                message: 'Profil mis à jour avec succès !',
                type: 'success',
            });

            // Reset dirty state
            reset(data);
        } catch (error) {
            addToast({
                message: 'Erreur lors de la sauvegarde',
                type: 'error',
            });
        }
    };

    // Reset form
    const handleReset = () => {
        reset();
        setAvatarFile(null);
    };

    return (
        <>
            <ToastContainer toasts={toasts} onRemove={removeToast} />

            {/* Page Header */}
            <div className="mb-6">
                <h2 className="text-2xl font-bold text-slate-900">Mon Profil</h2>
                <p className="text-slate-500 mt-1">
                    Gérez vos informations personnelles et professionnelles
                </p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
                {/* Avatar Section */}
                <section className="card-surface p-6">
                    <h3 className="text-lg font-semibold text-slate-900 mb-6 flex items-center gap-2">
                        <User className="w-5 h-5 text-brand-600" />
                        Photo de profil
                    </h3>
                    <div className="flex justify-center pb-8">
                        <ImageUploader
                            currentImageUrl={MOCK_USER.avatarUrl}
                            initials={`${MOCK_USER.firstName[0]}${MOCK_USER.lastName[0]}`}
                            onImageChange={setAvatarFile}
                            size="lg"
                        />
                    </div>
                </section>

                {/* Identity Section */}
                <section className="card-surface p-6">
                    <h3 className="text-lg font-semibold text-slate-900 mb-6 flex items-center gap-2">
                        <Briefcase className="w-5 h-5 text-brand-600" />
                        Identité
                    </h3>

                    <div className="grid gap-4 sm:grid-cols-2">
                        {/* First Name */}
                        <div>
                            <label htmlFor="firstName" className="block text-sm font-medium text-slate-700 mb-2">
                                Prénom
                            </label>
                            <input
                                id="firstName"
                                type="text"
                                {...register('firstName', { required: 'Prénom requis' })}
                                className={`input-premium ${errors.firstName ? 'border-red-500' : ''}`}
                            />
                            {errors.firstName && (
                                <p className="text-red-500 text-xs mt-1">{errors.firstName.message}</p>
                            )}
                        </div>

                        {/* Last Name */}
                        <div>
                            <label htmlFor="lastName" className="block text-sm font-medium text-slate-700 mb-2">
                                Nom
                            </label>
                            <input
                                id="lastName"
                                type="text"
                                {...register('lastName', { required: 'Nom requis' })}
                                className={`input-premium ${errors.lastName ? 'border-red-500' : ''}`}
                            />
                            {errors.lastName && (
                                <p className="text-red-500 text-xs mt-1">{errors.lastName.message}</p>
                            )}
                        </div>

                        {/* Title */}
                        <div>
                            <label htmlFor="title" className="block text-sm font-medium text-slate-700 mb-2">
                                Titre / Fonction
                            </label>
                            <input
                                id="title"
                                type="text"
                                placeholder="Ex: Infirmier, Éducateur spécialisé..."
                                {...register('title')}
                                className="input-premium"
                            />
                        </div>

                        {/* City */}
                        <div>
                            <label htmlFor="city" className="block text-sm font-medium text-slate-700 mb-2">
                                Ville
                            </label>
                            <input
                                id="city"
                                type="text"
                                placeholder="Ex: Lyon, Paris..."
                                {...register('city')}
                                className="input-premium"
                            />
                        </div>

                        {/* Phone */}
                        <div className="sm:col-span-2">
                            <label htmlFor="phone" className="block text-sm font-medium text-slate-700 mb-2">
                                Téléphone
                            </label>
                            <input
                                id="phone"
                                type="tel"
                                placeholder="06 12 34 56 78"
                                {...register('phone')}
                                className="input-premium"
                            />
                        </div>
                    </div>
                </section>

                {/* Bio Section */}
                <section className="card-surface p-6">
                    <h3 className="text-lg font-semibold text-slate-900 mb-6 flex items-center gap-2">
                        <FileText className="w-5 h-5 text-brand-600" />
                        Présentation
                    </h3>

                    <div>
                        <label htmlFor="bio" className="block text-sm font-medium text-slate-700 mb-2">
                            Bio
                        </label>
                        <textarea
                            id="bio"
                            rows={4}
                            placeholder="Décrivez votre parcours, vos compétences et ce qui vous distingue..."
                            {...register('bio', {
                                maxLength: {
                                    value: BIO_MAX_LENGTH,
                                    message: `Maximum ${BIO_MAX_LENGTH} caractères`,
                                },
                            })}
                            className={`input-premium resize-none ${errors.bio ? 'border-red-500' : ''}`}
                        />
                        <div className="mt-2">
                            <CharacterCounter current={bioValue.length} max={BIO_MAX_LENGTH} />
                        </div>
                        {errors.bio && (
                            <p className="text-red-500 text-xs mt-1">{errors.bio.message}</p>
                        )}
                    </div>
                </section>

                {/* Conditional Section: Skills (Freelance) or Amenities (Client) */}
                <section className="card-surface p-6">
                    {userRole === 'FREELANCE' ? (
                        <>
                            <h3 className="text-lg font-semibold text-slate-900 mb-6">
                                🎯 Compétences
                            </h3>
                            <p className="text-sm text-slate-500 mb-4">
                                Ajoutez vos compétences pour être mieux référencé
                            </p>
                            <Controller
                                name="skills"
                                control={control}
                                render={({ field }) => (
                                    <SkillsTagInput
                                        value={field.value}
                                        onChange={field.onChange}
                                        placeholder="Tapez une compétence puis Entrée..."
                                        maxTags={10}
                                    />
                                )}
                            />
                        </>
                    ) : (
                        <>
                            <h3 className="text-lg font-semibold text-slate-900 mb-6">
                                🏢 Équipements & Services
                            </h3>
                            <p className="text-sm text-slate-500 mb-4">
                                Indiquez les services disponibles dans votre établissement
                            </p>
                            <Controller
                                name="amenities"
                                control={control}
                                render={({ field }) => (
                                    <AmenitiesSelector
                                        value={field.value}
                                        onChange={field.onChange}
                                    />
                                )}
                            />
                        </>
                    )}
                </section>

                {/* Spacer for floating bar */}
                <div className="h-24" />
            </form>

            {/* Floating Save Bar */}
            <FloatingSaveBar
                isDirty={isDirty || avatarFile !== null}
                isSubmitting={isSubmitting}
                onSave={handleSubmit(onSubmit)}
                onReset={handleReset}
            />
        </>
    );
}
