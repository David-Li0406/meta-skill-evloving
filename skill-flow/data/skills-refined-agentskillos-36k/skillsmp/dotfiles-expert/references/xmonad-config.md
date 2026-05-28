# XMonad Configuration Reference

XMonad window manager configuration for this repository.

## Configuration Location

- **NixOS**: `roles/desktop-plasma/default.nix` enables xmonad
- **Home Manager**: `roles/home-manager/window-manager/xmonad/`
  - `default.nix` - Home-manager module
  - `xmonad.hs` - XMonad configuration

## Key Files

### roles/home-manager/window-manager/xmonad/default.nix
```nix
{ pkgs, config, lib, ... }:
{
  imports = [ ../shared/xmobar ];
  
  home.keyboard = null;
  
  xsession = {
    enable = true;
    windowManager.xmonad = {
      enableContribAndExtras = true;
      extraPackages = hp: [
        hp.xmonad-contrib
        hp.xmonad-extras
        hp.xmonad
      ];
      config = ./xmonad.hs;
    };
  };
  
  home.file.".xmonad/xmonad.hs".source = ./xmonad.hs;
}
```

## XMonad.hs Structure

### Core Settings
```haskell
myModMask :: KeyMask
myModMask = mod4Mask       -- Super/Windows key

myTerminal :: String
myTerminal = "alacritty"

myBrowser :: String
myBrowser = "firefox -P noscratchpad"

myBorderWidth :: Dimension
myBorderWidth = 1

myNormColor :: String
myNormColor   = "#292d3e"

myFocusColor :: String
myFocusColor  = "#bbc5ff"
```

### Workspaces
```haskell
myWorkspaces :: [String]
myWorkspaces = fmap xmobarEscape
  ["dev", "dev_two", "chat", "www", "sys", "mon"]

-- Dynamic projects with directory/startup hooks
projects :: [Project]
projects =
  [ Project { projectName = "dev"
            , projectDirectory = "~/"
            , projectStartHook = Nothing }
  -- ...
  ]
```

### Layouts
```haskell
myLayoutHook = showWorkspaceName
             $ fullscreenFloat
             $ fullScreenToggle
             $ fullBarToggle
             $ mirrorToggle
             $ reflectToggle
             $ flex ||| tabs ||| stacks ||| threeCol

-- Layout definitions
flex = trimNamed 5 "Flex"
     $ avoidStruts
     $ windowNavigation
     $ addTabs shrinkText myTabTheme
     $ subLayout [] (Simplest ||| Accordion)
     $ ifWider smallMonResWidth wideLayouts standardLayouts

tabs = named "Tabs"
     $ avoidStruts
     $ addTopBar
     $ addTabs shrinkText myTabTheme
     $ Simplest

stacks = named "Stacks"
       $ avoidStruts
       $ addTopBar
       $ myGaps
       $ mySpacing
       $ Tall 2 (3/100) (1/2)
```

### Scratchpads
```haskell
myScratchpads :: [NamedScratchpad]
myScratchpads =
  [ NS "term" spawnTerm findTerm manageTerm
  , NS "fox" spawnFox findFox manageFox
  , NS "obs" spawnObs findObs manageObs
  ]
  where
    spawnTerm = myTerminal ++ " -t scratchpad"
    findTerm = title =? "scratchpad"
    manageTerm = customFloating $ W.RationalRect l t w h
      where h = 5/6; w = 4/6; t = 0.08; l = 0.315
    
    spawnFox = "firefox -P scratchpad --class foxpad"
    findFox = className =? "foxpad"
    -- ...
```

## Key Bindings

### Window Management
| Key | Action |
|-----|--------|
| `M-<Return>` | Open terminal |
| `M-b` | Open browser |
| `M-<Space>` | Shell prompt |
| `M-<Backspace>` | Kill focused window |
| `M-S-<Backspace>` | Kill all windows |
| `M-<Delete>` | Push floating to tile |
| `M-S-<Delete>` | Sink all floating |

### Navigation
| Key | Action |
|-----|--------|
| `M-m` | Focus master |
| `M-j` | Focus next window |
| `M-k` | Focus previous window |
| `M-S-j` | Swap with next |
| `M-S-k` | Swap with previous |
| `M-S-.` | Promote to master |

### Layouts
| Key | Action |
|-----|--------|
| `M-<Tab>` | Next layout |
| `M-S-<Space>` | Toggle struts |
| `M-S-n` | Toggle no borders |
| `C-,` | Shrink horizontal |
| `C-.` | Expand horizontal |
| `M-C-j` | Shrink vertical |
| `M-C-k` | Expand vertical |

