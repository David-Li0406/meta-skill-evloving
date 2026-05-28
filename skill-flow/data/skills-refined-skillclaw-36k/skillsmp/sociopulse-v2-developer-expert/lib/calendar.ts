// =============================================================================
// CALENDAR UTILITY - Add to Calendar Links Generator
// =============================================================================
// Generate URLs for Google Calendar, Outlook, and ICS file download

export interface CalendarEvent {
    title: string;
    description?: string;
    location?: string;
    startDate: Date;
    endDate: Date;
    // Optional fields for richer events
    organizer?: string;
    url?: string;
}

export interface CalendarLinks {
    google: string;
    outlook: string;
    outlookWeb: string;
    ics: string;
}

/**
 * Format date for Google Calendar (YYYYMMDDTHHmmssZ)
 */
function formatGoogleDate(date: Date): string {
    return date.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
}

/**
 * Format date for Outlook (YYYY-MM-DDTHH:mm:ss)
 */
function formatOutlookDate(date: Date): string {
    return date.toISOString().slice(0, 19);
}

/**
 * Format date for ICS file (YYYYMMDDTHHmmssZ)
 */
function formatICSDate(date: Date): string {
    return date.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
}

/**
 * Escape special characters for ICS format
 */
function escapeICS(text: string): string {
    return text
        .replace(/\\/g, '\\\\')
        .replace(/;/g, '\\;')
        .replace(/,/g, '\\,')
        .replace(/\n/g, '\\n');
}

/**
 * Generate calendar links for an event
 * 
 * @param event - The event details
 * @returns Object containing URLs for different calendar services
 * 
 * @example
 * ```ts
 * const links = getCalendarLinks({
 *   title: 'Coaching Session',
 *   description: 'Video coaching with Sophie',
 *   location: 'Video Call',
 *   startDate: new Date('2026-01-25T14:00:00'),
 *   endDate: new Date('2026-01-25T15:00:00'),
 * });
 * 
 * // links.google -> Google Calendar URL
 * // links.outlook -> Outlook desktop URL
 * // links.outlookWeb -> Outlook web URL
 * // links.ics -> ICS file data URI
 * ```
 */
export function getCalendarLinks(event: CalendarEvent): CalendarLinks {
    const {
        title,
        description = '',
        location = '',
        startDate,
        endDate,
        organizer,
        url,
    } = event;

    // Build description with optional URL
    let fullDescription = description;
    if (url) {
        fullDescription += `\n\n🔗 Lien: ${url}`;
    }
    if (organizer) {
        fullDescription += `\n\n👤 Organisé par: ${organizer}`;
    }

    // ==========================================================================
    // GOOGLE CALENDAR
    // https://calendar.google.com/calendar/render?action=TEMPLATE&...
    // ==========================================================================
    const googleParams = new URLSearchParams({
        action: 'TEMPLATE',
        text: title,
        dates: `${formatGoogleDate(startDate)}/${formatGoogleDate(endDate)}`,
        details: fullDescription,
        location: location,
        // Optional: Add conference/video call data
        // trp: 'false', // Show as free/busy
    });
    const googleUrl = `https://calendar.google.com/calendar/render?${googleParams.toString()}`;

    // ==========================================================================
    // OUTLOOK WEB (Office 365)
    // https://outlook.live.com/calendar/0/deeplink/compose?...
    // ==========================================================================
    const outlookWebParams = new URLSearchParams({
        path: '/calendar/action/compose',
        rru: 'addevent',
        subject: title,
        body: fullDescription,
        startdt: formatOutlookDate(startDate),
        enddt: formatOutlookDate(endDate),
        location: location,
    });
    const outlookWebUrl = `https://outlook.live.com/calendar/0/deeplink/compose?${outlookWebParams.toString()}`;

    // ==========================================================================
    // OUTLOOK DESKTOP (via webcal protocol fallback to ICS)
    // ==========================================================================
    // Outlook desktop typically opens .ics files, so we use the ICS URL
    const outlookDesktopUrl = outlookWebUrl; // Fallback to web version

    // ==========================================================================
    // ICS FILE (Universal - Apple Calendar, Outlook, etc.)
    // ==========================================================================
    const icsContent = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//SocioPulse//Booking Calendar//FR',
        'CALSCALE:GREGORIAN',
        'METHOD:PUBLISH',
        'BEGIN:VEVENT',
        `DTSTART:${formatICSDate(startDate)}`,
        `DTEND:${formatICSDate(endDate)}`,
        `SUMMARY:${escapeICS(title)}`,
        `DESCRIPTION:${escapeICS(fullDescription)}`,
        `LOCATION:${escapeICS(location)}`,
        `UID:${crypto.randomUUID()}@sociopulse.fr`,
        `DTSTAMP:${formatICSDate(new Date())}`,
        'STATUS:CONFIRMED',
        'SEQUENCE:0',
        // Add alarm/reminder 30 minutes before
        'BEGIN:VALARM',
        'TRIGGER:-PT30M',
        'ACTION:DISPLAY',
        `DESCRIPTION:Rappel: ${escapeICS(title)}`,
        'END:VALARM',
        'END:VEVENT',
        'END:VCALENDAR',
    ].join('\r\n');

    // Create a data URI for the ICS file
    const icsDataUri = `data:text/calendar;charset=utf-8,${encodeURIComponent(icsContent)}`;

    return {
        google: googleUrl,
        outlook: outlookDesktopUrl,
        outlookWeb: outlookWebUrl,
        ics: icsDataUri,
    };
}

/**
 * Download an ICS file directly
 * 
 * @param event - The event details
 * @param filename - Optional filename (defaults to event title)
 */
export function downloadICS(event: CalendarEvent, filename?: string): void {
    const links = getCalendarLinks(event);
    const link = document.createElement('a');
    link.href = links.ics;
    link.download = `${filename || event.title.replace(/[^a-zA-Z0-9]/g, '_')}.ics`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

/**
 * Open a calendar link in a new window
 * 
 * @param url - The calendar URL to open
 */
export function openCalendarLink(url: string): void {
    window.open(url, '_blank', 'noopener,noreferrer');
}
