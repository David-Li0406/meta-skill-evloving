'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Building2,
    CreditCard,
    Bell,
    Shield,
    Save,
    CheckCircle,
    AlertTriangle,
    Info,
    FileCheck,
    FolderOpen,
} from 'lucide-react';
import { Badge, DocumentCard, type DocumentStatus } from '@/components/ui';
import { mockEstablishment } from '@/components/dashboard/client/mock-data';
import { toast } from 'sonner';

// =============================================================================
// CLIENT SETTINGS PAGE - With Conformité Tab
// =============================================================================

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: { staggerChildren: 0.1 }
    }
};

const itemVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: { opacity: 1, y: 0 }
};

// Tab definitions
const TABS = [
    { id: 'profile', label: 'Établissement', icon: Building2 },
    { id: 'compliance', label: 'Conformité', icon: FileCheck },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'security', label: 'Sécurité', icon: Shield },
] as const;

type TabId = typeof TABS[number]['id'];

// Document types for compliance
interface ComplianceDocument {
    id: string;
    title: string;
    description: string;
    status: DocumentStatus;
    rejectionReason?: string;
    fileName?: string;
    required: boolean;
}

const STORAGE_KEY = 'sociopulse_client_compliance_docs';

export default function ClientSettingsPage() {
    const [activeTab, setActiveTab] = useState<TabId>('profile');
    const [formData, setFormData] = useState({
        name: mockEstablishment.name,
        siret: mockEstablishment.siret || '',
        organizationType: mockEstablishment.organizationType || 'PRIVATE',
        address: mockEstablishment.address,
        city: mockEstablishment.city,
        postalCode: mockEstablishment.postalCode,
        chorusProCode: mockEstablishment.chorusProCode || '',
        ejNumber: '',
        siretPayer: '',
        tvaIntra: '',
    });

    const [notifications, setNotifications] = useState({
        newCandidates: true,
        contractReminders: true,
        availabilityAlerts: false,
    });

    // Compliance documents state
    const [complianceDocs, setComplianceDocs] = useState<ComplianceDocument[]>([
        {
            id: 'kbis',
            title: 'KBIS / Avis Sirene',
            description: 'Extrait de moins de 3 mois',
            status: 'MISSING',
            required: true,
        },
        {
            id: 'rib',
            title: 'RIB Bancaire',
            description: 'Pour le prélèvement des missions',
            status: 'MISSING',
            required: true,
        },
        {
            id: 'urssaf',
            title: 'Attestation URSSAF',
            description: 'Attestation de vigilance en cours de validité',
            status: 'MISSING',
            required: true,
        },
        {
            id: 'rcpro',
            title: 'Assurance RC Pro',
            description: 'Responsabilité Civile Professionnelle',
            status: 'MISSING',
            required: true,
        },
    ]);

    // Load compliance docs from localStorage on mount
    useEffect(() => {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) {
            try {
                const parsed = JSON.parse(saved);
                setComplianceDocs(parsed);
            } catch {
                console.error('Failed to parse saved compliance docs');
            }
        }
    }, []);

    // Save compliance docs to localStorage when changed
    useEffect(() => {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(complianceDocs));
    }, [complianceDocs]);

    // Check if all docs are complete (PENDING or VALIDATED) - show toast once
    const [hasShownCompleteToast, setHasShownCompleteToast] = useState(false);
    useEffect(() => {
        const allComplete = complianceDocs.every(
            doc => doc.status === 'PENDING' || doc.status === 'VALIDATED'
        );
        const hasAnyDoc = complianceDocs.some(doc => doc.status !== 'MISSING');

        if (allComplete && hasAnyDoc && !hasShownCompleteToast) {
            toast.success('Dossier complet !', {
                description: 'Vous pouvez maintenant publier des missions.',
                duration: 5000,
            });
            setHasShownCompleteToast(true);
        }
    }, [complianceDocs, hasShownCompleteToast]);

    // Calculate compliance progress
    const completedDocs = complianceDocs.filter(
        doc => doc.status === 'PENDING' || doc.status === 'VALIDATED'
    ).length;
    const totalDocs = complianceDocs.length;
    const complianceProgress = Math.round((completedDocs / totalDocs) * 100);

    // Handle document status change
    const handleDocStatusChange = (docId: string, newStatus: DocumentStatus) => {
        setComplianceDocs(prev =>
            prev.map(doc =>
                doc.id === docId ? { ...doc, status: newStatus } : doc
            )
        );
    };

    // Handle document upload
    const handleDocUpload = (docId: string, file: File) => {
        setComplianceDocs(prev =>
            prev.map(doc =>
                doc.id === docId ? { ...doc, fileName: file.name } : doc
            )
        );
    };

    // Validation
    const isSiretValid = /^\d{14}$/.test(formData.siret.replace(/\s/g, ''));
    const isPublicOrg = formData.organizationType === 'PUBLIC';
    const isChorusRequired = isPublicOrg;
    const isChorusFilled = formData.chorusProCode.trim().length > 0;
    const isProfileComplete = isSiretValid && (!isChorusRequired || isChorusFilled) && complianceProgress === 100;

    const handleChange = (field: string, value: string) => {
        setFormData(prev => ({ ...prev, [field]: value }));
    };

    return (
        <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="p-6 space-y-6"
        >
            {/* Header */}
            <motion.div variants={itemVariants} className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-slate-900">Paramètres</h1>
                    <p className="text-slate-500">
                        Profil établissement, conformité et préférences
                    </p>
                </div>
                {isProfileComplete ? (
                    <Badge variant="success" size="lg" icon={<CheckCircle className="h-4 w-4" />}>
                        Profil vérifié
                    </Badge>
                ) : (
                    <Badge variant="warning" size="lg" icon={<AlertTriangle className="h-4 w-4" />}>
                        Profil incomplet
                    </Badge>
                )}
            </motion.div>

            {/* Tabs */}
            <motion.div variants={itemVariants} className="border-b border-slate-200">
                <nav className="flex gap-1 -mb-px">
                    {TABS.map((tab) => {
                        const Icon = tab.icon;
                        const isActive = activeTab === tab.id;
                        return (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                className={`
                                    flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors
                                    ${isActive
                                        ? 'border-teal-500 text-teal-600'
                                        : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
                                    }
                                `}
                            >
                                <Icon className="h-4 w-4" />
                                {tab.label}
                                {tab.id === 'compliance' && complianceProgress < 100 && (
                                    <span className="ml-1 px-1.5 py-0.5 text-xs rounded-full bg-amber-100 text-amber-700">
                                        {complianceProgress}%
                                    </span>
                                )}
                            </button>
                        );
                    })}
                </nav>
            </motion.div>

            {/* Tab Content */}
            <AnimatePresence mode="wait">
                {/* Profile Tab */}
                {activeTab === 'profile' && (
                    <motion.div
                        key="profile"
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 10 }}
                        className="space-y-6"
                    >
                        {/* Warning for missing Chorus Pro */}
                        {isChorusRequired && !isChorusFilled && (
                            <div className="flex items-center gap-3 rounded-xl border border-amber-200 bg-amber-50 p-4">
                                <AlertTriangle className="h-5 w-5 text-amber-600" />
                                <div>
                                    <p className="font-medium text-amber-800">
                                        Configuration Chorus Pro requise
                                    </p>
                                    <p className="text-sm text-amber-600">
                                        En tant qu'établissement public, vous devez renseigner votre Code Service pour la facturation électronique.
                                    </p>
                                </div>
                            </div>
                        )}

                        {/* Establishment Profile */}
                        <SettingsSection
                            title="Profil Établissement"
                            description="Informations légales et de contact"
                            icon={Building2}
                        >
                            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                                <FormInput
                                    label="Nom de l'établissement"
                                    value={formData.name}
                                    onChange={(v) => handleChange('name', v)}
                                />
                                <FormInput
                                    label="SIRET"
                                    value={formData.siret}
                                    onChange={(v) => handleChange('siret', v)}
                                    placeholder="123 456 789 00012"
                                    error={formData.siret && !isSiretValid ? 'Format invalide (14 chiffres)' : undefined}
                                    success={isSiretValid}
                                />
                                <FormInput
                                    label="Adresse"
                                    value={formData.address}
                                    onChange={(v) => handleChange('address', v)}
                                />
                                <FormInput
                                    label="Ville"
                                    value={formData.city}
                                    onChange={(v) => handleChange('city', v)}
                                />
                                <FormInput
                                    label="Code Postal"
                                    value={formData.postalCode}
                                    onChange={(v) => handleChange('postalCode', v)}
                                />
                                <FormSelect
                                    label="Type d'organisation"
                                    value={formData.organizationType}
                                    onChange={(v) => handleChange('organizationType', v)}
                                    options={[
                                        { value: 'PUBLIC', label: 'Établissement Public' },
                                        { value: 'PRIVATE', label: 'Établissement Privé' },
                                        { value: 'ASSOCIATION', label: 'Association' },
                                    ]}
                                />
                            </div>
                        </SettingsSection>

                        {/* Chorus Pro Section */}
                        <SettingsSection
                            title="Chorus Pro"
                            description="Configuration pour la facturation publique"
                            icon={CreditCard}
                            badge={isChorusRequired ? (
                                <Badge variant="warning" size="sm">Obligatoire</Badge>
                            ) : undefined}
                        >
                            <div className="mb-4 flex items-start gap-2 rounded-lg bg-sky-50 p-3">
                                <Info className="mt-0.5 h-4 w-4 text-sky-600" />
                                <p className="text-sm text-sky-700">
                                    Ces informations sont obligatoires pour les établissements publics (EHPAD, ASE, Hôpitaux) utilisant la facturation Chorus Pro.
                                </p>
                            </div>
                            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                                <FormInput
                                    label="Code Service"
                                    value={formData.chorusProCode}
                                    onChange={(v) => handleChange('chorusProCode', v)}
                                    placeholder="Ex: SERVICE_ACHAT"
                                    required={isChorusRequired}
                                    error={isChorusRequired && !isChorusFilled ? 'Champ obligatoire' : undefined}
                                />
                                <FormInput
                                    label="Numéro d'engagement juridique"
                                    value={formData.ejNumber}
                                    onChange={(v) => handleChange('ejNumber', v)}
                                    placeholder="Ex: EJ-2026-001"
                                />
                                <FormInput
                                    label="SIRET Payeur"
                                    value={formData.siretPayer}
                                    onChange={(v) => handleChange('siretPayer', v)}
                                    placeholder="Identique au SIRET si même entité"
                                />
                                <FormInput
                                    label="N° TVA Intracommunautaire"
                                    value={formData.tvaIntra}
                                    onChange={(v) => handleChange('tvaIntra', v)}
                                    placeholder="FR12345678901"
                                />
                            </div>
                        </SettingsSection>
                    </motion.div>
                )}

                {/* Compliance Tab */}
                {activeTab === 'compliance' && (
                    <motion.div
                        key="compliance"
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 10 }}
                        className="space-y-6"
                    >
                        {/* Header */}
                        <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
                            <div className="flex items-start gap-4">
                                <div className="rounded-xl bg-teal-100 p-3">
                                    <FolderOpen className="h-6 w-6 text-teal-600" />
                                </div>
                                <div className="flex-1">
                                    <h2 className="text-lg font-semibold text-slate-900">
                                        Dossier Administratif
                                    </h2>
                                    <p className="text-sm text-slate-500 mt-1">
                                        Ces documents sont nécessaires pour valider vos missions et générer vos factures.
                                    </p>
                                    
                                    {/* Global Progress Bar */}
                                    <div className="mt-4">
                                        <div className="flex items-center justify-between mb-2">
                                            <span className="text-sm font-medium text-slate-700">
                                                Complétude du dossier
                                            </span>
                                            <span className={`text-sm font-bold ${
                                                complianceProgress === 100 
                                                    ? 'text-emerald-600' 
                                                    : complianceProgress >= 50 
                                                        ? 'text-amber-600' 
                                                        : 'text-slate-600'
                                            }`}>
                                                {complianceProgress}%
                                            </span>
                                        </div>
                                        <div className="h-3 bg-slate-100 rounded-full overflow-hidden">
                                            <motion.div
                                                className={`h-full rounded-full ${
                                                    complianceProgress === 100 
                                                        ? 'bg-gradient-to-r from-emerald-500 to-teal-500' 
                                                        : complianceProgress >= 50 
                                                            ? 'bg-gradient-to-r from-amber-500 to-orange-500' 
                                                            : 'bg-gradient-to-r from-slate-400 to-slate-500'
                                                }`}
                                                initial={{ width: 0 }}
                                                animate={{ width: `${complianceProgress}%` }}
                                                transition={{ duration: 0.8, ease: 'easeOut' }}
                                            />
                                        </div>
                                        <p className="text-xs text-slate-500 mt-2">
                                            {completedDocs}/{totalDocs} documents fournis
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Document Cards Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {complianceDocs.map((doc) => (
                                <DocumentCard
                                    key={doc.id}
                                    title={doc.title}
                                    description={doc.description}
                                    status={doc.status}
                                    rejectionReason={doc.rejectionReason}
                                    fileName={doc.fileName}
                                    onUpload={(file) => handleDocUpload(doc.id, file)}
                                    onStatusChange={(status) => handleDocStatusChange(doc.id, status)}
                                    onView={() => toast.info(`Aperçu de ${doc.title}`)}
                                    mockupMode={true}
                                    variant="teal"
                                />
                            ))}
                        </div>

                        {/* Help text */}
                        <div className="flex items-start gap-3 rounded-lg bg-sky-50 border border-sky-100 p-4">
                            <Info className="h-5 w-5 text-sky-600 flex-shrink-0 mt-0.5" />
                            <div>
                                <p className="text-sm font-medium text-sky-800">
                                    Besoin d&apos;aide ?
                                </p>
                                <p className="text-sm text-sky-700 mt-1">
                                    Nos équipes vérifient vos documents sous 24-48h ouvrées. 
                                    Pour toute question, contactez{' '}
                                    <a href="mailto:support@sociopulse.fr" className="underline font-medium">
                                        support@sociopulse.fr
                                    </a>
                                </p>
                            </div>
                        </div>
                    </motion.div>
                )}

                {/* Notifications Tab */}
                {activeTab === 'notifications' && (
                    <motion.div
                        key="notifications"
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 10 }}
                    >
                        <SettingsSection
                            title="Notifications"
                            description="Gérez vos préférences de notification"
                            icon={Bell}
                        >
                            <div className="space-y-4">
                                <ToggleSetting
                                    label="Nouvelles candidatures"
                                    description="Recevoir un email pour chaque nouvelle candidature"
                                    checked={notifications.newCandidates}
                                    onChange={(v) => setNotifications(prev => ({ ...prev, newCandidates: v }))}
                                />
                                <ToggleSetting
                                    label="Rappels de contrat"
                                    description="Rappel par email des contrats à signer"
                                    checked={notifications.contractReminders}
                                    onChange={(v) => setNotifications(prev => ({ ...prev, contractReminders: v }))}
                                />
                                <ToggleSetting
                                    label="Alertes disponibilité"
                                    description="Notifications quand un talent favori est disponible"
                                    checked={notifications.availabilityAlerts}
                                    onChange={(v) => setNotifications(prev => ({ ...prev, availabilityAlerts: v }))}
                                />
                            </div>
                        </SettingsSection>
                    </motion.div>
                )}

                {/* Security Tab */}
                {activeTab === 'security' && (
                    <motion.div
                        key="security"
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 10 }}
                    >
                        <SettingsSection
                            title="Sécurité"
                            description="Mot de passe et authentification"
                            icon={Shield}
                        >
                            <div className="space-y-4">
                                <button className="rounded-lg border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-50">
                                    Changer le mot de passe
                                </button>
                                <div className="pt-4 border-t border-slate-100">
                                    <h4 className="text-sm font-medium text-slate-900 mb-2">
                                        Authentification à deux facteurs
                                    </h4>
                                    <p className="text-sm text-slate-500 mb-3">
                                        Ajoutez une couche de sécurité supplémentaire à votre compte.
                                    </p>
                                    <button className="rounded-lg bg-teal-600 px-4 py-2 text-sm font-medium text-white hover:bg-teal-700 transition-colors">
                                        Activer la 2FA
                                    </button>
                                </div>
                            </div>
                        </SettingsSection>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Save Button (not shown on Compliance tab) */}
            {activeTab !== 'compliance' && (
                <motion.div
                    variants={itemVariants}
                    className="flex justify-end border-t border-slate-200 pt-6"
                >
                    <button className="inline-flex items-center gap-2 rounded-lg bg-teal-600 px-6 py-2.5 text-sm font-medium text-white shadow-sm transition-colors hover:bg-teal-700">
                        <Save className="h-4 w-4" />
                        Enregistrer les modifications
                    </button>
                </motion.div>
            )}
        </motion.div>
    );
}

