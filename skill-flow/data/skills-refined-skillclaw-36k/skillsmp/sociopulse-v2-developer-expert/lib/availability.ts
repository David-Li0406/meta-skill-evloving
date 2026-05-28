import { getApiUrl } from './config';

// =============================================================================
// AVAILABILITY API CLIENT
// Functions to interact with the availability endpoints
// =============================================================================

export interface TimeSlot {
  startTime: string; // ISO date string
  endTime: string;   // ISO date string
  available: boolean;
}

export interface AvailableSlotsResponse {
  talentId: string;
  date: string;
  slots: TimeSlot[];
  timezone: string;
}

export interface AvailabilityConfig {
  id: string;
  profileId: string;
  dayOfWeek: number;
  startTime: string;
  endTime: string;
  duration: number;
  isActive: boolean;
  isRecurring: boolean;
  specificDate?: string;
}

export interface WeeklyWorkingHours {
  dayOfWeek: number;
  startTime: string;
  endTime: string;
  isActive: boolean;
}

export interface AvailabilitySlotInput {
  dayOfWeek: number;
  startTime: string;
  endTime: string;
  duration?: number;
  isRecurring?: boolean;
  specificDate?: string;
  isActive?: boolean;
}

export interface BulkUpsertAvailabilitySlotsInput {
  profileId: string;
  slots: AvailabilitySlotInput[];
  replaceExisting?: boolean;
}

const getAuthToken = (): string | null => {
  if (typeof window === 'undefined') return null;

  const candidates = [
    window.localStorage.getItem('accessToken'),
    window.localStorage.getItem('token'),
    window.localStorage.getItem('jwt'),
  ].filter(Boolean) as string[];

  if (candidates.length > 0) return candidates[0];

  const cookieToken = document.cookie
    ?.split(';')
    .map((c) => c.trim())
    .find((c) => c.startsWith('token=') || c.startsWith('accessToken='));

  if (cookieToken) {
    const [, value] = cookieToken.split('=');
    return value;
  }

  return null;
};

const getAuthHeaders = (tokenOverride?: string): Record<string, string> => {
  const token = tokenOverride ?? getAuthToken();
  if (!token) return {};

  const cleaned = token.replace(/^Bearer\s+/i, '').trim();
  return { Authorization: `Bearer ${cleaned}` };
};

/**
 * Get available time slots for a talent on a specific date
 * 
 * @param talentId - The talent's user ID
 * @param date - The date in YYYY-MM-DD format
 * @param duration - Optional service duration in minutes
 * @returns Promise with available slots
 */
export async function getAvailableSlots(
  talentId: string,
  date: string,
  duration?: number,
): Promise<AvailableSlotsResponse> {
  const apiUrl = getApiUrl();
  const params = new URLSearchParams({
    talentId,
    date,
    ...(duration && { duration: String(duration) }),
  });

  const response = await fetch(`${apiUrl}/availability/slots?${params}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to fetch available slots');
  }

  const result = await response.json();
  return result.data;
}

/**
 * Get available slots for a talent for the next 7 days
 * 
 * @param talentId - The talent's user ID
 * @param duration - Optional service duration in minutes
 * @param startDate - Optional start date (defaults to today)
 * @returns Promise with slots organized by date
 */
export async function getWeekSlots(
  talentId: string,
  duration?: number,
  startDate?: string,
): Promise<{
  talentId: string;
  startDate: string;
  slotsByDate: Record<string, TimeSlot[]>;
}> {
  const apiUrl = getApiUrl();
  const params = new URLSearchParams({
    ...(duration && { duration: String(duration) }),
    ...(startDate && { startDate }),
  });

  const response = await fetch(
    `${apiUrl}/availability/week/${talentId}?${params}`,
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    },
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to fetch week slots');
  }

  const result = await response.json();
  return result.data;
}

/**
 * Get the availability configuration for a talent
 * 
 * @param talentId - The talent's user ID
 * @returns Promise with availability slots configuration
 */
export async function getTalentAvailabilityConfig(
  talentId: string,
): Promise<AvailabilityConfig[]> {
  const apiUrl = getApiUrl();

  const response = await fetch(`${apiUrl}/availability/config/${talentId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to fetch availability config');
  }

  const result = await response.json();
  return result.data.slots;
}

/**
 * Create or update an availability slot (requires auth)
 * 
 * @param token - JWT access token
 * @param data - Slot data
 * @returns Promise with created/updated slot
 */
export async function upsertAvailabilitySlot(
  token: string,
  data: {
    profileId: string;
    dayOfWeek: number;
    startTime: string;
    endTime: string;
    duration?: number;
    isRecurring?: boolean;
    specificDate?: string;
  },
): Promise<AvailabilityConfig> {
  const apiUrl = getApiUrl();

  const response = await fetch(`${apiUrl}/availability/slots`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to create/update slot');
  }

  const result = await response.json();
  return result.data;
}

/**
 * Bulk replace weekly availability slots (requires auth)
 *
 * @param data - Bulk slots payload
 * @param tokenOverride - Optional JWT access token
 * @returns Promise with created slots count
 */
export async function bulkUpsertAvailabilitySlots(
  data: BulkUpsertAvailabilitySlotsInput,
  tokenOverride?: string,
): Promise<{ profileId: string; count: number }> {
  const apiUrl = getApiUrl();
  const authHeaders = getAuthHeaders(tokenOverride);

  if (!authHeaders.Authorization) {
    throw new Error('Missing auth token');
  }

  const response = await fetch(`${apiUrl}/availability/slots`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...authHeaders,
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.message || 'Failed to save availability slots');
  }

  const result = await response.json();
  return result.data;
}

/**
 * Convert weekly working hours config into slot payloads
 */
export function buildSlotsFromWeeklyConfig(
  config: WeeklyWorkingHours[],
  duration: number = 60,
): AvailabilitySlotInput[] {
  return config
    .filter((day) => day.isActive)
    .map((day) => ({
      dayOfWeek: day.dayOfWeek,
      startTime: day.startTime,
      endTime: day.endTime,
      duration,
      isRecurring: true,
    }));
}

/**
 * Delete (deactivate) an availability slot (requires auth)
 * 
 * @param token - JWT access token
 * @param slotId - The slot ID to delete
 */
export async function deleteAvailabilitySlot(
  token: string,
  slotId: string,
): Promise<void> {
  const apiUrl = getApiUrl();

  const response = await fetch(`${apiUrl}/availability/slots/${slotId}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to delete slot');
  }
}

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

/**
 * Format a time slot for display
 */
export function formatTimeSlot(slot: TimeSlot): string {
  const start = new Date(slot.startTime);
  const end = new Date(slot.endTime);
  
  const formatTime = (date: Date) => 
    date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
  
  return `${formatTime(start)} - ${formatTime(end)}`;
}

/**
 * Get day name from day of week number
 */
export function getDayName(dayOfWeek: number): string {
  const days = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'];
  return days[dayOfWeek] || '';
}

/**
 * Get short day name from day of week number
 */
export function getShortDayName(dayOfWeek: number): string {
  const days = ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'];
  return days[dayOfWeek] || '';
}

/**
 * Generate an array of dates for the next N days
 */
export function getNextNDays(n: number, startFrom?: Date): Date[] {
  const start = startFrom || new Date();
  const dates: Date[] = [];
  
  for (let i = 0; i < n; i++) {
    const date = new Date(start);
    date.setDate(date.getDate() + i);
    dates.push(date);
  }
  
  return dates;
}

/**
 * Format a date for API calls (YYYY-MM-DD)
 */
export function formatDateForApi(date: Date): string {
  return date.toISOString().split('T')[0];
}
