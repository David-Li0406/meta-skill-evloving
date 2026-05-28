---
name: User Settings
description: Settings management, preferences, and account configuration
---

# User Settings Skill

## Overview
Manage user preferences, account settings, privacy controls, and personalization.

## Settings Categories
| Category | Settings |
|----------|----------|
| Account | Email, password, username, avatar |
| Display | Theme, language, display name preference |
| Notifications | Push, email, in-app preferences |
| Privacy | Profile visibility, online status |
| Sound | Volume levels, mute toggles |
| Gameplay | Auto-actions, bet sizing defaults |

## Database Schema
```sql
-- Main settings in profiles table
ALTER TABLE profiles ADD COLUMN settings JSONB DEFAULT '{
  "theme": "dark",
  "language": "en",
  "display_name_preference": "username",
  "notifications": {
    "push_enabled": true,
    "email_enabled": true,
    "likes": true,
    "comments": true,
    "follows": true,
    "game_invites": true,
    "promotions": false
  },
  "privacy": {
    "profile_public": true,
    "show_online_status": true,
    "show_xp_level": true
  },
  "sound": {
    "master_volume": 1.0,
    "sfx_volume": 0.8,
    "music_volume": 0.5,
    "notifications_sound": true
  },
  "gameplay": {
    "auto_muck_losers": true,
    "show_hand_strength": true,
    "confirm_folds": false,
    "default_bet_size": "pot"
  }
}';
```

## Get/Update Settings
```javascript
async function getUserSettings(userId) {
  const { data } = await supabase
    .from('profiles')
    .select('settings')
    .eq('id', userId)
    .single();
  
  return data?.settings || DEFAULT_SETTINGS;
}

async function updateUserSettings(userId, updates) {
  const current = await getUserSettings(userId);
  const merged = deepMerge(current, updates);
  
  await supabase
    .from('profiles')
    .update({ settings: merged })
    .eq('id', userId);
  
  return merged;
}
```

## React Context
```javascript
const SettingsContext = createContext();

export function SettingsProvider({ children }) {
  const { session } = useAuth();
  const [settings, setSettings] = useState(DEFAULT_SETTINGS);
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    if (session?.user) {
      getUserSettings(session.user.id).then(s => {
        setSettings(s);
        setIsLoading(false);
      });
    }
  }, [session]);
  
  const updateSetting = async (path, value) => {
    const update = pathToObject(path, value);
    const newSettings = await updateUserSettings(session.user.id, update);
    setSettings(newSettings);
  };
  
  return (
    <SettingsContext.Provider value={{ settings, updateSetting, isLoading }}>
      {children}
    </SettingsContext.Provider>
  );
}

export const useSettings = () => useContext(SettingsContext);
```

## Settings Components
```jsx
function SettingsPage() {
  const { settings, updateSetting } = useSettings();
  
  return (
    <div className="settings-page">
      <SettingsSection title="Display">
        <ThemeToggle 
          value={settings.theme} 
          onChange={(v) => updateSetting('theme', v)} 
        />
        <LanguageSelect 
          value={settings.language} 
          onChange={(v) => updateSetting('language', v)} 
        />
      </SettingsSection>
      
      <SettingsSection title="Notifications">
        <ToggleSetting 
          label="Push Notifications"
          value={settings.notifications.push_enabled}
          onChange={(v) => updateSetting('notifications.push_enabled', v)}
        />
        <ToggleSetting 
          label="Email Notifications"
          value={settings.notifications.email_enabled}
          onChange={(v) => updateSetting('notifications.email_enabled', v)}
        />
      </SettingsSection>
      
      <SettingsSection title="Sound">
        <VolumeSlider 
          label="Master Volume"
          value={settings.sound.master_volume}
          onChange={(v) => updateSetting('sound.master_volume', v)}
        />
      </SettingsSection>
      
      <SettingsSection title="Privacy">
        <ToggleSetting 
          label="Public Profile"
          value={settings.privacy.profile_public}
          onChange={(v) => updateSetting('privacy.profile_public', v)}
        />
      </SettingsSection>
      
      <DangerZone>
        <DeleteAccountButton />
      </DangerZone>
    </div>
  );
}
```

## Account Management
```javascript
// Change password
async function changePassword(currentPassword, newPassword) {
  const { error } = await supabase.auth.updateUser({
    password: newPassword
  });
  if (error) throw error;
}

// Delete account
async function deleteAccount(userId) {
  // Archive data (don't actually delete for legal reasons)
  await supabase.from('profiles')
    .update({ 
      is_deleted: true, 
      deleted_at: new Date(),
      username: `deleted_${userId.slice(0, 8)}`,
      avatar_url: null
    })
    .eq('id', userId);
  
  await supabase.auth.signOut();
}
```
