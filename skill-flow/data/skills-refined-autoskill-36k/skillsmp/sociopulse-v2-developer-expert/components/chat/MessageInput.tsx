'use client';

import { useState, useRef, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Send, Paperclip, Loader2 } from 'lucide-react';

// ===========================================
// TYPES
// ===========================================

export interface MessageInputProps {
    onSend: (content: string) => void;
    onAttachment?: () => void;
    disabled?: boolean;
    placeholder?: string;
}

// ===========================================
// COMPONENT
// ===========================================

export function MessageInput({
    onSend,
    onAttachment,
    disabled = false,
    placeholder = 'Écrivez votre message...',
}: MessageInputProps) {
    const [value, setValue] = useState('');
    const [isSending, setIsSending] = useState(false);
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    // Auto-expand textarea
    const adjustHeight = useCallback(() => {
        const textarea = textareaRef.current;
        if (!textarea) return;

        textarea.style.height = 'auto';
        const newHeight = Math.min(textarea.scrollHeight, 150);
        textarea.style.height = `${newHeight}px`;
    }, []);

    useEffect(() => {
        adjustHeight();
    }, [value, adjustHeight]);

    const handleSend = async () => {
        if (!value.trim() || disabled || isSending) return;

        setIsSending(true);
        try {
            await onSend(value.trim());
            setValue('');
        } finally {
            setIsSending(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const canSend = value.trim().length > 0 && !disabled && !isSending;

    return (
        <div className="flex-shrink-0 border-t border-slate-100 bg-white p-3 sm:p-4">
            <div className="flex items-end gap-2 sm:gap-3">
                {/* Attachment Button */}
                <motion.button
                    type="button"
                    onClick={onAttachment}
                    disabled={disabled}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="flex-shrink-0 p-2.5 rounded-xl text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors disabled:opacity-50"
                    aria-label="Joindre un fichier"
                >
                    <Paperclip className="w-5 h-5" />
                </motion.button>

                {/* Input */}
                <div className="flex-1 relative">
                    <textarea
                        ref={textareaRef}
                        value={value}
                        onChange={(e) => setValue(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder={placeholder}
                        disabled={disabled}
                        rows={1}
                        className="input-premium resize-none min-h-[44px] max-h-[150px] py-3 pr-4"
                        style={{ lineHeight: '1.4' }}
                    />
                </div>

                {/* Send Button */}
                <motion.button
                    type="button"
                    onClick={handleSend}
                    disabled={!canSend}
                    whileHover={{ scale: canSend ? 1.05 : 1 }}
                    whileTap={{ scale: canSend ? 0.95 : 1 }}
                    className={`
                        flex-shrink-0 w-11 h-11 rounded-full flex items-center justify-center
                        transition-colors
                        ${canSend
                            ? 'bg-brand-600 text-white shadow-lg shadow-brand-600/30 hover:bg-brand-700'
                            : 'bg-slate-100 text-slate-400 cursor-not-allowed'
                        }
                    `}
                    aria-label="Envoyer"
                >
                    {isSending ? (
                        <Loader2 className="w-5 h-5 animate-spin" />
                    ) : (
                        <Send className="w-5 h-5" />
                    )}
                </motion.button>
            </div>

            {/* Helper Text */}
            <p className="text-xs text-slate-400 mt-2 text-center hidden sm:block">
                Appuyez sur Entrée pour envoyer, Maj+Entrée pour une nouvelle ligne
            </p>
        </div>
    );
}
