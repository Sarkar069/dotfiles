#!/bin/bash

# Get date and time in 12-hour format with AM/PM
TIME=$(date '+%I:%M:%S %p')
DATE=$(date '+%A, %d %B %Y')

# Show as notification
notify-send "🕒 $TIME" "$DATE"

