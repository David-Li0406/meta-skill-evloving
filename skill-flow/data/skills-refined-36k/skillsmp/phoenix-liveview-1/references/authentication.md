# Authentication & Authorization Reference

## Phoenix 1.7+ Authentication

Phoenix 1.7+ uses `on_mount` hooks for authentication in LiveView.

### Basic Setup

```elixir
# lib/my_app_web/user_auth.ex
defmodule MyAppWeb.UserAuth do
  use MyAppWeb, :verified_routes

  import Phoenix.Component
  import Phoenix.LiveView

  def on_mount(:mount_current_user, _params, session, socket) do
    {:cont, mount_current_user(socket, session)}
  end

  def on_mount(:ensure_authenticated, _params, session, socket) do
    socket = mount_current_user(socket, session)

    if socket.assigns.current_user do
      {:cont, socket}
    else
      socket =
        socket
        |> put_flash(:error, "You must log in to access this page.")
        |> redirect(to: ~p"/users/log_in")

      {:halt, socket}
    end
  end

  def on_mount(:redirect_if_user_authenticated, _params, session, socket) do
    socket = mount_current_user(socket, session)

    if socket.assigns.current_user do
      {:halt, redirect(socket, to: ~p"/dashboard")}
    else
      {:cont, socket}
    end
  end

  defp mount_current_user(socket, session) do
    case session do
      %{"user_token" => user_token} ->
        assign_new(socket, :current_user, fn ->
          Accounts.get_user_by_session_token(user_token)
        end)

      %{} ->
        assign_new(socket, :current_user, fn -> nil end)
    end
  end
end
```

### Router Configuration

```elixir
# lib/my_app_web/router.ex
scope "/", MyAppWeb do
  pipe_through [:browser]

  # Public routes (current user loaded if present)
  live_session :public,
    on_mount: [{MyAppWeb.UserAuth, :mount_current_user}] do
    live "/", HomeLive
    live "/about", AboutLive
  end

  # Authentication routes (redirect if already logged in)
  live_session :auth,
    on_mount: [{MyAppWeb.UserAuth, :redirect_if_user_authenticated}] do
    live "/users/register", UserRegistrationLive
    live "/users/log_in", UserLoginLive
    live "/users/reset_password", UserForgotPasswordLive
    live "/users/reset_password/:token", UserResetPasswordLive
  end
end

scope "/", MyAppWeb do
  pipe_through [:browser, :require_authenticated_user]

  # Protected routes (require authentication)
  live_session :authenticated,
    on_mount: [{MyAppWeb.UserAuth, :ensure_authenticated}] do
    live "/dashboard", DashboardLive
    live "/settings", UserSettingsLive
    live "/profile", ProfileLive
  end
end
```

## Role-Based Authorization

### Define Roles

```elixir
# lib/my_app/accounts/user.ex
defmodule MyApp.Accounts.User do
  use Ecto.Schema

  schema "users" do
    field :email, :string
    field :role, Ecto.Enum, values: [:user, :moderator, :admin]

    timestamps()
  end
end
```

### Authorization Hook

```elixir
# lib/my_app_web/user_auth.ex
def on_mount(:require_admin, _params, session, socket) do
  socket = mount_current_user(socket, session)

  if socket.assigns.current_user && socket.assigns.current_user.role == :admin do
    {:cont, socket}
  else
    socket =
      socket
      |> put_flash(:error, "You don't have permission to access this page.")
      |> redirect(to: ~p"/")

    {:halt, socket}
  end
end

def on_mount(:require_moderator_or_admin, _params, session, socket) do
  socket = mount_current_user(socket, session)

  if socket.assigns.current_user && socket.assigns.current_user.role in [:moderator, :admin] do
    {:cont, socket}
  else
    socket =
      socket
      |> put_flash(:error, "You don't have permission to access this page.")
      |> redirect(to: ~p"/")

    {:halt, socket}
  end
end
```

### Router with Roles

```elixir
scope "/admin", MyAppWeb.Admin do
  pipe_through [:browser, :require_authenticated_user]

  live_session :admin,
    on_mount: [
      {MyAppWeb.UserAuth, :ensure_authenticated},
      {MyAppWeb.UserAuth, :require_admin}
    ] do
    live "/users", UserManagementLive
    live "/settings", AdminSettingsLive
  end
end
```

## Resource-Level Authorization

### Ownership Check

```elixir
def on_mount(:ensure_post_owner, %{"id" => post_id}, _session, socket) do
  post = Blog.get_post!(post_id)
  user = socket.assigns.current_user

  if post.user_id == user.id do
    {:cont, assign(socket, :post, post)}
  else
    socket =
      socket
      |> put_flash(:error, "You don't have permission to edit this post.")
      |> redirect(to: ~p"/posts")

    {:halt, socket}
  end
end
```

**Router:**

```elixir
live_session :post_owner,
  on_mount: [
    {MyAppWeb.UserAuth, :ensure_authenticated},
    {MyAppWeb.UserAuth, :ensure_post_owner}
  ] do
  live "/posts/:id/edit", PostEditLive
end
```

