#!/bin/bash

# Give X enough time to be fully ready
sleep 2

# Set resolution
xrandr --output eDP-1 --mode 1360x768

# Start compositor with small delay
sh -c "sleep 0.5 && picom --config ~/.config/picom/picom.conf" &

# Start clipboard manager (wait a bit longer)
sh -c "sleep 1 && copyq" &

# Autostart desktop apps
dex --autostart --environment i3 &
