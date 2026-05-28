'use client';

import { useState, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, Camera, Smartphone, X, Check, Loader2, QrCode } from 'lucide-react';

// =============================================================================
// SMART PHOTO UPLOADER - Multi-mode Photo Capture
// Supports: File Upload, Webcam, Mobile QR
// =============================================================================

type UploadMode = 'upload' | 'webcam' | 'mobile';

interface SmartPhotoUploaderProps {
    onPhotosCaptured: () => void;
    userId?: string;
    maxPhotos?: number;
}

export function SmartPhotoUploader({
    onPhotosCaptured,
    userId,
    maxPhotos = 3
}: SmartPhotoUploaderProps) {
    const [mode, setMode] = useState<UploadMode | null>(null);
    const [photos, setPhotos] = useState<string[]>([]);
    const [isCapturing, setIsCapturing] = useState(false);
    const [webcamStream, setWebcamStream] = useState<MediaStream | null>(null);

    const videoRef = useRef<HTMLVideoElement>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    // Start webcam
    const startWebcam = useCallback(async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'user', width: 640, height: 480 }
            });
            setWebcamStream(stream);
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
            }
        } catch (error) {
            console.error('Webcam error:', error);
            alert('Impossible d\'accéder à la caméra. Vérifiez vos permissions.');
            setMode(null);
        }
    }, []);

    // Stop webcam
    const stopWebcam = useCallback(() => {
        if (webcamStream) {
            webcamStream.getTracks().forEach(track => track.stop());
            setWebcamStream(null);
        }
    }, [webcamStream]);

    // Handle mode selection
    const handleModeSelect = async (selectedMode: UploadMode) => {
        setMode(selectedMode);
        if (selectedMode === 'webcam') {
            await startWebcam();
        }
    };

    // Capture from webcam
    const captureFromWebcam = useCallback(() => {
        if (!videoRef.current) return;

        setIsCapturing(true);
        const canvas = document.createElement('canvas');
        canvas.width = videoRef.current.videoWidth;
        canvas.height = videoRef.current.videoHeight;
        const ctx = canvas.getContext('2d');
        if (ctx) {
            ctx.drawImage(videoRef.current, 0, 0);
            const dataUrl = canvas.toDataURL('image/jpeg', 0.8);
            setPhotos(prev => {
                const newPhotos = [...prev, dataUrl].slice(0, maxPhotos);
                if (newPhotos.length > 0) {
                    onPhotosCaptured();
                }
                return newPhotos;
            });
        }
        setIsCapturing(false);
    }, [maxPhotos, onPhotosCaptured]);

    // Handle file upload
    const handleFileUpload = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;
        if (!files) return;

        Array.from(files).slice(0, maxPhotos - photos.length).forEach(file => {
            const reader = new FileReader();
            reader.onload = (event) => {
                const dataUrl = event.target?.result as string;
                setPhotos(prev => {
                    const newPhotos = [...prev, dataUrl].slice(0, maxPhotos);
                    if (newPhotos.length > 0) {
                        onPhotosCaptured();
                    }
                    return newPhotos;
                });
            };
            reader.readAsDataURL(file);
        });

        // Reset input
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    }, [maxPhotos, photos.length, onPhotosCaptured]);

    // Remove photo
    const removePhoto = useCallback((index: number) => {
        setPhotos(prev => prev.filter((_, i) => i !== index));
    }, []);

    // Close mode
    const closeMode = useCallback(() => {
        stopWebcam();
        setMode(null);
    }, [stopWebcam]);

    return (
        <div className="space-y-4">
            {/* Mode selector (when no mode selected) */}
            {!mode && (
                <div className="grid grid-cols-3 gap-3">
                    <button
                        onClick={() => handleModeSelect('upload')}
                        className="oracle-btn-secondary flex flex-col items-center gap-2 py-4"
                    >
                        <Upload className="w-5 h-5" />
                        <span className="text-xs">Fichier</span>
                    </button>
                    <button
                        onClick={() => handleModeSelect('webcam')}
                        className="oracle-btn-secondary flex flex-col items-center gap-2 py-4"
                    >
                        <Camera className="w-5 h-5" />
                        <span className="text-xs">Webcam</span>
                    </button>
                    <button
                        onClick={() => handleModeSelect('mobile')}
                        className="oracle-btn-secondary flex flex-col items-center gap-2 py-4"
                    >
                        <Smartphone className="w-5 h-5" />
                        <span className="text-xs">Mobile</span>
                    </button>
                </div>
            )}

            {/* Active mode content */}
            <AnimatePresence mode="wait">
                {mode === 'upload' && (
                    <motion.div
                        key="upload"
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="space-y-4"
                    >
                        <div className="relative">
                            <input
                                ref={fileInputRef}
                                type="file"
                                accept="image/*"
                                multiple
                                onChange={handleFileUpload}
                                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                                aria-label="Sélectionner des photos"
                                title="Sélectionner des photos à téléverser"
                            />
                            <div className="border-2 border-dashed border-white/20 rounded-xl p-8 text-center hover:border-amber-400/50 transition-colors">
                                <Upload className="w-8 h-8 mx-auto mb-3 text-white/40" />
                                <p className="text-white/60 text-sm">
                                    Glissez vos photos ici ou cliquez pour sélectionner
                                </p>
                                <p className="text-white/30 text-xs mt-1">
                                    Maximum {maxPhotos} photos
                                </p>
                            </div>
                        </div>
                        <button
                            onClick={closeMode}
                            className="text-white/50 text-sm hover:text-white/80"
                        >
                            ← Changer de méthode
                        </button>
                    </motion.div>
                )}

                {mode === 'webcam' && (
                    <motion.div
                        key="webcam"
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="space-y-4"
                    >
                        <div className="relative rounded-xl overflow-hidden bg-black aspect-video">
                            <video
                                ref={videoRef}
                                autoPlay
                                playsInline
                                muted
                                className="w-full h-full object-cover"
                            />
                            {/* Capture button overlay */}
                            <div className="absolute bottom-4 left-1/2 -translate-x-1/2">
                                <button
                                    onClick={captureFromWebcam}
                                    disabled={isCapturing || photos.length >= maxPhotos}
                                    className="w-14 h-14 rounded-full bg-white/20 backdrop-blur-sm border-4 border-white flex items-center justify-center hover:bg-white/30 transition-colors disabled:opacity-50"
                                >
                                    {isCapturing ? (
                                        <Loader2 className="w-6 h-6 text-white animate-spin" />
                                    ) : (
                                        <div className="w-10 h-10 rounded-full bg-white" />
                                    )}
                                </button>
                            </div>
                        </div>
                        <button
                            onClick={closeMode}
                            className="text-white/50 text-sm hover:text-white/80"
                        >
                            ← Changer de méthode
                        </button>
                    </motion.div>
                )}

                {mode === 'mobile' && (
                    <motion.div
                        key="mobile"
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="space-y-4"
                    >
                        <div className="bg-white/5 rounded-xl p-6 text-center">
                            <div className="w-32 h-32 mx-auto mb-4 bg-white rounded-lg flex items-center justify-center">
                                <QrCode className="w-24 h-24 text-slate-800" />
                            </div>
                            <p className="text-white/60 text-sm mb-2">
                                Scannez ce QR code avec votre téléphone
                            </p>
                            <p className="text-white/40 text-xs">
                                Fonctionnalité en développement
                            </p>
                        </div>
                        <button
                            onClick={closeMode}
                            className="text-white/50 text-sm hover:text-white/80"
                        >
                            ← Changer de méthode
                        </button>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Photo previews */}
            {photos.length > 0 && (
                <div className="mt-4">
                    <p className="text-white/50 text-xs mb-2">
                        {photos.length} / {maxPhotos} photos capturées
                    </p>
                    <div className="flex gap-2 flex-wrap">
                        {photos.map((photo, index) => (
                            <div key={index} className="relative group">
                                <img
                                    src={photo}
                                    alt={`Photo ${index + 1}`}
                                    className="w-16 h-16 object-cover rounded-lg border border-white/10"
                                />
                                <button
                                    onClick={() => removePhoto(index)}
                                    className="absolute -top-2 -right-2 w-5 h-5 bg-red-500 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                                    aria-label={`Supprimer photo ${index + 1}`}
                                    title="Supprimer cette photo"
                                >
                                    <X className="w-3 h-3 text-white" />
                                </button>
                                <div className="absolute bottom-1 right-1 w-4 h-4 bg-green-500 rounded-full flex items-center justify-center">
                                    <Check className="w-2.5 h-2.5 text-white" />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
