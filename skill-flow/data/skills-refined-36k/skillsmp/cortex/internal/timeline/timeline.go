package timeline

import (
	"database/sql"
	"fmt"
	"time"
)

// DayStats holds aggregated statistics for a single day
type DayStats struct {
	Date         string             // YYYY-MM-DD format
	TotalEvents  int                // Total events on this day
	BySender     map[string]int     // Events grouped by sender name
	ByChannel    map[string]int     // Events grouped by channel
	ByDirection  map[string]int     // Events grouped by direction (sent/received)
}

// TimelineOptions specifies what time period to query
type TimelineOptions struct {
	StartDate time.Time
	EndDate   time.Time
}

// QueryTimeline retrieves event statistics grouped by day for the specified time period
func QueryTimeline(db *sql.DB, opts TimelineOptions) ([]DayStats, error) {
	// Query to get daily aggregations
	query := `
		SELECT
			DATE(e.timestamp, 'unixepoch', 'localtime') as day,
			COUNT(*) as total_events,
			COALESCE(p.display_name, p.canonical_name, 'Unknown') as sender_name,
			e.channel,
			e.direction,
			COUNT(*) as count
		FROM events e
		LEFT JOIN event_participants ep ON e.id = ep.event_id AND ep.role = 'sender'
		LEFT JOIN persons p ON ep.person_id = p.id
		WHERE e.timestamp >= ? AND e.timestamp < ?
		GROUP BY day, sender_name, e.channel, e.direction
		ORDER BY day DESC, count DESC
	`

	rows, err := db.Query(query, opts.StartDate.Unix(), opts.EndDate.Unix())
	if err != nil {
		return nil, fmt.Errorf("failed to query timeline: %w", err)
	}
	defer rows.Close()

	// Group results by day
	dayMap := make(map[string]*DayStats)
	var days []string // Track order

	for rows.Next() {
		var day, senderName, channel, direction string
		var totalEvents, count int

		err := rows.Scan(&day, &totalEvents, &senderName, &channel, &direction, &count)
		if err != nil {
			return nil, fmt.Errorf("failed to scan timeline row: %w", err)
		}

		// Initialize day stats if needed
		if _, exists := dayMap[day]; !exists {
			dayMap[day] = &DayStats{
				Date:        day,
				TotalEvents: 0,
				BySender:    make(map[string]int),
				ByChannel:   make(map[string]int),
				ByDirection: make(map[string]int),
			}
			days = append(days, day)
		}

		stats := dayMap[day]
		stats.BySender[senderName] += count
		stats.ByChannel[channel] += count
		stats.ByDirection[direction] += count
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("error iterating timeline: %w", err)
	}

	// Get total events per day (separate query for accuracy)
	totalQuery := `
		SELECT
			DATE(timestamp, 'unixepoch', 'localtime') as day,
			COUNT(*) as total
		FROM events
		WHERE timestamp >= ? AND timestamp < ?
		GROUP BY day
		ORDER BY day DESC
	`

	totalRows, err := db.Query(totalQuery, opts.StartDate.Unix(), opts.EndDate.Unix())
	if err != nil {
		return nil, fmt.Errorf("failed to query total events: %w", err)
	}
	defer totalRows.Close()

	for totalRows.Next() {
		var day string
		var total int
		err := totalRows.Scan(&day, &total)
		if err != nil {
			return nil, fmt.Errorf("failed to scan total: %w", err)
		}
		if stats, exists := dayMap[day]; exists {
			stats.TotalEvents = total
		}
	}

	if err := totalRows.Err(); err != nil {
		return nil, fmt.Errorf("error iterating totals: %w", err)
	}

	// Convert map to slice in order
	result := make([]DayStats, 0, len(days))
	for _, day := range days {
		result = append(result, *dayMap[day])
	}

	return result, nil
}

// ParseTimelineArg parses a timeline argument into start/end dates
// Supports: "YYYY-MM-DD" (single day), "YYYY-MM" (month), "YYYY" (year)
func ParseTimelineArg(arg string) (TimelineOptions, error) {
	var opts TimelineOptions

	// Try YYYY-MM-DD format (specific day)
	if t, err := time.Parse("2006-01-02", arg); err == nil {
		opts.StartDate = time.Date(t.Year(), t.Month(), t.Day(), 0, 0, 0, 0, time.Local)
		opts.EndDate = opts.StartDate.AddDate(0, 0, 1)
		return opts, nil
	}

	// Try YYYY-MM format (month)
	if t, err := time.Parse("2006-01", arg); err == nil {
		opts.StartDate = time.Date(t.Year(), t.Month(), 1, 0, 0, 0, 0, time.Local)
		opts.EndDate = opts.StartDate.AddDate(0, 1, 0)
		return opts, nil
	}

	// Try YYYY format (year)
	if t, err := time.Parse("2006", arg); err == nil {
		opts.StartDate = time.Date(t.Year(), 1, 1, 0, 0, 0, 0, time.Local)
		opts.EndDate = opts.StartDate.AddDate(1, 0, 0)
		return opts, nil
	}

	return opts, fmt.Errorf("invalid date format '%s'. Use YYYY-MM-DD, YYYY-MM, or YYYY", arg)
}

// GetTodayRange returns start/end times for today
func GetTodayRange() TimelineOptions {
	now := time.Now()
	start := time.Date(now.Year(), now.Month(), now.Day(), 0, 0, 0, 0, time.Local)
	end := start.AddDate(0, 0, 1)
	return TimelineOptions{StartDate: start, EndDate: end}
}

// GetWeekRange returns start/end times for the current week (Monday-Sunday)
func GetWeekRange() TimelineOptions {
	now := time.Now()
	// Calculate Monday of current week
	weekday := int(now.Weekday())
	if weekday == 0 {
		weekday = 7 // Sunday = 7
	}
	daysToMonday := weekday - 1
	monday := now.AddDate(0, 0, -daysToMonday)

	start := time.Date(monday.Year(), monday.Month(), monday.Day(), 0, 0, 0, 0, time.Local)
	end := start.AddDate(0, 0, 7)
	return TimelineOptions{StartDate: start, EndDate: end}
}
