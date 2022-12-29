#!/bin/sh
osascript  <<EOF
tell app "Terminal"
  do script "cd ~/Sandbox/apython/examples && /opt/homebrew/bin/python3.10 stress.py &"
end tell
EOF
