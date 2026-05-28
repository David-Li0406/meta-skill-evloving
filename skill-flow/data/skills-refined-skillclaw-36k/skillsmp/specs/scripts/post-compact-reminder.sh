#!/bin/bash
# Reminder hook for specs workflow - triggered after context compaction
# Installed by: /specs setup
# Edit specs-reminder.txt to change the message, or re-run /specs setup

cat "$(dirname "$0")/specs-reminder.txt"
