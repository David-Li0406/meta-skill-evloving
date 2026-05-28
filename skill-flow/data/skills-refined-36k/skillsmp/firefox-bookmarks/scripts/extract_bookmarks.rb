#!/usr/bin/env ruby

require 'sqlite3'
require 'fileutils'

class FirefoxBookmarkExtractor
  def initialize
    @profile_path = find_firefox_profile
    @places_db = File.join(@profile_path, 'places.sqlite')
  end

  def extract_recent_bookmarks(limit = 50)
    unless File.exist?(@places_db)
      puts "Error: Firefox places.sqlite not found at #{@places_db}"
      return []
    end

    # Create a temporary copy to avoid locking issues
    temp_db = "/tmp/places_copy_#{Time.now.to_i}.sqlite"
    FileUtils.cp(@places_db, temp_db)

    begin
      db = SQLite3::Database.new(temp_db)
      db.results_as_hash = true

      query = <<~SQL
        SELECT
          p.url,
          p.title,
          datetime(b.dateAdded/1000000, 'unixepoch', 'localtime') as date_added,
          datetime(p.last_visit_date/1000000, 'unixepoch', 'localtime') as last_visited
        FROM moz_bookmarks b
        JOIN moz_places p ON b.fk = p.id
        WHERE b.type = 1
          AND p.url IS NOT NULL
          AND p.url != ''
          AND p.url NOT LIKE 'place:%'
          AND b.parent NOT IN (SELECT id FROM moz_bookmarks WHERE parent = 4)
        ORDER BY b.dateAdded DESC
        LIMIT ?
      SQL

      bookmarks = db.execute(query, [limit])
      db.close
      
      bookmarks
    rescue SQLite3::Exception => e
      puts "Database error: #{e.message}"
      []
    ensure
      File.delete(temp_db) if File.exist?(temp_db)
    end
  end

  def display_bookmarks(bookmarks)
    if bookmarks.empty?
      puts "No bookmarks found."
      return
    end

    puts "=" * 80
    puts "RECENT FIREFOX BOOKMARKS (#{bookmarks.length} found)"
    puts "=" * 80

    bookmarks.each_with_index do |bookmark, index|
      puts "\n#{index + 1}. #{bookmark['title'] || 'Untitled'}"
      puts "   URL: #{bookmark['url']}"
      puts "   Added: #{bookmark['date_added']}"
      puts "   Last Visited: #{bookmark['last_visited'] || 'Never'}"
      puts "   " + "-" * 76
    end
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

    # Find the default profile (usually ends with .default or .default-release)
    profiles = Dir.glob(File.join(base_path, "*default*"))
    
    if profiles.empty?
      # Fallback: use the first profile found
      profiles = Dir.glob(File.join(base_path, "*"))
      profiles = profiles.select { |p| File.directory?(p) }
    end

    if profiles.empty?
      raise "No Firefox profile found in #{base_path}"
    end

    # Use the most recently modified profile
    profiles.max_by { |profile| File.mtime(profile) }
  end
end

# Main execution
if __FILE__ == $0
  begin
    extractor = FirefoxBookmarkExtractor.new
    
    # Get number of bookmarks to display (default 50)
    limit = ARGV[0] ? ARGV[0].to_i : 50
    limit = 50 if limit <= 0
    
    puts "Extracting #{limit} most recent bookmarks from Firefox..."
    bookmarks = extractor.extract_recent_bookmarks(limit)
    extractor.display_bookmarks(bookmarks)
    
  rescue => e
    puts "Error: #{e.message}"
    puts "\nUsage: ruby #{__FILE__} [number_of_bookmarks]"
    puts "Example: ruby #{__FILE__} 25"
    exit 1
  end
end