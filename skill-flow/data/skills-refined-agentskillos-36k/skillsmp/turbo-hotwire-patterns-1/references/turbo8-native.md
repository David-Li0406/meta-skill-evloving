# Turbo 8 and Native Features Reference

## Page Refresh (Turbo 8+)

**Morphing** - Update page without full reload, preserving scroll and focus:

```html
<!-- Enable morphing globally -->
<meta name="turbo-refresh-method" content="morph">

<!-- Or per-page -->
<meta name="turbo-refresh-method" content="replace">
```

```ruby
# Controller - trigger page refresh
class TasksController < ApplicationController
  def update
    @task.update(task_params)

    # Send refresh signal to clients
    respond_to do |format|
      format.html { redirect_to tasks_path }
      format.turbo_stream {
        render turbo_stream: turbo_stream.action(:refresh)
      }
    end
  end
end
```

---

## Morph Refresh

**Preserve elements during morph:**

```html
<!-- Element persists across morphs -->
<div id="video-player" data-turbo-permanent>
  <video src="movie.mp4" controls></video>
</div>

<!-- Input state persists -->
<input type="text" data-turbo-permanent>
```

---

## View Transitions API Integration

```css
/* Smooth transitions during Turbo navigation */
@view-transition {
  navigation: auto;
}

::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 0.3s;
}

/* Custom transition for specific elements */
.task-card {
  view-transition-name: task-card;
}
```

---

## Turbo Native (iOS)

```swift
// iOS - SceneDelegate.swift
import Turbo

class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?
    var navigationController = UINavigationController()

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = (scene as? UIWindowScene) else { return }

        window = UIWindow(windowScene: windowScene)
        window?.rootViewController = navigationController
        window?.makeKeyAndVisible()

        visit(url: URL(string: "https://example.com")!)
    }

    func visit(url: URL) {
        let viewController = VisitableViewController(url: url)
        navigationController.pushViewController(viewController, animated: true)
    }
}
```

---

## Turbo Native (Android)

```kotlin
// Android - MainActivity.kt
import dev.hotwire.turbo.session.Session
import dev.hotwire.turbo.visit.TurboVisitOptions

class MainActivity : AppCompatActivity(), TurboActivity {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        TurboSessionNavHostFragment.visit(
            url = "https://example.com",
            options = TurboVisitOptions(action = TurboVisitAction.ADVANCE)
        )
    }
}
```

---

## Native Bridge Patterns

```erb
<!-- app/views/tasks/show.html.erb -->
<% if turbo_native_app? %>
  <%= link_to "Share", "#", data: {
    turbo_frame: "_top",
    controller: "bridge",
    action: "click->bridge#share"
  } %>
<% end %>
```

```javascript
// app/javascript/controllers/bridge_controller.js
import { BridgeComponent } from "@hotwired/turbo-ios"

export default class extends BridgeComponent {
  share() {
    this.send("share", {
      title: "Task Title",
      url: window.location.href
    })
  }
}
```
