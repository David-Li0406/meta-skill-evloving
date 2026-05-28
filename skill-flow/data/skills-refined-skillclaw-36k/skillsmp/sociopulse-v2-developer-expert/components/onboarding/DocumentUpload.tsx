'use client';

import { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Upload,
    X,
    FileText,
    Check,
    AlertCircle,
    Image as ImageIcon
} from 'lucide-react';

interface UploadedFile {
    id: string;
    name: string;
    size: number;
    type: string;
    preview?: string;
    status: 'uploading' | 'success' | 'error';
    progress: number;
}

interface DocumentUploadProps {
    label: string;
    description?: string;
    accept?: string;
    maxSize?: number; // in MB
    multiple?: boolean;
    required?: boolean;
    onFilesChange?: (files: UploadedFile[]) => void;
}

function formatFileSize(bytes: number): string {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function DocumentUpload({
    label,
    description,
    accept = '.pdf,.jpg,.jpeg,.png',
    maxSize = 5,
    multiple = false,
    required = false,
    onFilesChange,
}: DocumentUploadProps) {
    const [files, setFiles] = useState<UploadedFile[]>([]);
    const [isDragging, setIsDragging] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const processFiles = useCallback((fileList: FileList | File[]) => {
        setError(null);
        const newFiles: UploadedFile[] = [];

        Array.from(fileList).forEach((file) => {
            // Check size
            if (file.size > maxSize * 1024 * 1024) {
                setError(`Le fichier ${file.name} dépasse la taille maximale de ${maxSize}MB`);
                return;
            }

            const uploadedFile: UploadedFile = {
                id: Math.random().toString(36).substr(2, 9),
                name: file.name,
                size: file.size,
                type: file.type,
                status: 'uploading',
                progress: 0,
            };

            // Create preview for images
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    setFiles((prev) =>
                        prev.map((f) =>
                            f.id === uploadedFile.id
                                ? { ...f, preview: e.target?.result as string }
                                : f
                        )
                    );
                };
                reader.readAsDataURL(file);
            }

            newFiles.push(uploadedFile);

            // Simulate upload progress
            let progress = 0;
            const interval = setInterval(() => {
                progress += Math.random() * 30;
                if (progress >= 100) {
                    progress = 100;
                    clearInterval(interval);
                    setFiles((prev) =>
                        prev.map((f) =>
                            f.id === uploadedFile.id
                                ? { ...f, status: 'success', progress: 100 }
                                : f
                        )
                    );
                } else {
                    setFiles((prev) =>
                        prev.map((f) =>
                            f.id === uploadedFile.id ? { ...f, progress } : f
                        )
                    );
                }
            }, 200);
        });

        const updatedFiles = multiple ? [...files, ...newFiles] : newFiles;
        setFiles(updatedFiles);
        onFilesChange?.(updatedFiles);
    }, [files, maxSize, multiple, onFilesChange]);

    const handleDrop = useCallback(
        (e: React.DragEvent) => {
            e.preventDefault();
            setIsDragging(false);
            processFiles(e.dataTransfer.files);
        },
        [processFiles]
    );

    const handleDragOver = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    }, []);

    const handleDragLeave = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
    }, []);

    const handleFileInput = useCallback(
        (e: React.ChangeEvent<HTMLInputElement>) => {
            if (e.target.files) {
                processFiles(e.target.files);
            }
        },
        [processFiles]
    );

    const removeFile = useCallback(
        (id: string) => {
            const updatedFiles = files.filter((f) => f.id !== id);
            setFiles(updatedFiles);
            onFilesChange?.(updatedFiles);
        },
        [files, onFilesChange]
    );

    return (
        <div className="space-y-3">
            {/* Label */}
            <div>
                <label className="block text-sm font-medium text-slate-900">
                    {label}
                    {required && <span className="text-red-500 ml-1">*</span>}
                </label>
                {description && (
                    <p className="text-xs text-slate-500 mt-0.5">{description}</p>
                )}
            </div>

            {/* Drop Zone */}
            <div
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                className={`
          relative border-2 border-dashed rounded-xl p-6 text-center transition-all cursor-pointer
          ${isDragging
                        ? 'border-brand-500 bg-brand-50'
                        : 'border-slate-200 hover:border-slate-300 bg-slate-50/50'
                    }
        `}
            >
                <input
                    type="file"
                    accept={accept}
                    multiple={multiple}
                    onChange={handleFileInput}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                />

                <div className="space-y-2">
                    <div
                        className={`
              w-12 h-12 mx-auto rounded-xl flex items-center justify-center
              ${isDragging ? 'bg-brand-100' : 'bg-slate-100'}
            `}
                    >
                        <Upload
                            className={`w-6 h-6 ${isDragging ? 'text-brand-500' : 'text-slate-400'}`}
                        />
                    </div>
                    <div>
                        <p className="text-sm font-medium text-slate-700">
                            Glissez-déposez vos fichiers ici
                        </p>
                        <p className="text-xs text-slate-500 mt-1">
                            ou <span className="text-brand-600 font-medium">parcourir</span> •{' '}
                            {accept.replace(/\./g, '').toUpperCase()} • Max {maxSize}MB
                        </p>
                    </div>
                </div>
            </div>

            {/* Error */}
            {error && (
                <div className="flex items-center gap-2 text-red-600 text-sm">
                    <AlertCircle className="w-4 h-4" />
                    {error}
                </div>
            )}

            {/* File List */}
            <AnimatePresence>
                {files.length > 0 && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="space-y-2"
                    >
                        {files.map((file) => (
                            <motion.div
                                key={file.id}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: 20 }}
                                className="flex items-center gap-3 p-3 bg-white rounded-xl border border-slate-100"
                            >
                                {/* Preview/Icon */}
                                <div className="w-10 h-10 rounded-lg bg-slate-100 flex items-center justify-center overflow-hidden flex-shrink-0">
                                    {file.preview ? (
                                        <img
                                            src={file.preview}
                                            alt={file.name}
                                            className="w-full h-full object-cover"
                                        />
                                    ) : file.type === 'application/pdf' ? (
                                        <FileText className="w-5 h-5 text-red-500" />
                                    ) : (
                                        <ImageIcon className="w-5 h-5 text-blue-500" />
                                    )}
                                </div>

                                {/* File Info */}
                                <div className="flex-1 min-w-0">
                                    <p className="text-sm font-medium text-slate-900 truncate">
                                        {file.name}
                                    </p>
                                    <div className="flex items-center gap-2">
                                        <p className="text-xs text-slate-500">
                                            {formatFileSize(file.size)}
                                        </p>
                                        {file.status === 'uploading' && (
                                            <div className="flex-1 max-w-24 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                                                <div
                                                    className="h-full bg-brand-600 transition-all duration-300 rounded-full"
                                                    style={{ width: `${file.progress}%` }}
                                                />
                                            </div>
                                        )}
                                    </div>
                                </div>

                                {/* Status */}
                                {file.status === 'success' && (
                                    <div className="w-6 h-6 rounded-full bg-green-100 flex items-center justify-center">
                                        <Check className="w-4 h-4 text-green-600" />
                                    </div>
                                )}
                                {file.status === 'error' && (
                                    <div className="w-6 h-6 rounded-full bg-red-100 flex items-center justify-center">
                                        <AlertCircle className="w-4 h-4 text-red-600" />
                                    </div>
                                )}

                                {/* Remove */}
                                <button
                                    onClick={() => removeFile(file.id)}
                                    className="p-1 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition-colors"
                                >
                                    <X className="w-4 h-4" />
                                </button>
                            </motion.div>
                        ))}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
