from abc import ABC, abstractmethod
import requests
import json

class Client(ABC):
    '''
    Abstract class for clients 
    '''

    def __init__(self):
        self.init()

    @abstractmethod
    def init(self):
        pass


    def establish_connection(self):
        self.connect()

    def connect(self):
        '''
        Connect to PipesHub server and ask a token to establish socket connection
        '''


        r = requests.post("http://localhost:16916/auth", data={'name': 'guest'})

        print(r.text)