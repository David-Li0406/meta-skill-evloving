on run argv
    -- Parameters: query, listFilter, tagFilter, hasUrlFilter, maxResults
    -- query: keyword to search in title (required, use "*" for all)
    -- listFilter: inbox, today, anytime, upcoming, someday, or "" for all
    -- tagFilter: tag name to filter by, or "" for none
    -- hasUrlFilter: "true" to only show URL tasks, "" for all
    -- maxResults: limit results (optional)

    set searchQuery to ""
    set listFilter to ""
    set tagFilter to ""
    set hasUrlFilter to ""
    set maxResults to 100

    if (count of argv) > 0 then set searchQuery to item 1 of argv
    if (count of argv) > 1 then set listFilter to item 2 of argv
    if (count of argv) > 2 then set tagFilter to item 3 of argv
    if (count of argv) > 3 then set hasUrlFilter to item 4 of argv
    if (count of argv) > 4 then
        try
            set maxResults to (item 5 of argv) as integer
        end try
    end if

    tell application "Things3"
        set output to ""
        set todoCount to 0

        -- Determine which lists to search
        set listsToSearch to {}
        if listFilter is "" or listFilter is "*" then
            set listsToSearch to {"Inbox", "Today", "Anytime", "Upcoming", "Someday"}
        else if listFilter is "inbox" then
            set listsToSearch to {"Inbox"}
        else if listFilter is "today" then
            set listsToSearch to {"Today"}
        else if listFilter is "anytime" then
            set listsToSearch to {"Anytime"}
        else if listFilter is "upcoming" then
            set listsToSearch to {"Upcoming"}
        else if listFilter is "someday" then
            set listsToSearch to {"Someday"}
        end if

        repeat with listName in listsToSearch
            if todoCount ≥ maxResults then exit repeat

            repeat with toDo in to dos of list listName
                if todoCount ≥ maxResults then exit repeat

                try
                    set todoId to id of toDo
                    set todoName to name of toDo

                    -- Check query match (case insensitive)
                    set matchesQuery to false
                    if searchQuery is "" or searchQuery is "*" then
                        set matchesQuery to true
                    else
                        -- Case insensitive search
                        set lowerName to my toLowerCase(todoName)
                        set lowerQuery to my toLowerCase(searchQuery)
                        if lowerName contains lowerQuery then
                            set matchesQuery to true
                        end if
                    end if

                    if not matchesQuery then
                        -- Skip this todo
                    else
                        -- Check URL filter
                        set matchesUrlFilter to true
                        if hasUrlFilter is "true" then
                            if todoName does not contain "http://" and todoName does not contain "https://" then
                                set matchesUrlFilter to false
                            end if
                        end if

                        if matchesUrlFilter then
                            -- Check tag filter
                            set matchesTagFilter to true
                            set todoTags to ""
                            try
                                set todoTags to tag names of toDo
                                if todoTags is missing value then set todoTags to ""
                            on error
                                set todoTags to ""
                            end try

                            if tagFilter is not "" then
                                if todoTags does not contain tagFilter then
                                    set matchesTagFilter to false
                                end if
                            end if

                            if matchesTagFilter then
                                -- Get area name if exists
                                set todoArea to ""
                                if area of toDo is not missing value then
                                    set todoArea to name of area of toDo
                                end if

                                -- Build output line with list source
                                set output to output & todoId & "|" & todoName & "|" & todoArea & "|" & todoTags & "|" & listName & linefeed
                                set todoCount to todoCount + 1
                            end if
                        end if
                    end if

                on error errMsg
                    log "Error processing todo: " & errMsg
                end try
            end repeat
        end repeat

        return output
    end tell
end run

-- Helper function for case-insensitive comparison
on toLowerCase(theString)
    set lowercaseChars to "abcdefghijklmnopqrstuvwxyz"
    set uppercaseChars to "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    set resultString to ""

    repeat with i from 1 to length of theString
        set theChar to character i of theString
        set charOffset to offset of theChar in uppercaseChars
        if charOffset > 0 then
            set resultString to resultString & character charOffset of lowercaseChars
        else
            set resultString to resultString & theChar
        end if
    end repeat

    return resultString
end toLowerCase
