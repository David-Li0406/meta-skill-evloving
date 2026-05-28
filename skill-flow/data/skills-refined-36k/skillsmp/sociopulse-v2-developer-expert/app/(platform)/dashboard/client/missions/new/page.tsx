'use client';

import { useState, useMemo, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useForm, Controller } from 'react-hook-form';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Search,
    ChevronRight,
    ChevronLeft,
    Check,
    Moon,
    Car,
    Shield,
    Clock,
    MapPin,
    Euro,
    Users,
    Briefcase,
    Sparkles,
    AlertTriangle,
    Calendar,
    Building2,
    UserCheck,
    Zap,
    Info,
    X,
} from 'lucide-react';
import { Button, Badge, Input } from '@/components/ui';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import {
    useSOSConfig,
    type JobDefinition,
    type JobCategory,
    CATEGORY_LABELS,
    URGENCY_LABELS,
    SHIFT_TYPES,
    type UrgencyLevel,
    type ShiftType,
} from '@/lib/sos-config';
import { isMedical } from '@/lib/brand';
import { createReliefMission, getMissionCandidates } from '@/app/(platform)/services/matching.service';

// =============================================================================
// TYPES
// =============================================================================

interface SOSFormData {
    // Step 1: Job Selection
    jobId: string;
    requiresDriverLicense: boolean;
    isNightShift: boolean;
    
    // Step 2: Context & Specificities
    specialties: string[];
    serviceUnit: string; // Medical: "Unit 2B"
    targetPublic: string; // Social: "Teenagers 14-18"
    description: string;
    
    // Step 3: Offer & Matching
    urgencyLevel: UrgencyLevel;
    shiftType: ShiftType;
    startDate: string;
    endDate: string;
    hourlyRate: number;
    address: string;
    city: string;
    postalCode: string;
}

const STEPS = [
    { id: 1, title: 'Métier', icon: Briefcase },
    { id: 2, title: 'Contexte', icon: Building2 },
    { id: 3, title: 'Offre', icon: Euro },
];

// =============================================================================
// MOCK TALENT MATCHING
// =============================================================================

function calculateMatchingTalents(
    jobId: string,
    specialties: string[],
    hourlyRate: number,
    isNight: boolean
): number {
    // Mock calculation - in real app, this would call an API
    let base = 25;
    if (jobId) base += 15;
    if (specialties.length > 0) base -= specialties.length * 3;
    if (hourlyRate > 25) base += 10;
    if (isNight) base -= 5;
    return Math.max(3, Math.min(base, 50));
}

// =============================================================================
// COMBOBOX COMPONENT
// =============================================================================

interface JobComboboxProps {
    jobs: JobDefinition[];
    value: string;
    onChange: (value: string) => void;
    placeholder?: string;
}

