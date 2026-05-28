'use client';

import { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, X, Check, Sparkles } from 'lucide-react';
import {
    getJobTagsByBrand,
    getFeaturedTags,
    searchTags,
    getTagsGroupedByCategory,
    CATEGORY_LABELS,
    type JobTag,
    type JobCategory
} from '@/lib/constants/jobTags';
import { currentBrand } from '@/lib/brand';

// =============================================================================
// JOB TAG PICKER - Express Onboarding Component
// Tag cloud with search for ultra-fast profession identification
// =============================================================================

interface JobTagPickerProps {
    /** Selected tag IDs */
    value: string[];
    /** Callback when selection changes */
    onChange: (selectedIds: string[]) => void;
    /** Allow multiple selections (default: false for single job) */
    multiple?: boolean;
    /** Maximum selections allowed */
    maxSelections?: number;
    /** Show search bar */
    showSearch?: boolean;
    /** Show category headers */
    showCategories?: boolean;
    /** Placeholder for search */
    searchPlaceholder?: string;
}

export function JobTagPicker({
    value = [],
    onChange,
    multiple = false,
    maxSelections = 3,
    showSearch = true,
    showCategories = true,
    searchPlaceholder = 'Rechercher votre métier...',
}: JobTagPickerProps) {
    const [searchQuery, setSearchQuery] = useState('');

    // Get tags based on brand
    const allTags = useMemo(() => getJobTagsByBrand(currentBrand.mode), []);
    const featuredTags = useMemo(() => getFeaturedTags(currentBrand.mode), []);

    // Filter tags based on search
    const filteredTags = useMemo(() => {
        if (!searchQuery.trim()) return allTags;
        return searchTags(searchQuery, currentBrand.mode);
    }, [searchQuery, allTags]);

    // Group by category when not searching
    const groupedTags = useMemo(() => {
        if (searchQuery.trim() || !showCategories) return null;
        return getTagsGroupedByCategory(currentBrand.mode);
    }, [searchQuery, showCategories]);

    // Handle tag selection
    const handleTagClick = (tagId: string) => {
        if (multiple) {
            if (value.includes(tagId)) {
                onChange(value.filter(id => id !== tagId));
            } else if (value.length < maxSelections) {
                onChange([...value, tagId]);
            }
        } else {
            onChange(value.includes(tagId) ? [] : [tagId]);
        }
    };

    // Check if tag is selected
    const isSelected = (tagId: string) => value.includes(tagId);

    // Clear search
    const clearSearch = () => setSearchQuery('');

    return (
        <div className="space-y-4">
            {/* Search Bar */}
            {showSearch && (
                <div className="relative">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder={searchPlaceholder}
                        className="w-full pl-12 pr-10 py-3 rounded-theme-lg border border-slate-200 bg-white text-slate-900 placeholder:text-slate-400 focus:ring-2 focus:ring-primary-200 focus:border-primary-400 transition-all outline-none"
                    />
                    {searchQuery && (
                        <button
                            onClick={clearSearch}
                            className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                        >
                            <X className="w-5 h-5" />
                        </button>
                    )}
                </div>
            )}

            {/* Selection Counter */}
            {multiple && (
                <div className="flex items-center gap-2 text-sm text-slate-500">
                    <span>{value.length}/{maxSelections} sélectionnés</span>
                    {value.length > 0 && (
                        <button
                            onClick={() => onChange([])}
                            className="text-primary-600 hover:underline"
                        >
                            Tout effacer
                        </button>
                    )}
                </div>
            )}

            {/* Featured Tags (when not searching) */}
            {!searchQuery && featuredTags.length > 0 && (
                <div className="space-y-2">
                    <div className="flex items-center gap-2 text-xs font-medium text-slate-500">
                        <Sparkles className="w-3.5 h-3.5" />
                        <span>Métiers populaires</span>
                    </div>
                    <div className="flex flex-wrap gap-2">
                        {featuredTags.map(tag => (
                            <TagChip
                                key={tag.id}
                                tag={tag}
                                isSelected={isSelected(tag.id)}
                                onClick={() => handleTagClick(tag.id)}
                                featured
                            />
                        ))}
                    </div>
                </div>
            )}

            {/* Tags Display */}
            <div className="space-y-4">
                {/* Grouped by category */}
                {groupedTags && !searchQuery ? (
                    Object.entries(groupedTags).map(([category, tags]) => (
                        <div key={category} className="space-y-2">
                            <h4 className="text-sm font-semibold text-slate-700">
                                {CATEGORY_LABELS[category as JobCategory] || category}
                            </h4>
                            <div className="flex flex-wrap gap-2">
                                <AnimatePresence>
                                    {tags.map(tag => (
                                        <TagChip
                                            key={tag.id}
                                            tag={tag}
                                            isSelected={isSelected(tag.id)}
                                            onClick={() => handleTagClick(tag.id)}
                                        />
                                    ))}
                                </AnimatePresence>
                            </div>
                        </div>
                    ))
                ) : (
                    /* Flat list (search results or no categories) */
                    <div className="flex flex-wrap gap-2">
                        <AnimatePresence>
                            {filteredTags.length > 0 ? (
                                filteredTags.map(tag => (
                                    <TagChip
                                        key={tag.id}
                                        tag={tag}
                                        isSelected={isSelected(tag.id)}
                                        onClick={() => handleTagClick(tag.id)}
                                    />
                                ))
                            ) : (
                                <motion.p
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    className="text-sm text-slate-500 py-4"
                                >
                                    Aucun métier trouvé pour "{searchQuery}"
                                </motion.p>
                            )}
                        </AnimatePresence>
                    </div>
                )}
            </div>
        </div>
    );
}

