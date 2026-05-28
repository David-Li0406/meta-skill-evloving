# JavaScript Hooks Reference

## Hook Lifecycle

```javascript
let Hooks = {}

Hooks.MyHook = {
  mounted() {
    // Called when element is added to DOM
    console.log("Element mounted:", this.el)
  },

  updated() {
    // Called when element is updated by LiveView patch
    console.log("Element updated")
  },

  beforeUpdate() {
    // Called before LiveView patch (rarely needed)
  },

  destroyed() {
    // Called when element is removed from DOM
    // Clean up timers, listeners, etc.
    console.log("Element destroyed")
  },

  disconnected() {
    // Called when LiveView disconnects
  },

  reconnected() {
    // Called when LiveView reconnects
  }
}
```

## Accessing Hook Properties

```javascript
Hooks.MyHook = {
  mounted() {
    this.el           // The hook's DOM element
    this.el.dataset   // Data attributes (data-foo="bar" → dataset.foo)
    this.pushEvent()  // Send event to server
    this.handleEvent() // Receive event from server
    this.upload()     // Trigger file upload
    this.uploadTo()   // Upload to external service
  }
}
```

## Common Patterns

### Third-Party Library Integration

```javascript
Hooks.Chart = {
  mounted() {
    const data = JSON.parse(this.el.dataset.chartData)

    this.chart = new Chart(this.el.getContext('2d'), {
      type: 'line',
      data: data,
      options: {
        responsive: true
      }
    })

    // Listen for updates from server
    this.handleEvent("update-chart", ({data}) => {
      this.chart.data = data
      this.chart.update()
    })
  },

  updated() {
    // Re-parse data if element updated
    const data = JSON.parse(this.el.dataset.chartData)
    this.chart.data = data
    this.chart.update()
  },

  destroyed() {
    // Clean up
    this.chart.destroy()
  }
}
```

**Template:**

```heex
<canvas
  id="sales-chart"
  phx-hook="Chart"
  data-chart-data={Jason.encode!(@chart_data)}
  width="400"
  height="200">
</canvas>
```

### Clipboard Copy

```javascript
Hooks.CopyToClipboard = {
  mounted() {
    this.el.addEventListener("click", () => {
      const text = this.el.dataset.clipboardText

      navigator.clipboard.writeText(text).then(() => {
        this.pushEvent("copied", {text: text})
      })
    })
  }
}
```

**Template:**

```heex
<button
  id="copy-btn"
  phx-hook="CopyToClipboard"
  data-clipboard-text={@code}>
  Copy Code
</button>
```

### Local Storage Sync

```javascript
Hooks.LocalStorage = {
  mounted() {
    const key = this.el.dataset.key
    const storedValue = localStorage.getItem(key)

    if (storedValue) {
      this.pushEvent("load-from-storage", {
        key: key,
        value: JSON.parse(storedValue)
      })
    }

    this.handleEvent("save-to-storage", ({key, value}) => {
      localStorage.setItem(key, JSON.stringify(value))
    })
  }
}
```

**LiveView:**

```elixir
def mount(_params, _session, socket) do
  {:ok,
   socket
   |> assign(:settings, %{})
   |> attach_hook(:storage, :handle_event, &handle_storage/3)}
end

defp handle_storage("load-from-storage", %{"key" => key, "value" => value}, socket) do
  {:halt, assign(socket, String.to_atom(key), value)}
end

defp handle_storage(_, _, socket), do: {:cont, socket}

def handle_event("update_settings", settings, socket) do
  {:noreply,
   socket
   |> assign(:settings, settings)
   |> push_event("save-to-storage", %{key: "settings", value: settings})}
end
```

### Scroll Position Restoration

```javascript
Hooks.ScrollRestore = {
  mounted() {
    this.scrollPos = 0

    this.el.addEventListener("scroll", () => {
      this.scrollPos = this.el.scrollTop
    })
  },

  updated() {
    this.el.scrollTop = this.scrollPos
  }
}
```

### Infinite Scroll Detection

```javascript
Hooks.InfiniteScroll = {
  mounted() {
    this.pending = false

    this.observer = new IntersectionObserver(entries => {
      const entry = entries[0]

      if (entry.isIntersecting && !this.pending) {
        this.pending = true
        this.pushEvent("load-more", {}, () => {
          this.pending = false
        })
      }
    })

    this.observer.observe(this.el)
  },

  destroyed() {
    this.observer.disconnect()
  }
}
```

**Template:**

```heex
<div id="items">
  <div :for={{dom_id, item} <- @streams.items} id={dom_id}>
    <%= item.name %>
  </div>
  <div id="infinite-scroll" phx-hook="InfiniteScroll"></div>
</div>
```

### Form Autosave

```javascript
Hooks.Autosave = {
  mounted() {
    this.timeout = null

    this.el.addEventListener("input", () => {
      clearTimeout(this.timeout)

      this.timeout = setTimeout(() => {
        this.pushEvent("autosave", {
          data: new FormData(this.el)
        })
      }, 1000)
    })
  },

  destroyed() {
    clearTimeout(this.timeout)
  }
}
```

