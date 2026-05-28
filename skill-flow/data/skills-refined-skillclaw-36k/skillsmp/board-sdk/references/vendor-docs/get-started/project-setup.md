# Project Setup

Configure your Unity project for Board development.

## Platform Settings

### Switch to Android

1. Open **File > Build Settings** (Unity 6+: **File > Build Profiles**)
2. Select **Android** from the platform list
3. Click **Switch Platform**

### Configure Android Settings

Open **Edit > Project Settings > Player** and expand **Other Settings**.

**API Levels:**

- Set **Minimum API Level** to **Android 13.0 (API Level 33)**
- Set **Target API Level** to **Android 13.0 (API Level 33)**

**Scripting Backend:**

- Set **Scripting Backend** to **IL2CPP**
- Under **Target Architectures**, enable **ARM64** (disable ARMv7 and x86 options)

## Input System

Board requires Unity's Input System package.

### Enable the Input System

1. Open **Edit > Project Settings > Player**
2. Scroll to **Other Settings > Configuration**
3. Set **Active Input Handling** to **Input System Package (New)**
4. Click **Apply** when prompted to restart the editor

### Verify Input System Package

1. Open **Window > Package Manager**
2. Confirm **Input System** is installed (version 1.7.0 or higher)
3. If not installed, click **+** and search for "Input System"

## Board SDK Settings

The SDK requires configuration through settings assets before building.

### Configure Application ID

Your application needs a unique identifier for Board platform services including session management and save games.

1. In the Project window, navigate to **Assets > Board > Settings**
2. Select the **BoardGeneralSettings** asset
3. In the Inspector, enter your **Application ID**

The Application ID must be globally unique across all Board applications. We recommend using a UUID/GUID format:

```bash
550e8400-e29b-41d4-a716-446655440000
```

You can generate a UUID using online tools, or via command line:

```bash
# macOS/Linux
uuidgen

# Windows PowerShell
[guid]::NewGuid()
```

**Important:** The build will fail if the Application ID is empty. This ID is used by Board's platform services to identify your application for player sessions and save game data.

### Create BoardInputSettings

1. In the Project window, right-click in your Assets folder
2. Select **Create > Board > Input Settings**
3. Name the asset (e.g., "BoardInputSettings")

### Configure the Settings

Select your new BoardInputSettings asset and configure in the Inspector:

| Setting               | Description                                          |
| --------------------- | ---------------------------------------------------- |
| Glyph Model Filename  | Name of your Piece Set model file in StreamingAssets |
| Translation Smoothing | Smoothing applied to Piece position changes (0–1)    |
| Rotation Smoothing    | Smoothing applied to Piece rotation changes (0–1)    |
| Persistence           | How long Pieces remain tracked after losing contact  |

For detailed information on these parameters, see the **Touch Input** guide.

### Activate the Settings

Click **Make Active** in the Inspector to use this configuration.

Only one BoardInputSettings can be active at a time.

**Tip:** You can switch settings at runtime via `BoardInput.settings`. Changing settings resets all active contacts.

## Scene Setup

### Using BoardUIInputModule

Board's SDK blocks all system-level touch events to prevent conflicts with its own input handling. This means Unity's standard `InputSystemUIInputModule` will not receive touch input when running on Board hardware.

To enable UI interaction, use the SDK's input module:

1. Find your **EventSystem** GameObject in the scene hierarchy
2. Disable or remove the `InputSystemUIInputModule` component
3. Add a `BoardUIInputModule` component instead

**No EventSystem?** Unity automatically creates one when you add your first UI element (Button, Canvas, etc.).

BoardUIInputModule processes finger touches for UI while ignoring Piece contacts, preventing accidental button presses from Pieces.

**Editor Workflow:** Keep both modules in your scene. Enable InputSystemUIInputModule for Editor testing, then swap at runtime using `#if UNITY_ANDROID && !UNITY_EDITOR` to toggle which is active.

### Initializing the SDK

The Board SDK initializes automatically when your app starts. No explicit initialization call is required for basic input functionality.

For session management and save games, see:

- **Player Management**
- **Save Game System**

## Project Checklist

Before building, verify:

- ✓ Platform set to Android
- ✓ Minimum API Level: Android 13 (API 33)
- ✓ Scripting Backend: IL2CPP with ARM64
- ✓ Input System package installed and active
- ✓ Application ID configured in BoardGeneralSettings
- ✓ BoardInputSettings asset created and activated
- ✓ Piece Set model (.tflite) in StreamingAssets
- ✓ Model filename configured in BoardInputSettings

## Next Steps

- **Build & Deploy** - Build your project and deploy to Board
- **Sample Scene** - See working examples
- **Simulator** - Test input without hardware
