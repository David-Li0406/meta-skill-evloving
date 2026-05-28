#!/usr/bin/env ruby
# Rails Resource Generator Script
# Usage: ruby generate_resource.rb ResourceName [fields...]
# Example: ruby generate_resource.rb Article title:string content:text user:references status:integer

require 'fileutils'

class ResourceGenerator
  def initialize(name, fields)
    @name = name
    @table_name = name.tableize
    @fields = fields
  end

  def generate
    puts "🚀 Generating Rails resource: #{@name}"
    puts "📝 Fields: #{@fields.join(', ')}"

    steps = [
      method(:generate_migration),
      method(:generate_model),
      method(:generate_controller),
      method(:generate_routes),
      method(:generate_views),
      method(:generate_tests),
      method(:run_migration)
    ]

    steps.each_with_index do |step, idx|
      puts "\n[#{idx + 1}/#{steps.length}] #{step.name.to_s.gsub('_', ' ').capitalize}..."
      step.call
    end

    puts "\n✅ Resource generation complete!"
    puts "\n📋 Next steps:"
    puts "  1. Review generated files"
    puts "  2. Add validations to app/models/#{@table_name.singularize}.rb"
    puts "  3. Customize views in app/views/#{@table_name}/"
    puts "  4. Run tests: rails test"
  end

  private

  def generate_migration
    timestamp = Time.now.strftime("%Y%m%d%H%M%S")
    migration_file = "db/migrate/#{timestamp}_create_#{@table_name}.rb"

    field_definitions = @fields.map do |field|
      name, type = field.split(':')
      "      t.#{type || 'string'} :#{name}"
    end.join("\n")

    content = <<~RUBY
      class Create#{@name.pluralize} < ActiveRecord::Migration[8.0]
        def change
          create_table :#{@table_name} do |t|
      #{field_definitions}

            t.timestamps
          end

          # Add indexes
          # add_index :#{@table_name}, :user_id
          # add_index :#{@table_name}, [:user_id, :created_at]
        end
      end
    RUBY

    File.write(migration_file, content)
    puts "  ✓ Created #{migration_file}"
  end

  def generate_model
    model_file = "app/models/#{@table_name.singularize}.rb"

    content = <<~RUBY
      class #{@name} < ApplicationRecord
        # Associations
        # belongs_to :user

        # Validations
        # validates :title, presence: true, length: { maximum: 255 }

        # Enums
        # enum status: { draft: 0, published: 1 }

        # Scopes
        # scope :recent, -> { order(created_at: :desc) }

        # Methods
      end
    RUBY

    File.write(model_file, content)
    puts "  ✓ Created #{model_file}"
  end

  def generate_controller
    controller_file = "app/controllers/#{@table_name}_controller.rb"

    content = <<~RUBY
      class #{@name.pluralize}Controller < ApplicationController
        before_action :set_#{@table_name.singularize}, only: [:show, :edit, :update, :destroy]
        before_action :require_login, only: [:new, :create, :edit, :update, :destroy]

        def index
          @#{@table_name} = #{@name}.all.order(created_at: :desc)
        end

        def show
        end

        def new
          @#{@table_name.singularize} = #{@name}.new
        end

        def create
          @#{@table_name.singularize} = current_user.#{@table_name}.build(#{@table_name.singularize}_params)

          if @#{@table_name.singularize}.save
            redirect_to @#{@table_name.singularize}, notice: '#{@name} was successfully created.'
          else
            render :new, status: :unprocessable_entity
          end
        end

        def edit
        end

        def update
          if @#{@table_name.singularize}.update(#{@table_name.singularize}_params)
            redirect_to @#{@table_name.singularize}, notice: '#{@name} was successfully updated.'
          else
            render :edit, status: :unprocessable_entity
          end
        end

        def destroy
          @#{@table_name.singularize}.destroy
          redirect_to #{@table_name}_path, notice: '#{@name} was successfully deleted.'
        end

        private

        def set_#{@table_name.singularize}
          @#{@table_name.singularize} = #{@name}.find(params[:id])
        end

        def #{@table_name.singularize}_params
          params.require(:#{@table_name.singularize}).permit(:title, :content)
        end
      end
    RUBY

    File.write(controller_file, content)
    puts "  ✓ Created #{controller_file}"
  end

  def generate_routes
    puts "  ⚠️  Add to config/routes.rb manually:"
    puts "      resources :#{@table_name}"
  end

  def generate_views
    views_dir = "app/views/#{@table_name}"
    FileUtils.mkdir_p(views_dir)

    # index.html.erb
    File.write("#{views_dir}/index.html.erb", <<~ERB)
      <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold mb-6">#{@name.pluralize}</h1>

        <%= link_to "New #{@name}", new_#{@table_name.singularize}_path, class: "btn btn-primary mb-4" %>

        <div class="space-y-4">
          <% @#{@table_name}.each do |#{@table_name.singularize}| %>
            <div class="card">
              <%= link_to #{@table_name.singularize}_path(#{@table_name.singularize}) do %>
                <h2 class="text-xl font-semibold"><%= #{@table_name.singularize}.title %></h2>
              <% end %>
            </div>
          <% end %>
        </div>
      </div>
    ERB

    puts "  ✓ Created #{views_dir}/index.html.erb"
    puts "  ⚠️  Generate show, new, edit, _form views manually"
  end

  def generate_tests
    puts "  ⚠️  Use /test-gen skill to generate comprehensive tests"
  end

  def run_migration
    puts "  ⚠️  Run manually: rails db:migrate"
  end
end

if ARGV.length < 1
  puts "Usage: ruby generate_resource.rb ResourceName [fields...]"
  puts "Example: ruby generate_resource.rb Article title:string content:text user:references status:integer"
  exit 1
end

name = ARGV[0]
fields = ARGV[1..-1]

ResourceGenerator.new(name, fields).generate
