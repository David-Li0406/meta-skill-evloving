-- Delete a project by ID (moves to Trash)
-- Parameters: projectId
on run argv
    if (count of argv) < 1 then
        return "error:Missing project ID parameter"
    end if

    set projectId to item 1 of argv

    tell application "Things3"
        try
            set proj to project id projectId
            set projName to name of proj
            delete proj
            return "deleted|" & projectId & "|" & projName
        on error errMsg
            return "error:" & errMsg
        end try
    end tell
end run
