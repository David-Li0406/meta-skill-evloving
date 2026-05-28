'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    ArrowLeft,
    ArrowRight,
    Check,
    User,
    FileText,
    Upload,
    Loader2,
    CheckCircle
} from 'lucide-react';
import Link from 'next/link';
import { currentBrand } from '@/lib/brand';
import { getProfileSections } from '@/lib/formConfig';
import { DynamicForm } from '@/components/forms';

// =============================================================================
// COMPLETE ONBOARDING PAGE
// Multi-step wizard for full profile verification
// =============================================================================

type Step = 'profile' | 'documents' | 'review';

const STEPS: { id: Step; label: string; icon: typeof User }[] = [
    { id: 'profile', label: 'Informations', icon: User },
    { id: 'documents', label: 'Documents', icon: FileText },
    { id: 'review', label: 'Validation', icon: Check },
];

export default function CompleteOnboardingPage() {
    const [currentStep, setCurrentStep] = useState<Step>('profile');
    const [formData, setFormData] = useState<Record<string, any>>({});
    const [uploadedFiles, setUploadedFiles] = useState<{ diploma?: File; idCard?: File }>({});
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isComplete, setIsComplete] = useState(false);
    const [errors, setErrors] = useState<Record<string, string>>({});

    // Get form sections for current brand
    const profileSections = getProfileSections(currentBrand.mode);

    // Handle form field change
    const handleFieldChange = (name: string, value: any) => {
        setFormData(prev => ({ ...prev, [name]: value }));
        // Clear error when field is edited
        if (errors[name]) {
            setErrors(prev => {
                const { [name]: _, ...rest } = prev;
                return rest;
            });
        }
    };

    // Handle file upload
    const handleFileUpload = (type: 'diploma' | 'idCard', file: File | null) => {
        setUploadedFiles(prev => ({ ...prev, [type]: file || undefined }));
    };

    // Navigate steps
    const goToStep = (step: Step) => {
        setCurrentStep(step);
    };

    const goNext = () => {
        const stepIndex = STEPS.findIndex(s => s.id === currentStep);
        if (stepIndex < STEPS.length - 1) {
            setCurrentStep(STEPS[stepIndex + 1].id);
        }
    };

    const goPrev = () => {
        const stepIndex = STEPS.findIndex(s => s.id === currentStep);
        if (stepIndex > 0) {
            setCurrentStep(STEPS[stepIndex - 1].id);
        }
    };

    // Submit profile
    const handleSubmit = async () => {
        setIsSubmitting(true);

        try {
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 2000));

            // Success!
            setIsComplete(true);
        } catch (error) {
            console.error('Submission error:', error);
        } finally {
            setIsSubmitting(false);
        }
    };

    // Success state
    if (isComplete) {
        return (
            <div className="min-h-screen bg-canvas flex items-center justify-center p-4">
                <motion.div
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="bg-white rounded-theme-2xl shadow-soft-lg p-8 max-w-md w-full text-center"
                >
                    <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ type: 'spring', delay: 0.2 }}
                        className="w-20 h-20 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-6"
                    >
                        <CheckCircle className="w-10 h-10 text-green-600" />
                    </motion.div>

                    <h1 className="text-2xl font-bold text-slate-900 mb-2">
                        Profil complété ! 🎉
                    </h1>
                    <p className="text-slate-600 mb-6">
                        Vos documents sont en cours de vérification. Vous recevrez une notification dès validation.
                    </p>

                    <Link
                        href="/fil-pro"
                        className="inline-flex items-center gap-2 px-6 py-3 bg-primary-600 text-white font-semibold rounded-theme-lg hover:bg-primary-700 transition-colors"
                    >
                        Explorer les missions
                        <ArrowRight className="w-4 h-4" />
                    </Link>
                </motion.div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-canvas">
            {/* Header */}
            <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
                <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
                    <Link
                        href="/dashboard"
                        className="inline-flex items-center gap-2 text-slate-600 hover:text-slate-900"
                    >
                        <ArrowLeft className="w-5 h-5" />
                        <span className="hidden sm:inline">Retour</span>
                    </Link>

                    <h1 className="text-lg font-semibold text-slate-900">
                        Compléter mon profil
                    </h1>

                    <div className="w-20" /> {/* Spacer */}
                </div>

                {/* Step Indicator */}
                <div className="max-w-4xl mx-auto px-4 pb-4">
                    <div className="flex items-center justify-between">
                        {STEPS.map((step, index) => {
                            const isActive = step.id === currentStep;
                            const isPast = STEPS.findIndex(s => s.id === currentStep) > index;
                            const Icon = step.icon;

                            return (
                                <div key={step.id} className="flex items-center flex-1">
                                    <button
                                        onClick={() => isPast && goToStep(step.id)}
                                        disabled={!isPast}
                                        className={`
                      flex items-center gap-2 px-3 py-2 rounded-theme-lg transition-all
                      ${isActive ? 'bg-primary-100 text-primary-700' : ''}
                      ${isPast ? 'text-green-600 hover:bg-green-50 cursor-pointer' : ''}
                      ${!isActive && !isPast ? 'text-slate-400' : ''}
                    `}
                                    >
                                        <div className={`
                      w-8 h-8 rounded-full flex items-center justify-center
                      ${isActive ? 'bg-primary-600 text-white' : ''}
                      ${isPast ? 'bg-green-100 text-green-600' : ''}
                      ${!isActive && !isPast ? 'bg-slate-100 text-slate-400' : ''}
                    `}>
                                            {isPast ? <Check className="w-4 h-4" /> : <Icon className="w-4 h-4" />}
                                        </div>
                                        <span className="hidden sm:inline text-sm font-medium">
                                            {step.label}
                                        </span>
                                    </button>

                                    {index < STEPS.length - 1 && (
                                        <div className={`
                      flex-1 h-0.5 mx-2
                      ${isPast ? 'bg-green-300' : 'bg-slate-200'}
                    `} />
                                    )}
                                </div>
                            );
                        })}
                    </div>
                </div>
            </header>

            {/* Content */}
            <main className="max-w-4xl mx-auto px-4 py-8">
                <AnimatePresence mode="wait">
                    {/* Step 1: Profile Information */}
                    {currentStep === 'profile' && (
                        <motion.div
                            key="profile"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="bg-white rounded-theme-2xl shadow-soft p-6 sm:p-8"
                        >
                            <div className="mb-8">
                                <h2 className="text-xl font-bold text-slate-900 mb-2">
                                    Informations professionnelles
                                </h2>
                                <p className="text-slate-600">
                                    Ces informations sont nécessaires pour valider votre profil auprès des établissements.
                                </p>
                            </div>

                            <DynamicForm
                                sections={profileSections}
                                formData={formData}
                                onChange={handleFieldChange}
                                errors={errors}
                            />

                            <div className="mt-8 flex justify-end">
                                <button
                                    onClick={goNext}
                                    className="inline-flex items-center gap-2 px-6 py-3 bg-primary-600 text-white font-semibold rounded-theme-lg hover:bg-primary-700 transition-colors"
                                >
                                    Continuer
                                    <ArrowRight className="w-4 h-4" />
                                </button>
                            </div>
                        </motion.div>
                    )}

                    {/* Step 2: Documents Upload */}
                    {currentStep === 'documents' && (
                        <motion.div
                            key="documents"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="bg-white rounded-theme-2xl shadow-soft p-6 sm:p-8"
                        >
                            <div className="mb-8">
                                <h2 className="text-xl font-bold text-slate-900 mb-2">
                                    Documents justificatifs
                                </h2>
                                <p className="text-slate-600">
                                    Téléchargez vos documents pour vérification. Formats acceptés : PDF, JPG, PNG (max 5MB).
                                </p>
                            </div>

                            <div className="space-y-6">
                                {/* Diploma Upload */}
                                <FileUploadBox
                                    label="Diplôme / Attestation de formation"
                                    description="Votre diplôme d'État ou attestation équivalente"
                                    file={uploadedFiles.diploma}
                                    onUpload={(file) => handleFileUpload('diploma', file)}
                                    required
                                />

                                {/* ID Card Upload */}
                                <FileUploadBox
                                    label="Pièce d'identité"
                                    description="Carte d'identité ou passeport (recto/verso)"
                                    file={uploadedFiles.idCard}
                                    onUpload={(file) => handleFileUpload('idCard', file)}
                                    required
                                />
                            </div>

                            <div className="mt-8 flex justify-between">
                                <button
                                    onClick={goPrev}
                                    className="inline-flex items-center gap-2 px-6 py-3 border border-slate-200 text-slate-700 font-medium rounded-theme-lg hover:bg-slate-50 transition-colors"
                                >
                                    <ArrowLeft className="w-4 h-4" />
                                    Retour
                                </button>
                                <button
                                    onClick={goNext}
                                    className="inline-flex items-center gap-2 px-6 py-3 bg-primary-600 text-white font-semibold rounded-theme-lg hover:bg-primary-700 transition-colors"
                                >
                                    Continuer
                                    <ArrowRight className="w-4 h-4" />
                                </button>
                            </div>
                        </motion.div>
                    )}

                    {/* Step 3: Review & Submit */}
                    {currentStep === 'review' && (
                        <motion.div
                            key="review"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="bg-white rounded-theme-2xl shadow-soft p-6 sm:p-8"
                        >
                            <div className="mb-8">
                                <h2 className="text-xl font-bold text-slate-900 mb-2">
                                    Vérification finale
                                </h2>
                                <p className="text-slate-600">
                                    Relisez vos informations avant de soumettre votre profil pour validation.
                                </p>
                            </div>

                            {/* Summary */}
                            <div className="space-y-4 mb-8">
                                <div className="p-4 bg-slate-50 rounded-theme-lg">
                                    <h4 className="text-sm font-semibold text-slate-700 mb-2">
                                        📋 Informations personnelles
                                    </h4>
                                    <p className="text-sm text-slate-600">
                                        {formData.firstName || 'Non renseigné'} {formData.lastName || ''} • {formData.phone || 'Téléphone non renseigné'}
                                    </p>
                                </div>

                                <div className="p-4 bg-slate-50 rounded-theme-lg">
                                    <h4 className="text-sm font-semibold text-slate-700 mb-2">
                                        🎓 Diplôme
                                    </h4>
                                    <p className="text-sm text-slate-600">
                                        {formData.diploma || 'Non renseigné'} ({formData.diplomaYear || '—'})
                                    </p>
                                </div>

                                <div className="p-4 bg-slate-50 rounded-theme-lg">
                                    <h4 className="text-sm font-semibold text-slate-700 mb-2">
                                        📎 Documents
                                    </h4>
                                    <p className="text-sm text-slate-600">
                                        {uploadedFiles.diploma ? '✓ Diplôme' : '✗ Diplôme manquant'} •{' '}
                                        {uploadedFiles.idCard ? '✓ Pièce d\'identité' : '✗ ID manquant'}
                                    </p>
                                </div>
                            </div>

                            {/* Terms */}
                            <div className="p-4 border border-slate-200 rounded-theme-lg mb-8">
                                <label className="flex items-start gap-3 cursor-pointer">
                                    <input
                                        type="checkbox"
                                        className="mt-1 w-4 h-4 text-primary-600 rounded"
                                    />
                                    <span className="text-sm text-slate-600">
                                        Je certifie que les informations fournies sont exactes et j'accepte les{' '}
                                        <Link href="/legal/terms" className="text-primary-600 hover:underline">
                                            conditions générales
                                        </Link>{' '}
                                        et la{' '}
                                        <Link href="/legal/privacy" className="text-primary-600 hover:underline">
                                            politique de confidentialité
                                        </Link>.
                                    </span>
                                </label>
                            </div>

                            <div className="flex justify-between">
                                <button
                                    onClick={goPrev}
                                    className="inline-flex items-center gap-2 px-6 py-3 border border-slate-200 text-slate-700 font-medium rounded-theme-lg hover:bg-slate-50 transition-colors"
                                >
                                    <ArrowLeft className="w-4 h-4" />
                                    Retour
                                </button>
                                <button
                                    onClick={handleSubmit}
                                    disabled={isSubmitting}
                                    className="inline-flex items-center gap-2 px-8 py-3 bg-green-600 text-white font-semibold rounded-theme-lg hover:bg-green-700 transition-colors disabled:opacity-50"
                                >
                                    {isSubmitting ? (
                                        <>
                                            <Loader2 className="w-4 h-4 animate-spin" />
                                            Envoi...
                                        </>
                                    ) : (
                                        <>
                                            Soumettre mon profil
                                            <Check className="w-4 h-4" />
                                        </>
                                    )}
                                </button>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </main>
        </div>
    );
}