### Scratchpads
| Key | Action |
|-----|--------|
| `M-S-x` | Terminal scratchpad |
| `M-x` | Firefox scratchpad |
| `M-o` | Obsidian scratchpad |

### Grid Select
| Key | Action |
|-----|--------|
| `C-g g` | Grid select apps |
| `C-g t` | Go to selected window |
| `C-g b` | Bring selected window |

### Search Prompts
| Key | Action |
|-----|--------|
| `M-s a` | Arch wiki |
| `M-s d` | DuckDuckGo |
| `M-s g` | Google |
| `M-s h` | Hoogle |
| `M-s y` | YouTube |

## XMobar Configuration

Located at `roles/home-manager/window-manager/shared/xmobar/default.nix`:

```nix
programs.xmobar = {
  enable = true;
  extraConfig = ''
    Config { font = "xft:Ubuntu:weight=bold:pixelsize=11"
           , bgColor = "#292d3e"
           , fgColor = "#f07178"
           , position = TopSize L 100 24
           , commands = [
               Run Date "%b %d %Y (%H:%M)" "date" 50
             , Run Cpu ["-t", "cpu: (<total>%)","-H","50","--high","red"] 20
             , Run Memory ["-t", "mem: <used>M (<usedratio>%)"] 20
             , Run DiskU [("/", "hdd: <free> free")] [] 60
             , Run Battery ["BAT0"] 10
             , Run UnsafeStdinReader
             ]
           , template = "... %UnsafeStdinReader% ... %cpu% ... %memory% ... %date%"
           }
  '';
};
```

## Themes

### Solarized Colors
```haskell
base03  = "#002b36"
base02  = "#073642"
base01  = "#586e75"
base00  = "#657b83"
base0   = "#839496"
base1   = "#93a1a1"
base2   = "#eee8d5"
base3   = "#fdf6e3"
yellow  = "#b58900"
orange  = "#cb4b16"
red     = "#dc322f"
magenta = "#d33682"
violet  = "#6c71c4"
blue    = "#268bd2"
cyan    = "#2aa198"
green   = "#859900"

active      = blue
activeWarn  = red
inactive    = base02
focusColor  = blue
unfocusColor = base02
```

### Tab Theme
```haskell
myTabTheme = def
  { fontName          = myFont
  , activeColor       = active
  , inactiveColor     = base02
  , activeBorderColor = active
  , inactiveBorderColor = base02
  , activeTextColor   = base03
  , inactiveTextColor = base00
  }
```

## Adding Custom Key Bindings

Add to `myKeys` list in xmonad.hs:

```haskell
myKeys :: [(String, X ())]
myKeys =
  [ -- ... existing bindings
  
  -- Custom binding
  , ("M-p", spawn "my-command")
  
  -- With modifier combinations
  , ("M-S-p", spawn "another-command")
  , ("M-C-p", spawn "yet-another")
  
  -- Media keys
  , ("<XF86AudioPlay>", spawn "playerctl play-pause")
  ]
```

## Adding New Layouts

```haskell
-- In myLayoutHook, add to the layout chain:
myLayoutHook = ...
             $ flex ||| tabs ||| stacks ||| threeCol ||| myNewLayout

-- Define the layout:
myNewLayout = named "MyLayout"
            $ avoidStruts
            $ myGaps
            $ mySpacing
            $ ThreeColMid 1 (1/20) (1/2)  -- or any layout combinator
```

## Startup Hook

```haskell
myStartupHook :: X ()
myStartupHook = do
  spawnOnce "nitrogen --restore &"     -- Wallpaper
  spawnOnce "picom &"                  -- Compositor
  spawnOnce "nm-applet &"              -- Network applet
  spawnOnce "volumeicon &"             -- Volume icon
  setWMName "LG3D"                     -- Java compatibility
```

## Manage Hook

```haskell
myManageHook :: ManageHook
myManageHook =
      manageDocks                              -- Dock/panel handling
  <+> namedScratchpadManageHook myScratchpads  -- Scratchpads
  <+> fullscreenManageHook                     -- Fullscreen windows
  <+> manageSpawn                              -- spawnOn support
```

## Recompiling

After modifying xmonad.hs:
```bash
# Via home-manager
./hm-apply.sh

# Or manually
xmonad --recompile
xmonad --restart  # M-S-r from within xmonad
```
