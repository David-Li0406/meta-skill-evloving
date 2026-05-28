# LiveView Streams Reference

## Stream Operations

### Basic Operations

```elixir
# Initialize stream
stream(socket, :items, items)

# Insert at beginning (default)
stream_insert(socket, :items, new_item)

# Insert at end
stream_insert(socket, :items, new_item, at: -1)

# Insert at specific position
stream_insert(socket, :items, new_item, at: 2)

# Delete item
stream_delete(socket, :items, item)

# Reset stream (clear and re-populate)
stream(socket, :items, new_items, reset: true)
```

### Pagination with Streams

```elixir
defmodule MyAppWeb.ItemsLive do
  use MyAppWeb, :live_view

  def mount(_params, _session, socket) do
    {:ok,
     socket
     |> assign(:page, 1, :per_page, 20, :has_more, true)
     |> load_items()}
  end

  defp load_items(socket) do
    %{page: page, per_page: per_page} = socket.assigns
    items = Items.list_items(page: page, per_page: per_page + 1)

    has_more = length(items) > per_page
    items = Enum.take(items, per_page)

    socket
    |> assign(:has_more, has_more)
    |> stream(:items, items, at: -1)
  end

  def handle_event("load_more", _, socket) do
    {:noreply,
     socket
     |> update(:page, &(&1 + 1))
     |> load_items()}
  end
end
```

### Cursor-Based Pagination

```elixir
def mount(_params, _session, socket) do
  {items, next_cursor} = Items.list_items(cursor: nil, limit: 20)

  {:ok,
   socket
   |> assign(:cursor, next_cursor)
   |> stream(:items, items)}
end

def handle_event("load_more", _, socket) do
  {items, next_cursor} = Items.list_items(
    cursor: socket.assigns.cursor,
    limit: 20
  )

  {:noreply,
   socket
   |> assign(:cursor, next_cursor)
   |> stream(:items, items, at: -1)}
end
```

### Reordering Stream Items

```elixir
def handle_event("move_up", %{"id" => id}, socket) do
  items = Enum.to_list(socket.assigns.streams.items)
  index = Enum.find_index(items, fn {_dom_id, item} -> item.id == id end)

  if index > 0 do
    {item_above, updated_items} = List.pop_at(items, index - 1)
    {current_item, updated_items} = List.pop_at(updated_items, index)

    updated_items =
      updated_items
      |> List.insert_at(index - 1, current_item)
      |> List.insert_at(index, item_above)

    items_only = Enum.map(updated_items, fn {_, item} -> item end)

    {:noreply, stream(socket, :items, items_only, reset: true)}
  else
    {:noreply, socket}
  end
end
```

### Filtering Streams

```elixir
def handle_event("filter", %{"status" => status}, socket) do
  items = Items.list_items(status: status)

  {:noreply,
   socket
   |> assign(:filter_status, status)
   |> stream(:items, items, reset: true)}
end
```

### Stream Updates from PubSub

```elixir
def mount(_params, _session, socket) do
  if connected?(socket) do
    Phoenix.PubSub.subscribe(MyApp.PubSub, "items")
  end

  items = Items.list_items()

  {:ok,
   socket
   |> stream(:items, items)}
end

def handle_info({:item_created, item}, socket) do
  {:noreply, stream_insert(socket, :items, item, at: 0)}
end

def handle_info({:item_updated, item}, socket) do
  {:noreply, stream_insert(socket, :items, item)}
end

def handle_info({:item_deleted, item}, socket) do
  {:noreply, stream_delete(socket, :items, item)}
end
```

## Performance Considerations

### Large Lists

For very large lists, consider:
- Virtualization (only render visible items)
- Server-side pagination
- Cursor-based pagination over offset-based

### Memory Management

Streams keep items in memory. For large datasets:

```elixir
# Limit stream size
def handle_event("add_item", item, socket) do
  items = socket.assigns.streams.items

  socket =
    if length(items) > 1000 do
      # Remove oldest items
      stream(socket, :items, Enum.take(items, -900), reset: true)
    else
      socket
    end

  {:noreply, stream_insert(socket, :items, item, at: 0)}
end
```

## Common Patterns

### Nested Streams

```elixir
<div :for={{group_dom_id, group} <- @streams.groups} id={group_dom_id}>
  <h2><%= group.name %></h2>
  <div id={"items-#{group.id}"} phx-update="stream">
    <div :for={{dom_id, item} <- @streams["items_#{group.id}"]} id={dom_id}>
      <%= item.name %>
    </div>
  </div>
</div>
```

### Optimistic Stream Updates

```elixir
def handle_event("delete", %{"id" => id}, socket) do
  item = Items.get_item!(id)

  # Optimistically remove from stream
  socket = stream_delete(socket, :items, item)

  # Async delete
  Task.start(fn ->
    case Items.delete_item(item) do
      {:ok, _} -> :ok
      {:error, _} ->
        # Send message to revert
        send(self(), {:revert_delete, item})
    end
  end)

  {:noreply, socket}
end

def handle_info({:revert_delete, item}, socket) do
  {:noreply,
   socket
   |> put_flash(:error, "Failed to delete item")
   |> stream_insert(:items, item)}
end
```
