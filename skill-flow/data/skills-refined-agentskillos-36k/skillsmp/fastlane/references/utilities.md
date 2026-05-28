# Utilities Actions

## Notifications

### slack

Send messages to Slack.

```ruby
slack(
  message: "Build succeeded!",
  channel: "#builds",
  slack_url: ENV["SLACK_WEBHOOK_URL"],
  
  # Status
  success: true,
  default_payloads: [:git_branch, :git_author, :last_git_commit],
  
  # Attachments
  attachment_properties: {
    fields: [
      {
        title: "Version",
        value: "1.0.0",
        short: true
      },
      {
        title: "Build Number",
        value: "123",
        short: true
      }
    ]
  }
)
```

### notification

macOS notification.

```ruby
notification(
  title: "Build Complete",
  subtitle: "MyApp v1.0.0",
  message: "Build succeeded!",
  sound: "default"
)
```

### mailgun

Send email via Mailgun.

```ruby
mailgun(
  to: "team@example.com",
  from: "fastlane@example.com",
  subject: "Build Complete",
  message: "Build 123 has been uploaded.",
  api_key: ENV["MAILGUN_API_KEY"]
)
```

### twitter

Post to Twitter/X.

```ruby
twitter(
  access_token: ENV["TWITTER_ACCESS_TOKEN"],
  access_token_secret: ENV["TWITTER_ACCESS_TOKEN_SECRET"],
  consumer_key: ENV["TWITTER_CONSUMER_KEY"],
  consumer_secret: ENV["TWITTER_CONSUMER_SECRET"],
  message: "New version released! 🚀"
)
```

## Source Control

### git_commit

Commit files.

```ruby
git_commit(
  path: ["./Podfile.lock", "./fastlane/"],
  message: "Version bump",
  allow_nothing_to_commit: true
)
```

### git_add

Stage files.

```ruby
git_add(path: ".")
git_add(path: ["file1.txt", "file2.txt"])
git_add(path: "*.md")
```

### git_pull

Pull from remote.

```ruby
git_pull(rebase: true)
```

### push_to_git_remote

Push to remote.

```ruby
push_to_git_remote(
  remote: "origin",
  local_branch: "main",
  remote_branch: "main",
  force: false,
  tags: true
)
```

### add_git_tag

Create git tag.

```ruby
add_git_tag(
  tag: "v1.0.0",
  message: "Release version 1.0.0",
  sign: true
)

# Auto-generate tag from version
add_git_tag(
  grouping: "builds",
  build_number: "123"
)  # Creates builds/123
```

### push_git_tags

Push tags to remote.

```ruby
push_git_tags(
  remote: "origin",
  tag: "v1.0.0"
)
```

### ensure_git_status_clean

Fail if uncommitted changes exist.

```ruby
ensure_git_status_clean(
  show_uncommitted_changes: true,
  ignore_files: ["Pods/"]
)
```

### ensure_git_branch

Ensure on correct branch.

```ruby
ensure_git_branch(branch: "main")
ensure_git_branch(branch: "release/*")
```

### reset_git_repo

Reset repo to clean state.

```ruby
reset_git_repo(
  force: true,
  skip_clean: false,
  files: ["./build"]  # Only reset specific paths
)
```

### changelog_from_git_commits

Generate changelog from commits.

```ruby
changelog = changelog_from_git_commits(
  between: ["v1.0.0", "HEAD"],
  pretty: "- %s",
  merge_commit_filtering: "exclude_merges"
)
```

### last_git_commit

Get last commit info.

```ruby
commit = last_git_commit
puts commit[:message]
puts commit[:author]
puts commit[:commit_hash]
```

### git_branch

Get current branch name.

```ruby
branch = git_branch
puts "On branch: #{branch}"
```

### set_github_release

Create GitHub release.

```ruby
set_github_release(
  repository_name: "org/repo",
  api_token: ENV["GITHUB_TOKEN"],
  tag_name: "v1.0.0",
  name: "Release v1.0.0",
  description: changelog,
  is_prerelease: false,
  upload_assets: ["./build/MyApp.ipa"]
)
```

