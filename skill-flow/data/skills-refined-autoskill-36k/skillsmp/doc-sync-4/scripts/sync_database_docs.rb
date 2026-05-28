#!/usr/bin/env ruby
# Database Documentation Sync Script
# Automatically updates DATABASE.md with current schema

require 'fileutils'

class DatabaseDocSync
  SCHEMA_FILE = 'db/schema.rb'
  OUTPUT_FILE = '.claude/DATABASE.md'

  def initialize
    @schema = File.read(SCHEMA_FILE)
  end

  def sync
    puts "📊 Syncing database documentation..."

    tables = extract_tables

    content = build_documentation(tables)

    File.write(OUTPUT_FILE, content)

    puts "✅ Updated #{OUTPUT_FILE}"
    puts "📋 Summary:"
    puts "  - #{tables.length} tables documented"
    puts "  - #{count_total_columns(tables)} total columns"
    puts "  - #{count_indexes(tables)} indexes"
  end

  private

  def extract_tables
    tables = []

    @schema.scan(/create_table\s+"(\w+)".*?do \|t\|(.*?)end/m) do |table_name, definition|
      next if table_name.start_with?('ar_internal_')

      tables << {
        name: table_name,
        columns: parse_columns(definition),
        indexes: extract_indexes(table_name)
      }
    end

    tables.sort_by { |t| t[:name] }
  end

  def parse_columns(definition)
    columns = []

    # Standard columns
    definition.scan(/t\.([\w_]+)\s+"([\w_]+)"(?:,\s*(.+))?/) do |type, name, options|
      columns << {
        name: name,
        type: type,
        null: !(options&.include?('null: false')),
        default: extract_default(options)
      }
    end

    # Add default timestamp columns
    if definition.include?('t.timestamps')
      columns << { name: 'created_at', type: 'datetime', null: false, default: nil }
      columns << { name: 'updated_at', type: 'datetime', null: false, default: nil }
    end

    columns
  end

  def extract_default(options)
    return nil unless options

    match = options.match(/default:\s*([^,]+)/)
    match ? match[1].strip : nil
  end

  def extract_indexes(table_name)
    indexes = []

    @schema.scan(/add_index\s+"#{table_name}",\s+(.+)/) do |index_def|
      indexes << index_def[0].strip
    end

    indexes
  end

  def build_documentation(tables)
    doc = <<~MD
      # Database Schema

      **Last Updated**: #{Time.now.strftime("%Y-%m-%d %H:%M")}
      **Total Tables**: #{tables.length}

      ## ERD Overview

      ```
    MD

    # Add simple ERD
    doc += build_simple_erd(tables)
    doc += "```\n\n"

    # Add table details
    doc += "## Table Schemas\n\n"

    tables.each do |table|
      doc += build_table_section(table)
    end

    doc
  end

  def build_simple_erd(tables)
    # Group by association patterns
    core_tables = tables.select { |t| %w[users posts job_posts].include?(t[:name]) }

    erd = ""
    core_tables.each do |table|
      erd += "┌─────────────────────┐\n"
      erd += "│  #{table[:name].ljust(18)} │\n"
      erd += "├─────────────────────┤\n"

      # Show first 5 columns
      table[:columns].first(5).each do |col|
        marker = col[:name] == 'id' ? '(PK)' : ''
        marker = '(FK)' if col[:name].end_with?('_id')
        erd += "│ #{col[:name].ljust(13)} #{marker.ljust(5)}│\n"
      end

      erd += "└─────────────────────┘\n\n"
    end

    erd
  end

  def build_table_section(table)
    section = "### #{table[:name]}\n\n"

    # Columns table
    section += "| 컬럼명 | 타입 | Null | Default | 설명 |\n"
    section += "|--------|------|------|---------|------|\n"

    table[:columns].each do |col|
      null_str = col[:null] ? 'YES' : 'NO'
      default_str = col[:default] || '-'
      description = generate_column_description(col[:name], table[:name])

      section += "| #{col[:name]} | #{col[:type]} | #{null_str} | #{default_str} | #{description} |\n"
    end

    # Indexes
    if table[:indexes].any?
      section += "\n**인덱스**:\n"
      table[:indexes].each do |idx|
        section += "- `#{idx}`\n"
      end
    end

    # Associations
    associations = infer_associations(table)
    if associations.any?
      section += "\n**연관관계**:\n"
      associations.each do |assoc|
        section += "- #{assoc}\n"
      end
    end

    section += "\n---\n\n"
    section
  end

  def generate_column_description(col_name, table_name)
    case col_name
    when 'id' then 'Primary Key'
    when 'created_at' then '생성일시'
    when 'updated_at' then '수정일시'
    when 'user_id' then 'User 외래키'
    when 'email' then '이메일'
    when 'password_digest' then '암호화된 비밀번호'
    when 'title' then '제목'
    when 'content', 'body' then '내용'
    when 'status' then '상태 (enum)'
    when /_(count|total)$/ then '카운터 캐시'
    when /_at$/ then '일시'
    when /_id$/ then '외래키'
    else '-'
    end
  end

  def infer_associations(table)
    associations = []

    # belongs_to
    table[:columns].each do |col|
      if col[:name].end_with?('_id') && col[:name] != 'id'
        model = col[:name].gsub(/_id$/, '')
        associations << "belongs_to :#{model}"
      end
    end

    # has_many (common patterns)
    case table[:name]
    when 'users'
      associations += ['has_many :posts', 'has_many :comments', 'has_many :job_posts']
    when 'posts'
      associations += ['has_many :comments', 'has_many :likes, as: :likeable']
    when 'job_posts'
      associations += ['has_many :comments', 'has_many :likes, as: :likeable']
    end

    associations
  end

  def count_total_columns(tables)
    tables.sum { |t| t[:columns].length }
  end

  def count_indexes(tables)
    tables.sum { |t| t[:indexes].length }
  end
end

# Run if executed directly
if __FILE__ == $0
  DatabaseDocSync.new.sync
end
