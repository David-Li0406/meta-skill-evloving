import { Injectable } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

// =============================================================================
// AVAILABILITY SERVICE
// Calculate available slots for 1-to-1 bookings
// =============================================================================

export interface TimeSlot {
  startTime: Date;
  endTime: Date;
  available: boolean;
}

export interface AvailableSlotsResult {
  talentId: string;
  date: string;
  slots: TimeSlot[];
  timezone: string;
}

@Injectable()
export class AvailabilityService {
  private prisma = new PrismaClient();

  /**
   * Get available slots for a talent on a specific date
   * 
   * @param talentId - The talent's user ID
   * @param date - The date to check (YYYY-MM-DD format)
   * @param serviceDuration - Duration of the service in minutes (default: 60)
   * @returns Array of available time slots
   */
  async getAvailableSlots(
    talentId: string,
    date: string,
    serviceDuration: number = 60,
  ): Promise<AvailableSlotsResult> {
    // Parse the target date
    const targetDate = new Date(date);
    const dayOfWeek = targetDate.getDay(); // 0 = Sunday, 1 = Monday, etc.

    // Get talent's profile
    const user = await this.prisma.user.findUnique({
      where: { id: talentId },
      include: { profile: true },
    });

    if (!user?.profile) {
      return {
        talentId,
        date,
        slots: [],
        timezone: 'Europe/Paris',
      };
    }

    // Fetch availability slots for this day of week
    const availabilitySlots = await this.prisma.availabilitySlot.findMany({
      where: {
        profileId: user.profile.id,
        dayOfWeek,
        isActive: true,
        OR: [
          { isRecurring: true },
          {
            isRecurring: false,
            specificDate: {
              gte: new Date(date + 'T00:00:00'),
              lt: new Date(date + 'T23:59:59'),
            },
          },
        ],
      },
    });

    if (availabilitySlots.length === 0) {
      return {
        talentId,
        date,
        slots: [],
        timezone: 'Europe/Paris',
      };
    }

    // Fetch existing bookings for this date
    const startOfDay = new Date(date + 'T00:00:00');
    const endOfDay = new Date(date + 'T23:59:59');

    const existingBookings = await this.prisma.booking.findMany({
      where: {
        providerId: talentId,
        status: {
          in: ['PENDING', 'CONFIRMED', 'PAID', 'IN_PROGRESS'],
        },
        // Check sessionDate field for now (startTime/endTime will be added after db:push)
        sessionDate: { gte: startOfDay, lte: endOfDay },
      },
    });

    // =======================================================================
    // MISSION CONFLICT DETECTION
    // Check for accepted SOS/Relief Missions that block 1-to-1 slots
    // =======================================================================
    const acceptedMissions = await this.prisma.reliefMission.findMany({
      where: {
        assignedTalentId: talentId,
        status: {
          in: ['ASSIGNED', 'IN_PROGRESS'],
        },
        // Mission overlaps with the target date
        OR: [
          {
            // Single-day mission on this date
            startDate: { gte: startOfDay, lte: endOfDay },
          },
          {
            // Multi-day mission that spans this date
            AND: [
              { startDate: { lte: endOfDay } },
              { endDate: { gte: startOfDay } },
            ],
          },
        ],
      },
      select: {
        id: true,
        title: true,
        startDate: true,
        endDate: true,
        isNightShift: true,
      },
    });

    // Generate all possible time slots
    const allSlots: TimeSlot[] = [];

    for (const availability of availabilitySlots) {
      const slots = this.generateTimeSlots(
        targetDate,
        availability.startTime,
        availability.endTime,
        serviceDuration,
      );
      allSlots.push(...slots);
    }

    // Filter out slots that collide with existing bookings OR missions
    const availableSlots = allSlots.map((slot) => {
      // Check booking conflicts
      const isBooked = existingBookings.some((booking) => {
        // Check against sessionDate + sessionTime
        if (booking.sessionDate && booking.sessionTime) {
          const bookingStart = this.combineDateAndTime(
            booking.sessionDate,
            booking.sessionTime,
          );
          // Assume bookings are serviceDuration minutes
          const bookingEnd = new Date(bookingStart.getTime() + serviceDuration * 60 * 1000);
          return this.slotsOverlap(
            slot.startTime,
            slot.endTime,
            bookingStart,
            bookingEnd,
          );
        }

        return false;
      });

      // Check mission conflicts (SOS Renfort blocks 1-to-1 availability)
      const isBlockedByMission = acceptedMissions.some((mission) => {
        // ReliefMission uses startDate/endDate as full DateTime values
        // Check if the slot overlaps with the mission time range
        if (mission.startDate && mission.endDate) {
          return this.slotsOverlap(
            slot.startTime,
            slot.endTime,
            new Date(mission.startDate),
            new Date(mission.endDate),
          );
        }

        return false;
      });

      return {
        ...slot,
        available: !isBooked && !isBlockedByMission,
      };
    });

    // Sort by start time
    availableSlots.sort((a, b) => a.startTime.getTime() - b.startTime.getTime());

    return {
      talentId,
      date,
      slots: availableSlots,
      timezone: 'Europe/Paris',
    };
  }

