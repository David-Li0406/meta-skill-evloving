---
name: ruby-stdlib
description: This skill should be used when the user asks about "Ruby standard library", "stdlib", "FileUtils", "JSON", "CSV", "YAML", "Net::HTTP", "URI", "OpenStruct", "Struct", "Set", "Date", "Time", "Pathname", "StringIO", "Tempfile", "Logger", "OptionParser", or needs guidance on Ruby's built-in libraries.
version: 1.0.0
---

# Ruby Standard Library

Guide to Ruby's built-in standard library modules and classes.

## File Operations

### FileUtils

```ruby
require "fileutils"

# Copy files and directories
FileUtils.cp("source.txt", "dest.txt")
FileUtils.cp_r("source_dir", "dest_dir")

# Move/rename
FileUtils.mv("old.txt", "new.txt")

# Remove
FileUtils.rm("file.txt")
FileUtils.rm_rf("directory")  # Recursive, force

# Create directories
FileUtils.mkdir_p("path/to/nested/dir")

# Change permissions
FileUtils.chmod(0755, "script.sh")
FileUtils.chmod_R(0644, "directory")

# Touch (create/update timestamp)
FileUtils.touch("file.txt")
```

### Pathname

```ruby
require "pathname"

path = Pathname.new("/home/user/project/lib/file.rb")

path.dirname      # => Pathname("/home/user/project/lib")
path.basename     # => Pathname("file.rb")
path.extname      # => ".rb"
path.basename(".rb")  # => Pathname("file")

path.exist?       # => true/false
path.directory?   # => false
path.file?        # => true

path.read         # Read file contents
path.write("content")  # Write to file
path.readlines    # Array of lines

# Path manipulation
path.parent       # => Pathname("/home/user/project/lib")
path.join("sub", "file.txt")  # => Pathname(".../sub/file.txt")

path.relative_path_from(Pathname.new("/home/user"))
# => Pathname("project/lib/file.rb")

# Glob
Pathname.glob("**/*.rb").each do |file|
  puts file
end
```

### Tempfile and StringIO

```ruby
require "tempfile"
require "stringio"

# Tempfile - automatically cleaned up
Tempfile.create("prefix") do |file|
  file.write("data")
  file.rewind
  file.read  # => "data"
end  # File deleted after block

# Persist tempfile
tempfile = Tempfile.new(["report", ".csv"])
tempfile.path  # => "/tmp/report20231205-12345.csv"
tempfile.close
# tempfile.unlink when done

# StringIO - in-memory IO
io = StringIO.new
io.puts "line 1"
io.puts "line 2"
io.string  # => "line 1\nline 2\n"

io.rewind
io.readline  # => "line 1\n"

# Read from string
io = StringIO.new("existing content")
io.read  # => "existing content"
```

## Data Formats

### JSON

```ruby
require "json"

# Parse JSON
data = JSON.parse('{"name": "Alice", "age": 30}')
data["name"]  # => "Alice"

# Parse with symbol keys
data = JSON.parse('{"name": "Alice"}', symbolize_names: true)
data[:name]  # => "Alice"

# Generate JSON
{ name: "Alice", scores: [95, 87, 92] }.to_json
# => '{"name":"Alice","scores":[95,87,92]}'

# Pretty print
JSON.pretty_generate({ name: "Alice", nested: { key: "value" } })

# Stream parsing for large files
File.open("large.json") do |file|
  JSON.parse(file)
end
```

### CSV

```ruby
require "csv"

# Read CSV
CSV.foreach("data.csv", headers: true) do |row|
  puts row["name"]
  puts row["email"]
end

# Parse string
data = CSV.parse("name,age\nAlice,30\nBob,25", headers: true)
data.each do |row|
  puts "#{row['name']} is #{row['age']}"
end

# Read all at once
rows = CSV.read("data.csv", headers: true)

# Write CSV
CSV.open("output.csv", "w") do |csv|
  csv << ["name", "email"]
  csv << ["Alice", "alice@example.com"]
  csv << ["Bob", "bob@example.com"]
end

# Generate CSV string
csv_string = CSV.generate do |csv|
  csv << ["header1", "header2"]
  csv << ["value1", "value2"]
end

# With options
CSV.foreach("data.csv",
  headers: true,
  header_converters: :symbol,
  converters: :numeric
) do |row|
  row[:age]  # Numeric, symbol key
end
```

### YAML

```ruby
require "yaml"

# Parse YAML
config = YAML.load_file("config.yml")

# Parse string
data = YAML.safe_load(<<~YAML)
  database:
    host: localhost
    port: 5432
  features:
    - auth
    - api
YAML

# Generate YAML
{ name: "Alice", tags: %w[ruby rails] }.to_yaml

# Safe loading (recommended)
YAML.safe_load(yaml_string, permitted_classes: [Date, Time])

# With aliases
YAML.safe_load(yaml_string, aliases: true)
```

## Networking

### Net::HTTP

```ruby
require "net/http"
require "uri"
require "json"

# Simple GET
uri = URI("https://api.example.com/users")
response = Net::HTTP.get_response(uri)
response.body

# GET with headers
uri = URI("https://api.example.com/users")
request = Net::HTTP::Get.new(uri)
request["Authorization"] = "Bearer token"
request["Accept"] = "application/json"

response = Net::HTTP.start(uri.hostname, uri.port, use_ssl: true) do |http|
  http.request(request)
end

# POST with JSON body
uri = URI("https://api.example.com/users")
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true

request = Net::HTTP::Post.new(uri.path)
request["Content-Type"] = "application/json"
request.body = { name: "Alice", email: "alice@example.com" }.to_json

response = http.request(request)

case response
when Net::HTTPSuccess
  JSON.parse(response.body)
when Net::HTTPRedirection
  # Handle redirect
when Net::HTTPClientError
  raise "Client error: #{response.code}"
when Net::HTTPServerError
  raise "Server error: #{response.code}"
end

# With timeout
http = Net::HTTP.new(uri.host, uri.port)
http.open_timeout = 5
http.read_timeout = 10
```

