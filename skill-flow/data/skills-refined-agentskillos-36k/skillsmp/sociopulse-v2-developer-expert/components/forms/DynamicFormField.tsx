'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import * as LucideIcons from 'lucide-react';
import type { FieldDefinition, FormSection } from '@/lib/formConfig';

// =============================================================================
// DYNAMIC FORM FIELD - Config-Driven Form Renderer
// Renders form fields dynamically based on FieldDefinition
// =============================================================================

interface DynamicFieldProps {
    field: FieldDefinition;
    value: any;
    onChange: (name: string, value: any) => void;
    error?: string;
    formData?: Record<string, any>;
}

/**
 * Renders a single form field based on its FieldDefinition
 */
export function DynamicField({ field, value, onChange, error, formData = {} }: DynamicFieldProps) {
    // Check conditional visibility
    if (field.showIf) {
        const conditionValue = formData[field.showIf.field];
        if (conditionValue !== field.showIf.value) {
            return null;
        }
    }

    // Get icon component if specified
    const IconComponent = field.icon
        ? (LucideIcons as any)[field.icon]
        : null;

    const baseInputClass = `
    w-full px-4 py-3 rounded-theme-lg border border-slate-200 
    bg-white text-slate-900 placeholder:text-slate-400 
    focus:ring-2 focus:ring-primary-200 focus:border-primary-400 
    transition-all duration-200 outline-none
    ${error ? 'border-red-400 focus:ring-red-200' : ''}
  `;

    const labelClass = "block text-sm font-medium text-slate-700 mb-1.5";

    return (
        <div className="space-y-1">
            {/* Label */}
            <label htmlFor={field.name} className={labelClass}>
                <span className="flex items-center gap-2">
                    {IconComponent && <IconComponent className="w-4 h-4 text-slate-400" />}
                    {field.label}
                    {field.required && <span className="text-red-500">*</span>}
                </span>
            </label>

            {/* Field based on type */}
            {field.type === 'text' && (
                <input
                    id={field.name}
                    type="text"
                    value={value || ''}
                    onChange={(e) => onChange(field.name, e.target.value)}
                    placeholder={field.placeholder}
                    pattern={field.pattern}
                    minLength={field.min}
                    maxLength={field.max}
                    className={baseInputClass}
                    required={field.required}
                />
            )}

            {field.type === 'email' && (
                <input
                    id={field.name}
                    type="email"
                    value={value || ''}
                    onChange={(e) => onChange(field.name, e.target.value)}
                    placeholder={field.placeholder}
                    className={baseInputClass}
                    required={field.required}
                />
            )}

            {field.type === 'tel' && (
                <input
                    id={field.name}
                    type="tel"
                    value={value || ''}
                    onChange={(e) => onChange(field.name, e.target.value)}
                    placeholder={field.placeholder}
                    className={baseInputClass}
                    required={field.required}
                />
            )}

            {field.type === 'number' && (
                <input
                    id={field.name}
                    type="number"
                    value={value || ''}
                    onChange={(e) => onChange(field.name, parseFloat(e.target.value) || '')}
                    placeholder={field.placeholder}
                    min={field.min}
                    max={field.max}
                    className={baseInputClass}
                    required={field.required}
                />
            )}

            {field.type === 'date' && (
                <input
                    id={field.name}
                    type="date"
                    value={value || ''}
                    onChange={(e) => onChange(field.name, e.target.value)}
                    className={baseInputClass}
                    required={field.required}
                />
            )}

            {field.type === 'textarea' && (
                <textarea
                    id={field.name}
                    value={value || ''}
                    onChange={(e) => onChange(field.name, e.target.value)}
                    placeholder={field.placeholder}
                    rows={4}
                    className={`${baseInputClass} resize-none`}
                    required={field.required}
                />
            )}

            {field.type === 'select' && (
                <select
                    id={field.name}
                    value={value || ''}
                    onChange={(e) => onChange(field.name, e.target.value)}
                    className={baseInputClass}
                    required={field.required}
                >
                    <option value="">Sélectionnez...</option>
                    {field.options?.map(opt => (
                        <option key={opt.value} value={opt.value}>{opt.label}</option>
                    ))}
                </select>
            )}

            {field.type === 'multiselect' && (
                <MultiSelectField
                    field={field}
                    value={value || []}
                    onChange={onChange}
                />
            )}

            {field.type === 'boolean' && (
                <BooleanField
                    field={field}
                    value={value ?? field.defaultValue ?? false}
                    onChange={onChange}
                />
            )}

            {/* Help text */}
            {field.helpText && !error && (
                <p className="text-xs text-slate-500 mt-1">{field.helpText}</p>
            )}

            {/* Error message */}
            {error && (
                <p className="text-xs text-red-500 mt-1">{error}</p>
            )}
        </div>
    );
}

