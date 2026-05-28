-- Get task statistics from Things 3
-- Returns counts for inbox, today, upcoming, anytime, someday, logbook
on run argv
    tell application "Things3"
        try
            -- Count todos in each list
            set inboxCount to count of to dos of list "Inbox"
            set todayCount to count of to dos of list "Today"
            set upcomingCount to count of to dos of list "Upcoming"
            set anytimeCount to count of to dos of list "Anytime"
            set somedayCount to count of to dos of list "Someday"

            -- Count completed (logbook) - this can be slow for large logbooks
            set logbookCount to 0
            try
                set logbookCount to count of to dos of list "Logbook"
            end try

            -- Count active projects
            set projectCount to count of projects whose status is open

            -- Count areas
            set areaCount to count of areas

            -- Build output: inbox|today|upcoming|anytime|someday|logbook|projects|areas
            set output to (inboxCount as string) & "|"
            set output to output & (todayCount as string) & "|"
            set output to output & (upcomingCount as string) & "|"
            set output to output & (anytimeCount as string) & "|"
            set output to output & (somedayCount as string) & "|"
            set output to output & (logbookCount as string) & "|"
            set output to output & (projectCount as string) & "|"
            set output to output & (areaCount as string)

            return output
        on error errMsg
            return "error:" & errMsg
        end try
    end tell
end run
