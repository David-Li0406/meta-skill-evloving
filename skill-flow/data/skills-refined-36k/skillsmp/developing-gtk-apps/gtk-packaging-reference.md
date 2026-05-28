# GTK Packaging Reference

Desktop files, AppStream metadata, Meson build, and Flatpak packaging for GTK 4/libadwaita apps.

## Desktop File (com.example.MyApp.desktop)

```ini
[Desktop Entry]
Name=My App
Comment=Does something useful
Exec=myapp
Icon=com.example.MyApp
Terminal=false
Type=Application
Categories=Utility;
StartupNotify=true
```

## AppStream Metadata (com.example.MyApp.metainfo.xml)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
  <id>com.example.MyApp</id>
  <name>My App</name>
  <summary>Does something useful</summary>
  <metadata_license>CC0-1.0</metadata_license>
  <project_license>GPL-3.0-or-later</project_license>
  <description>
    <p>Longer description of the app.</p>
  </description>
  <launchable type="desktop-id">com.example.MyApp.desktop</launchable>
  <url type="homepage">https://example.com</url>
  <content_rating type="oars-1.1"/>
  <releases>
    <release version="1.0.0" date="2024-01-01"/>
  </releases>
</component>
```

## Meson Build (meson.build)

```meson
project('myapp', version: '1.0.0')

python = import('python')
py_installation = python.find_installation('python3')

# Install Python files
install_subdir('myapp', install_dir: py_installation.get_install_dir())

# Install data files
install_data('data/com.example.MyApp.desktop',
  install_dir: get_option('datadir') / 'applications')
install_data('data/com.example.MyApp.metainfo.xml',
  install_dir: get_option('datadir') / 'metainfo')

# Compile schemas
gnome = import('gnome')
gnome.compile_schemas(build_by_default: true)
```

## Flatpak Manifest (com.example.MyApp.json)

```json
{
    "app-id": "com.example.MyApp",
    "runtime": "org.gnome.Platform",
    "runtime-version": "47",
    "sdk": "org.gnome.Sdk",
    "command": "myapp",
    "finish-args": [
        "--share=ipc",
        "--socket=fallback-x11",
        "--socket=wayland",
        "--device=dri"
    ],
    "cleanup": [
        "/include",
        "/lib/pkgconfig",
        "*.a",
        "*.la"
    ],
    "modules": [
        {
            "name": "myapp",
            "buildsystem": "meson",
            "sources": [
                {
                    "type": "dir",
                    "path": "."
                }
            ]
        }
    ]
}
```

## Common Flatpak Permissions

| Permission | Arg | When Needed |
|------------|-----|-------------|
| Network access | `--share=network` | API calls, downloads |
| Home folder | `--filesystem=home` | User files (prefer portals) |
| Host files | `--filesystem=host` | File manager apps |
| Notifications | `--talk-name=org.freedesktop.Notifications` | System notifications |
| Secrets | `--talk-name=org.freedesktop.secrets` | Keyring access |
| Background | `--talk-name=org.freedesktop.portal.Background` | Background services |

## Build and Run Locally

```bash
# Build
flatpak-builder --user --install --force-clean build-dir com.example.MyApp.json

# Run
flatpak run com.example.MyApp

# Export bundle
flatpak build-bundle ~/.local/share/flatpak/repo myapp.flatpak com.example.MyApp
```

## Python Dependencies in Flatpak

For apps with Python dependencies, add pip modules:

```json
{
    "modules": [
        {
            "name": "python-requests",
            "buildsystem": "simple",
            "build-commands": [
                "pip3 install --prefix=/app --no-deps ."
            ],
            "sources": [
                {
                    "type": "archive",
                    "url": "https://files.pythonhosted.org/packages/.../requests-2.31.0.tar.gz",
                    "sha256": "..."
                }
            ]
        },
        {
            "name": "myapp",
            "buildsystem": "meson",
            "sources": [
                {
                    "type": "dir",
                    "path": "."
                }
            ]
        }
    ]
}
```

Or use `flatpak-pip-generator` to generate module definitions:

```bash
# Generate module for requests and dependencies
flatpak-pip-generator requests
# Creates python3-requests.json to include in manifest
```

## Icons

Install app icon at multiple sizes:

```meson
# data/meson.build
icon_sizes = ['16', '32', '48', '64', '128', '256', '512']

foreach size : icon_sizes
  install_data(
    'icons/hicolor/@0@x@0@/apps/com.example.MyApp.png'.format(size),
    install_dir: get_option('datadir') / 'icons' / 'hicolor' / '@0@x@0@'.format(size) / 'apps'
  )
endforeach

# Symbolic icon
install_data(
  'icons/hicolor/symbolic/apps/com.example.MyApp-symbolic.svg',
  install_dir: get_option('datadir') / 'icons' / 'hicolor' / 'symbolic' / 'apps'
)
```

## GSettings Schema Installation

```meson
# data/meson.build
install_data(
  'com.example.MyApp.gschema.xml',
  install_dir: get_option('datadir') / 'glib-2.0' / 'schemas'
)

gnome.post_install(glib_compile_schemas: true)
```

## Complete data/meson.build

```meson
# data/meson.build

# Desktop file
desktop_file = i18n.merge_file(
  input: 'com.example.MyApp.desktop.in',
  output: 'com.example.MyApp.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: get_option('datadir') / 'applications'
)

# Validate desktop file
desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('validate-desktop', desktop_utils, args: [desktop_file])
endif

# AppStream metadata
metainfo_file = i18n.merge_file(
  input: 'com.example.MyApp.metainfo.xml.in',
  output: 'com.example.MyApp.metainfo.xml',
  po_dir: '../po',
  install: true,
  install_dir: get_option('datadir') / 'metainfo'
)

# Validate AppStream
appstreamcli = find_program('appstreamcli', required: false)
if appstreamcli.found()
  test('validate-metainfo', appstreamcli, args: ['validate', '--no-net', metainfo_file])
endif

# GSettings schema
install_data(
  'com.example.MyApp.gschema.xml',
  install_dir: get_option('datadir') / 'glib-2.0' / 'schemas'
)

# DBus service (if needed)
install_data(
  'com.example.MyApp.service',
  install_dir: get_option('datadir') / 'dbus-1' / 'services'
)
```
