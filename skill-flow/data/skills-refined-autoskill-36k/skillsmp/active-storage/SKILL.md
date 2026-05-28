---
name: active-storage
description: This skill should be used when the user asks about "file uploads", "Active Storage", "attachments", "has_one_attached", "has_many_attached", "image variants", "S3", "cloud storage", "direct uploads", "file processing", "image transformations", or needs guidance on handling file uploads in Rails applications.
version: 1.0.0
---

# Active Storage

Comprehensive guide to file uploads and cloud storage in Rails.

## Setup

```bash
rails active_storage:install
rails db:migrate
```

This creates:
- `active_storage_blobs` - File metadata
- `active_storage_attachments` - Polymorphic join table
- `active_storage_variant_records` - Cached variant info

## Model Configuration

### Single Attachment

```ruby
class User < ApplicationRecord
  has_one_attached :avatar
end
```

### Multiple Attachments

```ruby
class Article < ApplicationRecord
  has_many_attached :images
end
```

### With Service Selection

```ruby
class Document < ApplicationRecord
  has_one_attached :file, service: :amazon
end
```

### With Variants

```ruby
class User < ApplicationRecord
  has_one_attached :avatar do |attachable|
    attachable.variant :thumb, resize_to_limit: [100, 100]
    attachable.variant :medium, resize_to_limit: [300, 300]
  end
end
```

## Attaching Files

### From Form Upload

```ruby
# Controller
def create
  @user = User.new(user_params)
  @user.save
end

def user_params
  params.require(:user).permit(:name, :avatar, images: [])
end
```

```erb
<%# Form %>
<%= form_with model: @user do |form| %>
  <%= form.file_field :avatar %>
  <%= form.file_field :images, multiple: true %>
  <%= form.submit %>
<% end %>
```

### Programmatically

```ruby
# From file
user.avatar.attach(io: File.open("/path/to/photo.jpg"), filename: "photo.jpg")

# From uploaded file
user.avatar.attach(params[:avatar])

# From URL (downloaded)
user.avatar.attach(
  io: URI.open("https://example.com/photo.jpg"),
  filename: "downloaded.jpg",
  content_type: "image/jpeg"
)

# From string content
user.avatar.attach(
  io: StringIO.new(pdf_content),
  filename: "document.pdf",
  content_type: "application/pdf"
)
```

### Check Attachment Status

```ruby
user.avatar.attached?  # true/false
user.images.attached?  # true/false
user.images.any?       # true/false
user.images.count      # number of attachments
```

## Displaying Files

### URLs

```erb
<%# Direct URL %>
<%= url_for(@user.avatar) %>

<%# Download URL %>
<%= rails_blob_path(@user.avatar, disposition: "attachment") %>

<%# Image tag %>
<%= image_tag @user.avatar %>

<%# With fallback %>
<%= image_tag(@user.avatar.attached? ? @user.avatar : "default_avatar.png") %>
```

### Variants (Image Transformations)

```erb
<%# On-the-fly transformation %>
<%= image_tag @user.avatar.variant(resize_to_limit: [100, 100]) %>

<%# Named variant %>
<%= image_tag @user.avatar.variant(:thumb) %>

<%# Complex transformations %>
<%= image_tag @user.avatar.variant(
  resize_to_fill: [200, 200],
  format: :webp,
  saver: { quality: 80 }
) %>
```

### Common Transformations

| Method | Description |
|--------|-------------|
| `resize_to_limit: [w, h]` | Resize to fit within bounds |
| `resize_to_fill: [w, h]` | Resize and crop to fill |
| `resize_to_fit: [w, h]` | Resize to fit exactly |
| `resize_and_pad: [w, h]` | Resize and pad to fill |
| `crop: "100x100+10+10"` | Crop specific area |
| `rotate: 90` | Rotate degrees |
| `format: :webp` | Convert format |

### Preview (PDFs, Videos)

```erb
<%# PDF preview (first page) %>
<%= image_tag @document.file.preview(resize_to_limit: [200, 200]) %>

<%# Video preview (frame) %>
<%= image_tag @article.video.preview(resize_to_limit: [300, 200]) %>
```

## Direct Uploads

### Setup

```erb
<%# Include JS %>
<%= javascript_include_tag "activestorage" %>

<%# Form with direct upload %>
<%= form_with model: @user do |form| %>
  <%= form.file_field :avatar, direct_upload: true %>
<% end %>
```

