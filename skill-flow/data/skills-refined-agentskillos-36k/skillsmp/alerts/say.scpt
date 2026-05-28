-- Text-to-speech alert
-- Usage: osascript say.scpt "Message to speak"

on run argv
    set theMessage to item 1 of argv
    say theMessage
end run
