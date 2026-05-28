'use client';

import { useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { Search } from 'lucide-react';

export type TagCategory = 'JOB' | 'STRUCTURE' | 'SKILL';

export interface GrowthTag {
    id: string;
    name: string;
    category: TagCategory;
}

export interface TagSelectorProps {
    tags: GrowthTag[];
    selectedIds: string[];
    onChange: (nextIds: string[]) => void;
    maxSelected?: number;
}

const CATEGORY_LABELS: Record<TagCategory, string> = {
    JOB: 'Métiers',
    STRUCTURE: 'Structures',
    SKILL: 'Compétences',
};

const normalize = (value: string) => value.trim().toLowerCase();

export function TagSelector({ tags, selectedIds, onChange, maxSelected = 10 }: TagSelectorProps) {
    const [activeCategory, setActiveCategory] = useState<TagCategory>('JOB');
    const [search, setSearch] = useState('');

    const selectedSet = useMemo(() => new Set(selectedIds), [selectedIds]);
    const normalizedSearch = normalize(search);

    const filtered = useMemo(() => {
        const byCategory = tags.filter((tag) => tag.category === activeCategory);
        if (!normalizedSearch) return byCategory;
        return byCategory.filter((tag) => normalize(tag.name).includes(normalizedSearch));
    }, [activeCategory, normalizedSearch, tags]);

    const toggle = (id: string) => {
        if (selectedSet.has(id)) {
            onChange(selectedIds.filter((x) => x !== id));
            return;
        }

        if (selectedIds.length >= maxSelected) return;
        onChange([...selectedIds, id]);
    };

    return (
        <div className="space-y-4">
            <div className="flex items-center justify-between gap-4">
                <div className="flex items-center gap-2 rounded-2xl bg-white border border-slate-200 p-1">
                    {(Object.keys(CATEGORY_LABELS) as TagCategory[]).map((cat) => {
                        const isActive = cat === activeCategory;
                        return (
                            <button
                                key={cat}
                                type="button"
                                onClick={() => setActiveCategory(cat)}
                                className={`px-3 py-2 rounded-xl text-sm font-semibold transition-colors ${
                                    isActive ? 'bg-slate-900 text-white' : 'text-slate-600 hover:bg-slate-50'
                                }`}
                            >
                                {CATEGORY_LABELS[cat]}
                            </button>
                        );
                    })}
                </div>

                <div className="text-sm text-slate-600">
                    <span className="font-semibold text-slate-900">{selectedIds.length}</span>/{maxSelected} sélectionnés
                </div>
            </div>

            <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-400" />
                <input
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="input-premium !pl-10"
                    placeholder={`Rechercher dans ${CATEGORY_LABELS[activeCategory].toLowerCase()}…`}
                />
            </div>

            <div className="flex flex-wrap gap-2">
                {filtered.map((tag) => {
                    const isSelected = selectedSet.has(tag.id);
                    return (
                        <motion.button
                            key={tag.id}
                            type="button"
                            onClick={() => toggle(tag.id)}
                            whileTap={{ scale: 0.97 }}
                            className={`px-4 py-2 rounded-full border text-sm font-semibold transition-colors ${
                                isSelected
                                    ? 'bg-brand-600 border-brand-600 text-white'
                                    : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50'
                            }`}
                        >
                            {tag.name}
                        </motion.button>
                    );
                })}
                {filtered.length === 0 ? (
                    <p className="text-sm text-slate-500 py-4">Aucun tag trouvé.</p>
                ) : null}
            </div>
        </div>
    );
}