// =============================================================================
// FILE UPLOAD BOX COMPONENT
// =============================================================================

interface FileUploadBoxProps {
    label: string;
    description: string;
    file?: File;
    onUpload: (file: File | null) => void;
    required?: boolean;
}

function FileUploadBox({ label, description, file, onUpload, required }: FileUploadBoxProps) {
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files?.[0];
        if (selectedFile) {
            onUpload(selectedFile);
        }
    };

    return (
        <div className="border-2 border-dashed border-slate-200 rounded-theme-lg p-6 hover:border-primary-300 transition-colors">
            <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-theme-lg bg-primary-100 flex items-center justify-center flex-shrink-0">
                    <Upload className="w-6 h-6 text-primary-600" />
                </div>
                <div className="flex-1">
                    <h4 className="font-medium text-slate-900">
                        {label}
                        {required && <span className="text-red-500 ml-1">*</span>}
                    </h4>
                    <p className="text-sm text-slate-500 mt-1">{description}</p>

                    {file ? (
                        <div className="mt-3 flex items-center gap-2 px-3 py-2 bg-green-50 rounded-theme-md">
                            <Check className="w-4 h-4 text-green-600" />
                            <span className="text-sm text-green-700 truncate">{file.name}</span>
                            <button
                                onClick={() => onUpload(null)}
                                className="ml-auto text-sm text-red-500 hover:text-red-700"
                            >
                                Supprimer
                            </button>
                        </div>
                    ) : (
                        <label className="mt-3 inline-flex items-center gap-2 px-4 py-2 bg-primary-50 text-primary-700 rounded-theme-md text-sm font-medium cursor-pointer hover:bg-primary-100 transition-colors">
                            <Upload className="w-4 h-4" />
                            Choisir un fichier
                            <input
                                type="file"
                                accept=".pdf,.jpg,.jpeg,.png"
                                onChange={handleChange}
                                className="hidden"
                            />
                        </label>
                    )}
                </div>
            </div>
        </div>
    );
}
