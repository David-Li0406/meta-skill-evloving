# Zimbra Modern UI Zimlet Slots - Complete Reference

Complete reference for available ZimletSlots in Zimbra Modern UI (v9.x/10.x).

> **💡 Essential Tip:** Add `?zimletSlots=show` to your Zimbra URL to visualize all slot locations in the UI!

## Slot System Overview

Slots are injection points in the Modern Web Client UI where zimlets can register components. Slots are enabled in `zimlet.json` and implemented in the zimlet's entry point via `plugins.register()`.

## Header & Navigation

| Slot Name | Location | Description |
|-----------|----------|-------------|
| `slot::app` | Top-level | Root application slot |
| `slot::menu` | Navigation | Main menu customization |
| `slot::vertical-menu-item` | Navigation bar | Add items to main vertical nav (Mail, Calendar, etc.) |
| `slot::web-search-toggle` | Search area | Add buttons/components next to search box |
| `slot::web-search` | Search (non-visible) | Search functionality hook |
| `slot::searchInputPlaceholder` | Search (non-visible) | Customize search placeholder |
| `slot::custom-fonts` | Application (non-visible) | Register custom fonts |

## Email View

| Slot Name | Location | Description |
|-----------|----------|-------------|
| `slot::email-tab-item` | Email header tabs | Add tabs next to "Mail" heading |
| `slot::email-default-tab` | Email (non-visible) | Default email tab configuration |
| `slot::email-attachment-action` | Attachments | Add actions to email attachments |
| `slot::message-body-top` | Message view | Content at top of message body |
| `slot::attachment-single-action` | Attachment | Action for single attachment |
| `slot::attachment-multi-action` | Attachments | Action for multiple attachments |

## Mail List & Sidebar

| Slot Name | Location | Description |
|-----------|----------|-------------|
| `slot::folder-list-middle` | Folder list | Insert items in middle of folder list |
| `slot::folder-group` | Folder list | Add folder groups |
| `slot::folder-list-end` | Folder list | Insert items at end of folder list |
| `slot::mail-sidebar-footer` | Sidebar | Footer area of mail sidebar |
| `slot::mail-pane` | Mail pane | Main mail content area |
| `slot::top-mail-ad-item` | Top of mail list | Insert content at top of mail list |
| `slot::top-mail-generic-slot` | Top of mail list | Generic slot at top of mail list |
| `slot::mail-preview-pane` | Preview (non-visible) | Mail preview pane hook |
| `slot::mail-sender` | Mail items (non-visible) | Sender display customization |

## Mail Actions & Toolbar

| Slot Name | Location | Description |
|-----------|----------|-------------|
| `slot::header-action-menu-item` | Action toolbar | Add items to mail action menu |
| `slot::action-menu-mail-more` | Mail "More" menu | Add items to mail More dropdown |
| `slot::mail-folder-context-menu` | Folder list | Context menu for mail folders |
| `slot::mail-shared-folder-context-menu` | Folder list | Context menu for shared folders |
| `slot::mail-composer-toolbar-send` | Composer | Add to send toolbar in composer |
| `slot::mail-composer-smime-dropdown` | Composer | S/MIME dropdown in composer |
| `slot::compose-attachment-action-menu` | Composer | Attachment action menu in composer |
| `slot::compose-sender-options-menu` | Composer | Sender options dropdown in composer |
| `slot::composer` | Composer | General composer slot |
| `slot::message-smime-status` | Message view | S/MIME status indicator |

## Right Panel

| Slot Name | Location | Description |
|-----------|----------|-------------|
| `slot::rightbar-50px` | Right side | 50px wide right sidebar |
| `slot::rightside-zimlet-slot` | Right side | General right side panel slot |

## Settings

| Slot Name | Location | Description |
|-----------|----------|-------------|
| `slot::settings-dropdown-item` | Settings menu | Add items to settings dropdown |
| `slot::settings-dropdown-item-end` | Settings menu | Add items at end of settings dropdown |
| `slot::additional-signature-settings` | Signature settings | Additional signature configuration |
| `slot::set-default-client` | Default client | Default client settings |

## Calendar

| Slot Name | Location | Description |
|-----------|----------|-------------|
| `slot::calendar-tab-item` | Calendar tabs | Add tabs to calendar page |
| `slot::calendar-folder-list-end` | Calendar sidebar | Content at end of calendar folder list |
| `slot::calendar-body-end` | Calendar view | Content at end of calendar body |
| `slot::calendar-appointment-edit-location` | Appointment edit | Location field customization |
| `slot::calendar-appointment-edit-video-call` | Appointment edit | Video call integration |
| `slot::calendar-subscription-list` | Calendar | Subscription list area |
| `slot::calendar-subscription-menu` | Calendar | Subscription menu |
| `slot::calendar-subscription-modal-flow` | Calendar | Subscription modal workflow |

## Briefcase

| Slot Name | Location | Description |
|-----------|----------|-------------|
| `slot::briefcase-tab-item` | Briefcase tabs | Add tabs to briefcase page |
| `slot::briefcase-default-tab` | Briefcase (non-visible) | Default briefcase tab config |
| `slot::briefcase-document-context-menu` | Document menu | Context menu for documents |
| `slot::briefcase-document-header-action` | Document header | Actions in document header |
| `slot::briefcase-upload-button` | Upload area | Custom upload button |