### URI

```ruby
require "uri"

uri = URI("https://user:pass@example.com:8080/path?query=value#fragment")

uri.scheme    # => "https"
uri.userinfo  # => "user:pass"
uri.host      # => "example.com"
uri.port      # => 8080
uri.path      # => "/path"
uri.query     # => "query=value"
uri.fragment  # => "fragment"

# Build URI
uri = URI::HTTPS.build(
  host: "api.example.com",
  path: "/v1/users",
  query: URI.encode_www_form(page: 1, limit: 10)
)
# => "https://api.example.com/v1/users?page=1&limit=10"

# Parse query string
URI.decode_www_form("name=Alice&age=30")
# => [["name", "Alice"], ["age", "30"]]

URI.decode_www_form("name=Alice&age=30").to_h
# => {"name"=>"Alice", "age"=>"30"}
```

## Data Structures

### Struct

```ruby
# Define a simple class
Person = Struct.new(:name, :age, keyword_init: true) do
  def adult?
    age >= 18
  end
end

person = Person.new(name: "Alice", age: 30)
person.name   # => "Alice"
person.adult? # => true
person.to_h   # => {name: "Alice", age: 30}

# With positional args
Point = Struct.new(:x, :y)
point = Point.new(10, 20)
```

### OpenStruct

```ruby
require "ostruct"

# Dynamic attributes
person = OpenStruct.new(name: "Alice", age: 30)
person.name     # => "Alice"
person.email = "alice@example.com"  # Add new attribute
person.email    # => "alice@example.com"

person.to_h     # => {name: "Alice", age: 30, email: "..."}

# From hash
data = { host: "localhost", port: 3000 }
config = OpenStruct.new(data)
config.host  # => "localhost"
```

### Set

```ruby
require "set"

set = Set.new([1, 2, 3])
set.add(4)
set.add(2)     # No duplicate
set.to_a       # => [1, 2, 3, 4]

set.include?(2)  # => true
set.member?(5)   # => false

# Set operations
a = Set[1, 2, 3]
b = Set[2, 3, 4]

a | b  # Union: Set[1, 2, 3, 4]
a & b  # Intersection: Set[2, 3]
a - b  # Difference: Set[1]
a ^ b  # Symmetric difference: Set[1, 4]

a.subset?(b)    # => false
a.superset?(b)  # => false

# SortedSet (requires 'sorted_set' gem in Ruby 3+)
```

## Date and Time

### Date

```ruby
require "date"

today = Date.today
date = Date.new(2024, 12, 25)
date = Date.parse("2024-12-25")
date = Date.strptime("25/12/2024", "%d/%m/%Y")

date.year   # => 2024
date.month  # => 12
date.day    # => 25
date.wday   # => 3 (Wednesday)
date.monday? # => false

date + 7          # 7 days later
date >> 1         # 1 month later
date << 1         # 1 month earlier
date.next_month
date.prev_year

date.strftime("%Y-%m-%d")  # => "2024-12-25"
date.strftime("%B %d, %Y") # => "December 25, 2024"

# Ranges
(Date.today..Date.today + 7).each { |d| puts d }
```

### Time

```ruby
now = Time.now
utc = Time.now.utc
time = Time.new(2024, 12, 25, 10, 30, 0)
time = Time.parse("2024-12-25 10:30:00")  # requires 'time'

time.hour    # => 10
time.min     # => 30
time.sec     # => 0
time.zone    # => "EST" or similar
time.utc?    # => false

time + 3600       # 1 hour later
time - 86400      # 1 day earlier

time.to_i         # Unix timestamp
Time.at(1703505000)  # From timestamp

time.strftime("%Y-%m-%d %H:%M:%S")
time.iso8601      # => "2024-12-25T10:30:00-05:00"
```

## Logging

### Logger

```ruby
require "logger"

# Basic usage
logger = Logger.new($stdout)
logger = Logger.new("application.log")
logger = Logger.new("app.log", "daily")  # Daily rotation

logger.level = Logger::INFO

logger.debug("Debug message")
logger.info("Info message")
logger.warn("Warning message")
logger.error("Error message")
logger.fatal("Fatal message")

# With block (only evaluated if level matches)
logger.debug { "Expensive debug: #{expensive_computation}" }

# Custom formatter
logger.formatter = proc do |severity, datetime, progname, msg|
  "[#{datetime.strftime('%Y-%m-%d %H:%M:%S')}] #{severity}: #{msg}\n"
end

# Tagged logging
logger.info("Processing") { "order_id=123" }
```

## CLI Parsing

### OptionParser

```ruby
require "optparse"

options = { verbose: false, output: "result.txt" }

OptionParser.new do |opts|
  opts.banner = "Usage: script.rb [options]"

  opts.on("-v", "--verbose", "Enable verbose output") do
    options[:verbose] = true
  end

  opts.on("-o", "--output FILE", "Output file") do |file|
    options[:output] = file
  end

  opts.on("-n", "--count NUM", Integer, "Number of items") do |n|
    options[:count] = n
  end

  opts.on("-t", "--type TYPE", %w[json xml csv], "Output type") do |type|
    options[:type] = type
  end

  opts.on("-h", "--help", "Show help") do
    puts opts
    exit
  end
end.parse!

# Remaining args in ARGV
files = ARGV
```