## Alpine.js Integration

### Basic Setup

```javascript
import Alpine from 'alpinejs'

// Make Alpine available globally
window.Alpine = Alpine

// Start Alpine
Alpine.start()

// LiveSocket setup
let liveSocket = new LiveSocket("/live", Socket, {
  params: {_csrf_token: csrfToken},
  dom: {
    onBeforeElUpdated(from, to) {
      if (from._x_dataStack) {
        window.Alpine.clone(from, to)
      }
    }
  }
})
```

### Alpine with LiveView

```heex
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>

  <div x-show="open" x-transition>
    <!-- LiveView content can update this area -->
    <div phx-click="do_something">
      <%= @dynamic_content %>
    </div>
  </div>
</div>
```

### Dropdown Component

```heex
<div
  x-data="{ open: false }"
  @click.outside="open = false"
  @keydown.escape.window="open = false">

  <button @click="open = !open">
    Options
  </button>

  <div x-show="open" x-transition>
    <button phx-click="edit">Edit</button>
    <button phx-click="delete">Delete</button>
  </div>
</div>
```

### Modal with LiveView

```heex
<div
  x-data="{ open: false }"
  @open-modal.window="open = true"
  @close-modal.window="open = false"
  x-show="open"
  x-transition>

  <div class="modal-backdrop"></div>

  <div class="modal">
    <!-- LiveView component -->
    <.live_component
      module={MyAppWeb.ModalComponent}
      id="modal"
      on_close={JS.dispatch("close-modal")} />
  </div>
</div>
```

## Client-Server Communication

### Pushing Events to Server

```javascript
Hooks.Counter = {
  mounted() {
    let count = 0

    this.el.addEventListener("click", () => {
      count++

      // Send event to server
      this.pushEvent("increment", {count: count}, (reply, ref) => {
        // Optional: handle reply
        console.log("Server replied:", reply)
      })
    })
  }
}
```

**LiveView:**

```elixir
def handle_event("increment", %{"count" => count}, socket) do
  # Reply is optional
  {:reply, %{new_total: socket.assigns.total + count}, socket}
end
```

### Receiving Events from Server

```javascript
Hooks.Notifier = {
  mounted() {
    this.handleEvent("show-notification", ({message, type}) => {
      // Show browser notification
      new Notification(message, {
        icon: `/images/${type}.png`
      })
    })

    this.handleEvent("play-sound", ({sound}) => {
      const audio = new Audio(`/sounds/${sound}.mp3`)
      audio.play()
    })
  }
}
```

**LiveView:**

```elixir
def handle_info({:new_message, message}, socket) do
  {:noreply,
   socket
   |> push_event("show-notification", %{
     message: message.body,
     type: "info"
   })
   |> push_event("play-sound", %{sound: "notification"})}
end
```

## Testing Hooks

### Jest Test Example

```javascript
import {Hooks} from '../hooks'

describe('CopyToClipboard', () => {
  let el, hook

  beforeEach(() => {
    el = document.createElement('button')
    el.dataset.clipboardText = 'test text'

    hook = Object.create(Hooks.CopyToClipboard)
    hook.el = el
    hook.pushEvent = jest.fn()
  })

  test('copies text to clipboard', async () => {
    navigator.clipboard = {
      writeText: jest.fn().mockResolvedValue()
    }

    hook.mounted()
    el.click()

    await Promise.resolve() // Wait for async operation

    expect(navigator.clipboard.writeText).toHaveBeenCalledWith('test text')
    expect(hook.pushEvent).toHaveBeenCalledWith('copied', {text: 'test text'})
  })
})
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing unique `id` on hook element | Add `id` attribute to element with `phx-hook` |
| Hook not cleaning up resources | Implement `destroyed()` to clean up timers, listeners, etc. |
| Accessing stale data in `updated()` | Re-read from `this.el.dataset` |
| Memory leaks from event listeners | Remove listeners in `destroyed()` |
| Not handling disconnection | Implement `disconnected()` and `reconnected()` for reconnection logic |
| Mutating LiveView DOM directly | Use `pushEvent` to trigger server updates instead |

## Best Practices

1. **Keep hooks focused** - One responsibility per hook
2. **Clean up resources** - Always implement `destroyed()`
3. **Use data attributes** - Pass data via `data-*` attributes
4. **Handle edge cases** - Check for null/undefined before accessing properties
5. **Debounce expensive operations** - Use timeouts for scroll, resize, input events
6. **Test hooks** - Write unit tests for hook logic
7. **Document hook purpose** - Add comments explaining what the hook does
8. **Use IntersectionObserver** - Better than scroll events for visibility detection
9. **Prefer server updates** - Let LiveView manage state when possible
10. **Handle reconnection** - Restore state in `reconnected()` if needed
