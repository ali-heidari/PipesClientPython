from abc import ABC, abstractmethod
import requests
import json
import socketio
import asyncio
from component.socket_namespace import SocketNamespace


class Client(ABC):
    '''
    Abstract class for clients 
    '''

    def __init__(self, name):
        self.init()
        self.name = name
        self.sio = socketio.Client()
        self.__pipes__ = {"name": name}
        self.responses = []

    @abstractmethod
    def init(self):
        pass

    def establish_connection(self):
        token = self.connect()
        if not token:
            raise ValueError("No token received.")
        self.sio.connect('http://localhost:3000/?name='+self.name,
                         headers={'authorization': token}, transports='polling')
        self.sio.register_namespace(
            SocketNamespace('', lambda: self.__pipes__))

    def connect(self):
        '''
        Connect to PipesHub server and ask a token to establish socket connection
        '''

        r = requests.post("http://localhost:16916/auth",
                          data={'name': 'guest'})

        if r.status_code == 200:
            return r.text
        return None

    async def ask(self, unitId, operation, input):
        '''
        Send a request to other unit and delivers the result

        @param {*} unitId The receiver unit id
        @param {*} operation Id or name of operation on other side
        @param {*} input Input data receiver needs to run operation
        '''

        self.sio.emit('gateway',  {
            "senderId": self.name,
            "receiverId": unitId,
            "operation": operation,
            "input": input,
            "awaiting": True
        })

        self.sio.on('responseGateway', lambda x: self.responses.append(x))
        filteredResponse = []
        while len(filteredResponse) < 1:
            try:
                filteredResponse = list(filter(
                    lambda x: x["receiverId"] == unitId and x["operation"] == operation, self.responses))
            except ValueError:
                pass
            await asyncio.sleep(0.01)
        self.responses.remove(filteredResponse[0])
        return filteredResponse[0]

    def request(self, unitId, operation, input):
        '''
            Send a request to other unit and no result expected
            @param {*} unitId The receiver unit id
            @param {*} operation Id or name of operation on other side
            @param {*} input Input data receiver needs to run operation
        '''
        self.sio.emit('gateway', {
            "senderId": self.name,
            "receiverId": unitId,
            "operation": operation,
            "input": input,
            "awaiting": False
        })

    def add(self, funcName, handler):
        '''
            Add a function to global __pipes prototype
            @param {*} funcName A name for operation
            @param {*} handler Operation body
        '''

        if self.__pipes__.__contains__(funcName):
            raise KeyError('This function already exists.')
        self.__pipes__[funcName] = handler