// Sub-components

interface SettingsSectionProps {
    title: string;
    description: string;
    icon: React.ElementType;
    children: React.ReactNode;
    badge?: React.ReactNode;
}

function SettingsSection({ title, description, icon: Icon, children, badge }: SettingsSectionProps) {
    return (
        <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="mb-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="rounded-lg bg-slate-100 p-2 text-slate-600">
                        <Icon className="h-5 w-5" />
                    </div>
                    <div>
                        <h2 className="font-semibold text-slate-900">{title}</h2>
                        <p className="text-sm text-slate-500">{description}</p>
                    </div>
                </div>
                {badge}
            </div>
            {children}
        </div>
    );
}

interface FormInputProps {
    label: string;
    value: string;
    onChange: (value: string) => void;
    placeholder?: string;
    error?: string;
    success?: boolean;
    required?: boolean;
}

function FormInput({ label, value, onChange, placeholder, error, success, required }: FormInputProps) {
    return (
        <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">
                {label}
                {required && <span className="ml-1 text-rose-500">*</span>}
            </label>
            <div className="relative">
                <input
                    type="text"
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    placeholder={placeholder}
                    className={`w-full rounded-lg border px-3 py-2 text-sm transition-colors focus:outline-none focus:ring-1 ${error
                            ? 'border-rose-300 focus:border-rose-500 focus:ring-rose-500'
                            : success
                                ? 'border-emerald-300 focus:border-emerald-500 focus:ring-emerald-500'
                                : 'border-slate-200 focus:border-teal-500 focus:ring-teal-500'
                        }`}
                />
                {success && (
                    <CheckCircle className="absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-emerald-500" />
                )}
            </div>
            {error && <p className="mt-1 text-xs text-rose-600">{error}</p>}
        </div>
    );
}

