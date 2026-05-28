'use client';

import { useState, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Upload,
    Clock,
    ShieldCheck,
    AlertCircle,
    Eye,
    RefreshCw,
    FileText,
    X,
    CheckCircle2,
} from 'lucide-react';

// =============================================================================
// DOCUMENT CARD - Smart Upload Component
// Mockup Mode with simulated upload flow
// =============================================================================

export type DocumentStatus = 'MISSING' | 'UPLOADING' | 'PENDING' | 'VALIDATED' | 'REJECTED';

export interface DocumentCardProps {
    /** Document title (e.g., "KBIS", "Diplôme") */
    title: string;
    /** Document description */
    description?: string;
    /** Current status */
    status: DocumentStatus;
    /** Rejection reason (when status is REJECTED) */
    rejectionReason?: string;
    /** File name when uploaded */
    fileName?: string;
    /** Callback when file is uploaded */
    onUpload?: (file: File) => void;
    /** Callback when "View" is clicked */
    onView?: () => void;
    /** Callback when status changes (for controlled mode) */
    onStatusChange?: (status: DocumentStatus) => void;
    /** Whether to use internal state simulation (Mockup Mode) */
    mockupMode?: boolean;
    /** Accent color variant */
    variant?: 'primary' | 'teal' | 'rose';
    /** Custom icon to display in header (ReactNode) */
    icon?: React.ReactNode;
}

// Status configuration
const STATUS_CONFIG = {
    MISSING: {
        icon: Upload,
        label: 'À fournir',
        bg: 'bg-slate-50',
        border: 'border-slate-300 border-dashed',
        text: 'text-slate-500',
        iconColor: 'text-slate-400',
    },
    UPLOADING: {
        icon: Upload,
        label: 'Envoi en cours...',
        bg: 'bg-blue-50',
        border: 'border-blue-200',
        text: 'text-blue-600',
        iconColor: 'text-blue-500',
    },
    PENDING: {
        icon: Clock,
        label: 'En cours de validation',
        bg: 'bg-amber-50',
        border: 'border-amber-200',
        text: 'text-amber-700',
        iconColor: 'text-amber-500',
    },
    VALIDATED: {
        icon: ShieldCheck,
        label: 'Vérifié',
        bg: 'bg-emerald-50',
        border: 'border-emerald-200',
        text: 'text-emerald-700',
        iconColor: 'text-emerald-500',
    },
    REJECTED: {
        icon: AlertCircle,
        label: 'Refusé',
        bg: 'bg-rose-50',
        border: 'border-rose-200',
        text: 'text-rose-700',
        iconColor: 'text-rose-500',
    },
};

