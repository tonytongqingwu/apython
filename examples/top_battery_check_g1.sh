#!/bin/sh
osascript  <<EOF
tell app "Terminal"
  do script "cd ~/Sandbox/apython/examples && python3 battery_g1.py &"
end tell
EOF
