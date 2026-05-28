---
name: Accessibility Auditor
description: Add accessibilityLabel and accessibilityHint to Images and Buttons in Leavn app for VoiceOver support
allowed-tools: Read, Edit, Grep
---

# Accessibility Auditor

Add accessibility to UI elements:

1. **Images**: `.accessibilityLabel("Icon description")`
2. **Buttons**: `.accessibilityHint("What happens when tapped")`
3. **Selection**: `.accessibilityAddTraits([.isSelected])`
4. **Hide decorative**: `.accessibilityHidden(true)`

Priority: Home, Community, Bible, ShareVerse features

Use when: Accessibility issues, VoiceOver support, icon-only buttons
