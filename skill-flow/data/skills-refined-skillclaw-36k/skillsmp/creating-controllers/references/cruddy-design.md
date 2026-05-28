# Cruddy by Design

Detailed patterns for keeping controllers focused on standard RESTful actions.

## Contents

- [The 7 Standard Actions](#the-7-standard-actions)
- [When to Create New Controllers](#when-to-create-new-controllers)
- [Pattern 1: Nested Resources](#pattern-1-nested-resources)
- [Pattern 2: Properties Edited Independently](#pattern-2-properties-edited-independently)
- [Pattern 3: Pivot Models](#pattern-3-pivot-models)
- [Pattern 4: Different States](#pattern-4-different-states)

---

## The 7 Standard Actions

Follow Laravel's resource controller conventions strictly:

- `index()` - Display list of resources
- `create()` - Show form to create resource
- `store()` - Store new resource
- `show()` - Display single resource
- `edit()` - Show form to edit resource
- `update()` - Update resource
- `destroy()` - Delete resource

**Philosophy:** Always stick to these 7 actions. If you need a custom action, create a new controller instead. This forces you to think about what resource the user is actually interacting with.

---

## When to Create New Controllers

**Key Insight:** Resources in your controllers don't have to map 1:1 with database tables. Think about what the user is actually doing, not what database table you're updating.

---

## Pattern 1: Nested Resources

If you have a route like `/podcasts/{id}/episodes`, create a dedicated controller:

```php
// Do this
final class PodcastEpisodesController extends Controller
{
    public function index($podcastId): Response
    {
        $podcast = Podcast::with('episodes')->findOrFail($podcastId);

        return Inertia::render('podcast-episodes/index', [
            'podcast' => $podcast,
        ]);
    }
}
```

```php
// Don't do this
final class PodcastsController extends Controller
{
    public function listEpisodes($id) { } // Custom action
}
```

---

## Pattern 2: Properties Edited Independently

If a model property is edited through a separate form, treat it as its own resource:

```php
// Do this
final class PodcastCoverImageController extends Controller
{
    public function update($podcastId): RedirectResponse
    {
        // Handle cover image update
    }
}

Route::put('/podcasts/{id}/cover-image', [PodcastCoverImageController::class, 'update']);
```

```php
// Don't do this
final class PodcastsController extends Controller
{
    public function update($id) { }             // Updates basic fields
    public function updateCoverImage($id) { }   // Custom action
}
```

**Real examples from this codebase:**

- `AccountAvatarController` - Avatar edited separately from account details
- `AccountPreferencesController` - Preferences edited separately from account
- `AccountSecurityController` - Security settings edited separately

---

## Pattern 3: Pivot Models

Treat pivot tables as their own resource:

```php
// For a user_podcast pivot table
final class UserPodcastSubscriptionController extends Controller
{
    public function index(User $user): Response
    {
        $subscriptions = $user->podcastSubscriptions()->get();

        return Inertia::render('subscriptions/index', [
            'subscriptions' => $subscriptions,
        ]);
    }

    public function store(User $user, Podcast $podcast): RedirectResponse
    {
        $user->podcastSubscriptions()->attach($podcast->id);

        return back();
    }

    public function destroy(User $user, Podcast $podcast): RedirectResponse
    {
        $user->podcastSubscriptions()->detach($podcast->id);

        return back();
    }
}
```

---

## Pattern 4: Different States

Different states of the same model are different resources:

```php
// Do this
final class PublishedPostsController extends Controller
{
    public function index() { }
}

final class DraftPostsController extends Controller
{
    public function index() { }
}
```

```php
// Don't do this
final class PostsController extends Controller
{
    public function index($status = 'published') { }  // Optional parameter
    public function listDrafts() { }                  // Custom action
}
```

---

## Anti-Patterns

### Don't add custom actions

```php
// Don't do this
final class PodcastsController extends Controller
{
    public function update($id) { }
    public function updateCoverImage($id) { }   // Custom action
    public function listEpisodes($id) { }       // Custom action
    public function approve($id) { }            // Custom action
}
```

### Don't reuse one action for multiple intents

```php
// Don't do this
public function index($id = null)  // Optional parameter
{
    if ($id === null) {
        // List all episodes
    } else {
        // List specific podcast's episodes
    }
}
```

### Don't make $id mean different things

```php
// Don't do this
final class EpisodesController extends Controller
{
    public function show($id) {
        $episode = Episode::find($id);  // $id is Episode ID
    }

    public function create($id) {
        $podcast = Podcast::find($id);  // $id is Podcast ID - Confusing!
    }
}
```

### Do this instead

```php
// Each controller concerned with one type of resource ID
final class PodcastEpisodesController extends Controller
{
    public function index($podcastId) { }   // Clear naming
    public function create($podcastId) { }  // Consistent parameter
}
```
