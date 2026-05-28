'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    FileText,
    Download,
    Eye,
    Clock,
    CheckCircle2,
    AlertCircle,
    Euro,
    Calendar,
    Building2,
    Search,
    FileCheck,
    Receipt,
    Pen,
    XCircle,
    ShieldCheck,
    Award,
    Star,
    UserCheck,
    GraduationCap,
    Scale,
    Shield,
    Info,
} from 'lucide-react';
import { Card, CardContent, Button, Badge, Input, DocumentCard, type DocumentStatus } from '@/components/ui';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';

// =============================================================================
// TYPES
// =============================================================================

type ContractStatus = 'DRAFT' | 'PENDING_SIGNATURE' | 'SIGNED' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED';
type InvoiceStatus = 'PENDING' | 'PAID' | 'OVERDUE';
type MainTab = 'documents' | 'verification';

interface Contract {
    id: string;
    reference: string;
    title: string;
    client: {
        name: string;
        type: string;
    };
    type: 'MISSION_SOS' | 'SERVICE_BOOKING' | 'FRAMEWORK';
    status: ContractStatus;
    amount: number;
    startDate: string;
    endDate?: string;
    signedAt?: string;
}

interface Invoice {
    id: string;
    reference: string;
    contractRef: string;
    client: string;
    amount: number;
    status: InvoiceStatus;
    issuedAt: string;
    dueDate: string;
    paidAt?: string;
}

// Verification documents
interface VerificationDocument {
    id: string;
    title: string;
    description: string;
    status: DocumentStatus;
    rejectionReason?: string;
    fileName?: string;
    icon: React.ElementType;
    required: boolean;
}

// Trust Level type
type TrustLevel = 'BEGINNER' | 'VERIFIED' | 'PREMIUM';

const VERIFICATION_STORAGE_KEY = 'sociopulse_talent_verification_docs';

// =============================================================================
// MOCK DATA
// =============================================================================

const mockContracts: Contract[] = [
    {
        id: '1',
        reference: 'CTR-2026-001',
        title: 'Mission Renfort AS - EHPAD Les Tilleuls',
        client: { name: 'EHPAD Les Tilleuls', type: 'EHPAD' },
        type: 'MISSION_SOS',
        status: 'PENDING_SIGNATURE',
        amount: 180,
        startDate: '2026-01-21',
    },
    {
        id: '2',
        reference: 'CTR-2026-002',
        title: 'Atelier Gestion du Stress',
        client: { name: 'MECS Horizon', type: 'MECS' },
        type: 'SERVICE_BOOKING',
        status: 'SIGNED',
        amount: 350,
        startDate: '2026-01-25',
        signedAt: '2026-01-18',
    },
    {
        id: '3',
        reference: 'CTR-2025-089',
        title: 'Contrat Cadre - Vacations IDE',
        client: { name: 'SSIAD Rhône', type: 'SSIAD' },
        type: 'FRAMEWORK',
        status: 'IN_PROGRESS',
        amount: 2400,
        startDate: '2025-09-01',
        endDate: '2026-08-31',
        signedAt: '2025-08-28',
    },
    {
        id: '4',
        reference: 'CTR-2026-003',
        title: 'Coaching Orientation Carrière x3',
        client: { name: 'Marie Dupont', type: 'Particulier' },
        type: 'SERVICE_BOOKING',
        status: 'COMPLETED',
        amount: 225,
        startDate: '2026-01-10',
        endDate: '2026-01-17',
        signedAt: '2026-01-08',
    },
];

const mockInvoices: Invoice[] = [
    {
        id: '1',
        reference: 'FAC-2026-001',
        contractRef: 'CTR-2025-089',
        client: 'SSIAD Rhône',
        amount: 600,
        status: 'PAID',
        issuedAt: '2026-01-05',
        dueDate: '2026-02-05',
        paidAt: '2026-01-12',
    },
    {
        id: '2',
        reference: 'FAC-2026-002',
        contractRef: 'CTR-2026-003',
        client: 'Marie Dupont',
        amount: 225,
        status: 'PENDING',
        issuedAt: '2026-01-17',
        dueDate: '2026-02-17',
    },
    {
        id: '3',
        reference: 'FAC-2025-045',
        contractRef: 'CTR-2025-078',
        client: 'Foyer Le Phare',
        amount: 180,
        status: 'OVERDUE',
        issuedAt: '2025-12-15',
        dueDate: '2026-01-15',
    },
];

