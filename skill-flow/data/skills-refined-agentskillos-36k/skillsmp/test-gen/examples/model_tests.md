# Model Test Examples

## Complete Model Test

```ruby
require "test_helper"

class PostTest < ActiveSupport::TestCase
  # === Associations ===
  test "should belong to user" do
    post = posts(:one)
    assert_instance_of User, post.user
  end

  test "should have many comments" do
    post = posts(:one)
    assert_respond_to post, :comments
  end

  # === Validations ===
  test "should validate presence of title" do
    post = Post.new(user: users(:one), content: "Content")
    assert_not post.valid?
    assert_includes post.errors[:title], "can't be blank"
  end

  test "should validate title length" do
    post = Post.new(user: users(:one), title: "a" * 256, content: "Content")
    assert_not post.valid?
    assert_includes post.errors[:title], "is too long"
  end

  # === Enums ===
  test "should have status enum" do
    post = posts(:one)
    post.draft!
    assert post.draft?

    post.published!
    assert post.published?
  end

  test "status_i18n should return Korean" do
    post = posts(:one)
    post.published!
    assert_equal "게시됨", post.status_i18n
  end

  # === Scopes ===
  test "recent scope should order by created_at desc" do
    posts = Post.recent.to_a
    assert posts.first.created_at >= posts.last.created_at
  end

  test "published scope should return only published" do
    Post.published.each do |post|
      assert post.published?
    end
  end

  # === Instance Methods ===
  test "increment_views! should increase views_count" do
    post = posts(:one)
    initial = post.views_count
    post.increment_views!
    assert_equal initial + 1, post.reload.views_count
  end

  # === Counter Cache ===
  test "creating comment should increment comments_count" do
    post = posts(:one)
    initial = post.comments_count

    Comment.create!(post: post, user: users(:one), content: "Test")

    assert_equal initial + 1, post.reload.comments_count
  end
end
```

## Polymorphic Association Test

```ruby
test "like should work with post" do
  post = posts(:one)
  like = Like.create!(user: users(:one), likeable: post)

  assert_equal post, like.likeable
  assert_instance_of Post, like.likeable
end
```
