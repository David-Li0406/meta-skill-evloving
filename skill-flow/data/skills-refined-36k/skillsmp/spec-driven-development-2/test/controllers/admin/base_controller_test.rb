require "test_helper"

class Admin::BaseControllerTest < ActionDispatch::IntegrationTest
  setup do
    @admin = Admin.create!(
      username: 'basecontrollertest',
      password: 'password123',
      password_confirmation: 'password123'
    )
  end

  # Test authentication requirement by trying to access admin area
  # We'll use a real admin route once sessions controller is created
  # For now, we test the authentication logic conceptually

  test "require_admin redirects when not authenticated" do
    # Create a simple controller instance to test the method
    controller = Admin::BaseController.new
    controller.request = ActionDispatch::Request.new({})
    controller.response = ActionDispatch::Response.new

    # Stub session to return nil admin_id
    def controller.session
      {}
    end

    def controller.redirect_to(path, options = {})
      @redirected = true
      @redirect_path = path
      @redirect_options = options
    end

    def controller.admin_login_path
      '/admin/login'
    end

    # Test that require_admin redirects
    controller.send(:require_admin)
    assert controller.instance_variable_get(:@redirected), "Should redirect when not authenticated"
  end

  test "current_admin returns nil when session is empty" do
    controller = Admin::BaseController.new
    controller.request = ActionDispatch::Request.new({})
    controller.response = ActionDispatch::Response.new

    def controller.session
      {}
    end

    assert_nil controller.send(:current_admin), "Should return nil when no admin_id in session"
  end

  test "current_admin returns admin when session has admin_id" do
    controller = Admin::BaseController.new
    controller.request = ActionDispatch::Request.new({})
    controller.response = ActionDispatch::Response.new

    def controller.session
      { admin_id: @admin.id }
    end

    # Define the instance variable for the admin
    controller.instance_variable_set(:@admin, @admin)

    result = controller.send(:current_admin)
    assert_equal @admin.id, result.id, "Should return admin from session"
  end

  test "current_admin caches the result" do
    controller = Admin::BaseController.new
    controller.request = ActionDispatch::Request.new({})
    controller.response = ActionDispatch::Response.new

    def controller.session
      { admin_id: @admin.id }
    end

    controller.instance_variable_set(:@admin, @admin)

    # Call twice to test caching
    first_call = controller.send(:current_admin)
    second_call = controller.send(:current_admin)

    assert_equal first_call.object_id, second_call.object_id, "Should cache the admin instance"
  end
end
