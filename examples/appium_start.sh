#!/bin/sh
# Script: nw2
# Opens a new Terminal window
osascript  <<EOF
tell app "Terminal"
  do script "appium --relaxed-security --command-timeout 120000 &"
end tell
EOF
