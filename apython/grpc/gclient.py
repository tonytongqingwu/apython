from grpc_requests import Client


class GrpcClient:
    def __init__(self, address, pair_code, transmitter_id):
        self.client = Client.get_by_endpoint("localhost:44444")
        self.state = dict()
        self.state['pairingCode'] = pair_code
        self.state['transmitterSNR'] = transmitter_id
        self.state['autoMode'] = 0
        self.state['commInterval'] = 'SEC_30'
        self.state['prodCertType'] = 'NON_PROD_CERTS'
        self.state['transmitterStatus'] = 'HEALTHY'

        self.request = dict()
        self.request['address'] = address
        self.request['caller'] = 1

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

            result = self.client.request("G7TransmitterSimulatorService", "SaveG7TransmitterSimulatorState", self.request)
            print(result)