function JobCombobox({ jobs, value, onChange, placeholder = 'Rechercher un métier...' }: JobComboboxProps) {
    const [isOpen, setIsOpen] = useState(false);
    const [search, setSearch] = useState('');

    const selectedJob = jobs.find((j) => j.id === value);

    const filteredJobs = useMemo(() => {
        if (!search.trim()) return jobs;
        const query = search.toLowerCase();
        return jobs.filter(
            (job) =>
                job.label.toLowerCase().includes(query) ||
                job.shortCode?.toLowerCase().includes(query) ||
                job.specialties.some((s) => s.toLowerCase().includes(query))
        );
    }, [jobs, search]);

    const groupedJobs = useMemo(() => {
        const groups: Record<JobCategory, JobDefinition[]> = {
            SOIN: [],
            EDUC: [],
            HOTELLERIE: [],
            ADMIN: [],
            MANAGEMENT: [],
            PARAMEDICAL: [],
        };
        filteredJobs.forEach((job) => {
            if (groups[job.category]) {
                groups[job.category].push(job);
            }
        });
        return groups;
    }, [filteredJobs]);

    return (
        <div className="relative">
            {/* Trigger Button */}
            <button
                type="button"
                onClick={() => setIsOpen(!isOpen)}
                className={cn(
                    'w-full flex items-center justify-between gap-2 px-4 py-3 rounded-xl border-2 transition-all text-left',
                    isOpen
                        ? 'border-primary-500 ring-4 ring-primary-500/20'
                        : 'border-slate-200 hover:border-slate-300',
                    selectedJob ? 'bg-white' : 'bg-slate-50'
                )}
            >
                {selectedJob ? (
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-lg bg-primary-100 flex items-center justify-center">
                            <Briefcase className="w-5 h-5 text-primary-600" />
                        </div>
                        <div>
                            <p className="font-semibold text-slate-900">{selectedJob.label}</p>
                            <p className="text-sm text-slate-500">{selectedJob.shortCode}</p>
                        </div>
                    </div>
                ) : (
                    <span className="text-slate-400">{placeholder}</span>
                )}
                <ChevronRight
                    className={cn(
                        'w-5 h-5 text-slate-400 transition-transform',
                        isOpen && 'rotate-90'
                    )}
                />
            </button>

            {/* Dropdown */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="absolute z-50 top-full left-0 right-0 mt-2 bg-white rounded-xl border border-slate-200 shadow-xl max-h-[400px] overflow-hidden"
                    >
                        {/* Search Input */}
                        <div className="p-3 border-b border-slate-100">
                            <div className="relative">
                                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                                <input
                                    type="text"
                                    value={search}
                                    onChange={(e) => setSearch(e.target.value)}
                                    placeholder="Rechercher..."
                                    className="w-full pl-10 pr-4 py-2 rounded-lg border border-slate-200 text-sm focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20"
                                    autoFocus
                                />
                            </div>
                        </div>

                        {/* Job List */}
                        <div className="overflow-y-auto max-h-[320px] p-2">
                            {Object.entries(groupedJobs).map(([category, categoryJobs]) => {
                                if (categoryJobs.length === 0) return null;
                                return (
                                    <div key={category} className="mb-2">
                                        <p className="px-3 py-1.5 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                                            {CATEGORY_LABELS[category as JobCategory]}
                                        </p>
                                        {categoryJobs.map((job) => (
                                            <button
                                                key={job.id}
                                                type="button"
                                                onClick={() => {
                                                    onChange(job.id);
                                                    setIsOpen(false);
                                                    setSearch('');
                                                }}
                                                className={cn(
                                                    'w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-left',
                                                    value === job.id
                                                        ? 'bg-primary-50 text-primary-700'
                                                        : 'hover:bg-slate-50'
                                                )}
                                            >
                                                <div className="flex-1">
                                                    <p className="font-medium text-sm">{job.label}</p>
                                                    <div className="flex items-center gap-2 mt-0.5">
                                                        {job.shortCode && (
                                                            <Badge variant="secondary" className="text-xs">
                                                                {job.shortCode}
                                                            </Badge>
                                                        )}
                                                        {job.requiresAdeli && (
                                                            <Badge variant="outline" className="text-xs text-blue-600 border-blue-200">
                                                                ADELI
                                                            </Badge>
                                                        )}
                                                    </div>
                                                </div>
                                                {value === job.id && (
                                                    <Check className="w-4 h-4 text-primary-600" />
                                                )}
                                            </button>
                                        ))}
                                    </div>
                                );
                            })}

                            {filteredJobs.length === 0 && (
                                <div className="text-center py-8 text-slate-500">
                                    <Search className="w-8 h-8 mx-auto mb-2 opacity-50" />
                                    <p>Aucun métier trouvé</p>
                                </div>
                            )}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Backdrop */}
            {isOpen && (
                <div
                    className="fixed inset-0 z-40"
                    onClick={() => setIsOpen(false)}
                />
            )}
        </div>
    );
}

// =============================================================================
// MULTI-SELECT COMPONENT (Specialties)
// =============================================================================

interface SpecialtyMultiSelectProps {
    options: string[];
    value: string[];
    onChange: (value: string[]) => void;
    placeholder?: string;
}

