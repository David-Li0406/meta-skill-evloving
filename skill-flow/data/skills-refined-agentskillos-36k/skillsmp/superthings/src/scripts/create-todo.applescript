-- Create a new todo in Things 3 (silent - does not activate app)
-- Arguments: title, notes, when, deadline, tags (comma-separated), list, listId, heading, completed, canceled, checklistItems (newline-separated)
on run argv
    set todoTitle to ""
    set todoNotes to ""
    set todoWhen to ""
    set todoDeadline to ""
    set todoTags to ""
    set todoList to ""
    set todoListId to ""
    set todoHeading to ""
    set todoCompleted to false
    set todoCanceled to false
    set todoChecklistItems to ""

    -- Parse arguments
    if (count of argv) > 0 then set todoTitle to item 1 of argv
    if (count of argv) > 1 then set todoNotes to item 2 of argv
    if (count of argv) > 2 then set todoWhen to item 3 of argv
    if (count of argv) > 3 then set todoDeadline to item 4 of argv
    if (count of argv) > 4 then set todoTags to item 5 of argv
    if (count of argv) > 5 then set todoList to item 6 of argv
    if (count of argv) > 6 then set todoListId to item 7 of argv
    if (count of argv) > 7 then set todoHeading to item 8 of argv
    if (count of argv) > 8 then
        if item 9 of argv is "true" then set todoCompleted to true
    end if
    if (count of argv) > 9 then
        if item 10 of argv is "true" then set todoCanceled to true
    end if
    if (count of argv) > 10 then set todoChecklistItems to item 11 of argv

    tell application "Things3"
        -- Build properties record
        set todoProps to {name:todoTitle}

        if todoNotes is not "" then
            set notes of todoProps to todoNotes
        end if

        -- Create the todo
        set newTodo to make new to do with properties todoProps

        -- Set additional properties after creation
        if todoNotes is not "" then
            set notes of newTodo to todoNotes
        end if

        -- Handle scheduling (when)
        if todoWhen is not "" then
            if todoWhen is "today" then
                set activation date of newTodo to current date
            else if todoWhen is "tomorrow" then
                set activation date of newTodo to (current date) + 1 * days
            else if todoWhen is "evening" then
                set activation date of newTodo to current date
                -- Things handles evening internally
            else if todoWhen is "anytime" then
                -- Do nothing, this is default
            else if todoWhen is "someday" then
                move newTodo to list "Someday"
            else
                -- Assume it's a date string (YYYY-MM-DD)
                try
                    set activation date of newTodo to date todoWhen
                end try
            end if
        end if

        -- Handle deadline
        if todoDeadline is not "" then
            try
                set due date of newTodo to date todoDeadline
            end try
        end if

        -- Handle tags
        if todoTags is not "" then
            set AppleScript's text item delimiters to ","
            set tagList to text items of todoTags
            set AppleScript's text item delimiters to ""
            set tag names of newTodo to tagList
        end if

        -- Handle list assignment (by name or ID)
        if todoListId is not "" then
            try
                move newTodo to project id todoListId
            on error
                try
                    move newTodo to area id todoListId
                end try
            end try
        else if todoList is not "" then
            if todoList is "inbox" or todoList is "Inbox" then
                move newTodo to list "Inbox"
            else if todoList is "today" or todoList is "Today" then
                set activation date of newTodo to current date
            else
                -- Try to find as project first, then area
                try
                    set targetProject to first project whose name is todoList
                    move newTodo to targetProject
                on error
                    try
                        set targetArea to first area whose name is todoList
                        move newTodo to targetArea
                    end try
                end try
            end if
        end if

        -- Handle completion status
        if todoCompleted then
            set status of newTodo to completed
        end if

        if todoCanceled then
            set status of newTodo to canceled
        end if

        -- Return the ID of the created todo
        return id of newTodo
    end tell
end run
