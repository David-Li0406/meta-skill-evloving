import {
  Controller,
  Get,
  Post,
  Delete,
  Query,
  Body,
  Param,
  UseGuards,
  BadRequestException,
} from '@nestjs/common';
import { AvailabilityService } from './availability.service';
import { JwtAuthGuard } from '../common/guards';

// =============================================================================
// AVAILABILITY CONTROLLER
// Endpoints for managing talent availability and fetching slots
// =============================================================================

// DTOs
class GetSlotsQueryDto {
  talentId: string;
  date: string; // YYYY-MM-DD format
  duration?: number;
}

class CreateSlotDto {
  profileId: string;
  dayOfWeek: number; // 0-6 (Sunday-Saturday)
  startTime: string; // HH:mm format
  endTime: string;   // HH:mm format
  duration?: number;
  isRecurring?: boolean;
  specificDate?: string;
}

class BulkUpsertSlotDto {
  dayOfWeek: number;
  startTime: string;
  endTime: string;
  duration?: number;
  isRecurring?: boolean;
  specificDate?: string;
  isActive?: boolean;
}

class BulkUpsertSlotsDto {
  profileId: string;
  slots: BulkUpsertSlotDto[];
  replaceExisting?: boolean;
}

@Controller('availability')
export class AvailabilityController {
  constructor(private readonly availabilityService: AvailabilityService) {}

  /**
   * GET /api/v1/availability/slots
   * 
   * Get available time slots for a talent on a specific date.
   * This is the main endpoint for the booking calendar.
   * 
   * Query params:
   * - talentId: The talent's user ID
   * - date: Date in YYYY-MM-DD format
   * - duration: (optional) Service duration in minutes
   * 
   * Returns: Array of available time slots
   */
  @Get('slots')
  async getAvailableSlots(@Query() query: GetSlotsQueryDto) {
    const { talentId, date, duration } = query;

    // Validate required params
    if (!talentId) {
      throw new BadRequestException('talentId is required');
    }

    if (!date) {
      throw new BadRequestException('date is required (YYYY-MM-DD format)');
    }

    // Validate date format
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(date)) {
      throw new BadRequestException('Invalid date format. Use YYYY-MM-DD');
    }

    // Validate date is not in the past
    const targetDate = new Date(date);
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    if (targetDate < today) {
      throw new BadRequestException('Cannot get slots for past dates');
    }

    // Get available slots
    const result = await this.availabilityService.getAvailableSlots(
      talentId,
      date,
      duration ? parseInt(String(duration), 10) : 60,
    );

    return {
      success: true,
      data: result,
    };
  }

  /**
   * GET /api/v1/availability/config/:talentId
   * 
   * Get the availability configuration for a talent.
   * Returns all active availability slots (weekly schedule).
   */
  @Get('config/:talentId')
  async getTalentConfig(@Param('talentId') talentId: string) {
    const slots = await this.availabilityService.getTalentAvailabilityConfig(talentId);

    return {
      success: true,
      data: {
        talentId,
        slots,
      },
    };
  }

  /**
   * POST /api/v1/availability/slots
   * 
   * Create or update an availability slot.
   * Requires authentication.
   */
  @Post('slots')
  @UseGuards(JwtAuthGuard)
  async createSlot(@Body() body: CreateSlotDto | BulkUpsertSlotsDto) {
    if (Array.isArray((body as BulkUpsertSlotsDto).slots)) {
      const { profileId, slots, replaceExisting } = body as BulkUpsertSlotsDto;

      if (!profileId) {
        throw new BadRequestException('profileId is required');
      }

      if (!Array.isArray(slots)) {
        throw new BadRequestException('slots must be an array');
      }

      const activeSlots = slots.filter((slot) => slot.isActive !== false);

      activeSlots.forEach((slot) => {
        this.validateSlotInput(slot.dayOfWeek, slot.startTime, slot.endTime);
      });

      const created = await this.availabilityService.replaceRecurringSlots(
        profileId,
        activeSlots.map((slot) => ({
          dayOfWeek: slot.dayOfWeek,
          startTime: slot.startTime,
          endTime: slot.endTime,
          duration: slot.duration ?? 60,
          isRecurring: slot.isRecurring ?? true,
          specificDate: slot.specificDate ? new Date(slot.specificDate) : undefined,
        })),
        replaceExisting ?? true,
      );

      return {
        success: true,
        data: {
          profileId,
          count: created.length,
        },
      };
    }

    const { profileId, dayOfWeek, startTime, endTime, duration, isRecurring, specificDate } = body as CreateSlotDto;

    // Validate required fields
    if (!profileId) {
      throw new BadRequestException('profileId is required');
    }

    this.validateSlotInput(dayOfWeek, startTime, endTime);

    const slot = await this.availabilityService.upsertAvailabilitySlot(profileId, {
      dayOfWeek,
      startTime,
      endTime,
      duration: duration ?? 60,
      isRecurring: isRecurring ?? true,
      specificDate: specificDate ? new Date(specificDate) : undefined,
    });

    return {
      success: true,
      data: slot,
    };
  }

  private validateSlotInput(dayOfWeek: number, startTime: string, endTime: string) {
    if (dayOfWeek === undefined || dayOfWeek < 0 || dayOfWeek > 6) {
      throw new BadRequestException('dayOfWeek must be between 0 (Sunday) and 6 (Saturday)');
    }

    const timeRegex = /^([01]\d|2[0-3]):([0-5]\d)$/;
    if (!timeRegex.test(startTime)) {
      throw new BadRequestException('startTime must be in HH:mm format');
    }
    if (!timeRegex.test(endTime)) {
      throw new BadRequestException('endTime must be in HH:mm format');
    }

    if (startTime >= endTime) {
      throw new BadRequestException('startTime must be before endTime');
    }
  }

  /**
   * DELETE /api/v1/availability/slots/:slotId
   * 
   * Deactivate an availability slot.
   * Requires authentication.
   */
  @Delete('slots/:slotId')
  @UseGuards(JwtAuthGuard)
  async deleteSlot(@Param('slotId') slotId: string) {
    await this.availabilityService.deleteAvailabilitySlot(slotId);

    return {
      success: true,
      message: 'Availability slot deactivated',
    };
  }

  /**
   * GET /api/v1/availability/week/:talentId
   * 
   * Get available slots for a talent for the next 7 days.
   * Useful for showing a week view in the booking interface.
   */
  @Get('week/:talentId')
  async getWeekSlots(
    @Param('talentId') talentId: string,
    @Query('duration') duration?: number,
    @Query('startDate') startDateParam?: string,
  ) {
    const startDate = startDateParam ? new Date(startDateParam) : new Date();
    const results: Record<string, unknown> = {};

    // Get slots for the next 7 days
    for (let i = 0; i < 7; i++) {
      const currentDate = new Date(startDate);
      currentDate.setDate(currentDate.getDate() + i);
      const dateStr = currentDate.toISOString().split('T')[0];

      const daySlots = await this.availabilityService.getAvailableSlots(
        talentId,
        dateStr,
        duration ? parseInt(String(duration), 10) : 60,
      );

      results[dateStr] = daySlots.slots.filter(s => s.available);
    }

    return {
      success: true,
      data: {
        talentId,
        startDate: startDate.toISOString().split('T')[0],
        slotsByDate: results,
      },
    };
  }
}
