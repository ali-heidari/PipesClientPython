from .client import Client

class ClientService(Client):
    '''
    Client example of service 
    '''

    def init(self):
        print('Service init')

