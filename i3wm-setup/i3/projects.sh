#!/usr/bin/env bash
# Rofi-based VS Code project launcher with pywal theme

PROJECT_DIR="$HOME/Pyprojects"
ROFI_THEME="$HOME/.cache/wal/colors-rofi-dark.rasi"

# Ensure project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
  notify-send "⚠️ Pyprojects not found" "No directory at $PROJECT_DIR"
  exit 1
fi

# Build project list (+ "New Project" option)
PROJECTS=$(find "$PROJECT_DIR" -mindepth 1 -maxdepth 1 -type d |
  sort |
  sed "s|$PROJECT_DIR/||")

CHOICE=$(echo -e "🆕 New Project\n$PROJECTS" |
  rofi -dmenu -i -p "Open project in VS Code:" -theme "$ROFI_THEME")

# Handle cancel
[ -z "$CHOICE" ] && exit 0

# If user chose to create new project
if [ "$CHOICE" = "🆕 New Project" ]; then
  NEW_NAME=$(rofi -dmenu -p "Enter new project name:" -theme "$ROFI_THEME")
  [ -z "$NEW_NAME" ] && exit 0
  mkdir -p "$PROJECT_DIR/$NEW_NAME"
  code "$PROJECT_DIR/$NEW_NAME"
  exit 0
fi

# Otherwise open selected project
code "$PROJECT_DIR/$CHOICE"
