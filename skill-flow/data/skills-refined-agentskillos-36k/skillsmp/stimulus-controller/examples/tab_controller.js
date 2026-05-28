// app/javascript/controllers/tab_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["trigger", "content"]
  static classes = ["active", "hidden"]
  static values = { defaultTab: String }

  connect() {
    // Show default tab on load
    if (this.defaultTabValue) {
      this.showTab(this.defaultTabValue)
    } else {
      // Show first tab by default
      this.showTab(this.triggerTargets[0].dataset.tabId)
    }
  }

  switch(event) {
    event.preventDefault()
    const tabId = event.currentTarget.dataset.tabId
    this.showTab(tabId)
  }

  showTab(tabId) {
    // Deactivate all triggers
    this.triggerTargets.forEach(trigger => {
      trigger.classList.remove(...this.activeClasses)
    })

    // Hide all content
    this.contentTargets.forEach(content => {
      content.classList.add(...this.hiddenClasses)
    })

    // Activate selected trigger
    const activeTrigger = this.triggerTargets.find(t => t.dataset.tabId === tabId)
    if (activeTrigger) {
      activeTrigger.classList.add(...this.activeClasses)
    }

    // Show selected content
    const activeContent = this.contentTargets.find(c => c.dataset.tabId === tabId)
    if (activeContent) {
      activeContent.classList.remove(...this.hiddenClasses)
    }

    // Dispatch custom event
    this.dispatch("changed", { detail: { tabId } })
  }
}

// HTML Usage:
/*
<div data-controller="tab"
     data-tab-active-class="bg-background text-foreground shadow"
     data-tab-hidden-class="hidden"
     data-tab-default-tab-value="jobs">

  <!-- Tab Triggers -->
  <div class="flex gap-2">
    <button data-tab-target="trigger"
            data-tab-id="jobs"
            data-action="click->tab#switch">
      구인
    </button>
    <button data-tab-target="trigger"
            data-tab-id="talents"
            data-action="click->tab#switch">
      구직
    </button>
  </div>

  <!-- Tab Contents -->
  <div data-tab-target="content" data-tab-id="jobs">
    Jobs content
  </div>
  <div data-tab-target="content" data-tab-id="talents">
    Talents content
  </div>
</div>
*/
