# apython

Dexcom internal Android Python Library to support Dexcom appliation testing like G7, etc.  It uses Appium or uiautomator as needed.

adbd, uiauto, appm.

## install apython

1. Clone python package use following command:

`mkdir ~/Sandbox/ ; cd ~/Sandbox && git clone https://github.com/tonytongqingwu/apython.git`   

NOTE: if you have control USB board, also clone this:

`cd ~/Sandbox && git clone https://github.com/dexcom-inc/G7X_Tests.git`

2. Then just run the setup.py file from that directory,

`sudo python3 setup.py install`

NOTE: if you don't want to check example code or create your own scripts, just run:

`pip3 install git+https://github.com/tonytongqingwu/apython.git#egg=apython`

## How to run stress test

1. Connect your device with USB, make sure adb enabled for development
2. Check examples folder, create own test, or just run:

`bash stress_check.sh`

## Check logs:

Home folder has a new folder like this - /module/adb_serial_num/timestamp 

## If you have issue of installation, or running message like:
`ModuleNotFoundError: No module named ‘google.protobuf’`

Follow steps to fix:
1. install python 3.10.8 https://www.python.org/downloads/release/python-3108/   
2. Go to new script folder
`cd ~/Sandbox/apython ; git pull`
to update the script - remove USB power support for now.   
3. Run setup from the same folder
`sudo python3 setup.py install`
4. if you got errors complains about failure of installation of appium or grpc-requests, just remove lin 13, 14 in setup.py file, and rerun step 3 command and then run following command manually:
`pip3 install grpc-requests ; pip3 install Appium-Python-Client==1.1.0`
5. Now setup G7, pair with DrStange, and ready to run:
`cd ~/Sandbox/apython/examples ; bash stress_check.sh`


