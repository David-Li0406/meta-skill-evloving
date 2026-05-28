# Controller Test Examples

```ruby
require "test_helper"

class PostsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @post = posts(:one)
    @user = users(:one)
  end

  # === Public Actions ===
  test "should get index" do
    get posts_path
    assert_response :success
    assert_not_nil assigns(:posts)
  end

  test "should show post" do
    get post_path(@post)
    assert_response :success
  end

  # === Authentication ===
  test "should redirect to login for new when not logged in" do
    get new_post_path
    assert_redirected_to login_path
  end

  test "should get new when logged in" do
    log_in_as @user
    get new_post_path
    assert_response :success
  end

  # === Create ===
  test "should create when valid" do
    log_in_as @user

    assert_difference('Post.count', 1) do
      post posts_path, params: {
        post: { title: "Test", content: "Content", status: :published }
      }
    end

    assert_redirected_to post_path(Post.last)
    assert_equal "게시글이 생성되었습니다.", flash[:notice]
  end

  test "should not create when invalid" do
    log_in_as @user

    assert_no_difference('Post.count') do
      post posts_path, params: { post: { title: "" } }
    end

    assert_response :unprocessable_entity
  end

  # === Authorization ===
  test "should update when authorized" do
    log_in_as @post.user
    patch post_path(@post), params: { post: { title: "Updated" } }

    assert_redirected_to post_path(@post)
    assert_equal "Updated", @post.reload.title
  end

  test "should not update when unauthorized" do
    log_in_as users(:two)
    patch post_path(@post), params: { post: { title: "Hacked" } }

    assert_redirected_to root_path
    assert_not_equal "Hacked", @post.reload.title
  end

  test "should destroy when authorized" do
    log_in_as @post.user

    assert_difference('Post.count', -1) do
      delete post_path(@post)
    end

    assert_redirected_to posts_path
  end
end
```
