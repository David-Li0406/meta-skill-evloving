# Hotwire Testing Reference

## System Tests for Turbo

```ruby
# spec/system/tasks_spec.rb
require 'rails_helper'

RSpec.describe "Tasks", type: :system do
  before do
    driven_by(:selenium_chrome_headless)
  end

  it "creates a task with Turbo" do
    visit tasks_path

    within "#task_form" do
      fill_in "Title", with: "New Task"
      click_button "Create"
    end

    # Verify Turbo update without page reload
    expect(page).to have_content("New Task")
    expect(page).to have_current_path(tasks_path) # No redirect
    expect(page).to have_selector("#task_form input[value='']") # Form reset
  end

  it "updates task via Turbo Stream" do
    task = create(:task, title: "Old Title")
    visit tasks_path

    within "##{dom_id(task)}" do
      click_link "Edit"
      fill_in "Title", with: "New Title"
      click_button "Update"
    end

    # Frame updated in place
    within "##{dom_id(task)}" do
      expect(page).to have_content("New Title")
      expect(page).not_to have_field("Title")
    end
  end

  it "handles validation errors with Turbo" do
    visit tasks_path

    within "#task_form" do
      fill_in "Title", with: "" # Invalid
      click_button "Create"
    end

    expect(page).to have_content("can't be blank")
    expect(page).to have_selector("#task_form") # Form still visible
  end
end
```

---

## Testing Stimulus Controllers

```javascript
// spec/javascript/controllers/search_controller.test.js
import { Application } from "@hotwired/stimulus"
import SearchController from "controllers/search_controller"

describe("SearchController", () => {
  let application
  let controller

  beforeEach(() => {
    document.body.innerHTML = `
      <div data-controller="search">
        <input data-search-target="input" type="text">
        <div data-search-target="results"></div>
      </div>
    `

    application = Application.start()
    application.register("search", SearchController)
    controller = application.getControllerForElementAndIdentifier(
      document.querySelector('[data-controller="search"]'),
      "search"
    )
  })

  afterEach(() => {
    application.stop()
  })

  it("clears input and results", () => {
    controller.inputTarget.value = "test query"
    controller.resultsTarget.innerHTML = "<div>Results</div>"

    controller.clear()

    expect(controller.inputTarget.value).toBe("")
    expect(controller.resultsTarget.innerHTML).toBe("")
  })

  it("searches when input changes", async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve("<div>Search results</div>")
      })
    )

    controller.inputTarget.value = "rails"
    await controller.search()

    expect(global.fetch).toHaveBeenCalledWith("/search?q=rails")
    expect(controller.resultsTarget.innerHTML).toContain("Search results")
  })
})
```

---

## Turbo Events Debugging

```javascript
// Listen to Turbo events for debugging
document.addEventListener("turbo:before-fetch-request", (event) => {
  console.log("Turbo request:", event.detail.url)
})

document.addEventListener("turbo:frame-missing", (event) => {
  console.log("Frame missing:", event.target.id)
})

// Log all Turbo events
[
  "turbo:click",
  "turbo:before-visit",
  "turbo:visit",
  "turbo:before-fetch-request",
  "turbo:before-fetch-response",
  "turbo:submit-start",
  "turbo:submit-end",
  "turbo:before-stream-render",
  "turbo:before-frame-render",
  "turbo:frame-render",
  "turbo:frame-load",
  "turbo:load"
].forEach(event => {
  document.addEventListener(event, (e) => console.log(event, e.detail))
})
```

---

## Common Debugging Issues

| Issue | Solution |
|-------|----------|
| Frame not updating | Check frame IDs match between source and target |
| Streams not working | Verify `turbo_stream_from` subscription |
| Actions not firing | Check data-action syntax and controller registration |
| Morphing issues | Use `data-turbo-permanent` for persistent elements |
| Focus loss | Implement focus management in Stimulus controllers |
| Screen reader issues | Add proper ARIA attributes and live regions |
