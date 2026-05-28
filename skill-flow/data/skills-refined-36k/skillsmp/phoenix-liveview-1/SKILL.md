---
name: phoenix-liveview
description: Use when working with Phoenix LiveView - streams, forms, authentication, hooks, real-time features, or encountering LiveView-specific issues
---

# Phoenix LiveView Patterns

## Overview

Phoenix LiveView enables rich, real-time user experiences with server-rendered HTML. This skill covers essential patterns, common gotchas, and best practices for building production-quality LiveView applications.

## When to Use

Use this skill when:
- Building or modifying LiveView components
- Implementing forms with validation
- Working with streams for dynamic lists
- Setting up authentication and authorization
- Creating JS hooks for client-side interactivity
- Debugging LiveView-specific issues
- Implementing real-time features with PubSub

## Core Patterns

### Stream Operations

Streams provide efficient updates for dynamic lists without re-rendering the entire list:

```elixir
# In mount/3 or handle_info/2
def mount(_params, _session, socket) do
  {:ok,
   socket
   |> assign(:page_title, "Users")
   |> stream(:users, Accounts.list_users())}
end

# In handle_event/3
def handle_event("delete", %{"id" => id}, socket) do
  user = Accounts.get_user!(id)
  {:ok, _} = Accounts.delete_user(user)

  {:noreply, stream_delete(socket, :users, user)}
end

# In template
<table>
  <tbody id="users" phx-update="stream">
    <tr :for={{dom_id, user} <- @streams.users} id={dom_id}>
      <td><%= user.name %></td>
      <td>
        <button phx-click="delete" phx-value-id={user.id}>Delete</button>
      </td>
    </tr>
  </tbody>
</table>
```

**Key points:**
- Always use unique `id` attribute on stream container
- Stream items must have unique DOM IDs (provided by `{dom_id, item}` tuple)
- Use `stream_insert/4` with `:at` option to control position
- `stream_delete/3` removes items efficiently

See `@references/streams.md` for comprehensive stream patterns.

### Form Handling

LiveView forms use `Phoenix.Component.to_form/2` with changesets:

```elixir
def mount(_params, _session, socket) do
  changeset = Accounts.change_user(%User{})

  {:ok,
   socket
   |> assign(:form, to_form(changeset))}
end

def handle_event("validate", %{"user" => user_params}, socket) do
  changeset =
    %User{}
    |> Accounts.change_user(user_params)
    |> Map.put(:action, :validate)

  {:noreply, assign(socket, :form, to_form(changeset))}
end

def handle_event("save", %{"user" => user_params}, socket) do
  case Accounts.create_user(user_params) do
    {:ok, user} ->
      {:noreply,
       socket
       |> put_flash(:info, "User created successfully")
       |> push_navigate(to: ~p"/users/#{user}")}

    {:error, %Ecto.Changeset{} = changeset} ->
      {:noreply, assign(socket, :form, to_form(changeset))}
  end
end
```

**Template:**

```heex
<.simple_form for={@form} phx-change="validate" phx-submit="save">
  <.input field={@form[:name]} label="Name" />
  <.input field={@form[:email]} type="email" label="Email" />
  <:actions>
    <.button>Save</.button>
  </:actions>
</.simple_form>
```

**Key points:**
- Always use `to_form/2` to convert changesets
- Set `:action` to `:validate` for validation events
- Use `phx-change` for live validation, `phx-submit` for submission
- Handle both `{:ok, result}` and `{:error, changeset}` cases

See `@references/forms.md` for advanced form patterns including file uploads, nested forms, and dynamic inputs.

### Authentication Scopes

Phoenix 1.7+ uses router scopes for authentication:

```elixir
# In router.ex
scope "/", MyAppWeb do
  pipe_through [:browser, :require_authenticated_user]

  live_session :require_authenticated_user,
    on_mount: [{MyAppWeb.UserAuth, :ensure_authenticated}] do
    live "/dashboard", DashboardLive
    live "/settings", SettingsLive
  end
end

scope "/", MyAppWeb do
  pipe_through [:browser, :redirect_if_user_is_authenticated]

  live_session :redirect_if_user_is_authenticated,
    on_mount: [{MyAppWeb.UserAuth, :redirect_if_user_authenticated}] do
    live "/users/register", UserRegistrationLive
    live "/users/log_in", UserLoginLive
  end
end

scope "/", MyAppWeb do
  pipe_through [:browser]

  live_session :current_user,
    on_mount: [{MyAppWeb.UserAuth, :mount_current_user}] do
    live "/", HomeLive
    live "/about", AboutLive
  end
end
```

**Common on_mount hooks:**
- `:ensure_authenticated` - Require logged-in user, redirect to login if not
- `:redirect_if_user_authenticated` - Redirect logged-in users away (for login/register pages)
- `:mount_current_user` - Load current user if present, allow anonymous if not

**In LiveView:**

```elixir
def mount(_params, _session, socket) do
  # Current user available via @current_user assign
  # (set by on_mount hook)
  user = socket.assigns.current_user

  {:ok, socket}
end
```

