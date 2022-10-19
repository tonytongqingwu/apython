import os
import time
import re
from time import sleep
from apython.utils import run_command, get_battery_level, get_top_info


class AdbDevice:
    def __init__(self, adb_id):
        self.adb_id = adb_id

    def open_url_in_chrome(self, url):
        os.system("adb -s " + self.adb_id +
                  " shell am start -n com.android.chrome/com.google.android.apps.chrome.Main -d " + url)

    def start_app(self, app_name):
        """

        :param app_name:  ex. android.settings.SETTINGS
        :return:
        """
        try:
            os.system("adb -s " + self.adb_id + "  shell am start -a " + app_name)
        except Exception as e:
            print('Start app failed {}'.format(e))
        finally:
            print('Failed start app {}'.format(app_name))

    def start_app_settings(self):
        self.start_app('android.settings.SETTINGS')

    def dump_top_cpu(self, file_path):
        """
        Dump memory, cpu to files
        :param file_path:
        :return:
        """
        time_str = time.strftime("%Y%m%d-%H%M%S")
        os.system('adb -s {0} shell top -n 1 > {1}_{0}_{2}_top.log'.format(self.adb_id, file_path, time_str))
        os.system('adb -s {0} shell dumpsys cpuinfo | head -10 > {1}_{0}_{2}_cpu.log'.format(self.adb_id, file_path, time_str))

    def key_five(self, key_code):
        """
        Send keyevent for 5 times .
        :param key_code: 0 -->  "KEYCODE_UNKNOWN"
1 -->  "KEYCODE_MENU"
2 -->  "KEYCODE_SOFT_RIGHT"
3 -->  "KEYCODE_HOME"
4 -->  "KEYCODE_BACK"
5 -->  "KEYCODE_CALL"
6 -->  "KEYCODE_ENDCALL"
7 -->  "KEYCODE_0"
8 -->  "KEYCODE_1"
9 -->  "KEYCODE_2"
10 -->  "KEYCODE_3"
11 -->  "KEYCODE_4"
12 -->  "KEYCODE_5"
13 -->  "KEYCODE_6"
14 -->  "KEYCODE_7"
15 -->  "KEYCODE_8"
16 -->  "KEYCODE_9"
17 -->  "KEYCODE_STAR"
18 -->  "KEYCODE_POUND"
19 -->  "KEYCODE_DPAD_UP"
20 -->  "KEYCODE_DPAD_DOWN"
21 -->  "KEYCODE_DPAD_LEFT"
22 -->  "KEYCODE_DPAD_RIGHT"
23 -->  "KEYCODE_DPAD_CENTER"
24 -->  "KEYCODE_VOLUME_UP"
25 -->  "KEYCODE_VOLUME_DOWN"
26 -->  "KEYCODE_POWER"
27 -->  "KEYCODE_CAMERA"
28 -->  "KEYCODE_CLEAR"
29 -->  "KEYCODE_A"
30 -->  "KEYCODE_B"
31 -->  "KEYCODE_C"
32 -->  "KEYCODE_D"
33 -->  "KEYCODE_E"
34 -->  "KEYCODE_F"
35 -->  "KEYCODE_G"
36 -->  "KEYCODE_H"
37 -->  "KEYCODE_I"
38 -->  "KEYCODE_J"
39 -->  "KEYCODE_K"
40 -->  "KEYCODE_L"
41 -->  "KEYCODE_M"
42 -->  "KEYCODE_N"
43 -->  "KEYCODE_O"
44 -->  "KEYCODE_P"
45 -->  "KEYCODE_Q"
46 -->  "KEYCODE_R"
47 -->  "KEYCODE_S"
48 -->  "KEYCODE_T"
49 -->  "KEYCODE_U"
50 -->  "KEYCODE_V"
51 -->  "KEYCODE_W"
52 -->  "KEYCODE_X"
53 -->  "KEYCODE_Y"
54 -->  "KEYCODE_Z"
55 -->  "KEYCODE_COMMA"
56 -->  "KEYCODE_PERIOD"
57 -->  "KEYCODE_ALT_LEFT"
58 -->  "KEYCODE_ALT_RIGHT"
59 -->  "KEYCODE_SHIFT_LEFT"
60 -->  "KEYCODE_SHIFT_RIGHT"
61 -->  "KEYCODE_TAB"
62 -->  "KEYCODE_SPACE"
63 -->  "KEYCODE_SYM"
64 -->  "KEYCODE_EXPLORER"
65 -->  "KEYCODE_ENVELOPE"
66 -->  "KEYCODE_ENTER"
67 -->  "KEYCODE_DEL"
68 -->  "KEYCODE_GRAVE"
69 -->  "KEYCODE_MINUS"
70 -->  "KEYCODE_EQUALS"
71 -->  "KEYCODE_LEFT_BRACKET"
72 -->  "KEYCODE_RIGHT_BRACKET"
73 -->  "KEYCODE_BACKSLASH"
74 -->  "KEYCODE_SEMICOLON"
75 -->  "KEYCODE_APOSTROPHE"
76 -->  "KEYCODE_SLASH"
77 -->  "KEYCODE_AT"
78 -->  "KEYCODE_NUM"
79 -->  "KEYCODE_HEADSETHOOK"
80 -->  "KEYCODE_FOCUS"
81 -->  "KEYCODE_PLUS"
82 -->  "KEYCODE_MENU"
83 -->  "KEYCODE_NOTIFICATION"
84 -->  "KEYCODE_SEARCH"
85 -->  "TAG_LAST_KEYCODE"
        :return:
        """
        try:
            os.system("adb -s " + self.adb_id + " shell input keyevent " + str(key_code))
        except Exception as e:
            print(e)
            print("Unable to click on {} button".format(key_code))
            for i in range(0, 5):
                self.key_home()
                sleep(0.2)

    def key_home(self):
        self.key_five(3)

    def key_enter(self):
        self.key_five('KEYCODE_ENTER')

    def key_back(self):
        self.key_five(4)

    def adb_get_battery_level(self):
        r_code, s_out, s_err = run_command('adb -s {0} shell dumpsys battery | grep level'.format(self.adb_id))
        if r_code == 0:
            return get_battery_level(s_out)
        else:
            return 0

    def adb_get_top_info(self):
        r_code, s_out, s_err = run_command('adb -s {0} shell top -n 1 | head -4'.format(self.adb_id))
        if r_code == 0:
            return get_top_info(s_out)
        else:
            return 0, 0

    def dump_screen(self, s_name):
        """
        dump screen to png and txt file
        :param s_name: full path of dump file (folder/name)
        :return:
        """
        os.system('adb -s {} exec-out screencap -p > {}.png'.format(self.adb_id, s_name))
        os.system('adb -s {} exec-out uiautomator dump /dev/tty > {}.txt'.format(self.adb_id, s_name))

    def set_adb_wifi(self, t_port=5555):
        r_code, s_out, s_err = run_command('adb -s {0} shell ip addr show wlan0 | grep "global wlan"'.format(self.adb_id))
        if r_code == 0:
            print(s_out)
            m = re.search('inet (\d+\.\d+\.\d+\.\d+)\/2', s_out)
            if m:
                wlan_ip = m.group(1)
                print(wlan_ip)

                os.system('adb -s {} tcpip {}'.format(self.adb_id, t_port))
                os.system('adb -s {} connect {}:{}'.format(self.adb_id, wlan_ip, t_port))
                os.system('adb devices')

                # print('Connecting to wifi now, you can disconnect cable anytime now')
                return wlan_ip
        else:
            print('Can not get wlan ip, return code {}, error {}'.format(r_code, s_err))
            return ''

    def adb_get_model(self):
        r_code, s_out, s_err = run_command('adb -s {0} shell getprop ro.product.model'.format(self.adb_id))
        if r_code == 0:
            m = s_out.replace(' ', '').strip()
            return m
