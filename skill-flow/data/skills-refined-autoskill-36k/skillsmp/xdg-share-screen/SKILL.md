---
name: xdg-share-screen
description: Strategies for automating the XDG Desktop Portal "Share Screen" dialog
---

# XDG Share Screen Automation

This skill documents the strategies used in `automateLinux` to handle and automate the XDG Desktop Portal "Share Screen" dialog, which is common in modern Linux desktop environments (especially Wayland) for screen recording and sharing applications.

## The Challenge

The XDG Desktop Portal (`xdg-desktop-portal`) provides a sandboxed way for applications to request screen access. It presents a system dialog asking the user to select a screen or window to share. This dialog is security-critical and deliberately difficult to bypass automatedly without specific provisions (like restore tokens).

## Strategies

We employ two primary strategies to handle this dialog:

### 1. The "Clean" Way: Native Portal Handler with Restore Tokens

This is the preferred method for robust, invisible automation. It uses the DBus interface directly to request a session and manages `restore_token`s.

**Key Component:** `utilities/portal-handler/src/PortalManager.cpp`

**Mechanism:**
1.  **CreateSession**: The application requests a session from `org.freedesktop.portal.ScreenCast`.
2.  **Restore Token**: If a `restore_token` from a previous successful session is provided during creation, the portal **automatically grants access** without showing the popup, assuming the permission persistence policies allow it.
3.  **Persistence**: The application must save the `restore_token` returned by the portal after a successful `Start` call and use it for future sessions.

**Implementation Details:**
-   **DBus Interface**: `org.freedesktop.portal.ScreenCast`
-   **Token Storage**: Saved to `~/.config/automatelinux/portal/restore_token` (or similar, configured via flags).
-   **Fallback**: If the token is invalid, the handler clears it and falls back to requesting a new session (which triggers the popup).

### 2. The "Brute Force" Way: Input Simulation

This is the fallback method when native tokens act up or for applications that don't support them natively. It involves visually identifying the window and simulating user input to select the screen.

**Key Components:**
-   `utilities/autoSelectLoomScreen.py` (Python script)
-   `terminal/functions/loom.sh` -> `forceLoomShare` (Bash function)

**Mechanism:**
1.  **Detection**: Poll `listWindows` (daemon command) for a window titled "Share Screen" or with class `xdg-desktop-portal`.
2.  **Focus**: call `activateWindow` (daemon command) to bring the portal dialog to the front.
3.  **Navigation**: Send a sequence of keypresses via `simulateInput` (daemon command) to navigate the UI grid.
    -   **Sequence**: `SPACE` (Select default/first screen) -> `TAB` -> `TAB` -> `ENTER` (Click Share).
    -   *Note*: The sequence may vary by multiple factors (OS version, previous selection state). The script often spams `TAB` and `ENTER` to be robust ("Kitchen Sink" strategy).
4.  **Verification**: Continued polling to ensure the window closes (success) vs times out.

## Usage

### Using the Python Automator
The Python script is the most robust implementation of the simulate input method.

```bash
# Run in background to catch the popup when it appears
python3 utilities/autoSelectLoomScreen.py &
```

### Using the Bash Function
Quick manual trigger from the terminal.

```bash
source terminal/functions/loom.sh
forceLoomShare
```

## Troubleshooting

-   **Window Not Focusing**: System animations can delay window activation. The scripts include `sleep` delays to account for this.
-   **Wrong Key Sequence**: Different GNOME/GTK versions might have slightly different tab orders. `SPACE` usually selects the currently highlighted item (defaulting to the entire screen).
-   **"Kitchen Sink"**: If the clean sequence fails, the scripts may resort to spamming `TAB` and `ENTER`, which can have side effects if the window loses focus. Ensure the machine is idle during automation.