  /**
   * Generate time slots within a time range
   */
  private generateTimeSlots(
    date: Date,
    startTimeStr: string,
    endTimeStr: string,
    slotDuration: number,
  ): TimeSlot[] {
    const slots: TimeSlot[] = [];

    const [startHour, startMinute] = startTimeStr.split(':').map(Number);
    const [endHour, endMinute] = endTimeStr.split(':').map(Number);

    // Create start and end times for the day
    const dayStart = new Date(date);
    dayStart.setHours(startHour, startMinute, 0, 0);

    const dayEnd = new Date(date);
    dayEnd.setHours(endHour, endMinute, 0, 0);

    // Generate slots
    let currentStart = new Date(dayStart);

    while (currentStart < dayEnd) {
      const currentEnd = new Date(currentStart.getTime() + slotDuration * 60 * 1000);
      
      // Only add if the slot ends before or at the availability end time
      if (currentEnd <= dayEnd) {
        slots.push({
          startTime: new Date(currentStart),
          endTime: new Date(currentEnd),
          available: true, // Will be updated later
        });
      }

      // Move to next slot (same duration as service)
      currentStart = new Date(currentEnd);
    }

    return slots;
  }

  /**
   * Check if two time slots overlap
   */
  private slotsOverlap(
    start1: Date,
    end1: Date,
    start2: Date,
    end2: Date,
  ): boolean {
    return start1 < end2 && end1 > start2;
  }

  /**
   * Combine a date with a time string
   */
  private combineDateAndTime(date: Date, timeStr: string): Date {
    const [hours, minutes] = timeStr.split(':').map(Number);
    const result = new Date(date);
    result.setHours(hours, minutes, 0, 0);
    return result;
  }

  /**
   * Get availability slots configuration for a talent
   */
  async getTalentAvailabilityConfig(talentId: string) {
    const user = await this.prisma.user.findUnique({
      where: { id: talentId },
      include: { profile: true },
    });

    if (!user?.profile) {
      return [];
    }

    return this.prisma.availabilitySlot.findMany({
      where: {
        profileId: user.profile.id,
        isActive: true,
      },
      orderBy: [
        { dayOfWeek: 'asc' },
        { startTime: 'asc' },
      ],
    });
  }

  /**
   * Create or update availability slot
   */
  async upsertAvailabilitySlot(
    profileId: string,
    data: {
      dayOfWeek: number;
      startTime: string;
      endTime: string;
      duration?: number;
      isRecurring?: boolean;
      specificDate?: Date;
    },
  ) {
    // Check if slot already exists for this day
    const existing = await this.prisma.availabilitySlot.findFirst({
      where: {
        profileId,
        dayOfWeek: data.dayOfWeek,
        startTime: data.startTime,
      },
    });

    if (existing) {
      return this.prisma.availabilitySlot.update({
        where: { id: existing.id },
        data: {
          endTime: data.endTime,
          duration: data.duration ?? 60,
          isRecurring: data.isRecurring ?? true,
          specificDate: data.specificDate,
          isActive: true,
        },
      });
    }

    return this.prisma.availabilitySlot.create({
      data: {
        profileId,
        dayOfWeek: data.dayOfWeek,
        startTime: data.startTime,
        endTime: data.endTime,
        duration: data.duration ?? 60,
        isRecurring: data.isRecurring ?? true,
        specificDate: data.specificDate,
      },
    });
  }

  /**
   * Replace recurring weekly slots for a profile
   */
  async replaceRecurringSlots(
    profileId: string,
    slots: {
      dayOfWeek: number;
      startTime: string;
      endTime: string;
      duration?: number;
      isRecurring?: boolean;
      specificDate?: Date;
    }[],
    replaceExisting: boolean = true,
  ) {
    return this.prisma.$transaction(async (tx) => {
      if (replaceExisting) {
        await tx.availabilitySlot.updateMany({
          where: {
            profileId,
            isRecurring: true,
          },
          data: { isActive: false },
        });
      }

      if (slots.length === 0) {
        return [];
      }

      const created = await Promise.all(
        slots.map((slot) =>
          tx.availabilitySlot.create({
            data: {
              profileId,
              dayOfWeek: slot.dayOfWeek,
              startTime: slot.startTime,
              endTime: slot.endTime,
              duration: slot.duration ?? 60,
              isRecurring: slot.isRecurring ?? true,
              specificDate: slot.specificDate,
              isActive: true,
            },
          }),
        ),
      );

      return created;
    });
  }

  /**
   * Delete availability slot
   */
  async deleteAvailabilitySlot(slotId: string) {
    return this.prisma.availabilitySlot.update({
      where: { id: slotId },
      data: { isActive: false },
    });
  }
}
