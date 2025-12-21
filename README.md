# 🖥️ Dotfiles

Personal Linux dotfiles for **SwayFX (Wayland)** and **i3wm (X11)**, with shared configurations for terminals, notifications, scripts, and utilities.

Designed to keep **shared configs reusable** and **WM-specific logic isolated**.

---

## ✨ Features

- **SwayFX** (Wayland) setup with swaylock 
- **i3wm** (X11) setup with picom 
- Shared configs for:
  - Alacritty
  - Kitty
  - Dunst
  - Scripts
- Minimal duplication
- Clean, readable structure

---

## 📂 Repository Structure

```text
dotfiles/
├── wm/
│   ├── swayfx/        # Wayland WM config
│   │   └── scripts/   # only works on wayland
│   └── i3/            # X11 WM config
│       └── scripts/   # only works on x11
│
├── dunst/             # notifications 
├── picom/             # X11 compositor
├── swaylock/          # Wayland lockscreen
│
├── scripts/           # shared scripts
└── wallpapers/


