// app/javascript/controllers/modal_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["dialog", "backdrop"]

  connect() {
    // Prevent body scroll when modal is open
    document.body.style.overflow = "hidden"

    // Add event listeners
    document.addEventListener("keydown", this.handleEscape.bind(this))
  }

  disconnect() {
    // Restore body scroll
    document.body.style.overflow = ""

    // Remove event listeners
    document.removeEventListener("keydown", this.handleEscape.bind(this))
  }

  close(event) {
    if (event) {
      event.preventDefault()
    }

    // Remove modal element from DOM
    this.element.remove()
  }

  closeOnBackdrop(event) {
    // Close only if clicked on backdrop, not dialog
    if (event.target === this.element) {
      this.close()
    }
  }

  handleEscape(event) {
    if (event.key === "Escape") {
      this.close()
    }
  }
}
