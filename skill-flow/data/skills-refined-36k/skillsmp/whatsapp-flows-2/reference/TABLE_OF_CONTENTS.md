# WhatsApp Flows Reference - Table of Contents

Quick navigation to find what you need.

## By Topic

### Components
**[components.md](components.md)** - All 22 components with full details
- Text components (TextHeading, TextBody, RichText, etc.)
- Input components (TextInput, TextArea, DatePicker, etc.)
- Selection components (Dropdown, CheckboxGroup, RadioButtonsGroup, etc.)
- Media components (Image, ImageCarousel, PhotoPicker, etc.)
- Navigation & action components (Footer, EmbeddedLink, If, Switch)

### Data & Binding
**[data-binding.md](data-binding.md)** - How data flows through your Flow
- Form data: `${form.field_name}`
- Server data: `${data.field_name}`
- Global references: `${screen.SCREEN_ID.form.field}`
- Nested expressions: `${`...`}`
- Data schemas with `__example__`

### Actions & Navigation
**[actions.md](actions.md)** - What happens when users interact
- navigate - Move to another screen
- data_exchange - Send data to server
- complete - End flow with response
- update_data - Update screen state (v6.0+)
- open_url - Open external link (v6.0+)

### Logic & Conditions
**[conditional-logic.md](conditional-logic.md)** - Build dynamic flows
- If component for boolean conditions
- Switch component for multiple cases
- Nested expressions with `${`...`}`
- Maximum 3 levels of nesting

### Server Integration
**[server-integration.md](server-integration.md)** - Stateful flows with backends
- Routing models for flow control
- Data endpoints and API integration
- Request/response patterns
- Validation and error handling
- Dynamic data from server

### Constraints & Validation
**[constraints.md](constraints.md)** - Limits and validation rules
- Character limits per component
- Component counts per screen
- Option limits for selections
- Screen structure rules
- Flow JSON size limits

### Security & Best Practices
**[security.md](security.md)** - Secure and maintainable flows
- Sensitive data handling (passwords, SSNs, etc.)
- HTTPS requirements
- Best practices (10 key points)
- Common patterns
- Testing strategies

### Versions & Features
**[versions.md](versions.md)** - Feature availability by version
- Complete feature matrix v4.0-7.1
- Breaking changes between versions
- Migration guide
- Version recommendations

## By Use Case

### I'm building a simple form
1. Read **SKILL.md** quick start
2. Check **[components.md](components.md)** for TextInput, TextArea, Footer
3. Check **[data-binding.md](data-binding.md)** for form data syntax
4. See **[examples.md](../examples.md)** for multi-screen form example
5. Run **validate_flow.py** to check your JSON

### I need conditional logic
1. Read **SKILL.md** conditional logic section
2. Read **[conditional-logic.md](conditional-logic.md)** for If/Switch components
3. Check **[data-binding.md](data-binding.md)** for nested expressions
4. See **[examples.md](../examples.md)** for age verification example

### I'm integrating with a server
1. Read **[server-integration.md](server-integration.md)** for routing model setup
2. Check **[actions.md](actions.md)** for data_exchange action
3. See **[examples.md](../examples.md)** for server validation example
4. Read **[data-binding.md](data-binding.md)** for dynamic data binding

### I need to display dynamic data
1. Check **[data-binding.md](data-binding.md)** for server data syntax
2. Read **[components.md](components.md)** for Dropdown, NavigationList with dynamic data
3. See **[examples.md](../examples.md)** for e-commerce example
4. Read **[server-integration.md](server-integration.md)** for fetching data

### I'm building something advanced
1. Read **[conditional-logic.md](conditional-logic.md)** for If/Switch
2. Read **[server-integration.md](server-integration.md)** for routing
3. Check **[data-binding.md](data-binding.md)** for nested expressions
4. Review **[security.md](security.md)** for best practices
5. Check **[constraints.md](constraints.md)** for limits

### I need to validate my Flow
1. Run **`python scripts/validate_flow.py your-flow.json`**
2. Run **`python scripts/validate_components.py your-flow.json`**
3. Check **[constraints.md](constraints.md)** if errors occur
4. Review **[security.md](security.md)** for quality checks

## By Component Type

### Text Components
See **[components.md](components.md)** - Text section
- TextHeading (80 chars)
- TextSubheading (80 chars)
- TextBody (4096 chars, markdown v5.1+)
- TextCaption (409 chars, markdown v5.1+)
- RichText (4096 chars, full markdown v5.1+)

### Input Components
See **[components.md](components.md)** - Input section
- TextInput (7 input types)
- TextArea (600 chars)
- DatePicker (native date picker)
- CalendarPicker (calendar v6.1+)
- PhotoPicker (image upload v5.0+)
- DocumentPicker (file upload v5.0+)

### Selection Components
See **[components.md](components.md)** - Selection section
- CheckboxGroup (multiple, max 20)
- RadioButtonsGroup (single, max 20)
- Dropdown (static/dynamic, max 200/100)
- OptIn (checkbox with link, max 5/screen)
- ChipsSelector (buttons, v6.3+)
- NavigationList (rich items, v6.2+)

### Media Components
See **[components.md](components.md)** - Media section
- Image (max 3/screen, HTTPS only)
- ImageCarousel (slides, v7.1+)

### Action Components
See **[components.md](components.md)** - Actions section
- Footer (primary button, required on terminal)
- EmbeddedLink (secondary link)
- If (conditional, v4.0+)
- Switch (multi-way conditional, v4.0+)

## Quick Reference

- **SKILL.md** - Overview and quick start
- **examples.md** - 4 complete working flows
- **reference/** - Detailed documentation (this folder)
- **scripts/** - Validation tools
