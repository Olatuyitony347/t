#!/bin/bash

while true; do
    echo "Running base-op.py..."
    ( echo "10000" | python3 base-op.py ) &  # Run in background
    pid=$!  # Capture process ID

    sleep 120  # Wait for 120 seconds

    echo "Switching to op-base.py..."
    kill $pid 2>/dev/null  # Terminate base-op.py before switching
    ( echo "10000" | python3 op-base.py ) &  # Run in background
    pid=$!  # Capture new process ID

    sleep 120  # Wait for 120 seconds before switching back

    echo "Switching back to base-op.py..."
    kill $pid 2>/dev/null  # Terminate op-base.py before switching
done
