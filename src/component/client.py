from abc import ABC, abstractmethod

class BaseComponent(ABC):
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
        pass