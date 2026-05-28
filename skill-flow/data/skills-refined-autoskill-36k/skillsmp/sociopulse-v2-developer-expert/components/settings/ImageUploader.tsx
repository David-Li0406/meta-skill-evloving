'use client';

import { useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Camera, X, Upload, Loader2 } from 'lucide-react';

// ===========================================
// TYPES
// ===========================================

export interface ImageUploaderProps {
    currentImageUrl?: string | null;
    initials?: string;
    onImageChange: (file: File | null) => void;
    size?: 'sm' | 'md' | 'lg';
    shape?: 'circle' | 'square';
    disabled?: boolean;
}

// ===========================================
// COMPONENT
// ===========================================

export function ImageUploader({
    currentImageUrl,
    initials = '?',
    onImageChange,
    size = 'lg',
    shape = 'circle',
    disabled = false,
}: ImageUploaderProps) {
    const inputRef = useRef<HTMLInputElement>(null);
    const [previewUrl, setPreviewUrl] = useState<string | null>(null);
    const [isHovered, setIsHovered] = useState(false);
    const [isUploading, setIsUploading] = useState(false);

    const sizeClasses = {
        sm: 'w-16 h-16',
        md: 'w-24 h-24',
        lg: 'w-32 h-32',
    };

    const shapeClasses = {
        circle: 'rounded-full',
        square: 'rounded-2xl',
    };

    const displayUrl = previewUrl || currentImageUrl;

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        // Validate file type
        if (!file.type.startsWith('image/')) {
            alert('Veuillez sélectionner une image');
            return;
        }

        // Validate file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
            alert('L\'image ne doit pas dépasser 5MB');
            return;
        }

        // Create preview
        const reader = new FileReader();
        reader.onloadend = () => {
            setPreviewUrl(reader.result as string);
        };
        reader.readAsDataURL(file);

        // Notify parent
        onImageChange(file);
    };

    const handleRemove = () => {
        setPreviewUrl(null);
        onImageChange(null);
        if (inputRef.current) {
            inputRef.current.value = '';
        }
    };

    const handleClick = () => {
        if (!disabled) {
            inputRef.current?.click();
        }
    };

    return (
        <div className="relative inline-block">
            {/* Hidden File Input */}
            <input
                ref={inputRef}
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                className="hidden"
                disabled={disabled}
            />

            {/* Image Container */}
            <motion.button
                type="button"
                onClick={handleClick}
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
                disabled={disabled}
                className={`
                    relative ${sizeClasses[size]} ${shapeClasses[shape]}
                    bg-gradient-to-br from-brand-100 to-indigo-100
                    flex items-center justify-center
                    overflow-hidden border-4 border-white shadow-lg
                    transition-all cursor-pointer
                    ${disabled ? 'opacity-60 cursor-not-allowed' : 'hover:shadow-xl'}
                `}
                whileHover={{ scale: disabled ? 1 : 1.02 }}
                whileTap={{ scale: disabled ? 1 : 0.98 }}
            >
                {/* Current/Preview Image */}
                {displayUrl ? (
                    <img
                        src={displayUrl}
                        alt="Avatar"
                        className="w-full h-full object-cover"
                    />
                ) : (
                    <span className="text-2xl font-bold text-brand-600">
                        {initials.slice(0, 2).toUpperCase()}
                    </span>
                )}

                {/* Hover Overlay */}
                <AnimatePresence>
                    {(isHovered || isUploading) && !disabled && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className={`
                                absolute inset-0 bg-black/50 backdrop-blur-sm
                                flex flex-col items-center justify-center gap-1
                                ${shapeClasses[shape]}
                            `}
                        >
                            {isUploading ? (
                                <Loader2 className="w-6 h-6 text-white animate-spin" />
                            ) : (
                                <>
                                    <Camera className="w-6 h-6 text-white" />
                                    <span className="text-xs text-white font-medium">
                                        Modifier
                                    </span>
                                </>
                            )}
                        </motion.div>
                    )}
                </AnimatePresence>
            </motion.button>

            {/* Remove Button */}
            {displayUrl && !disabled && (
                <motion.button
                    type="button"
                    onClick={(e) => {
                        e.stopPropagation();
                        handleRemove();
                    }}
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    exit={{ scale: 0 }}
                    className={`
                        absolute -top-1 -right-1 w-7 h-7
                        bg-red-500 text-white rounded-full
                        flex items-center justify-center
                        shadow-lg hover:bg-red-600 transition-colors
                    `}
                    aria-label="Supprimer l'image"
                >
                    <X className="w-4 h-4" />
                </motion.button>
            )}

            {/* Upload Hint */}
            <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 whitespace-nowrap">
                <span className="text-xs text-slate-400 flex items-center gap-1">
                    <Upload className="w-3 h-3" />
                    JPG, PNG • Max 5MB
                </span>
            </div>
        </div>
    );
}
