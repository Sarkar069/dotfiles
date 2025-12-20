#!/bin/bash

# Check if dunstify is installed
if ! command -v dunstify &> /dev/null; then
    echo "Error: dunstify not found. Please install Dunst."
    exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq not found. Please install jq."
    exit 1
fi

# Get the workspace information from swaymsg
workspaces=$(swaymsg -t get_workspaces | jq -r '.[] | {num: .num, focused: .focused}')

# Get the current workspace number
current_workspace=$(echo "$workspaces" | jq -r 'select(.focused == true) | .num')

# Initialize an empty string for the output
output=""

# Loop through workspaces to build the display string
for ws in $(echo "$workspaces" | jq -r '.num' | sort -n); do
    if [ "$ws" == "$current_workspace" ]; then
        # Highlight the current workspace with square brackets
        output="$output [$ws]"
    else
        output="$output $ws"
    fi
done

# Trim leading/trailing whitespace
output=$(echo "$output" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

# Send a notification using dunstify
dunstify -a "Sway Workspaces" -u normal -t 3000 -r 1000 "Workspaces" "$output"
