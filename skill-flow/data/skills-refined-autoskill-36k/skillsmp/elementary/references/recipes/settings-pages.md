# Settings Pages Wireframes

> Forms, toggles, and preference management patterns.

## About This Recipe

Settings pages often have complex state management. These wireframes explore toggle patterns, form layouts, and save behaviors.

```css live
@import '../../assets/elementary/tokens/sketch.css';
@import '../../assets/elementary/components.css';
```
## Settings Panel

```jsx live
function ToggleButton({ active, onToggle, label }) {
  return (
    <button
      onClick={onToggle}
      className={`wf-toggle ${active ? 'active' : ''}`}
      aria-label={`Toggle ${label}`}
    >
      <span className="thumb" />
    </button>
  );
}

function SettingItem({ setting, onToggle }) {
  return (
    <li className="item">
      <div className="info">
        <div className="label">{setting.label}</div>
        <div className="description">{setting.desc}</div>
      </div>
      <ToggleButton
        active={setting.value}
        onToggle={() => onToggle(setting.key)}
        label={setting.label}
      />
    </li>
  );
}

export default function SettingsPanel() {
  const [settings, setSettings] = React.useState({
    notifications: true,
    darkMode: false,
    autoSave: true,
    twoFactor: false,
  });

  const [saved, setSaved] = React.useState(false);

  const toggle = (key) => {
    setSettings({ ...settings, [key]: !settings[key] });
    setSaved(false);
  };

  const save = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  const settingsList = [
    { key: 'notifications', label: 'Push Notifications', desc: 'Receive alerts about important updates' },
    { key: 'darkMode', label: 'Dark Mode', desc: 'Use dark theme across the app' },
    { key: 'autoSave', label: 'Auto-save', desc: 'Automatically save your work' },
    { key: 'twoFactor', label: 'Two-Factor Auth', desc: 'Extra security for your account' },
  ].map(s => ({ ...s, value: settings[s.key] }));

  return (
    <section className="wf-settings">
      <header className="header">
        <h2 className="title">Settings</h2>
      </header>

      <ul className="list">
        {settingsList.map((setting) => (
          <SettingItem
            key={setting.key}
            setting={setting}
            onToggle={toggle}
          />
        ))}
      </ul>

      <footer className="footer">
        <button
          onClick={save}
          className="wf-btn action full"
        >
          {saved ? '✓ Saved!' : 'Save Changes'}
        </button>
      </footer>
    </section>
  );
}
```

---
*Created with [Reactive MD](https://marketplace.visualstudio.com/items?itemName=million-views.reactive-md)*
