'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    AlertCircle,
    Clock,
    Users,
    Calendar,
    MapPin,
    ChevronRight,
    Loader2,
    CheckCircle,
    Zap
} from 'lucide-react';

// ===========================================
// TYPES
// ===========================================

type UrgencyLevel = 'MEDIUM' | 'HIGH' | 'CRITICAL';
type JobCategory = 'AIDE_SOIGNANT' | 'INFIRMIER' | 'EDUCATEUR' | 'AMP' | 'ASH' | 'OTHER';

interface SOSFormData {
    urgencyLevel: UrgencyLevel | null;
    jobCategory: JobCategory | null;
    numberOfPeople: number;
    date: string;
    city: string;
    additionalNotes: string;
}

// ===========================================
// CARD SELECTOR COMPONENT
// ===========================================

interface SelectorCardProps {
    icon: React.ReactNode;
    title: string;
    description: string;
    isSelected: boolean;
    onClick: () => void;
    accentColor?: 'amber' | 'orange' | 'red' | 'coral';
}

function SelectorCard({
    icon,
    title,
    description,
    isSelected,
    onClick,
    accentColor = 'coral'
}: SelectorCardProps) {
    const colorMap = {
        amber: 'border-amber-400 bg-amber-50 ring-amber-200',
        orange: 'border-orange-400 bg-orange-50 ring-orange-200',
        red: 'border-red-500 bg-red-50 ring-red-200',
        coral: 'border-rose-500 bg-rose-50 ring-rose-200',
    };

    const iconColorMap = {
        amber: 'text-amber-600',
        orange: 'text-orange-600',
        red: 'text-red-600',
        coral: 'text-rose-600',
    };

    return (
        <motion.button
            whileHover={{ scale: 1.02, y: -2 }}
            whileTap={{ scale: 0.98 }}
            onClick={onClick}
            className={`
                relative flex flex-col items-center p-6 rounded-2xl border-2 
                transition-all duration-300 cursor-pointer text-center
                ${isSelected
                    ? `${colorMap[accentColor]} ring-4`
                    : 'border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50'
                }
            `}
        >
            {/* Selection Indicator */}
            <AnimatePresence>
                {isSelected && (
                    <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        exit={{ scale: 0 }}
                        className="absolute -top-2 -right-2 w-6 h-6 rounded-full bg-rose-500 text-white flex items-center justify-center"
                    >
                        <CheckCircle className="w-4 h-4" />
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Icon */}
            <div className={`mb-3 ${isSelected ? iconColorMap[accentColor] : 'text-slate-400'}`}>
                {icon}
            </div>

            {/* Title */}
            <h3 className={`font-semibold text-sm mb-1 ${isSelected ? 'text-slate-900' : 'text-slate-700'}`}>
                {title}
            </h3>

            {/* Description */}
            <p className="text-xs text-slate-500">
                {description}
            </p>
        </motion.button>
    );
}

// ===========================================
// PULSING SOS ICON
// ===========================================

function PulsingSosIcon() {
    return (
        <motion.div
            className="relative w-24 h-24 mx-auto mb-6"
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.5 }}
        >
            {/* Outer Pulse Ring */}
            <motion.div
                className="absolute inset-0 rounded-full bg-rose-200"
                animate={{
                    scale: [1, 1.5, 1],
                    opacity: [0.6, 0, 0.6],
                }}
                transition={{
                    duration: 2,
                    repeat: Infinity,
                    ease: "easeInOut",
                }}
            />
            {/* Middle Pulse Ring */}
            <motion.div
                className="absolute inset-2 rounded-full bg-rose-300"
                animate={{
                    scale: [1, 1.3, 1],
                    opacity: [0.7, 0.2, 0.7],
                }}
                transition={{
                    duration: 2,
                    repeat: Infinity,
                    ease: "easeInOut",
                    delay: 0.3,
                }}
            />
            {/* Core Icon */}
            <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-rose-500 to-rose-600 rounded-full shadow-lg">
                <Zap className="w-10 h-10 text-white" />
            </div>
        </motion.div>
    );
}

// ===========================================
// MAIN SOS PAGE
// ===========================================