function SpecialtyMultiSelect({
    options,
    value,
    onChange,
    placeholder = 'Sélectionner des spécialités...',
}: SpecialtyMultiSelectProps) {
    const [isOpen, setIsOpen] = useState(false);

    const toggleOption = (option: string) => {
        if (value.includes(option)) {
            onChange(value.filter((v) => v !== option));
        } else {
            onChange([...value, option]);
        }
    };

    return (
        <div className="relative">
            {/* Selected Tags */}
            <div
                onClick={() => setIsOpen(!isOpen)}
                className={cn(
                    'min-h-[48px] px-3 py-2 rounded-xl border-2 cursor-pointer transition-all',
                    isOpen
                        ? 'border-primary-500 ring-4 ring-primary-500/20'
                        : 'border-slate-200 hover:border-slate-300'
                )}
            >
                {value.length > 0 ? (
                    <div className="flex flex-wrap gap-1.5">
                        {value.map((v) => (
                            <Badge
                                key={v}
                                variant="secondary"
                                className="flex items-center gap-1 bg-primary-100 text-primary-700"
                            >
                                {v}
                                <button
                                    type="button"
                                    title={`Retirer ${v}`}
                                    aria-label={`Retirer ${v}`}
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        toggleOption(v);
                                    }}
                                    className="ml-1 hover:bg-primary-200 rounded-full p-0.5"
                                >
                                    <X className="w-3 h-3" />
                                </button>
                            </Badge>
                        ))}
                    </div>
                ) : (
                    <span className="text-slate-400">{placeholder}</span>
                )}
            </div>

            {/* Dropdown */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="absolute z-50 top-full left-0 right-0 mt-2 bg-white rounded-xl border border-slate-200 shadow-xl max-h-[280px] overflow-y-auto p-2"
                    >
                        {options.map((option) => (
                            <button
                                key={option}
                                type="button"
                                onClick={() => toggleOption(option)}
                                className={cn(
                                    'w-full flex items-center justify-between px-3 py-2 rounded-lg transition-colors text-left text-sm',
                                    value.includes(option)
                                        ? 'bg-primary-50 text-primary-700'
                                        : 'hover:bg-slate-50'
                                )}
                            >
                                <span>{option}</span>
                                {value.includes(option) && (
                                    <Check className="w-4 h-4 text-primary-600" />
                                )}
                            </button>
                        ))}

                        {options.length === 0 && (
                            <p className="text-center py-4 text-slate-400 text-sm">
                                Aucune spécialité disponible
                            </p>
                        )}
                    </motion.div>
                )}
            </AnimatePresence>

            {isOpen && (
                <div className="fixed inset-0 z-40" onClick={() => setIsOpen(false)} />
            )}
        </div>
    );
}

// =============================================================================
// TOGGLE SWITCH COMPONENT
// =============================================================================

interface ToggleSwitchProps {
    checked: boolean;
    onChange: (checked: boolean) => void;
    label: string;
    description?: string;
    icon: React.ElementType;
    iconColor?: string;
}