### In-LiveView Authorization

```elixir
defmodule MyAppWeb.PostLive.Show do
  use MyAppWeb, :live_view

  def mount(%{"id" => id}, _session, socket) do
    post = Blog.get_post!(id)

    socket =
      socket
      |> assign(:post, post)
      |> assign(:can_edit?, can_edit_post?(socket.assigns.current_user, post))
      |> assign(:can_delete?, can_delete_post?(socket.assigns.current_user, post))

    {:ok, socket}
  end

  defp can_edit_post?(user, post) do
    user && (user.id == post.user_id || user.role in [:moderator, :admin])
  end

  defp can_delete_post?(user, post) do
    user && (user.id == post.user_id || user.role == :admin)
  end

  def handle_event("delete", _, socket) do
    if socket.assigns.can_delete? do
      Blog.delete_post(socket.assigns.post)

      {:noreply,
       socket
       |> put_flash(:info, "Post deleted successfully")
       |> push_navigate(to: ~p"/posts")}
    else
      {:noreply, put_flash(socket, :error, "You don't have permission to delete this post")}
    end
  end
end
```

**Template:**

```heex
<div class="actions">
  <.link :if={@can_edit?} navigate={~p"/posts/#{@post}/edit"}>
    Edit
  </.link>

  <button :if={@can_delete?} phx-click="delete" data-confirm="Are you sure?">
    Delete
  </button>
</div>
```

## Policy Modules

### Centralized Authorization

```elixir
# lib/my_app/policies/post_policy.ex
defmodule MyApp.Policies.PostPolicy do
  alias MyApp.Accounts.User
  alias MyApp.Blog.Post

  def can_view?(_user, _post), do: true

  def can_create?(%User{}), do: true
  def can_create?(nil), do: false

  def can_edit?(%User{id: user_id}, %Post{user_id: post_user_id})
      when user_id == post_user_id,
      do: true

  def can_edit?(%User{role: role}, _post) when role in [:moderator, :admin],
    do: true

  def can_edit?(_, _), do: false

  def can_delete?(%User{id: user_id}, %Post{user_id: post_user_id})
      when user_id == post_user_id,
      do: true

  def can_delete?(%User{role: :admin}, _post), do: true

  def can_delete?(_, _), do: false
end
```

### Using Policies

```elixir
defmodule MyAppWeb.PostLive.Show do
  use MyAppWeb, :live_view

  alias MyApp.Policies.PostPolicy

  def mount(%{"id" => id}, _session, socket) do
    post = Blog.get_post!(id)
    user = socket.assigns.current_user

    unless PostPolicy.can_view?(user, post) do
      raise MyAppWeb.ForbiddenError
    end

    socket =
      socket
      |> assign(:post, post)
      |> assign(:can_edit?, PostPolicy.can_edit?(user, post))
      |> assign(:can_delete?, PostPolicy.can_delete?(user, post))

    {:ok, socket}
  end

  def handle_event("delete", _, socket) do
    post = socket.assigns.post
    user = socket.assigns.current_user

    if PostPolicy.can_delete?(user, post) do
      Blog.delete_post(post)

      {:noreply,
       socket
       |> put_flash(:info, "Post deleted")
       |> push_navigate(to: ~p"/posts")}
    else
      {:noreply, put_flash(socket, :error, "Unauthorized")}
    end
  end
end
```

## Session Management

### Remember Me

```elixir
def handle_event("login", %{"user" => user_params}, socket) do
  %{"email" => email, "password" => password, "remember_me" => remember_me} = user_params

  case Accounts.get_user_by_email_and_password(email, password) do
    {:ok, user} ->
      {:noreply,
       socket
       |> put_flash(:info, "Welcome back!")
       |> redirect(to: signed_in_path(socket, user, remember_me == "true"))}

    {:error, _} ->
      {:noreply,
       socket
       |> put_flash(:error, "Invalid email or password")
       |> assign(:trigger_submit, false)}
  end
end

defp signed_in_path(socket, user, remember_me) do
  socket
  |> UserAuth.log_in_user(user, %{"remember_me" => to_string(remember_me)})
  |> then(fn socket -> socket.assigns[:redirect_to] || ~p"/dashboard" end)
end
```

### Force Logout Other Sessions

```elixir
def handle_event("logout_other_sessions", _, socket) do
  user = socket.assigns.current_user
  current_token = get_session(socket, :user_token)

  # Delete all other sessions
  Accounts.delete_user_sessions_except(user, current_token)

  {:noreply, put_flash(socket, :info, "All other sessions have been logged out")}
end
```

### Session Timeout

