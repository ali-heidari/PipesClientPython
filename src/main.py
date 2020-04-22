import socketio

sio = socketio.Client()


@sio.event
def connect():
    print('connection established')


@sio.event
def responseGateway(data):
    print('message received with ', data)


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://localhost:16916')
sio.emit('gateway',  {
    "senderId": 'this.name',
    "receiverId": 'unitId',
    "operation": 'operation',
    "input": 'input',
    "awaiting": 'false'
})
