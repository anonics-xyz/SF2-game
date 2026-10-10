# 🕹️ Terminal Arcade Suite

A zero-dependency, cross-platform terminal arcade suite written in pure Python. Play classic arcade games directly inside your command-line interface with ANSI-colored visuals and real-time keyboard controls.

---

## 🎮 Included Games

| Game | Description | Controls |
| :--- | :--- | :--- |
| **Snake** | Navigate the grid, collect food (`*`), avoid walls and your own tail. | `W/A/S/D` or `Arrow Keys` |
| **Flappy Bird** | Flap through randomly generated pipe obstacles using real-time gravity physics. | `W`, `Up Arrow`, or `Space` |
| **2048** | Slide and merge matching numbered tiles to achieve the elusive 2048 tile. | `W/A/S/D` or `Arrow Keys` |

---

## ✨ Features

- **Zero External Dependencies:** Built using standard Python libraries (`msvcrt`, `termios`, `select`, `time`, `random`).
- **Cross-Platform Input Handling:**
  - Non-blocking input on Windows via `msvcrt`.
  - Raw TTY and POSIX stream polling on Linux/macOS via `termios` and `select`.
- **Interactive Menu:** Navigate the launcher menu using keyboard shortcuts or direct number hotkeys (`1`–`4`).
- **ANSI Color Graphics:** Dynamic color coding for game boundaries, score displays, and tile ranks in 2048.

---

## 📋 Prerequisites

- **Python 3.7+**
- A terminal that supports ANSI escape codes (Windows Terminal, PowerShell, Command Prompt on Windows 10+, iTerm2, macOS Terminal, GNOME Terminal, etc.).

---

## 🚀 Quick Start

1. **Save the script** as `arcade.py`:
   ```bash
   # Clone or save your script file locally
