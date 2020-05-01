
from component.app import ClientApp
from component.service import ClientService

ca = ClientApp('cAppPy')
ca.establish_connection()



cs = ClientService('cServicePy');
cs.establish_connection()
cs.add('sum', lambda args: args["pushResponse"](args["a"] + args["b"]));
theList = []
cs.add('add', lambda args: theList.append(args["a"]));
cs.add('list', lambda args: args["pushResponse"](theList));



ca.ask(unitId='cServicePy', operation='sum', input={'a': 5, 'b': 6})
ca.request('cServicePy', 'add', {
    "a": 555
});
ca.request('cServicePy', 'add', {
    "a": "test"
});

ca.ask('cServicePy', 'list', None);
