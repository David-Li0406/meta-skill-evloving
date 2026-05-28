# htmx Attributes Quick Reference

## Core Request Attributes

| Attribute | Description | Example |
|-----------|-------------|---------|
| `hx-get` | GET request to URL | `hx-get="/api/users"` |
| `hx-post` | POST request to URL | `hx-post="/api/users"` |
| `hx-put` | PUT request to URL | `hx-put="/api/users/1"` |
| `hx-patch` | PATCH request to URL | `hx-patch="/api/users/1"` |
| `hx-delete` | DELETE request to URL | `hx-delete="/api/users/1"` |

## Trigger Modifiers

| Modifier | Description | Example |
|----------|-------------|---------|
| `changed` | Only fire if value changed | `hx-trigger="keyup changed"` |
| `delay:<time>` | Delay before firing | `hx-trigger="keyup delay:500ms"` |
| `throttle:<time>` | Throttle requests | `hx-trigger="scroll throttle:500ms"` |
| `once` | Fire only once | `hx-trigger="load once"` |
| `from:<selector>` | Listen on different element | `hx-trigger="click from:body"` |
| `target:<selector>` | Filter to target element | `hx-trigger="click target:.btn"` |
| `consume` | Prevent event propagation | `hx-trigger="click consume"` |
| `queue:<type>` | Queue behavior (first, last, all, none) | `hx-trigger="click queue:last"` |

## Special Triggers

| Trigger | Description |
|---------|-------------|
| `load` | Fire on element load |
| `revealed` | Fire when element enters viewport |
| `intersect` | Fire on intersection (with options) |
| `every <time>` | Polling interval |

## Swap Strategies

| Value | Description |
|-------|-------------|
| `innerHTML` | Replace inner content (default) |
| `outerHTML` | Replace entire element |
| `beforebegin` | Insert before element |
| `afterbegin` | Insert at start of element |
| `beforeend` | Insert at end of element |
| `afterend` | Insert after element |
| `delete` | Delete target element |
| `none` | No swap (process OOB only) |

## Swap Modifiers

| Modifier | Description | Example |
|----------|-------------|---------|
| `swap:<time>` | Delay before swap | `hx-swap="innerHTML swap:500ms"` |
| `settle:<time>` | Delay after swap | `hx-swap="innerHTML settle:500ms"` |
| `scroll:<target>` | Scroll behavior | `hx-swap="innerHTML scroll:top"` |
| `show:<target>` | Show element | `hx-swap="innerHTML show:top"` |
| `focus-scroll:true` | Scroll focused element | `hx-swap="innerHTML focus-scroll:true"` |
| `ignoreTitle:true` | Ignore title in response | `hx-swap="innerHTML ignoreTitle:true"` |

## Target Extended Selectors

| Selector | Description |
|----------|-------------|
| `this` | Target the triggering element |
| `closest <sel>` | Closest ancestor matching selector |
| `find <sel>` | First descendant matching selector |
| `next` | Next sibling element |
| `next <sel>` | Next sibling matching selector |
| `previous` | Previous sibling element |
| `previous <sel>` | Previous sibling matching selector |

## Request Parameters

| Attribute | Description | Example |
|-----------|-------------|---------|
| `hx-include` | Include element values | `hx-include="[name='extra']"` |
| `hx-params` | Filter parameters | `hx-params="*"`, `hx-params="not secret"` |
| `hx-vals` | Add values (JSON) | `hx-vals='{"key":"value"}'` |
| `hx-headers` | Add headers (JSON) | `hx-headers='{"X-Token":"abc"}'` |

## Synchronization

| Pattern | Description |
|---------|-------------|
| `hx-sync="closest form:abort"` | Abort on new request from form |
| `hx-sync="this:drop"` | Drop new requests while one in flight |
| `hx-sync="this:replace"` | Replace in-flight request |
| `hx-sync="this:queue first"` | Queue first request only |
| `hx-sync="this:queue last"` | Queue last request only |
| `hx-sync="this:queue all"` | Queue all requests |

## CSS Classes Applied by htmx

| Class | Applied When |
|-------|--------------|
| `htmx-added` | New content added (settle period) |
| `htmx-indicator` | Loading indicator element |
| `htmx-request` | Request in progress |
| `htmx-settling` | During settle phase |
| `htmx-swapping` | During swap phase |

## Response Headers from Server

| Header | Purpose |
|--------|---------|
| `HX-Location` | Client-side redirect with context |
| `HX-Push-Url` | Push URL to history |
| `HX-Redirect` | Full page redirect |
| `HX-Refresh` | Refresh the page |
| `HX-Replace-Url` | Replace URL in history |
| `HX-Reswap` | Override hx-swap |
| `HX-Retarget` | Override hx-target |
| `HX-Reselect` | Override hx-select |
| `HX-Trigger` | Trigger client events |
| `HX-Trigger-After-Settle` | Trigger after settle |
| `HX-Trigger-After-Swap` | Trigger after swap |

## Request Headers Sent by htmx

| Header | Value |
|--------|-------|
| `HX-Boosted` | true if boosted request |
| `HX-Current-URL` | Current page URL |
| `HX-History-Restore-Request` | true if history restore |
| `HX-Prompt` | User prompt response |
| `HX-Request` | Always "true" |
| `HX-Target` | Target element ID |
| `HX-Trigger` | Triggering element ID |
| `HX-Trigger-Name` | Name attribute of trigger |
