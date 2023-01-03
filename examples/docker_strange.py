import os
import sys

from apython.utils import get_transmitter_info


if __name__ == '__main__':
    state = sys.argv[1]
    prod_type, address, transmitter_id, pair_code = get_transmitter_info()
    user_home = os.getenv('HOME')
    cmd = f"docker run -v {user_home}/Sandbox/apython/examples:/examples  quick-test examples/strange2.py " \
          f"{address} {pair_code} {transmitter_id} host.docker.internal:44444 {state}"
    print(cmd)
    os.system(cmd)


