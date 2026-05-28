'use client';

import { motion } from 'framer-motion';
import {
    Car,
    Utensils,
    Coffee,
    Wifi,
    ParkingCircle,
    ShowerHead,
    Sofa,
    CheckCircle,
} from 'lucide-react';

// ===========================================
// TYPES
// ===========================================

export interface Amenity {
    id: string;
    label: string;
    icon: typeof Car;
}

export interface AmenitiesSelectorProps {
    value: string[];
    onChange: (amenities: string[]) => void;
    disabled?: boolean;
}

// ===========================================
// AMENITIES OPTIONS
// ===========================================

export const AMENITIES: Amenity[] = [
    { id: 'parking', label: 'Parking', icon: ParkingCircle },
    { id: 'meals', label: 'Repas', icon: Utensils },
    { id: 'coffee', label: 'Café', icon: Coffee },
    { id: 'wifi', label: 'Wifi', icon: Wifi },
    { id: 'shower', label: 'Douche', icon: ShowerHead },
    { id: 'lounge', label: 'Salle de repos', icon: Sofa },
];

// ===========================================
// COMPONENT
// ===========================================

export function AmenitiesSelector({
    value,
    onChange,
    disabled = false,
}: AmenitiesSelectorProps) {
    const toggleAmenity = (amenityId: string) => {
        if (disabled) return;

        if (value.includes(amenityId)) {
            onChange(value.filter(id => id !== amenityId));
        } else {
            onChange([...value, amenityId]);
        }
    };

    return (
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {AMENITIES.map((amenity) => {
                const Icon = amenity.icon;
                const isSelected = value.includes(amenity.id);

                return (
                    <motion.button
                        key={amenity.id}
                        type="button"
                        onClick={() => toggleAmenity(amenity.id)}
                        disabled={disabled}
                        whileHover={{ scale: disabled ? 1 : 1.02 }}
                        whileTap={{ scale: disabled ? 1 : 0.98 }}
                        className={`
                            relative flex flex-col items-center gap-2 p-4 rounded-2xl
                            border-2 transition-all
                            ${isSelected
                                ? 'border-brand-500 bg-brand-50 text-brand-600'
                                : 'border-slate-200 bg-white text-slate-600 hover:border-slate-300 hover:bg-slate-50'
                            }
                            ${disabled ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer'}
                        `}
                    >
                        {/* Selected Indicator */}
                        {isSelected && (
                            <motion.div
                                initial={{ scale: 0 }}
                                animate={{ scale: 1 }}
                                className="absolute -top-1.5 -right-1.5 w-5 h-5 rounded-full bg-brand-600 text-white flex items-center justify-center"
                            >
                                <CheckCircle className="w-3.5 h-3.5" />
                            </motion.div>
                        )}

                        <Icon className={`w-6 h-6 ${isSelected ? 'text-brand-600' : 'text-slate-400'}`} />
                        <span className="text-sm font-medium">{amenity.label}</span>
                    </motion.button>
                );
            })}
        </div>
    );
}
