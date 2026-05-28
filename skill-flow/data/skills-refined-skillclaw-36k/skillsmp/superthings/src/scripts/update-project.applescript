-- Update an existing project in Things 3 (silent - does not activate app)
-- Arguments: id, title, notes, when, deadline, tags (comma-separated), areaId, area, completed, canceled
on run argv
    set projectId to ""
    set newTitle to ""
    set newNotes to ""
    set newWhen to ""
    set newDeadline to ""
    set newTags to ""
    set newAreaId to ""
    set newArea to ""
    set newCompleted to ""
    set newCanceled to ""

    -- Parse arguments (empty string means don't update)
    if (count of argv) > 0 then set projectId to item 1 of argv
    if (count of argv) > 1 then set newTitle to item 2 of argv
    if (count of argv) > 2 then set newNotes to item 3 of argv
    if (count of argv) > 3 then set newWhen to item 4 of argv
    if (count of argv) > 4 then set newDeadline to item 5 of argv
    if (count of argv) > 5 then set newTags to item 6 of argv
    if (count of argv) > 6 then set newAreaId to item 7 of argv
    if (count of argv) > 7 then set newArea to item 8 of argv
    if (count of argv) > 8 then set newCompleted to item 9 of argv
    if (count of argv) > 9 then set newCanceled to item 10 of argv

    if projectId is "" then
        error "Project ID is required"
    end if

    tell application "Things3"
        -- Find the project by ID
        set targetProject to project id projectId

        -- Update title if provided
        if newTitle is not "" then
            set name of targetProject to newTitle
        end if

        -- Update notes if provided
        if newNotes is not "" then
            if newNotes is "__CLEAR__" then
                set notes of targetProject to ""
            else
                set notes of targetProject to newNotes
            end if
        end if

        -- Handle scheduling (when)
        if newWhen is not "" then
            if newWhen is "today" then
                set activation date of targetProject to current date
            else if newWhen is "tomorrow" then
                set activation date of targetProject to (current date) + 1 * days
            else if newWhen is "anytime" then
                set activation date of targetProject to missing value
            else if newWhen is "someday" then
                move targetProject to list "Someday"
            else
                try
                    set activation date of targetProject to date newWhen
                end try
            end if
        end if

        -- Handle deadline
        if newDeadline is not "" then
            if newDeadline is "__CLEAR__" then
                set due date of targetProject to missing value
            else
                try
                    set due date of targetProject to date newDeadline
                end try
            end if
        end if

        -- Handle tags
        if newTags is not "" then
            if newTags is "__CLEAR__" then
                set tag names of targetProject to {}
            else
                set AppleScript's text item delimiters to ","
                set tagList to text items of newTags
                set AppleScript's text item delimiters to ""
                set tag names of targetProject to tagList
            end if
        end if

        -- Handle area assignment
        if newAreaId is not "" then
            try
                move targetProject to area id newAreaId
            end try
        else if newArea is not "" then
            try
                set targetArea to first area whose name is newArea
                move targetProject to targetArea
            end try
        end if

        -- Handle completion status
        if newCompleted is "true" then
            set status of targetProject to completed
        else if newCompleted is "false" then
            set status of targetProject to open
        end if

        -- Handle canceled status
        if newCanceled is "true" then
            set status of targetProject to canceled
        else if newCanceled is "false" then
            set status of targetProject to open
        end if

        return "success"
    end tell
end run
