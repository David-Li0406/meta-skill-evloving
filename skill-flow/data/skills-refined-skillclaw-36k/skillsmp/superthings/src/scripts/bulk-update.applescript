-- Bulk update multiple todos in Things 3
-- Arguments: idsString, when, deadline, tagsAdd, tagsRemove, listId, list
-- idsString is comma-separated list of todo IDs
-- Returns: success|count|failed:id1,id2... (pipe-separated)

on run argv
	set idsString to item 1 of argv
	set whenValue to item 2 of argv
	set deadlineValue to item 3 of argv
	set tagsAddValue to item 4 of argv
	set tagsRemoveValue to item 5 of argv
	set listIdValue to item 6 of argv
	set listValue to item 7 of argv

	-- Parse comma-separated IDs
	set AppleScript's text item delimiters to ","
	set todoIds to text items of idsString
	set AppleScript's text item delimiters to ""

	-- Parse tags to add/remove
	set tagsToAdd to {}
	if tagsAddValue is not "" then
		set AppleScript's text item delimiters to ","
		set tagsToAdd to text items of tagsAddValue
		set AppleScript's text item delimiters to ""
	end if

	set tagsToRemove to {}
	if tagsRemoveValue is not "" then
		set AppleScript's text item delimiters to ","
		set tagsToRemove to text items of tagsRemoveValue
		set AppleScript's text item delimiters to ""
	end if

	set successCount to 0
	set failedIds to {}

	tell application "Things3"
		-- Find target list/project if specified
		set targetList to missing value
		if listIdValue is not "" then
			try
				set targetList to project id listIdValue
			on error
				try
					set targetList to area id listIdValue
				end try
			end try
		else if listValue is not "" then
			try
				set targetList to project listValue
			on error
				try
					set targetList to area listValue
				end try
			end try
		end if

		-- Process each todo
		repeat with todoId in todoIds
			try
				set toDo to to do id todoId

				-- Set when/activation date
				if whenValue is not "" then
					if whenValue is "today" then
						set activation date of toDo to current date
					else if whenValue is "tomorrow" then
						set activation date of toDo to (current date) + (1 * days)
					else if whenValue is "evening" then
						set activation date of toDo to current date
						-- Note: Things doesn't have separate "evening" concept in AppleScript
					else if whenValue is "anytime" then
						set activation date of toDo to missing value
					else if whenValue is "someday" then
						-- Move to someday by clearing activation and setting status
						set activation date of toDo to missing value
					else
						-- Parse date string YYYY-MM-DD
						set theYear to text 1 thru 4 of whenValue as integer
						set theMonth to text 6 thru 7 of whenValue as integer
						set theDay to text 9 thru 10 of whenValue as integer
						set theDate to current date
						set year of theDate to theYear
						set month of theDate to theMonth
						set day of theDate to theDay
						set activation date of toDo to theDate
					end if
				end if

				-- Set deadline
				if deadlineValue is not "" then
					set theYear to text 1 thru 4 of deadlineValue as integer
					set theMonth to text 6 thru 7 of deadlineValue as integer
					set theDay to text 9 thru 10 of deadlineValue as integer
					set theDate to current date
					set year of theDate to theYear
					set month of theDate to theMonth
					set day of theDate to theDay
					set due date of toDo to theDate
				end if

				-- Add tags
				repeat with tagName in tagsToAdd
					try
						set theTag to tag tagName
						set tag names of toDo to (tag names of toDo) & tagName
					end try
				end repeat

				-- Remove tags
				if (count of tagsToRemove) > 0 then
					set currentTags to tag names of toDo
					set newTags to {}
					repeat with aTag in currentTags
						set shouldKeep to true
						repeat with removeTag in tagsToRemove
							if (aTag as text) is equal to (removeTag as text) then
								set shouldKeep to false
								exit repeat
							end if
						end repeat
						if shouldKeep then
							set end of newTags to aTag
						end if
					end repeat
					set tag names of toDo to newTags
				end if

				-- Move to new list/project
				if targetList is not missing value then
					move toDo to targetList
				end if

				set successCount to successCount + 1
			on error
				set end of failedIds to (todoId as text)
			end try
		end repeat
	end tell

	-- Build result string
	if (count of failedIds) is 0 then
		return "success|" & successCount
	else
		set AppleScript's text item delimiters to ","
		set failedString to failedIds as text
		set AppleScript's text item delimiters to ""
		return "success|" & successCount & "|failed:" & failedString
	end if
end run
