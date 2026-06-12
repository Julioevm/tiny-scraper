# AGENTS.md — Tiny Scraper Development Guide

## Project Overview

**Tiny Scraper** is a Python-based utility that runs on **Anbernic RGXX handheld gaming devices** (stock firmware). It scrapes game cover art/screenshots from [ScreenScraper.fr](https://www.screenscraper.fr) and saves them alongside ROM files so the device's stock UI can display them.

The app uses **SDL2** for full-screen rendering and reads raw input from `/dev/input/event1` (the device's gamepad). It is **not** a desktop GUI app — it is designed exclusively for the constraints of embedded Linux on Anbernic hardware.

---

## Target Environment

- **Devices:** Anbernic RG35XX H, RG40XXV, RGcubexx, RG28XX (and potentially others)
- **OS:** Anbernic stock firmware (Linux-based, musl libc)
- **Python:** 3.12 (device ships with a bundled interpreter)
- **Available on device:** `python3`, `sdl2` (via `PYSDL2_DLL_PATH=/usr/lib`), `PIL` (Pillow), basic Linux utilities
- **NOT available on device:** `pip`, `uv`, compilers, heavy dev tooling
- **Architecture:** ARM (device-side); development happens on x86 Windows

### Device Filesystem Conventions

| Path | Purpose |
|---|---|
| `/mnt/mmc/Roms/` | SD1 (internal) ROM storage |
| `/mnt/sdcard/Roms/` | SD2 (external) ROM storage |
| `/mnt/vendor/oem/board.ini` | Board model identifier (first line) |
| `/mnt/vendor/oem/language.ini` | System language index |
| `/sys/class/extcon/hdmi/state` | HDMI connection state |
| `/dev/input/event1` | Gamepad input device |
| `/mnt/vendor/bin/default.ttf` | System font |
| `/mnt/mod/ctrl/volumeCtrl.dge` | Optional volume control daemon |

---

## Architecture

```
tiny-scraper.sh          # Entry point — runs on device via App Center
├── tiny_scraper/
│   ├── main.py          # Bootstraps SDL2, detects hardware, launches app
│   ├── app.py           # Main application loop & UI screens
│   ├── graphic.py       # SDL2 rendering layer (PIL → SDL2 surface blitting)
│   ├── input.py         # Raw gamepad input from /dev/input/event1
│   ├── scraper.py       # ScreenScraper.fr API client + CRC32 calculation
│   ├── anbernic.py      # Device-specific: SD card paths, storage switching
│   ├── systems.py       # ROM system definitions (names, IDs, file extensions)
│   ├── language.py      # i18n translator (JSON-based)
│   ├── config.json      # User config (ScreenScraper credentials, media type, region)
│   ├── lang/            # Translation files (en_US, ja_JP, zh_CN)
│   ├── font/            # Bundled font (font.ttf)
│   └── sdl2.zip         # Bundled SDL2 Python module (extracted on first run)
```

### Key Design Decisions

- **Singleton UI:** `UserInterface` uses `__new__` singleton pattern — only one instance ever exists.
- **Polling loop:** `main()` calls `app.update()` in an infinite `while True` loop. Each iteration reads input and redraws the active screen.
- **PIL for drawing, SDL2 for display:** All shapes and text are drawn onto a PIL `Image`, then blitted to the SDL2 renderer as an RGBA surface. This is done every frame.
- **No async:** Everything is synchronous. Long operations (scraping, bulk downloads) block the UI and show progress via `draw_log` overlays.
- **Hardware detection:** `hw_info` (from `board.ini`) controls screen resolution. `hdmi_info` controls whether the image is rotated 90° (for the RG28XX's portrait screen).

---

## Dependencies

| Package | Version | Notes |
|---|---|---|
| `requests` | 2.32.3 | Listed in requirements.txt but **not imported** — `scraper.py` uses `urllib.request` instead. Consider removing from deps. |
| `Pillow` (PIL) | — | Used for image rendering and optional resize. Must be available on device. |
| `pysdl2` (sdl2) | — | SDL2 bindings. Bundled in `sdl2.zip` and extracted on first run. |
| `ruff` | ≥0.9.6 | Dev dependency (linter/formatter) |

> **Note:** `pyproject.toml` only lists `requests` as a runtime dependency, but the app also requires `Pillow` and `sdl2` at runtime. The device firmware is expected to provide these pre-installed.

---

## Input System

Input is read as raw 24-byte `struct` events from `/dev/input/event1`:

```c
struct input_event {
    long tv_sec;    // 8 bytes
    long tv_usec;   // 8 bytes
    unsigned short type;   // 2 bytes
    unsigned short code;   // 2 bytes
    unsigned int value;    // 4 bytes
};
```

**Button mapping** (`input.py`):

| Code | Button | Action |
|---|---|---|
| 304 | A | Select / Download |
| 305 | B | Back |
| 306 | Y | Switch SD card |
| 307 | X | — |
| 308/309 | L1/R1 | Page up/down (by `max_elem`) |
| 314/315 | L2/R2 | Fast scroll (±100) |
| 311 | START | Download all (bulk scrape) |
| 312 | MENUF | Exit app |
| 17 | DY | D-pad up/down (`value=1` down, `value=-1` up) |

---

## UI Screens

1. **Console Menu** (`load_console_menu`) — Lists all systems that have ROMs. Shows missing media count per system. Buttons: A=select, Y=switch SD, M=exit.
2. **ROMs Menu** (`load_roms_menu`) — Lists ROMs missing media for the selected system. Buttons: A=scrape one, Start=scrape all, B=back, M=exit.

---

## Configuration (`config.json`)

```json
{
    "user": "screenscraper_username",
    "password": "screenscraper_password",
    "media_type": "sstitle",
    "region": "wor",
    "resize": false
}
```

- **media_type:** `ss` (screenshot), `sstitle` (title screen), `box-2D`, `box-3D`, `mixrbv1`, `mixrbv2`, etc.
- **region:** `wor`, `jp`, `eu`, `asi`, `kr`, `ss`, `us`
- **resize:** When `true`, images are downscaled to 320×240 using `Image.LANCZOS`

---

## Screen Resolutions

Determined by `hw_info` from board detection (`graphic.py`):

| `hw_info` | Device | Resolution | Max visible items |
|---|---|---|---|
| 1 | RGcubexx | 720×720 | 18 |
| 2 | RG34xx | 720×480 | 11 |
| 3 | RG28xx | 640×480 (rotated 90°) | 11 |
| 4 | RG35xx+ | 640×480 | 11 |
| 5 | RG35xxH (default) | 640×480 | 11 |
| 6 | RG35xxSP | 640×480 | 11 |
| 7 | RG40xxH | 640×480 | 11 |
| 8 | RG40xxV | 640×480 | 11 |
| 9 | RG35xxPRO | 640×480 | 11 |

---

## ScreenScraper API

- **Endpoint:** `https://api.screenscraper.fr/api2/jeuInfos.php`
- **Auth:** Dev credentials are base64-encoded in `scraper.py` (`devid`/`devpassword`). User credentials come from `config.json`.
- **Lookup strategy:** CRC32 hash + game name + system ID → API returns game metadata with media URLs.
- **SSL:** Hostname verification is **disabled** (`ctx.check_hostname = False`, `ctx.verify_mode = ssl.CERT_NONE`). This is likely needed for the device's older CA certificates.
- **Media selection priority:** Preferred region → `wor` (world) → first available.

---

## Development Guidelines

### Running Locally

The app **cannot run fully on a desktop** — it requires SDL2, `/dev/input/event1`, and Anbernic filesystem paths. For testing logic:

- `scraper.py` and `systems.py` can be unit-tested independently (pure Python).
- `graphic.py` and `input.py` require the device environment.
- `main.py` will fall back to `board_info='RG35xxH'` and `lang_info=2` when device files are missing.

### Coding Style

- Python 3.12+ (uses `match` / type hints / walrus operator `:=`)
- Dev dependency: `ruff` for linting/formatting
- Line endings: LF only (enforced via `.gitattributes`)

### Releasing

1. Tag-based: push a `v*` tag → GitHub Actions builds `tiny-scraper.zip` and creates a Release.
2. Manual: run `release.sh` (Linux/macOS) or `release.ps1` (Windows PowerShell) to create the zip locally.
3. The zip bundles: `tiny-scraper.sh`, `tiny_scraper/`, `Imgs/`, `README.md`.

```bash
git tag v1.x.x
git push origin v1.x.x
```

### Things to Keep in Mind

- **No heavy dependencies.** The device has limited CPU/RAM. Avoid adding packages that are large or slow to import.
- **No pip on device.** Any new runtime dependency must be pre-bundled or already available on the stock firmware.
- **Blocking I/O is expected.** There is no event loop or threading. Network calls freeze the UI (the "Scraping..." overlay is the only feedback).
- **File system paths are hardcoded.** All device paths (`/mnt/mmc`, `/mnt/sdcard`, etc.) are Linux-specific absolute paths.
- **Logs go to `log.txt`.** The shell script redirects all stdout/stderr to `tiny_scraper/log.txt`. Use `print()` for logging — it all ends up there.
- **Gamepad only.** There is no keyboard, mouse, or touchscreen input. All interaction is via the mapped buttons.
