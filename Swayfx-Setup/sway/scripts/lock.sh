#!/bin/bash

# Swayidle script with display off and lock
swayidle -w \
    timeout 600 'swaymsg "output * dpms off"' \  # Turn off display after 10 minutes
    resume 'swaymsg "output * dpms on"' \       # Turn display on when activity resumes
    timeout 3600 'swaylock -f'                  # Lock screen after 1 hour