// =============================================================================
// TAG CHIP COMPONENT
// =============================================================================

interface TagChipProps {
    tag: JobTag;
    isSelected: boolean;
    onClick: () => void;
    featured?: boolean;
}

function TagChip({ tag, isSelected, onClick, featured }: TagChipProps) {
    return (
        <motion.button
            type="button"
            layout
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            whileTap={{ scale: 0.95 }}
            onClick={onClick}
            className={`
        inline-flex items-center gap-2 px-3 py-2 rounded-theme-md text-sm font-medium
        transition-all duration-200 cursor-pointer
        ${isSelected
                    ? 'bg-primary-600 text-white shadow-md ring-2 ring-primary-300'
                    : featured
                        ? 'bg-primary-50 text-primary-700 hover:bg-primary-100 border border-primary-200'
                        : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }
      `}
        >
            <span className="text-base">{tag.emoji}</span>
            <span>{tag.shortLabel}</span>
            {isSelected && (
                <Check className="w-4 h-4 ml-1" />
            )}
        </motion.button>
    );
}

// =============================================================================
// COMPACT TAG DISPLAY (for showing selected tags)
// =============================================================================

interface SelectedTagsDisplayProps {
    selectedIds: string[];
    onRemove?: (id: string) => void;
}

export function SelectedTagsDisplay({ selectedIds, onRemove }: SelectedTagsDisplayProps) {
    const allTags = getJobTagsByBrand(currentBrand.mode);
    const selectedTags = selectedIds
        .map(id => allTags.find(t => t.id === id))
        .filter((t): t is JobTag => t !== undefined);

    if (selectedTags.length === 0) return null;

    return (
        <div className="flex flex-wrap gap-2">
            {selectedTags.map(tag => (
                <span
                    key={tag.id}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-primary-100 text-primary-700 text-sm font-medium"
                >
                    <span>{tag.emoji}</span>
                    <span>{tag.shortLabel}</span>
                    {onRemove && (
                        <button
                            onClick={() => onRemove(tag.id)}
                            className="ml-1 hover:text-primary-900"
                        >
                            <X className="w-3.5 h-3.5" />
                        </button>
                    )}
                </span>
            ))}
        </div>
    );
}
