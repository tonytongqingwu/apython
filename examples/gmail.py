import os
import sys
from apython.uiauto import UADevice
from apython.utils import find_element_has_text_with_bounds


id_adb = sys.argv[1]
ua = UADevice(id_adb)

# os.system('adb -s {}  shell monkey -p com.google.android.gm -v 5'.format(id_adb))
# os.system('adb -s {} shell am start com.google.android.gm'.format(id_adb))
ua.select_text('Confirm your email to test Dex')
ua.dump_screen('gmail')

file_name = id_adb + '_gmail.xml'
start_x, start_y, end_x, end_y = find_element_has_text_with_bounds(file_name, 'Search release')
print(start_x, start_y, end_x, end_y)
m_x = (end_x - start_x) / 2
m_y = (end_y - start_y) / 2
print(m_x)
print(m_y)
os.system('adb -s {} shell input tap {} {}'.format(id_adb, m_x, m_y))


