from apython.grpc.d1pake import D1Pake
from apython.utils import get_transmitter_info_d1_pake, get_egv_from_log
from time import sleep


prod_type, address, transmitter_id = get_transmitter_info_d1_pake()
g = D1Pake(address, transmitter_id)
egv = g.get_egv()
print(egv)
g.save_state('PAUSE_ADVERTISING')
# sleep(70)
# g.save_state('START_ADVERTISING')


