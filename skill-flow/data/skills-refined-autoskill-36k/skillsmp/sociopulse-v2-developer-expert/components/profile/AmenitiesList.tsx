'use client';

import { motion } from 'framer-motion';
import { 
    Car, 
    Utensils, 
    Users, 
    Coffee, 
    Wifi, 
    Clock, 
    Shield, 
    Heart,
    Accessibility,
    TreePine,
    Bus,
    Baby,
    Dumbbell,
    Music,
    Palette,
    Dog,
    Sun,
    Moon,
    type LucideIcon
} from 'lucide-react';

export type AmenityType = 
    | 'parking'
    | 'meals'
    | 'young_team'
    | 'coffee'
    | 'wifi'
    | 'flexible_hours'
    | 'insurance'
    | 'care'
    | 'accessibility'
    | 'garden'
    | 'transport'
    | 'childcare'
    | 'gym'
    | 'music_therapy'
    | 'art_therapy'
    | 'pets_allowed'
    | 'day_shift'
    | 'night_shift';

export interface Amenity {
    type: AmenityType;
    label?: string;
}

const amenityConfig: Record<AmenityType, {
    icon: LucideIcon;
    label: string;
}> = {
    parking: {
        icon: Car,
        label: 'Parking gratuit',
    },
    meals: {
        icon: Utensils,
        label: 'Repas offert',
    },
    young_team: {
        icon: Users,
        label: 'Équipe jeune',
    },
    coffee: {
        icon: Coffee,
        label: 'Café à volonté',
    },
    wifi: {
        icon: Wifi,
        label: 'WiFi disponible',
    },
    flexible_hours: {
        icon: Clock,
        label: 'Horaires flexibles',
    },
    insurance: {
        icon: Shield,
        label: 'Assurance incluse',
    },
    care: {
        icon: Heart,
        label: 'Ambiance bienveillante',
    },
    accessibility: {
        icon: Accessibility,
        label: 'Accessible PMR',
    },
    garden: {
        icon: TreePine,
        label: 'Espace vert',
    },
    transport: {
        icon: Bus,
        label: 'Transports à proximité',
    },
    childcare: {
        icon: Baby,
        label: 'Crèche d\'entreprise',
    },
    gym: {
        icon: Dumbbell,
        label: 'Salle de sport',
    },
    music_therapy: {
        icon: Music,
        label: 'Musicothérapie',
    },
    art_therapy: {
        icon: Palette,
        label: 'Art-thérapie',
    },
    pets_allowed: {
        icon: Dog,
        label: 'Animaux acceptés',
    },
    day_shift: {
        icon: Sun,
        label: 'Poste de jour',
    },
    night_shift: {
        icon: Moon,
        label: 'Poste de nuit',
    },
};

export interface AmenitiesListProps {
    amenities: Amenity[];
    /** Display style */
    variant?: 'grid' | 'inline' | 'compact';
    /** Maximum items to show before "more" */
    maxVisible?: number;
}

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: {
            staggerChildren: 0.05,
        },
    },
};

const itemVariants = {
    hidden: { opacity: 0, scale: 0.9 },
    visible: {
        opacity: 1,
        scale: 1,
        transition: {
            type: 'spring' as const,
            stiffness: 200,
            damping: 20,
        },
    },
};

