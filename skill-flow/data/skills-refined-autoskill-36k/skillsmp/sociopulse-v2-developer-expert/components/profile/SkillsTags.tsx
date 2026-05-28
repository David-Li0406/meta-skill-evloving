'use client';

import { motion } from 'framer-motion';
import { 
    Stethoscope,
    Heart,
    Brain,
    Activity,
    Pill,
    Baby,
    UserCheck,
    Car,
    Languages,
    Clock,
    Shield,
    Zap,
    Sparkles,
    type LucideIcon
} from 'lucide-react';

export interface Skill {
    name: string;
    category?: 'medical' | 'soft' | 'transport' | 'language' | 'certification';
    isHighlighted?: boolean;
}

export interface SkillsTagsProps {
    skills: Skill[];
    /** Display variant */
    variant?: 'pills' | 'badges' | 'chips';
    /** Maximum visible skills */
    maxVisible?: number;
    /** Enable animations */
    animated?: boolean;
}

// Skill category styling - Premium Soft Pill Design
// Default: slate-100 background, Highlighted: brand-50 background
const categoryStyles: Record<string, { bg: string; text: string; border: string; hoverBorder: string }> = {
    medical: {
        bg: 'bg-slate-100',
        text: 'text-slate-700',
        border: 'border-transparent',
        hoverBorder: 'hover:border-brand-200',
    },
    soft: {
        bg: 'bg-slate-100',
        text: 'text-slate-700',
        border: 'border-transparent',
        hoverBorder: 'hover:border-brand-200',
    },
    transport: {
        bg: 'bg-slate-100',
        text: 'text-slate-700',
        border: 'border-transparent',
        hoverBorder: 'hover:border-brand-200',
    },
    language: {
        bg: 'bg-slate-100',
        text: 'text-slate-700',
        border: 'border-transparent',
        hoverBorder: 'hover:border-brand-200',
    },
    certification: {
        bg: 'bg-slate-100',
        text: 'text-slate-700',
        border: 'border-transparent',
        hoverBorder: 'hover:border-brand-200',
    },
    default: {
        bg: 'bg-slate-100',
        text: 'text-slate-700',
        border: 'border-transparent',
        hoverBorder: 'hover:border-brand-200',
    },
};

// Highlighted skill style (brand theme)
const highlightedStyle = {
    bg: 'bg-brand-50',
    text: 'text-brand-700',
    border: 'border-brand-200',
    hoverBorder: 'hover:border-brand-300',
};

// Auto-detect category from skill name
function detectCategory(skillName: string): Skill['category'] {
    const normalized = skillName.toLowerCase();
    
    // Medical/Healthcare
    if (/infirmier|aide.soignant|médical|soins|santé|paramédical|kiné|ergo|psycho|dentaire/.test(normalized)) {
        return 'medical';
    }
    
    // Transport
    if (/permis|conduite|véhicule|voiture/.test(normalized)) {
        return 'transport';
    }
    
    // Languages
    if (/anglais|français|espagnol|allemand|arabe|langue|bilingue/.test(normalized)) {
        return 'language';
    }
    
    // Certifications
    if (/diplôme|certificat|formation|dees|deas|dei|bafa|psc1|sst/.test(normalized)) {
        return 'certification';
    }
    
    // Soft skills
    if (/gestion|stress|communication|écoute|patience|organisation|autonome|équipe/.test(normalized)) {
        return 'soft';
    }
    
    return undefined;
}

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: {
            staggerChildren: 0.03,
        },
    },
};

const itemVariants = {
    hidden: { opacity: 0, scale: 0.8, y: 10 },
    visible: {
        opacity: 1,
        scale: 1,
        y: 0,
        transition: {
            type: 'spring' as const,
            stiffness: 300,
            damping: 25,
        },
    },
};

