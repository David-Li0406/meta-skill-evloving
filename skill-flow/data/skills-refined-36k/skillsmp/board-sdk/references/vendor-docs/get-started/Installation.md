# Installation

Install the Board Unity SDK in your Unity project.

## Developer Access

The Board SDK and deployment tools are provided separately to developers in the program. If you don't have access yet, request access here.

Once approved, you'll receive:

- **Board SDK** - Unity package (.tgz) for touch input, session management, save games, and pause screen integration
- **Board Developer Bridge (BDB)** - Command-line tool for deploying to Board hardware
- **Piece Set Models** - Machine learning models (.tflite) for Piece recognition

## Prerequisites

Before installing the SDK:

- Unity 2022.3 LTS or later (Unity 6 also supported)
- Android Build Support module installed via Unity Hub
- Unity Input System package (1.7.0+)

**Windows Users:** You may need to run Unity as Administrator for the first build if you encounter "SDK directory is not writable" errors.

## Create a New Unity Project

If starting fresh:

1. Open Unity Hub and click **New Project**
2. Select a template (2D or 3D, both work with Board)
3. For render pipeline, use **Universal Render Pipeline (URP)** for best performance on Board hardware

**Note:** The High Definition Render Pipeline (HDRP) is not compatible with Board's hardware.

## Install the SDK

### Step 1: Open Package Manager

In Unity, select **Window > Package Manager** from the menu bar.

### Step 2: Add Package from Tarball

Click the **+** button in the top-left of the Package Manager window and select **Add package from tarball…**.

### Step 3: Select the SDK Package

Navigate to your downloaded SDK file (the .tgz file you received) and click **Open**.

The package will install as "Board SDK" in your project.

## Install Piece Set Models

The SDK requires a Piece Set model to recognize Pieces on Board. These machine learning models are provided separately and determine which Pieces your game can detect.

### Step 1: Create StreamingAssets Folder

In your Unity project, create a folder at `Assets/StreamingAssets` if it doesn't exist.

### Step 2: Add the Model File

Copy the Piece Set model file (with .tflite extension) into `Assets/StreamingAssets`.

**Note:** Each model corresponds to a specific Piece Set (e.g., Arcade, Mushka, etc). You select which set to use when configuring the SDK.

## Install Board Developer Bridge

Board Developer Bridge (BDB) is a command-line tool for deploying your builds to Board hardware.

### macOS

1. Download the `bdb` binary from your developer package
2. Move it to a directory in your PATH (e.g., `/usr/local/bin`)
3. Make it executable: `chmod +x /usr/local/bin/bdb`
4. Verify installation by running `bdb help`

### Windows

1. Download the `bdb.exe` binary from your developer package
2. Add its directory to your system PATH, or place it in a directory already in PATH
3. Verify installation

## Verify Installation

Open a terminal and run:

```bash
bdb help
```

You should see the bdb help output listing available commands.

To confirm the SDK installed correctly:

1. Open **Window > Package Manager**
2. Find "Board SDK" in the list of installed packages
3. Check that the version matches what you downloaded

The SDK package includes:

- Runtime libraries for Board input, sessions, and save games
- Editor tools including the Simulator
- Sample scenes demonstrating SDK features

## Next Steps

- **Project Setup** - Configure Unity for Board platform
- **Build & Deploy** - Build and run on Board hardware
