# Promptly — Smart Reminder Assistant

> **Never miss a moment.** Promptly lives quietly in your Windows system tray and fires native notifications exactly when you need them — for one-time meetings, repeating check-ins, or daily routines.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Screenshots & UI Guide](#screenshots--ui-guide)
4. [System Requirements](#system-requirements)
5. [Quick Start (Run from Source)](#quick-start-run-from-source)
6. [Building Promptly.exe](#building-promptlyexe)
7. [File Structure](#file-structure)
8. [How Reminders Work](#how-reminders-work)
9. [Data Storage](#data-storage)
10. [Reminder Types Reference](#reminder-types-reference)
11. [Theme System](#theme-system)
12. [Architecture](#architecture)
13. [Troubleshooting](#troubleshooting)
14. [Uninstalling](#uninstalling)
15. [Changelog](#changelog)

---

## Overview

Promptly is a **single-file, offline Windows tray assistant** written in Python. It sits in the notification area (system tray) and uses Windows native toast notifications to alert you on schedule. There is no cloud, no login, no telemetry — all data stays in a single `data.json` file on your machine.

| Property | Value |
|---|---|
| Platform | Windows 10 / 11 (64-bit) |
| Python version | 3.11 or higher |
| UI framework | PyQt6 (Qt 6.4+) |
| Notifications | Windows Toast (WinRT) with Qt balloon fallback |
| Data | `data.json` (plain JSON, human-readable) |
| Distribution | Single `Promptly.exe` — no installer, no Python needed |

---

## Features

### Core Scheduling
- **Three reminder modes** — One Time, Interval, and Daily (see [Reminder Types](#reminder-types-reference))
- **Deterministic scheduler** — uses a `heapq` priority queue + `QTimer`. Zero polling loops. CPU usage is ~0% at idle.
- **Crash recovery** — on restart, Promptly recalculates overdue reminders and reschedules them correctly. No reminders are silently dropped.
- **System sleep / clock-change safe** — the scheduler re-arms itself after wake or DST transitions.
- **Duplicate-fire guard** — a 10-second window prevents the same reminder from firing twice.

### Reminders
- Title (required), notes, contact name, and contact info per reminder
- Pause or resume individual reminders without deleting them
- Global pause / resume for all notifications at once (tray menu)
- Edit any reminder at any time; reschedules automatically
- One-time reminders auto-complete after firing

### User Interface
- **Dashboard window** — full list of all reminders with search and filter
- **Stats strip** — live counts of Active, Interval, Daily, and Done reminders
- **Filter** — All / Active / Paused / Completed
- **Search** — searches across title, notes, contact name, and contact info simultaneously
- **Colour-coded left bar** on each card (teal = one-time, purple = interval, green = daily, amber = paused, grey = done)
- **Dark mode & Light mode** — toggle with one click; persists for the session
- **Tray icon states** — blue (active), amber (paused)
- Double-click tray icon to open dashboard
- Right-click tray icon for quick menu

### Reliability
- **Atomic JSON writes** — saves to `.tmp` then `os.replace()`. A crash mid-save never corrupts your data.
- **Corrupted file quarantine** — if `data.json` is unreadable, it is renamed to `data.json.corrupted_TIMESTAMP` and Promptly starts fresh.
- **Schema validation** — every field from disk is validated and sanitised before use.
- **UUID4 reminder IDs** — unique, collision-proof, human-inspectable in JSON.

---

## Screenshots & UI Guide

```
┌─────────────────────────────────────────────────────────────────────┐
│  PROMPTLY          Smart Reminders · Never Miss a Moment            │
│                                            ● Active  ☀ Light  ＋ Add│
├─────────────────────────────────────────────────────────────────────┤
│  4 Active   2 Interval   1 Daily   1 Done                           │
├─────────────────────────────────────────────────────────────────────┤
│  All Reminders ▾   🔍 Search...                          8 reminders│
├─────────────────────────────────────────────────────────────────────┤
│ ┃ Weekly Team Sync            [Interval]                      ⏸ ✎ ✕ │
│   🕐  Mon, 02 Jun 2025  ·  09:00 AM      👤  Arjun Mehta           │
│   Discuss sprint progress and blockers                              │
│                                                                     │
│ ┃ Doctor Appointment          [One Time]                      ⏸ ✎ ✕ │
│   🕐  Fri, 06 Jun 2025  ·  02:30 PM      👤  Dr. Sharma            │
│   Bring blood test results                                          │
├─────────────────────────────────────────────────────────────────────┤
│ Promptly running  ·  6 active reminders              v1.0  Enterprise│
└─────────────────────────────────────────────────────────────────────┘
```

### Tray Icon Menu
Right-click the tray icon (bell with lightning bolt) for:
- **Open Promptly** — open the dashboard
- **Add Reminder** — jump straight to the new reminder form
- **Pause / Resume Notifications** — globally mute all alerts
- **Exit Promptly** — saves data and quits cleanly

### Add / Edit Reminder Form
| Field | Required | Notes |
|---|---|---|
| Reminder Title | ✅ Yes | Up to 200 characters |
| Notes | No | Up to 2,000 characters |
| Contact Name | No | Up to 100 characters |
| Contact Info | No | Phone or email, up to 200 characters |
| Reminder Type | ✅ Yes | One Time / Interval / Daily |
| Date & Time | Conditional | Shown for One Time and Daily types |
| Repeat Every | Conditional | Shown for Interval type only (1–43,200 minutes) |

---

## System Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| OS | Windows 10 (1903+) | Windows 11 |
| Python | 3.11 | 3.12 |
| RAM | 80 MB | — |
| Disk | 30 MB (exe) + tiny data.json | — |
| System Tray | Must be available | — |
| Notifications | Windows Action Center enabled | Focus Assist off |

> **Note:** To run from source, Python 3.11+ is required. The compiled `Promptly.exe` does not require Python to be installed on the target machine.

---

## Quick Start (Run from Source)

### 1. Clone or download the project

```
Promptly/
├── Promptly.py        ← main source file (entire app)
├── Promptly.ico       ← multi-resolution icon (embedded in .py too)
├── Promptly.spec      ← PyInstaller build spec
├── requirements.txt   ← pip dependencies
└── README.md          ← this file
```

### 2. Create a virtual environment (recommended)

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```cmd
pip install -r requirements.txt
```

Or manually:

```cmd
pip install PyQt6>=6.4.0 windows-toasts>=1.0.0
```

### 4. Run

```cmd
python Promptly.py
```

Promptly starts silently. Look for the bell icon in your system tray (you may need to expand hidden icons with the `^` arrow in the taskbar corner).

---

## Building Promptly.exe

The included `Promptly.spec` produces a **single, self-contained executable** using PyInstaller. No Python installation is needed on the target PC.

### Install PyInstaller

```cmd
pip install pyinstaller>=5.13.0
```

### Build

```cmd
pyinstaller Promptly.spec
```

Output: `dist\Promptly.exe`

### What the build produces
- `dist\Promptly.exe` — ~30–50 MB standalone executable
- The `.ico` file is embedded inside the `.py` source as base64, so **no separate icon file is needed at runtime**
- `Promptly.exe` creates only `data.json` in the same folder as itself — nothing else

### Optional: Add to Windows Startup

To launch Promptly automatically when you log in:

1. Press `Win + R`, type `shell:startup`, press Enter
2. Create a shortcut to `Promptly.exe` in the Startup folder

Or via PowerShell:
```powershell
$exe = "C:\Path\To\Promptly.exe"
$wsh = New-Object -ComObject WScript.Shell
$lnk = $wsh.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\Promptly.lnk")
$lnk.TargetPath = $exe
$lnk.Save()
```

### Optional: Code-sign the .exe

PyInstaller executables may trigger antivirus false positives because of the way they bundle Python. To suppress this:
1. Obtain a code-signing certificate (e.g., from DigiCert or Sectigo)
2. Sign with: `signtool sign /fd SHA256 /tr http://timestamp.digicert.com dist\Promptly.exe`
3. Or add an exclusion in Windows Defender / your AV for the `dist\` folder

---

## File Structure

```
project/
├── Promptly.py          Application source (entire app in one file)
├── Promptly.ico         Multi-resolution icon: 16, 24, 32, 48, 64, 128, 256 px
├── Promptly.spec        PyInstaller build configuration
├── requirements.txt     Pip dependencies
├── README.md            This file
│
└── dist/                Created by PyInstaller
    └── Promptly.exe     Standalone executable
```

**Runtime files created by Promptly:**

```
(same folder as Promptly.exe or Promptly.py)
├── data.json            All your reminders (auto-created on first run)
└── data.json.tmp        Temporary write file (auto-deleted after each save)
```

If `data.json` becomes corrupted, Promptly renames it:
```
data.json.corrupted_20250602_143022
```
and starts fresh. Your corrupted file is preserved for manual inspection or recovery.

---

## How Reminders Work

### Lifecycle of a Reminder

```
Created → Scheduled → [Paused ↔ Resumed] → Triggered → [Re-scheduled or Completed]
```

1. **Creation** — you fill in the form and click Save. Promptly computes `next_trigger_utc` immediately and saves to `data.json`.
2. **Scheduling** — the scheduler engine inserts the reminder into a `heapq` priority queue keyed by `next_trigger_utc`. A single `QTimer` is armed to fire at exactly the right millisecond — no polling.
3. **Triggering** — when the timer fires, Promptly sends a Windows toast notification (or Qt balloon fallback). For One Time reminders, status is set to `completed`. For Interval/Daily, `next_trigger_utc` is recalculated and the reminder is re-queued.
4. **Crash recovery** — on next launch, Promptly loads all tasks, identifies any whose `next_trigger_utc` is in the past, fires once immediately (if Interval/Daily), then reschedules correctly going forward.

### Global Pause

When you pause Promptly (tray menu → Pause Notifications):
- The `QTimer` is stopped — no callbacks fire
- Individual task schedules are preserved in memory
- All `next_trigger_utc` values remain intact
- Resume re-arms the timer from the current time forward

---

## Data Storage

Reminders are stored in `data.json` — a plain UTF-8 JSON file located next to the executable. You can back it up, copy it between machines, or inspect it in any text editor.

### File format

```json
{
  "schema_version": 1,
  "app": "Promptly",
  "saved_utc": "2025-06-02T09:31:00.123456+00:00",
  "tasks": [
    {
      "id": "a3f2c1d4-...",
      "title": "Weekly Team Sync",
      "notes": "Discuss sprint progress",
      "contact_name": "Arjun Mehta",
      "contact_info": "arjun@company.com",
      "reminder_type": "interval",
      "interval_minutes": 10080,
      "scheduled_time": "2025-06-02T09:00:00+00:00",
      "next_trigger_utc": "2025-06-09T04:30:00+00:00",
      "last_trigger_utc": "2025-06-02T04:30:00+00:00",
      "created_utc": "2025-05-28T11:22:33+00:00",
      "completed": false,
      "paused": false
    }
  ]
}
```

### Field reference

| Field | Type | Description |
|---|---|---|
| `id` | UUID4 string | Unique identifier, never changes |
| `title` | string (max 200) | Reminder title shown in notifications |
| `notes` | string (max 2000) | Optional detail text |
| `contact_name` | string (max 100) | Associated person's name |
| `contact_info` | string (max 200) | Phone number or email address |
| `reminder_type` | `"one_time"` \| `"interval"` \| `"daily"` | Controls how scheduling works |
| `interval_minutes` | integer \| null | Minutes between triggers (Interval only, range 1–43200) |
| `scheduled_time` | ISO 8601 UTC \| null | The target time set in the form |
| `next_trigger_utc` | ISO 8601 UTC | When the next notification will fire |
| `last_trigger_utc` | ISO 8601 UTC \| null | When the last notification fired |
| `created_utc` | ISO 8601 UTC | When the reminder was first created |
| `completed` | boolean | `true` after a One Time reminder fires |
| `paused` | boolean | `true` when individually paused |

All timestamps are stored in **UTC** and converted to local time only in the UI.

---

## Reminder Types Reference

### One Time
- Fires **once** at the exact date and time you specify.
- After firing, the reminder is marked `completed` and moves to the Done filter.
- Best for: meetings, appointments, one-off tasks.

### Interval
- Fires **repeatedly** every N minutes (1 minute to 30 days / 43,200 minutes).
- Starts at creation + interval. Does not use the date picker.
- Continues indefinitely until paused or deleted.
- Best for: recurring check-ins, hydration reminders, break timers.
- Example intervals:
  - 30 min = short break reminder
  - 60 min = hourly check-in
  - 1440 min = daily task (use Daily type instead for time-of-day precision)
  - 10080 min = weekly

### Daily
- Fires **every day at the same time** you set in the date/time picker. The date you pick is ignored; only the time matters.
- On first creation, if the specified time has already passed today, it schedules for tomorrow.
- Best for: morning routines, end-of-day reviews, medication reminders.

---

## Theme System

Promptly ships with two complete themes derived from the design tokens in `globals.css`.

### Switching
Click **☀ Light** or **🌙 Dark** in the top-right of the dashboard. The entire application re-styles instantly.

### Dark Theme (`--dark` tokens)
| Element | Colour |
|---|---|
| Background | `#000000` |
| Card surface | `#17181C` |
| Primary blue | `#1C9CF0` |
| Text | `#E7E9EA` |
| Muted text | `#72767A` |
| Border | `#242628` |
| Success | `#17BF63` |
| Warning | `#F7B928` |
| Danger | `#F4212E` |

### Light Theme (`:root` tokens)
| Element | Colour |
|---|---|
| Background | `#FFFFFF` |
| Card surface | `#F7F8F8` |
| Primary blue | `#1E9DF1` |
| Text | `#0F1419` |
| Muted text | `#8B98A5` |
| Border | `#E1EAF0` |
| Success | `#17BF63` |
| Warning | `#F7B928` |
| Danger | `#F4212E` |

---

## Architecture

Promptly follows a strict **layered architecture** — no business logic in UI classes.

```
┌─────────────────────────────────────────────────────────┐
│                   UI Layer                              │
│  DashboardWindow  TaskCard  TaskFormDialog  TrayIcon    │
└───────────────────────┬─────────────────────────────────┘
                        │ signals / slots
┌───────────────────────▼─────────────────────────────────┐
│                Application Layer                        │
│                   AppController                         │
│  (state machine: RUNNING / PAUSED / SHUTTING_DOWN /     │
│   RECOVERING — coordinates all layers)                  │
└──────┬────────────────┬──────────────────┬──────────────┘
       │                │                  │
┌──────▼──────┐  ┌──────▼──────┐  ┌────────▼──────────────┐
│  Scheduler  │  │   Storage   │  │  NotificationService  │
│   Engine    │  │ JsonStorage │  │  (WinRT Toast / Qt    │
│ (heapq +    │  │ (atomic R/W)│  │   balloon fallback)   │
│  QTimer)    │  └─────────────┘  └───────────────────────┘
└──────┬──────┘
       │
┌──────▼──────┐
│  Domain     │
│  Task       │
│  AppState   │
└─────────────┘
```

### Key design decisions

| Decision | Why |
|---|---|
| Single `.py` file | Zero deployment friction — copy one file and run |
| Icon embedded as base64 | No asset files needed alongside the exe |
| `heapq` + single `QTimer` | O(log n) scheduling, zero CPU at idle, no threads |
| Atomic save (`tmp` → `replace`) | Power loss mid-write never corrupts data |
| UTC storage, local display | Correct across DST changes and timezone moves |
| Defensive schema loading | Malformed or partially-written JSON never crashes the app |
| `QObject` + `pyqtSignal` | All cross-layer communication is signal-driven, not callbacks |

---

## Troubleshooting

### Promptly doesn't appear in the tray
- Click the `^` (Show hidden icons) arrow in the taskbar system tray area.
- Windows may have moved it to the overflow tray. Right-click the taskbar → Taskbar settings → Other system tray icons → enable Promptly.

### Notifications don't appear
1. Check Windows notification settings: Settings → System → Notifications → make sure notifications are On.
2. Check Focus Assist (Do Not Disturb): if Focus Assist is active, toast notifications are suppressed. Promptly will fall back to a Qt balloon message in the tray.
3. Check if Promptly is globally paused: right-click the tray icon — if it says "Resume Notifications", click it.
4. Check if the individual reminder is paused: open the dashboard and look for the amber "Paused" badge on the card.

### Antivirus flags Promptly.exe
PyInstaller bundles Python inside the exe, which some antivirus heuristics flag as suspicious. This is a false positive. Resolution options:
- Add an exclusion in Windows Defender for `Promptly.exe` or the `dist\` folder.
- Code-sign the exe with a purchased certificate.
- Run from source (`python Promptly.py`) to avoid bundling entirely.

### data.json was corrupted
Promptly automatically renames corrupted files to `data.json.corrupted_YYYYMMDD_HHMMSS` and starts fresh. To recover:
1. Open the `.corrupted` file in a text editor.
2. If it is mostly intact, repair the JSON manually and rename it back to `data.json`.
3. Restart Promptly.

### System tray not available
On some remote desktop or minimal Windows Server sessions, the system tray may not be available. Promptly will display an error dialog and exit in this case. Run on a full desktop session.

### Reminders fired at wrong time
All times are stored in UTC. If you moved the executable to a machine in a different timezone after creating reminders, the notification time will appear shifted in local time. Edit and re-save the affected reminders to update them.

---

## Uninstalling

Promptly makes no registry entries, creates no background services, and writes no files outside its own folder.

**To uninstall completely:**
1. Right-click the tray icon → Exit Promptly.
2. Delete `Promptly.exe` (or `Promptly.py` if running from source).
3. Delete `data.json` (your reminders).
4. If you added it to the Startup folder, delete the shortcut from `shell:startup`.

That's it. Nothing else to clean up.

---

## Changelog

### v1.0 — Initial Release

**Application**
- Full tray-resident assistant with system tray icon, context menu, and dashboard window
- Three reminder types: One Time, Interval, Daily
- Per-reminder: title, notes, contact name, contact info
- Individual pause/resume per reminder
- Global pause/resume from tray menu
- Startup recovery for overdue reminders

**Scheduler**
- `heapq`-based priority queue with single `QTimer` — zero polling, ~0% idle CPU
- System sleep / DST / clock-change safe
- Duplicate-fire guard (10-second window)

**Storage**
- Atomic JSON writes (tmp → replace)
- Corrupted file auto-quarantine
- Full schema validation on load
- UUID4 reminder IDs, all timestamps in UTC

**Notifications**
- Windows Toast (WinRT) via `windows-toasts`
- Qt balloon tray fallback if WinRT unavailable
- Title + notes + contact in notification body

**UI**
- Dark and Light themes (CSS design tokens)
- One-click theme toggle
- Dashboard: search, filter (All/Active/Paused/Completed), stats strip
- Colour-coded card accent bars by reminder type
- Tray icon state: blue (active), amber (paused)
- Bell + lightning bolt icon at 7 resolutions (16–256 px)
- Single `Promptly.exe` via PyInstaller — no Python needed on target machine

---

*Promptly — Smart Reminders · Never Miss a Moment*
