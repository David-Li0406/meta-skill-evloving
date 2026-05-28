#!/usr/bin/env ruby

require 'sqlite3'
require 'fileutils'

# Find Firefox profile
base_path = File.expand_path("~/Library/Application Support/Firefox/Profiles")
profiles = Dir.glob(File.join(base_path, "*default*"))
profiles = Dir.glob(File.join(base_path, "*")).select { |p| File.directory?(p) } if profiles.empty?
profile = profiles.max_by { |p| File.mtime(p) }
places_db = File.join(profile, 'places.sqlite')

# Create temporary copy
temp_db = "/tmp/places_explore_#{Time.now.to_i}.sqlite"
FileUtils.cp(places_db, temp_db)

begin
  db = SQLite3::Database.new(temp_db)

  puts "=" * 80
  puts "DATABASE SCHEMA"
  puts "=" * 80

  # Get all tables
  tables = db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
  puts "\nTables:"
  tables.each { |t| puts "  - #{t[0]}" }

  # Show moz_bookmarks structure
  puts "\n" + "=" * 80
  puts "moz_bookmarks table structure:"
  puts "=" * 80
  schema = db.execute("PRAGMA table_info(moz_bookmarks)")
  schema.each do |col|
    puts "  #{col[1]} (#{col[2]})"
  end

  # Sample some bookmarks
  puts "\n" + "=" * 80
  puts "Sample moz_bookmarks entries (first 10):"
  puts "=" * 80
  sample = db.execute("SELECT id, type, parent, title FROM moz_bookmarks LIMIT 10")
  sample.each do |row|
    puts "  ID: #{row[0]}, Type: #{row[1]}, Parent: #{row[2]}, Title: #{row[3]}"
  end

  # Check for Tags folder
  puts "\n" + "=" * 80
  puts "Looking for 'Tags' folder:"
  puts "=" * 80
  tags_folder = db.execute("SELECT id, parent, title FROM moz_bookmarks WHERE title = 'Tags'")
  if tags_folder.empty?
    puts "  No 'Tags' folder found"
  else
    tags_folder.each do |row|
      puts "  ID: #{row[0]}, Parent: #{row[1]}, Title: #{row[2]}"
    end
  end

  # Show all special folders
  puts "\n" + "=" * 80
  puts "Special bookmark folders:"
  puts "=" * 80
  special = db.execute("SELECT id, parent, title FROM moz_bookmarks WHERE parent = 1 OR id <= 10")
  special.each do |row|
    puts "  ID: #{row[0]}, Parent: #{row[1]}, Title: #{row[2]}"
  end

  # Check moz_places structure
  puts "\n" + "=" * 80
  puts "moz_places table structure:"
  puts "=" * 80
  schema = db.execute("PRAGMA table_info(moz_places)")
  schema.each do |col|
    puts "  #{col[1]} (#{col[2]})"
  end

  db.close
ensure
  File.delete(temp_db) if File.exist?(temp_db)
end