/**
 * Multi-select field with chips
 */
function MultiSelectField({
    field,
    value,
    onChange
}: {
    field: FieldDefinition;
    value: string[];
    onChange: (name: string, value: string[]) => void;
}) {
    const toggleOption = (optValue: string) => {
        const newValue = value.includes(optValue)
            ? value.filter(v => v !== optValue)
            : [...value, optValue];
        onChange(field.name, newValue);
    };

    return (
        <div className="flex flex-wrap gap-2">
            {field.options?.map(opt => {
                const isSelected = value.includes(opt.value);
                return (
                    <motion.button
                        key={opt.value}
                        type="button"
                        whileTap={{ scale: 0.95 }}
                        onClick={() => toggleOption(opt.value)}
                        className={`
              px-3 py-1.5 rounded-theme-md text-sm font-medium
              transition-all duration-200
              ${isSelected
                                ? 'bg-primary-600 text-white shadow-sm'
                                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                            }
            `}
                    >
                        {opt.label}
                    </motion.button>
                );
            })}
        </div>
    );
}

/**
 * Boolean toggle field
 */
function BooleanField({
    field,
    value,
    onChange,
}: {
    field: FieldDefinition;
    value: boolean;
    onChange: (name: string, value: boolean) => void;
}) {
    return (
        <label className="flex items-center gap-3 cursor-pointer">
            <button
                type="button"
                role="switch"
                aria-checked={value}
                onClick={() => onChange(field.name, !value)}
                className={`
          relative w-12 h-6 rounded-full transition-colors duration-200
          ${value ? 'bg-primary-600' : 'bg-slate-200'}
        `}
            >
                <motion.span
                    className="absolute top-1 left-1 w-4 h-4 bg-white rounded-full shadow"
                    animate={{ x: value ? 24 : 0 }}
                    transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                />
            </button>
            <span className="text-sm text-slate-700">
                {value ? 'Oui' : 'Non'}
            </span>
        </label>
    );
}

// =============================================================================
// FORM SECTION RENDERER
// =============================================================================

interface FormSectionRendererProps {
    section: FormSection;
    formData: Record<string, any>;
    onChange: (name: string, value: any) => void;
    errors?: Record<string, string>;
}

export function FormSectionRenderer({
    section,
    formData,
    onChange,
    errors = {}
}: FormSectionRendererProps) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
        >
            {/* Section Header */}
            <div>
                <h3 className="text-lg font-semibold text-slate-900">{section.title}</h3>
                {section.description && (
                    <p className="text-sm text-slate-500 mt-1">{section.description}</p>
                )}
            </div>

            {/* Fields Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {section.fields.map(field => (
                    <div
                        key={field.name}
                        className={field.type === 'textarea' ? 'md:col-span-2' : ''}
                    >
                        <DynamicField
                            field={field}
                            value={formData[field.name]}
                            onChange={onChange}
                            error={errors[field.name]}
                            formData={formData}
                        />
                    </div>
                ))}
            </div>
        </motion.div>
    );
}

// =============================================================================
// FULL FORM RENDERER (All Sections)
// =============================================================================

interface DynamicFormProps {
    sections: FormSection[];
    formData: Record<string, any>;
    onChange: (name: string, value: any) => void;
    errors?: Record<string, string>;
}

export function DynamicForm({ sections, formData, onChange, errors = {} }: DynamicFormProps) {
    return (
        <div className="space-y-8">
            {sections.map((section, index) => (
                <motion.div
                    key={section.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                >
                    <FormSectionRenderer
                        section={section}
                        formData={formData}
                        onChange={onChange}
                        errors={errors}
                    />
                    {index < sections.length - 1 && (
                        <hr className="mt-8 border-slate-200" />
                    )}
                </motion.div>
            ))}
        </div>
    );
}