export function SkillsTags({ 
    skills, 
    variant = 'pills',
    maxVisible = 12,
    animated = true,
}: SkillsTagsProps) {
    if (skills.length === 0) return null;

    const visibleSkills = skills.slice(0, maxVisible);
    const hiddenCount = skills.length - maxVisible;

    const Container = animated ? motion.div : 'div';
    const Item = animated ? motion.span : 'span';

    const containerProps = animated ? {
        variants: containerVariants,
        initial: 'hidden',
        animate: 'visible',
    } : {};

    const getItemProps = (skill: Skill, index: number) => animated ? {
        variants: itemVariants,
        whileHover: { scale: 1.05, transition: { duration: 0.2 } },
        whileTap: { scale: 0.98 },
        key: index,
    } : { key: index };

    if (variant === 'badges') {
        return (
            <Container {...containerProps} className="flex flex-wrap gap-2">
                {visibleSkills.map((skill, index) => {
                    const style = skill.isHighlighted ? highlightedStyle : categoryStyles[skill.category || detectCategory(skill.name) || 'default'];

                    return (
                        <Item
                            {...getItemProps(skill, index)}
                            className={`
                                inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border
                                ${style.bg} ${style.text} ${style.border} ${style.hoverBorder}
                                text-sm font-medium cursor-default
                                transition-all duration-200
                            `}
                        >
                            {skill.isHighlighted && <Sparkles className="w-3.5 h-3.5 text-brand-500" />}
                            {skill.name}
                        </Item>
                    );
                })}
                {hiddenCount > 0 && (
                    <Item
                        {...getItemProps({ name: 'more' }, visibleSkills.length)}
                        className="inline-flex items-center px-3 py-1.5 rounded-lg bg-slate-100 text-slate-500 text-sm font-medium border border-transparent hover:border-slate-200 cursor-pointer transition-all duration-200"
                    >
                        +{hiddenCount}
                    </Item>
                )}
            </Container>
        );
    }

    if (variant === 'chips') {
        return (
            <Container {...containerProps} className="flex flex-wrap gap-2">
                {visibleSkills.map((skill, index) => {
                    const style = skill.isHighlighted ? highlightedStyle : categoryStyles['default'];

                    return (
                        <Item
                            {...getItemProps(skill, index)}
                            className={`
                                inline-flex items-center gap-1 px-2.5 py-1 rounded-md border
                                ${style.bg} ${style.text} ${style.border} ${style.hoverBorder}
                                text-xs font-semibold uppercase tracking-wide
                                cursor-default transition-all duration-200
                            `}
                        >
                            {skill.name}
                        </Item>
                    );
                })}
            </Container>
        );
    }

    // Pills variant (default) - Premium Soft Pill Design
    return (
        <Container {...containerProps} className="flex flex-wrap gap-2">
            {visibleSkills.map((skill, index) => {
                const isHighlighted = skill.isHighlighted;

                return (
                    <Item
                        {...getItemProps(skill, index)}
                        className={`
                            inline-flex items-center gap-1.5 px-4 py-2 rounded-full border
                            text-sm font-medium cursor-default
                            transition-all duration-200
                            ${isHighlighted 
                                ? 'bg-brand-50 text-brand-700 border-brand-200 hover:border-brand-300' 
                                : 'bg-slate-100 text-slate-700 border-transparent hover:border-brand-200'
                            }
                        `}
                    >
                        {isHighlighted && (
                            <Sparkles className="w-3.5 h-3.5 text-brand-500" />
                        )}
                        {skill.name}
                    </Item>
                );
            })}
            {hiddenCount > 0 && (
                <Item
                    {...getItemProps({ name: 'more' }, visibleSkills.length)}
                    className="inline-flex items-center justify-center px-3 py-2 rounded-full bg-slate-100 text-slate-500 text-sm font-medium border border-transparent hover:border-brand-200 hover:text-brand-600 transition-all duration-200 cursor-pointer"
                    title={`${hiddenCount} compétences supplémentaires`}
                >
                    +{hiddenCount}
                </Item>
            )}
        </Container>
    );
}

// Helper to convert string array to Skill array
export function parseSkills(skillStrings: string[], highlightFirst?: number): Skill[] {
    return skillStrings.map((name, index) => ({
        name,
        category: detectCategory(name),
        isHighlighted: highlightFirst !== undefined && index < highlightFirst,
    }));
}
