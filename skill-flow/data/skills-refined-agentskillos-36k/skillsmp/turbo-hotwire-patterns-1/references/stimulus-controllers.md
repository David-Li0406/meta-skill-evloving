# Stimulus Controllers Reference

## Basic Controller

```javascript
// app/javascript/controllers/hello_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  connect() {
    console.log("Hello controller connected!")
  }

  greet() {
    alert("Hello, Stimulus!")
  }
}
```

```erb
<div data-controller="hello">
  <button data-action="click->hello#greet">Greet</button>
</div>
```

---

## Targets

```javascript
// app/javascript/controllers/search_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input", "results", "count"]

  search() {
    const query = this.inputTarget.value

    fetch(`/search?q=${query}`)
      .then(response => response.text())
      .then(html => {
        this.resultsTarget.innerHTML = html
      })
  }

  clear() {
    this.inputTarget.value = ""
    this.resultsTarget.innerHTML = ""
  }

  // Check if target exists
  updateCount() {
    if (this.hasCountTarget) {
      this.countTarget.textContent = this.resultsTarget.children.length
    }
  }
}
```

```erb
<div data-controller="search">
  <input data-search-target="input"
         data-action="input->search#search">

  <button data-action="click->search#clear">Clear</button>

  <span data-search-target="count"></span>

  <div data-search-target="results"></div>
</div>
```

---

## Values

```javascript
// app/javascript/controllers/countdown_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static values = {
    seconds: { type: Number, default: 60 },
    url: String,
    autoStart: { type: Boolean, default: false }
  }

  connect() {
    if (this.autoStartValue) {
      this.start()
    }
  }

  start() {
    this.remaining = this.secondsValue
    this.timer = setInterval(() => this.tick(), 1000)
  }

  tick() {
    if (this.remaining > 0) {
      this.remaining--
      this.element.textContent = this.remaining
    } else {
      this.finish()
    }
  }

  finish() {
    clearInterval(this.timer)
    if (this.hasUrlValue) {
      window.location.href = this.urlValue
    }
  }

  // Called when value changes
  secondsValueChanged() {
    this.remaining = this.secondsValue
  }

  disconnect() {
    clearInterval(this.timer)
  }
}
```

```erb
<div data-controller="countdown"
     data-countdown-seconds-value="30"
     data-countdown-url-value="/timeout"
     data-countdown-auto-start-value="true">
  30
</div>
```

---

## Actions

```javascript
// app/javascript/controllers/form_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["submit"]

  // Default action (no method specified)
  submit(event) {
    event.preventDefault()
    this.submitTarget.disabled = true
    // ... form submission logic
  }

  // With event options
  // data-action="keydown.enter->form#submit"
  // data-action="click->form#submit:prevent"
}
```

```erb
<form data-controller="form"
      data-action="submit->form#submit">

  <input data-action="keydown.enter->form#submit:prevent">

  <button data-form-target="submit"
          data-action="click->form#validate">
    Submit
  </button>
</form>
```

---

## Classes

```javascript
// app/javascript/controllers/dropdown_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static classes = ["open", "closed"]
  static targets = ["menu"]

  toggle() {
    if (this.menuTarget.classList.contains(this.openClass)) {
      this.close()
    } else {
      this.open()
    }
  }

  open() {
    this.menuTarget.classList.remove(this.closedClass)
    this.menuTarget.classList.add(this.openClass)
  }

  close() {
    this.menuTarget.classList.remove(this.openClass)
    this.menuTarget.classList.add(this.closedClass)
  }
}
```

```erb
<div data-controller="dropdown"
     data-dropdown-open-class="block"
     data-dropdown-closed-class="hidden">

  <button data-action="click->dropdown#toggle">Menu</button>

  <div data-dropdown-target="menu" class="hidden">
    Menu content
  </div>
</div>
```

---

## Outlets (Controller Communication)

```javascript
// app/javascript/controllers/modal_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static outlets = ["form"]

  open() {
    this.element.classList.add("open")

    // Call method on connected form controller
    if (this.hasFormOutlet) {
      this.formOutlet.reset()
    }
  }

  close() {
    this.element.classList.remove("open")
  }
}
```

```erb
<div data-controller="modal"
     data-modal-form-outlet="#task-form">

  <div id="task-form" data-controller="form">
    <!-- form content -->
  </div>
</div>
```

---

## Debounce Pattern

```javascript
// app/javascript/controllers/debounced_search_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static values = { delay: { type: Number, default: 300 } }
  static targets = ["input", "results"]

  search() {
    clearTimeout(this.timeout)

    this.timeout = setTimeout(() => {
      this.performSearch()
    }, this.delayValue)
  }

  async performSearch() {
    const query = this.inputTarget.value

    if (query.length < 2) return

    const response = await fetch(`/search?q=${encodeURIComponent(query)}`)
    const html = await response.text()
    this.resultsTarget.innerHTML = html
  }

  disconnect() {
    clearTimeout(this.timeout)
  }
}
```

---

## Throttle Pattern

```javascript
// app/javascript/controllers/scroll_tracking_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static values = { interval: { type: Number, default: 200 } }

  connect() {
    this.lastRun = 0
    this.element.addEventListener("scroll", this.handleScroll.bind(this))
  }

  handleScroll() {
    const now = Date.now()

    if (now - this.lastRun >= this.intervalValue) {
      this.track()
      this.lastRun = now
    }
  }

  track() {
    const scrollPercentage = (this.element.scrollTop / this.element.scrollHeight) * 100
    console.log(`Scrolled ${scrollPercentage}%`)
  }
}
```
