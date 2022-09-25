# apython

Dexcom internal Android Python Library to support Dexcom appliation testing like G7, etc.  It uses Appium or uiautomator as needed.

adbd, uiauto, appm.

## install apython

1. Clone this repository.

`git clone https://github.com/tonytongqingwu/apython.git`   

2. Then just run the setup.py file from that directory,

`sudo python setup.py install`

## How to run

1. Start appium:

`appium --relaxed-security `

2. Check examples folder, create own test, or just run:

`python3 examples/stress.py R58R50YXKEP  '/Users/tt0622/a52/all'`

With serial number , and log path