function ToggleSwitch({
    checked,
    onChange,
    label,
    description,
    icon: Icon,
    iconColor = 'text-slate-600',
}: ToggleSwitchProps) {
    const switchId = `switch-${label.replace(/\s+/g, '-').toLowerCase()}`;
    
    return (
        <div className="flex items-center justify-between p-4 rounded-xl border-2 border-slate-200 hover:border-slate-300 transition-all">
            <div className="flex items-center gap-3">
                <div className={cn('w-10 h-10 rounded-lg flex items-center justify-center', 
                    checked ? 'bg-primary-100' : 'bg-slate-100'
                )}>
                    <Icon className={cn('w-5 h-5', checked ? 'text-primary-600' : iconColor)} />
                </div>
                <div>
                    <label htmlFor={switchId} className="font-medium text-slate-900 cursor-pointer">
                        {label}
                    </label>
                    {description && (
                        <p className="text-sm text-slate-500">{description}</p>
                    )}
                </div>
            </div>
            <label htmlFor={switchId} className="relative cursor-pointer">
                <input
                    type="checkbox"
                    id={switchId}
                    checked={checked}
                    onChange={(e) => onChange(e.target.checked)}
                    className="sr-only peer"
                />
                <div
                    className={cn(
                        'w-12 h-7 rounded-full transition-colors',
                        checked ? 'bg-primary-500' : 'bg-slate-300'
                    )}
                >
                    <span
                        className={cn(
                            'absolute top-1 left-1 w-5 h-5 bg-white rounded-full shadow-sm transition-transform',
                            checked && 'translate-x-5'
                        )}
                    />
                </div>
            </label>
        </div>
    );
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export default function NewSOSMissionPage() {
    const router = useRouter();
    const [currentStep, setCurrentStep] = useState(1);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const { jobs } = useSOSConfig();
    const isMedicalMode = isMedical();

    const {
        control,
        watch,
        handleSubmit,
        setValue,
        formState: { errors },
    } = useForm<SOSFormData>({
        defaultValues: {
            jobId: '',
            requiresDriverLicense: false,
            isNightShift: false,
            specialties: [],
            serviceUnit: '',
            targetPublic: '',
            description: '',
            urgencyLevel: 'MEDIUM',
            shiftType: 'JOUR',
            startDate: '',
            endDate: '',
            hourlyRate: 18,
            address: '',
            city: '',
            postalCode: '',
        },
    });

    const watchedJobId = watch('jobId');
    const watchedSpecialties = watch('specialties');
    const watchedHourlyRate = watch('hourlyRate');
    const watchedIsNight = watch('isNightShift');

    // Get selected job details
    const selectedJob = useMemo(() => {
        return jobs.find((j) => j.id === watchedJobId);
    }, [jobs, watchedJobId]);

    // Reset specialties when job changes
    useEffect(() => {
        if (selectedJob) {
            setValue('specialties', []);
            // Set suggested hourly rate
            if (selectedJob.minHourlyRate) {
                setValue('hourlyRate', selectedJob.minHourlyRate);
            }
        }
    }, [selectedJob, setValue]);

    // Calculate matching talents
    const matchingTalents = useMemo(() => {
        return calculateMatchingTalents(
            watchedJobId,
            watchedSpecialties,
            watchedHourlyRate,
            watchedIsNight
        );
    }, [watchedJobId, watchedSpecialties, watchedHourlyRate, watchedIsNight]);

    const onSubmit = async (data: SOSFormData) => {
        if (!selectedJob) {
            toast.error('Veuillez sélectionner un métier');
            return;
        }

        if (!data.startDate) {
            toast.error('Veuillez sélectionner une date de début');
            return;
        }

        if (!data.city && !data.address) {
            toast.error('Veuillez renseigner la ville');
            return;
        }

        setIsSubmitting(true);

        try {
            const isNight = data.isNightShift || data.shiftType === 'NUIT';
            const payload = {
                title: `Mission SOS - ${selectedJob.label}`,
                jobTitle: selectedJob.label,
                jobId: data.jobId,
                specialtiesTags: data.specialties,
                requiredSkills: data.specialties,
                requiresCar: data.requiresDriverLicense,
                requiresNight: isNight,
                requiresDiploma: selectedJob.requiresDiploma,
                serviceName: isMedicalMode ? data.serviceUnit || undefined : undefined,
                targetPublic: !isMedicalMode ? data.targetPublic || undefined : undefined,
                hourlyRate: data.hourlyRate,
                isNightShift: isNight,
                urgencyLevel: data.urgencyLevel,
                description: data.description,
                startDate: data.startDate,
                endDate: data.endDate || undefined,
                address: data.address || data.city,
                city: data.city || data.address,
                postalCode: data.postalCode,
                radiusKm: 30,
            };

            const mission = await createReliefMission(payload);
            const missionId = mission?.id || mission?.missionId;

            if (missionId) {
                try {
                    await getMissionCandidates(missionId);
                } catch (matchingError) {
                    console.warn('Matching trigger failed', matchingError);
                }
            }

            toast.success('Mission lancée : Recherche de talents en cours...');
            router.push('/dashboard/tracking');
        } catch (error) {
            console.error('SOS mission creation failed:', error);
            toast.error('Erreur lors du lancement de la mission');
        } finally {
            setIsSubmitting(false);
        }
    };

    const canProceedStep1 = !!watchedJobId;
    const canProceedStep2 = true; // Optional fields

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100/50 p-4 sm:p-6 lg:p-8">
            <div className="max-w-3xl mx-auto">
                {/* Header */}
                <div className="mb-8">
                    <div className="flex items-center gap-3 mb-2">
                        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-red-500 to-orange-500 flex items-center justify-center">
                            <Zap className="w-6 h-6 text-white" />
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold text-slate-900">
                                Nouvelle Mission SOS
                            </h1>
                            <p className="text-slate-600">
                                Trouvez un renfort rapidement
                            </p>
                        </div>
                    </div>
                </div>

                {/* Progress Steps */}
                <div className="mb-8">
                    <div className="flex items-center justify-between">
                        {STEPS.map((step, index) => {
                            const Icon = step.icon;
                            const isActive = currentStep === step.id;
                            const isCompleted = currentStep > step.id;

                            return (
                                <div key={step.id} className="flex items-center">
                                    <button
                                        type="button"
                                        onClick={() => {
                                            if (isCompleted || isActive) {
                                                setCurrentStep(step.id);
                                            }
                                        }}
                                        className={cn(
                                            'flex items-center gap-2 px-4 py-2 rounded-xl transition-all',
                                            isActive && 'bg-primary-100 text-primary-700',
                                            isCompleted && 'text-primary-600',
                                            !isActive && !isCompleted && 'text-slate-400'
                                        )}
                                    >
                                        <div
                                            className={cn(
                                                'w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold',
                                                isActive && 'bg-primary-500 text-white',
                                                isCompleted && 'bg-primary-500 text-white',
                                                !isActive && !isCompleted && 'bg-slate-200 text-slate-500'
                                            )}
                                        >
                                            {isCompleted ? (
                                                <Check className="w-4 h-4" />
                                            ) : (
                                                step.id
                                            )}
                                        </div>
                                        <span className="hidden sm:inline font-medium">
                                            {step.title}
                                        </span>
                                    </button>

                                    {index < STEPS.length - 1 && (
                                        <div
                                            className={cn(
                                                'w-12 sm:w-24 h-0.5 mx-2',
                                                currentStep > step.id
                                                    ? 'bg-primary-500'
                                                    : 'bg-slate-200'
                                            )}
                                        />
                                    )}
                                </div>
                            );
                        })}
                    </div>
                </div>

                {/* Form Card */}
                <form onSubmit={handleSubmit(onSubmit)}>
                    <div className="bg-white rounded-2xl border border-slate-200 shadow-lg overflow-hidden">
                        <AnimatePresence mode="wait">
                            {/* ============================================= */}
                            {/* STEP 1: JOB SELECTION */}
                            {/* ============================================= */}
                            {currentStep === 1 && (
                                <motion.div
                                    key="step1"
                                    initial={{ opacity: 0, x: 20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: -20 }}
                                    className="p-6 space-y-6"
                                >
                                    <div>
                                        <h2 className="text-lg font-semibold text-slate-900 mb-1">
                                            Quel métier recherchez-vous ?
                                        </h2>
                                        <p className="text-sm text-slate-500">
                                            Sélectionnez le profil correspondant à votre besoin
                                        </p>
                                    </div>

                                    {/* Job Combobox */}
                                    <Controller
                                        name="jobId"
                                        control={control}
                                        rules={{ required: 'Veuillez sélectionner un métier' }}
                                        render={({ field }) => (
                                            <JobCombobox
                                                jobs={jobs}
                                                value={field.value}
                                                onChange={field.onChange}
                                            />
                                        )}
                                    />

                                    {/* Dynamic Toggles - "Chameleon" Logic */}
                                    {selectedJob && (
                                        <motion.div
                                            initial={{ opacity: 0, height: 0 }}
                                            animate={{ opacity: 1, height: 'auto' }}
                                            className="space-y-3"
                                        >
                                            {/* ADELI Info Message */}
                                            {selectedJob.requiresAdeli && (
                                                <div className="flex items-start gap-3 p-4 bg-blue-50 rounded-xl border border-blue-200">
                                                    <Shield className="w-5 h-5 text-blue-600 mt-0.5" />
                                                    <div>
                                                        <p className="font-medium text-blue-800">
                                                            Numéro ADELI requis
                                                        </p>
                                                        <p className="text-sm text-blue-600">
                                                            Ce métier nécessite une vérification ADELI.
                                                            Seuls les talents avec un numéro ADELI valide pourront postuler.
                                                        </p>
                                                    </div>
                                                </div>
                                            )}

                                            {/* Night Shift Toggle */}
                                            {selectedJob.canDoNight && (
                                                <Controller
                                                    name="isNightShift"
                                                    control={control}
                                                    render={({ field }) => (
                                                        <ToggleSwitch
                                                            checked={field.value}
                                                            onChange={field.onChange}
                                                            label="Poste de Nuit ?"
                                                            description="Le talent travaillera sur des horaires nocturnes"
                                                            icon={Moon}
                                                            iconColor="text-indigo-600"
                                                        />
                                                    )}
                                                />
                                            )}

                                            {/* Driver License Toggle */}
                                            {selectedJob.requiresDriverLicense && (
                                                <Controller
                                                    name="requiresDriverLicense"
                                                    control={control}
                                                    render={({ field }) => (
                                                        <ToggleSwitch
                                                            checked={field.value}
                                                            onChange={field.onChange}
                                                            label="Permis B obligatoire ?"
                                                            description="Le talent doit posséder le permis de conduire"
                                                            icon={Car}
                                                            iconColor="text-emerald-600"
                                                        />
                                                    )}
                                                />
                                            )}

                                            {/* Job Info Card */}
                                            <div className="p-4 bg-slate-50 rounded-xl">
                                                <p className="text-sm text-slate-600">
                                                    <strong>Spécialités disponibles:</strong>{' '}
                                                    {selectedJob.specialties.slice(0, 5).join(', ')}
                                                    {selectedJob.specialties.length > 5 && '...'}
                                                </p>
                                                {selectedJob.minHourlyRate && (
                                                    <p className="text-sm text-slate-600 mt-1">
                                                        <strong>Taux horaire suggéré:</strong>{' '}
                                                        {selectedJob.minHourlyRate}€ - {selectedJob.maxHourlyRate}€/h
                                                    </p>
                                                )}
                                            </div>
                                        </motion.div>
                                    )}
                                </motion.div>
                            )}

                            {/* ============================================= */}
                            {/* STEP 2: CONTEXT & SPECIFICITIES */}
                            {/* ============================================= */}
                            {currentStep === 2 && (
                                <motion.div
                                    key="step2"
                                    initial={{ opacity: 0, x: 20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: -20 }}
                                    className="p-6 space-y-6"
                                >
                                    <div>
                                        <h2 className="text-lg font-semibold text-slate-900 mb-1">
                                            Contexte de la mission
                                        </h2>
                                        <p className="text-sm text-slate-500">
                                            Précisez les spécificités pour un meilleur matching
                                        </p>
                                    </div>

                                    {/* Specialties Multi-Select */}
                                    {selectedJob && (
                                        <div>
                                            <label className="block text-sm font-medium text-slate-700 mb-2">
                                                Spécialités recherchées
                                            </label>
                                            <Controller
                                                name="specialties"
                                                control={control}
                                                render={({ field }) => (
                                                    <SpecialtyMultiSelect
                                                        options={selectedJob.specialties}
                                                        value={field.value}
                                                        onChange={field.onChange}
                                                        placeholder="Sélectionner des spécialités..."
                                                    />
                                                )}
                                            />
                                        </div>
                                    )}

                                    {/* Mode-specific Input */}
                                    {isMedicalMode ? (
                                        <div>
                                            <label className="block text-sm font-medium text-slate-700 mb-2">
                                                Service / Unité
                                            </label>
                                            <Controller
                                                name="serviceUnit"
                                                control={control}
                                                render={({ field }) => (
                                                    <Input
                                                        {...field}
                                                        placeholder="Ex: Unité 2B, Service Cardiologie..."
                                                        className="w-full"
                                                    />
                                                )}
                                            />
                                            <p className="text-xs text-slate-500 mt-1">
                                                Précisez le service ou l'unité de soins
                                            </p>
                                        </div>
                                    ) : (
                                        <div>
                                            <label className="block text-sm font-medium text-slate-700 mb-2">
                                                Public accompagné
                                            </label>
                                            <Controller
                                                name="targetPublic"
                                                control={control}
                                                render={({ field }) => (
                                                    <Input
                                                        {...field}
                                                        placeholder="Ex: Adolescents 14-18, Adultes handicapés..."
                                                        className="w-full"
                                                    />
                                                )}
                                            />
                                            <p className="text-xs text-slate-500 mt-1">
                                                Décrivez le public que le talent accompagnera
                                            </p>
                                        </div>
                                    )}

                                    {/* Description */}
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 mb-2">
                                            Description de la mission
                                        </label>
                                        <Controller
                                            name="description"
                                            control={control}
                                            render={({ field }) => (
                                                <textarea
                                                    {...field}
                                                    rows={4}
                                                    placeholder="Décrivez le contexte, les missions principales, les attentes..."
                                                    className="w-full px-4 py-3 rounded-xl border-2 border-slate-200 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/20 transition-all resize-none"
                                                />
                                            )}
                                        />
                                    </div>
                                </motion.div>
                            )}

                            {/* ============================================= */}
                            {/* STEP 3: OFFER & MATCHING */}
                            {/* ============================================= */}
                            {currentStep === 3 && (
                                <motion.div
                                    key="step3"
                                    initial={{ opacity: 0, x: 20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: -20 }}
                                    className="p-6 space-y-6"
                                >
                                    <div>
                                        <h2 className="text-lg font-semibold text-slate-900 mb-1">
                                            Votre offre
                                        </h2>
                                        <p className="text-sm text-slate-500">
                                            Définissez les conditions de la mission
                                        </p>
                                    </div>

                                    {/* Urgency Level */}
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 mb-3">
                                            Niveau d'urgence
                                        </label>
                                        <Controller
                                            name="urgencyLevel"
                                            control={control}
                                            render={({ field }) => (
                                                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                                                    {(Object.entries(URGENCY_LABELS) as [UrgencyLevel, typeof URGENCY_LABELS[UrgencyLevel]][]).map(
                                                        ([key, config]) => (
                                                            <button
                                                                key={key}
                                                                type="button"
                                                                onClick={() => field.onChange(key)}
                                                                className={cn(
                                                                    'p-3 rounded-xl border-2 text-center transition-all',
                                                                    field.value === key
                                                                        ? `border-${config.color}-500 bg-${config.color}-50`
                                                                        : 'border-slate-200 hover:border-slate-300'
                                                                )}
                                                            >
                                                                <p className={cn(
                                                                    'font-semibold text-sm',
                                                                    field.value === key ? `text-${config.color}-700` : 'text-slate-700'
                                                                )}>
                                                                    {config.label}
                                                                </p>
                                                                <p className="text-xs text-slate-500 mt-0.5">
                                                                    {config.description}
                                                                </p>
                                                            </button>
                                                        )
                                                    )}
                                                </div>
                                            )}
                                        />
                                    </div>

                                    {/* Dates */}
                                    <div className="grid grid-cols-2 gap-4">
                                        <div>
                                            <label className="block text-sm font-medium text-slate-700 mb-2">
                                                Date de début
                                            </label>
                                            <Controller
                                                name="startDate"
                                                control={control}
                                                render={({ field }) => (
                                                    <Input
                                                        {...field}
                                                        type="date"
                                                        className="w-full"
                                                    />
                                                )}
                                            />
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-slate-700 mb-2">
                                                Date de fin
                                            </label>
                                            <Controller
                                                name="endDate"
                                                control={control}
                                                render={({ field }) => (
                                                    <Input
                                                        {...field}
                                                        type="date"
                                                        className="w-full"
                                                    />
                                                )}
                                            />
                                        </div>
                                    </div>

                                    {/* Hourly Rate */}
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 mb-2">
                                            Taux horaire proposé
                                        </label>
                                        <Controller
                                            name="hourlyRate"
                                            control={control}
                                            render={({ field }) => (
                                                <div className="relative">
                                                    <Euro className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                                                    <input
                                                        type="number"
                                                        {...field}
                                                        onChange={(e) => field.onChange(parseFloat(e.target.value) || 0)}
                                                        className="w-full pl-12 pr-16 py-3 rounded-xl border-2 border-slate-200 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/20 transition-all"
                                                    />
                                                    <span className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500">
                                                        /heure
                                                    </span>
                                                </div>
                                            )}
                                        />
                                        {selectedJob?.minHourlyRate && (
                                            <p className="text-xs text-slate-500 mt-1">
                                                💡 Taux suggéré pour ce métier : {selectedJob.minHourlyRate}€ - {selectedJob.maxHourlyRate}€/h
                                            </p>
                                        )}
                                    </div>

                                    {/* Location */}
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 mb-2">
                                            Localisation
                                        </label>
                                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                                            <Controller
                                                name="address"
                                                control={control}
                                                render={({ field }) => (
                                                    <Input
                                                        {...field}
                                                        placeholder="Adresse"
                                                        className="sm:col-span-2"
                                                    />
                                                )}
                                            />
                                            <Controller
                                                name="city"
                                                control={control}
                                                render={({ field }) => (
                                                    <Input
                                                        {...field}
                                                        placeholder="Ville"
                                                    />
                                                )}
                                            />
                                            <Controller
                                                name="postalCode"
                                                control={control}
                                                render={({ field }) => (
                                                    <Input
                                                        {...field}
                                                        placeholder="Code postal"
                                                    />
                                                )}
                                            />
                                        </div>
                                    </div>

                                    {/* Matching Counter */}
                                    <motion.div
                                        key={matchingTalents}
                                        initial={{ scale: 0.95 }}
                                        animate={{ scale: 1 }}
                                        className="p-4 bg-gradient-to-r from-primary-50 to-emerald-50 rounded-xl border border-primary-200"
                                    >
                                        <div className="flex items-center gap-4">
                                            <div className="w-14 h-14 rounded-full bg-gradient-to-br from-primary-500 to-emerald-500 flex items-center justify-center">
                                                <Users className="w-7 h-7 text-white" />
                                            </div>
                                            <div>
                                                <p className="text-3xl font-bold text-primary-700">
                                                    {matchingTalents}
                                                </p>
                                                <p className="text-sm text-primary-600">
                                                    Talents correspondent à vos critères
                                                </p>
                                            </div>
                                            <Sparkles className="w-6 h-6 text-amber-500 ml-auto" />
                                        </div>
                                    </motion.div>
                                </motion.div>
                            )}
                        </AnimatePresence>

                        {/* Footer Navigation */}
                        <div className="px-6 py-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between">
                            {currentStep > 1 ? (
                                <Button
                                    type="button"
                                    variant="outline"
                                    onClick={() => setCurrentStep(currentStep - 1)}
                                >
                                    <ChevronLeft className="w-4 h-4 mr-1" />
                                    Retour
                                </Button>
                            ) : (
                                <div />
                            )}

                            {currentStep < 3 ? (
                                <Button
                                    type="button"
                                    onClick={() => setCurrentStep(currentStep + 1)}
                                    disabled={currentStep === 1 && !canProceedStep1}
                                >
                                    Continuer
                                    <ChevronRight className="w-4 h-4 ml-1" />
                                </Button>
                            ) : (
                                <Button
                                    type="submit"
                                    className="bg-gradient-to-r from-red-500 to-orange-500 hover:from-red-600 hover:to-orange-600"
                                    disabled={isSubmitting}
                                >
                                    <Zap className="w-4 h-4 mr-2" />
                                    {isSubmitting ? 'Envoi...' : 'Publier la mission SOS'}
                                </Button>
                            )}
                        </div>
                    </div>
                </form>
            </div>
        </div>
    );
}
