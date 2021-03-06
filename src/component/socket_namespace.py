import copy
import socketio


class SocketNamespace(socketio.ClientNamespace):

    def __init__(self, namespace=None, getPipes=None):
        super().__init__(namespace=namespace)
        self.getPipes = getPipes

    def on_connect(self):
        print('connection established')

    def send_response(self, data, res):
        data["res"] = res
        dataToSend = copy.deepcopy(data)
        dataToSend["input"].pop("pushResponse", None)
        self.emit('responseGateway', dataToSend)

    def on_gateway(self, data):
        if isinstance(data, dict):
            if data["receiverId"] != self.getPipes()["name"]:
                data["res"] = "I am not who you looking for :)"
            else:
                if data["awaiting"]:
                    if not data["input"]:
                        data["input"] = {}

                data["input"]["pushResponse"] = lambda res: self.send_response(
                    data, res)
                self.getPipes()[data["operation"]](data["input"])

    def on_disconnect(self):
        print('disconnected from server')
