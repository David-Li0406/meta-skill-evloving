-- Non-modal notification (banner)
-- Usage: osascript notify.scpt "Title" "Message"

on run argv
    set theTitle to item 1 of argv
    set theMessage to item 2 of argv

    display notification theMessage with title theTitle
end run