```elixir
def mount(_params, session, socket) do
  if connected?(socket) do
    # Set timeout for 30 minutes
    Process.send_after(self(), :check_session, :timer.minutes(30))
  end

  {:ok, mount_current_user(socket, session)}
end

def handle_info(:check_session, socket) do
  if Accounts.valid_session?(get_session(socket, :user_token)) do
    # Reset timeout
    Process.send_after(self(), :check_session, :timer.minutes(30))
    {:noreply, socket}
  else
    {:noreply,
     socket
     |> put_flash(:error, "Session expired. Please log in again.")
     |> redirect(to: ~p"/users/log_in")}
  end
end
```

## Multi-Factor Authentication

### Setup Flow

```elixir
defmodule MyAppWeb.MFASetupLive do
  use MyAppWeb, :live_view

  def mount(_params, _session, socket) do
    user = socket.assigns.current_user

    # Generate TOTP secret
    secret = :crypto.strong_rand_bytes(20) |> Base.encode32(padding: false)

    {:ok,
     socket
     |> assign(:secret, secret)
     |> assign(:qr_code, generate_qr_code(user.email, secret))
     |> assign(:form, to_form(%{}))}
  end

  def handle_event("verify", %{"code" => code}, socket) do
    if valid_totp?(socket.assigns.secret, code) do
      Accounts.enable_mfa(socket.assigns.current_user, socket.assigns.secret)

      {:noreply,
       socket
       |> put_flash(:info, "Two-factor authentication enabled")
       |> push_navigate(to: ~p"/settings")}
    else
      {:noreply, put_flash(socket, :error, "Invalid code. Please try again.")}
    end
  end

  defp valid_totp?(secret, code) do
    NimbleTOTP.valid?(secret, code)
  end

  defp generate_qr_code(email, secret) do
    uri = NimbleTOTP.otpauth_uri("MyApp:#{email}", secret, issuer: "MyApp")
    uri |> EQRCode.encode() |> EQRCode.svg()
  end
end
```

### Login with MFA

```elixir
def handle_event("login", %{"user" => user_params}, socket) do
  %{"email" => email, "password" => password} = user_params

  case Accounts.get_user_by_email_and_password(email, password) do
    {:ok, user} ->
      if user.mfa_enabled do
        {:noreply,
         socket
         |> assign(:awaiting_mfa, true)
         |> assign(:user, user)}
      else
        {:noreply, log_in_user(socket, user)}
      end

    {:error, _} ->
      {:noreply, put_flash(socket, :error, "Invalid email or password")}
  end
end

def handle_event("verify_mfa", %{"code" => code}, socket) do
  user = socket.assigns.user

  if Accounts.valid_mfa_code?(user, code) do
    {:noreply, log_in_user(socket, user)}
  else
    {:noreply, put_flash(socket, :error, "Invalid code")}
  end
end
```

## Security Best Practices

### Rate Limiting

```elixir
def handle_event("login", params, socket) do
  ip = get_connect_info(socket, :peer_data).address

  case RateLimiter.check_rate(ip, :login_attempt) do
    {:allow, _count} ->
      # Process login
      attempt_login(params, socket)

    {:deny, _limit} ->
      {:noreply,
       socket
       |> put_flash(:error, "Too many login attempts. Please try again later.")
       |> assign(:trigger_submit, false)}
  end
end
```

### Secure Password Reset

```elixir
def handle_event("send_reset", %{"email" => email}, socket) do
  # Always show success to prevent email enumeration
  if user = Accounts.get_user_by_email(email) do
    Accounts.deliver_user_reset_password_instructions(
      user,
      &url(~p"/users/reset_password/#{&1}")
    )
  end

  {:noreply,
   socket
   |> put_flash(:info, "If that email exists, you will receive reset instructions.")
   |> push_navigate(to: ~p"/")}
end
```

### CSRF Protection

CSRF tokens are automatically handled by LiveView. For custom forms:

```heex
<form action="/api/logout" method="post">
  <input type="hidden" name="_csrf_token" value={get_csrf_token()} />
  <button type="submit">Logout</button>
</form>
```

## Testing Authentication

```elixir
defmodule MyAppWeb.DashboardLiveTest do
  use MyAppWeb.ConnCase, async: true

  import Phoenix.LiveViewTest

  test "requires authentication", %{conn: conn} do
    assert {:error, {:redirect, %{to: "/users/log_in"}}} =
             live(conn, ~p"/dashboard")
  end

  test "shows dashboard when authenticated", %{conn: conn} do
    user = insert(:user)
    conn = log_in_user(conn, user)

    {:ok, _lv, html} = live(conn, ~p"/dashboard")

    assert html =~ "Dashboard"
    assert html =~ user.email
  end

  test "redirects admin route when not admin", %{conn: conn} do
    user = insert(:user, role: :user)
    conn = log_in_user(conn, user)

    assert {:error, {:redirect, %{to: "/", flash: %{"error" => "You don't have permission"}}}} =
             live(conn, ~p"/admin")
  end

  test "allows admin access", %{conn: conn} do
    admin = insert(:user, role: :admin)
    conn = log_in_user(conn, admin)

    {:ok, _lv, html} = live(conn, ~p"/admin")

    assert html =~ "Admin Panel"
  end
end
```
