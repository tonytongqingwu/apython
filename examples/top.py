import sys
from apython.adbd import AdbDevice

"""
Example: add a wifi connection
input: adb id
"""
id_adb = sys.argv[1]
a_d = AdbDevice(id_adb)
m, c = a_d.adb_get_top_info()

print('Free memory : {} and used cpu : {}'.format(m, c))