## Video Apps

| Slot Name | Location | Description |
|-----------|----------|-------------|
| `slot::videoapps-tab-item` | Video apps | Tab items in video apps section |
| `slot::videoapps-landing-page-description` | Video apps | Landing page description |
| `slot::collaboration-zimlet-collaboration-list-videos` | Collaboration | Video list in collaboration |

## Contacts

| Slot Name | Location | Description |
|-----------|----------|-------------|
| `slot::contacts-tab-item` | Contacts tabs | Add tabs to contacts page |
| `slot::contacts-default-tab` | Contacts (non-visible) | Default contacts tab config |
| `slot::contact-add-server-smime-cert` | Contact add | S/MIME certificate for contacts |

## Integrations & Cloud Apps

| Slot Name | Location | Description |
|-----------|----------|-------------|
| `slot::integrations-tab-item` | Integrations page | Add tabs to integrations |
| `slot::cloudapps-tab-item` | Cloud apps | Tab item for cloud app integrations |

## Routing

| Slot Name | Location | Description |
|-----------|----------|-------------|
| `slot::routes` | Application (non-visible) | Register custom URL routes |

## Slot Registration Patterns

### Basic Registration

```javascript
export default function Zimlet(context) {
    const { plugins } = context;
    const exports = {};

    exports.init = function init() {
        // Register a simple component
        plugins.register('slot::web-search-toggle', MyButtonComponent);

        // Register with context passing
        plugins.register('slot::rightside-zimlet-slot', () => (
            <RightPanel context={context} />
        ));

        // Register with props passing
        plugins.register('slot::action-menu-mail-more', (props) => (
            <EmailActionMenu {...props} context={context} />
        ));
    };

    return exports;
}
```

### Route Registration

```javascript
plugins.register('slot::routes', () => [
    <MyComponent path="/email/my-zimlet" />,
    <SettingsPage path="/settings/my-zimlet" />
]);
```

### Menu Item Registration

```javascript
plugins.register('slot::email-tab-item', () => (
    <TabItem
        icon="fa fa-star"
        label="My Feature"
        onClick={() => context.openSidebar('my-panel')}
    />
));
```

## zimlet.json Slot Configuration

Enable slots in `zimlet.json`:

```json
{
  "name": "my-zimlet",
  "slots": {
    "menu": true,
    "routes": true,
    "composer": true,
    "action-menu-mail-more": true,
    "rightside-zimlet-slot": true,
    "settings-dropdown-item": true
  }
}
```

## Handler Context Object

Slot handlers receive a context object with:

```javascript
{
    // Zimbra components for building UI
    zimletComps: { MenuItem, Button, Dialog, TabItem, ... },

    // Account information
    account: { name, email, authToken, ... },

    // Sidebar actions
    openSidebar: (name) => void,
    closeSidebar: () => void,

    // Apollo GraphQL client
    getApolloClient: () => ApolloClient,

    // Internationalization
    intl: { formatMessage, ... },

    // Zimbra origin URL
    zimbraOrigin: 'https://mail.example.com',

    // Zimbra API client
    zimbra: { /* API methods */ }
}
```

## User Properties API

Store per-user settings in LDAP:

```javascript
// Get user property
const value = await context.zimbra.zimlet.getUserProperty('settingName');

// Set user property
await context.zimbra.zimlet.setUserProperty('settingName', 'value');
```

## Discovering New Slots

### Method 1: URL Parameter (Recommended)
Navigate to Zimbra with `?zimletSlots=show` appended to URL.
This highlights all available slot locations in the UI.

### Method 2: Console Messages
Check browser console for "non-visible ZimletSlot" messages when loading Zimbra.

### Method 3: Inspect Deployed Zimlets
```bash
grep -r 'slot::' /opt/zimbra/zimlets-deployed/
```

### Method 4: Check Source
Review Zimbra Modern UI source for `ZimletSlot` components.

## Common Use Cases

| Use Case | Recommended Slot |
|----------|------------------|
| Add button near search | `slot::web-search-toggle` |
| Extend mail actions | `slot::action-menu-mail-more` |
| Add right sidebar panel | `slot::rightside-zimlet-slot` |
| Custom routes/pages | `slot::routes` |
| Composer toolbar | `slot::composer` |
| Settings integration | `slot::settings-dropdown-item` |
| Calendar integration | `slot::calendar-appointment-edit-video-call` |
| Attachment handling | `slot::attachment-single-action` |

## References

- [Zimbra Zimlet Guide](https://github.com/Zimbra/zm-zimlet-guide)
- [Zimbra Wiki - ModernUI Zimlets](https://wiki.zimbra.com/wiki/ModernUI-Zimlets)
- [Zimbra Zimlet Gallery](https://gallery.zetalliance.org/extend/category/modern)
- [Example: zimbra-zimlet-nextcloud](https://github.com/Zimbra/zimbra-zimlet-nextcloud)
- [Example: zimbra-zimlet-sticky-notes](https://github.com/Zimbra/zimbra-zimlet-sticky-notes)

---
*Reference based on Zimbra 10.1.x - Slots may vary by version*