export function AmenitiesList({ 
    amenities, 
    variant = 'grid',
    maxVisible = 8,
}: AmenitiesListProps) {
    if (amenities.length === 0) return null;

    const visibleAmenities = amenities.slice(0, maxVisible);
    const hiddenCount = amenities.length - maxVisible;

    if (variant === 'compact') {
        return (
            <div className="flex flex-wrap gap-2">
                {visibleAmenities.map((amenity, index) => {
                    const config = amenityConfig[amenity.type];
                    const Icon = config.icon;

                    return (
                        <span
                            key={index}
                            className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-600 border border-transparent hover:border-brand-200 transition-all duration-200"
                            title={amenity.label || config.label}
                        >
                            <span className="w-4 h-4 rounded-full bg-blue-50 flex items-center justify-center flex-shrink-0">
                                <Icon className="w-2.5 h-2.5 text-blue-600" />
                            </span>
                            {amenity.label || config.label}
                        </span>
                    );
                })}
                {hiddenCount > 0 && (
                    <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-500 border border-transparent hover:border-slate-200 cursor-pointer transition-all duration-200">
                        +{hiddenCount}
                    </span>
                )}
            </div>
        );
    }

    if (variant === 'inline') {
        return (
            <motion.div
                variants={containerVariants}
                initial="hidden"
                animate="visible"
                className="flex flex-wrap gap-2"
            >
                {visibleAmenities.map((amenity, index) => {
                    const config = amenityConfig[amenity.type];
                    const Icon = config.icon;

                    return (
                        <motion.div
                            key={index}
                            variants={itemVariants}
                            whileHover={{ scale: 1.02 }}
                            className="inline-flex items-center gap-2 px-3 py-2 rounded-xl bg-white border border-slate-100 hover:border-brand-200 shadow-sm hover:shadow transition-all duration-200"
                        >
                            <span className="w-6 h-6 rounded-full bg-blue-50 flex items-center justify-center flex-shrink-0">
                                <Icon className="w-3.5 h-3.5 text-blue-600" />
                            </span>
                            <span className="text-sm text-slate-600">
                                {amenity.label || config.label}
                            </span>
                        </motion.div>
                    );
                })}
            </motion.div>
        );
    }

    // Grid variant (default) - Premium Icon + Text Design
    // 2 columns on mobile, 3 columns on desktop
    return (
        <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="grid grid-cols-2 sm:grid-cols-3 gap-3"
        >
            {visibleAmenities.map((amenity, index) => {
                const config = amenityConfig[amenity.type];
                const Icon = config.icon;

                return (
                    <motion.div
                        key={index}
                        variants={itemVariants}
                        whileHover={{ scale: 1.02 }}
                        className="flex items-center gap-3 p-3 rounded-xl bg-white border border-slate-100 hover:border-brand-200 shadow-sm hover:shadow transition-all duration-200 cursor-default"
                    >
                        {/* Icon Circle - Blue theme */}
                        <div className="w-8 h-8 rounded-full bg-blue-50 flex items-center justify-center flex-shrink-0">
                            <Icon className="w-4 h-4 text-blue-600" />
                        </div>
                        <span className="text-sm text-slate-600">
                            {amenity.label || config.label}
                        </span>
                    </motion.div>
                );
            })}
            
            {hiddenCount > 0 && (
                <motion.button
                    variants={itemVariants}
                    whileHover={{ scale: 1.02 }}
                    className="flex items-center justify-center gap-2 p-3 rounded-xl bg-slate-50 border border-slate-200 text-sm font-medium text-slate-500 hover:text-brand-600 hover:border-brand-200 transition-all duration-200 cursor-pointer"
                >
                    +{hiddenCount} autres
                </motion.button>
            )}
        </motion.div>
    );
}

// Helper to convert string array to Amenity array
export function parseAmenities(amenityStrings: string[]): Amenity[] {
    const typeMap: Record<string, AmenityType> = {
        'parking': 'parking',
        'parking gratuit': 'parking',
        'repas': 'meals',
        'repas offert': 'meals',
        'équipe jeune': 'young_team',
        'jeune équipe': 'young_team',
        'café': 'coffee',
        'wifi': 'wifi',
        'horaires flexibles': 'flexible_hours',
        'flexible': 'flexible_hours',
        'assurance': 'insurance',
        'bienveillant': 'care',
        'bienveillance': 'care',
        'accessible': 'accessibility',
        'pmr': 'accessibility',
        'jardin': 'garden',
        'espace vert': 'garden',
        'transport': 'transport',
        'métro': 'transport',
        'crèche': 'childcare',
        'sport': 'gym',
        'musique': 'music_therapy',
        'musicothérapie': 'music_therapy',
        'art': 'art_therapy',
        'art-thérapie': 'art_therapy',
        'animaux': 'pets_allowed',
        'jour': 'day_shift',
        'nuit': 'night_shift',
    };

    return amenityStrings.map(str => {
        const normalized = str.toLowerCase().trim();
        const type = typeMap[normalized] || 'care';
        return { type, label: str };
    });
}
