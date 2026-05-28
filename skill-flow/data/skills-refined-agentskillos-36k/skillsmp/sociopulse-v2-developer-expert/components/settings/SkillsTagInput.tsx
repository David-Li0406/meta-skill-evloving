'use client';

import { useState, useCallback, KeyboardEvent } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Plus } from 'lucide-react';

// ===========================================
// TYPES
// ===========================================

export interface SkillsTagInputProps {
    value: string[];
    onChange: (tags: string[]) => void;
    placeholder?: string;
    maxTags?: number;
    disabled?: boolean;
}

// ===========================================
// COMPONENT
// ===========================================

export function SkillsTagInput({
    value,
    onChange,
    placeholder = 'Ajouter une compétence...',
    maxTags = 10,
    disabled = false,
}: SkillsTagInputProps) {
    const [inputValue, setInputValue] = useState('');

    const addTag = useCallback((tag: string) => {
        const trimmed = tag.trim();
        if (!trimmed) return;
        if (value.includes(trimmed)) return;
        if (value.length >= maxTags) return;

        onChange([...value, trimmed]);
        setInputValue('');
    }, [value, onChange, maxTags]);

    const removeTag = useCallback((tagToRemove: string) => {
        onChange(value.filter(tag => tag !== tagToRemove));
    }, [value, onChange]);

    const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            addTag(inputValue);
        }
        if (e.key === 'Backspace' && !inputValue && value.length > 0) {
            removeTag(value[value.length - 1]);
        }
    };

    return (
        <div className="space-y-3">
            {/* Input Field */}
            <div className="relative">
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder={value.length >= maxTags ? `Maximum ${maxTags} compétences` : placeholder}
                    disabled={disabled || value.length >= maxTags}
                    className="input-premium pr-12"
                />
                <button
                    type="button"
                    onClick={() => addTag(inputValue)}
                    disabled={disabled || !inputValue.trim() || value.length >= maxTags}
                    className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-lg bg-brand-600 text-white hover:bg-brand-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    aria-label="Ajouter"
                >
                    <Plus className="w-4 h-4" />
                </button>
            </div>

            {/* Tags */}
            <div className="flex flex-wrap gap-2 min-h-[40px]">
                <AnimatePresence mode="popLayout">
                    {value.map((tag) => (
                        <motion.span
                            key={tag}
                            initial={{ scale: 0, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0, opacity: 0 }}
                            layout
                            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-brand-100 text-brand-700 text-sm font-medium"
                        >
                            {tag}
                            {!disabled && (
                                <button
                                    type="button"
                                    onClick={() => removeTag(tag)}
                                    className="p-0.5 rounded-full hover:bg-brand-200 transition-colors"
                                    aria-label={`Supprimer ${tag}`}
                                >
                                    <X className="w-3.5 h-3.5" />
                                </button>
                            )}
                        </motion.span>
                    ))}
                </AnimatePresence>

                {value.length === 0 && (
                    <span className="text-sm text-slate-400 italic py-1.5">
                        Aucune compétence ajoutée
                    </span>
                )}
            </div>

            {/* Counter */}
            <div className="text-right">
                <span className={`text-xs ${value.length >= maxTags ? 'text-red-500' : 'text-slate-400'}`}>
                    {value.length} / {maxTags} compétences
                </span>
            </div>
        </div>
    );
}
