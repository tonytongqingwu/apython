#!/bin/sh
osascript  <<EOF
tell app "Terminal"
  do script "cd ~/Sandbox/apython/examples && python3 stress_ios.py &"
end tell
EOF