### JavaScript Events

```javascript
// Listen for upload events
addEventListener("direct-upload:initialize", event => {
  const { target, detail } = event
  const { id, file } = detail
  // Show upload UI
})

addEventListener("direct-upload:progress", event => {
  const { id, progress } = event.detail
  // Update progress bar
})

addEventListener("direct-upload:error", event => {
  const { id, error } = event.detail
  // Handle error
})

addEventListener("direct-uploads:end", event => {
  // All uploads complete
})
```

## Storage Services

### Configuration

```yaml
# config/storage.yml
local:
  service: Disk
  root: <%= Rails.root.join("storage") %>

test:
  service: Disk
  root: <%= Rails.root.join("tmp/storage") %>

amazon:
  service: S3
  access_key_id: <%= Rails.application.credentials.dig(:aws, :access_key_id) %>
  secret_access_key: <%= Rails.application.credentials.dig(:aws, :secret_access_key) %>
  region: us-east-1
  bucket: my-app-<%= Rails.env %>

google:
  service: GCS
  project: my-project
  credentials: <%= Rails.root.join("path/to/keyfile.json") %>
  bucket: my-app-<%= Rails.env %>

azure:
  service: AzureStorage
  storage_account_name: myaccount
  storage_access_key: <%= Rails.application.credentials.dig(:azure, :storage_access_key) %>
  container: my-container

mirror:
  service: Mirror
  primary: amazon
  mirrors: [ google, azure ]
```

### Environment Selection

```ruby
# config/environments/development.rb
config.active_storage.service = :local

# config/environments/production.rb
config.active_storage.service = :amazon
```

### Public Files

```yaml
# config/storage.yml
amazon_public:
  service: S3
  access_key_id: <%= Rails.application.credentials.dig(:aws, :access_key_id) %>
  secret_access_key: <%= Rails.application.credentials.dig(:aws, :secret_access_key) %>
  region: us-east-1
  bucket: my-public-bucket
  public: true
```

```ruby
class Article < ApplicationRecord
  has_many_attached :images, service: :amazon_public
end
```

## Validations

### Using active_storage_validations Gem

```ruby
# Gemfile
gem "active_storage_validations"

# Model
class User < ApplicationRecord
  has_one_attached :avatar

  validates :avatar,
    attached: true,
    content_type: ["image/png", "image/jpeg"],
    size: { less_than: 5.megabytes }
end

class Article < ApplicationRecord
  has_many_attached :images

  validates :images,
    content_type: /\Aimage\/.*\z/,
    size: { less_than: 10.megabytes },
    limit: { max: 10 }
end
```

### Custom Validation

```ruby
class User < ApplicationRecord
  has_one_attached :avatar

  validate :acceptable_avatar

  private

  def acceptable_avatar
    return unless avatar.attached?

    unless avatar.blob.byte_size <= 5.megabyte
      errors.add(:avatar, "is too large (max 5MB)")
    end

    acceptable_types = ["image/jpeg", "image/png", "image/gif"]
    unless acceptable_types.include?(avatar.content_type)
      errors.add(:avatar, "must be JPEG, PNG, or GIF")
    end
  end
end
```

## Downloading and Processing

```ruby
# Download content
binary = user.avatar.download

# Open as tempfile
user.avatar.open do |file|
  # file is a Tempfile
  ImageProcessor.process(file.path)
end

# Access metadata
user.avatar.blob.byte_size
user.avatar.blob.content_type
user.avatar.blob.filename
user.avatar.blob.created_at
```

## Removing Attachments

```ruby
# Remove single attachment
user.avatar.purge        # Sync
user.avatar.purge_later  # Async (recommended)

# Remove specific from many
user.images.find(attachment_id).purge_later

# Remove all
user.images.purge_later
```

## Eager Loading

```ruby
# Avoid N+1 queries
@users = User.with_attached_avatar
@articles = Article.with_attached_images

# Named scope automatically created
User.with_attached_avatar.where(active: true)
```

## Testing

```ruby
# test/models/user_test.rb
require "test_helper"

class UserTest < ActiveSupport::TestCase
  test "can attach avatar" do
    user = users(:one)

    user.avatar.attach(
      io: file_fixture("avatar.png").open,
      filename: "avatar.png",
      content_type: "image/png"
    )

    assert user.avatar.attached?
  end
end
```