interface FormSelectProps {
    label: string;
    value: string;
    onChange: (value: string) => void;
    options: { value: string; label: string }[];
}

function FormSelect({ label, value, onChange, options }: FormSelectProps) {
    return (
        <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">{label}</label>
            <select
                value={value}
                onChange={(e) => onChange(e.target.value)}
                aria-label={label}
                className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm transition-colors focus:border-teal-500 focus:outline-none focus:ring-1 focus:ring-teal-500"
            >
                {options.map((opt) => (
                    <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
            </select>
        </div>
    );
}

interface ToggleSettingProps {
    label: string;
    description: string;
    checked: boolean;
    onChange: (checked: boolean) => void;
}

function ToggleSetting({ label, description, checked, onChange }: ToggleSettingProps) {
    return (
        <div className="flex items-center justify-between">
            <div>
                <p className="text-sm font-medium text-slate-900">{label}</p>
                <p className="text-sm text-slate-500">{description}</p>
            </div>
            <button
                type="button"
                onClick={() => onChange(!checked)}
                aria-label={`Toggle ${label}`}
                className={`relative h-6 w-11 rounded-full transition-colors ${checked ? 'bg-teal-500' : 'bg-slate-200'
                    }`}
            >
                <span
                    className={`absolute top-0.5 h-5 w-5 rounded-full bg-white shadow transition-transform ${checked ? 'left-5' : 'left-0.5'
                        }`}
                />
            </button>
        </div>
    );
}
