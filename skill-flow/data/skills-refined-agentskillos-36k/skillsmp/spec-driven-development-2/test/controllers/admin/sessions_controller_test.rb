require "test_helper"

class Admin::SessionsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @admin = Admin.create!(
      username: 'sessiontest',
      password: 'password123',
      password_confirmation: 'password123'
    )
  end

  # GET /admin/login
  test "should get login page" do
    get admin_login_path
    assert_response :success
    assert_select "form"
  end

  test "should redirect to dashboard if already logged in" do
    # Log in first
    post admin_login_path, params: {
      username: @admin.username,
      password: 'password123'
    }

    # Try to access login page again
    get admin_login_path
    assert_redirected_to admin_dashboard_path
  end

  # POST /admin/login
  test "should log in with valid credentials" do
    post admin_login_path, params: {
      username: @admin.username,
      password: 'password123'
    }

    assert_redirected_to admin_dashboard_path
    assert_equal @admin.id, session[:admin_id]
    assert_not_nil session[:admin_expires_at]
    assert_equal "Welcome back, #{@admin.username}!", flash[:notice]
  end

  test "should not log in with invalid username" do
    post admin_login_path, params: {
      username: 'wronguser',
      password: 'password123'
    }

    assert_response :unprocessable_entity
    assert_nil session[:admin_id]
    assert_equal "Invalid username or password", flash[:alert]
  end

  test "should not log in with invalid password" do
    post admin_login_path, params: {
      username: @admin.username,
      password: 'wrongpassword'
    }

    assert_response :unprocessable_entity
    assert_nil session[:admin_id]
    assert_equal "Invalid username or password", flash[:alert]
  end

  test "should set session expiration time on login" do
    post admin_login_path, params: {
      username: @admin.username,
      password: 'password123'
    }

    assert_not_nil session[:admin_expires_at]
    # Check it's approximately 12 hours from now (within 1 minute tolerance)
    expected_expiry = 12.hours.from_now
    actual_expiry = session[:admin_expires_at]
    assert_in_delta expected_expiry.to_i, actual_expiry.to_i, 60
  end

  # DELETE /admin/logout
  test "should log out and clear session" do
    # Log in first
    post admin_login_path, params: {
      username: @admin.username,
      password: 'password123'
    }
    assert_not_nil session[:admin_id]

    # Log out
    delete admin_logout_path

    assert_redirected_to root_path
    assert_nil session[:admin_id]
    assert_nil session[:admin_expires_at]
    assert_equal "Logged out successfully", flash[:notice]
  end

  test "should handle logout when not logged in" do
    delete admin_logout_path

    assert_redirected_to root_path
    assert_nil session[:admin_id]
  end

  # Security tests
  test "should not expose which field is incorrect" do
    # Wrong username
    post admin_login_path, params: {
      username: 'nonexistent',
      password: 'password123'
    }
    wrong_username_message = flash[:alert]

    # Wrong password
    post admin_login_path, params: {
      username: @admin.username,
      password: 'wrongpass'
    }
    wrong_password_message = flash[:alert]

    # Messages should be identical for security
    assert_equal wrong_username_message, wrong_password_message
    assert_equal "Invalid username or password", wrong_username_message
  end

  test "should handle empty credentials" do
    post admin_login_path, params: {
      username: '',
      password: ''
    }

    assert_response :unprocessable_entity
    assert_nil session[:admin_id]
  end

  test "should handle nil credentials" do
    post admin_login_path, params: {}

    assert_response :unprocessable_entity
    assert_nil session[:admin_id]
  end
end
