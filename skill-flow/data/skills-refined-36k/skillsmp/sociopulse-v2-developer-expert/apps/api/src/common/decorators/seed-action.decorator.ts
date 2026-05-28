/**
 * =============================================================================
 * SEED ACTION DECORATOR - Scarcity Feed Algorithm
 * =============================================================================
 * 
 * Marks an endpoint for seed interception. When applied, the SeedInterceptionGuard
 * will check if the target entity is a seed account and return a FOMO message.
 * 
 * USAGE:
 * @UseGuards(JwtAuthGuard, SeedInterceptionGuard)
 * @SeedAction('CONTACT_TALENT')
 * async contactTalent() { }
 */

import { SetMetadata } from '@nestjs/common';
import { SEED_ACTION_KEY, SeedActionType } from '../guards/seed-interception.guard';

/**
 * Decorator to specify which seed action type applies to this endpoint.
 * Used by SeedInterceptionGuard to determine how to extract target ID
 * and which FOMO message to return.
 * 
 * @param action - The type of seed action: 'CONTACT_TALENT' | 'APPLY_MISSION' | 'BOOK_SERVICE' | 'START_CHAT'
 */
export const SeedAction = (action: SeedActionType) => SetMetadata(SEED_ACTION_KEY, action);
