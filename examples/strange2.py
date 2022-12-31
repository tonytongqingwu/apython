import sys
from time import sleep
from grpc_requests import Client


class GrpcClient:
    def __init__(self, address, pair_code, transmitter_id, end_point='localhost:44444'):
        self.client = Client.get_by_endpoint(end_point)
        self.state = dict()
        self.state['pairingCode'] = pair_code
        self.state['transmitterSNR'] = transmitter_id
        self.state['autoMode'] = 'OFF'
        self.state['commInterval'] = 'SEC_30'
        self.state['prodCertType'] = 'NON_PROD_CERTS'
        self.state['transmitterStatus'] = 'HEALTHY'

        self.request = dict()
        self.request['address'] = address
        self.request['caller'] = 1

        self.egv_request = dict()
        self.egv_request['address'] = address
        self.egv_request['transmitterId'] = transmitter_id

    def get_egv(self):
        result = self.client.request("G7TransmitterSimulatorService", "GetG7CommunicatedEGV", self.egv_request)
        print(type(result))
        egvs = result['communicatedEGV']
        # last_3_egv = egvs[-3:]
        # print(last_3_egv)
        last_egv = egvs[-1]
        return last_egv['egv']

    def save_state(self, state_string):
        """
        Save state with string input:
        :param state_string:
        :return:
        """
        states = ['START_ADVERTISING', 'STOP_ADVERTISING', 'PAUSE_ADVERTISING']
        if state_string not in states:
            print('!!!!!!!!!!! Invalid state')
        else:
            self.state['advertisingState'] = state_string
            self.request['transmitterSimulatorState'] = self.state

            result = self.client.request("G7TransmitterSimulatorService", "SaveG7TransmitterSimulatorState",
                                         self.request)
            print(result)


g = GrpcClient(sys.argv[1], sys.argv[2], sys.argv[3], end_point=sys.argv[4])
g.save_state(sys.argv[5])


