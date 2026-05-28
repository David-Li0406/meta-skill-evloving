-- Update an existing todo in Things 3 (silent - does not activate app)
-- Arguments: id, title, notes, when, deadline, tags (comma-separated), list, listId, completed, canceled
on run argv
    set todoId to ""
    set newTitle to ""
    set newNotes to ""
    set newWhen to ""
    set newDeadline to ""
    set newTags to ""
    set newList to ""
    set newListId to ""
    set newCompleted to ""
    set newCanceled to ""

    -- Parse arguments (empty string means don't update)
    if (count of argv) > 0 then set todoId to item 1 of argv
    if (count of argv) > 1 then set newTitle to item 2 of argv
    if (count of argv) > 2 then set newNotes to item 3 of argv
    if (count of argv) > 3 then set newWhen to item 4 of argv
    if (count of argv) > 4 then set newDeadline to item 5 of argv
    if (count of argv) > 5 then set newTags to item 6 of argv
    if (count of argv) > 6 then set newList to item 7 of argv
    if (count of argv) > 7 then set newListId to item 8 of argv
    if (count of argv) > 8 then set newCompleted to item 9 of argv
    if (count of argv) > 9 then set newCanceled to item 10 of argv

    if todoId is "" then
        error "Todo ID is required"
    end if

    tell application "Things3"
        -- Find the todo by ID
        set targetTodo to to do id todoId

        -- Update title if provided
        if newTitle is not "" then
            set name of targetTodo to newTitle
        end if

        -- Update notes if provided (use special marker for clearing)
        if newNotes is not "" then
            if newNotes is "__CLEAR__" then
                set notes of targetTodo to ""
            else
                set notes of targetTodo to newNotes
            end if
        end if

        -- Handle scheduling (when)
        if newWhen is not "" then
            if newWhen is "today" then
                set activation date of targetTodo to current date
            else if newWhen is "tomorrow" then
                set activation date of targetTodo to (current date) + 1 * days
            else if newWhen is "anytime" then
                set activation date of targetTodo to missing value
            else if newWhen is "someday" then
                move targetTodo to list "Someday"
            else
                -- Assume it's a date string
                try
                    set activation date of targetTodo to date newWhen
                end try
            end if
        end if

        -- Handle deadline
        if newDeadline is not "" then
            if newDeadline is "__CLEAR__" then
                set due date of targetTodo to missing value
            else
                try
                    set due date of targetTodo to date newDeadline
                end try
            end if
        end if

        -- Handle tags
        if newTags is not "" then
            if newTags is "__CLEAR__" then
                set tag names of targetTodo to {}
            else
                set AppleScript's text item delimiters to ","
                set tagList to text items of newTags
                set AppleScript's text item delimiters to ""
                set tag names of targetTodo to tagList
            end if
        end if

        -- Handle list assignment (by ID) - use set property, not move command
        if newListId is not "" then
            try
                set project of targetTodo to project id newListId
            on error
                try
                    set area of targetTodo to area id newListId
                end try
            end try
        else if newList is not "" then
            if newList is "inbox" or newList is "Inbox" then
                -- To move to Inbox, detach from current project/area
                try
                    delete project of targetTodo
                end try
                try
                    delete area of targetTodo
                end try
            else
                try
                    set project of targetTodo to project newList
                on error
                    try
                        set area of targetTodo to area newList
                    end try
                end try
            end if
        end if

        -- Handle completion status
        if newCompleted is "true" then
            set status of targetTodo to completed
        else if newCompleted is "false" then
            set status of targetTodo to open
        end if

        -- Handle canceled status
        if newCanceled is "true" then
            set status of targetTodo to canceled
        else if newCanceled is "false" then
            set status of targetTodo to open
        end if

        return "success"
    end tell
end run
