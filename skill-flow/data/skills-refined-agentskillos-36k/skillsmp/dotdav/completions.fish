# dotdav completions

function __dotdav_profiles
    dotdav profile | string replace "Current profile: " ""
    # TODO: Parse config cleanly
end

function __dotdav_files
    # Parse mappings.yaml for keys
    # Simple grep/sed for now as a fallback
    cat mappings.yaml | grep "^    " | sed "s/    \(.*\):/\1/"
end

# Remove global -f to allow default file completion where needed
# complete -c dotdav -f

# init
complete -c dotdav -n "__fish_use_subcommand" -f -a init -d "Initialize repository"
complete -c dotdav -n "__fish_seen_subcommand_from init" -l remote -d "Rclone remote name"
complete -c dotdav -n "__fish_seen_subcommand_from init" -l path -d "Path on remote"

# add (NO -f here, so default file completion works)
complete -c dotdav -n "__fish_use_subcommand" -f -a add -d "Add file"
complete -c dotdav -n "__fish_seen_subcommand_from add" -l profile -d "Specific profile"
# Implicit file completion enabled

# remove
complete -c dotdav -n "__fish_use_subcommand" -f -a remove -d "Remove file from management"
complete -c dotdav -n "__fish_seen_subcommand_from remove" -l profile -d "Specific profile"
# Implicit file completion enabled (removed explicit source to allow path completion)

# profile
complete -c dotdav -n "__fish_use_subcommand" -f -a profile -d "Switch profile"
complete -c dotdav -n "__fish_seen_subcommand_from profile" -a "(echo default; echo desktop; echo laptop)"

# deploy
complete -c dotdav -n "__fish_use_subcommand" -f -a deploy -d "Deploy symlinks"
complete -c dotdav -n "__fish_seen_subcommand_from deploy" -l force

# sync
complete -c dotdav -n "__fish_use_subcommand" -f -a sync -d "Manual sync"
complete -c dotdav -n "__fish_seen_subcommand_from sync" -a "push pull"

# autosync
complete -c dotdav -n "__fish_use_subcommand" -f -a autosync -d "Run auto-sync daemon"

# service
complete -c dotdav -n "__fish_use_subcommand" -f -a service -d "Manage systemd service"
complete -c dotdav -n "__fish_seen_subcommand_from service" -a "install uninstall"
