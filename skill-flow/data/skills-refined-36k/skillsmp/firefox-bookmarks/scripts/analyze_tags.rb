#!/usr/bin/env ruby

require 'sqlite3'
require 'fileutils'

class FirefoxTagAnalyzer
  def initialize
    @profile_path = find_firefox_profile
    @places_db = File.join(@profile_path, 'places.sqlite')
  end

  def analyze_tags
    unless File.exist?(@places_db)
      puts "Error: Firefox places.sqlite not found at #{@places_db}"
      return {}
    end

    # Create a temporary copy to avoid locking issues
    temp_db = "/tmp/places_copy_#{Time.now.to_i}.sqlite"
    FileUtils.cp(@places_db, temp_db)

    begin
      db = SQLite3::Database.new(temp_db)
      db.results_as_hash = true

      # Query to get all tags and their usage count
      # Tags are stored as folders under parent ID 4 (the 'tags' folder)
      # Tagged bookmarks are children of those tag folders
      query = <<~SQL
        SELECT
          tag_folder.title as tag,
          COUNT(*) as count,
          GROUP_CONCAT(p.title, ' | ') as bookmarks
        FROM moz_bookmarks tag_folder
        JOIN moz_bookmarks tagged_item ON tagged_item.parent = tag_folder.id
        JOIN moz_places p ON tagged_item.fk = p.id
        WHERE tag_folder.parent = 4
          AND tag_folder.title IS NOT NULL
          AND tag_folder.fk IS NULL
        GROUP BY tag_folder.title
        ORDER BY count DESC
      SQL

      tags = db.execute(query)
      db.close

      tags
    rescue SQLite3::Exception => e
      puts "Database error: #{e.message}"
      puts "Note: Your Firefox database might not have tags, or the schema might be different."
      []
    ensure
      File.delete(temp_db) if File.exist?(temp_db)
    end
  end

  def display_tag_stats(tags)
    if tags.empty?
      puts "\nNo tags found in your Firefox bookmarks."
      puts "\nNote: Firefox tags are stored in a specific way. If you have tags,"
      puts "they should appear here. If not, you may not be using tags in Firefox."
      return
    end

    puts "\n" + "=" * 80
    puts "FIREFOX BOOKMARK TAGS ANALYSIS"
    puts "=" * 80
    puts "\nTotal unique tags: #{tags.length}"
    puts "\n" + "-" * 80

    tags.each_with_index do |tag, index|
      puts "\n#{index + 1}. #{tag['tag']}"
      puts "   Used #{tag['count']} time#{'s' if tag['count'] > 1}"

      # Show sample bookmarks (first 3)
      if tag['bookmarks']
        bookmarks = tag['bookmarks'].split(' | ').first(3)
        puts "   Sample bookmarks:"
        bookmarks.each do |bm|
          puts "     - #{bm[0..70]}#{'...' if bm.length > 70}"
        end
      end
      puts "   " + "-" * 76
    end

    puts "\n" + "=" * 80
  end

  private

  def find_firefox_profile
    case RUBY_PLATFORM
    when /darwin/
      base_path = File.expand_path("~/Library/Application Support/Firefox/Profiles")
    when /linux/
      base_path = File.expand_path("~/.mozilla/firefox")
    when /win32|mingw/
      base_path = File.expand_path("~/AppData/Roaming/Mozilla/Firefox/Profiles")
    else
      raise "Unsupported platform: #{RUBY_PLATFORM}"
    end

    unless Dir.exist?(base_path)
      raise "Firefox profiles directory not found: #{base_path}"
    end

    # Find the default profile
    profiles = Dir.glob(File.join(base_path, "*default*"))

    if profiles.empty?
      profiles = Dir.glob(File.join(base_path, "*"))
      profiles = profiles.select { |p| File.directory?(p) }
    end

    if profiles.empty?
      raise "No Firefox profile found in #{base_path}"
    end

    profiles.max_by { |profile| File.mtime(profile) }
  end
end

# Main execution
if __FILE__ == $0
  begin
    analyzer = FirefoxTagAnalyzer.new

    puts "Analyzing Firefox bookmark tags..."
    tags = analyzer.analyze_tags
    analyzer.display_tag_stats(tags)

  rescue => e
    puts "Error: #{e.message}"
    exit 1
  end
end
