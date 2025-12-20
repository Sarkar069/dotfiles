#!/bin/bash

# Give X enough time to be fully ready
sleep 2

# Start clipboard manager (wait a bit longer)
sh -c "sleep 1 && copyq" &
