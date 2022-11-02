from grpc_requests import Client
from apython.utils import get_egv_from_log


SERVICE = 'TransmitterSimulatorService'


class D1Pake:
    def __init__(self, address, transmitter_id):
        self.client = Client.get_by_endpoint("localhost:44444")
        self.state = dict()
        self.state['transmitterId'] = transmitter_id
        self.state['commInterval'] = 0
        self.state["supportedType"] = "DEXCOM_ONE_2019"

        self.request = dict()
        self.request['address'] = address
        # self.request['caller'] = 2
        self.request['caller'] = "CLIENT"

        self.egv_request = dict()
        self.egv_request['address'] = address
        self.egv_request['transmitterId'] = transmitter_id

    def get_egv(self):
        """
        Get nothing for this API
        :return:
        """
        result = self.client.request(SERVICE, "GetCommunicatedEGV", self.egv_request)
        print(type(result))
        # print('Result from API {}'.format(result))
        if result:  # not empty
            egvs = result['communicatedEGV']
            last_egv = egvs[-1]
            return last_egv['egv']
        else:  # use log
            result = get_egv_from_log()
            return result

    def get_state(self):
        """
        Get nothing from API
        :return:
        """
        result = self.client.request(SERVICE, 'GetTransmitterSimulatorState')
        print(result)
        return result

    def save_state(self, state_string):
        """
        Save state with string input:
            START_ADVERTISING(0),
            STOP_ADVERTISING(1),
            PAUSE_ADVERTISING(2),
            UNRECOGNIZED(-1);
        :param state_string:
        :return:
        """
        # states = [0, 1, 2]
        states = ['START_ADVERTISING', 'STOP_ADVERTISING', 'PAUSE_ADVERTISING']
        if state_string not in states:
            print('!!!!!!!!!!! Invalid state')
        else:
            self.state['advertisingState'] = state_string
            self.request['transmitterSimulatorState'] = self.state
            # D1 has upper case SaveT
            result = self.client.request(SERVICE, "SaveTransmitterSimulatorState", self.request)
            print(result)