export default function SOSPage() {
    const [formData, setFormData] = useState<SOSFormData>({
        urgencyLevel: null,
        jobCategory: null,
        numberOfPeople: 1,
        date: '',
        city: '',
        additionalNotes: '',
    });
    const [step, setStep] = useState(1);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isSuccess, setIsSuccess] = useState(false);

    const urgencyOptions: { value: UrgencyLevel; icon: React.ReactNode; title: string; description: string; color: 'amber' | 'orange' | 'red' }[] = [
        { value: 'MEDIUM', icon: <Clock className="w-8 h-8" />, title: 'Sous 48h', description: 'Planning flexible', color: 'amber' },
        { value: 'HIGH', icon: <AlertCircle className="w-8 h-8" />, title: 'Sous 24h', description: 'Besoin rapide', color: 'orange' },
        { value: 'CRITICAL', icon: <Zap className="w-8 h-8" />, title: 'Immédiat', description: 'Urgence absolue', color: 'red' },
    ];

    const jobOptions: { value: JobCategory; title: string; description: string }[] = [
        { value: 'AIDE_SOIGNANT', title: 'Aide-Soignant(e)', description: 'AS / ASD' },
        { value: 'INFIRMIER', title: 'Infirmier(ère)', description: 'IDE / IDEC' },
        { value: 'EDUCATEUR', title: 'Éducateur(trice)', description: 'ES / ME / AES' },
        { value: 'AMP', title: 'AMP / AES', description: 'Accompagnement' },
        { value: 'ASH', title: 'ASH', description: 'Services hôteliers' },
        { value: 'OTHER', title: 'Autre', description: 'Autre profil' },
    ];

    const handleSubmit = async () => {
        setIsSubmitting(true);
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 2000));
        setIsSubmitting(false);
        setIsSuccess(true);
    };

    const isStepValid = () => {
        if (step === 1) return formData.urgencyLevel !== null;
        if (step === 2) return formData.jobCategory !== null;
        if (step === 3) return formData.date && formData.city;
        return true;
    };

    const nextStep = () => {
        if (step < 4 && isStepValid()) {
            setStep(step + 1);
        }
    };

    // Success State
    if (isSuccess) {
        return (
            <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
                <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="bg-white rounded-3xl p-8 shadow-xl text-center max-w-md"
                >
                    <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: 0.2, type: 'spring' }}
                        className="w-20 h-20 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-6"
                    >
                        <CheckCircle className="w-10 h-10 text-green-600" />
                    </motion.div>
                    <h1 className="text-2xl font-bold text-slate-900 mb-2">SOS Envoyé !</h1>
                    <p className="text-slate-600 mb-6">
                        Votre demande de renfort a été transmise. Nos équipes vous contactent sous peu.
                    </p>
                    <a href="/fil-pro" className="btn-primary w-full">
                        Retour au fil d'actualité
                    </a>
                </motion.div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-slate-50">
            {/* Header */}
            <div className="bg-gradient-to-br from-rose-500 to-rose-600 text-white pt-12 pb-16 px-4">
                <div className="max-w-2xl mx-auto text-center">
                    <PulsingSosIcon />
                    <h1 className="text-3xl font-bold mb-2">SOS Renfort</h1>
                    <p className="text-rose-100 text-lg">
                        Trouvez un professionnel en urgence
                    </p>
                </div>
            </div>

            {/* Form Container */}
            <div className="max-w-2xl mx-auto px-4 -mt-8">
                <div className="bg-white rounded-3xl shadow-xl p-6 sm:p-8">
                    {/* Progress Bar */}
                    <div className="flex gap-2 mb-8">
                        {[1, 2, 3, 4].map((s) => (
                            <div
                                key={s}
                                className={`h-1.5 rounded-full flex-1 transition-colors ${s <= step ? 'bg-rose-500' : 'bg-slate-200'
                                    }`}
                            />
                        ))}
                    </div>

                    {/* Step Content */}
                    <AnimatePresence mode="wait">
                        {/* Step 1: Urgency Level */}
                        {step === 1 && (
                            <motion.div
                                key="step1"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                            >
                                <h2 className="text-xl font-bold text-slate-900 mb-2">
                                    Niveau d'urgence
                                </h2>
                                <p className="text-slate-500 mb-6">
                                    Dans quel délai avez-vous besoin de renfort ?
                                </p>
                                <div className="grid grid-cols-3 gap-4">
                                    {urgencyOptions.map((option) => (
                                        <SelectorCard
                                            key={option.value}
                                            icon={option.icon}
                                            title={option.title}
                                            description={option.description}
                                            isSelected={formData.urgencyLevel === option.value}
                                            onClick={() => setFormData({ ...formData, urgencyLevel: option.value })}
                                            accentColor={option.color}
                                        />
                                    ))}
                                </div>
                            </motion.div>
                        )}

                        {/* Step 2: Job Category */}
                        {step === 2 && (
                            <motion.div
                                key="step2"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                            >
                                <h2 className="text-xl font-bold text-slate-900 mb-2">
                                    Type de professionnel
                                </h2>
                                <p className="text-slate-500 mb-6">
                                    Quel profil recherchez-vous ?
                                </p>
                                <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                                    {jobOptions.map((option) => (
                                        <SelectorCard
                                            key={option.value}
                                            icon={<Users className="w-6 h-6" />}
                                            title={option.title}
                                            description={option.description}
                                            isSelected={formData.jobCategory === option.value}
                                            onClick={() => setFormData({ ...formData, jobCategory: option.value })}
                                        />
                                    ))}
                                </div>
                            </motion.div>
                        )}

                        {/* Step 3: Details */}
                        {step === 3 && (
                            <motion.div
                                key="step3"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                            >
                                <h2 className="text-xl font-bold text-slate-900 mb-2">
                                    Détails de la mission
                                </h2>
                                <p className="text-slate-500 mb-6">
                                    Précisez les informations pratiques
                                </p>
                                <div className="space-y-4">
                                    {/* Date */}
                                    <div>
                                        <label htmlFor="sos-date" className="label-sm block mb-2">
                                            <Calendar className="w-4 h-4 inline mr-1" />
                                            Date de début
                                        </label>
                                        <input
                                            id="sos-date"
                                            type="date"
                                            value={formData.date}
                                            onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                                            className="input-premium"
                                        />
                                    </div>

                                    {/* City */}
                                    <div>
                                        <label className="label-sm block mb-2">
                                            <MapPin className="w-4 h-4 inline mr-1" />
                                            Ville
                                        </label>
                                        <input
                                            type="text"
                                            value={formData.city}
                                            onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                                            placeholder="Ex: Lyon, Paris..."
                                            className="input-premium"
                                        />
                                    </div>

                                    {/* Number of People */}
                                    <div>
                                        <label className="label-sm block mb-2">
                                            <Users className="w-4 h-4 inline mr-1" />
                                            Nombre de personnes
                                        </label>
                                        <div className="flex items-center gap-4">
                                            <button
                                                type="button"
                                                onClick={() => setFormData({ ...formData, numberOfPeople: Math.max(1, formData.numberOfPeople - 1) })}
                                                className="btn-secondary w-12 h-12 !p-0"
                                            >
                                                -
                                            </button>
                                            <span className="text-2xl font-bold text-slate-900 w-12 text-center">
                                                {formData.numberOfPeople}
                                            </span>
                                            <button
                                                type="button"
                                                onClick={() => setFormData({ ...formData, numberOfPeople: formData.numberOfPeople + 1 })}
                                                className="btn-secondary w-12 h-12 !p-0"
                                            >
                                                +
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </motion.div>
                        )}

                        {/* Step 4: Confirmation */}
                        {step === 4 && (
                            <motion.div
                                key="step4"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                            >
                                <h2 className="text-xl font-bold text-slate-900 mb-2">
                                    Récapitulatif
                                </h2>
                                <p className="text-slate-500 mb-6">
                                    Vérifiez les informations avant envoi
                                </p>

                                <div className="bg-slate-50 rounded-2xl p-6 space-y-4">
                                    <div className="flex justify-between">
                                        <span className="text-slate-500">Urgence</span>
                                        <span className="font-semibold text-slate-900">
                                            {urgencyOptions.find(o => o.value === formData.urgencyLevel)?.title}
                                        </span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-slate-500">Profil</span>
                                        <span className="font-semibold text-slate-900">
                                            {jobOptions.find(o => o.value === formData.jobCategory)?.title}
                                        </span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-slate-500">Date</span>
                                        <span className="font-semibold text-slate-900">
                                            {new Date(formData.date).toLocaleDateString('fr-FR')}
                                        </span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-slate-500">Ville</span>
                                        <span className="font-semibold text-slate-900">{formData.city}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-slate-500">Personnes</span>
                                        <span className="font-semibold text-slate-900">{formData.numberOfPeople}</span>
                                    </div>
                                </div>

                                {/* Additional Notes */}
                                <div className="mt-6">
                                    <label className="label-sm block mb-2">Notes additionnelles (optionnel)</label>
                                    <textarea
                                        value={formData.additionalNotes}
                                        onChange={(e) => setFormData({ ...formData, additionalNotes: e.target.value })}
                                        placeholder="Informations complémentaires..."
                                        rows={3}
                                        className="input-premium resize-none"
                                    />
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>

                    {/* Navigation */}
                    <div className="flex gap-4 mt-8">
                        {step > 1 && (
                            <button
                                type="button"
                                onClick={() => setStep(step - 1)}
                                className="btn-secondary flex-1"
                            >
                                Retour
                            </button>
                        )}
                        {step < 4 ? (
                            <motion.button
                                whileHover={{ scale: 1.02 }}
                                whileTap={{ scale: 0.98 }}
                                type="button"
                                onClick={nextStep}
                                disabled={!isStepValid()}
                                className={`btn-primary flex-1 ${!isStepValid() ? 'opacity-50 cursor-not-allowed' : ''}`}
                            >
                                Continuer
                                <ChevronRight className="w-4 h-4" />
                            </motion.button>
                        ) : (
                            <motion.button
                                whileHover={{ scale: 1.02 }}
                                whileTap={{ scale: 0.98 }}
                                type="button"
                                onClick={handleSubmit}
                                disabled={isSubmitting}
                                className="btn-primary flex-1"
                            >
                                {isSubmitting ? (
                                    <>
                                        <Loader2 className="w-4 h-4 animate-spin" />
                                        Envoi en cours...
                                    </>
                                ) : (
                                    <>
                                        <Zap className="w-4 h-4" />
                                        Envoyer le SOS
                                    </>
                                )}
                            </motion.button>
                        )}
                    </div>
                </div>
            </div>

            {/* Bottom Spacing */}
            <div className="h-8" />
        </div>
    );
}
