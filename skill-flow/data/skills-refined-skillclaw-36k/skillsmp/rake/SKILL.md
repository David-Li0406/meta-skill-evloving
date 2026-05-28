---
name: rake
description: This skill should be used when the user asks about "Rake", "rake tasks", "Rakefile", "task dependencies", "rake namespace", "rake desc", "rake file tasks", "invoke", "execute", "task arguments", or needs guidance on creating and managing Rake tasks.
version: 1.0.0
---

# Rake Task System

Guide to creating and managing Rake tasks for Ruby projects.

## Basic Tasks

### Defining Tasks

```ruby
# Rakefile or lib/tasks/*.rake

desc "Greet the user"
task :greet do
  puts "Hello, World!"
end

# Run with: rake greet
```

### Task with Description

```ruby
desc "Generate the weekly report"
task :weekly_report do
  Report.generate(:weekly)
end

# Shows in: rake -T
```

### Tasks Without Description

```ruby
# Not shown in rake -T, but still runnable
task :internal_cleanup do
  Cleaner.run
end
```

## Task Dependencies

### Simple Dependencies

```ruby
task :build => :compile do
  puts "Building..."
end

task :compile do
  puts "Compiling..."
end

# rake build -> runs compile, then build
```

### Multiple Dependencies

```ruby
task :deploy => [:test, :build, :upload] do
  puts "Deployed!"
end

# Dependencies run in order: test, build, upload, deploy
```

### Default Task

```ruby
task :default => [:test, :lint]

# rake (with no args) runs test and lint
```

## Namespaces

### Organizing Tasks

```ruby
namespace :db do
  desc "Create the database"
  task :create do
    Database.create
  end

  desc "Run migrations"
  task :migrate do
    Database.migrate
  end

  desc "Seed the database"
  task :seed => :migrate do
    Database.seed
  end
end

# Run with: rake db:create, rake db:migrate, etc.
```

### Nested Namespaces

```ruby
namespace :db do
  namespace :schema do
    desc "Dump the schema"
    task :dump do
      Schema.dump
    end

    desc "Load the schema"
    task :load do
      Schema.load
    end
  end
end

# Run with: rake db:schema:dump
```

## Task Arguments

### Simple Arguments

```ruby
desc "Greet a person"
task :greet, [:name] do |t, args|
  puts "Hello, #{args[:name]}!"
end

# Run with: rake "greet[Alice]"
```

### Multiple Arguments

```ruby
desc "Create a user"
task :create_user, [:name, :email] do |t, args|
  User.create(
    name: args[:name],
    email: args[:email]
  )
end

# Run with: rake "create_user[Alice,alice@example.com]"
```

### Arguments with Defaults

```ruby
task :greet, [:name] do |t, args|
  args.with_defaults(name: "World")
  puts "Hello, #{args[:name]}!"
end
```

### Arguments with Dependencies

```ruby
task :deploy, [:env] => :build do |t, args|
  args.with_defaults(env: "staging")
  Deploy.to(args[:env])
end

# Run with: rake "deploy[production]"
```

## Environment and Configuration

### Using Environment Variables

```ruby
task :deploy do
  env = ENV.fetch("DEPLOY_ENV", "staging")
  Deploy.to(env)
end

# Run with: DEPLOY_ENV=production rake deploy
```

### Loading Application Environment

```ruby
# Load application environment (example for framework integration)
task :my_task => :environment do
  # Your application code here
  process_items
end

# Note: The :environment task must be defined in your Rakefile
# This pattern is common in frameworks like Rails
```

## File Tasks

### Building Files

```ruby
file "output.txt" => "input.txt" do |t|
  # t.name is the target file
  # t.prerequisites are the source files
  File.write(t.name, File.read(t.prerequisites.first).upcase)
end
```

### Directory Tasks

```ruby
directory "tmp/cache"

task :cache_setup => "tmp/cache" do
  puts "Cache directory ready"
end
```

### File Lists

```ruby
# Create a file list with glob patterns
SRC = FileList["src/**/*.rb"]
TESTS = FileList["test/**/*_test.rb"]

task :test do
  TESTS.each { |f| ruby f }
end
```

### Rules

```ruby
# Pattern-based file generation
rule ".html" => ".md" do |t|
  sh "pandoc #{t.source} -o #{t.name}"
end

# Any .html file will be built from corresponding .md
```

## Invoking Tasks

### Invoke vs Execute

```ruby
task :setup do
  # Invoke only runs the task once (with dependencies)
  Rake::Task["db:create"].invoke
  Rake::Task["db:migrate"].invoke

  # Execute runs the task again (skips dependencies)
  Rake::Task["db:seed"].execute
end
```

### Re-enabling Tasks

```ruby
task :multi_run do
  3.times do
    Rake::Task["process"].reenable
    Rake::Task["process"].invoke
  end
end
```

### Passing Arguments to Invoked Tasks

```ruby
task :deploy_all do
  %w[staging production].each do |env|
    Rake::Task["deploy"].reenable
    Rake::Task["deploy"].invoke(env)
  end
end
```

## Testing Rake Tasks

### With Minitest

```ruby
require "test_helper"
require "rake"

class MyTaskTest < Minitest::Test
  def setup
    Rake.application.load_rakefile
  end

  def test_greet_task
    output = capture_io do
      Rake::Task["greet"].invoke("Alice")
    end
    assert_match(/Hello, Alice/, output.first)
  ensure
    Rake::Task["greet"].reenable
  end
end
```

### With RSpec

```ruby
require "rails_helper"
require "rake"

RSpec.describe "greet task" do
  before do
    Rake.application.load_rakefile
  end

  after do
    Rake::Task["greet"].reenable
  end

  it "greets the user" do
    expect { Rake::Task["greet"].invoke("Alice") }
      .to output(/Hello, Alice/).to_stdout
  end
end
```

## Best Practices

### Task Organization

```ruby
# lib/tasks/database.rake - Database tasks
# lib/tasks/assets.rake - Asset tasks
# lib/tasks/reports.rake - Report generation
```

### Error Handling

```ruby
desc "Safe task with error handling"
task :safe_task do
  begin
    risky_operation
  rescue StandardError => e
    warn "Task failed: #{e.message}"
    exit 1
  end
end
```

### Verbose Output

```ruby
task :process do
  items.each do |item|
    puts "Processing #{item}..." if Rake.verbose
    process(item)
  end
end

# Run with: rake process --verbose
```

### Dry Run Support

```ruby
task :delete_old_files do
  old_files.each do |file|
    if Rake.application.options.dryrun
      puts "Would delete: #{file}"
    else
      FileUtils.rm(file)
    end
  end
end

# Test with: rake delete_old_files --dry-run
```

## Common Patterns

### Progress Reporting

```ruby
desc "Process all items"
task :process_all do
  items = Item.all
  total = items.count

  items.each_with_index do |item, i|
    print "\rProcessing #{i + 1}/#{total}..."
    process(item)
  end

  puts "\nDone!"
end
```

### Confirmation Prompt

```ruby
desc "Dangerous operation"
task :dangerous do
  print "Are you sure? (y/N) "
  abort "Cancelled" unless $stdin.gets.chomp.downcase == "y"

  perform_dangerous_operation
end
```

### Parallel Execution

```ruby
require "parallel"

task :parallel_process do
  items = Item.all
  Parallel.each(items, in_processes: 4) do |item|
    process(item)
  end
end
```
