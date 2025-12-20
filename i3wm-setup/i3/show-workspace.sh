#!/bin/bash

# Get list of workspaces, highlight the focused one
ws=$(i3-msg -t get_workspaces | jq -r '
    map(if .focused
        then "<b><span foreground=\"#88c0d0\">[" + (.name|tostring) + "]</span></b>"
        else .name end)
    | join("\n")')

# Show notification with markup
notify-send -t 3000 -u low "Workspaces" "$ws" \
  -h string:x-canonical-private-synchronous:workspaces