See `@references/authentication.md` for role-based authorization patterns.

### JS Hooks

LiveView supports client-side JavaScript hooks for DOM manipulation:

**Colocated hook (recommended):**

```elixir
# In your LiveView module
def render(assigns) do
  ~H"""
  <div id="map" phx-hook="Map" data-lat={@lat} data-lng={@lng}></div>
  """
end

# JavaScript hook
let Hooks = {}

Hooks.Map = {
  mounted() {
    const lat = parseFloat(this.el.dataset.lat)
    const lng = parseFloat(this.el.dataset.lng)

    this.map = L.map(this.el).setView([lat, lng], 13)

    this.handleEvent("update-location", ({lat, lng}) => {
      this.map.setView([lat, lng], 13)
    })
  },

  updated() {
    // Called when element is updated
    const lat = parseFloat(this.el.dataset.lat)
    const lng = parseFloat(this.el.dataset.lng)
    this.map.setView([lat, lng])
  },

  destroyed() {
    // Cleanup
    this.map.remove()
  }
}

let liveSocket = new LiveSocket("/live", Socket, {
  params: {_csrf_token: csrfToken},
  hooks: Hooks
})
```

**Push events from server:**

```elixir
def handle_event("update_location", %{"lat" => lat, "lng" => lng}, socket) do
  {:noreply,
   socket
   |> assign(:lat, lat, :lng, lng)
   |> push_event("update-location", %{lat: lat, lng: lng})}
end
```

**Key points:**
- Hook element must have unique `id` attribute
- Use `data-*` attributes to pass data to hooks
- Hooks have lifecycle: `mounted()`, `updated()`, `destroyed()`
- Use `this.handleEvent()` to receive server push events
- Use `this.pushEvent()` to send events to server

See `@references/hooks.md` for advanced hook patterns including Alpine.js integration.

## Common Gotchas

### No `else if` in HEEx Templates

HEEx doesn't support `else if` - use separate `:if` attributes:

```heex
<!-- ❌ WRONG - doesn't work -->
<div :if={@status == :loading}>Loading...</div>
<div :else if={@status == :error}>Error!</div>
<div :else>Success!</div>

<!-- ✅ CORRECT - use cond or case in assign -->
<%= case @status do %>
  <% :loading -> %>
    <div>Loading...</div>
  <% :error -> %>
    <div>Error!</div>
  <% :success -> %>
    <div>Success!</div>
<% end %>

<!-- ✅ CORRECT - multiple :if attributes -->
<div :if={@status == :loading}>Loading...</div>
<div :if={@status == :error}>Error!</div>
<div :if={@status == :success}>Success!</div>
```

### Attribute Interpolation Requires `{...}`

```heex
<!-- ❌ WRONG - missing braces -->
<div class=@class>Content</div>

<!-- ✅ CORRECT -->
<div class={@class}>Content</div>

<!-- ✅ CORRECT - multiple classes -->
<div class={[@base_class, @modifier_class]}>Content</div>
```

### Stream IDs Must Match Template IDs

When using streams, the stream name and template container ID must match:

```elixir
# ❌ WRONG - mismatched names
socket |> stream(:products, products)

# Template
<div id="items" phx-update="stream">  <!-- ID doesn't match -->
  <div :for={{dom_id, product} <- @streams.products} id={dom_id}>
    <%= product.name %>
  </div>
</div>

# ✅ CORRECT - names match
socket |> stream(:products, products)

# Template
<div id="products" phx-update="stream">  <!-- ID matches stream name -->
  <div :for={{dom_id, product} <- @streams.products} id={dom_id}>
    <%= product.name %>
  </div>
</div>
```

### Form Field Access

Always use `field[:name]` syntax, not `field.name`:

```heex
<!-- ❌ WRONG -->
<.input field={@form.email} label="Email" />

<!-- ✅ CORRECT -->
<.input field={@form[:email]} label="Email" />
```

### LiveView Mount Runs Multiple Times

`mount/3` is called multiple times during the LiveView lifecycle:
1. During initial HTTP request (disconnected)
2. When establishing WebSocket connection (connected)

Check `connected?(socket)` if you need different behavior:

```elixir
def mount(_params, _session, socket) do
  if connected?(socket) do
    # Only run on WebSocket connection
    Phoenix.PubSub.subscribe(MyApp.PubSub, "topic")
  end

  {:ok, socket}
end
```

### Handle Async Operations Carefully

Use `assign_async/3` for async operations to avoid race conditions:

```elixir
def mount(%{"id" => id}, _session, socket) do
  {:ok,
   socket
   |> assign(:id, id)
   |> assign_async(:user, fn ->
     {:ok, %{user: Accounts.get_user!(id)}}
   end)}
end

# In template
<div :if={@user.loading}>Loading...</div>
<div :if={@user.ok?}>
  <%= @user.result.name %>
</div>
```

## Quick Reference

