import {
  startOfDay,
  endOfDay,
  startOfWeek,
  endOfWeek,
  subDays,
  addDays,
  format,
  parse,
  isValid,
} from 'date-fns';

/**
 * Parse a date string into a Date object
 * Supports: "today", "yesterday", "2026-01-20", "2026-01-20 14:30"
 */
export function parseDate(input: string): Date {
  const lower = input.toLowerCase().trim();

  if (lower === 'today') {
    return new Date();
  }

  if (lower === 'yesterday') {
    return subDays(new Date(), 1);
  }

  if (lower === 'tomorrow') {
    return addDays(new Date(), 1);
  }

  // Try parsing as YYYY-MM-DD HH:MM
  if (/^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}$/.test(input)) {
    const parsed = parse(input, 'yyyy-MM-dd HH:mm', new Date());
    if (isValid(parsed)) return parsed;
  }

  // Try parsing as YYYY-MM-DD
  if (/^\d{4}-\d{2}-\d{2}$/.test(input)) {
    const parsed = parse(input, 'yyyy-MM-dd', new Date());
    if (isValid(parsed)) return parsed;
  }

  // Try parsing as MM/DD/YYYY
  if (/^\d{1,2}\/\d{1,2}\/\d{4}$/.test(input)) {
    const parsed = parse(input, 'M/d/yyyy', new Date());
    if (isValid(parsed)) return parsed;
  }

  // Fallback to native Date parsing
  const date = new Date(input);
  if (isValid(date)) return date;

  throw new Error(`Invalid date format: "${input}". Use YYYY-MM-DD or keywords like "today", "yesterday".`);
}

/**
 * Parse a datetime string into a timestamp (milliseconds)
 */
export function parseDateTimeToMs(input: string): number {
  return parseDate(input).getTime();
}

/**
 * Get start of day in milliseconds
 */
export function getStartOfDay(date: Date | string): number {
  const d = typeof date === 'string' ? parseDate(date) : date;
  return startOfDay(d).getTime();
}

/**
 * Get end of day in milliseconds
 */
export function getEndOfDay(date: Date | string): number {
  const d = typeof date === 'string' ? parseDate(date) : date;
  return endOfDay(d).getTime();
}

/**
 * Get start of week (Monday) for a date
 */
export function getWeekStart(date: Date | string): Date {
  const d = typeof date === 'string' ? parseDate(date) : date;
  return startOfWeek(d, { weekStartsOn: 1 }); // Monday
}

/**
 * Get end of week (Sunday) for a date
 */
export function getWeekEnd(date: Date | string): Date {
  const d = typeof date === 'string' ? parseDate(date) : date;
  return endOfWeek(d, { weekStartsOn: 1 }); // Sunday
}

/**
 * Get the week date range as timestamps
 */
export function getWeekRange(date: Date | string): { start: number; end: number } {
  const d = typeof date === 'string' ? parseDate(date) : date;
  return {
    start: startOfDay(getWeekStart(d)).getTime(),
    end: endOfDay(getWeekEnd(d)).getTime(),
  };
}

/**
 * Format a date as YYYY-MM-DD
 */
export function formatDateYMD(date: Date): string {
  return format(date, 'yyyy-MM-dd');
}

/**
 * Format a date as readable string
 */
export function formatDateReadable(date: Date): string {
  return format(date, 'MMM d, yyyy');
}

/**
 * Get day of week name
 */
export function getDayOfWeek(date: Date): string {
  return format(date, 'EEEE');
}

/**
 * Get all days in a week as an array
 */
export function getWeekDays(weekStart: Date): Date[] {
  const days: Date[] = [];
  for (let i = 0; i < 7; i++) {
    days.push(addDays(weekStart, i));
  }
  return days;
}

/**
 * Check if two dates are the same day
 */
export function isSameDay(date1: Date, date2: Date): boolean {
  return (
    date1.getFullYear() === date2.getFullYear() &&
    date1.getMonth() === date2.getMonth() &&
    date1.getDate() === date2.getDate()
  );
}
