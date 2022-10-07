from apython.grpc.gclient import GrpcClient
from apython.utils import get_transmitter_info


prod_type, address, transmitter_id, pair_code = get_transmitter_info()
g = GrpcClient(address, pair_code, transmitter_id)
# g.save_state('START_ADVERTISING')
g.save_state('PAUSE_ADVERTISING')
