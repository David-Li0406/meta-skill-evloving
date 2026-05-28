# Calendly Embed Widget Guide

Embed Calendly scheduling pages directly into your website using the Embed API.

## Setup

Add Calendly's widget assets to your page:

```html
<!-- Calendly CSS -->
<link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">

<!-- Calendly JavaScript -->
<script src="https://assets.calendly.com/assets/external/widget.js" type="text/javascript" async></script>
```

## Embed Types

### 1. Inline Embed

Displays scheduling page embedded within your page content.

**HTML Method:**
```html
<div class="calendly-inline-widget"
     data-url="https://calendly.com/your-link"
     style="min-width:320px;height:700px;">
</div>
```

**JavaScript Method:**
```javascript
Calendly.initInlineWidget({
  url: 'https://calendly.com/your-link',
  parentElement: document.getElementById('calendly-container'),
  prefill: {},
  utm: {}
});
```

### 2. Popup Widget

Opens scheduling in a modal overlay.

```javascript
// Trigger popup on button click
document.getElementById('schedule-btn').addEventListener('click', function() {
  Calendly.initPopupWidget({
    url: 'https://calendly.com/your-link'
  });
});
```

**HTML with onclick:**
```html
<button onclick="Calendly.initPopupWidget({url: 'https://calendly.com/your-link'});">
  Schedule Meeting
</button>
```

### 3. Badge Widget

Floating button that opens popup when clicked.

```javascript
Calendly.initBadgeWidget({
  url: 'https://calendly.com/your-link',
  text: 'Schedule time with me',
  color: '#006bff',
  textColor: '#ffffff',
  branding: true
});
```

**Configuration Options:**
- `text`: Button text
- `color`: Background color (hex)
- `textColor`: Text color (hex)
- `branding`: Show Calendly branding (true/false)

## Prefilling Invitee Information

Pre-populate form fields for returning users:

```javascript
Calendly.initInlineWidget({
  url: 'https://calendly.com/your-link',
  prefill: {
    name: 'John Doe',
    firstName: 'John',
    lastName: 'Doe',
    email: 'john@example.com',
    customAnswers: {
      a1: 'Answer to question 1',
      a2: 'Answer to question 2'
    }
  }
});
```

**URL Parameter Method:**
```
https://calendly.com/your-link?name=John%20Doe&email=john@example.com&a1=Answer
```

## UTM Tracking

Pass marketing attribution data:

```javascript
Calendly.initInlineWidget({
  url: 'https://calendly.com/your-link',
  utm: {
    utmSource: 'website',
    utmMedium: 'embed',
    utmCampaign: 'demo',
    utmContent: 'homepage',
    utmTerm: 'scheduling'
  }
});
```

**URL Parameter Method:**
```
https://calendly.com/your-link?utm_source=website&utm_medium=embed&utm_campaign=demo
```

## Retrieving Scheduling Links via API

Get scheduling URLs dynamically:

### Current User's Scheduling Page
```javascript
fetch('https://api.calendly.com/users/me', {
  headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
})
.then(res => res.json())
.then(data => {
  const schedulingUrl = data.resource.scheduling_url;
  Calendly.initInlineWidget({ url: schedulingUrl });
});
```

### Specific Event Type
```javascript
fetch('https://api.calendly.com/event_types?user=USER_URI', {
  headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
})
.then(res => res.json())
.then(data => {
  const eventType = data.collection[0];
  Calendly.initInlineWidget({ url: eventType.scheduling_url });
});
```

### Team Member Scheduling Pages
```javascript
fetch('https://api.calendly.com/organization_memberships?organization=ORG_URI', {
  headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
})
.then(res => res.json())
.then(data => {
  // data.collection contains all team members with scheduling_url
  const members = data.collection.map(m => ({
    name: m.user.name,
    url: m.user.scheduling_url
  }));
});
```

## Event Listeners

Listen for scheduling events:

```javascript
// Check if Calendly widget is ready
function isCalendlyEvent(e) {
  return e.origin === 'https://calendly.com' &&
         e.data.event &&
         e.data.event.indexOf('calendly.') === 0;
}

// Listen for events
window.addEventListener('message', function(e) {
  if (isCalendlyEvent(e)) {
    console.log('Event:', e.data.event);
    console.log('Payload:', e.data.payload);

    if (e.data.event === 'calendly.event_scheduled') {
      // Booking completed
      console.log('Meeting scheduled!');
      console.log('Event URI:', e.data.payload.event.uri);
      console.log('Invitee URI:', e.data.payload.invitee.uri);
    }

    if (e.data.event === 'calendly.profile_page_viewed') {
      // User viewed scheduling page
    }

    if (e.data.event === 'calendly.event_type_viewed') {
      // User viewed specific event type
    }

    if (e.data.event === 'calendly.date_and_time_selected') {
      // User selected a time slot
    }
  }
});
```

### Available Events

| Event | Description |
|-------|-------------|
| `calendly.profile_page_viewed` | User viewed the scheduling page |
| `calendly.event_type_viewed` | User viewed a specific event type |
| `calendly.date_and_time_selected` | User selected a time slot |
| `calendly.event_scheduled` | Booking completed successfully |

## Styling

### Responsive Container
```css
.calendly-container {
  min-width: 320px;
  height: 700px;
  max-width: 100%;
}

@media (max-width: 768px) {
  .calendly-container {
    height: 900px; /* Taller on mobile */
  }
}
```

### Hide Calendly Branding
Set `hide_gdpr_banner=1` in the URL (requires paid plan):
```
https://calendly.com/your-link?hide_gdpr_banner=1
```

### Custom Colors
Use URL parameters:
```
https://calendly.com/your-link?primary_color=006bff&text_color=4d5055
```

## React Integration

```jsx
import { useEffect, useRef } from 'react';

function CalendlyWidget({ url }) {
  const containerRef = useRef(null);

  useEffect(() => {
    // Load Calendly script if not already loaded
    if (!window.Calendly) {
      const script = document.createElement('script');
      script.src = 'https://assets.calendly.com/assets/external/widget.js';
      script.async = true;
      script.onload = initWidget;
      document.body.appendChild(script);
    } else {
      initWidget();
    }

    function initWidget() {
      window.Calendly.initInlineWidget({
        url,
        parentElement: containerRef.current
      });
    }
  }, [url]);

  return <div ref={containerRef} style={{ minWidth: '320px', height: '700px' }} />;
}

export default CalendlyWidget;
```

## Vue.js Integration

```vue
<template>
  <div ref="calendlyContainer" style="min-width: 320px; height: 700px;"></div>
</template>

<script>
export default {
  props: ['url'],
  mounted() {
    if (window.Calendly) {
      this.initWidget();
    } else {
      const script = document.createElement('script');
      script.src = 'https://assets.calendly.com/assets/external/widget.js';
      script.async = true;
      script.onload = () => this.initWidget();
      document.body.appendChild(script);
    }
  },
  methods: {
    initWidget() {
      window.Calendly.initInlineWidget({
        url: this.url,
        parentElement: this.$refs.calendlyContainer
      });
    }
  }
};
</script>
```

## Troubleshooting

**Widget not loading:**
- Ensure Calendly script is loaded before initialization
- Check browser console for errors
- Verify the scheduling URL is correct

**Height issues:**
- Set explicit height on container
- Use CSS min-height for flexibility

**Events not firing:**
- Check origin in event listener (must be 'https://calendly.com')
- Ensure event listener is added before widget loads