// Initial verification documents - Demo setup
const initialVerificationDocs: Omit<VerificationDocument, 'icon'>[] = [
    {
        id: 'identity',
        title: 'Carte d\'Identité / Passeport',
        description: 'Recto et verso en cours de validité',
        status: 'MISSING',
        required: true,
    },
    {
        id: 'diploma',
        title: 'Diplôme le plus élevé',
        description: 'Ex: DEES, IDE, DEASS, CAFERUIS...',
        status: 'VALIDATED', // Pre-filled for demo
        fileName: 'diplome_dees_2019.pdf',
        required: true,
    },
    {
        id: 'criminal',
        title: 'Casier Judiciaire B3',
        description: 'Extrait de moins de 3 mois',
        status: 'MISSING', // Left for user to try upload
        required: true,
    },
    {
        id: 'insurance',
        title: 'Assurance Responsabilité Civile',
        description: 'Attestation RC Pro en cours de validité',
        status: 'MISSING',
        required: true,
    },
];

// Trust level configuration
const TRUST_LEVELS: Record<TrustLevel, { label: string; color: string; bgColor: string; borderColor: string; minDocs: number }> = {
    BEGINNER: {
        label: 'Débutant',
        color: 'text-slate-500',
        bgColor: 'bg-slate-100',
        borderColor: 'border-slate-300',
        minDocs: 0,
    },
    VERIFIED: {
        label: 'Vérifié',
        color: 'text-blue-600',
        bgColor: 'bg-blue-100',
        borderColor: 'border-blue-400',
        minDocs: 2,
    },
    PREMIUM: {
        label: 'Premium',
        color: 'text-amber-600',
        bgColor: 'bg-gradient-to-r from-amber-100 to-yellow-100',
        borderColor: 'border-amber-400',
        minDocs: 4,
    },
};

// =============================================================================
// COMPONENTS
// =============================================================================

