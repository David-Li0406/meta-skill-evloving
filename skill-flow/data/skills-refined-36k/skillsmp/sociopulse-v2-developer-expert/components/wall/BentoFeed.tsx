'use client';

import { motion } from 'framer-motion';
import { SmartCard, type DiscoveryMode } from './SmartCard';

export interface BentoFeedProps {
    items: any[];
    mode: DiscoveryMode;
    isLoading?: boolean;
}

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: {
            staggerChildren: 0.06,
            delayChildren: 0.05,
        },
    },
};

const itemVariants = {
    hidden: { opacity: 0, y: 14 },
    visible: {
        opacity: 1,
        y: 0,
        transition: {
            type: 'spring' as const,
            stiffness: 110,
            damping: 16,
        },
    },
};

const isUrgentMission = (item: any) => {
    const isMission = String(item?.type || '').toUpperCase() === 'MISSION' || Boolean(item?.urgencyLevel);
    if (!isMission) return false;
    const urgency = String(item?.urgencyLevel || '').toUpperCase();
    return urgency === 'HIGH' || urgency === 'CRITICAL';
};

const isService = (item: any) =>
    String(item?.type || '').toUpperCase() === 'SERVICE' ||
    Boolean(item?.serviceType) ||
    Boolean(item?.basePrice) ||
    Boolean(item?.profile);

const getSpanClass = (item: any, index: number) => {
    if (isService(item) && index % 7 === 0) {
        return 'md:col-span-2 md:row-span-2';
    }

    if (isUrgentMission(item)) {
        return 'md:col-span-2';
    }

    if (index % 11 === 5) {
        return 'md:col-span-2';
    }

    return '';
};

export function BentoFeed({ items, mode, isLoading = false }: BentoFeedProps) {
    if (isLoading && items.length === 0) {
        return (
            <div className="grid grid-cols-1 md:grid-cols-3 auto-rows-[18rem] gap-5 md:gap-6 [grid-auto-flow:dense]">
                {Array.from({ length: 9 }).map((_, index) => (
                    <div
                        key={index}
                        className={`rounded-3xl bg-white/60 backdrop-blur-md border border-white/60 shadow-soft animate-pulse ${
                            index % 7 === 0 ? 'md:col-span-2 md:row-span-2' : ''
                        }`}
                    />
                ))}
            </div>
        );
    }

    return (
        <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="grid grid-cols-1 md:grid-cols-3 auto-rows-[18rem] gap-5 md:gap-6 [grid-auto-flow:dense]"
        >
            {items.map((item, index) => (
                <motion.div
                    key={String(item?.id ?? index)}
                    variants={itemVariants}
                    className={`h-full ${getSpanClass(item, index)}`}
                >
                    <SmartCard item={item} mode={mode} />
                </motion.div>
            ))}
        </motion.div>
    );
}

