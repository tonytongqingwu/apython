import os
import os.path
from time import sleep
from apython.adbd import AdbDevice
from apython.utils import record_top, get_id, create_log_path


if __name__ == '__main__':
    id_adb = get_id()
    print('id: ---------')
    print(id_adb)

    adb_d = AdbDevice(id_adb)

    # create folder
    model = adb_d.adb_get_model()
    print('----{}-----'.format(model))
    log_path = create_log_path(model, id_adb)
    print('log path {}'.format(log_path))

    min_mem_free = 4000
    max_cpu_used = 0

    top_mem = log_path + '/free_mem.log'
    top_cpu = log_path + '/used_cpu.log'

    while True:
        sleep(60)
        # get top info
        m, c = adb_d.adb_get_top_info()
        if m < min_mem_free:
            min_mem_free = m
            record_top(top_mem, min_mem_free)

        if c > max_cpu_used:
            max_cpu_used = c
            record_top(top_cpu, max_cpu_used)
