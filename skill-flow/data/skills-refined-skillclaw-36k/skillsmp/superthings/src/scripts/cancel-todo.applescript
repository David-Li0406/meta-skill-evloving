-- Cancel a to-do by ID
-- Parameters: todoId
on run argv
    if (count of argv) < 1 then
        return "error:Missing todo ID parameter"
    end if

    set todoId to item 1 of argv

    tell application "Things3"
        try
            set toDo to to do id todoId
            set todoName to name of toDo
            set status of toDo to canceled
            return "canceled|" & todoId & "|" & todoName
        on error errMsg
            return "error:" & errMsg
        end try
    end tell
end run
