import sys
from apython.adbd import AdbDevice

"""
Example: add a wifi connection
input: adb id
"""
id_adb = sys.argv[1]
a_d = AdbDevice(id_adb)
w_ip = a_d.set_adb_wifi()

print(w_ip)


