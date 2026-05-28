export OBSIDIAN_VAULT="/Users/ansonlee/Library/Mobile Documents/iCloud~md~obsidian/Documents/notes-icloud"

# olog - Obsidian Log
# Uses Opencode Command to add a work log to the daily journal
# Injects the OBSIDIAN_VAULT environment variable
# Usage: olog "Task description"
olog() {
    echo "Logging work to $OBSIDIAN_VAULT"
    opencode run --command obsidian-log $OBSIDIAN_VAULT "$1"
}


# osummary - Obsidian Summary
# Uses Opencode Command to summarize the wins of the day
# Injects the OBSIDIAN_VAULT environment variable
osummary() {
    echo "Summarizing wins for $OBSIDIAN_VAULT"
    opencode run --command obsidian-summary $OBSIDIAN_VAULT
}
