import threading
import datetime
import asyncio
from component.app import ClientApp
from component.service import ClientService

ca = ClientApp('cAppPy')
ca.establish_connection()

cs = ClientService('cServicePy')
cs.establish_connection()
cs.add('sum', lambda args: args["pushResponse"](args["a"] + args["b"]))
theList = []
cs.add('add', lambda args: theList.append(args["a"]))
cs.add('list', lambda args: args["pushResponse"](theList))


def setInterval(func,time,args):
    e = threading.Event()
    while not e.wait(time):
        func(args)

cs.add('message', lambda args:setInterval(lambda args:args["pushResponse"]("Time is " + str(datetime.datetime.now())),5,args))


async def tests():
    res = await ca.ask(unitId='cServicePy', operation='sum', input={'a': 5, 'b': 6})
    print("The sum is "+str(res["res"]))

    ca.request('cServicePy', 'add', {
        "a": 555
    })
    ca.request('cServicePy', 'add', {
        "a": "test"
    })

    res = await ca.ask('cServicePy', 'list', None)
    print("The list is "+str(res["res"]))

    ca.persist('cServicePy', 'message', None,lambda data: print(data["res"]));


futures = [tests()]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(futures))
# Python 3.7+
# asyncio.run()
