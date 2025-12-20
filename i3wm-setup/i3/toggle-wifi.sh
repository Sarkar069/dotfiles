#!/bin/bash

# Get current Wi-Fi state (enabled/disabled)
STATE=$(nmcli -t -f WIFI radio)

if [[ $STATE == "enabled" || $STATE == "on" ]]; then
  nmcli radio wifi off
  if [[ $? -eq 0 ]]; then
    dunstify -t 1500 "Wi-Fi ❌" "Radio is now OFF"
  else
    dunstify -t 1500 "Wi-Fi ❗" "Failed to disable Wi-Fi"
  fi
else
  nmcli radio wifi on
  if [[ $? -eq 0 ]]; then
    dunstify -t 1500 "Wi-Fi 📶" "Radio is now ON"
  else
    dunstify -t 1500 "Wi-Fi ❗" "Failed to enable Wi-Fi"
  fi
fi
