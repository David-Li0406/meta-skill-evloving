#!/usr/bin/env ruby
# Fixture Generator Script
# Usage: ruby generate_fixtures.rb ModelName [count]
# Example: ruby generate_fixtures.rb Post 3

require 'yaml'

class FixtureGenerator
  def initialize(model_name, count = 2)
    @model_name = model_name
    @table_name = model_name.tableize
    @count = count.to_i
  end

  def generate
    puts "📝 Generating fixtures for #{@model_name} (#{@count} records)"

    # Read schema to get column information
    schema_file = 'db/schema.rb'
    unless File.exist?(schema_file)
      puts "❌ Schema file not found. Run 'rails db:migrate' first."
      exit 1
    end

    schema = File.read(schema_file)
    table_definition = extract_table_definition(schema)

    if table_definition.nil?
      puts "❌ Table '#{@table_name}' not found in schema."
      exit 1
    end

    columns = parse_columns(table_definition)
    fixtures = build_fixtures(columns)

    output_file = "test/fixtures/#{@table_name}.yml"
    write_fixtures(output_file, fixtures)

    puts "✅ Fixtures written to #{output_file}"
    puts "\n📋 Next steps:"
    puts "  1. Review and customize the generated fixtures"
    puts "  2. Add more realistic test data"
    puts "  3. Ensure associations are valid"
  end

  private

  def extract_table_definition(schema)
    # Find table definition in schema
    pattern = /create_table\s+"#{@table_name}".*?do \|t\|(.*?)end/m
    match = schema.match(pattern)
    match ? match[1] : nil
  end

  def parse_columns(definition)
    columns = []

    # Parse each column definition
    definition.scan(/t\.([\w_]+)\s+"([\w_]+)"(?:,\s*(.+))?/) do |type, name, options|
      next if %w[created_at updated_at].include?(name)

      columns << {
        name: name,
        type: type,
        options: parse_options(options)
      }
    end

    columns
  end

  def parse_options(options_string)
    return {} if options_string.nil?

    opts = {}
    options_string.scan(/(\w+):\s*([^,]+)/) do |key, value|
      opts[key.to_sym] = value.strip
    end
    opts
  end

  def build_fixtures(columns)
    fixtures = {}

    (1..@count).each do |i|
      label = number_to_label(i)
      fixtures[label] = generate_record(columns, i)
    end

    fixtures
  end

  def generate_record(columns, index)
    record = {}

    columns.each do |col|
      record[col[:name]] = generate_value(col[:name], col[:type], index)
    end

    # Add timestamps
    record['created_at'] = "<%= #{index}.days.ago %>"
    record['updated_at'] = "<%= #{index}.days.ago %>"

    record
  end

  def generate_value(name, type, index)
    # Handle associations
    if name.end_with?('_id')
      association = name.gsub(/_id$/, '')
      return association == 'user' ? number_to_label(index) : 'one'
    end

    # Handle common column names
    case name
    when 'email'
      "#{@table_name.singularize}#{index}@example.com"
    when 'password_digest'
      "<%= BCrypt::Password.create('password', cost: 4) %>"
    when 'title'
      "Test #{@model_name} #{index}"
    when 'name'
      "Test Name #{index}"
    when 'content', 'body', 'description'
      "This is test content for #{@model_name} number #{index}. It has enough text to pass validation."
    when 'status'
      index.even? ? 1 : 0  # Alternate between statuses
    when /_(count|total)$/
      index * 10
    when 'published_at', 'deleted_at'
      index == 1 ? "<%= 1.day.ago %>" : nil
    else
      # Generate by type
      case type
      when 'string', 'text'
        "Sample #{name} #{index}"
      when 'integer', 'bigint'
        index * 10
      when 'boolean'
        index.odd?
      when 'datetime', 'timestamp'
        "<%= #{index}.days.ago %>"
      when 'date'
        "<%= #{index}.days.ago.to_date %>"
      when 'decimal', 'float'
        (index * 10.5).round(2)
      when 'references'
        'one'
      else
        "value_#{index}"
      end
    end
  end

  def number_to_label(num)
    labels = %w[one two three four five six seven eight nine ten]
    labels[num - 1] || "fixture_#{num}"
  end

  def write_fixtures(filepath, fixtures)
    # Ensure directory exists
    FileUtils.mkdir_p(File.dirname(filepath))

    File.write(filepath, fixtures.to_yaml)
  end
end

if ARGV.length < 1
  puts "Usage: ruby generate_fixtures.rb ModelName [count]"
  puts "Example: ruby generate_fixtures.rb Post 3"
  exit 1
end

model_name = ARGV[0]
count = ARGV[1] || 2

FixtureGenerator.new(model_name, count).generate
