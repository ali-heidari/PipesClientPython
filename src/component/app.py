from .client import Client

class App(Client):
    '''
    Client example of consumer app 
    '''

    def __init__(self,name):
        super().__init__(name)

    def init(self):
        pass

