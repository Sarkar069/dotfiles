#!/bin/bash

# Ensure environment is available for notify-send under i3
export DISPLAY=:0
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"

# Use hardcoded path (from your system)
BATTERY_PATH="/org/freedesktop/UPower/devices/battery_BAT0"

# Get battery info safely
INFO=$(upower -i "$BATTERY_PATH")

STATE=$(echo "$INFO" | grep -E "^\s*state:" | awk -F: '{print $2}' | xargs)
PERCENT=$(echo "$INFO" | grep -E "^\s*percentage:" | awk -F: '{print $2}' | xargs)
TIME=$(echo "$INFO" | grep -E "^\s*time to (empty|full):" | awk -F: '{print $2}' | xargs)

# Icon logic
case "$STATE" in
charging) ICON="⚡" ;;
discharging) ICON="🔋" ;;
fully-charged) ICON="✅" ;;
*) ICON="🔌" ;;
esac

# Message format
if [ -n "$TIME" ]; then
  MESSAGE="$STATE\n🔋 $PERCENT\n⏳ $TIME remaining"
else
  MESSAGE="$STATE\n🔋 $PERCENT"
fi

# Show notification with dunst
notify-send "$ICON Battery Status" "$MESSAGE"
