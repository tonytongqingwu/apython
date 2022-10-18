import os
import subprocess
import re
import time
import json
from time import sleep


def record_top(file_name, value):
    """
    Record value to a file
    :param file_name: any file path
    :param value: any value
    :return:
    """
    with open(file_name, 'w') as f:
        f.writelines(str(value))


def record_apps(file_name, value):
    """
    Append app name to a file
    :param file_name: any file
    :param value: any name
    :return:
    """
    with open(file_name, 'a') as f:
        f.write(value + ',')


def log_info(file_name, value):
    """
    Append app name to a file
    :param file_name: any file
    :param value: any name
    :return:
    """
    with open(file_name, 'a') as f:
        f.writelines(value + '\n')


def logcat(log_path, adb_id):
    os.system('adb -s {} -d logcat com.dexcom.g7:V -d > {}/logcat.txt'.format(adb_id, log_path))


def get_app_list(apps_file):
    with open(apps_file) as f:
        apps_string = f.read().rstrip()

    a_list = apps_string.split(',')
    # print(a_list)
    print(a_list.count('G7'))
    return a_list


def run_command(command):
    c_list = str.split(command)
    p = subprocess.run(c_list, capture_output=True)

    r_code = p.returncode
    s_out = p.stdout.decode()
    s_err = p.stderr.decode()
    # print(r_code)
    # print(s_out)
    # print(s_err)
    return r_code, s_out, s_err


def get_battery_level(output):
    """
    Get level from output from command: adb -s xxx shell dumpsys battery | grep level
    :param output: adb command output
    :return: level number
    """
    m = re.search('level: (\d+)', output)
    if m:
        battery_level = int(m.group(1))
        print(battery_level)
        return battery_level


def get_top_info(out):
    """
    Get cpu/mem info from top command: adb -s xxx shell top -n 1 | head -4
    :param out:
    :return:
    """
    mem_free = cpu_total = cpu_idle = cpu_used = 0
    mem_unit = 'M'
    out = re.sub(r'\W+', '', out)
    print(out)
    # used60Mfree51MbuffersSwap20Gtotal14Gused517Mfree920Mcached800cpu117user0nice60sys607idle0iow13irq3sirq0host
    # used1885132Kfree6438912buffersSwap2621436Ktotal1942704Kused678732Kfree960304Kcached800cpu100user0nice107sys579idle0iow10irq3sirq0host
    m = re.search('used(\d+)(\w)free.+\d+\wfree.+cached(\d+)cpu.+sys(\d+)idle', out)
    if m:
        mem_free = int(m.group(1))
        mem_unit = m.group(2)
        cpu_total = int(m.group(3))
        cpu_idle = int(m.group(4))

        print(cpu_idle)
        print(cpu_total)
        print(mem_free)
        print(mem_unit)
        cpu_used = int(cpu_total) - int(cpu_idle)

        if mem_unit == 'G':
            mem_free *= 1000
        elif mem_unit == 'K':
            mem_free = int(mem_free / 1000)

    return mem_free, cpu_used


def get_id():
    os.system('adb kill-server && adb start-server && adb devices ')
    r_code, s_out, s_err = run_command('adb shell getprop ro.serialno')
    if r_code == 0:
        return s_out.strip()
    else:
        return ''


def get_wip_id():
    r_code, s_out, s_err = run_command('adb devices')
    if r_code == 0:
        print(s_out)
        m = re.search('(\d+\.\d+\.\d+\.\d+:\d+)', s_out.strip())
        if m:
            return m.group(1)
    else:
        print(r_code)
        return ''


def create_log_path(model, id_adb):
    log_path = os.getenv('HOME')
    log_path = '{}/{}'.format(log_path, model)
    os.system('mkdir {}'.format(log_path))
    log_path = '{}/{}'.format(log_path, id_adb)
    os.system('mkdir {}'.format(log_path))
    log_path = '{}/{}'.format(log_path, time.strftime("%Y%m%d-%H%M"))
    os.system('mkdir {}'.format(log_path))

    print('-------log path {}'.format(log_path))
    return log_path


def remove_appium(id_adb):
    os.system("adb -s {} uninstall io.appium.uiautomator2.server".format(id_adb))
    sleep(2)
    os.system("adb -s {} uninstall io.appium.uiautomator2.server.test".format(id_adb))
    sleep(2)
    os.system("adb -s {} uninstall io.appium.settings".format(id_adb))
    sleep(2)


# old method, not working all the time due to update device
def get_transmitter_info_old(url='http://localhost:7890/nodes/'):
    r = requests.get(url)
    da = r.text
    data = json.loads(da)
    data = data[0]
    # print(data)
    transmitter = (data['transmitters'])[0]
    # print(transmitter)
    transmitter_id = transmitter['transmitterId']
    pair_code = transmitter['pairingCode']
    address = transmitter['address']
    prod_type = transmitter['productType']

    # print(transmitter_id)
    # print(pair_code)
    # print(address)
    # print(prod_type)

    return prod_type, address, transmitter_id, pair_code


def get_transmitter_info():
    transmitter_id = pair_code = 0
    address = ''
    prod_type = 'G7'
    r_code, s_out, s_err = run_command('docker logs jarvis_server --since=6m')

    if r_code == 0:
        print('Get all info')
        s_out = s_out.replace(' ', '').strip()
        # print(s_out)
        m = re.search('pairingCode:(\d+)', s_out)
        o = re.search('address:\"(\d+\.\d+\.\d+\.\d+)\"', s_out)
        n = re.search('transmitterId:\"(\d+)\"', s_out)
        if m:
            pair_code = int(m.group(1))
        else:
            print('No pattern for code')

        if o:
            address = o.group(1)
        else:
            print('No pattern for address')

        if n:
            transmitter_id = n.group(1)
        else:
            print('No pattern for id')
    else:
        print(s_err)
        print('Get no info')

    print(transmitter_id)
    print(pair_code)
    print(address)
    print(prod_type)

    return prod_type, address, transmitter_id, pair_code


def check_signal_loss_message(file_name):
    cmd = "grep 'id_glucose_state_card_title_label' {} | grep 'Signal Loss'".format(file_name)
    print(cmd)
    r_code, s_out, s_err = run_command(cmd)
    print('out ----------------')
    print(s_out)
    print('err ----------------')
    print(s_err)
    if r_code == 0:
        return True
    else:
        return False


def get_widget_bounds(bounds):
    print('bound is '.format(bounds))
    start_x = start_y = end_x = end_y = 0
    m = re.search('^\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
    if m:
        start_x = int(m.group(1))
        start_y = int(m.group(2))
        end_x = int(m.group(3))
        end_y = int(m.group(4))

    return start_x, start_y, end_x, end_y


def find_element_has_text_with_bounds(file_name, text):
    with open(file_name) as f:
        for line in f:
            print(line)
            # m = re.search(text + '.+bounds="(\[.+\])"', line)  #  also works
            m = re.search('text.+' + text + '.+bounds="(\[.+\])"', line)
            if m:
                print('Found match')
                b = m.group(1)
                print(b)
                return get_widget_bounds(b)


