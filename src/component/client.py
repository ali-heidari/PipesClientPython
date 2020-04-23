from abc import ABC, abstractmethod
import requests
import json
import socketio


class Client(ABC):
    '''
    Abstract class for clients 
    '''

    sio = socketio.Client()

    def __init__(self, name):
        self.init()
        self.name = name

    @abstractmethod
    def init(self):
        pass

    def establish_connection(self):
        token = self.connect()
        if not token:
            raise ValueError("No token received.")
        self.sio.connect('http://localhost:3000/?name='+self.name,
                         headers={'authorization': token}, transports='polling')
        self.sio.emit('gateway',  {
            "senderId": self.name,
            "receiverId": 'unitId',
            "operation": 'operation',
            "input": 'input',
            "awaiting": 'false'
        })

    def connect(self):
        '''
        Connect to PipesHub server and ask a token to establish socket connection
        '''

        r = requests.post("http://localhost:16916/auth",
                          data={'name': 'guest'})

        if r.status_code == 200:
            return r.text
        return None

    @sio.event
    def socket_connect(self):
        print('connection established')

    @sio.event
    def socket_responseGateway(self, data):
        print('message received with ', data)

    @sio.event
    def socket_disconnect(self):
        print('disconnected from server')