// Trust Score Gauge Component
function TrustScoreGauge({ validatedCount, totalCount }: { validatedCount: number; totalCount: number }) {
    // Determine trust level based on validated docs
    const getTrustLevel = (): TrustLevel => {
        if (validatedCount >= totalCount) return 'PREMIUM';
        if (validatedCount >= 2) return 'VERIFIED';
        return 'BEGINNER';
    };

    const trustLevel = getTrustLevel();
    const config = TRUST_LEVELS[trustLevel];
    const percentage = (validatedCount / totalCount) * 100;

    // Arc calculation for semi-circle gauge
    const radius = 80;
    const strokeWidth = 12;
    const circumference = Math.PI * radius;
    const offset = circumference - (percentage / 100) * circumference;

    return (
        <div className="flex flex-col items-center">
            {/* Gauge */}
            <div className="relative w-48 h-28">
                <svg
                    viewBox="0 0 200 110"
                    className="w-full h-full"
                >
                    {/* Background arc */}
                    <path
                        d="M 20 100 A 80 80 0 0 1 180 100"
                        fill="none"
                        stroke="#e2e8f0"
                        strokeWidth={strokeWidth}
                        strokeLinecap="round"
                    />
                    {/* Progress arc */}
                    <motion.path
                        d="M 20 100 A 80 80 0 0 1 180 100"
                        fill="none"
                        stroke={
                            trustLevel === 'PREMIUM' ? '#f59e0b' :
                            trustLevel === 'VERIFIED' ? '#3b82f6' : '#94a3b8'
                        }
                        strokeWidth={strokeWidth}
                        strokeLinecap="round"
                        strokeDasharray={circumference}
                        initial={{ strokeDashoffset: circumference }}
                        animate={{ strokeDashoffset: offset }}
                        transition={{ duration: 1.2, ease: 'easeOut' }}
                    />
                    {/* Level markers */}
                    <circle cx="20" cy="100" r="4" fill="#94a3b8" />
                    <circle cx="100" cy="20" r="4" fill="#3b82f6" />
                    <circle cx="180" cy="100" r="4" fill="#f59e0b" />
                </svg>
                
                {/* Center content */}
                <div className="absolute inset-0 flex flex-col items-center justify-end pb-2">
                    <motion.div
                        initial={{ scale: 0.5, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        transition={{ delay: 0.5, duration: 0.3 }}
                        className={cn(
                            'p-2 rounded-full',
                            trustLevel === 'PREMIUM' ? 'bg-amber-100' :
                            trustLevel === 'VERIFIED' ? 'bg-blue-100' : 'bg-slate-100'
                        )}
                    >
                        {trustLevel === 'PREMIUM' ? (
                            <Star className="h-6 w-6 text-amber-500 fill-amber-500" />
                        ) : trustLevel === 'VERIFIED' ? (
                            <ShieldCheck className="h-6 w-6 text-blue-500" />
                        ) : (
                            <UserCheck className="h-6 w-6 text-slate-400" />
                        )}
                    </motion.div>
                </div>
            </div>

            {/* Label */}
            <motion.div
                initial={{ y: 10, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.7 }}
                className="text-center mt-2"
            >
                <h3 className="text-lg font-bold text-slate-900">Niveau de Confiance</h3>
                <div className={cn(
                    'inline-flex items-center gap-2 mt-2 px-4 py-1.5 rounded-full border-2',
                    config.bgColor,
                    config.borderColor
                )}>
                    {trustLevel === 'PREMIUM' && <Award className="h-4 w-4 text-amber-500" />}
                    {trustLevel === 'VERIFIED' && <ShieldCheck className="h-4 w-4 text-blue-500" />}
                    <span className={cn('font-bold', config.color)}>
                        {config.label}
                    </span>
                </div>
                <p className="text-sm text-slate-500 mt-2">
                    {validatedCount}/{totalCount} documents validés
                </p>
            </motion.div>
        </div>
    );
}

// Document icon mapping
const DOC_ICONS: Record<string, React.ElementType> = {
    identity: UserCheck,
    diploma: GraduationCap,
    criminal: Scale,
    insurance: Shield,
};

function ContractStatusBadge({ status }: { status: ContractStatus }) {
    const config = {
        DRAFT: { label: 'Brouillon', icon: FileText, className: 'bg-slate-100 text-slate-600' },
        PENDING_SIGNATURE: { label: 'À signer', icon: Pen, className: 'bg-amber-100 text-amber-700' },
        SIGNED: { label: 'Signé', icon: FileCheck, className: 'bg-emerald-100 text-emerald-700' },
        IN_PROGRESS: { label: 'En cours', icon: Clock, className: 'bg-blue-100 text-blue-700' },
        COMPLETED: { label: 'Terminé', icon: CheckCircle2, className: 'bg-slate-100 text-slate-600' },
        CANCELLED: { label: 'Annulé', icon: XCircle, className: 'bg-rose-100 text-rose-600' },
    };

    const { label, icon: Icon, className } = config[status];

    return (
        <span className={cn('inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold rounded-full', className)}>
            <Icon size={12} />
            {label}
        </span>
    );
}

function InvoiceStatusBadge({ status }: { status: InvoiceStatus }) {
    const config = {
        PENDING: { label: 'En attente', className: 'bg-amber-100 text-amber-700' },
        PAID: { label: 'Payée', className: 'bg-emerald-100 text-emerald-700' },
        OVERDUE: { label: 'En retard', className: 'bg-rose-100 text-rose-700' },
    };

    const { label, className } = config[status];

    return (
        <span className={cn('px-2.5 py-1 text-xs font-semibold rounded-full', className)}>
            {label}
        </span>
    );
}

function ContractTypeBadge({ type }: { type: Contract['type'] }) {
    const config = {
        MISSION_SOS: { label: 'Mission SOS', className: 'bg-rose-50 text-rose-600 border-rose-200' },
        SERVICE_BOOKING: { label: 'Service', className: 'bg-teal-50 text-teal-600 border-teal-200' },
        FRAMEWORK: { label: 'Contrat Cadre', className: 'bg-indigo-50 text-indigo-600 border-indigo-200' },
    };

    const { label, className } = config[type];

    return (
        <span className={cn('px-2 py-0.5 text-xs font-medium rounded border', className)}>
            {label}
        </span>
    );
}

function ContractRow({ contract }: { contract: Contract }) {
    const formatDate = (dateStr: string) => {
        return new Date(dateStr).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' });
    };

    return (
        <div className="flex items-center gap-4 p-4 hover:bg-slate-50 rounded-xl transition-colors border border-transparent hover:border-slate-200">
            <div className="p-2 bg-slate-100 rounded-lg">
                <FileText size={20} className="text-slate-600" />
            </div>
            <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-mono text-slate-400">{contract.reference}</span>
                    <ContractTypeBadge type={contract.type} />
                </div>
                <h3 className="font-semibold text-slate-900 truncate">{contract.title}</h3>
                <div className="flex items-center gap-3 mt-1 text-sm text-slate-500">
                    <span className="flex items-center gap-1">
                        <Building2 size={12} />
                        {contract.client.name}
                    </span>
                    <span className="flex items-center gap-1">
                        <Calendar size={12} />
                        {formatDate(contract.startDate)}
                    </span>
                </div>
            </div>
            <div className="text-right">
                <p className="font-bold text-slate-900">{contract.amount}€</p>
                <ContractStatusBadge status={contract.status} />
            </div>
            <div className="flex items-center gap-2">
                <Button variant="outline" size="sm" className="gap-1">
                    <Eye size={14} /> Voir
                </Button>
                {contract.status === 'PENDING_SIGNATURE' && (
                    <Button size="sm" className="bg-amber-500 hover:bg-amber-600 text-white gap-1">
                        <Pen size={14} /> Signer
                    </Button>
                )}
            </div>
        </div>
    );
}

function InvoiceRow({ invoice }: { invoice: Invoice }) {
    const formatDate = (dateStr: string) => {
        return new Date(dateStr).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' });
    };

    return (
        <div className={cn(
            'flex items-center gap-4 p-4 rounded-xl transition-colors',
            invoice.status === 'OVERDUE' ? 'bg-rose-50 border border-rose-200' : 'hover:bg-slate-50'
        )}>
            <div className={cn(
                'p-2 rounded-lg',
                invoice.status === 'PAID' ? 'bg-emerald-100' :
                invoice.status === 'OVERDUE' ? 'bg-rose-100' : 'bg-amber-100'
            )}>
                <Receipt size={20} className={cn(
                    invoice.status === 'PAID' ? 'text-emerald-600' :
                    invoice.status === 'OVERDUE' ? 'text-rose-600' : 'text-amber-600'
                )} />
            </div>
            <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-mono text-slate-400">{invoice.reference}</span>
                    <span className="text-xs text-slate-400">→ {invoice.contractRef}</span>
                </div>
                <h3 className="font-semibold text-slate-900">{invoice.client}</h3>
                <div className="flex items-center gap-3 mt-1 text-sm text-slate-500">
                    <span>Émise le {formatDate(invoice.issuedAt)}</span>
                    <span className={cn(
                        invoice.status === 'OVERDUE' && 'text-rose-600 font-medium'
                    )}>
                        Échéance: {formatDate(invoice.dueDate)}
                    </span>
                </div>
            </div>
            <div className="text-right">
                <p className="font-bold text-slate-900">{invoice.amount}€</p>
                <InvoiceStatusBadge status={invoice.status} />
            </div>
            <Button variant="outline" size="sm" className="gap-1">
                <Download size={14} /> PDF
            </Button>
        </div>
    );
}

// =============================================================================
// PAGE
// =============================================================================

export default function TalentAdminPage() {
    const [mainTab, setMainTab] = useState<MainTab>('documents');
    const [activeTab, setActiveTab] = useState<'contracts' | 'invoices'>('contracts');
    const [searchQuery, setSearchQuery] = useState('');

    // Verification documents state
    const [verificationDocs, setVerificationDocs] = useState<VerificationDocument[]>(() => 
        initialVerificationDocs.map(doc => ({
            ...doc,
            icon: DOC_ICONS[doc.id] || FileCheck,
        }))
    );

    // Load verification docs from localStorage on mount
    useEffect(() => {
        const saved = localStorage.getItem(VERIFICATION_STORAGE_KEY);
        if (saved) {
            try {
                const parsed = JSON.parse(saved);
                setVerificationDocs(parsed.map((doc: Omit<VerificationDocument, 'icon'>) => ({
                    ...doc,
                    icon: DOC_ICONS[doc.id] || FileCheck,
                })));
            } catch {
                console.error('Failed to parse saved verification docs');
            }
        }
    }, []);

    // Save verification docs to localStorage when changed
    useEffect(() => {
        const toSave = verificationDocs.map(({ icon, ...rest }) => rest);
        localStorage.setItem(VERIFICATION_STORAGE_KEY, JSON.stringify(toSave));
    }, [verificationDocs]);

    // Calculate verified docs count
    const validatedCount = verificationDocs.filter(
        doc => doc.status === 'VALIDATED'
    ).length;
    const pendingOrValidatedCount = verificationDocs.filter(
        doc => doc.status === 'PENDING' || doc.status === 'VALIDATED'
    ).length;
    const totalDocs = verificationDocs.length;

    // Check if all docs are complete - show toast once
    const [hasShownCompleteToast, setHasShownCompleteToast] = useState(false);
    useEffect(() => {
        if (validatedCount === totalDocs && !hasShownCompleteToast) {
            toast.success('Félicitations ! Statut Premium débloqué 🌟', {
                description: 'Tous vos documents sont validés.',
                duration: 5000,
            });
            setHasShownCompleteToast(true);
        }
    }, [validatedCount, totalDocs, hasShownCompleteToast]);

    // Handle document status change
    const handleDocStatusChange = (docId: string, newStatus: DocumentStatus) => {
        setVerificationDocs(prev =>
            prev.map(doc =>
                doc.id === docId ? { ...doc, status: newStatus } : doc
            )
        );
    };

    // Handle document upload
    const handleDocUpload = (docId: string, file: File) => {
        setVerificationDocs(prev =>
            prev.map(doc =>
                doc.id === docId ? { ...doc, fileName: file.name } : doc
            )
        );
    };

    const stats = {
        pendingSignature: mockContracts.filter(c => c.status === 'PENDING_SIGNATURE').length,
        activeContracts: mockContracts.filter(c => c.status === 'IN_PROGRESS' || c.status === 'SIGNED').length,
        pendingInvoices: mockInvoices.filter(i => i.status === 'PENDING').length,
        overdueInvoices: mockInvoices.filter(i => i.status === 'OVERDUE').length,
        totalPending: mockInvoices.filter(i => i.status !== 'PAID').reduce((sum, i) => sum + i.amount, 0),
    };

    return (
        <div className="space-y-6 max-w-6xl mx-auto">
            {/* Header */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
                        <FileText className="text-slate-600" />
                        Administratif
                    </h1>
                    <p className="text-slate-500 mt-1">Contrats, Factures & Vérification</p>
                </div>
                {/* Trust Badge in header */}
                {validatedCount >= 2 && (
                    <Badge 
                        variant={validatedCount === totalDocs ? 'default' : 'secondary'}
                        size="lg"
                        className={cn(
                            validatedCount === totalDocs 
                                ? 'bg-gradient-to-r from-amber-500 to-yellow-500 text-white border-0' 
                                : 'bg-blue-100 text-blue-700 border-blue-200'
                        )}
                        icon={validatedCount === totalDocs ? <Star className="h-4 w-4 fill-current" /> : <ShieldCheck className="h-4 w-4" />}
                    >
                        {validatedCount === totalDocs ? 'Premium' : 'Vérifié'}
                    </Badge>
                )}
            </div>

            {/* Main Tabs: Documents vs Verification */}
            <div className="flex gap-2 border-b border-slate-200">
                <button
                    onClick={() => setMainTab('documents')}
                    className={cn(
                        'flex items-center gap-2 px-4 py-3 text-sm font-semibold border-b-2 transition-colors',
                        mainTab === 'documents'
                            ? 'border-teal-500 text-teal-600'
                            : 'border-transparent text-slate-500 hover:text-slate-700'
                    )}
                >
                    <FileText size={16} />
                    Contrats & Factures
                </button>
                <button
                    onClick={() => setMainTab('verification')}
                    className={cn(
                        'flex items-center gap-2 px-4 py-3 text-sm font-semibold border-b-2 transition-colors',
                        mainTab === 'verification'
                            ? 'border-teal-500 text-teal-600'
                            : 'border-transparent text-slate-500 hover:text-slate-700'
                    )}
                >
                    <ShieldCheck size={16} />
                    Vérification
                    {pendingOrValidatedCount < totalDocs && (
                        <span className="ml-1 px-1.5 py-0.5 text-xs rounded-full bg-amber-100 text-amber-700">
                            {pendingOrValidatedCount}/{totalDocs}
                        </span>
                    )}
                </button>
            </div>

            <AnimatePresence mode="wait">
                {/* Documents Tab Content */}
                {mainTab === 'documents' && (
                    <motion.div
                        key="documents"
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 10 }}
                        className="space-y-6"
                    >
                        {/* Stats */}
                        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                            <Card className={cn(
                                'border-2',
                                stats.pendingSignature > 0 ? 'border-amber-200 bg-amber-50/50' : 'border-slate-200'
                            )}>
                                <CardContent className="p-4">
                                    <div className="flex items-center gap-3">
                                        <div className="p-2 bg-amber-100 rounded-lg">
                                            <Pen size={18} className="text-amber-600" />
                                        </div>
                                        <div>
                                            <p className="text-2xl font-bold text-amber-700">{stats.pendingSignature}</p>
                                            <p className="text-xs text-amber-600">À signer</p>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                            <Card className="border-slate-200">
                                <CardContent className="p-4">
                                    <div className="flex items-center gap-3">
                                        <div className="p-2 bg-blue-100 rounded-lg">
                                            <FileCheck size={18} className="text-blue-600" />
                                        </div>
                                        <div>
                                            <p className="text-2xl font-bold text-blue-700">{stats.activeContracts}</p>
                                            <p className="text-xs text-slate-500">Contrats actifs</p>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                            <Card className={cn(
                                'border-2',
                                stats.overdueInvoices > 0 ? 'border-rose-200 bg-rose-50/50' : 'border-slate-200'
                            )}>
                                <CardContent className="p-4">
                                    <div className="flex items-center gap-3">
                                        <div className={cn(
                                            'p-2 rounded-lg',
                                            stats.overdueInvoices > 0 ? 'bg-rose-100' : 'bg-slate-100'
                                        )}>
                                            <AlertCircle size={18} className={cn(
                                                stats.overdueInvoices > 0 ? 'text-rose-600' : 'text-slate-600'
                                            )} />
                                        </div>
                                        <div>
                                            <p className={cn(
                                                'text-2xl font-bold',
                                                stats.overdueInvoices > 0 ? 'text-rose-700' : 'text-slate-700'
                                            )}>{stats.overdueInvoices}</p>
                                            <p className="text-xs text-slate-500">Factures en retard</p>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                            <Card className="border-slate-200">
                                <CardContent className="p-4">
                                    <div className="flex items-center gap-3">
                                        <div className="p-2 bg-emerald-100 rounded-lg">
                                            <Euro size={18} className="text-emerald-600" />
                                        </div>
                                        <div>
                                            <p className="text-2xl font-bold text-emerald-700">{stats.totalPending}€</p>
                                            <p className="text-xs text-slate-500">En attente</p>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        </div>

                        {/* Sub Tabs: Contracts vs Invoices */}
                        <div className="flex gap-2 border-b border-slate-200">
                            <button
                                onClick={() => setActiveTab('contracts')}
                                className={cn(
                                    'px-4 py-3 text-sm font-semibold border-b-2 transition-colors',
                                    activeTab === 'contracts'
                                        ? 'border-primary-600 text-primary-600'
                                        : 'border-transparent text-slate-500 hover:text-slate-700'
                                )}
                            >
                                Contrats ({mockContracts.length})
                            </button>
                            <button
                                onClick={() => setActiveTab('invoices')}
                                className={cn(
                                    'px-4 py-3 text-sm font-semibold border-b-2 transition-colors flex items-center gap-2',
                                    activeTab === 'invoices'
                                        ? 'border-primary-600 text-primary-600'
                                        : 'border-transparent text-slate-500 hover:text-slate-700'
                                )}
                            >
                                Factures ({mockInvoices.length})
                                {stats.overdueInvoices > 0 && (
                                    <span className="px-1.5 py-0.5 text-xs bg-rose-500 text-white rounded-full">
                                        {stats.overdueInvoices}
                                    </span>
                                )}
                            </button>
                        </div>

                        {/* Search */}
                        <div className="relative max-w-md">
                            <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                            <Input
                                placeholder="Rechercher par référence, client..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="pl-10"
                            />
                        </div>

                        {/* Content */}
                        <Card className="border-slate-200">
                            <CardContent className="p-0">
                                {activeTab === 'contracts' ? (
                                    <div className="divide-y divide-slate-100">
                                        {mockContracts.map((contract) => (
                                            <ContractRow key={contract.id} contract={contract} />
                                        ))}
                                    </div>
                                ) : (
                                    <div className="divide-y divide-slate-100">
                                        {mockInvoices.map((invoice) => (
                                            <InvoiceRow key={invoice.id} invoice={invoice} />
                                        ))}
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    </motion.div>
                )}

                {/* Verification Tab Content */}
                {mainTab === 'verification' && (
                    <motion.div
                        key="verification"
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 10 }}
                        className="space-y-6"
                    >
                        {/* Trust Score Header Card */}
                        <Card className="border-slate-200 overflow-hidden">
                            <CardContent className="p-6">
                                <div className="flex flex-col lg:flex-row items-center gap-8">
                                    {/* Gauge */}
                                    <TrustScoreGauge 
                                        validatedCount={validatedCount} 
                                        totalCount={totalDocs} 
                                    />
                                    
                                    {/* Level Explanation */}
                                    <div className="flex-1 space-y-4">
                                        <h2 className="text-lg font-semibold text-slate-900">
                                            Centre de Vérification
                                        </h2>
                                        <p className="text-sm text-slate-500">
                                            Complétez votre dossier pour augmenter votre niveau de confiance et accéder à plus de missions.
                                        </p>
                                        
                                        {/* Level Progress */}
                                        <div className="grid grid-cols-3 gap-3">
                                            <div className={cn(
                                                'p-3 rounded-lg border-2 text-center transition-all',
                                                validatedCount === 0 
                                                    ? 'border-slate-300 bg-slate-50' 
                                                    : 'border-slate-200 bg-white opacity-50'
                                            )}>
                                                <UserCheck className="h-5 w-5 mx-auto text-slate-400 mb-1" />
                                                <p className="text-xs font-medium text-slate-600">Débutant</p>
                                                <p className="text-xs text-slate-400">0 doc</p>
                                            </div>
                                            <div className={cn(
                                                'p-3 rounded-lg border-2 text-center transition-all',
                                                validatedCount >= 2 && validatedCount < totalDocs
                                                    ? 'border-blue-400 bg-blue-50' 
                                                    : 'border-slate-200 bg-white opacity-50'
                                            )}>
                                                <ShieldCheck className="h-5 w-5 mx-auto text-blue-500 mb-1" />
                                                <p className="text-xs font-medium text-blue-600">Vérifié</p>
                                                <p className="text-xs text-slate-400">2+ docs</p>
                                            </div>
                                            <div className={cn(
                                                'p-3 rounded-lg border-2 text-center transition-all',
                                                validatedCount === totalDocs
                                                    ? 'border-amber-400 bg-gradient-to-r from-amber-50 to-yellow-50' 
                                                    : 'border-slate-200 bg-white opacity-50'
                                            )}>
                                                <Star className="h-5 w-5 mx-auto text-amber-500 mb-1" />
                                                <p className="text-xs font-medium text-amber-600">Premium</p>
                                                <p className="text-xs text-slate-400">Tous docs</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>

                        {/* Document Cards Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {verificationDocs.map((doc) => {
                                const Icon = doc.icon;
                                return (
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
                                        icon={<Icon className="h-5 w-5" />}
                                    />
                                );
                            })}
                        </div>

                        {/* Help text */}
                        <div className="flex items-start gap-3 rounded-lg bg-sky-50 border border-sky-100 p-4">
                            <Info className="h-5 w-5 text-sky-600 flex-shrink-0 mt-0.5" />
                            <div>
                                <p className="text-sm font-medium text-sky-800">
                                    Pourquoi ces documents ?
                                </p>
                                <p className="text-sm text-sky-700 mt-1">
                                    Ces pièces justificatives sont requises par les établissements partenaires 
                                    pour garantir la sécurité et la conformité réglementaire de leurs équipes. 
                                    Vérification sous 24-48h ouvrées.
                                </p>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
