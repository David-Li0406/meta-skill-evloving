-- Modal dialog (blocks until dismissed)
-- Usage: osascript dialog.scpt "Title" "Message" [SoundName]

on run argv
    set theTitle to item 1 of argv
    set theMessage to item 2 of argv

    if (count of argv) > 2 then
        set theSound to item 3 of argv
        display dialog theMessage with title theTitle buttons {"OK"} default button "OK" with icon note giving up after 300
        do shell script "afplay /System/Library/Sounds/" & theSound & ".aiff &"
    else
        display dialog theMessage with title theTitle buttons {"OK"} default button "OK" with icon note giving up after 300
    end if
end run
