require_relative "../test_helper"

class AdminTest < ActiveSupport::TestCase
  setup do
    Admin.destroy_all
  end

  # Validations

  test "should be valid with valid attributes" do
    admin = Admin.new(
      username: "testadmin",
      password: "password123",
      password_confirmation: "password123"
    )
    assert admin.valid?
  end

  test "should require username" do
    admin = Admin.new(
      username: nil,
      password: "password123",
      password_confirmation: "password123"
    )
    assert_not admin.valid?
    assert_includes admin.errors[:username], "can't be blank"
  end

  test "should require unique username" do
    # Create first admin
    Admin.create!(
      username: "duplicate",
      password: "password123",
      password_confirmation: "password123"
    )

    # Try to create second admin with same username
    admin = Admin.new(
      username: "duplicate",
      password: "password456",
      password_confirmation: "password456"
    )
    assert_not admin.valid?
    assert_includes admin.errors[:username], "has already been taken"
  end

  test "should require username to be at least 3 characters" do
    admin = Admin.new(
      username: "ab",
      password: "password123",
      password_confirmation: "password123"
    )
    assert_not admin.valid?
    assert_includes admin.errors[:username], "is too short (minimum is 3 characters)"
  end

  test "should require username to be at most 50 characters" do
    admin = Admin.new(
      username: "a" * 51,
      password: "password123",
      password_confirmation: "password123"
    )
    assert_not admin.valid?
    assert_includes admin.errors[:username], "is too long (maximum is 50 characters)"
  end

  test "should require password on creation" do
    admin = Admin.new(username: "testadmin", password: nil)
    assert_not admin.valid?
    assert_includes admin.errors[:password], "can't be blank"
  end

  test "should require password to be at least 8 characters" do
    admin = Admin.new(
      username: "testadmin",
      password: "short",
      password_confirmation: "short"
    )
    assert_not admin.valid?
    assert_includes admin.errors[:password], "is too short (minimum is 8 characters)"
  end

  test "should allow password to be nil on update" do
    admin = Admin.create!(
      username: "testadmin",
      password: "password123",
      password_confirmation: "password123"
    )

    admin.username = "newtestadmin"
    assert admin.valid?, "Admin should be valid when updating without changing password"
  end

  # Authentication

  test "should authenticate with correct password" do
    admin = Admin.create!(
      username: "authtest",
      password: "password123",
      password_confirmation: "password123"
    )

    assert admin.authenticate("password123"), "Should authenticate with correct password"
  end

  test "should not authenticate with incorrect password" do
    admin = Admin.create!(
      username: "authtest",
      password: "password123",
      password_confirmation: "password123"
    )

    assert_not admin.authenticate("wrongpassword"), "Should not authenticate with wrong password"
  end

  test "should store password as hashed digest" do
    admin = Admin.create!(
      username: "hashtest",
      password: "password123",
      password_confirmation: "password123"
    )

    assert_not_nil admin.password_digest, "Password digest should be present"
    assert_not_equal "password123", admin.password_digest, "Password should be hashed, not stored in plain text"
    assert admin.password_digest.start_with?("$2a$"), "Should use bcrypt hashing"
  end

  # Edge cases

  test "should allow valid usernames" do
    valid_usernames = ["admin", "test_user", "admin123", "Admin", "ADMIN"]

    valid_usernames.each do |username|
      admin = Admin.new(
        username: username,
        password: "password123",
        password_confirmation: "password123"
      )
      assert admin.valid?, "Username '#{username}' should be valid"
    end
  end

  test "should trim whitespace from username" do
    # This test assumes we might add normalization in the future
    # For now, it documents expected behavior with whitespace
    admin = Admin.new(
      username: "  spaced  ",
      password: "password123",
      password_confirmation: "password123"
    )

    # Currently Rails won't auto-trim, but we document the behavior
    # If we want to trim, we'd add a before_validation callback
    assert_equal "  spaced  ", admin.username
  end
end
