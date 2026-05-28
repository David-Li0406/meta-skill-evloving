'use client';

import { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, X, Check, AlertTriangle, FileSpreadsheet, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import { importTalentsAction, type ImportResult } from '@/app/actions/import-talents';

interface TalentImportModalProps {
    isOpen: boolean;
    onClose: () => void;
    establishmentId: string; // Passed from parent or context
}

export function TalentImportModal({ isOpen, onClose, establishmentId }: TalentImportModalProps) {
    const [uploading, setUploading] = useState(false);
    const [result, setResult] = useState<ImportResult | null>(null);

    const onDrop = async (acceptedFiles: File[]) => {
        if (acceptedFiles.length === 0) return;

        const file = acceptedFiles[0];
        const formData = new FormData();
        formData.append('file', file);
        formData.append('establishmentId', establishmentId);

        setUploading(true);
        setResult(null);

        try {
            const res = await importTalentsAction(formData);
            setResult(res);
            if (res.errors.length === 0) {
                toast.success(`${res.success} talents importés avec succès !`);
            } else {
                toast.warning(`${res.success} importés, ${res.errors.length} erreurs.`);
            }
        } catch (error: any) {
            console.error(error);
            toast.error("Erreur lors de l'import : " + error.message);
        } finally {
            setUploading(false);
        }
    };

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
            'application/vnd.ms-excel': ['.xls'],
            'text/csv': ['.csv']
        },
        maxFiles: 1,
        disabled: uploading
    });

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
            <div className="bg-white rounded-2xl shadow-xl w-full max-w-lg overflow-hidden flex flex-col max-h-[90vh]">
                {/* Header */}
                <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100">
                    <h3 className="text-lg font-semibold text-slate-900">Importer des vacataires</h3>
                    <button
                        onClick={onClose}
                        className="p-2 rounded-full hover:bg-slate-100 text-slate-500 transition-colors"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Content */}
                <div className="p-6 overflow-y-auto">
                    {!result ? (
                        <>
                            <div
                                {...getRootProps()}
                                className={`
                  border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all
                  ${isDragActive ? 'border-brand-500 bg-brand-50' : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50'}
                  ${uploading ? 'opacity-50 cursor-not-allowed' : ''}
                `}
                            >
                                <input {...getInputProps()} />
                                <div className="flex flex-col items-center gap-3">
                                    {uploading ? (
                                        <Loader2 className="w-10 h-10 text-brand-600 animate-spin" />
                                    ) : (
                                        <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center text-slate-500">
                                            <Upload className="w-6 h-6" />
                                        </div>
                                    )}

                                    <div className="space-y-1">
                                        <p className="font-medium text-slate-900">
                                            {uploading ? "Importation en cours..." : "Cliquez ou glissez un fichier ici"}
                                        </p>
                                        <p className="text-sm text-slate-500">
                                            Supporte .xlsx, .xls, .csv
                                        </p>
                                    </div>
                                </div>
                            </div>

                            <div className="mt-4 bg-slate-50 rounded-lg p-4 text-sm text-slate-600">
                                <p className="font-medium mb-2 flex items-center gap-2">
                                    <FileSpreadsheet className="w-4 h-4" />
                                    Format attendu :
                                </p>
                                <ul className="list-disc list-inside space-y-1 ml-1">
                                    <li>Colonnes : Prénom, Nom, Email, Métier</li>
                                    <li>Optionnel : Téléphone, Tags</li>
                                </ul>
                            </div>
                        </>
                    ) : (
                        <div className="space-y-4">
                            {/* Résumé */}
                            <div className="grid grid-cols-2 gap-4">
                                <div className="bg-emerald-50 text-emerald-700 p-4 rounded-xl flex flex-col items-center justify-center text-center">
                                    <span className="text-2xl font-bold">{result.success}</span>
                                    <span className="text-sm font-medium flex items-center gap-1">
                                        <Check className="w-4 h-4" /> Importés
                                    </span>
                                </div>
                                <div className={`p-4 rounded-xl flex flex-col items-center justify-center text-center ${result.errors.length > 0 ? 'bg-amber-50 text-amber-700' : 'bg-slate-50 text-slate-500'}`}>
                                    <span className="text-2xl font-bold">{result.errors.length}</span>
                                    <span className="text-sm font-medium flex items-center gap-1">
                                        <AlertTriangle className="w-4 h-4" /> Erreurs
                                    </span>
                                </div>
                            </div>

                            {/* Liste des erreurs */}
                            {result.errors.length > 0 && (
                                <div className="border border-amber-100 rounded-xl overflow-hidden">
                                    <div className="bg-amber-50 px-4 py-2 text-xs font-semibold text-amber-700 uppercase tracking-wider">
                                        Détails des erreurs
                                    </div>
                                    <div className="max-h-48 overflow-y-auto divide-y divide-amber-100">
                                        {result.errors.map((err, idx) => (
                                            <div key={idx} className="px-4 py-3 text-sm">
                                                <div className="flex items-start gap-2">
                                                    <span className="font-mono text-amber-600 bg-amber-100 px-1.5 rounded text-xs mt-0.5">
                                                        Ligne {err.row}
                                                    </span>
                                                    <div className="flex-1">
                                                        <p className="text-slate-900 font-medium">{err.data?.email || 'N/A'}</p>
                                                        <p className="text-amber-600">{err.error}</p>
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            <div className="pt-2 flex justify-end">
                                <button
                                    onClick={() => setResult(null)}
                                    className="text-sm text-slate-500 hover:text-slate-900 font-medium px-4 py-2 hover:bg-slate-100 rounded-lg transition-colors"
                                >
                                    Importer un autre fichier
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