export function DocumentCard({
    title,
    description,
    status: externalStatus,
    rejectionReason = 'Document illisible',
    fileName,
    onUpload,
    onView,
    onStatusChange,
    mockupMode = true,
    variant = 'primary',
    icon,
}: DocumentCardProps) {
    // Internal state for mockup mode
    const [internalStatus, setInternalStatus] = useState<DocumentStatus>(externalStatus);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [uploadedFileName, setUploadedFileName] = useState<string | undefined>(fileName);
    const fileInputRef = useRef<HTMLInputElement>(null);

    // Use internal or external status based on mockup mode
    const status = mockupMode ? internalStatus : externalStatus;
    const config = STATUS_CONFIG[status];
    const StatusIcon = config.icon;

    // Handle file selection
    const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        setUploadedFileName(file.name);

        if (mockupMode) {
            // Simulate upload with progress
            setInternalStatus('UPLOADING');
            setUploadProgress(0);

            const duration = 2000; // 2 seconds
            const startTime = Date.now();

            const animateProgress = () => {
                const elapsed = Date.now() - startTime;
                const progress = Math.min((elapsed / duration) * 100, 100);
                setUploadProgress(progress);

                if (progress < 100) {
                    requestAnimationFrame(animateProgress);
                } else {
                    // Upload complete - change to PENDING
                    setTimeout(() => {
                        setInternalStatus('PENDING');
                        onStatusChange?.('PENDING');
                    }, 200);
                }
            };

            requestAnimationFrame(animateProgress);
        }

        onUpload?.(file);
        
        // Reset input to allow re-upload of same file
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    }, [mockupMode, onUpload, onStatusChange]);

    // Trigger file input click
    const handleUploadClick = () => {
        fileInputRef.current?.click();
    };

    // Handle retry (reset to MISSING)
    const handleRetry = () => {
        if (mockupMode) {
            setInternalStatus('MISSING');
            setUploadedFileName(undefined);
            onStatusChange?.('MISSING');
        }
        handleUploadClick();
    };

    // Accent colors based on variant
    const accentColors = {
        primary: 'bg-indigo-600 hover:bg-indigo-700',
        teal: 'bg-teal-600 hover:bg-teal-700',
        rose: 'bg-rose-600 hover:bg-rose-700',
    };

    return (
        <motion.div
            layout
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`
                relative rounded-xl border-2 p-4 transition-all duration-300
                ${config.bg} ${config.border}
            `}
        >
            {/* Hidden file input */}
            <input
                ref={fileInputRef}
                type="file"
                className="hidden"
                accept=".pdf,.jpg,.jpeg,.png,.doc,.docx"
                onChange={handleFileSelect}
                title="Sélectionner un fichier"
                aria-label="Sélectionner un fichier à uploader"
            />

            {/* Header */}
            <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-3">
                    {/* Status Icon or Custom Icon */}
                    <div className={`
                        flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center
                        ${status === 'VALIDATED' ? 'bg-emerald-100' : 
                          status === 'REJECTED' ? 'bg-rose-100' :
                          status === 'PENDING' ? 'bg-amber-100' :
                          status === 'UPLOADING' ? 'bg-blue-100' : 'bg-slate-100'}
                    `}>
                        {icon ? (
                            <span className={config.iconColor}>{icon}</span>
                        ) : (
                            <StatusIcon className={`w-5 h-5 ${config.iconColor}`} />
                        )}
                    </div>

                    {/* Title & Description */}
                    <div>
                        <h3 className="font-semibold text-slate-900">{title}</h3>
                        {description && (
                            <p className="text-sm text-slate-500 mt-0.5">{description}</p>
                        )}
                    </div>
                </div>

                {/* Status Badge */}
                <span className={`
                    flex-shrink-0 px-2.5 py-1 rounded-full text-xs font-semibold
                    ${config.bg} ${config.text} border ${config.border.replace('border-dashed', '')}
                `}>
                    {config.label}
                </span>
            </div>

            {/* Content based on status */}
            <AnimatePresence mode="wait">
                {/* MISSING State - Upload Area */}
                {status === 'MISSING' && (
                    <motion.div
                        key="missing"
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="mt-4"
                    >
                        <button
                            onClick={handleUploadClick}
                            className="
                                w-full py-6 rounded-lg border-2 border-dashed border-slate-300
                                bg-white/50 hover:bg-white hover:border-slate-400
                                transition-all duration-200 group
                                flex flex-col items-center justify-center gap-2
                            "
                        >
                            <div className="w-12 h-12 rounded-full bg-slate-100 group-hover:bg-slate-200 flex items-center justify-center transition-colors">
                                <Upload className="w-6 h-6 text-slate-400 group-hover:text-slate-600" />
                            </div>
                            <span className="text-sm font-medium text-slate-600">
                                Cliquez pour téléverser
                            </span>
                            <span className="text-xs text-slate-400">
                                PDF, JPG, PNG (max 5 Mo)
                            </span>
                        </button>
                    </motion.div>
                )}

                {/* UPLOADING State - Progress Bar */}
                {status === 'UPLOADING' && (
                    <motion.div
                        key="uploading"
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="mt-4"
                    >
                        <div className="bg-white rounded-lg p-4 border border-blue-100">
                            <div className="flex items-center gap-3 mb-3">
                                <FileText className="w-5 h-5 text-blue-500" />
                                <span className="text-sm font-medium text-slate-700 truncate flex-1">
                                    {uploadedFileName || 'document.pdf'}
                                </span>
                                <span className="text-sm font-semibold text-blue-600">
                                    {Math.round(uploadProgress)}%
                                </span>
                            </div>
                            
                            {/* Progress Bar */}
                            <div className="h-2 bg-blue-100 rounded-full overflow-hidden">
                                <motion.div
                                    className="h-full bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full"
                                    initial={{ width: 0 }}
                                    animate={{ width: `${uploadProgress}%` }}
                                    transition={{ duration: 0.1, ease: 'linear' }}
                                />
                            </div>
                        </div>
                    </motion.div>
                )}

                {/* PENDING State - Waiting Message */}
                {status === 'PENDING' && (
                    <motion.div
                        key="pending"
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="mt-4"
                    >
                        <div className="bg-white rounded-lg p-4 border border-amber-100">
                            <div className="flex items-center gap-3">
                                <div className="relative">
                                    <Clock className="w-5 h-5 text-amber-500" />
                                    <motion.div
                                        className="absolute inset-0"
                                        animate={{ rotate: 360 }}
                                        transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
                                    >
                                        <div className="w-1.5 h-1.5 bg-amber-500 rounded-full absolute top-0 left-1/2 -translate-x-1/2" />
                                    </motion.div>
                                </div>
                                <div className="flex-1">
                                    <p className="text-sm font-medium text-slate-700">
                                        En cours de validation par SocioPulse
                                    </p>
                                    <p className="text-xs text-slate-500 mt-0.5">
                                        Délai moyen : 24-48h ouvrées
                                    </p>
                                </div>
                            </div>
                            
                            {uploadedFileName && (
                                <div className="mt-3 pt-3 border-t border-amber-100 flex items-center gap-2">
                                    <FileText className="w-4 h-4 text-slate-400" />
                                    <span className="text-xs text-slate-500 truncate">
                                        {uploadedFileName}
                                    </span>
                                </div>
                            )}
                        </div>
                    </motion.div>
                )}

                {/* VALIDATED State - Success */}
                {status === 'VALIDATED' && (
                    <motion.div
                        key="validated"
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="mt-4"
                    >
                        <div className="bg-white rounded-lg p-4 border border-emerald-100">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                                    <div>
                                        <p className="text-sm font-medium text-emerald-700">
                                            Document vérifié et validé
                                        </p>
                                        {uploadedFileName && (
                                            <p className="text-xs text-slate-500 mt-0.5 truncate max-w-[200px]">
                                                {uploadedFileName}
                                            </p>
                                        )}
                                    </div>
                                </div>
                                
                                <button
                                    onClick={onView}
                                    className="
                                        px-3 py-1.5 rounded-lg text-sm font-medium
                                        bg-emerald-100 text-emerald-700 hover:bg-emerald-200
                                        transition-colors flex items-center gap-1.5
                                    "
                                >
                                    <Eye className="w-4 h-4" />
                                    Voir
                                </button>
                            </div>
                        </div>
                    </motion.div>
                )}

                {/* REJECTED State - Error */}
                {status === 'REJECTED' && (
                    <motion.div
                        key="rejected"
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="mt-4"
                    >
                        <div className="bg-white rounded-lg p-4 border border-rose-100">
                            <div className="flex items-start gap-3">
                                <X className="w-5 h-5 text-rose-500 flex-shrink-0 mt-0.5" />
                                <div className="flex-1">
                                    <p className="text-sm font-medium text-rose-700">
                                        Document refusé
                                    </p>
                                    <p className="text-xs text-rose-600 mt-1 bg-rose-50 px-2 py-1 rounded">
                                        <span className="font-semibold">Motif :</span> {rejectionReason}
                                    </p>
                                </div>
                            </div>
                            
                            <button
                                onClick={handleRetry}
                                className={`
                                    mt-3 w-full py-2 rounded-lg text-sm font-semibold text-white
                                    ${accentColors[variant]} transition-colors
                                    flex items-center justify-center gap-2
                                `}
                            >
                                <RefreshCw className="w-4 h-4" />
                                Réessayer
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
}

// =============================================================================
// DOCUMENT CARD LIST - Helper component for displaying multiple documents
// =============================================================================

export interface DocumentItem {
    id: string;
    title: string;
    description?: string;
    status: DocumentStatus;
    rejectionReason?: string;
    fileName?: string;
}

interface DocumentCardListProps {
    documents: DocumentItem[];
    onUpload?: (id: string, file: File) => void;
    onView?: (id: string) => void;
    onStatusChange?: (id: string, status: DocumentStatus) => void;
    mockupMode?: boolean;
    variant?: 'primary' | 'teal' | 'rose';
}

export function DocumentCardList({
    documents,
    onUpload,
    onView,
    onStatusChange,
    mockupMode = true,
    variant = 'primary',
}: DocumentCardListProps) {
    return (
        <div className="space-y-4">
            {documents.map((doc) => (
                <DocumentCard
                    key={doc.id}
                    title={doc.title}
                    description={doc.description}
                    status={doc.status}
                    rejectionReason={doc.rejectionReason}
                    fileName={doc.fileName}
                    onUpload={(file) => onUpload?.(doc.id, file)}
                    onView={() => onView?.(doc.id)}
                    onStatusChange={(status) => onStatusChange?.(doc.id, status)}
                    mockupMode={mockupMode}
                    variant={variant}
                />
            ))}
        </div>
    );
}

export default DocumentCard;
