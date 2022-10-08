#!/bin/bash
kill_ps () {
  kill -9 $(ps aux | grep "$1" | grep -v "grep"  | awk '{print $2}')
}

kill_ps battery.py
kill_ps appium

