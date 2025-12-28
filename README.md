# FletMinesweeper app

A classic Minesweeper game built with Flet 0.80.0, featuring the nostalgic Windows 95/98 look with 3D borders and classic gameplay mechanics.

## Features

- **Classic UI**: Authentic Windows Minesweeper appearance with 3D borders
- **Multiple Grid Sizes**: 8x8, 16x16, 24x24, and 30x16 (Expert) modes
- **Flag System**: Right-click to place/remove flags
- **Flood Fill**: Automatic revealing of empty areas
- **Game State Indicators**: Smiley face button and counters
- **Win/Lose Dialogs**: Professional alert dialogs for game outcomes

## Requirements

- Python 3.9+
- Flet 0.80.0

## Installation

### Using uv (recommended)

```bash
# Install dependencies
uv sync

# Run as desktop app
uv run flet run

# Run as web app
uv run flet run --web
```

### Using Poetry

```bash
# Install dependencies
poetry install

# Run as desktop app
poetry run flet run

# Run as web app
poetry run flet run --web
```

### Using pip

```bash
# Install dependencies
pip install -r requirements.txt

# Run as desktop app
flet run

# Run as web app
flet run --web
```

## Build the app

### Android

```bash
flet build apk -v
```

### iOS

```bash
flet build ipa -v
```

### Web

```bash
flet build web -v
```

For more details on building and signing, refer to the [Flet Packaging Guide](https://flet.dev/docs/publish/).

## Flet 0.80.0 Migration Notes

This app has been updated to use Flet 0.80.0 with the following key changes:

- Updated `pyproject.toml` dependencies to `flet==0.80.0`
- Updated dialog handling to use `page.show_dialog()` and `page.pop_dialog()`
- Added type hints for better code clarity
- Enhanced event handling with modern Flet patterns
- Improved UI consistency with Flet 0.80.0 theming

## Game Controls

- **Left Click**: Reveal a cell
- **Right Click**: Place/remove flag
- **Menu**: Change grid size via the "Game" menu

## License

MIT License

### iOS

```
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://flet.dev/docs/publish/ios/).

### macOS

```
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://flet.dev/docs/publish/macos/).

### Linux

```
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://flet.dev/docs/publish/linux/).

### Windows

```
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).