# Accessibility, Localization & Productivity

## Internationalization (i18n)
The engine supports multiple locales for numbers, dates, and UI labels.

### Global & Per-Chart Settings
```typescript
import { setGlobalLocale } from 'scichart-engine';

setGlobalLocale('es-ES'); // Global setting

const chart = createChart({
  container,
  locale: 'de-DE' // Individual override
});
```

### Supported Locales:
`en-US`, `es-ES`, `de-DE`, `fr-FR`, `pt-BR`, `zh-CN`, `ja-JP`.

## Keyboard Shortcuts
The `PluginKeyboard` provides a centralized manager for hotkeys.

```typescript
import { PluginKeyboard } from 'scichart-engine/plugins/keyboard';

chart.use(PluginKeyboard({
  extraShortcuts: [
    { key: 'Cmd+S', action: () => chart.snapshot.download() },
    { key: 'R', action: () => chart.resetZoom() }
  ]
}));
```

## Clipboard Integration
The `PluginClipboard` allows users to copy chart data directly to Excel, MATLAB, or other tools.

```typescript
import { PluginClipboard } from 'scichart-engine/plugins/clipboard';

chart.use(PluginClipboard({
  format: 'csv', // 'csv', 'tsv', 'json'
  includeHeaders: true,
  notify: true
}));
```

## Screen Readers & A11y
The engine exposes a simplified ARIA-compatible tree of the chart structure (axes, legend, series summaries) for screen readers.
- Use `chart.setA11y(true)` to enable.
- Legend items are automatically tab-accessible.
