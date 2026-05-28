# Fixture Examples

## Users Fixture

```yaml
one:
  email: user1@example.com
  password_digest: <%= BCrypt::Password.create('password', cost: 4) %>
  name: Test User One
  role_title: Developer
  bio: I am a test developer
  created_at: <%= 2.days.ago %>

two:
  email: user2@example.com
  password_digest: <%= BCrypt::Password.create('password', cost: 4) %>
  name: Test User Two
  role_title: Designer
  created_at: <%= 1.day.ago %>
```

## Posts Fixture

```yaml
one:
  user: one
  title: First Test Post
  content: This is test content with enough text to be valid.
  status: 1  # published
  views_count: 10
  likes_count: 5
  comments_count: 3
  created_at: <%= 1.day.ago %>

two:
  user: two
  title: Second Test Post
  content: Another test post with different content.
  status: 0  # draft
  views_count: 0
  created_at: <%= 2.hours.ago %>
```

## Key Points

- BCrypt cost 4 (faster tests)
- Valid associations (user: one)
- Realistic data
- ERB for dynamic values
- Proper timestamps
