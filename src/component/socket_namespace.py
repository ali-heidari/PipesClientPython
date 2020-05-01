

import socketio

class SocketNamespace(socketio.ClientNamespace):
    
    def on_connect(self):
        print('connection established')

    def on_responseGateway(self, data):
        print('message received with ', data)

    def on_gateway(self, data):
        print('message received with ', data)

    def on_disconnect(self):
        print('disconnected from server')