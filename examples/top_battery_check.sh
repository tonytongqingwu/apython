#!/bin/sh
osascript  <<EOF
tell app "Terminal"
  do script "cd ~/Sandbox/apython/examples && python3 battery.py &"
end tell
EOF