### create_pull_request

Create GitHub PR.

```ruby
create_pull_request(
  repo: "org/repo",
  api_token: ENV["GITHUB_TOKEN"],
  title: "Release v1.0.0",
  body: "Release notes here",
  head: "release/1.0.0",
  base: "main"
)
```

## Version Management

### increment_build_number

Increment build number in Xcode project.

```ruby
increment_build_number
increment_build_number(build_number: 123)
increment_build_number(
  xcodeproj: "MyApp.xcodeproj",
  build_number: latest_testflight_build_number + 1
)
```

### increment_version_number

Increment version number.

```ruby
increment_version_number  # Patch: 1.0.0 -> 1.0.1
increment_version_number(bump_type: "minor")  # 1.0.0 -> 1.1.0
increment_version_number(bump_type: "major")  # 1.0.0 -> 2.0.0
increment_version_number(version_number: "2.0.0")  # Explicit
```

### get_version_number / get_build_number

Read current version/build.

```ruby
version = get_version_number(xcodeproj: "MyApp.xcodeproj")
build = get_build_number(xcodeproj: "MyApp.xcodeproj")
```

### commit_version_bump

Commit version changes.

```ruby
commit_version_bump(
  message: "Version bump to #{version}",
  xcodeproj: "MyApp.xcodeproj"
)
```

## File Operations

### copy_artifacts

Copy build artifacts.

```ruby
copy_artifacts(
  artifacts: ["./build/*.ipa", "./build/*.dSYM.zip"],
  target_path: "./artifacts"
)
```

### zip

Create zip archive.

```ruby
zip(
  path: "./build/MyApp.dSYM",
  output_path: "./build/MyApp.dSYM.zip"
)
```

### backup_file / restore_file

Backup and restore files.

```ruby
backup_file(path: "MyApp/Info.plist")
# Make changes...
restore_file(path: "MyApp/Info.plist")
```

### download

Download file from URL.

```ruby
download(url: "https://example.com/file.zip")
```

## Miscellaneous

### sh

Run shell command.

```ruby
sh("echo 'Hello World'")
sh("./scripts/build.sh", log: false)

result = sh("git rev-parse HEAD", capture: true)
```

### prompt

Interactive prompt.

```ruby
answer = prompt(text: "Enter version number:")
yes = prompt(boolean: true, text: "Continue?")
```

### is_ci

Check if running on CI.

```ruby
if is_ci
  # CI-specific logic
end
```

### clean_build_artifacts

Remove build artifacts.

```ruby
clean_build_artifacts  # Removes .ipa, .app, .dSYM created by fastlane
```

### skip_docs

Skip README generation.

```ruby
skip_docs  # Don't generate fastlane/README.md
```

### rocket

Print rocket ASCII art (for fun! 🚀).

```ruby
rocket
```

## Environment & Debugging

### debug

Print lane context for debugging.

```ruby
debug
```

### puts / println / echo

Print messages.

```ruby
puts("Build complete!")
```

### environment_variable

Manage environment variables.

```ruby
ENV["MY_VAR"] = "value"
value = ENV["MY_VAR"]
```

### ensure_env_vars

Ensure required env vars are set.

```ruby
ensure_env_vars(
  env_vars: ["SLACK_URL", "GITHUB_TOKEN"]
)
```

## Lane Context

Access shared values between actions.

```ruby
lane :build do
  build_app(scheme: "MyApp")
  
  # Access build output path
  ipa_path = lane_context[SharedValues::IPA_OUTPUT_PATH]
  dsym_path = lane_context[SharedValues::DSYM_OUTPUT_PATH]
  
  upload_to_testflight(ipa: ipa_path)
end
```

**Common SharedValues:**
- `IPA_OUTPUT_PATH`: Built IPA path
- `DSYM_OUTPUT_PATH`: dSYM path
- `GRADLE_AAB_OUTPUT_PATH`: Android AAB path
- `GRADLE_APK_OUTPUT_PATH`: Android APK path
- `LANE_NAME`: Current lane name
- `PLATFORM_NAME`: Current platform
