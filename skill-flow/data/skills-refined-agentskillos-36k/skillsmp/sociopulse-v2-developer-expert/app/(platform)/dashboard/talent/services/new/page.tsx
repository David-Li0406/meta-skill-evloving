'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import {
    ArrowLeft,
    User,
    Users,
    Euro,
    Clock,
    FileText,
    Sparkles,
    CheckCircle2,
} from 'lucide-react';
import { Button, Input, Badge } from '@/components/ui';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';

// =============================================================================
// TYPES
// =============================================================================

type ServiceType = 'ONE_TO_ONE' | 'GROUP' | null;
type Duration = 30 | 60 | 90;

interface ServiceForm {
    title: string;
    description: string;
    price: string;
    duration: Duration;
}

// =============================================================================
// PAGE
// =============================================================================

export default function ServiceCreatorPage() {
    const router = useRouter();
    const [selectedType, setSelectedType] = useState<ServiceType>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [form, setForm] = useState<ServiceForm>({
        title: '',
        description: '',
        price: '',
        duration: 60,
    });

    const durations: { value: Duration; label: string }[] = [
        { value: 30, label: '30 min' },
        { value: 60, label: '60 min' },
        { value: 90, label: '90 min' },
    ];

    const handleSelectType = (type: ServiceType) => {
        if (type === 'GROUP') return; // Disabled
        setSelectedType(type);
    };

    const handleInputChange = (field: keyof ServiceForm, value: string | number) => {
        setForm(prev => ({ ...prev, [field]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!form.title.trim()) {
            toast.error('Veuillez entrer un titre pour votre service');
            return;
        }

        if (!form.price || parseFloat(form.price) <= 0) {
            toast.error('Veuillez entrer un prix valide');
            return;
        }

        setIsSubmitting(true);

        try {
            // TODO: API call to create service
            await new Promise(resolve => setTimeout(resolve, 1500));

            toast.success('Service créé avec succès !', {
                description: 'Votre service est maintenant visible sur votre profil.',
            });

            router.push('/dashboard/talent/services');
        } catch (error) {
            toast.error('Erreur lors de la création du service');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-teal-50/30">
            <div className="max-w-4xl mx-auto px-4 py-8 sm:py-12">
                {/* Back Button */}
                <Link
                    href="/dashboard/talent/services"
                    className="inline-flex items-center gap-2 text-slate-600 hover:text-slate-900 mb-8 group transition-colors"
                >
                    <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
                    <span className="text-sm font-medium">Retour aux services</span>
                </Link>

                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                    className="text-center mb-10"
                >
                    <div className="inline-flex items-center gap-2 px-4 py-2 bg-teal-50 rounded-full mb-4">
                        <Sparkles className="w-4 h-4 text-teal-600" />
                        <span className="text-sm font-medium text-teal-700">SocioLive</span>
                    </div>
                    <h1 className="text-3xl sm:text-4xl font-bold text-slate-900 mb-3">
                        Créer un nouveau service
                    </h1>
                    <p className="text-lg text-slate-600 max-w-xl mx-auto">
                        Partagez votre expertise via SocioLive.
                    </p>
                </motion.div>

                {/* Selection Grid */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.1 }}
                    className="grid sm:grid-cols-2 gap-6 mb-10"
                >
                    {/* Card A: Coaching / Supervision (Active) */}
                    <motion.button
                        onClick={() => handleSelectType('ONE_TO_ONE')}
                        whileHover={{ scale: 1.02, y: -4 }}
                        whileTap={{ scale: 0.98 }}
                        className={cn(
                            'relative p-6 rounded-2xl text-left transition-all duration-300',
                            'bg-white border-2 shadow-sm hover:shadow-xl',
                            selectedType === 'ONE_TO_ONE'
                                ? 'border-teal-500 ring-4 ring-teal-100 shadow-lg'
                                : 'border-slate-200 hover:border-teal-400'
                        )}
                    >
                        {/* Selected indicator */}
                        {selectedType === 'ONE_TO_ONE' && (
                            <motion.div
                                initial={{ scale: 0 }}
                                animate={{ scale: 1 }}
                                className="absolute -top-2 -right-2 w-6 h-6 bg-teal-500 rounded-full flex items-center justify-center"
                            >
                                <CheckCircle2 className="w-4 h-4 text-white" />
                            </motion.div>
                        )}

                        <div className={cn(
                            'w-14 h-14 rounded-xl flex items-center justify-center mb-4 transition-colors',
                            selectedType === 'ONE_TO_ONE' ? 'bg-teal-100' : 'bg-slate-100'
                        )}>
                            <User className={cn(
                                'w-7 h-7',
                                selectedType === 'ONE_TO_ONE' ? 'text-teal-600' : 'text-slate-600'
                            )} />
                        </div>

                        <h3 className="text-xl font-semibold text-slate-900 mb-2">
                            Coaching / Supervision
                        </h3>
                        <p className="text-slate-600 leading-relaxed">
                            Séance individuelle 1-to-1. Idéal pour l'analyse de pratique ou le soutien.
                        </p>

                        <div className="mt-4 pt-4 border-t border-slate-100">
                            <span className={cn(
                                'text-sm font-medium',
                                selectedType === 'ONE_TO_ONE' ? 'text-teal-600' : 'text-slate-500'
                            )}>
                                {selectedType === 'ONE_TO_ONE' ? '✓ Sélectionné' : 'Cliquez pour sélectionner'}
                            </span>
                        </div>
                    </motion.button>

                    {/* Card B: Atelier Groupe / Masterclass (Disabled) */}
                    <div
                        className={cn(
                            'relative p-6 rounded-2xl text-left',
                            'bg-slate-50 border-2 border-slate-200',
                            'opacity-60 cursor-not-allowed grayscale'
                        )}
                    >
                        {/* Coming Soon Badge */}
                        <Badge
                            className="absolute -top-2 -right-2 bg-purple-500 hover:bg-purple-500 text-white px-3 py-1 text-xs font-medium shadow-lg"
                        >
                            🚀 Bientôt disponible
                        </Badge>

                        <div className="w-14 h-14 rounded-xl bg-slate-200 flex items-center justify-center mb-4">
                            <Users className="w-7 h-7 text-slate-500" />
                        </div>

                        <h3 className="text-xl font-semibold text-slate-700 mb-2">
                            Atelier Groupe / Masterclass
                        </h3>
                        <p className="text-slate-500 leading-relaxed">
                            Webinaire ou formation collective.
                        </p>

                        <div className="mt-4 pt-4 border-t border-slate-200">
                            <span className="text-sm font-medium text-slate-400">
                                Non disponible
                            </span>
                        </div>
                    </div>
                </motion.div>

                {/* Details Form */}
                <AnimatePresence mode="wait">
                    {selectedType === 'ONE_TO_ONE' && (
                        <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            transition={{ duration: 0.4, ease: 'easeInOut' }}
                        >
                            <motion.form
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.2 }}
                                onSubmit={handleSubmit}
                                className="bg-white rounded-2xl border border-slate-200 shadow-xl p-6 sm:p-8"
                            >
                                <div className="flex items-center gap-3 mb-6">
                                    <div className="w-10 h-10 rounded-lg bg-teal-100 flex items-center justify-center">
                                        <FileText className="w-5 h-5 text-teal-600" />
                                    </div>
                                    <div>
                                        <h2 className="text-xl font-semibold text-slate-900">
                                            Détails du service
                                        </h2>
                                        <p className="text-sm text-slate-500">
                                            Configurez votre offre de coaching
                                        </p>
                                    </div>
                                </div>

                                <div className="space-y-6">
                                    {/* Title */}
                                    <div className="space-y-2">
                                        <label htmlFor="title" className="block text-sm font-medium text-slate-700">
                                            Titre du service *
                                        </label>
                                        <Input
                                            id="title"
                                            value={form.title}
                                            onChange={(e) => handleInputChange('title', e.target.value)}
                                            placeholder="Ex: Supervision individuelle - Analyse de pratique"
                                            className="h-12 border-slate-200 focus:border-teal-500 focus:ring-teal-500"
                                        />
                                    </div>

                                    {/* Description */}
                                    <div className="space-y-2">
                                        <label htmlFor="description" className="block text-sm font-medium text-slate-700">
                                            Description
                                        </label>
                                        <textarea
                                            id="description"
                                            value={form.description}
                                            onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => handleInputChange('description', e.target.value)}
                                            placeholder="Décrivez votre service, votre approche et ce que le client peut attendre..."
                                            rows={4}
                                            className="w-full px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-teal-500 resize-none"
                                        />
                                    </div>

                                    {/* Price & Duration Row */}
                                    <div className="grid sm:grid-cols-2 gap-6">
                                        {/* Price */}
                                        <div className="space-y-2">
                                            <label htmlFor="price" className="block text-sm font-medium text-slate-700">
                                                Prix *
                                            </label>
                                            <div className="relative">
                                                <Euro className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                                                <Input
                                                    id="price"
                                                    type="number"
                                                    min="0"
                                                    step="0.01"
                                                    value={form.price}
                                                    onChange={(e) => handleInputChange('price', e.target.value)}
                                                    placeholder="75.00"
                                                    className="h-12 pl-10 border-slate-200 focus:border-teal-500 focus:ring-teal-500"
                                                />
                                            </div>
                                        </div>

                                        {/* Duration */}
                                        <div className="space-y-2">
                                            <span className="block text-sm font-medium text-slate-700">
                                                Durée *
                                            </span>
                                            <div className="flex gap-2">
                                                {durations.map((d) => (
                                                    <button
                                                        key={d.value}
                                                        type="button"
                                                        onClick={() => handleInputChange('duration', d.value)}
                                                        className={cn(
                                                            'flex-1 h-12 rounded-lg border-2 font-medium transition-all',
                                                            'flex items-center justify-center gap-2',
                                                            form.duration === d.value
                                                                ? 'border-teal-500 bg-teal-50 text-teal-700'
                                                                : 'border-slate-200 bg-white text-slate-600 hover:border-slate-300'
                                                        )}
                                                    >
                                                        <Clock className="w-4 h-4" />
                                                        {d.label}
                                                    </button>
                                                ))}
                                            </div>
                                        </div>
                                    </div>

                                    {/* Preview Card */}
                                    <div className="bg-slate-50 rounded-xl p-4 border border-slate-200">
                                        <p className="text-xs font-medium text-slate-500 uppercase tracking-wide mb-2">
                                            Aperçu
                                        </p>
                                        <div className="flex items-center justify-between">
                                            <div>
                                                <p className="font-semibold text-slate-900">
                                                    {form.title || 'Titre du service'}
                                                </p>
                                                <p className="text-sm text-slate-500">
                                                    Coaching 1-to-1 · {form.duration} min
                                                </p>
                                            </div>
                                            <div className="text-right">
                                                <p className="text-2xl font-bold text-teal-600">
                                                    {form.price ? `${parseFloat(form.price).toFixed(2)}€` : '0.00€'}
                                                </p>
                                            </div>
                                        </div>
                                    </div>

                                    {/* Submit Button */}
                                    <Button
                                        type="submit"
                                        disabled={isSubmitting || !form.title || !form.price}
                                        className="w-full h-12 bg-teal-600 hover:bg-teal-700 text-white font-semibold rounded-xl shadow-lg shadow-teal-600/25 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                                    >
                                        {isSubmitting ? (
                                            <span className="flex items-center gap-2">
                                                <svg className="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                                </svg>
                                                Publication en cours...
                                            </span>
                                        ) : (
                                            'Publier le service'
                                        )}
                                    </Button>
                                </div>
                            </motion.form>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Help Text */}
                {!selectedType && (
                    <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.3 }}
                        className="text-center text-slate-500 text-sm"
                    >
                        Sélectionnez un type de service pour commencer
                    </motion.p>
                )}
            </div>
        </div>
    );
}