| Operation | Function | Notes |
|-----------|----------|-------|
| Add stream item | `stream_insert(socket, :name, item, at: pos)` | Default prepends (`:at -1`) |
| Remove stream item | `stream_delete(socket, :name, item)` | Requires item with `:id` |
| Reset stream | `stream(socket, :name, items, reset: true)` | Clears existing items |
| Push event to client | `push_event(socket, "event-name", %{data})` | Received by JS hooks |
| Navigate | `push_navigate(socket, to: path)` | Client-side navigation |
| Redirect | `redirect(socket, to: path)` | Server redirect |
| Update page title | `assign(socket, :page_title, "Title")` | Must define `@page_title` in layout |

## Real-World Patterns

### Infinite Scroll with Streams

```elixir
def mount(_params, _session, socket) do
  {:ok,
   socket
   |> assign(:page, 1, :per_page, 20)
   |> stream(:items, list_items(1, 20))
   |> attach_hook(:scroll, :handle_event, fn
     "load_more", _, socket ->
       {:halt, handle_event("load_more", %{}, socket)}
     _, _, socket ->
       {:cont, socket}
   end)}
end

def handle_event("load_more", _, socket) do
  %{page: page, per_page: per_page} = socket.assigns
  next_page = page + 1
  items = list_items(next_page, per_page)

  {:noreply,
   socket
   |> assign(:page, next_page)
   |> stream(:items, items, at: -1)}
end
```

### Debounced Search

```elixir
def handle_event("search", %{"query" => query}, socket) do
  Process.send_after(self(), {:run_search, query}, 300)
  {:noreply, assign(socket, :query, query)}
end

def handle_info({:run_search, query}, socket) do
  # Only run if query hasn't changed
  if socket.assigns.query == query do
    results = search(query)
    {:noreply, stream(socket, :results, results, reset: true)}
  else
    {:noreply, socket}
  end
end
```

### Optimistic Updates

```elixir
def handle_event("toggle_complete", %{"id" => id}, socket) do
  item = Enum.find(socket.assigns.items, &(&1.id == String.to_integer(id)))

  # Optimistic update
  updated_item = %{item | completed: !item.completed}

  {:noreply,
   socket
   |> stream_insert(:items, updated_item)
   |> assign(:async_update,
     Task.async(fn ->
       Todos.update_item(item, %{completed: updated_item.completed})
     end))}
end

def handle_info({ref, result}, socket) when socket.assigns.async_update.ref == ref do
  case result do
    {:ok, item} ->
      {:noreply, stream_insert(socket, :items, item)}
    {:error, _} ->
      # Revert optimistic update
      old_item = %{socket.assigns.items | completed: !completed}
      {:noreply,
       socket
       |> stream_insert(:items, old_item)
       |> put_flash(:error, "Failed to update")}
  end
end
```

## Testing LiveView

```elixir
test "creates item when form is valid", %{conn: conn} do
  {:ok, lv, _html} = live(conn, ~p"/items/new")

  # Test validation
  lv
  |> form("#item-form", item: %{name: ""})
  |> render_change()

  assert has_element?(lv, "#item-form .invalid-feedback")

  # Test submission
  {:ok, _lv, html} =
    lv
    |> form("#item-form", item: %{name: "Buy milk"})
    |> render_submit()
    |> follow_redirect(conn)

  assert html =~ "Item created successfully"
  assert html =~ "Buy milk"
end

test "updates item stream on create", %{conn: conn} do
  {:ok, lv, _html} = live(conn, ~p"/items")

  # Subscribe to updates
  Phoenix.PubSub.subscribe(MyApp.PubSub, "items")

  # Trigger create in another process
  item = insert(:item)
  Phoenix.PubSub.broadcast(MyApp.PubSub, "items", {:item_created, item})

  # Verify stream updated
  assert render(lv) =~ item.name
end
```

**Key testing points:**
- Use `live/2` to mount LiveView in tests
- Use `has_element?/2` to check for presence
- Use `form/2` with `render_change/1` for validation
- Use `render_submit/1` and `follow_redirect/2` for form submission
- Test PubSub integration by broadcasting messages
- Verify IDs match between stream calls and templates

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgot `:id` on phx-update element | Add unique `id` attribute matching stream name |
| Stream items don't have DOM IDs | Use `{dom_id, item}` tuple from stream |
| Form not using `to_form/2` | Always convert changesets with `to_form/2` |
| Missing `:action` on validation | Set `Map.put(:action, :validate)` on changeset |
| Hook not receiving events | Check element has unique `id` and hook name matches |
| Data not updating in hook | Implement `updated()` lifecycle callback |
| Race condition in async operations | Use `assign_async/3` instead of manual async |

## References

- `@references/streams.md` - Comprehensive stream patterns and pagination
- `@references/forms.md` - Advanced form patterns including uploads and nested forms
- `@references/hooks.md` - JavaScript hooks with Alpine.js and third-party library integration
- `@references/authentication.md` - Role-based authorization and session management
