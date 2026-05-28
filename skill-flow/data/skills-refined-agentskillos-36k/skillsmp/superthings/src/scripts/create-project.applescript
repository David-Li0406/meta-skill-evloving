-- Create a new project in Things 3 (silent - does not activate app)
-- Arguments: title, notes, when, deadline, tags (comma-separated), areaId, area, completed, canceled
on run argv
    set projectTitle to ""
    set projectNotes to ""
    set projectWhen to ""
    set projectDeadline to ""
    set projectTags to ""
    set projectAreaId to ""
    set projectArea to ""
    set projectCompleted to false
    set projectCanceled to false

    -- Parse arguments
    if (count of argv) > 0 then set projectTitle to item 1 of argv
    if (count of argv) > 1 then set projectNotes to item 2 of argv
    if (count of argv) > 2 then set projectWhen to item 3 of argv
    if (count of argv) > 3 then set projectDeadline to item 4 of argv
    if (count of argv) > 4 then set projectTags to item 5 of argv
    if (count of argv) > 5 then set projectAreaId to item 6 of argv
    if (count of argv) > 6 then set projectArea to item 7 of argv
    if (count of argv) > 7 then
        if item 8 of argv is "true" then set projectCompleted to true
    end if
    if (count of argv) > 8 then
        if item 9 of argv is "true" then set projectCanceled to true
    end if

    tell application "Things3"
        -- Create the project
        set newProject to make new project with properties {name:projectTitle}

        -- Set notes
        if projectNotes is not "" then
            set notes of newProject to projectNotes
        end if

        -- Handle scheduling (when)
        if projectWhen is not "" then
            if projectWhen is "today" then
                set activation date of newProject to current date
            else if projectWhen is "tomorrow" then
                set activation date of newProject to (current date) + 1 * days
            else if projectWhen is "anytime" then
                -- Do nothing, this is default
            else if projectWhen is "someday" then
                move newProject to list "Someday"
            else
                -- Assume it's a date string
                try
                    set activation date of newProject to date projectWhen
                end try
            end if
        end if

        -- Handle deadline
        if projectDeadline is not "" then
            try
                set due date of newProject to date projectDeadline
            end try
        end if

        -- Handle tags
        if projectTags is not "" then
            set AppleScript's text item delimiters to ","
            set tagList to text items of projectTags
            set AppleScript's text item delimiters to ""
            set tag names of newProject to tagList
        end if

        -- Handle area assignment
        if projectAreaId is not "" then
            try
                move newProject to area id projectAreaId
            end try
        else if projectArea is not "" then
            try
                set targetArea to first area whose name is projectArea
                move newProject to targetArea
            end try
        end if

        -- Handle completion status
        if projectCompleted then
            set status of newProject to completed
        end if

        if projectCanceled then
            set status of newProject to canceled
        end if

        -- Return the ID of the created project
        return id of newProject
    end tell
end run
