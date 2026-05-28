#!/usr/bin/osascript
-- Convert DOCX to PDF using Microsoft Word
-- Usage: osascript convert-docx.applescript "/path/to/input.docx" "/path/to/output.pdf"

on run argv
    if (count of argv) < 2 then
        log "Usage: convert-docx.applescript <input.docx> <output.pdf>"
        return "Error: Missing arguments"
    end if

    set inputFile to item 1 of argv
    set outputFile to item 2 of argv

    -- Convert to POSIX paths for Word
    set inputPosix to POSIX file inputFile
    set outputPosix to POSIX file outputFile

    tell application "Microsoft Word"
        -- Don't bring Word to front
        set visible of window 1 to false

        -- Open the document
        open inputPosix

        -- Wait for document to load
        delay 2

        -- Get reference to active document
        set theDoc to active document

        -- Export as PDF
        -- file format: format PDF = 17
        save as theDoc file name outputPosix file format format PDF

        -- Close without saving (we saved as PDF)
        close theDoc saving no
    end tell

    return "Converted: " & inputFile & " -> " & outputFile
end run
