# apython

Dexcom internal Android Python Library to support Dexcom appliation testing like G7, etc.  It uses Appium or uiautomator as needed.

adbd, uiauto, appm.

## install apython

1. Clone this repository to your home folder, cd ~/Sandbox/

`mkdir ~/Sandbox/ ; cd ~/Sandbox && git clone https://github.com/tonytongqingwu/apython.git`   

2. Then just run the setup.py file from that directory,

`sudo python3 setup.py install`

NOTE: if you don't want to check example code or create your own scripts, just run:

`pip3 install git+https://github.com/tonytongqingwu/apython.git#egg=apython`

## How to run stress test

1. Connect your device with USB, make sure adb enabled for development
2. Check examples folder, create own test, or just run:

`python3 stress.py`

## Check logs:

Home folder has a new folder like this - /module/adb_serial_num/timestamp 
